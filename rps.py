# rps.py
# Description: RPS vs Bot
# Authors:
#   Andrew Sadahiro - asadahiro1@seattleu.edu
#   Edrich Rabanes - erabanes@seattleu.edu
#   Shawna Sanjay - ssanjay2@seattleu.edu

"""ECEGR 2000 01 Final Project - Group 4
Andrew Sadahiro, Edrich Rabanes, Shawna Sanjay

This project uses a single raspberry pi, this code, an ADS1115, and 2 flex sensors (along with a mess of wires and resistors)
to allow someone to play Rock Paper Scissors against a bot, at varying difficulties. An LCD screen will display a countdown,
after which the code will check which sign the player has thrown. The result of the game will be shown on the LCD. A buzzer will
also make corresponding beeps, based on the outcome, and for the countdown before the game.

Simply attach the flex sensors to your fingers (any two fingers that aren't both flexed/not flexed when making a scissors), and throw a sign
by the time the countdown is done.

Below are the config settings. You can leave them as they are, or modify them to adjust your experience.
use rps_callibration.py to callibrate if its consistently misreading inputs

"""

# ===CONFIG===

# Toggle debug print statements
DEBUG = True

# Toggle Sound
SOUND = False

# Countdown Timer (seconds)
TIMER = 4

# Delay between games (seconds)
GAME_DELAY = 2


DIFFICULTY = 'Hard' #'Easy' or 'Hard'

# use rps_callibration.py to get these
FLEX_VAL = 24598
UNFLEX_VAL = 21948

# ============


import time
import random
from collections import Counter
import board
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

from gpiozero import OutputDevice
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone



# === BUZZER ===
# By Shawna
# Initialize Buzzer
tb = TonalBuzzer(4)

tA3 = Tone(note= "A3")
tA4 = Tone(note= "A#4")
tA5 = Tone(note= "A5")
tC4 = Tone(note= "C4")
tC5 = Tone(note= "C5")
tE4 = Tone(note= "E4")
tF4 = Tone(note= "F4")

def lose_sfx():
    tb.play(tC4)
    time.sleep(0.1)
    tb.play(tF4)
    time.sleep(0.5)
    tb.play(tF4)
    time.sleep(0.5)
    tb.stop()
    
def win_sfx():
    tb.play(tA3)
    time.sleep(0.1)
    tb.play(tC5)
    time.sleep(0.1)
    tb.play(tC5)
    time.sleep(0.3)
    tb.play(tA4)
    time.sleep(0.5)
    tb.play(tA3)
    tb.stop()
    
def tie_sfx():
    tb.play(tE4)
    time.sleep(0.5)
    tb.stop()

# ==============



# === LCD ===
# By Edrich
LCD_RS = OutputDevice(25)
LCD_E = OutputDevice(24)
LCD_D4 = OutputDevice(23)
LCD_D5 = OutputDevice(18)
LCD_D6 = OutputDevice(27)
LCD_D7 = OutputDevice(17)

LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

E_PULSE = 0.0005
E_DELAY = 0.0005

def lcd_init():
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    time.sleep(E_DELAY)
    
def lcd_byte(bits, mode):
    LCD_RS.value = mode

    # HIGH nibble
    LCD_D4.value = 1 if bits & 0x10 else 0
    LCD_D5.value = 1 if bits & 0x20 else 0
    LCD_D6.value = 1 if bits & 0x40 else 0
    LCD_D7.value = 1 if bits & 0x80 else 0
    lcd_toggle_enable()

    # LOW nibble
    LCD_D4.value = 1 if bits & 0x01 else 0
    LCD_D5.value = 1 if bits & 0x02 else 0
    LCD_D6.value = 1 if bits & 0x04 else 0
    LCD_D7.value = 1 if bits & 0x08 else 0
    lcd_toggle_enable()
    
def lcd_toggle_enable():
    time.sleep(E_DELAY)
    LCD_E.on()
    time.sleep(E_PULSE)
    LCD_E.off()
    time.sleep(E_DELAY)
    
def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH, " ")
    
    lcd_byte(line, LCD_CMD)
    
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)
        
lcd_init()
# ===========






# Create the I2C bus
i2c = board.I2C()
# Create the ADC object using the I2C bus
ads = ADS1115(i2c)

# initialize sign tuple
sign = ('Rock', 'Paper', 'Scissors')

# matchup dicts
wins_against = {
    'Rock': 'Scissors',
    'Paper': 'Rock',
    'Scissors': 'Paper'
}

loses_against = {
    'Rock': 'Paper',
    'Paper': 'Scissors',
    'Scissors': 'Rock'
}

# initialize list for tracking player input
input_list = []

# score tracking variables
p_score = 0 #player
b_score = 0 #bot

# Two flex sensors on A0 and A1
flex1 = AnalogIn(ads, ads1x15.Pin.A0)
flex2 = AnalogIn(ads, ads1x15.Pin.A1)

# threshold that determines if sensor if flexed or not
FLEX_DIFF = abs(FLEX_VAL - UNFLEX_VAL)

#is flexed variables - False -> not flex, True -> flexed
flex1_status = False
flex2_status = False
                 
# uses atleast 2 flex sensors to detect sign held when func called
# returns a string from sign list
def get_input():
    global input_list, flex1, flex2, flex1_status, flex2_status, DEBUG
       
    #determine if sensors are flexed beyond threshold or not
    if (abs(flex1.value - FLEX_VAL))<=FLEX_DIFF:
        flex1_status = True
    else:
        flex1_status = False
        
    if (abs(flex2.value - FLEX_VAL))<=FLEX_DIFF:
        flex2_status = True
    else:
        flex2_status = False
    
    
    #if sensor 1 != sensor 2 -> scissor
    #if both = flex -> rock
    # if both != flex -> paper
    
    if flex1_status != flex2_status:
        x = 2 #Scissors
    else: #flex1_status == flex2_status
        if (abs(flex1.value - FLEX_VAL))<=FLEX_DIFF:
            x = 0 #Rock
        else: #flex1.value >= FLEX_THRESHOLD   
            x = 1 #Paper
    
    if DEBUG:
        print("Flex1:", flex1.value, "Flex2:", flex2.value)
    
    input_list.append(sign[x])
    return sign[x]



# gets the bot's move
# intakes string 'Easy' or 'Hard' to determine how move is chosen
# returns a string from sign list
def get_bot(difficulty):
    global input_list, loses_against, DEBUG
    
    if difficulty == 'Easy':
        return sign[random.randint(0,2)]
    
    if difficulty == 'Hard':
        #use input_list to find pattern in player input, predict what happens next

        c = Counter(input_list)
        common = c.most_common(1)[0][0] # most common input

        if DEBUG:
            print('Input List:',input_list)
            print('Predicted:',common)
            print('Will PLay:',loses_against[common])
        
        c.clear()
        return loses_against[common]

# handle game conclusion
# takes in string (outcome) that tells it what to do
# keeps track of score
# does LCD display (WIP)
def game_conc(outcome):
    global p_score, b_score
    if outcome == "Tie":
        print("Tie")
        if SOUND:
            tie_sfx()
        lcd_string("   ITS A", LCD_LINE_1)
        lcd_string("    TIE", LCD_LINE_2)
    elif outcome == "Win":
        print("You Win")
        p_score += 1
        if SOUND:
            win_sfx()
        lcd_string("      YOU", LCD_LINE_1)
        lcd_string("      WIN   :D", LCD_LINE_2)
    elif outcome == "Lose":
        print("You Lose")
        b_score += 1
        if SOUND:
            lose_sfx()
        lcd_string("      YOU", LCD_LINE_1)
        lcd_string("      LOSE   :(", LCD_LINE_2)
    print(f'\n    ==Score Board==\nPlayer = {p_score} | Computer = {b_score}\n')
    
# main game function
# checks player input after countdown
def play_game():
    global TIMER
    timer = TIMER
    for i in range(TIMER):
        timer -= 1
        if timer == 0:
            if SOUND:
                tb.play(tC5)
                time.sleep(0.1)
                tb.stop()
            lcd_string("       GO!", LCD_LINE_1)
            lcd_string("", LCD_LINE_2)
            print('Go!')
        else:
            if SOUND:
                tb.play(tE4)
                time.sleep(0.1)
                tb.stop()
            lcd_string(f"       {timer}", LCD_LINE_1)
            lcd_string("", LCD_LINE_2)
            print(timer)
        time.sleep(1)
        
    #compare input vs AI
    player_move = get_input()
    bot_move = get_bot(DIFFICULTY)
    
    print(f"Player played {player_move}, Bot played {bot_move}")
    lcd_string(f"     {player_move} vs", LCD_LINE_1)
    lcd_string(f"      {bot_move}", LCD_LINE_2)
    time.sleep(1)
    
    #tie
    if bot_move == player_move:
        game_conc("Tie")
    #player lose
    elif wins_against[bot_move] == player_move:
        game_conc("Lose")
    #player win
    else:
        game_conc("Win")
        
    time.sleep(GAME_DELAY)
    
    
    
x = 1
while x == 1:
    try:
        play_game()
    except Exception as e:
        print(f"Error: {e}")
        
        
        


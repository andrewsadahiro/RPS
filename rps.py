# rps.py
# Description: RPS vs Bot
# Author: Andrew Sadahiro - asadahiro1@seattleu.edu


"""ECEGR 2000 01 Final Project - Group 4
Edrich Rabanes, Andrew Sadahiro, Shawna Sanjay

This project uses a single raspberry pi, this code, an ADS1115, and 2 flex sensors (along with a mess of wires and resistors)
to allow someone to play Rock Paper Scissors against a bot, at varying difficulties. An LCD screen will display a countdown,
after which the code will check which sign the player has thrown. The result of the game will be shown on the LCD.

Simply attach the flex sensors to your fingers (any two fingers that aren't both flexed/not flexed when making a scissors), and throw a sign
by the time the countdown is done.

Below are the config settings. You can leave them as they are, or modify them to adjust your experience.

"""

# ===CONFIG===

# Toggle debug print statements
DEBUG = True

# Toggle Sound
SOUND = True

# Countdown Timer
TIMER = 4

# Delay between games
GAME_DELAY = 2


DIFFICULTY = 'Hard' #'Easy' or 'Hard'

# ============


import time
import random
from collections import Counter
import board
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

from gpiozero import OutputDevice
from gpiozero import TonalBuzzer



# === BUZZER ===
# Initialize Buzzer
b = TonalBuzzer(4) #GPIO pin 4
 # simplified tone function
def bplay(tone):
    b.play(tone)
    time.sleep(0.2)
    b.stop()
    
def win_sfx():
    bplay("B3") 
    bplay("A4")
    
def lose_sfx():
    bplay("A4")
    bplay("B3")
    
def tie_sfx():
    bplay("E4")

# ==============



# === LCD ===
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
FLEX_THRESHOLD = 21000 #FIX THIS
                 
#is flexed variables - False -> not flex, True -> flexed
flex1_status = False
flex2_status = False
                 
# uses atleast 2 flex sensors to detect sign held when func called
# returns a string from sign list
def get_input():
    global input_list, flex1, flex2, flex1_status, flex2_status, DEBUG
       
    #determine if sensors are flexed beyond threshold or not
    if flex1.value <= FLEX_THRESHOLD:
        flex1_status = True
    else:
        flex1_status = False
        
    if flex2.value <= FLEX_THRESHOLD:
        flex2_status = True
    else:
        flex2_status = False
    
    
    
    #if sensor 1 != sensor 2 -> scissor
    #if both = flex -> rock
    # if both != flex -> paper
    
    if flex1_status != flex2_status:
        x = 2 #Scissors
    else: #flex1_status == flex2_status
        if flex1.value > FLEX_THRESHOLD:
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
    #LCD Placeholder Function
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
        lcd_string("      WIN", LCD_LINE_2)
    elif outcome == "Lose":
        print("You Lose")
        b_score += 1
        if SOUND:
            lose_sfx()
        lcd_string("      YOU", LCD_LINE_1)
        lcd_string("      LOSE", LCD_LINE_2)
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
                print() #TODO
            print('Go!')
        else:
            if SOUND:
                print() #TODO
            print(timer)
        time.sleep(1)
        
    #compare input vs AI
    player_move = get_input()
    bot_move = get_bot(DIFFICULTY)
    
    print(f"Player played {player_move}, Bot played {bot_move}")
    
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
    
    
    
    
while True:
    try:
        play_game()
    except:
        print("Error")

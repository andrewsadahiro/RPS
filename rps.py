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
DEBUG = False

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
FLEX_THRESHOLD = 19000 #~20000 -> not flex, 18000 -> flex
                 
#is flexed variables - False -> not flex, True -> flexed
flex1_status = False
flex2_status = False
                 
# uses atleast 2 flex sensors to detect sign held when func called
# returns a string from sign list
def get_input():
    global input_list, flex1, flex2, flex1_status, flex2_status, DEBUG
       
    #determine if sensors are flexed beyond threshold or not
    if flex1.value >= FLEX_THRESHOLD:
        flex1_status = True
    else:
        flex1_status = False
        
    if flex2.value >= FLEX_THRESHOLD:
        flex2_status = True
    else:
        flex2_status = False
    
    
    
    #if sensor 1 != sensor 2 -> scissor
    #if both = flex -> rock
    # if both != flex -> paper
    
    if flex1_status != flex2_status:
        x = 2 #Scissors
    else: #flex1_status == flex2_status
        if flex1.value < FLEX_THRESHOLD:
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
        tie_sfx()
    elif outcome == "Win":
        print("You Win")
        p_score += 1
        win_sfx()
    elif outcome == "Lose":
        print("You Lose")
        b_score += 1
        lose_sfx()
    print(f'\n    ==Score Board==\nPlayer = {p_score} | Computer = {b_score}\n')
    
# main game function
# checks player input after countdown
def play_game():
    global TIMER
    timer = TIMER
    for i in range(TIMER):
        timer -= 1
        if timer == 0:
            print('Go!')
        else:
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

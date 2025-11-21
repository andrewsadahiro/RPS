# rps.py
# Description: RPS vs AI
# Author: Andrew Sadahiro - asadahiro1@seattleu.edu


"""ECEGR 2000 01 Final Project - Group 4
Edrich Rabanes, Andrew Sadahiro, Shawna Sanjay

This project uses a single raspberry pi, this code, an ADS1115, and 2 flex sensors (along with a mess of wires) to allow
someone to play Rock Paper Scissors against a computer, at varying difficulties.
An LCD screen will display a countdown, after which the code will check which sign the player has thrown
The result of the game will be shown on the LCD

"""

import time
import random
from collections import Counter

import board
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

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
o_score = 0 #opponent

# Toggle debut print statements
DEBUG = False


# countdown timer
TIMER = 4
GAME_DELAY = 2 # Delay between games

DIFFICULTY = 'Hard' #'Easy' or 'Hard' determines algorithm



# Two flex sensors on A0 and A1
flex1 = AnalogIn(ads, ads1x15.Pin.A0)
flex2 = AnalogIn(ads, ads1x15.Pin.A1)

# threshold that determines if sensor if flexed or not
FLEX_THRESHOLD = 19000 #~20000 -> not flex, 18000 -> flex
                 
#is flexed variables |F -> not flex, T -> flexed
flex1_status = False
flex2_status = False
                 
# uses atleast 2 flex sensors to detect sign held when func called
# returns a string from sign list
def get_input():
    global input_list, flex1, flex2, flex1_status, flex2_status, DEBUG
       
    if flex1.value >= FLEX_THRESHOLD:
        flex1_status = True
    else:
        flex1_status = False
        
    if flex2.value >= FLEX_THRESHOLD:
        flex2_status = True
    else:
        flex2_status = False
    
    
    
    #if sensor 1 = flex, sensor 2 != flex -> scissor
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


# gets the opponent's move
# intakes string 'Easy' or 'Hard' to determine how move is chosen
# returns a string from sign list
def get_opponent(difficulty):
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
    global p_score, o_score
    #LCD Placeholder Function
    if outcome == "Tie":
        print("Tie")
    elif outcome == "Win":
        print("You Win")
        p_score += 1
    elif outcome == "Lose":
        print("You Lose")
        o_score += 1
    print(f'\n    ==Score Board==\nPlayer = {p_score} | Computer = {o_score}\n')
    
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
    opp_move = get_opponent(DIFFICULTY)
    
    print(f"Player played {player_move}, Opponent played {opp_move}")
    
    #tie
    if opp_move == player_move:
        game_conc("Tie")
    #player lose
    elif wins_against[opp_move] == player_move:
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

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
import gpiozero as GPIO
import random

sign = ['Rock', 'Paper', 'Scissors']


TIMER = 4

input_list = []


# uses atleast 2 flex sensors to detect sign held when func called
# returns a string from sign list
def get_input():
    global input_list
    x = 1 #placeholder
    
    #use flex sensors to get sign
    
    
    #if sensor 1 = flex, sensor 2 != flex -> scissor
    #if both = flex -> rock
    # if both != flex -> paper
    
    input_list.append(sign[x])
    return sign[x]


# gets the opponent's move
# intakes string 'Easy' or 'Hard' to determine how move is chosen
# returns a string from sign list
def get_opponent(difficulty):
    global input_list
    
    if difficulty == 'Easy':
        return sign[random.randint(0,2)]
    
    if difficulty == 'Hard':
        #insert AI here
        
        #use input_list to find pattern in player input, try and predict what happens next
        pass
    

# determines winner  
# intakes two strings, opponent's move, and player's move 
# calls game_conc function after determining winner
# references dict

wins_against = {
    'Rock': 'Scissors',
    'Paper': 'Rock',
    'Scissors': 'Paper'
}


def get_winner(opp_move, player_move):
    
    #tie
    if opp_move == player_move:
        game_conc("Tie")
    #player lose
    elif wins_against[opp_move] == player_move:
        game_conc("Lose")
    #player win
    else:
        game_conc("Win")
    

# takes in string from get_winner
# displays win/lost on LCD screen
# buzzer(?)


def game_conc(outcome):
    print(f"Player played {player_move}, Opponent played {opp_move}")
    if outcome == "Tie":
        print("Tie")
    elif outcome == "Win":
        print("Win")
    elif outcome == "Lose":
        print("Lose")
    
# main game function
# checks player input after countdown
def play_game():
    global TIMER
    timer = TIMER
    for i in range(TIMER):
        timer -= 1
        print(timer)
        time.sleep(1)
    #compare input vs AI
    get_winner(get_opponent('Easy'),get_input())



play_game()
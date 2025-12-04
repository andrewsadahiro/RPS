#buzzer_test.py
#Description: Creating the sound for winning and losing

import RPi.GPIO as GPIO
from time import sleep
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone

tb = TonalBuzzer(23)
tA3 = Tone(note= "A3")
tA4 = Tone(note= "A#4")
tA5 = Tone(note= "A5")
tC4 = Tone(note= "C4")
tC5 = Tone(note= "C5")
tF4 = Tone(note= "F4")

def lose_sfx():
    print("You Lose")
    tb.play(tC4)
    sleep(0.1)
    tb.play(tF4)
    sleep(0.5)
    tb.play(tF4)
    sleep(0.5)
    tb.stop()
    
def win_sfx():
    print("You Win")
    tb.play(tA3)
    sleep(0.1)
    tb.play(tC5)
    sleep(0.1)
    tb.play(tC5)
    sleep(0.3)
    tb.play(tA4)
    sleep(0.5)
    tb.play(tA3)
    tb.stop()
    

try:
    game_won = False

    if game_won:
        win_sfx()
    else:
        lose_sfx()
    sleep(1)
    
except KeyboardInterrupt:
    print("Exiting...")

finally:
    pass

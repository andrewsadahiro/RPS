from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import time

b = TonalBuzzer(4) #GPIO pin 4

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

tie_sfx()
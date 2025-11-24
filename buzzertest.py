from gpiozero import TonalBuzzer
from gpiozero.tones import Tone

b = TonalBuzzer(4) #GPIO pin 4


b.play("A4")
time.sleep(0.1)
b.stop()

time.sleep(1)

b.play("B4")
time.sleep(0.1)
b.stop()
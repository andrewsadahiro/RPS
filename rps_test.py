import time

import board

from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

# Create the I2C bus
i2c = board.I2C()

# Create the ADC object using the I2C bus
ads = ADS1115(i2c)

    
    
# Two flex sensors on A0 and A1
flex1 = AnalogIn(ads, ads1x15.Pin.A0)
flex2 = AnalogIn(ads, ads1x15.Pin.A1)

while True:
    print("Flex1:", flex1.value, "Flex2:", flex2.value)
    time.sleep(0.5)

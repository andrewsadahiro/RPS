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

unflex_ave = []
flex_ave = []

def callibrate():
    print("DO NOT FLEX SENSORS")
    for i in range(10):
        print("Flex1:", flex1.value, "Flex2:", flex2.value)
        time.sleep(0.5)
        unflex_ave.append(flex1.value)
        unflex_ave.append(flex2.value)

    print("PREPARE TO FLEX SENSORS")

    time.sleep(3)

    print("FLEX SENSORS")
    for i in range(10):
        print("Flex1:", flex1.value, "Flex2:", flex2.value)
        time.sleep(0.5)
        flex_ave.append(flex1.value)
        flex_ave.append(flex2.value)

    unflex_ave_val = sum(unflex_ave)/len(unflex_ave)

    print(f"Average Unflex Value: {unflex_ave_val}")

    flex_ave_val = sum(flex_ave)/len(flex_ave)

    print(f"Average flex Value: {flex_ave_val}")

    FLEX_VAL = flex_ave_val
    UNFLEX_VAL = unflex_ave_val


FLEX_VAL = 24598
UNFLEX_VAL = 21948

FLEX_DIFF = abs(FLEX_VAL - UNFLEX_VAL)

print(FLEX_DIFF)

print("flex val")
print(flex2.value)

print("flex dif")
print(abs(flex2.value - UNFLEX_VAL))


if (abs(flex2.value - FLEX_VAL))<=FLEX_DIFF:
    flex2_status = True
else:
    flex2_status = False

print(flex2_status)

from gpiozero import OutputDevice
from time import sleep

LCD_RS = OutputDevice(25)
LCD_E = OutputDevice(24)
LCD_D4 = OutputDevice(23)
LCD_D5 = OutputDevice(18)
LCD_D6 = OutputDevice(15)
LCD_D7 = OutputDevice(14)

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
    sleep(E_DELAY)
    
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
    sleep(E_DELAY)
    LCD_E.on()
    sleep(E_PULSE)
    LCD_E.off()
    sleep(E_DELAY)
    
def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH, " ")
    
    lcd_byte(line, LCD_CMD)
    
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)
        
lcd_init()
lcd_string("HI", LCD_LINE_1)
lcd_string("MEOWW", LCD_LINE_2)

    

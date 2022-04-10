from pyb import RTC
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import sys
print(sys.path)

week = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
time = ['', '', '']
i2c = I2C(sda=Pin("Y8"), scl=Pin("Y6"))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)
rtc = RTC()
if rtc.datetime()[0] != 2022:
    rtc.datetime((2022, 3, 24, 4, 21, 37, 0, 0))
while True:
    datetime = rtc.datetime()  
    oled.fill(0)
    oled.text('chvos', 0, 0)
    oled.text('RTC Clock', 0, 15) 
    oled.text(str(datetime[0]) + '-' + str(datetime[1]) + '-' + str(datetime[2]) + ' ' + week[(datetime[3] - 1)], 0, 40)
    for i in range(4, 7):
        if datetime[i] < 10:
            time[i - 4] = "0"
        else:
            time[i - 4] = ""
    oled.text(time[0] + str(datetime[4]) + ':' + time[1] + str(datetime[5]) + ':' + time[2] + str(datetime[6]), 0, 55)
    oled.show()
    pyb.delay(300)
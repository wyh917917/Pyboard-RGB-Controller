import pyb
from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C
from onewire import OneWire
from ds18x20 import DS18X20
from dht import DHT11
from RGB.ws2812 import WS2812
from RGB.colors import *

# 初始化OLED
i2c = SoftI2C(sda=Pin("Y8"), scl=Pin("Y6"))
oled = SSD1306_I2C(128, 64, i2c)
# 初始化按键
sw = pyb.Switch()  # 定义按键对象名字为sw
# 初始化内部三轴加速度传感器
accel = pyb.Accel()
# 初始化ADC,Pin='X7'
adc = pyb.ADC('X7')
# 初始化DAC,输出引脚为'X5'
dac = pyb.DAC(1)
# 定义8位精度下方波的值。0、255分别对应输出0V、3.3V。需要定义成字节数组。
buf = bytearray(2)
buf[0] = 0
buf[1] = 255
# 初始化DS18B20
ow = OneWire(Pin('X11'))  # 使能单总线
ds = DS18X20(ow)  # 传感器是DS18B20
rom = ds.scan()  # 扫描单总线上的传感器地址，支持多个传感器同时连接
# 初始化DHT11
dt = DHT11(Pin('X12'))  # 'X20'连接到开发板上的DHT11
# 定义灯带连接引脚，Y11接口
LED = Pin('Y11', Pin.OUT, value=0)
# 构建RGB灯带对象,定义控制引脚和灯珠数量
ring = WS2812(spi_bus=LED, led_count=17)
key_node = 0  # 按键标志位
currenct_temp = 0


def print_temp():
    global currenct_temp
    oled.fill(0)  # 清屏显示黑色背景
    ds.convert_temp()  # 温度采集转换
    currenct_temp = ds.read_temp(rom[0])  # 温度显示,rom[0]为第1个DS18B20

    oled.text(str('%.2f' % currenct_temp) + ' C', 0, 20)  # 显示temp,保留2位小数
    oled.show()


def oled_show_center(text):
    oled.fill(0)
    oled.text(text, 64, 32)
    oled.show()


def breath_light(rate=100, delay=15, delay_peak=800):
    intensify = 0
    interval = 1 / rate
    for i in range(rate):
        intensify += interval
        intensify = round(intensify, 2)
        ring.set_intensity(intensify)
        ring.show(fill_color(RED))
        pyb.delay(delay)
        print(str(intensify))
    pyb.delay(delay_peak)
    for i in range(rate):
        intensify -= interval
        intensify = round(intensify, 2)
        ring.set_intensity(intensify)
        ring.show(fill_color(RED))
        pyb.delay(delay)
        print(str(intensify))
    pyb.delay(delay_peak)


def light(intensify=0):
    ring.set_intensity(intensify)
    ring.show(fill_color(RED))


def light_off():
    ring.show(fill_color(EMPTY))
    global key_node
    key_node = 2


def fill_color(color):
    data = []
    for i in range(ring.led_count):
        data.append(color)
    return data


def key():
    global key_node
    if key_node == 1:
        key_node = 0
    elif key_node == 0 | key_node == 2:
        key_node = 1


sw.callback(key)  # 当按键被按下时，执行函数key()
while True:
    print_temp()
    if key_node == 1:
        print("trun on light")
        if currenct_temp < 40:
            currenct_temp = round(currenct_temp)
            light(intensify=currenct_temp * 0.025)
        elif currenct_temp >= 40:
            breath_light()
    elif key_node == 0:
        print("trun off light")
        light_off()

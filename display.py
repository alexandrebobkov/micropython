from machine import Pin, SoftI2C
import ssd1306

i2c = SoftI2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

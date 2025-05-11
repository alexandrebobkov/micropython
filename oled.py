import machine, ssd1306

i2c = machine.SoftI2C(scl=machine.Pin(5), sda=machine.Pin(4), freq=200000)
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

oled.fill(1)
oled.show()
oled.fill(0)
oled.text("Hi Foxie!", 0, 0, 1)
oled.text("Wolfie loves you!", 0, 12, 1)
oled.show()
#machine.SoftI2C.scan(i2c)
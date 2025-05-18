# Very simple script to blink LED and output info about ESP32

import esp, esp32, time, os, _thread
from machine import Pin, SoftI2C

# An infinite loop thread to blink LED
def status_led():
    # Blink pattern blink-blink-pause
    while True:
        led.value(1)
        time.sleep_ms(250)
        led.value(0)
        time.sleep_ms(250)
        led.value(1)
        time.sleep_ms(250)
        led.value(0)
        time.sleep_ms(750)
        
def connect_wifi():
    import network
    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('IoT_bots', '208208208')
        while not wlan.isconnected():
            pass
    print('Network Config:', wlan.ipconfig('addr4'))

# Display information about ESP32S3 module
print("=====================================\n")
print(os.uname())
print("\n=====================================")
print("Flash size: ", esp.flash_size()/1024/1024, "Mb")
#rint("MCU Temperature: ", esp32.mcu_temperature(), "C")
print("MCU Temperature: {:4.1f} C".format(esp32.mcu_temperature()))

connect_wifi()

# Configure LED pin and start the blinky loop thread
#led = Pin(45, Pin.OUT)
#led.value(0)
#_thread.start_new_thread(status_led, ())
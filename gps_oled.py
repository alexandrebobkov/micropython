# Obtains location coordinates from GPS module and displays them on the OLED display
# Alexander B.


from machine import Pin, SoftI2C, UART
from machine import Timer
from utime import sleep_ms

import network, ssd1306, esp32, _thread, time, utime

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
networks = wlan.scan()

ONBOARD_LED = 10	# GPIO10, PIN 7
ONBOARD_BTN = 3		# GPIO3, 13

# Configure on-board LED and push button
# Stated GPIOs correspond to the wiring schematic
onboard_led = Pin(ONBOARD_LED, Pin.OUT)
onboard_button = Pin(ONBOARD_BTN, Pin.IN, Pin.PULL_UP)

# Configure OLED 0.91" display
i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=200000)
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

# Configure GPS module
# GPIO 6 -> Green; GPIO 7 -> Red
# SCL -> Blue; SDA -> Black
gpsModule = UART(1, baudrate=9600, tx=Pin(7), rx=Pin(6))
buff = bytearray(255)
latitude = ""
longtitude = ""
satellites = ""
GPStime = ""
TIMEOUT = False
FIX_STATUS = False

# Interrupt function to alternate on-board LED state
def led_interrupt(t):
    onboard_led.value(not onboard_led.value())
    oled.fill(0)
    oled.text("Core Temp: " +str(esp32.mcu_temperature()), 0, 12, 1);
    oled.show()
    print("Core Temp: ",esp32.mcu_temperature(), "C")
    ##print(gpsModule.read())
    #getGPSInfo(gpsModule)
    
def info_interrupt(t):
    oled.fill(0)
    oled.text("Temp: " +str(esp32.mcu_temperature()), 0, 12, 1);
    oled.show()    
    #print(gpsModule)
  
# Interrupt function to turn LED ON when on-board button is pressed
def button_interrupt(pin):
    print("Button was pressed")    
    onboard_led.value(1)
    oled.fill(0)
    oled.text(network.hostname(), 0, 0, 1)
    oled.text("Wi-Fi: " +wlan.config('ssid'), 0, 12, 1)
        #oled.text("Channel: " +str(wlan.config('channel')), 0, 24, 1)
    oled.text("IP: " +str(wlan.ifconfig()[0]), 0, 24, 1)
    oled.contrast(32)
    oled.show()
    sleep_ms(500)
    
def getGPSInfo(gpsModule):
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, GPStime
    #print(gpsModule.readline())
    print("Reading GPS info")
    
    timeout = time.time() + 10
    
    while True:
        gpsModule.readline()
        buff = str(gpsModule.readline())
        parts = buff.split(',')
    
        if (parts[0] == "b'$GPGGA" and len(parts) == 15):
            if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                print(buff)
                
                latitude = convertToDegree(parts[2])
                if (parts[3] == 'S'):
                    latitude = "-"+latitude
                longitude = convertToDegree(parts[4])
                if (parts[5] == 'W'):
                    longitude = "-"+longitude
                satellites = parts[7]
                GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                FIX_STATUS = True
                break
                
        if (time.time() > timeout):
            TIMEOUT = True
            break
        #utime.sleep_ms(500)
        
def convertToDegree(RawDegrees):

    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return str(Converted)

def gps_info_interrupt(t):
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, GPStime
    getGPSInfo(gpsModule)
    if(FIX_STATUS == True):
        print("Printing GPS data...")
        print(" ")
        print("Latitude: "+latitude)
        print("Longitude: "+longitude)
        print("Satellites: " +satellites)
        print("Time: "+GPStime)
        print("----------------------")
        
        oled.fill(0)
        oled.text("Lat: "+latitude, 0, 0)
        oled.text("Lng: "+longitude, 0, 10)
        #oled.text("Satellites: "+satellites, 0, 20)
        oled.text("Time: "+GPStime, 0, 30)
        oled.show()
        
        FIX_STATUS = False
        
    if(TIMEOUT == True):
        print("No GPGGA GPS data is found.")
        oled.fill(0)
        oled.text("No GPS", 0, 12, 1)
        oled.show()
        TIMEOUT = False

    
def main():
    onboard_led_timer = Timer(0)
    gps_info_timer = Timer(0)
    #info_display_timer = Timer(0)
#    connect_wireless()
    # initialize oled
    oled.fill(1)
    oled.show()
    sleep_ms(250)
    oled.fill(0)
    oled.pixel(1, 31, 1)
    oled.show()
    sleep_ms(1000)
    oled.fill(0)
    oled.show()
    
    if not wlan.isconnected():
        onboard_led_timer.init(mode=Timer.PERIODIC,period=1000,callback=led_interrupt)
        gps_info_timer.init(mode=Timer.PERIODIC,period=2000,callback=gps_info_interrupt)
        #info_display_timer.init(mode=Timer.PERIODIC,period=1000,callback=info_interrupt)
        print("Connecting to Wi-Fi ...")
        wlan.connect('IoT_bots', '208208208')
    
    if wlan.isconnected():
        print("Wi-Fi: " +wlan.config('ssid'))
        print("Channel: ", wlan.config('channel'))
        print("Hostname: ", wlan.config('hostname'))
        print("IP Address: ", wlan.ifconfig()[0])
        print(esp32.mcu_temperature(), "C")
        
        #oled.text(network.hostname(), 0, 0, 1)
        #oled.text("Wi-Fi: " +wlan.config('ssid'), 0, 12, 1)
        ##oled.text("Channel: " +str(wlan.config('channel')), 0, 24, 1)
        #oled.text("IP: " +str(wlan.ifconfig()[0]), 0, 24, 1)
        #oled.contrast(32)
        #oled.show()
        onboard_led_timer.init(mode=Timer.PERIODIC,period=1000,callback=led_interrupt)
        gps_info_timer.init(mode=Timer.PERIODIC,period=2000,callback=gps_info_interrupt)
        
        #info_display_timer.init(mode=Timer.PERIODIC,period=1000,callback=info_interrupt)
 
    # Assign interrupt to the on-board push button
    onboard_button.irq(trigger=Pin.IRQ_FALLING, handler=button_interrupt)
    
    
if __name__ == '__main__':
    main()

#while True:
#    onboard_led.value(1)
#    onboard_led.value(not onboard_led.value())
#    sleep_ms(500)
#    onboard_led.value(0)
#    time.sleep(1)
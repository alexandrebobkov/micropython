import esp, esp32, time, os, _thread
from time import sleep
from machine import Pin, SoftI2C, I2C
from ina219 import INA219
#from pca9685 import PCA9685Driver

from umqtt.simple import MQTTClient
import network
import config

MQTT_SERVER = config.mqtt_server
MQTT_PORT = config.mqtt_port #1883
MQTT_CLIENT = b"esp32s3 uno"
MQTT_KEEPALIVE = 7200
MQTT_CLIENT_ID = b"1030"

MQTT_TOPIC_TEMPERATURE = 'nodes/esp32s3-uno/mcu_temp'
MQTT_TOPIC_VOLTAGE_SHUNT = 'node/esp32s3-uno/voltage_shunt'
MQTT_TOPIC_CURRENT = 'node/esp32s3-uno/current'
MQTT_TOPIC_VOLTAGE_BUS = 'node/esp32s3-uno/voltage_bus'

def initialize_wifi(ssid, password):
    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('IoT_bots', '208208208')
        while not wlan.isconnected():
            pass
    print('Network Config:', wlan.ipconfig('addr4'))
    print('Connection Status:', wlan.status())

    # Connect to the network
    #wlan.connect('IoT_bots', '208208208')

    # Wait for Wi-Fi connection
    #connection_timeout = 10
    #while connection_timeout > 0:
    #    if wlan.status() < 1010:
    #        break
    #    connection_timeout -= 1
    #    print('Waiting for Wi-Fi connection...')
    #    sleep(1)

    # Check if connection is successful
    if wlan.status() != 1010:
        return False
    else:
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])
        return True

def connect_mqtt():
    try:
        client = MQTTClient(client_id=MQTT_CLIENT_ID,
                            server=MQTT_SERVER,
                            port=MQTT_PORT,
                            #user=MQTT_USER,
                            #password=MQTT_PASSWORD,
                            keepalive=MQTT_KEEPALIVE)
        client.connect()
        return client
    except Exception as e:
        print('Error connecting to MQTT:', e)
        raise  # Re-raise the exception to see the full traceback

def publish_mqtt(topic, value):
    client.publish(topic, value)
    print(topic)
    print(value)
    print("Publish Done")

def status_led():
    while True:
        led.value(1)
        time.sleep_ms(250)
        led.value(0)
        time.sleep_ms(250)
        led.value(1)
        time.sleep_ms(250)
        led.value(0)
        time.sleep_ms(750)
        
def measure():
    while True:
        current_mA = ina.current
        voltage_V = ina.bus_voltage
        shunt_voltage_V = ina.shunt_voltage * 1000
        power_mW = current_mA * shunt_voltage_V
        #print("{:4.1f} mA {:4.2f} V shunt {:4.2f} V {:4.2f} mW ".format(current_mA, voltage_V, shunt_voltage_V, power_mW))
        #print (esp32.mcu_temperature())
        print("{:4.1f} mA {:4.2f} V shunt {:4.2f} V {:4.2f} mW {:} C".format(current_mA, voltage_V, shunt_voltage_V, power_mW, esp32.mcu_temperature()))
        time.sleep(1)
    
    
# Display information about ESP32S3 module
print(os.uname())
print("Flash size: ", esp.flash_size()/1024/1024, "Mb")
print("MCU Temperature: ", esp32.mcu_temperature(), "C")

led = Pin(45, Pin.OUT)
led.value(0)
_thread.start_new_thread(status_led, ())

#i2c = I2C(0)
#i2c = SoftI2C(scl=Pin(48), sda=Pin(47))
i2c = SoftI2C(scl=Pin(9), sda=Pin(8))
print('Scanning I2C ( SCL pin', 9, "SDA pin", 8, ") ...")
devices = i2c.scan()
if len(devices) == 0:
    print("No I2C devices were found")
else:
    print ("I2C devices found:", len(devices))
    for device in devices:
        print("I2C HEX address: ", hex(device))
        
# INA219
ina = INA219(i2c, addr=0x40)
ina.set_calibration_16V_400mA()
#ina.set_calibration_32V_1A()
_thread.start_new_thread(measure, ())


# MQTT
try:
    if not initialize_wifi(config.wifi_ssid, config.wifi_password):
        print('Error connecting to the network... exiting program')
    else:
        # Connect to MQTT broker, start MQTT client
        client = connect_mqtt()
        while True:
            # Read sensor data
            #temperature, humidity, pressure = get_sensor_readings()

            # Publish as MQTT payload
            print("Publishing MQTT topics ...")
            publish_mqtt(MQTT_TOPIC_TEMPERATURE, str(esp32.mcu_temperature()))
            publish_mqtt(MQTT_TOPIC_VOLTAGE_SHUNT, str(ina.shunt_voltage * 1000))
            publish_mqtt(MQTT_TOPIC_VOLTAGE_BUS, str(ina.bus_voltage))
            publish_mqtt(MQTT_TOPIC_CURRENT, str(ina.current))
            
            #publish_mqtt(MQTT_TOPIC_PRESSURE, str(pressure))
            #publish_mqtt(MQTT_TOPIC_HUMIDITY, str(humidity))

            # Delay 10 seconds
            sleep(3)

except Exception as e:
    print('Error:', e)



#p = PCA9685Driver
#p.set_pwm_frequency(1200)
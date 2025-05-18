from machine import Pin, I2C
from time import sleep
import esp32
import network
from umqtt.simple import MQTTClient
import config

MQTT_SERVER = config.mqtt_server
MQTT_PORT = config.mqtt_port #1883
MQTT_CLIENT = b"esp32c3 breadboard"
MQTT_KEEPALIVE = 7200
MQTT_CLIENT_ID = b"1010"

MQTT_TOPIC_TEMPERATURE = 'nodes/esp32c3-1010/mcu_temp'

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
            publish_mqtt(MQTT_TOPIC_TEMPERATURE, str(esp32.mcu_temperature()))
            #publish_mqtt(MQTT_TOPIC_PRESSURE, str(pressure))
            #publish_mqtt(MQTT_TOPIC_HUMIDITY, str(humidity))

            # Delay 10 seconds
            sleep(10)

except Exception as e:
    print('Error:', e)
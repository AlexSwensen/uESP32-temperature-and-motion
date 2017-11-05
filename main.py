"""
Code to connect an ESP32 to wifi, and publish information about temperature,
humidity, pressure, and motion.

Written by Alexander Gregory Swensen <alex.swensen@gmail.com>
Distributed under the MIT License.
"""
from time import sleep
from umqtt.simple import MQTTClient
from machine import Pin
import machine
#import bme280
import network
import ubinascii

# sensor pins
led_pin = 4
pir_sensor_pin = 17

# Wifi credentials
wifi_ssid = "..." # wifinetworkname
wifi_password = "..." # wifipassword

# Motion Status
motion = "on" # when there is motion, send this to MQTT Broker
still = "off" # When there is no motion, send this to MQTT Broker

# MQTT
mqtt_user = "..." # User for MQTT
mqtt_passsword = "..." # MQTT Password for that user
mqtt_server = b"192.168.1.92" # IP Address of mqtt server
mqtt_topic = b"home/sensors/1/motion" # Topic for publishing to
mqtt_client_id = ubinascii.hexlify(machine.unique_id()) # Unique ID of the board

mqtt = MQTTClient(mqtt_client_id, mqtt_server, 
                  user=mqtt_user, password=mqtt_passsword)

# Setup external LED, PIR Sensor, and I2C bus
led = Pin(led_pin, Pin.OUT)
ir = Pin(pir_sensor_pin, Pin.IN)

# setup WIFI
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(wifi_ssid, wifi_password)

# motion state
motion_state = 0

def turn_led_on():
    """
    Turns the LED On
    """
    led.value(1)
    print("The LED is on!")

def turn_led_off():
    """
    Turns the LED Off
    """
    led.value(0)
    print("The LED is off!")

def check_connection():
    """
    Will check for wifi connection.
    If the wifi is not connected, it will attempt to connect until a connection is successful.
    """
    connected = station.isconnected()
    if not connected:
        while not connected:
            print("Not connected, attempting to connect")
            station.connect(wifi_ssid, wifi_password)
            sleep(5)
            connected = station.isconnected()

def publish(val):
    if station.isconnected():

        value = bytes(val, 'utf-8')
        mqtt.connect()
        mqtt.publish(mqtt_topic, value)
        mqtt.disconnect()

def check_for_motion():
    global motion_state
    if ir.value() == 1:
        if motion_state == 0:
            # Send message over MQTT
            publish(motion)
            turn_led_on()

        motion_state = ir.value()
    else: 
        if motion_state == 1:
            # Send message over MQTT
            publish(still)
            turn_led_off()
        motion_state = 0
    

def main():
    while True:
        check_connection()
        while station.isconnected():
            check_for_motion()
            sleep(0.1)


if __name__ == "__main__":
    main()
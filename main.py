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
import bme280
import network
import ubinascii

# sensor pins
led_pin = 4
pir_sensor_pin = 17

# Wifi credentials
wifi_ssid = "wifinetworkname" # wifinetworkname
wifi_password = "wifipassword" # wifipassword

# MQTT
mqtt_user = "..." # User for MQTT
mqtt_passsword = "..." # MQTT Password for that user
mqtt_server = "..." # IP Address of mqtt server
mqtt_topic = "..." # Topic for publishing to
mqtt_client_id = ubinascii.hexlify(machine.unique_id()) # Unique ID of the board

# Setup external LED, PIR Sensor, and I2C bus
led = Pin(led_pin, Pin.OUT)
ir = Pin(pir_sensor_pin, Pin.IN)

# setup WIFI
station = network.WLAN(network.STA_IF)
station.active(True)

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

while True:
    check_connection()
    if ir.value() == 1:
        turn_led_on()
    else: 
        turn_led_off()
    sleep(0.1)
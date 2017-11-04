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
# Setup external LED, PIR Sensor, and I2C bus
led = Pin(4, Pin.OUT)
ir = Pin(17, Pin.IN)

# setup WIFI
wifi_ssid = "wifinetworkname"
wifi_password = "wifipassword"
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(wifi_ssid, wifi_password)

def turn_led_on():
    led.value(1)
    print("The LED is on!")

def turn_led_off():
    led.value(0)
    print("The LED is off!")

def checkConnection():
    connected = station.isconnected()
    if not connected:
        while not connected:
            print("Not connected, attempting to connect")
            station.connect(wifi_ssid, wifi_password)
            sleep(5)
            connected = station.isconnected()

while True:
    checkConnection()
    if ir.value() == 1:
        turn_led_on()
    else: 
        turn_led_off()
    sleep(0.2)
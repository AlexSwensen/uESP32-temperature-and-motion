from time import sleep
import machine
import bme280
import network
# Setup external LED, PIR Sensor, and I2C bus
led = machine.Pin(4, machine.Pin.OUT)
ir = machine.Pin(17, machine.Pin.IN)

# setup WIFI
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("YourNetworkName", "YourNetworkPassword")



def turn_led_on():
    led.value(1)
    print("The LED is on!")

def turn_led_off():
    led.value(0)
    print("The LED is off!")

while True:
    if ir.value() == 1:
        turn_led_on()
    else: 
        turn_led_off()
    sleep(0.2)
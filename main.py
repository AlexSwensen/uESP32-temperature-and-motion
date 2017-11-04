from time import sleep
import machine
import bme280
import network
led = machine.Pin(4, machine.Pin.OUT)

# i2c = machine.I2C()


ir = machine.Pin(17, machine.Pin.IN)


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
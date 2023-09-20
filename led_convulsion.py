from machine import Pin
from time import sleep

button = Pin(14, Pin.IN, Pin.PULL_UP)
led_one = Pin(15, Pin.OUT)
led_two = Pin(0, Pin.OUT)
led_three = Pin(1, Pin.OUT)

i = 0
n = 4



while True:
   if button.value() == 0:
    while i < n:
        led_one.on()
        sleep(0.1)
        led_one.off()
        led_two.on()
        sleep(0.1)
        led_two.off()
        led_three.on()
        sleep(0.1)
        led_three.off()
        i += 1
    i = 0
    while i < n:
        led_one.on()
        led_two.on()
        led_three.on()
        sleep(0.1)
        led_one.off()
        led_two.off()
        led_three.off()
        sleep(0.1)
        i += 1
    i = 0
    while i < n:
        led_one.on()
        sleep(0.1)
        led_three.on()
        sleep(0.1)
        led_one.off()
        sleep(0.08)
        led_two.on()
        led_three.off()
        sleep(0.08)
        led_two.off()
        i += 1
    i = 0
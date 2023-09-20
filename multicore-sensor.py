from machine import Pin
from time import sleep
import _thread
 
 
def thread0():
    ldr = machine.ADC(27)
    led = Pin(14,Pin.OUT)
    while True:
         if (ldr.read_u16() > 1000):
             led.value(1)
         else:
            led.value(0)

def thread1():
    onboardLed = machine.Pin("LED", machine.Pin.OUT)
    while True:
        onboardLed.on()
        sleep(2)
        onboardLed.off()
        sleep(2)
        

second_thread = _thread.start_new_thread(thread1, ())

thread0()
     

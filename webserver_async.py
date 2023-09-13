import network
import socket
import time
import utime

from machine import Pin
import uasyncio as asyncio

button_presses = 0
last_time = 0
old_presses = 0

second_button_presses = 0
second_last_time = 0
second_old_presses = 0

button_pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
button_two_pin = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
onboard = Pin("LED", Pin.OUT, value=0)

ssid = 'ssid'
password = 'password'

def webpage(score, second):
    
    html = """ <html>
    <head>
    </head>
    <body>
    <center>
    <h1>Time 1: {0}</h1>
    <h1>Time 2: {1}</h1>
    </center>
    </body>
    <script>
            setInterval(() => location.reload(), 500)
        </script>
    </html> """.format(score, second)
    return str(html)

wlan = network.WLAN(network.STA_IF)

def button_pressed_handler(pin):
    global button_presses, last_time, old_presses
    new_time = utime.ticks_ms()

    if (new_time - last_time) > 200: 
        button_presses +=1
        last_time = new_time
        
    if button_presses != old_presses:
        print('Time 1: ' + str(button_presses) + ' pontos')
        old_presses = button_presses
        
def second_button_pressed_handler(pin):
    global second_button_presses, second_last_time, second_old_presses
    new_time = utime.ticks_ms()

    if (new_time - second_last_time) > 200: 
        second_button_presses +=1
        second_last_time = new_time
    if second_button_presses != second_old_presses:
        print('Time 2: ' + str(second_button_presses) + ' pontos')
        second_old_presses = second_button_presses
        
def connect_to_network():
    wlan.active(True)
    wlan.config(pm = 0xa11140)  # Disable power-save mode
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])

async def serve_client(reader, writer):
    global button_presses, second_button_presses
    score = str(button_presses)
    second_score = str(second_button_presses)
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
        
    response = webpage(str(score), str(second_score))
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)

    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")

async def main():
    global button_presses, last_time, old_presses, button_pin
    button_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler = button_pressed_handler)
    button_two_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler = second_button_pressed_handler)
    print('Connecting to Network...')
    onboard.on()
    connect_to_network()
    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    while True:
        print('Running')
        await asyncio.sleep(10)
        
try:   
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
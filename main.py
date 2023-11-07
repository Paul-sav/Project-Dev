# Import configuration from config.py
import config
import machine
import time
# Your main application logic
print("Running the main application...")

led = machine.Pin(2, machine.Pin.OUT)
while True:
    led.value(1)
    time.sleep(1)led.value(0)
    time.sleep(1)

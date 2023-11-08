# Import configuration from config.py
import config
import machine
import time
# Your main application logic
print("Running the main application...")

led = machine.Pin(2, machine.Pin.OUT)
led.value(1)

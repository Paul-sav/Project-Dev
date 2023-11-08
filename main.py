import config
import machine
import time
# Your main application logic
print("Running the main application...")

afwd = machine.Pin(4, machine.Pin.OUT)
arev = machine.Pin(15, machine.Pin.OUT)
while True:
    afwd.value(1)
    arev.value(0)
    time.sleep(3)
    
    afwd.value(0)
    arev.value(1)
    time.sleep(3)
  

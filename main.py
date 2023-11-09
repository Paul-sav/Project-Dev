import config
import machine
import time

afwd = machine.Pin(4, machine.Pin.OUT)
arev = machine.Pin(15, machine.Pin.OUT)
while 1:
    afwd.value(1)
    arev.value(0)
    time.sleep(1)
    
    afwd.value(0)
    arev.value(1)
    time.sleep(1)

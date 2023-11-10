# Import configuration from config.py
import config
import machine
import time

# region Pin initialization
# Actuator initialization
afwd = machine.Pin(4, machine.Pin.OUT); afwd.value(0)
arev = machine.Pin(15, machine.Pin.OUT); arev.value(0)

# PWM for motor wheels
wheel_PWM_B = machine.PWM(machine.Pin(25))
wheel_PWM_B.freq(1000)
wheel_PWM_B.duty(0)
wheel_PWM_A = machine.PWM(machine.Pin(26))
wheel_PWM_A.freq(1000)
wheel_PWM_A.duty(0)

# Wheel initialization
wheel_B1 = machine.Pin(12, machine.Pin.OUT); wheel_B1.value(0)
wheel_B2 = machine.Pin(27, machine.Pin.OUT); wheel_B2.value(0)
wheel_A1 = machine.Pin(13, machine.Pin.OUT); wheel_A1.value(0)
wheel_A2 = machine.Pin(14, machine.Pin.OUT); wheel_A2.value(0)
wheel_stby = machine.Pin(33, machine.Pin.OUT); wheel_stby.value(0)
# endregion

wheel_PWM_B.duty(512)
wheel_PWM_A.duty(512)

while 1:
    afwd.value(0)
    arev.value(1)
    time.sleep(1)

    wheel_B1.value(0)
    wheel_B2.value(1)
    wheel_A1.value(0)
    wheel_A2.value(1)
    time.sleep(5)

    wheel_B1.value(1)
    wheel_B2.value(0)
    wheel_A1.value(1)
    wheel_A2.value(0)
    time.sleep(5)

    afwd.value(1)
    arev.value(0)
    time.sleep(1)

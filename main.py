# Import configuration from config.py
import config
import machine
import time

wheel_PWM_B.duty(5000)
wheel_PWM_A.duty(5000)

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

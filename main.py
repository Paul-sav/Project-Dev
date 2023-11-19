# Import configuration from config.py
import config
import machine
import time

wheel_PWM_B.duty(700)
wheel_PWM_A.duty(650)
wheel_B1.value(1)
wheel_B2.value(0)
wheel_A1.value(0)
wheel_A2.value(1)
time.sleep(1)

wheel_B1.value(1)
wheel_B2.value(0)
wheel_A1.value(1)
wheel_A2.value(0)
time.sleep(1)

wheel_B1.value(0)
wheel_B2.value(1)
wheel_A1.value(0)
wheel_A2.value(1)
time.sleep(1)

# region Pin settings for directions
# Actuator Down
# afwd.value(0)
# arev.value(1)

# Actuator Up
# afwd.value(1)
# arev.value(0)

# Wheel Forward
# wheel_B1.value(1)
# wheel_B2.value(0)
# wheel_A1.value(0)
# wheel_A2.value(1)

# Wheel Reverse
# wheel_B1.value(0)
# wheel_B2.value(1)
# wheel_A1.value(1)
# wheel_A2.value(0)
# endregion


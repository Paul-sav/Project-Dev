import config
import machine
import time
# Initialize PWM objects for pins 4 and 15
pwm_pin4 = machine.PWM(machine.Pin(4))
pwm_pin15 = machine.PWM(machine.Pin(15))

# Set the PWM frequency to 50 kHz (50000 Hz)
pwm_pin4.freq(50000)
pwm_pin15.freq(50000)

# Your main application logic
print("Running the main application...")

#while True:
	# Alternate between pins 4 and 15
pwm_pin4.duty(0)
#	pwm_pin15.duty(512)  # 50% duty cycle
#	time.sleep(2)  # Wait for 2 seconds
	
#	pwm_pin4.duty(512)  # 50% duty cycle
pwm_pin15.duty(0)
#	time.sleep(2)  # Wait for 2 seconds

#!/usr/bin/env python
import RPi.GPIO as GPIO

ObstaclePin = 7
LedPin = 11
def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(ObstaclePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(LedPin, GPIO.OUT)
	GPIO.output(LedPin, GPIO.LOW)

def loop():
	while True:
		if (0 == GPIO.input(ObstaclePin)):
			GPIO.output(LedPin, GPIO.HIGH)
			print("Barrier is detected !")
		else:
			GPIO.output(LedPin, GPIO.LOW)

			

def destroy():
	GPIO.cleanup()                     # Release resource
	GPIO.output(LedPin, GPIO.LOW)

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
#!/usr/bin/env python
import RPi.GPIO as GPIO

SIG = 7
LedPin  = 11


def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.setup(SIG, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.output(LedPin, GPIO.LOW) # Set LedPin high(+3.3V) to off led

def loop():
	while True:
		if GPIO.input(SIG) == GPIO.LOW:
			GPIO.output(LedPin, GPIO.LOW)  # led on
		else:
			GPIO.output(LedPin, GPIO.HIGH) # led off

def destroy():
	GPIO.output(LedPin, GPIO.LOW)     # led off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
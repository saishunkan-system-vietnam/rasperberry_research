#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

FlamePin = 7
LedPin = 11
def init():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LedPin, GPIO.OUT)
	GPIO.setup(FlamePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.output(LedPin, GPIO.LOW)

def loop():
	while True:
		if GPIO.input(FlamePin) == GPIO.LOW:
			GPIO.output(LedPin, GPIO.LOW)  # led on
		else:
			GPIO.output(LedPin, GPIO.HIGH) # led off
			
def destroy():
	GPIO.output(LedPin, GPIO.LOW)     
	GPIO.cleanup() 

if __name__ == '__main__':
	init()
	try:
		loop()
	except KeyboardInterrupt: 
		destroy()
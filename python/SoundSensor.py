#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

SoundPin = 7
LedPin = 11
def init():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LedPin, GPIO.OUT)
	GPIO.setup(SoundPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.output(LedPin, GPIO.LOW)

def loop():
	while True:
		if GPIO.input(SoundPin) == GPIO.LOW:
			GPIO.output(LedPin, GPIO.HIGH)  # led on
		else:
			GPIO.output(LedPin, GPIO.LOW) # led off
			
def destroy():
	GPIO.output(LedPin, GPIO.LOW)     
	GPIO.cleanup() 

if __name__ == '__main__':
	init()
	try:
		loop()
	except KeyboardInterrupt: 
		destroy()
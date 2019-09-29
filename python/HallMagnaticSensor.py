#!/usr/bin/env python
import RPi.GPIO as GPIO

HallPin = 7 
LedPin  = 11

def setup():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setwarnings(False) 
  GPIO.setup(HallPin,GPIO.IN, pull_up_down=GPIO.PUD_UP) 
  GPIO.setup(LedPin, GPIO.OUT)
  GPIO.output(LedPin, GPIO.HIGH)
    
def loop():
	while True:
		if GPIO.input(HallPin) == GPIO.LOW:
			GPIO.output(LedPin, GPIO.LOW)  # led on
		else:
			GPIO.output(LedPin, GPIO.HIGH) # led off

def destroy():
	GPIO.output(LedPin, GPIO.HIGH)     # led off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

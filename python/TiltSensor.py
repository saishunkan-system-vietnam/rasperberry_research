#!/usr/bin/env python
import RPi.GPIO as GPIO

TiltPin = 7
LedPin  = 11

Led_status = 1

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LedPin, GPIO.OUT)
	GPIO.setup(TiltPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.output(LedPin, GPIO.LOW)

def swLed(ev=None):
	global Led_status
	Led_status = not Led_status
	GPIO.output(LedPin, Led_status)
	print("LED: off" if Led_status else "LED: on")

def loop():
	GPIO.add_event_detect(TiltPin, GPIO.FALLING, callback=swLed, bouncetime=100)
	while True:
		pass 

def destroy():
	GPIO.output(LedPin, GPIO.LOW)     
	GPIO.cleanup()                    

if __name__ == '__main__':    
	setup()
	try:
		loop()
	except KeyboardInterrupt:  
		destroy()
#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

LaserPin = 7    

def setup():
	GPIO.setmode(GPIO.BOARD)       
	GPIO.setup(LaserPin, GPIO.OUT)   
	GPIO.output(LaserPin, GPIO.HIGH) 

def loop():
	while True:
		GPIO.output(LaserPin, GPIO.HIGH)  
		time.sleep(0.5)
		GPIO.output(LaserPin, GPIO.LOW) 
		time.sleep(0.5)

def destroy():
	GPIO.output(LaserPin, GPIO.LOW)     
	GPIO.cleanup()                     

if __name__ == '__main__':     
	setup()
	try:
		loop()
	except KeyboardInterrupt: 
		destroy()

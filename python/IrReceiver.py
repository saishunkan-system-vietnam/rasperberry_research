#!/usr/bin/env python
import RPi.GPIO as GPIO

IrPin  = 7
count = 0

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(IrPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def cnt(ev=None):
	global count
	count += 1
	print('Received infrared. cnt = ', count)

def loop():
	GPIO.add_event_detect(IrPin, GPIO.FALLING, callback=cnt)
	while True:
		pass

def destroy():
	GPIO.cleanup()                    

if __name__ == '__main__':  
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()

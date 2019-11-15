#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

RED = 11
GREEN = 13

PEOPLE = 29				#signalling detected people
BUZZER = 31

# Set pins' mode is output
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(PEOPLE, GPIO.IN)	
GPIO.setup(BUZZER, GPIO.OUT)

#out put
GPIO.output(RED,GPIO.LOW)
GPIO.output(GREEN,GPIO.LOW)
GPIO.output(BUZZER, GPIO.LOW)

def setColor(numberPeople):
  if(numberPeople == 0):
    if(GPIO.input(PEOPLE)):
      GPIO.output(BUZZER, GPIO.HIGH)
      GPIO.output(RED,GPIO.LOW)
      GPIO.output(GREEN,GPIO.LOW)
    else:
      GPIO.output(BUZZER, GPIO.LOW)
  else:
    GPIO.output(BUZZER,GPIO.LOW)
    if(numberPeople>=1 and numberPeople <= 5):
      GPIO.output(RED,GPIO.LOW)
      GPIO.output(GREEN,GPIO.HIGH)
    else:
      GPIO.output(RED,GPIO.HIGH)
      GPIO.output(GREEN,GPIO.LOW)
  


def destroy():
  GPIO.cleanup()
  GPIO.output(RED,GPIO.LOW)
  GPIO.output(GREEN,GPIO.LOW)
  GPIO.output(BUZZER, GPIO.LOW)


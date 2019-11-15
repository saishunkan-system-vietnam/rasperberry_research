import RPi.GPIO as GPIO

PEOPLE = 29				#signalling detected people
BUZZER = 31
GPIO.setmode(GPIO.BOARD)		#choose pin no. system
GPIO.setup(PEOPLE, GPIO.IN)	
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.output(BUZZER, GPIO.LOW)

def detectPeople(){
    if(GPIO.input(PIR_input)):
        GPIO.output(LED, GPIO.HIGH)
    else:
        GPIO.output(LED, GPIO.LOW)
}
from time import sleep
import RPi.GPIO as GPIO

#asetetaan pinnit ledeille
LED_RED = 16
LED_YELLOW = 24
LED_GREEN = 23

#pinnit asetetaan output moodiin
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_RED, GPIO.OUT)
GPIO.setup(LED_YELLOW, GPIO.OUT)
GPIO.setup(LED_GREEN, GPIO.OUT)
print("CTRL + C to quit")
try:
#looppi, jossa ledit ovat valaistuneena sekunnin ajan, jonka jälkeen ledi sammuu ja seuraava syttyy
	while True:
		GPIO.output(LED_RED, GPIO.HIGH)
		sleep(1)
		GPIO.output(LED_RED, GPIO.LOW)
		sleep(1)
		GPIO.output(LED_YELLOW, GPIO.HIGH)
		sleep(1)
		GPIO.output(LED_YELLOW, GPIO.LOW)
		sleep(1)
		GPIO.output(LED_GREEN, GPIO.HIGH)
		sleep(1)
		GPIO.output(LED_GREEN, GPIO.LOW)
		sleep(1)
finally:
	GPIO.cleanup()

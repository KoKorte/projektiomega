import time
import RPi.GPIO as GPIO

relay_ch = 17

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(relay_ch, GPIO.OUT)
GPIO.output(relay_ch, GPIO.LOW)
time.sleep(3)
GPIO.output(relay_ch, GPIO.HIGH)
GPIO.cleanup()

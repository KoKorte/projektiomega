import RPi.GPIO as GPIO
import time

#def button_callback(channel):
#	print("Button was pushed!")
	
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#GPIO.add_event_detect(27,GPIO.RISING,callback=button_callback)
while True:
	if GPIO.input(27):
		pressed_time=time.monotonic()
		while GPIO.input(27):
			pass
		pressed_time=time.monotonic()-pressed_time
		if pressed_time<1:
			print("Button was clicked")
		elif pressed_time>1:
			print("Button was held")
message = input("Press enter to quit\n\n")
GPIO.cleanup()

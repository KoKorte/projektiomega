import RPi.GPIO as GPIO, time, os

GPIO.setmode(GPIO.BCM)

button = 27
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

rebootti = 5

button_time = None

def button_call(channel):
	global button_time
	
	if GPIO.input(channel)==GPIO.LOW:
		button_time=time.time()
	else:
		if button_time is not None:
			button_timer=time.time()-button_time
			if button_timer >= rebootti:
				os.system("reboot")
			else:
				os.system("sudo shutdown -h now")

GPIO.add_event_detect(button, GPIO.BOTH, callback=button_call, bouncetime=200)

try:
	while True:
		time.sleep(1)

except KeyboardInterrupt:
	print("CTRL + C to shutdown")
	GPIO.cleanup()

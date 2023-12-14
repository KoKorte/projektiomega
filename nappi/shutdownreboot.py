import RPi.GPIO as GPIO, time, os

# Asetetaan GPIO BCM -tilaan
GPIO.setmode(GPIO.BCM)

# Asetetaan napille pinni
button = 27
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# Napin pinnin asetus pulled up tilaan

reboot = 3	# Reboot muuttuja, jonka arvo on sekunnit

button_time = None	# Muuttuja napin painallukselle, 

# Funktio napin painalluksen tarkistamiselle
def button_call(channel):	
	global button_time
	
	if GPIO.input(channel)==GPIO.LOW:
		button_time=time.time()
	else:
		# Jos button_time muuttuja saa jonkin muun arvon kuin None, alkaa ajastin button_timer
		if button_time is not None:
			button_timer=time.time()-button_time	# Luodaan muuttuja button_timer ajastimelle
			if button_timer >= reboot:				# Jos reboot muutujan arvo täyttyy, käynnistetään järjestelmä uudestaan
				os.system("reboot")
			else:
				os.system("sudo shutdown -h now")	# Suljetaan järjestelmä, jos reboot muutujan arvo ei täyty

GPIO.add_event_detect(button, GPIO.BOTH, callback=button_call, bouncetime=200)

try:
	while True:
		time.sleep(1)

except KeyboardInterrupt:
	print("CTRL + C to shutdown")
	GPIO.cleanup()

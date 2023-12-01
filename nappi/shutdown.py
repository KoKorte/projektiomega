import os, time, RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Our function on what to do when the button is pressed
def Reboot(channel):
    os.system('wall Button shutdown started...')
    os.system('reboot')

# Add our function to execute when the button pressed event happens
GPIO.add_event_detect(27, GPIO.FALLING, callback=Reboot, bouncetime=3000)

# Now wait!
while 1:
    time.sleep(1)

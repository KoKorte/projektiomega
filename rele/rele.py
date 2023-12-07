import time
import RPi.GPIO as GPIO
import sys

#testi tulostus mikä on ensimmäinen parametri. sys.argv[0] on ajettavan tiedoston nimi.
print(sys.argv[1])
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

relay_ch = 17 # releen portti

# jos rele.py saa argumentiksi komentoriviltä 'on' niin gpio.out ja .high
if sys.argv[1] == 'on':
    print ("rele päälle")
    GPIO.setup(relay_ch, GPIO.OUT)
    #GPIO.output(relay_ch, GPIO.LOW)
    GPIO.output(relay_ch, GPIO.HIGH)

# jos rele.py saa argumentiksi komentoriviltä 'off' niin gpio.low ja .in SEKÄ gpio.cleanup() joka sulkee myös käytetyt portit + asettaa virran nollaksi.
#time.sleep(3)
if sys.argv[1] == 'off':
    print ("rele pois päältä")
  #  GPIO.output(relay_ch, GPIO.LOW)
    GPIO.setup(relay_ch, GPIO.IN)
    GPIO.cleanup()

import time
import RPi.GPIO as GPIO
import sys
import datetime

# Testi tulostus mikä on ensimmäinen parametri. sys.argv[0] on ajettavan tiedoston nimi.
#print(sys.argv[1])
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

x = datetime.datetime.now()	    # Nykyinen ajanmääre
t = x.strftime("%Y-%m-%d %H:%M ")# Aika ilmoitetaan muodossa vuosi-kuukausi-päivä

relay_ch = 17 # releen portti

# Jos rele.py saa argumentiksi komentoriviltä 'on' niin gpio.out ja .high
if sys.argv[1] == 'on':
    #print ("rele päälle")
    GPIO.setup(relay_ch, GPIO.OUT)
    GPIO.output(relay_ch, GPIO.HIGH)
# Luodaan tekstitiedosto logitukselle
    #f=open("relelog.txt", "a")
    #f.write(t + 'rele on' + '\n')
    #f.close()

# Jos rele.py saa argumentiksi komentoriviltä 'off' niin gpio.low ja .in SEKÄ gpio.cleanup() joka sulkee myös käytetyt portit + asettaa virran nollaksi.
if sys.argv[1] == 'off':
    #print ("rele pois päältä")
    GPIO.setup(relay_ch, GPIO.IN)
    GPIO.cleanup()
# Luodaan tekstitiedosto logitukselle
    #f=open("relelog.txt", "a")
    #f.write(t + 'rele off' + '\n')
    #f.close()

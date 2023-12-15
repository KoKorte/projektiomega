import datetime
import Adafruit_DHT
import time
import sqlite3
import math
import os
import RPi.GPIO as GPIO

# Testataan yhteys tietokantaan ja tarkastetaan tuleeko ongelmia
try:
	# Avataan yhteys omega.db tietokantaan
	connection = sqlite3.connect('/home/omega/PythonKoodit/projektiomega/db/omega.db')
	cursor = connection.cursor()
# Luodaan except joka hakee virheen
except sqlite3.Error as e:
	print(f"Database error: {e}")	# Tulostetaan mistä virhe johtuu

# Haetaan datetime -kirjastosta vaadittavat ajanmääreet
x = datetime.datetime.now()         # Nykyinen ajanmääre
t = x.strftime("%Y-%m-%d %H:%M:%S") # Aika ilmoitetaan muodossa vuosi-kuukausi-päivä tunti:minuutti:sekunti
#print("Time:", t)

# Haetaan ConfigValues -taulu, josta haetaan raja-arvot
configList = []
cursor = connection.cursor()
cursor.execute("SELECT * from ConfigValues")
rows = cursor.fetchall()
for row in rows:
    configList = [row]

#print("Min. temperature: ", configList[0][0])   # Tulostetaan minimi lämpöarvo
minTemp=configList[0][0] 
time.sleep(1)

# Määritetään DHT lämpö- ja kosteusanturille pinnit
humidity, temperature = Adafruit_DHT.read_retry(22, 18) # 22 on DHT 22 ja 18 on GPIO 18 pinni

# Tarkistetaan saadaanko lämpötilalle ja kosteudelle arvoja
#if humidity is not None and temperature is not None:
#    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
#else:
#    print('Failed to get reading. Try again!')

# Muuttujat, joilla pyöristetään lämpötila ja kosteus tietokantaa varten
temperature = round(temperature, 1)
humidity = round(humidity, 1)

# SQL INSERT -lause omega.db tietokantaan, temperature tauluun
connection.execute("""INSERT into Temperature (LoggedTime, Temperature, Humidity) Values(?, ?, ?)""",(t, temperature, humidity))
connection.commit() # Syötetään muutokset tauluun
connection.close()  # Suljetaan yhteys

# Verrataan minimilämpötilaa nykyiseen mitattuun lämpötilaan
# jos anturin nykyinen mitattu lämpötila on pienempi kuin minimilämpötila niin suoritetaan laitteiden automatio-ohjaus pythonscripti.
# sekä lokimerkintä. 
if temperature < minTemp:
    #print("Suorita laitteiden automaatio-ohjaus rele päälle!")
    os.system("python /home/omega/PythonKoodit/projektiomega/automaatio/automaatio.py")

elif temperature > minTemp:
    #print("Suorita laitteiden automaatio-ohjaus rele pois päältä!")
    os.system("python /home/omega/PythonKoodit/projektiomega/automaatio/automaatio.py")

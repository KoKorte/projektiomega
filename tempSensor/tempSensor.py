import datetime
import Adafruit_DHT
import time
import sqlite3
import math
import os
import RPi.GPIO as GPIO

# TODO lisää automaatio.py tiedosto kun se on tehty if-lauseeseen, lisää lokimerkintä SEKÄ RELEEN PINNIN tilan tarkistus??? configvalues db puuttuu lämpötiloja...
#
#print("________________________________________")#viiva rivi erottamaan datan helpommin katsottavaksi
#y = datetime.datetime.now()
#d = y.strftime("%d/%m/%Y")
#print("Date:", d)
#print("________________________________________")


connection = sqlite3.connect('/home/omega/Database/omega.db')#avataan yhteys omega.db tietokantaan

x = datetime.datetime.now()
t = x.strftime("%Y-%m-%d %H:%M:%S")#aika ilmoitetaan muodossa vuosi-kuukausi-päivä tunti:minuutti:sekunti
print("Time:", t)

configlista = []
cursor = connection.cursor()
cursor.execute("SELECT * from ConfigValues")
rows = cursor.fetchall()
for row in rows:
    configlista = [row]

print(configlista[0])
print(configlista[0][0])



# 22 on DHT 22 ja 18 on GPIO 18 pinni
humidity, temperature = Adafruit_DHT.read_retry(22, 18)


if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
#    print("________________________________________")

#funktiot joilla pyöristetään lämpötila ja kosteus databasea varten
temperature = round(temperature, 1)
humidity = round(humidity, 1)

#sql insert lause omega.db tietokantaan, temperature tauluun
connection.execute("""INSERT into Temperature (LoggedTime, Temperature, Humidity) Values(?, ?, ?)""",(t, temperature, humidity))
connection.commit()#syötetään muutokset tauluun
connection.close()#suljetaan yhteys

# Verrataan minimilämpötilaa (configlistan antaman tuplen ensimmäinen elementti) nykyiseen mitattuun lämpötilaan
# jos anturin nykyinen mitattu lämpötila on pienempi kuin minimilämpötila niin suoritetaan laitteiden automatio-ohjaus pythonscripti.
# sekä lokimerkintä. 
if temperature < configlista[0][0] and GPIO.input(17) == False:
    print("Suorita laitteiden automaatio-ohjaus!")
    #os.system("py automaatio.py")
elif temperature > configlista[0][0] and GPIO.input(17) == True:
    print("Suorita laitteiden automaatio-ohjaus!")
    #os.system("py automaatio.py")


#time.sleep(3.0)

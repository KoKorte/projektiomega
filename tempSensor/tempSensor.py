import datetime
import Adafruit_DHT
import time
import sqlite3
import math


#
print("________________________________________")#viiva rivi erottamaan datan helpommin katsottavaksi
y = datetime.datetime.now()
d = y.strftime("%d/%m/%Y")
print("Date:", d)
print("________________________________________")

while True:
    connection = sqlite3.connect('/home/omega/Database/omega.db')#avataan yhteys omega.db tietokantaan

    x = datetime.datetime.now()
    t = x.strftime("%Y-%m-%d %H:%M:%S")#aika ilmoitetaan muodossa vuosi-kuukausi-päivä tunti:minuutti:sekunti
    print("Time:", t)

#   22 on DHT 22 ja 18 on GPIO 18 pinni
    humidity, temperature = Adafruit_DHT.read_retry(22, 18)


    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')
    print("________________________________________")
    #funktiot joilla pyöristetään lämpötila ja kosteus databasea varten
    temperature = round(temperature, 1)
    humidity = round(humidity, 1)
    #sql insert lause omega.db tietokantaan, temperature tauluun
    connection.execute("""INSERT into Temperature (LoggedTime, Temperature, Humidity) Values(?, ?, ?)""",(t, temperature, humidity))
    connection.commit()#syötetään muutokset tauluun
    connection.close()#suljetaan yhteys

    time.sleep(3.0)

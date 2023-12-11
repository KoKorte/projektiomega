# Pohja laitteiden automaatio-ohjaukselle
# Tee muutokset!

import datetime
import sqlite3

# datetime
x = datetime.datetime.now()
t = x.strftime("%Y-%m-%d"+'%')#aika ilmoitetaan muodossa vuosi-kuukausi-päivä
h = x.strftime("%H") # tunti jota käytetään sähkönhinnan haussa kyseiselle tunnille.


connection = sqlite3.connect('/home/omega/Database/omega.db')#avataan yhteys omega.db tietokantaan

# ladataan config
configlista = []
cursor = connection.cursor()
cursor.execute("SELECT * from ConfigValues")
rows = cursor.fetchall()

for row in rows:
	configlista = [row]

print("Min hinta ", configlista[0][2])
print("Max hinta ", configlista[0][3])



# ladataan hintatiedot
cursor = connection.cursor()
cursor.execute("SELECT * from ElectricityPrices WHERE PriceDate like ? AND DateHour=?",(t,h))
rivit = cursor.fetchall()
for rivi in rivit:
	pricelista = [rivi]

print("Hinta nyt ", pricelista[0][3])

# ladataan lämpötilatiedot
temperatureLista = []
cursor = connection.cursor()
cursor.execute("SELECT * from Temperature where LoggedTime = (select max(LoggedTime) from Temperature)")
rows = cursor.fetchall()
for row in rows:
	temperatureLista = [row]

print("Viimeisin lämpötila ", temperatureLista[0][3])
connection.close()#suljetaan yhteys

# ylittyykö raja-arvot lämpötiloissa
tempOffset = 0

if configlista[0][2] < pricelista[0][3]:
	tempOffset = 3


if temperatureLista[0][3] < configlista[0][0]+tempOffset:
    print("rele päälle!")
    #os.system("python rele.py on")

elif temperatureLista[0][3] > configlista[0][0]+tempOffset:
    print("rele pois päältä!")
    #os.system("python rele.py off")


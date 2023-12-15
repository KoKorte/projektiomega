# Laitteiden automaattinen ohjaus, joka ohjaa relettä tempSensor.py:n kutsusta
# Lisätään kirjastot datetime, os ja sqlite3
import datetime, os
import sqlite3

# Haetaan datetime -kirjastosta vaadittavat ajanmääreet
x = datetime.datetime.now()	# Nykyinen ajanmääre
t = x.strftime("%Y-%m-%d")	# Aika ilmoitetaan muodossa vuosi-kuukausi-päivä
h = x.strftime("%H") 		# Tunti jota käytetään sähkönhinnan haussa kyseiselle tunnille

# Testataan yhteys tietokantaan ja tarkastetaan tuleeko ongelmia
try:
    # Avataan yhteys omega.db tietokantaan
    connection = sqlite3.connect('/home/omega/PythonKoodit/projektiomega/db/omega.db')
    cursor = connection.cursor()
# Luodaan except joka hakee virheen
except sqlite3.Error as e:
    print(f"Database error: {e}")	# Tulostetaan mistä virhe johtuu

# Haetaan ConfigValues -taulu, josta haetaan raja-arvot
configList = []
cursor = connection.cursor()
cursor.execute("SELECT * from ConfigValues")
rows = cursor.fetchall()

for row in rows:
    configList = [row]

#print("Min temperature: ", configList[0][0])
minTemp=configList[0][0] 
#print("Min price: ", configList[0][2])
minPrice=configList[0][2]
#print("Max price: ", configList[0][3])
maxPrice=configList[0][3]


# Haetaan sähkönhinnat ElectricityPrices -taulusta
cursor = connection.cursor()
cursor.execute("SELECT * from ElectricityPrices WHERE PriceDate=? AND DateHour=?",(t,h))
rivit = cursor.fetchall()
for rivi in rivit:
    priceList = [rivi]
	
roundedPrice = round(priceList[0][4], 5)
#print("Price now: ", roundedPrice)

# Haetaan viimeisin mitattu lämpötila Temperature -taulusta
temperatureList = []
cursor = connection.cursor()
cursor.execute("SELECT * from Temperature where LoggedTime = (select max(LoggedTime) from Temperature)")
rows = cursor.fetchall()
for row in rows:
    temperatureList = [row]

#print("Latest temperature: ", temperatureList[0][2])
currentTemp=temperatureList[0][2]
connection.close()#suljetaan yhteys

# Tarkistetaan ylittyvätkö raja-arvot lämpötiloissa
tempOffset = 0	# Annetaan tempOffsetille alkuarvo

if minPrice >= roundedPrice:	# Jos sähkönhinta on alle tai yhtäsuuri kuin minimi hinta,
    tempOffset = 2		# lisätään minimi lämpötilaan +2 Celsiusta

# Jos nykyinen lämpötila on alle minimiarvon, kytketään rele päälle
if currentTemp < minTemp+tempOffset:
    os.system("python /home/omega/PythonKoodit/projektiomega/rele/rele.py on")
    #f1=open("automaatiolog.txt", "a")
    #f1.write(f"{t} {h} Rele ON currentTemp: {currentTemp} tempOffset: {tempOffset}\n")
    #f1.close()

# Jos nykyinen lämpötila on yli minimiarvon, kytketään rele pois päältä
elif currentTemp > minTemp+tempOffset:
    os.system("python /home/omega/PythonKoodit/projektiomega/rele/rele.py off")
   #f2=open("automaatiolog.txt", "a")
    #f2.write(f"{t} {h} Rele OFF currentTemp: {currentTemp} tempOffset: {tempOffset}\n")
    #f2.close()


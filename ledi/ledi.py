from time import sleep
import RPi.GPIO as GPIO, sqlite3, time, datetime, sys

# Testataan yhteys tietokantaan ja tarkastetaan tuleeko ongelmia
try:
	# Avataan yhteys omega.db tietokantaan
	connection = sqlite3.connect('/home/omega/PythonKoodit/projektiomega/db/omega.db')
	cursor = connection.cursor()
# Luodaan except joka hakee virheen
except sqlite3.Error as e:
	print(f"Database error: {e}")	# Tulostetaan mistä virhe johtuu
	
# Ulkoinen while loop, joka käy kerran tunnissa päivittämässä nykyisen sähkönhinnan
while True:
	# Avataan yhteys omega.db tietokantaan
	connection = sqlite3.connect('/home/omega/PythonKoodit/projektiomega/db/omega.db')
	test = datetime.datetime.today().timetuple()
	x = datetime.datetime.now()	# Haetaan datetime -kirjastosta vaadittavat ajanmääreet
	t = x.strftime("%Y-%m-%d")	# Aika ilmoitetaan muodossa vuosi-kuukausi-päivä
	h = x.strftime("%H")		# Tunti jota käytetään sähkönhinnan haussa kyseiselle tunnille.
	#print("Time:", t)
	#print(h)

# Haetaan config-listasta tietoja
	configList = []
	priceList = []
	cursor = connection.cursor()
	cursor.execute("SELECT * from ConfigValues")
	rows = cursor.fetchall()
	for row in rows:
		configList = [row]
	#print("Current hour:", test[3])
	#print("Min. price:", configList[0][2])
	minPrice=configList[0][2]
	#print("Max. price:", configList[0][3])
	maxPrice=configList[0][3]

# Haetaan nykyisen tunnin sähkönhinta
	cursor = connection.cursor()
	cursor.execute("SELECT * from ElectricityPrices WHERE PriceDate=? AND DateHour=?",(t,h))
	rivit = cursor.fetchall()
	for rivi in rivit:
		priceList = [rivi]

	#print("Current price:", priceList[0][4])
	currentPrice=priceList[0][4]
	connection.close()	# Suljetaan yhteys

# Asetetaan pinnit ledeille
	LED_RED = 16
	LED_YELLOW = 24
	LED_GREEN = 23

# Asetetaan GPIO BCM -tilaan
	GPIO.setmode(GPIO.BCM)

# Väläytetään kaikki ledit kun hintatiedot päivittyvät
	# Vihreä ledi output -> high -> low -> input 
	GPIO.setup(LED_GREEN, GPIO.OUT)
	GPIO.output(LED_GREEN, GPIO.HIGH)
	sleep(0.2)
	GPIO.output(LED_GREEN, GPIO.LOW)
	sleep(0.2)
	GPIO.setup(LED_GREEN, GPIO.IN)
	
	# Keltainen ledi output -> high -> low -> input 
	GPIO.setup(LED_YELLOW, GPIO.OUT)
	GPIO.output(LED_YELLOW, GPIO.HIGH)
	sleep(0.2)
	GPIO.output(LED_YELLOW, GPIO.LOW)
	sleep(0.2)
	GPIO.setup(LED_YELLOW, GPIO.IN)
	
	# Punainen ledi output -> high -> low -> input 
	GPIO.setup(LED_RED, GPIO.OUT)
	GPIO.output(LED_RED, GPIO.HIGH)
	sleep(0.2)
	GPIO.output(LED_RED, GPIO.LOW)
	sleep(0.2)
	GPIO.setup(LED_RED, GPIO.IN)
	
	
# Jos hinta on halpaa, vilkutetaan vihreää lediä
	if minPrice > currentPrice:
		GPIO.setup(LED_GREEN, GPIO.OUT)
		hintapinni = LED_GREEN

# Jos hinta on kallista, vilkutetaan punaista lediä
	elif maxPrice < currentPrice:
		GPIO.setup(LED_RED, GPIO.OUT)
		hintapinni = LED_RED

# Jos hinta ei ole halpaa, eikä kallista, vilkutetaan keltaista lediä
	else:
		GPIO.setup(LED_YELLOW, GPIO.OUT)
		hintapinni = LED_YELLOW

# Luodaan tekstitiedosto logitukselle
	#f=open("ledlog.txt", "a")
	#f.write(f"{t} {h} LED käynyt päällä Current Price: {currentPrice} Väri: {hintapinni}\n")
	#f.close()
	
	hours = test[3]	
# Sisempi silmukka, joka pyörii tunnin ajan ja poistutaan tunnin vaihtuessa ulompaan silmukkaan
	try:
		while hours == test[3]:
			# Ledi pysyy päällä yhden sekunnin, jonka jälkeen se sammuu kolmeksi sekunniksi
			test = datetime.datetime.today().timetuple()
			GPIO.output(hintapinni, GPIO.HIGH)
			sleep(1)
			GPIO.output(hintapinni, GPIO.LOW)
			sleep(3)

	except:
		GPIO.cleanup()
		sys.exit(0)

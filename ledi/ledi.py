from time import sleep
import RPi.GPIO as GPIO, sqlite3, time, datetime, sys

#testataan yhteys tietokantaan ja tarkastetaan tuleeko ongelmia
try:
	connection = sqlite3.connect('/home/omega/PythonKoodit/projektiomega/db/omega.db')#avataan yhteys omega.db tietokantaan
	cursor = connection.cursor()
#luodaan except joka hakee virheen
except sqlite3.Error as e:
	print(f"Database error: {e}")#tulostetaan mistä virhe johtuu
	
#luodaan yhteys tietokantaan
while True:
	connection = sqlite3.connect('/home/omega/PythonKoodit/projektiomega/db/omega.db')#avataan yhteys omega.db tietokantaan
	test = datetime.datetime.today().timetuple()
	x = datetime.datetime.now()
	t = x.strftime("%Y-%m-%d"+'%')#aika ilmoitetaan muodossa vuosi-kuukausi-päivä
	h = x.strftime("%H")
	print("Time:", t)
	print(h)

#haetaan config ja price listoista tietoja
	configlista = []
	pricelista = []
	cursor = connection.cursor()
	cursor.execute("SELECT * from ConfigValues")
	rows = cursor.fetchall()
	for row in rows:
		configlista = [row]
	print("timetuple ", test)
	print("minutes ", test[4])
	print("hours ", test[3])
	print("Min hinta ", configlista[0][2])
	print("Max hinta ", configlista[0][3])

#haetaan ElectricityP
	LED_YELLOW = 24
	LED_GREEN = 23
	cursor = connection.cursor()
	cursor.execute("SELECT * from ElectricityPrices WHERE PriceDate like ? AND DateHour=?",(t,h))
	rivit = cursor.fetchall()
	for rivi in rivit:
		pricelista = [rivi]

	print("Hinta nyt ", pricelista[0][4])
	connection.close()#suljetaan yhteys

#asetetaan pinnit ledeille
	LED_RED = 16
	LED_YELLOW = 24
	LED_GREEN = 23

#pinnit asetetaan output moodiin
	GPIO.setmode(GPIO.BCM)

#väläytetään kaikki ledit kun hintatiedot päivittyvät
	#vihreä ledi output -> high -> low -> input 
	GPIO.setup(LED_GREEN, GPIO.OUT)
	GPIO.output(LED_GREEN, GPIO.HIGH)
	sleep(0.2)
	GPIO.output(LED_GREEN, GPIO.LOW)
	sleep(0.2)
	GPIO.setup(LED_GREEN, GPIO.IN)
	
	#keltainen ledi output -> high -> low -> input 
	GPIO.setup(LED_YELLOW, GPIO.OUT)
	GPIO.output(LED_YELLOW, GPIO.HIGH)
	sleep(0.2)
	GPIO.output(LED_YELLOW, GPIO.LOW)
	sleep(0.2)
	GPIO.setup(LED_YELLOW, GPIO.IN)
	
	#punainen ledi output -> high -> low -> input 
	GPIO.setup(LED_RED, GPIO.OUT)
	GPIO.output(LED_RED, GPIO.HIGH)
	sleep(0.2)
	GPIO.output(LED_RED, GPIO.LOW)
	sleep(0.2)
	GPIO.setup(LED_RED, GPIO.IN)
	
	
#jos hinta on halpaa, vilkutetaan vihreää lediä
	if configlista[0][2] > pricelista[0][4]:
		GPIO.setup(LED_GREEN, GPIO.OUT)
		hintapinni = LED_GREEN

#jos hinta on kallista, vilkutetaan punaista lediä
	elif configlista[0][3] < pricelista[0][4]:
		GPIO.setup(LED_RED, GPIO.OUT)
		hintapinni = LED_RED

#jos hinta ei ole halpaa, eikä kallista, vilkutetaan keltaista lediä
	else:
		GPIO.setup(LED_YELLOW, GPIO.OUT)
		hintapinni = LED_YELLOW

	tunnit = test[3]	
#looppi, jossa ledit ovat valaistuneena sekunnin ajan, jonka jälkeen ledi sammuu ja seuraava syttyy
	try:
		while tunnit == test[3]:
			test = datetime.datetime.today().timetuple()
			GPIO.output(hintapinni, GPIO.HIGH)
			sleep(1)
			GPIO.output(hintapinni, GPIO.LOW)
			sleep(3)

	except:
		GPIO.cleanup()
		sys.exit(0)

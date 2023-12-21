# Omega

![raspi](https://github.com/Zame76/projektiomega/assets/28978509/4c4a0ae3-8167-4a2c-b8de-b22f9fb56eb9)

## Project description
Omega is embedded systems project made on embedded systems course.
Goal of this project was to build a Linux based system which can measure room temperature, find next day electricity market prices and tell if price of the electricity is cheap, medium or expensive depending on set preferences by user and then controls a heating or cooling device with relay. The user can remotely change set minimun and maximum values for room temperatures and the electricity price preferences and also user can remotely check current room temperature. The electricity price preferences affect the air temperature in the room, for example if the electricity price is expensive, the room temperature is kept cooler than when it is cheap.

### UI
UI is a simple webpage that collects relevant data from public weather data, electricity prices and data from device through API interfaces. UI can be run on device itself, but it can be configured to run on a dedicated web server. If dedicated web server is to be used, UI has a simple API which can receive data from device and send back the configuration data.  
On configuration page, user can set values to control device on how to behave regarding room temperature and electricity prices. Both of these have lower limit and upper limit, which affects how the device works. More options have been planned, but these are the required settings. 

### Raspberry
- electricity_api.py: Is ran at 18:00 when new electricity market prices are released by ENTSO-E.
- tempSensor: Is timed to run every 10 minutes, measures room temperature and humidity, stores values to omega database.
- ledi.py: Is ran on system startup, flashes the corresponding LED component depending on electricity market price (Green for cheap, Yellow for medium, Red for expensive).
- automaatio.py: Is called to run by tempSensor.py if needed. Depends on user's preference for room temperature. 
- rele.py: Is called to run by automaatio.py to toggle electricity device on or off.
- shutdownreboot.py: Simple script for manual button to either shutdown the system on click or reboot the system if the button is held for at least three seconds.
- config-site/app.py: Is called to run the UI website. It can be either run on this machine or be placed on a dedicated web server.
- sync.py: Is only needed when UI is run on different machine. It handles the data transfer between device and website.
- omega.db: SQL database for storing and fetching data.

## Tools and technologies
- Raspberry Pi 4
- DHT22 temperature and humidity sensor
- Relay module
- SQLite database
- ENTSO-E API
- Digitrafic API
- Flask
- Linux Cron

## Contributors
- Juntunen Sampo
- Korteniemi Niko
- Penttinen Kimmo

## License
This project falls under MIT license

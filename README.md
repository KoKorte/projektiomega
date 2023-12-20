# Omega

![raspi](https://github.com/Zame76/projektiomega/assets/28978509/4c4a0ae3-8167-4a2c-b8de-b22f9fb56eb9)

## Project description
Omega is embedded systems project made on embedded systems course.
Goal of this project was to build a Linux based system which can measure room temperature, find next day electricity market prices and tell if price of the electricity is cheap, medium or expensive depending on set preferences by user and then controls a heating or cooling device with relay. The user can remotely change set minimun and maximum values for room temperatures and the electricity price preferences and also user can remotely check room current room temperature. The electricity price preferences affect the air temperature in the room, for example if the electricity price is expensive, the room temperature is kept cooler than when it is cheap.

### UI

### Raspberry
- electricity_api.py: Is ran at 18:00 when new electricity market prices are released by ENTSO-E.
- tempSensor: Is timed to runn every 10 minutes, measures room temperature and humidity, stores values to omega.db database.
- ledi.py: Is ran on system startup, flashes the corresponding LED component depending on electricity market price (Green for cheap, Yellow for medium, Red for expensive).
- automaatio.py: Is called to run by tempSensor.py if needed. Depends on user's preference for room temperature. 
- rele.py: Is called to run by automaatio.py to toggle on or off.
- shutdownreboot.py: Simple script for manual button to either shutdown the system on click or reboot the system if the button is held for at least three seconds.
- omega.db: SQL database for storing and fetching data.

## Tools and technologies
- Raspberry Pi 4
- DHT22 temperature and humidity sensor
- Relay module
- SQLite database
- ENSO-E API
- Flask
- Linux Cron

## Contributors
- Juntunen Sampo
- Korteniemi Niko
- Penttinen Kimmo

## License
This project falls under MIT license

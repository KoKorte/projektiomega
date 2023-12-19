# Omega

![raspi](https://github.com/Zame76/projektiomega/assets/28978509/4c4a0ae3-8167-4a2c-b8de-b22f9fb56eb9)

## Project description
Omega is embedded systems project made on embedded systems course.
Goal of this project was to build a Linux based system which can measure room temperature, find next day electricity market prices and tell if price of the electricity is cheap, medium or expensive depending on set preferences by user and then controls a heating or cooling device with relay. The user can remotely change set minimun and maximum values for room temperatures and the electricity price preferences and also user can remotely check room current room temperature. The electricity price prefenrences affect the air temperature in the room, for example if the electricity price is expensive, the room temperature is kept cooler than when it is cheap.

### UI part

### Raspberry
- electricity_api.py
- tempSensor
- ledi.py
- automaatio.py
- rele.py
- rebootshutdown.py
- omega.db

## Tools and technologies
- Raspberry Pi 4
- DHT22 temperature and humidity sensor
- Relay module
- SQLite database

## Contributors
- Juntunen Sampo
- Korteniemi Niko
- Penttinen Kimmo

## License
This project falls under MIT license

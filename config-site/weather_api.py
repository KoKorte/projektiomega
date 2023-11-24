# Import libraries
from datetime import datetime
from requests import get
from sql import createTables, getLatestPhoto, getLatestWeather, insertPhoto, insertWeather
import photo
import config

def windSpeed(speed):
    if 0 <= speed < 1:
        return "Tyyntä"
    if 1 <= speed < 4:
        return "Heikkoa"
    if 4 <= speed < 8:
        return "Kohtalaista"
    if 8 <= speed < 14:
        return "Navakkaa"
    if 14 <= speed < 21:
        return "Kovaa"
    if 21 <= speed < 33:
        return "Myrsky"
    if 33 <= speed:
        return "Hirmumyrsky"
    

def getWeatherData():
    return_value = dict()
    getapi = False

    # Digitraffic.fi allows maximum of 60 apicalls per minute, so we are going to store the results into the database and only get
    # refreshed periodically in order to not get blocked by digitraffic. 
    createTables()
    weather = getLatestWeather()
    photoinfo = getLatestPhoto()    

    # Get the current datetime value
    current_time = datetime.now()

    # If database is empty
    if weather == None or photoinfo == None:
        # Get fresh data from api
        getapi = True
    # Otherwise check the time difference, if more than 5 minutes has passed since last api call    
    else: 
         # Convert time from sql database to datetime format
        date_format = '%Y-%m-%d %H:%M:%S.%f'
        sql_time = datetime.strptime(weather[0], date_format)
        # Get the time difference in minutes
        timediff = (current_time - sql_time).total_seconds() / 60        
        # If more than 5 minutes has passed, get fresh data from api
        if timediff > 5:
            getapi = True
        # Otherwise use data from database
        else:
            getapi = False

    # Do the api call    
    if getapi == True:
        # print this to terminal running the framework to see where the data came from
        print("api")

        # Url for open source api call, provider digitraffic.fi, which maintains lots of weather stations along Finnish road network
        # This site is located alongside Highway no 4, Oulu (Intiö), Finland (https://tie.digitraffic.fi/api/weather/v1/stations/12019)
        # List of all weather stations: https://tie.digitraffic.fi/api/weather/v1/stations
        url = "https://tie.digitraffic.fi/api/weather/v1/stations/12019/data"

        # Digitraffic.fi requires a user information, so we provide one. You can create your own by creating config.py on root directory
        # and inserting digitraffic_user variable with proper name. Read more: 
        # https://www.digitraffic.fi/tuki/ohjeita/#yleist%C3%A4-huomioitavaa
        headers = {'Digitraffic-User': config.digitraffic_user}
        # Make the api call and get refresh weather data
        response = get(url, headers=headers)
        sensors = response.json()['sensorValues']

        # Turn ISO-formatted datetime string to UTC-datetime object
        measuredtime = datetime.fromisoformat(sensors[0]['measuredTime'])
        # Convert utc time to local time. From Python 3.6. and onwards, .astimezone returns localtimezone value if no tz-option is None
        localsensortime = datetime.astimezone(measuredtime).strftime("%d.%m.%Y %H:%M:%S")

        # Create a tuple of parameters to be inserted to Weather table
        parameters = (current_time, localsensortime, sensors[0]['value'], sensors[12]['value'], sensors[14]['value'], sensors[15]['value'], 
                    sensors[16]['value'], sensors[16]['sensorValueDescriptionFi'],  sensors[16]['sensorValueDescriptionEn'])
        
        # Insert values to Weather table
        insertWeather(parameters)
        
        # Get the photo metainfo
        url = "https://tie.digitraffic.fi/api/weathercam/v1/stations/C12612/data"
        response = get(url, headers=headers)
        # Convert utc time to local time. From Python 3.6. and onwards, .astimezone returns localtimezone value if no tz-option is None
        presets = response.json()['presets']   

        # Turn ISO-formatted datetime string to UTC-datetime object
        measuredtime = datetime.fromisoformat(presets[1]['measuredTime'])
        localpresettime = datetime.astimezone(measuredtime).strftime("%d.%m.%Y %H:%M:%S")

        # Get the photo
        url = "https://weathercam.digitraffic.fi/" + presets[1]['id'] + ".jpg"
        response = get(url)
        # Process and resize the photo
        b64photo = photo.processPhoto(response)

        # Create tuple of parameters to be inserted to Photo table
        parameters = (current_time, localpresettime, b64photo)
        # Insert values to Photo table
        insertPhoto(parameters)

        # Draw wind direction compass and save it as compass.jpg
        photo.drawArrow(sensors[14]['value'])

        # Get wind speed description
        windspeed = windSpeed(sensors[12]['value'])

        # SensorValueDescriptionFi values
        # - Pouta
        # - Heikko
        # - Kohtalainen
        # - Runsas
        # - Heikko lumi/räntä
        # - Kohtalainen lumi/räntä
        # - Runsas lumi/räntä

        # Create dictionary from api values
        return_value = {"MITTAUSAIKA":localsensortime,
                        sensors[0]['name']:sensors[0]['value'],
                        sensors[12]['name']:sensors[12]['value'],
                        sensors[14]['name']:sensors[14]['value'],
                        sensors[15]['name']:sensors[15]['value'],
                        sensors[16]['name']:sensors[16]['value'],
                        sensors[16]['name']+"_KUVAUS":sensors[16]['sensorValueDescriptionFi'],
                        sensors[16]['name']+"_DESC":sensors[16]['sensorValueDescriptionEn'],
                        "TUULISELITE": windspeed,
                        "KUVAUSAIKA":localpresettime,
                        "KUVA": b64photo}
        
        # DEBUG INFORMATION
        # Print all the sensor data, 85 rows
        # j = 0
        # for i in sensors:
        #     print(j,"\t",i)
        #     j += 1

        # Print the collected sensor data
        # print("\n\n")
        # print(response.json()['dataUpdatedTime'])  #  
        # print("Air temp:",sensors[0]['name'],sensors[0]['value'], 'degrees(C)') 
        # print("Wind speed:",sensors[12]['name'],sensors[12]['value'], 'm/s')
        # print("Wind direction:",sensors[14]['name'],sensors[14]['value'], 'degrees')
        # print("Moisture:",sensors[15]['name'],sensors[15]['value'], "%")
        # print("Rain:",sensors[16]['name'],sensors[16]['value'])
        # print("Rain_kuvaus:", sensors[16]['name']+"_kuvaus", sensors[16]['sensorValueDescriptionFi'])
        # print("Rain_desc:", sensors[16]['name']+"_desc", sensors[16]['sensorValueDescriptionEn'])

    # Return values from sql database
    else:
        # print this to terminal running the framework to see where the data came from
        print("sql")

        # Get wind speed description
        windspeed = windSpeed(weather[3])

        # Create dictionary from sql values
        return_value = {"MITTAUSAIKA":weather[1],
                        "ILMA":weather[2],
                        "KESKITUULI":weather[3],
                        "TUULENSUUNTA":weather[4],
                        "ILMAN_KOSTEUS":weather[5],
                        "SADE":weather[6],
                        "SADE_KUVAUS":weather[7],
                        "SADE_DESC":weather[8],
                        "TUULISELITE":windspeed,
                        "KUVAUSAIKA": photoinfo[1],
                        "KUVA": photoinfo[2]}
    # Return the correct dictionary
    return return_value
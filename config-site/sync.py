import json
from sql import getConfigValues, insertDeviceData
import config

# Get data from device and create json message for the device
def synchronize(seckey, timestamp, temperature, humidity):
    message = dict()
    # Check that security keys match
    if seckey == config.seckey:
        # Only insert data to database if it exists
        if timestamp != '' and temperature != '' and humidity != '':
            values = (timestamp, float(temperature), float(humidity))            
            insertDeviceData(values)
        # Get the configuration values from database to be sent to the device
        values = getConfigValues()
        message["values"] = values
    else:
        # security keys did not match
        message["message"] ="Virheellinen kutsu."
    # Return json message
    return json.dumps(message)
    
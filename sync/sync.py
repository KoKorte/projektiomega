from requests import post
from sql import fromAPI, toAPI
import json
import config

data = dict()

# Get data from database
values = toAPI()
print(values)
# Create POST data
data['seckey'] = config.seckey
data['timestamp'] = values[0]
data['temperature'] = values[1]
data['humidity'] = values[2]

# Get response
response = post(config.url, data=data)
response.close()

# Turn response into dictionary
response = json.loads(response.content)
# Get config values
values = tuple(response['values'])

# Insert new config values to database
fromAPI(values)

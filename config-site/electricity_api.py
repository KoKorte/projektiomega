from datetime import date, datetime, timedelta
from requests import get
from sql import insertElectricityLog, insertElectricityPrices, checkElectricityDate, getTodaysElectricityPrices
import xmltodict
import config

# In this file, we are going to get electricity prices for today and tomorrow (when available)
# To use this feature, you will need to register to the site https://transparency.entsoe.eu/
# and after that, ask permission to use Api by email. You will then generate the needed security token
# and store it to the config.py file as entsoe_securitytoken variable.
# More information here: https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html

# Prices returned with this api call are in €/MWh and do not include the 24% tax. Also with empirical testing
# it would seem that this api call returns hours in CET timezone, so the first price is 0:00 from CET which is
# 1:00 EET

def callAPI(daterange, fetchdate):
    # Code to get electricity prices in Finland
    finland = "10YFI-1--------U"
    # Construct api call
    apiurl = "https://web-api.tp.entsoe.eu/api"
    # Set generated security token to api call
    apiurl += "?securityToken=" + config.entsoe_securitytoken
    apiurl += "&documentType=A44"
    # Set country code to fetch the prices in Finland
    apiurl += "&out_Domain=" + finland
    apiurl += "&in_Domain=" + finland        
    # Set the start and end times to get todays prices using datetuple and adding time itself
    apiurl += daterange    

    # Get the data
    response = get(apiurl)
    
    # Data comes in a horrible xml format, which seems to be a real pain to try and parse with python. Luckily,
    # there is this nice little module that turns xml data to structured collection of dictionaries and 
    # occasional lists, which are a bit easier to navigate through.
    responsedict = xmltodict.parse(response.content)

    # Check that we have correct response before starting to parse the message
    if list(responsedict.keys())[0] == 'Publication_MarketDocument':                        
        parameters = []
        # Hourly prices are inside many Point dictionaries, so we need to loop them through to get the data
        i = 0
        for item in responsedict['Publication_MarketDocument']['TimeSeries']['Period']['Point']: 
            # Since the results start at midnight CET, which is 1 at EET and hour position id in response
            # starts at 1 and goes through to 24, we can use this as our hour position. As this is coded in
            # the normal time, this logic should be double checked when the summer time is in action            
                        
            # Check the price of current 
            if float(item['price.amount']) < 0:
                # Turn price from €/MWh to c/kWh, there is no tax on negative prices
                price = (float(item['price.amount']) / 10)
            else:
                # Turn price from €/MWh to c/kWh and add 24% electricity tax
                price = (float(item['price.amount']) / 10) * 1.24
            # Insert the data into value list as a tuple, so it could be inserted to database easily
            if item['position'] == '24':
                # Last item is the first hour of the next day, so we need to alter the parameters 
                values = (str(fetchdate + timedelta(days=1)), i, 0, price)
            else:    
                values = (str(fetchdate), i, int(item['position']), price)            
            parameters.append(values)
            i += 1        
        # Insert the data to the ElectricityPrices table
        insertElectricityPrices(parameters)
        value = True
    # This is not a valid response that contains values, return with error
    else:        
        value = False
    return value


def getElectricityPrices():
    average = 0
    highest = 0
    tomorrowdata = False
    # Get date as tuple so we can construct period start and end for api call
    datetuple = datetime.now().timetuple()
    year = str(datetuple[0])
    month = str(f'{datetuple[1]:02d}')
    yesterday = str(f'{(datetuple[2] - 1):02d}')
    today = str(f'{(datetuple[2]):02d}')
    tomorrow = str(f'{(datetuple[2] + 1):02d}')
    hour = datetuple[3]    

    # Check if today's electricity prices can be found in database
    check = checkElectricityDate((str(date.today()),))
    # If today's prices are missing, try to get them
    if check == False:
        # Fetch today's electricity prices
        daterange = "&periodStart=" + year + month + yesterday + "2300"
        daterange += "&periodEnd=" + year + month + today + "2300"
        response = callAPI(daterange, date.today())
        # If api call was successful, add the date to the ElectricityLog table
        if response == True:
            insertElectricityLog((year + '-' + month + '-' + today,))
    
    # Check if tomorrow's electricity prices can be found in database
    check = checkElectricityDate((str(date.today() + timedelta(days=1)),))
    # If tomorrow's prices are missing, try to get them, after they have been published at 14:00 EET
    if check == False and hour >= 14:
        # Fetch today's electricity prices
        daterange = "&periodStart=" + year + month + today + "2300"
        daterange += "&periodEnd=" + year + month + tomorrow + "2300"
        response = callAPI(daterange, date.today() + timedelta(days=1))
        # If api call was successful, add the date to the ElectricityLog table
        if response == True:
            # insertElectricityLog((str(date.today() + timedelta(days=1)),))
            insertElectricityLog((year + '-' + month + '-' + tomorrow,))

    # Get todays data from database 
    prices = dict(getTodaysElectricityPrices((year + '-' + month + '-' + today,)))
    average = f'{(sum(prices.values()) / len(prices)):.2f}'
    prices ={k:v for k,v in prices.items() if k >= hour}
    pricenow = prices[hour]
    highest = max(prices, key=prices.get)
    lowest = min(prices, key=prices.get)
    values = {'now': pricenow, 'hour': hour, 'average1': average, 'high_hour1': highest, 'high_price1': prices[highest], 'low_hour1': lowest, 'low_price1': prices[lowest]}
    # values.update({'kukkuu':'pöö', 'test':1})

    # Get tomorrows data from database (if they exist)    
    prices = dict(getTodaysElectricityPrices((year + '-' + month + '-' + tomorrow,)))
    if len(prices) > 0:
        tomorrowdata = True
        average = f'{(sum(prices.values()) / len(prices)):.2f}'        
        highest = max(prices, key=prices.get)
        lowest = min(prices, key=prices.get)
        values.update({'average2': average, 'high_hour2': highest, 'high_price2': prices[highest], 'low_hour2': lowest, 'low_price2': prices[lowest]})
    
    # Insert boolean to tell if tomorrows data is available
    values['tomorrow'] = tomorrowdata
        
    return values

# DEBUG function call
# print(getElectricityPrices())
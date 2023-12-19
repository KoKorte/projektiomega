# This is file is in  development mode, do not use as production server.
# For setting up production service, search "flask deploy to production"

# Folder system
# Root folder holds python files
# - app.py runs the development webserver, default location http://localhost:5000 
# Templates folder holds our template html pages
# - layout.html file holds the webpage template that is implemented on other pages
# - read more about this in the comments of html files
# Static folder is a place holder for our stylesheets, javascripts, images and such
# - Styles folder contains our .css files

# Import needed libraries and functions
from flask import Flask, render_template, request, jsonify
from weather_api import getWeatherData
from electricity_api import getElectricityPrices
from sql import getDeviceData, getConfigValues, insertConfigValues
from sync import synchronize
import config

# Initialize app
app = Flask(__name__)

# Set root folder, this tells what happens when the default location is loaded
@app.route('/', methods = ['GET','POST'])
# Tell flask to render template page index.html
def root():    
    values = getWeatherData() 
    # Only show electricity prices on webpage if they exist       
    if config.show_electricityprices == True:        
       values.update(getElectricityPrices())        
    # Get data from device if they exist and show them on webpage
    devicedata = getDeviceData()
    if devicedata:        
        values['devicetime'] = devicedata[0]
        values['devicetemperature'] = devicedata[1]
        values['devicehumidity'] = devicedata[2]
    return render_template("index.html", values = values)

# Device configuration page
@app.route('/config', methods = ['POST'])
def configuration():    
    # Get configuration values from database
    configvalues = getConfigValues()
    values = {'templow': configvalues[0], 'temphigh': configvalues[1], 'pricelow': configvalues[2], 'pricehigh': configvalues[3]}
    # Check if something has been posted
    if request.method == 'POST' and len(request.form) > 0:
        # Check that all the posted form fields are not empty
        if request.form['templow'] == '' or request.form['temphigh'] == '' or request.form['pricelow'] == '' or request.form['pricehigh'] == '':
            # There are empty form fields            
            values['errormessage'] = "Tapahtui virhe, syötä arvot uudelleen."
        else:
            # Everything checks out, create tuple from form data            
            formvalues = (float(request.form['templow']), float(request.form['temphigh']), float(request.form['pricelow']), float(request.form['pricehigh']))
            print('formvalues:',formvalues)
            # Check if values where changed after pressing the save button
            if formvalues == configvalues:
                # Nothing to change
                values['message'] = "Arvoja ei muutettu, tietoja ei tallennettu."
            else:                
                # Insert new values to database and send them back to config page
                insertConfigValues(formvalues)
                values = {'templow': formvalues[0], 'temphigh': formvalues[1], 'pricelow': formvalues[2], 'pricehigh': formvalues[3], 'message': "Uudet arvot tallennettu."}    
    return render_template("config.html", values = values)

# Simple API page 
@app.route('/dataexchange', methods = ['POST'])
def dataexchange():
    message = ""    
    # Only deal with POST method
    if request.method == 'POST':        
        # Send data from POST to synchronize function to get json message as a result
        message = synchronize(request.form['seckey'],request.form['timestamp'],request.form['temperature'],request.form['humidity'])        
    else:
        # This should never happen
        message = "Virheellinen kutsu. (" + request.method + ")"
    # set the json message on the webpage to be read
    return message
    
# Set app to run with debug on
if __name__ == "__main__":
    app.run(debug=True)

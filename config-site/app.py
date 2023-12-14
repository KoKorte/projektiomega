# This is file is in  development mode, do not use as production server.
# For setting up production service, search "flask deploy to production"

# Folder system
# Root folder holds python files
# - app.py runs the webserver, default location http://localhost:5000 
# Templates folder holds our template html pages
# - layout.html file holds the webpage template that is implemented on other pages
# - read more about this in the comments of html files
# Static folder is a place holder for our stylesheets, javascripts, images and such
# - Styles folder contains our .css files

# Import needed libraries and functions
from flask import Flask, render_template
from weather_api import getWeatherData
from electricity_api import getElectricityPrices
import sqlite3
import config

# Initialize app
app = Flask(__name__)

# Set root folder, this tells what happens when the default location is loaded
@app.route('/')
# Tell flask to render template page index.html
def root():    
    values = getWeatherData()
    if config.show_electricityprices == True:        
        values.update(getElectricityPrices())    
    return render_template("index.html", values = values)


@app.route('/photo')
def photo():
    path = "static/db/website.db"
    conn = sqlite3.connect(path)
    sql = conn.cursor()
    photo = sql.execute("select photo from Test where id = (select max(id) from Test)").fetchone()    
    conn.close()
    return render_template("photo.html", photo = photo)

# Set app to run with debug on
if __name__ == "__main__":
    app.run(debug=True)

This project will start flask framework website development site.

NOTE: this uses pipenv virtual environment, run
    pipenv install 
at root directory to install virtual environment with needed packages.

Needed packages are:
    - flask
    - requests
    - pillow

NOTE: You will need to create this file to root directory of this project
    config.py 
Variables in this file are:
    digitraffic_user = "<insert username here>"         
    show_electricityprices = True or False
    entsoe_securitytoken = "<generated hash>"
    database_path = "<folder outside of this project>"
- Replace <insert username here> with your username in digitraffic_user. You can 
  use anything you want here.
- Also if you wish to get Electricity prices in Finland on the web page, you need 
  to register yourself to entsoe site. Read more in electricity_api.py
- If you do not want to show electricity prices or have not generated security token,
  set show_electricityprices to False, otherwise set it True
- If you have generated security token, insert it to entsoe_securitytoken variable
- Create or select a folder outside of this project and copy the folder path to 
  database_path variable. This app will create database file there when run first time.

To run this website, use command
    py app.py

NOTE: Do NOT use this in production environment, it is not safe! This is intended
for development use only. Search more information:
    flask production environment

There are a lot of comments in the code files, that explain the scripts better. Please
read more from there.

Files in this project:
.gitattributes
.gitignore
    - git configuration files
app.py
    - flask web server, use http://localhost:5000 address in browser when this is running 
config.py
    - you need to create this file, contains digitraffic_user information
photo.py
    - converts traffic cam photo to base64 encoded string and reduces the image size
Pipfile
Pipfile.lock
    - pipenv virtual environment setup files
README.txr
    - this file
sql.py
    - sql commands as functions
    - NOTE! at this point, there is no automatic database cleanup happening, feature is 
      coming soon. 
weather_api.py
    - calls api and return fetched information for the website, if less than 5 minutes 
      has passed, use information from database instead. This is to prevent too many
      api calls to Digitraffic
static/db/db-folder.txt
    - placeholder file, that forces creating db folder. Db folder will hold website.db
      file
static/images/
    - holds image-files used by website
static/styles/default.css
    - css stylesheet file to be used by website
templates/index.html
    - contains root webpage
templates/layout.html
    - contains layout template that other html pages implement
templates/photo.html
    - shows the traffic cam photo for testing purposes

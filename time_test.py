from datetime import datetime
from requests import get
import base64
import sqlite3
import photo

print("-"*80)

dataformat = "%Y-%m-%dT%H:%M:%SZ"
testtime = "2023-11-14T07:55:43Z"
# utctime = datetime.strptime(testtime, dataformat)
utctime = datetime.fromisoformat(testtime)
localtime = datetime.astimezone(utctime)
localtimestr = datetime.strftime(localtime, "%d.%m.%Y %H:%M:%S")

print("testime:\t", type(testtime),"\t"*3, testtime)
print("utctime:\t", type(utctime),"\t", utctime)
print("localtime:\t", type(localtime),"\t", localtime)
print("localtimestr:\t", type(localtimestr),"\t"*3, localtimestr)

print("-"*80)

# url = "https://weathercam.digitraffic.fi/C1261202.jpg"
# response = get(url)
# base64photo = photo.processPhoto(response)
# print(type(base64photo))

# base64photo = ("data:" + response.headers['Content-Type'] + ";base64, " + str(base64.b64encode(response.content).decode("utf-8")))
# print(response.headers['Content-Type'])
# print(len(base64photo))

# path = "static/db/website.db"
# conn = sqlite3.connect(path)
# sql = conn.cursor()
# sql.execute("insert into Test (photo) values (?)", (base64photo,))
# conn.commit()
# conn.close()

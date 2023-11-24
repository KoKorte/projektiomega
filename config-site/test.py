from datetime import date, timedelta
import sqlite3

conn = sqlite3.connect("C:/Koodit/Databases/website.db")
sql = conn.cursor()
sqldate = sql.execute("select date()").fetchone()

print(date.today())
print(str(date.today() + timedelta(days=1)))
print(sqldate[0])

if str(date.today()) == sqldate[0]:
    print("päivät täsmää")
else:
    print("homma kusee")
today = str(date.today())
tulos = sql.execute("select * from ElectricityPrices where PriceDate = ?", (today,)).fetchall()
for i in tulos:
    print(i)

conn.close()

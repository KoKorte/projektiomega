import sqlite3
import config

# Set path to database
path = config.path + "omega.db"

# Handle the incoming data 
def fromAPI(parameters):
    conn = sqlite3.connect(path)
    sql = conn.cursor()
    # Check if table is empty
    clause = "select count(temp_low) from ConfigValues"
    count = sql.execute(clause).fetchone()
    if count == 0:
        # Table is empty, insert the data
        clause = "insert into ConfigValues "
        clause += "(Temp_low, Temp_high, Price_low, Price_high) "
        clause += "values (?, ?, ?, ?)"
    else:
        # Table is not empty, update the data
        clause = "update Configvalues set "
        clause += "Temp_low = ?, "
        clause += "Temp_high = ?, "
        clause += "Price_low = ?, "
        clause += "Price_high = ?"
    sql.execute(clause, parameters)
    conn.commit()
    conn.close()    

# Get the data to be POSTed
def toAPI():
    conn = sqlite3.connect(path)
    sql = conn.cursor()
    clause = "select LoggedTime, Temperature, Humidity "
    clause += "from Temperature "
    clause += "where LoggedTime = (select max(LoggedTime) from Temperature)"
    values = sql.execute(clause).fetchone()
    conn.close()
    return values
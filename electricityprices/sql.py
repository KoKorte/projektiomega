import sqlite3
import config

# Set the path to database file
path = config.database_path + "omega.db"

# Create tables to database if they don't exist already
def createTables():
    conn = sqlite3.connect(path)
    sql = conn.cursor()

    # Create the ElectricityLog table
    clause = "create table if not exists ElectricityLog ("
    clause += "DataFetched date)"
    sql.execute(clause)

    # Create the ElectricityPrices table
    clause = "create table if not exists ElectricityPrices ("
    clause += "EID integer primary key autoincrement, "
    clause += "PriceDate date, "
    clause += "TimeID integert, "
    clause += "DateHour integer, "
    clause += "Price real)"
    sql.execute(clause)

    # Create the Log table
    clause = "create table if not exists Log ("
    clause += "LogID integer primary key autoincrement, "
    clause += "LogTime datetime not null, "
    clause += "Script text not null, "
    clause += "Status integer not null, "
    clause += "StatusMsg text not null)"
    sql.execute(clause)

    # Commit the changes to the database
    conn.commit()
    conn.close()

# Insert date of data gotten from the electricity api call to the table ElectricityLog
def insertElectricityLog(parameters):
    conn = sqlite3.connect(path)
    sql = conn.cursor()
    # Clean up ElectricityLog table of dates older than a week
    clause = "delete from ElectricityLog where DataFetched < date(date(), '-7 days')"
    sql.execute(clause)
    # Insert the data from parameters into the ElectricityLog table
    clause = "insert into ElectricityLog (DataFetched) values (?)"
    sql.execute(clause, parameters)
    # Commit the changes to the database
    conn.commit()
    conn.close()

# Insert data from the electricity api call to the table ElectricityPrices
def insertElectricityPrices(parameters):
    conn = sqlite3.connect(path)
    sql = conn.cursor()
    # Clean up ElectricityPrices table
    clause = "delete from ElectricityPrices where PriceDate < date(date(), '-7 days')"
    sql.execute(clause)
    # Insert the data from parameters to the ElectricityPrices table
    clause = "insert into ElectricityPrices "
    clause += "(PriceDate, TimeID, DateHour, Price) "
    clause += "values (?, ?, ?, ?)"
    # This time parameters is a list of tuples, so we need to use the executemany function
    sql.executemany(clause, parameters)
    # Commit the changes to the database
    conn.commit()
    conn.close()

# Insert log stamp
def insertLogStamp(parameters):
    conn = sqlite3.connect(path)
    sql = conn.cursor()
    # Clean up Log table
    clause = "delete from Log where LogTime < date(date(), '-2 months')"
    sql.execute(clause)
    # Insert data to Log Table
    clause = "insert into Log "
    clause += "(LogTime, Script, Status, StatusMsg) "
    clause += "values (datetime(), ?, ?, ?)"
    sql.execute(clause, parameters)
    # Commit the changes to the database
    conn.commit()
    conn.close()
    
# Check if given date can be found in ElectricityLog table
def checkElectricityDate(parameters):
    conn = sqlite3.connect(path)
    sql = conn.cursor()
    # Check if date is in database
    clause = "select count(DataFetched) from ElectricityLog where DataFetched = ?"
    value = sql.execute(clause, parameters).fetchone()
    conn.close()
    if value[0] == 0:
        return False
    else:
        return True
    

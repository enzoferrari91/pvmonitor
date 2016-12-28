from __future__ import print_function 
import sqlite3
import time
from datetime import datetime
import config

def getDateToday():
	dateToday = time.strftime("%Y-%m-%d")
	return(dateToday)

print("Write new data to database...",end="")

db = sqlite3.connect(config.dbfilepath)
cur = db.cursor()

dateToday = getDateToday()
datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))

cur.execute("SELECT * FROM powerLog WHERE datetime LIKE ?", (dateToday+'%' ,))
data = cur.fetchall()

power_bez = list(zip(*data)[1])
power_einsp = list(zip(*data)[2])
power_pv = list(zip(*data)[3])

if(len(power_bez) == 288 & len(power_einsp) == 288 & len(power_pv) == 288):
	status = 1
else:
	status = 0

energy_bez = round( sum([(i/12)/1000 for i in power_bez]), 0 ) 		# 5 minute intervall = factor 12
energy_einsp = round( sum([(i/12)/1000 for i in power_einsp]), 0 ) 	# 5 minute intervall = factor 12
energy_pv = round( sum([(i/12)/1000 for i in power_pv]), 1 ) 		# 5 minute intervall = factor 12

sql_insert = ("""INSERT INTO dayLog (datetime,energy_bez,energy_einsp,energy_pv,status) VALUES (?,?,?,?,?)""",(datetimeWrite,energy_bez,energy_einsp,energy_pv,status))
cur.execute(*sql_insert)
db.commit()
db.close()

print("OK!")
print("Status data...",end="")
print(status)
print(datetimeWrite)


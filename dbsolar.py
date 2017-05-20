from datetime import datetime
from datetime import timedelta
import sqlite3
import csv
import config

base = "2017-01-01 00:00"
base = datetime.strptime(base,"%Y-%m-%d %H:%M")

date_list = [base + timedelta(minutes=5*x) for x in range(0, 12*24*365)]
date_list = [datetime.strftime(x, "%Y-%m-%d %H:%M") for x in date_list]

solar_list = list()
with open('solar.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		solar_list.append(float(row[0]))

out = list()
out.append(date_list)
out.append(solar_list)
data_list = zip(*out)

db = sqlite3.connect(config.dbfilepath)
cur = db.cursor()
for row in data_list:
	sql_insert = ("""INSERT INTO solarLog (datetime, solar) VALUES (?,?)""",(row[0],row[1]))
	cur.execute(*sql_insert)
	db.commit()
db.close()
print("DATABASE - OK!")
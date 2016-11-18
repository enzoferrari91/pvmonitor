import json
import requests
from datetime import datetime
from datetime import timedelta
from dateutil import tz
import sqlite3
import config

def UTCtoCET(timestampUTC):
	#timestampUTC = datetime.strptime(timestampUTC, '%Y-%m-%d %H:%M:%S')
	# Tell the datetime object that it's in UTC time zone since 
	# datetime objects are 'naive' by default
	timestampUTC = timestampUTC.replace(tzinfo=from_zone)
	# Convert time zone
	timestampCET = timestampUTC.astimezone(to_zone)
	timestampCET = datetime.strftime(timestampCET, '%Y-%m-%d %H:%M')
	return(timestampCET)

def savetoDB(db_data):
	db = sqlite3.connect(config.dbfilepath)
	cur = db.cursor()

	for row in db_data:
		sql_insert = ("""INSERT INTO forecastLogAPI (datetime, ghi_sfc) VALUES (?,?)""",
						(row[0],row[1]))
		cur.execute(*sql_insert)
		db.commit()

	db.close()
	print("DATABASE - OK!")


f = open(config.apifilepath,"r")
API_KEY = f.read()
f.close()

# Zwettl
lat = config.lat
lon = config.lon
from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Europe/Vienna')

var = "Downward_Short-Wave_Radiation_Flux_surface"
count=10

today = datetime.today()
yesterday = today - timedelta(days=1)
url_date = datetime.strftime(yesterday, '%Y-%m-%d')

timestamp_base = datetime(today.year, today.month, today.day, 0, 0, 0, 0)
timestamp_list = [timestamp_base + timedelta(hours=x*3) for x in range(0, 8)]
timestamp_list = [UTCtoCET(timestamp) for timestamp in timestamp_list]

url = ( "http://api.planetos.com/v1/datasets/noaa_gfs_global_sflux_0.12d/point?" +
		"apikey=" + API_KEY +
		"&lat="   + str(lat) +
		"&lon="   + str(lon) + 
		"&var="   + var +
		"&reftime_start=" + url_date + "T18:00:00Z&count=" + str(count) )

print(url)

r = requests.get(url)
data = json.loads(r.text)

time=list()
ghi=list()

out=list()
out.append(timestamp_list)

for x in range(2,count):
	time.append(data['entries'][x]['axes']['time'])
	ghi.append(data['entries'][x]['data'][var])

out.append(ghi)
print(time)
print(timestamp_list)
print(ghi)

dataDB = zip(*out)
savetoDB(dataDB)
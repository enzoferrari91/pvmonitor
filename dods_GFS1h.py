import requests
import re
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
		sql_insert = ("""INSERT INTO forecastLog (datetime, cloud_cover_total, temp_gnd, u_wind_gnd, v_wind_gnd, ghi_sfc) VALUES (?,?,?,?,?,?)""",
						(row[0],row[1], row[2], row[3], row[4], row[5]))
		cur.execute(*sql_insert)
		db.commit()

	db.close()
	print("DATABASE - OK!")

# --------------------------------------------------------------------
# "tcdcclm"  ...  entire atmosphere total cloud cover [%]
# "tmp2m"    ...  2 m above ground temperature [k] 
# "ugrd10m"  ...  10 m above ground u-component of wind [m/s] 
# "vgrd10m"  ...  10 m above ground v-component of wind [m/s]
# "dswrfsfc" ...  surface downward short-wave radiation flux [w/m^2] 
# --------------------------------------------------------------------
variables = ["tcdcclm","tmp2m", "ugrd10m", "vgrd10m" ,"dswrfsfc"]

# --------------------------------------------------------------------
# "12z" ... 1200 UTC run day n --> day n+1 00:00 - 21:00 UTC 
# "18z" ... 1800 UTC run day n --> day n+1 00:00 - 21:00 UTC
# --------------------------------------------------------------------
modelrun = {"12z" : "[12:35]", "18z" : "[6:29]"}

# Zwettl
lat = 48.50
lon = 15.25

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Europe/Vienna')

today = datetime.today()
yesterday = today - timedelta(days=1)

timestamp_base = datetime(today.year, today.month, today.day, 0, 0, 0, 0)
timestamp_list = [timestamp_base + timedelta(hours=x) for x in range(0, 23)]
timestamp_list = [UTCtoCET(timestamp) for timestamp in timestamp_list]

url_date = str(yesterday.year) + str(yesterday.month) + str(yesterday.day)
url_lat = str(int(360 + lat / 0.25))
url_lon = str(int(lon / 0.25))


print("Forecast start date: " + url_date)


out=list()
out.append(timestamp_list)

for v in variables:

	print("Download: " + v)
	url = ("http://nomads.ncep.noaa.gov:9090/dods/gfs_0p25_1hr/gfs"  + 
			url_date + "/gfs_0p25_1hr_18z.ascii?" + v + modelrun["18z"] +
			"[" + url_lat + ":" + url_lat + "]" +
			"[" + url_lon + ":" + url_lon + "]")
	print(url)
	r = requests.get(url)
	data = r.text
	if "error" not in data:
		print("OK")
	else:
		print("ERROR - Dateset not available...using previous modelrun '12z' instead...")
		url = ("http://nomads.ncep.noaa.gov:9090/dods/gfs_0p25/gfs"  + 
		url_date + "/gfs_0p25_1hr_12z.ascii?" + v + modelrun["12z"] +
		"[" + url_lat + ":" + url_lat + "]" +
		"[" + url_lon + ":" + url_lon + "]")
		print(url)
		r = requests.get(url)
		data = r.text

	end = data.index("time")
	data = data[0:end]
	data = str(data)
	data = data.replace("\n","")
	data = data.replace(" ","")
	data = re.sub("[\(\[].*?[\)\]]","",data)
	datalist = data.split(",")
	datalist = datalist[2:26]
	datalist = [float(x) for x in datalist]
	print(datalist)
	out.append(datalist)

dataDB = zip(*out)
savetoDB(dataDB)




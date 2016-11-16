from siphon.catalog import TDSCatalog
from siphon.ncss import NCSS
from datetime import datetime, timedelta
from dateutil import tz
from netCDF4 import num2date

import time
import sqlite3
import config

import csv

def savetoDB(db_data):
	db = sqlite3.connect(config.dbfilepath)
	cur = db.cursor()

	for row in db_data:
		sql_insert = ("""INSERT INTO forecastLog (datetime, cloud_cover_total, temp_gnd, u_wind_gnd, v_wind_gnd, ghi_sfc) VALUES (?,?,?,?,?,?)""",
						(row[0],row[1], row[2], row[3], row[4], row[5]))
		cur.execute(*sql_insert)
		db.commit()

	db.close()
	print("OK!")

def UTCtoCET(timestampUTC):
	#timestampUTC = datetime.strptime(timestampUTC, '%Y-%m-%d %H:%M:%S')
	# Tell the datetime object that it's in UTC time zone since 
	# datetime objects are 'naive' by default
	timestampUTC = timestampUTC.replace(tzinfo=from_zone)
	# Convert time zone
	timestampCET = timestampUTC.astimezone(to_zone)
	timestampCET = datetime.strftime(timestampCET, '%Y-%m-%d %H:%M')
	return(timestampCET)

def convert_csv(data, variables):
	out = list()
	for v in variables:
		temp_data = data.variables[v]
		if v == "time":
			array_data = num2date(temp_data[:].squeeze(), temp_data.units)
			list_data = array_data.tolist()
			list_data = [UTCtoCET(dateUTC) for dateUTC in list_data]
		else:
			array_data = temp_data[:].squeeze()
			list_data = array_data.tolist()
		if v == "Temperature_height_above_ground" or v == "u-component_of_wind_height_above_ground" or v == "v-component_of_wind_height_above_ground":
			out.append(zip(*list_data)[0])
		else:
			out.append(list_data)
	return(zip(*out))

def start_end():
	x = datetime.utcnow() + timedelta(days=1) # DEBUGGING
	#x = datetime.utcnow() - timedelta(days=1)
	start = datetime(x.year, x.month, x.day, 0, 0, 0, 0)
	end = start + timedelta(hours=21)
	return(start, end)

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Europe/Vienna')

variables = [ 	
				"time",
				"Total_cloud_cover_entire_atmosphere_Mixed_intervals_Average",
				"Temperature_height_above_ground",
				"u-component_of_wind_height_above_ground",
				"v-component_of_wind_height_above_ground",
				"Downward_Short-Wave_Radiation_Flux_surface_Mixed_intervals_Average"
			]

# Zwettl
lon = 48.50
lat = 15.25
start, end = start_end()
print("Start/UTC: " + str(start))
print("End  /UTC: " + str(end))

latest_gfs = TDSCatalog("http://thredds.ucar.edu/thredds/catalog/grib/NCEP/GFS/Global_0p25deg/latest.xml")
latest_ds = list(latest_gfs.datasets.values())[0]
ncss = NCSS(latest_ds.access_urls['NetcdfSubset'])

query = ncss.query()
query.lonlat_point(lat,lon)
query.time_range(start,end)
query.variables(variables[1],variables[2],variables[3],variables[4],variables[5])
query.accept('netcdf4')

print("Download: " + latest_ds.access_urls['NetcdfSubset'])
data = ncss.get_data(query)

db_data = convert_csv(data,variables)

print db_data

savetoDB(db_data)


#csv_data = convert_csv(data,variables)
#csv_data.insert(0,variables)

#with open("output.csv", "wb") as f:
#    writer = csv.writer(f)
#    writer.writerows(csv_data)

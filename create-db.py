import sqlite3
import os
import config

print("Create database...")

db = sqlite3.connect(config.dbfilepath)
cur = db.cursor()
try:
	cur.execute("CREATE TABLE powerLog(datetime DATETIME NOT NULL, power_bez FLOAT(7,2), power_einsp FLOAT(7,2), power_pv FLOAT(7,2));")
except:
	print("Table 'powerLog' already exists.")

try:
	cur.execute("CREATE TABLE dayLog(datetime DATETIME NOT NULL, energy_bez FLOAT(7,2), energy_einsp FLOAT(7,2), energy_pv FLOAT(7,2));")
except:
	print("Table 'dayLog' already exists.")

try:
	cur.execute("CREATE TABLE forecastLog(datetime DATETIME NOT NULL, cloud_cover_total FLOAT(7,2), temp_gnd FLOAT(7,2), u_wind_gnd FLOAT(7,2), v_wind_gnd FLOAT(7,2), ghi_sfc FLOAT(7,2));")
except:
	print("Table 'forecastLog' already exists.")

try:
	cur.execute("CREATE TABLE forecastLogAPI(datetime DATETIME NOT NULL, ghi_sfc FLOAT(7,2));")
except:
	print("Table 'forecastLogAPI' already exists.")

db.close()

print("Database sucessfully created!")

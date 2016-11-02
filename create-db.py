import sqlite3
import os



print("Create database...")

if(os.path.isfile('./power.db)')):
	print("Database 'power.db' already exists.")

else:
	db = sqlite3.connect("power.db")
	cur = db.cursor()
	cur.execute("CREATE TABLE powerLog(datetime DATETIME NOT NULL, power_bez FLOAT(7,2), power_einsp FLOAT(7,2), power_pv FLOAT(7,2));")
	db.close()
	print("Database sucessfully created!")
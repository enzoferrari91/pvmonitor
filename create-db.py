import sqlite3
import os
import config

print("Create database...")

db = sqlite3.connect(config.dbfilepath)
cur = db.cursor()
cur.execute("CREATE TABLE powerLog(datetime DATETIME NOT NULL, power_bez FLOAT(7,2), power_einsp FLOAT(7,2), power_pv FLOAT(7,2));")
db.close()

print("Database sucessfully created!")

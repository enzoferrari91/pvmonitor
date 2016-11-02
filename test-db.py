import sqlite3
import time
import random

db = sqlite3.connect("/home/pi/Desktop/python/hoelzl/power.db")

cur = db.cursor()

dateToday = time.strftime("%Y-%m-%d ")

cur.execute("SELECT * FROM powerLog WHERE datetime LIKE ?", (dateToday+'%' ,))

data = cur.fetchall()
power_bez = list(zip(*data)[1])
power_einsp = list(zip(*data)[2])
power_pv = list(zip(*data)[3])
timestampList = list(zip(*data)[0])

print power_bez
print power_einsp
print power_pv
print timestampList

db.close()
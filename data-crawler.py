from __future__ import print_function 
import serial
import time
import sys
import sqlite3
import config

serialElster = '/dev/ttyUSB0'  # Serial port for Elster AS 1440
serialArduino = '/dev/ttyACM0' # Serial port for Arduino

def extractobis(data,obis):
  start = data.index(obis)
  return float(data[(start+6):(start+14)])

def send(port, bytes, tr): 
  port.write(bytes)
  time.sleep(tr)
  
def readElster():
  tr = 0.2

  try:
    Elster=serial.Serial(port=serialElster, baudrate=300, bytesize=7, parity='E', stopbits=1, timeout=1.5, dsrdtr=True)
    time.sleep(tr)
    Request_message='/?!\r\n'
    send(Elster, Request_message, tr)
    time.sleep(3)

    datablock = ""
    x = Elster.read()
    while(x != '!'):
      datablock = datablock + x
      x = Elster.read()

    Elster.close()
    print("Result OK!")
    return datablock

  except:
    print("Some error reading data")
    if (Elster.isOpen()):
      Elster.close()
    return ""

def readArduino(msg):
  print ("Open serial port /dev/tty/ACM0...", end="")
  Arduino=serial.Serial(port=serialArduino, baudrate=9600)
  time.sleep(2)

  send(Arduino, msg, 0.5)
  print("Ready to receive...",end="")

  data=""
  c = Arduino.read()
  while c != "!":
    data = data + c
    c = Arduino.read()
    
  print("Result OK!")
  power = round(float(data),2) 
  return power


print("Starting communication!")
print("ARDUINO...",end="")
power_pv = readArduino("?")   # W
if power_pv < 70:             # Threshold for Power
  power_pv = 0


"""
print("ELSTER...",end="")
data = readElster()

####################################################
zst_bez = extractobis(data,"1.8.1")
zst_einsp = extractobis(data,"2.8.1")
temp_zst = str(zst_bez) + ";" + str(zst_einsp)

print("ZST: ", end="")
print(temp_zst)

f = open('temp_zst.txt' , 'r')
s = f.read()
f.close()

s = s.split(";")
old_zst_list = [float(i) for i in s]

energy_bez =   (zst_bez - old_zst_list[0])     # kWh
energy_einsp = (zst_einsp - old_zst_list[1])   # kWh

power_bez =   (energy_bez * 12 * 1000)   # W (12 * 5-minutes per hour)
power_einsp = (energy_einsp * 12 * 1000) # W

f = open(config.zstfilepath, 'w')
f.write(temp_zst)
f.close()

print("Leistungen:")
print(power_bez)
print(power_einsp)
####################################################
"""

print("Write new data to database...",end="")
db = sqlite3.connect(config.dbfilepath)
cur = db.cursor()
datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))

#sql_insert = ("""INSERT INTO powerLog (datetime,power_bez,power_einsp,power_pv) VALUES (?,?,?,?)""",(datetimeWrite,power_bez,power_einsp,power_pv))
sql_insert = ("""INSERT INTO powerLog (datetime,power_pv) VALUES (?,?)""",(datetimeWrite,power_pv))
cur.execute(*sql_insert)
db.commit()
db.close()
print("OK!")

print("Sucessfully finished all tasks!")
print(datetimeWrite)






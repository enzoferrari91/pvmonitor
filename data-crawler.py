from __future__ import print_function 
import serial
import time
import sys
import sqlite3
import config

#serialElster = '/dev/ttyUSB0'  # Serial port for Elster AS 1440
serialArduino = '/dev/ttyACM0' # Serial port for Arduino

def extractobis(data,obis):
  start = data.index(obis)
  return float(data[(start+6):(start+14)])

def extractobisvoltage(data,obis):
  start = data.index(obis)
  return float(data[(start+7):(start+12)])

def send(port, bytes, tr): 
  port.write(bytes)
  time.sleep(tr)
  
def readElster():
  ACK = '\x06'
  STX = '\x02'
  ETX = '\x03'
  tr = 0.2

  try:

    Elster=serial.Serial(port=serialElster, baudrate=300, bytesize=7, parity='E', stopbits=1, timeout=1.5, dsrdtr=True)
    time.sleep(tr)
    Request_message='/?!\r\n'
    send(Elster, Request_message, tr)
    time.sleep(tr)

    Identification_message=Elster.readline()

    if (len(Identification_message) < 1 or Identification_message[0] != '/'):
      print("No Identification message")
      Elster.close()
      return ""
    if (len(Identification_message) < 7):
      print("Identification message to short")
      Elster.close()
      return ""
    if (Identification_message[4].islower()):
      tr = 0.02
    manufacturers_ID = Identification_message[1:4]
    if (Identification_message[5] == '\\'):
      identification = Identification_message[7:-2]
    else:
      identification = Identification_message[5:-2]
    
    speed = Identification_message[4]

    if (speed == "1"): new_baud_rate = 600
    elif (speed == "2"): new_baud_rate = 1200
    elif (speed == "3"): new_baud_rate = 2400
    elif (speed == "4"): new_baud_rate = 4800
    elif (speed == "5"): new_baud_rate = 9600
    elif (speed == "6"): new_baud_rate = 19200
    else:
      new_baud_rate = 300
      speed = "0"

    print("Identification message OK...", end="")
    Acknowledgement_message=ACK + '0' + speed + '0\r\n'
    send(Elster, Acknowledgement_message, tr)
    Elster.baudrate=new_baud_rate
    time.sleep(tr)

    datablock = ""
    if (Elster.read() == STX):
    	x = Elster.read()
    	BCC = 0
    	while (x  != '!'):
    		BCC = BCC ^ ord(x)
    		datablock = datablock + x
    		x = Elster.read()
    	while (x  != ETX):
    		BCC = BCC ^ ord(x) # ETX itself is part of block check
    		x = Elster.read()
    	BCC = BCC ^ ord(x)
    	x = Elster.read() # x is now the Block Check Character

    	# last character is read, could close connection here
    	if (BCC != ord(x)): # received correctly?
    		datablock = ""
    		print("Result not OK, try again")

    	print("Result OK!")

    else:
      print("No STX found, not handled.")

    Elster.close()
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
#print("ELSTER...",end="")
#data = readElster()

#zst_bez_night = extractobis(data,"1.8.1")
#zst_bez_day   = extractobis(data,"1.8.2")
#zst_einsp_night = extractobis(data,"2.8.1")
#zst_einsp_day   = extractobis(data,"2.8.2")
#temp_zst = str(zst_bez_night) + ";" + str(zst_bez_day) + ";" + str(zst_einsp_night) + ";" + str(zst_einsp_day)

#u1 = extractobisvoltage(data,"32.7.0")
#u2 = extractobisvoltage(data,"52.7.0")
#u3 = extractobisvoltage(data,"72.7.0")
#msg = str(u1) + ";" + str(u2) + ";" + str(u3)

print("ARDUINO...",end="")
power_pv = readArduino("?")   # W
if power_pv < 70:             # Threshold for Power
  power_pv = 0

################################################################################################
#f = open('temp_zst.txt' , 'r')
#s = f.read()
#f.close()

#s = s.split(";")
#old_zst_list = [float(i) for i in s]

#energy_bez =   (zst_bez_night - old_zst_list[0]) + (zst_bez_day - old_zst_list[1])       # kWh
#energy_einsp = (zst_einsp_night - old_zst_list[2]) + (zst_einsp_day - old_zst_list[3])   # kWh

#power_bez =   (energy_bez * 60)   # kW (60 minutes per hour)
#power_einsp = (energy_einsp * 60) # kW

#f = open('temp_zst.txt', 'w')
#f.write(temp_zst)
#f.close()
################################################################################################

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






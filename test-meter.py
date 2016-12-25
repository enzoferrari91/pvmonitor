from __future__ import print_function 
import serial
import time
import sys

serialElster = '/dev/ttyUSB0'  # Serial port for Elster AS 1440


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


print("Starting communication!")
print("ELSTER...",end="")
data = readElster()
print(data)
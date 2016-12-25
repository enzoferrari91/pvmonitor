from __future__ import print_function 
import serial
import time
import sys

serialport = '/dev/ttyUSB0'  # Serial port for Elster AS 1440

def send(port, bytes, tr): 
  port.write(bytes)
  time.sleep(tr)
  
def read_datablock():
  ACK = '\x06'
  STX = '\x02'
  ETX = '\x03'
  tr = 0.2

  try:

    Elster=serial.Serial(port=serialport, baudrate=300, bytesize=7, parity='E', stopbits=1, timeout=1.5, dsrdtr=True)
    time.sleep(tr)
    Request_message='/?!\r\n'
    send(Elster, Request_message, tr)
    print("Sende Request")
    
    Identification_message=Elster.readline()
    print(Identification_message)
    
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

    Acknowledgement_message=ACK + '0' + speed + '0\r\n'
    send(Elster, Acknowledgement_message, tr)
    Elster.baudrate=new_baud_rate
    time.sleep(tr)




    #time.sleep(3)

    datablock = ""
    x=Elster.read()
    while (x  != '!'):
      datablock = datablock + x
      x = Elster.read()
      print(x,end="")
      
    return datablock
  
  except:
    print("Some error reading data")
    if (Elster.isOpen()):
      Elster.close()
    return ""

data = read_datablock()
print (data)
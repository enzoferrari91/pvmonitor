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

    Elster=serial.Serial(port=serialport, baudrate=4800, bytesize=7, parity='E', stopbits=1, timeout=1.5, dsrdtr=True)
    time.sleep(tr)
    Request_message='/?!\r\n'
    send(Elster, Request_message, tr)
    print("Sende Request")
    time.sleep(3)

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
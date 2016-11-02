from __future__ import print_function
import serial
import time
import sys

serialport = '/dev/ttyACM0'

def send(port, bytes, tr):
  port.write(bytes)
  time.sleep(tr)

tr=0.2
Request_message='?'

print ("Starte seriellen Port /dev/tty/ACM0...")
Elster=serial.Serial(port=serialport, baudrate=9600)
time.sleep(2)
print("Empfange..")

send(Elster, Request_message, tr)
time.sleep(tr)


c = Elster.read()
while c != "!":
        print(c,end="")
        c = Elster.read()

print("\nEnde")


  

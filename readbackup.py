#!/usr/bin/python
import serial

loclist = {}

with serial.Serial(port='/dev/mdrrc2',baudrate=115200, timeout=1) as ser:
  ser.write('LOCLIST\r')
  l = ser.read(2000)
  ser.close()

locdump=l.splitlines()
for d in locdump:
  for offset in [0,18,36]:
    a=d[offset:offset+18]
    if (a[0:4].strip().isdigit()):
       if (a[5:8]) == 'DCC':
          loclist[int(a[0:4].strip())]=[a[9:18],'DCC']
       elif (a[6:8]) == 'MM':
          loclist[int(a[0:4].strip())]=[a[9:18],'MM']

# loclist.sort()
print("Address".ljust(10)+"Name".ljust(10)+"Protocol")
for l in loclist:
  print(str(l).ljust(10)+loclist[l][0].ljust(10)+loclist[l][1])

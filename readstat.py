#!/usr/bin/python
import serial
with serial.Serial(port='/dev/mdrrc2',baudrate=115200, timeout=1) as ser:
#  ser.write('L1')
  ser.write(bytes(0xa5))
  ser.write('\n')
  s = ser.read(2000)
  print(s)
  ser.close()

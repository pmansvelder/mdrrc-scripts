#!/usr/bin/python
import serial
with serial.Serial(port='/dev/mdrrc2',baudrate=115200, timeout=1) as ser:
  ser.write('STAT\r')
  s = ser.read(2000)
  print(s)
  ser.close()

#!/usr/bin/python
import serial

with serial.Serial(port='/dev/mdrrc2',baudrate=115200, timeout=1) as ser:
  ser.write(bytes(0xA5))
  ser.write('\r')
  ser.close()


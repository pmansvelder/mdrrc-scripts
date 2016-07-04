#!/usr/bin/python
import mdrrc2serial
import locgrid
import copy

def PrintLocList(loclist):
  print("Address".ljust(10)+"Name".ljust(10)+"Protocol")
  for l in loclist:
    print(str(l).ljust(10)+loclist[l][0].ljust(10)+loclist[l][1])

loclist = mdrrc2serial.ParseLocList()
if len(loclist) > 0:
#  PrintLocList(loclist)
  locgrid.LocGrid(loclist)
#  mdrrc2serial.StopConfig()
else:
  app = wx.PySimpleApp()
  Foutmelding(None, 'Centrale not in config mode or not connected!')
  print("Not able to read loclist from controller...")
  print("Make sure MDRRC-II controller is connected and set to config mode (SET->CON)...")


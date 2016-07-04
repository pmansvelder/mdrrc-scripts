import serial
import ConfigParser as cf
import os

config = cf.ConfigParser()
config.read('settings.cfg')

mdrrc2_port = config.get('Connection', 'port').encode('ascii','ignore')
mdrrc2_baud = config.get('Connection', 'speed').encode('ascii','ignore')

def TestConnection():
  try:
    with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
      ser.write('HELP\r')
      locdata = ser.read(2000)
      ser.close()
      return True
  except:
      return False

def ReceiveLocList():
  with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
    ser.write('LOCLIST\r')
    locdata = ser.read(2000)
    ser.close()
    return locdata

def ChangeLocName(address, newname):
  with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
    ser.write('LOCNAME '+str(address)+' '+newname+'\r')
    ser.close()

def ChangeLocType(address):
  with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
    ser.write('LOCTYPE '+str(address)+'\r')
    ser.close()
    
def AddLoco(address):
  with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
    ser.write('LOCADD '+str(address)+'\r')
    message = ser.read(255)
    ser.close()
    return message

def StopConfig():
  with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
    ser.write('EXIT\r')
    ser.close()

def StoreConfig():
  with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
    ser.write('STORE\r')
    ser.close()

def ParseLocList():
  loclist = {}
  locdump=ReceiveLocList().splitlines()
  for d in locdump:
    for offset in [0,18,36]:
      a=d[offset:offset+18]
      if (a[0:4].strip().isdigit()):
        if (a[5:8]) == 'DCC':
          loclist[int(a[0:4].strip())]=[a[9:18],'DCC']
        elif (a[6:8]) == 'MM':
          loclist[int(a[0:4].strip())]=[a[9:18],'MM']
  return loclist

def ReadConfig():
  configlist = {}
  with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
    ser.write('STAT\r')
    configdata = ser.read(2000)
    ser.close()
  for l in configdata.splitlines():
    if len(l.split(':')) > 1:
      key = l.split(':')[0].strip()
      value = l.split(':')[1].strip()
      configlist[key]=value
  return configlist

def ChangeConfig(key, value, configlist):
  for k in configlist:
    if key == k:
      print('Old value: '+configlist[k])
      print('New value: '+value)
      with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
        if k == 'S88 frequency':
          ser.write('S88FREQ'+' '+str(value)+'\r')
        elif k == 'S88 Number of units':
          ser.write('S88NR'+' '+str(value)+'\r')
        elif k == 'MM locs only':
          ser.write('MML'+'\r')
        elif k == 'Turnout DCC Only':
          ser.write('DCCT'+'\r')
        elif k == 'Turnout auto off':
          ser.write('AUTO_OFF'+'\r')
        elif k == 'Booster S/C enable':
          ser.write('BOOSTERENABLESC'+'\r')
        elif k == 'Booster S/C change':
          ser.write('BOOSTERSC'+'\r')
        elif k == 'Booster S/C delay time':
          ser.write('BOOSTERDELAY='+str(value)+'\r')
        elif k == 'Acknowlegde enable':
          ser.write('ACK'+'\r')
        elif k == 'I2C manual control':
          ser.write('I2C'+'\r')
        elif k == 'XPressNet':
          ser.write('XP'+'\r')
        ser.close()

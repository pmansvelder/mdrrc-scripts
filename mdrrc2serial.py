import serial
import ConfigParser as cf
import os

def ReadConfigParams():
  config = cf.ConfigParser()
  config.read('settings.cfg')
  port = config.get('Connection', 'port').encode('ascii','ignore')
  speed = config.get('Connection', 'speed').encode('ascii','ignore')
  return (port, speed)

def ReadVersionParams():
  config = cf.ConfigParser()
  config.read('settings.cfg')
  try:
    spacing = int(config.get('Format', 'spacing').encode('ascii','ignore'))
  except:
    spacing = 18
  return (spacing)

def TestConnection():
  (mdrrc2_port,mdrrc2_baud) = ReadConfigParams()
  try:
    with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
      ser.write('HELP\r')
      locdata = ser.read(2000)
      ser.close()
      return True
  except:
      return False

def ReceiveLocList():
  (mdrrc2_port,mdrrc2_baud) = ReadConfigParams()
  with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
    ser.write('LOCLIST\r')
    locdata = ser.read(2000)
    ser.close()
    return locdata

def ChangeLocName(address, newname):
  (mdrrc2_port,mdrrc2_baud) = ReadConfigParams()
  with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
    ser.write('LOCNAME '+str(address)+' '+newname+'\r')
    ser.close()

def ChangeLocType(address, protocol):
  (mdrrc2_port,mdrrc2_baud) = ReadConfigParams()
  with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
    if protocol == 'DCC14':
      ser.write('14DCC '+str(address)+'\r')
    elif protocol == 'DCC128':
      ser.write('128DCC '+str(address)+'\r')
    else:
      ser.write('LOCTYPE '+str(address)+'\r')
    ser.close()

def AddLoco(address):
  (mdrrc2_port,mdrrc2_baud) = ReadConfigParams()
  with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
    ser.write('LOCADD '+str(address)+'\r')
    message = ser.read(255)
    ser.close()
    return message

def RemoveLoco(address):
  (mdrrc2_port,mdrrc2_baud) = ReadConfigParams()
  with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
    ser.write('LOCDEL '+str(address)+'\r')
    message = ser.read(255)
    ser.close()
    return message

def StopConfig():
  (mdrrc2_port,mdrrc2_baud) = ReadConfigParams()
  with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
    ser.write('EXIT\r')
    ser.close()

def StoreConfig():
  (mdrrc2_port,mdrrc2_baud) = ReadConfigParams()
  with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
    ser.write('STORE\r')
    ser.close()

def ParseLocList():
  (mdrrc2_port,mdrrc2_baud) = ReadConfigParams()
  loclist = {}
  spacing = ReadVersionParams()
  locdump=ReceiveLocList().splitlines()
  for d in locdump:
    for offset in [0,spacing,spacing*2]:
      a=d[offset:offset+spacing]
      if a != '' :
              listitem = a.split(None,2)
              if listitem:
                if (listitem[0]).isdigit():
                  try:
                    loclist[listitem[0]]=[listitem[2],listitem[1]]
                  except:
                    loclist[listitem[0]]=['',listitem[1]] 
  return loclist

def ReadConfig():
  (mdrrc2_port,mdrrc2_baud) = ReadConfigParams()
  configlist = {}
  with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
    ser.write('STAT\r\n')
    configdata = ser.read(4000)
    ser.close()
  for l in configdata.splitlines():
    if len(l.split(':')) > 1:
      key = l.split(':')[0].strip()
      value = l.split(':')[1].strip()
      configlist[key]=value
  return configlist

def ChangeConfig(key, value, configlist):
  (mdrrc2_port,mdrrc2_baud) = ReadConfigParams()
  for k in configlist:
    if key == k:
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
        elif k == 'Text colour':
          ser.write('CF'+str(value)+'\r')
        elif k == 'Background colour':
          ser.write('CB'+str(value)+'\r')
        ser.close()
        
def SendCommand(command):
  (mdrrc2_port,mdrrc2_baud) = ReadConfigParams()
  with serial.Serial(port=mdrrc2_port,baudrate=mdrrc2_baud, timeout=1) as ser:
    ser.write(command)
    message = ser.read(63)
    for i in range(0, len(message)):
      print i,':',hex(ord(message[i])),'/',bin(ord(message[i]))
    ser.close()

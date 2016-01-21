#!/usr/local/bin/python3
from hazc import hazc_device

import time

# dev = hazc_device.hazc_device("127.0.0.1")
dev = hazc_device.hazc_device("192.168.1.2")
# dev = hazc_device.hazc_device("0.0.0.0")

def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    
dev.addStatus('time', now)

pwrlvl = 0
def changepower(lvl):
    global pwrlvl
    pwrlvl = lvl
    print("Changing power level to: " + str(lvl))
    #return "powerlevel set to "+str(lvl)
    
def getpowerlevel():
    global pwrlvl
    print("Getting power level.. " + str(pwrlvl))
    return str(pwrlvl)

dev.addControl('powerlevel', changepower, getpowerlevel, dev.INT)



dev.advertise()
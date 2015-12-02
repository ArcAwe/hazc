#!/usr/local/bin/python3
from hazc import hazc_device

import time

dev = hazc_device.hazc_device("127.0.0.1")

def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    
dev.addStatus('time', now)

pwrlvl = 0
def changepower(lvl):
    global pwrlvl
    pwrlvl = lvl
    
def getowerlevel():
    global pwrlvl
    return str(pwrlvl)

dev.addControl('powerlevel', changepower, getpowerlevel, hazc_device.INT)



dev.advertise()
#!/usr/local/bin/python3
from hazc import hazc_master

master = hazc_master.hazc_master()
master.setDebugCommandLine(True)
master.detectDevices()

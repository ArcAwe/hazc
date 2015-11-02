# This project is to allow for home automation using zeroconf to make setting up new custom devices.

## Config File
Everything except method calls and statuses is configured here.

### GLOBAL
- service_prefix: what name this HAZC announces and looks for, should be unique
- port: the port the HTTP-like protocol uses, can't conflict with any ports already in use by the automation device

## API
You import the hazc library to your python program, instantiate the hazc_master and hazc_device classes, interface them to your automation methods, point your webserver at the web folder and you're good!

You'll probably want to edit the config.ini file too, but if it's your first device and master on the network it should work just fine.

NOTE: I will be adding handlers for other languages. Eventually...

### Simple example
From your server running python3:
```python
#/usr/home/me/project/hazc-python.py
from hazc import *
home_control = hazc.hazc_master()
home_control.start()
```

```text
#/etc/
...
document-root:/usr/home/me/project/web/
...
```

From your thermostat running python3 on a Raspberry Pi:
```python
from hazc import *
network_interface = hazc.hazc_device()
network_interface.add
```

## Protocol
There are two main portions of this project:
(1) The 'Master'
(2) The 'Device'
The master discovers all HAZC devices on the network and provides a dynamic, versatile web interface (also announced via zeroconf). The device is the actual automation device, which broadcasts its ip address and available automation commands over zeroconf. Both the master and device programs can run on the same machine, but they are two separate processes.

NOTE: Theoretically, there can be multiple Masters if you want redundancy, but there really isn't much need of more than one.

### Discovery
The master uses zeroconf to locate any operating HAZC devices. After finding an announced HAZC service, it asks a series of questions to figure out what commands it takes and how to determine its status. 
First it asks for 'version?' to allow for future backwards-compatibility. Secondly it asks 'commands?' to detect how to command the connected device. Lastly, it asks for the status to detect the current state of the device and determine what statuses it can announce.

#### Required commands
Version 1 or less requires the following commands to exist:
- version? return the HAZC version number currently running
- commands? return a list of available commands (e.g. this list)
- status? return a key,value list of the device's status. Every configuration command must be returned here as the key.
- shutdown! power down the device - useful for gracefully shutting down an embedded device before pulling the power cord.

And 1 or more of the following:
- set-[some config]:[type of value] This is where your program describes the interfaces to the HAZC system. It is up to you to handle input validation. Example ```set-color:int``` or ```set-temp:float``` or ```set-lights:bool```

#### Commands in-depth
- version? Returns a float
- commands? Returns a semicolon-delimitated string of commands, e.g. ```version?;commands?;status?;shutdown!;set-lights:bool```
- status? Returns a list of all configs and possibly other status values: ```lights,TRUE;current_temp,30.3;temp_unit,c```
- shutdown! Returns a 'goodbye!' and removes the service from zeroconf then powers down
- set-[some config]:[some value] The master will determine what configs are available via the commands? command and response. Obviously, the value sent to the device must be of the type previously announced. Returns TRUE on success.

#### Example TCP stream:
```
Connection established at 192.168.0.20
master:version?
device:1.0
master:commands?
device:version?;commands?;status?;shutdown!;set-lights:bool;set-desired_temp:float;set-temp_unit:char
master:status?
device:lights,TRUE;desired_temp,68.5;temp_unit,f;current_temp,70.4
master:set-lights:FALSE
device:TRUE
```

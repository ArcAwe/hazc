# Version 1.0
### Config File
#### GLOBAL
- service_prefix: what name this HAZC announces and looks for, should be unique. (_hazc.tcp.local.)
- port: the port the HTTP-like protocol uses, can't conflict with any ports already in use by the automation device (551)
#### DISCOVERY
- minversion: The minimum version required by the 'master', should be at least as high as the master's version
- xml_location: the relative location and name of the xml file for the web server
#### DEVICE
- hostname: the name you want to advertise your device as

### API
#### Functions
- addControl(name, type, function): name is the unique string to advertise and reference the control as, the type is a constant provided by the hazc class that tells the master what kind of parameters this function can take, and function is the handler function in your code that gets run when called by the master - parameters as defined by the type.

#### Control 'Surfaces' or allowed control type names
- colorRGB: (Red,Green,Blue) from 0-255 as in (23,200,25)
- ENUM: enumerated options to be listed in enum sub-element
	- List comma-deliminated names

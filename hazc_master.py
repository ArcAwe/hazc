#!/usr/local/bin/python3

#Discover devices and update table

from zeroconf import Zeroconf, ServiceBrowser
import socket
import configparser
import xml.etree.cElementTree as ET
import os.path

class hazc_master:
#     global inst

    global instance

    def __init__(self): #, ipaddr):
#         global instance
#         instance = self
        
        #ipaddr = 'localhost'
    
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        #self.ip = ipaddr
        self.MSGLEN = 1024
        self.END_OF_MSG = '*'
        
        self.xmlpath = self.config['discovery']['xml_location']
        self.checkXML()
        
#         self.xmlroot = ET.Element("root")
        
#         global inst
#         inst = self
        #init the XML file
        
    #start searching - THE method to run
    def detectDevices(self):
        self.zeroconf = Zeroconf()
        self.listener = hazcListener()
        self.browser = ServiceBrowser(self.zeroconf, self.config['global']['service_prefix'], hazcListener)
        try:
            input("Press enter to exit...\n\n")
#             while(1):
                #loop
        finally:
            self.zeroconf.close()
#             self.webcontrol.close() #May not be neccesary
        
        #self.bindConnection() #option2
    
    def bindConnection(self):
        self.webcontrol = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.webcontrol.bind(('localhost', 8796))
        self.webcontrol.listen(1)    
    
#     TODO: send variable length packets
    def getInfo(self, ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((str(ip),int(config['global']['port'])))
        
        attr = {}
        
        self.senddata(s, "version?")
        version = recvdata(s)
        attr['version'] = version
        
        self.senddata(s, "commands?")
        #retrieve commands as according to README
        commands = recvdata(s)
        #version 1 contains version? commands? status? shutdown!
        commandlist = self.parseconfigs(commands.split(';'))
        self.senddata(s, "status?")
        # control surfaces
        controls = list()
        
        attr['controls'] = controls
        
        s.shutdown(1)
        s.close()
        
        return attr
        
    def parseconfigs(self, cmdlist):
        confs = list()
        for str in cmdlist:
            if(str[0:4] is "set-"):
                confs.append(str[4:])
        return confs
        
    def fixmsglength(self, msg):
        if msg < self.MSGLEN:
            while len(msg) < self.MSGLEN:
                msg.append(self.END_OF_MSG)
        else:
            return msg[0:self.MSGLEN]
        
    def senddata(self, sock, msg):
        msg = self.fixmsglength(msg)
        totalsent = 0
        while totalsent < self.MSGLEN:
            sent = sock.send(msg[totalsent:])
            if sent == 0:
                # closed
                raise RuntimeError("socket connection broken unexpectedly. Was trying:" + str(msg))
            totalsent = totalsent + sent
    
    def recvdata(self, sock):
        chunks = []
        bytes_recd = 0
        while bytes_recd < self.MSGLEN:
            chunk = sock.recv(MSGLEN - bytes_recd)
        if chunk == b'':
            raise RuntimeError("Socket connection broken unexpectedly")
        chunks.append(chunk)
        bytes_recd += len(chunk)
        
        msg = b''.join(chunks)
        return msg.strip(self.END_OF_MSG)
        
    def checkXML(self): #see if XML exists, otherwise create it.
#         root = ET.Element("root")
        #if(not os.path.isfile(self.xmlpath)):
        
        #Set up a new clean XML - as loading one may have old devices
        devices = ET.Element('devices')
        tree = ET.ElementTree(devices)
#             root = ET.Element('devices')
        tree.write(self.xmlpath)
        
    def add_service_xml(self, info):
        tree = ET.parse(self.xmlpath)
        devices = tree.getroot()
        
        cleanname = info.split(self.config['global']['service_prefix'])[0]
        newservice = ET.SubElement(devices, cleanname)
        
        
#         tree = ET.ElementTree(self.xmlroot)
        deviceAttribs = self.getInfo(socket.inet_ntoa(info.address))
        
        version = ET.SubElement(newservice, "version")
        version.text = deviceAttribs['version']
        
        control = ET.SubElement(newservice, "control")
        for controlsurface in deviceAttribs['controls']:
            newsurface = ET.SubElement(control, controlsurface['name'])
            type = ET.SubElement(newsurface, "type")
            type.text = controlsurface['type']
            if(type.text == "ENUM"):
                enum = ET.SubElement(type, "enum")
                enum.text = controlsurface['enum']
            value = ET.SubElement(newsurface, "value")
            value.text = controlsurface['value']
        

        
#         devices.append(newdevice)
        tree.write(self.xmlpath)
        
    def remove_service(self, info):
        tree = ET.parse(self.xmlpath)
        devices = tree.getroot()
        
        cleanname = info.split(self.config['global']['service_prefix'])[0]
        
        devices.remove(devices.find(cleanname))
        tree.write(self.xmlpath)

class hazcListener(object):

    def remove_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        hazc_master.instance.remove_service_xml(info)
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print("Service %s added, service info: %s" % (name, info))
        # Add to XML
        hazc_master.instance.add_service(info)
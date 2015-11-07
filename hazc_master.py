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

    def __init__(self, ipaddr):
        global instance
        instance = self
    
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.ip = ipaddr
        self.MSGLEN = 1024
        self.END_OF_MSG = '*'
        self.checkXML()
        
        self.xmlroot = ET.Element("root")
        
#         global inst
#         inst = self
        #init the XML file
        
    #start searching - THE method to run
    def detectDevices(self):
        self.zeroconf = Zeroconf()
        self.listener = hazcListener()
        self.browser = ServiceBrowser(self.zeroconf, self.config['global']['service_prefix'], self.listener)
        try:
            input("Press enter to exit...\n\n")
#             while(1):
                #loop
        finally:
            zeroconf.close()
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
        self.version = recvdata(s)
        self.senddata(s, "commands?")
        #retrieve commands as according to README
        commands = recvdata(s)
        #version 1 contains version? commands? status? shutdown!
        commandlist = self.parseconfigs(commands.split(';'))
        self.senddata(s, "commands?")
        
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
        else
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
        os.path.isfile(xmlpath)
        
    def add_service_xml(self, info):
        xmlpath = self.config['global']['xml_location']
        tree = ET.parse(xmlpath)
        root = tree.getroot()
#         tree = ET.ElementTree(self.xmlroot)
        deviceAttribs = self.getInfo(info.addr)
        root.subElement(info.name, deviceAttribs)

        tree.write(xmlpath)
        
    def remove_service(self, info):

class hazcListener(object):

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))
        hazc_master.instance.remove_service_xml(info)

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print("Service %s added, service info: %s" % (name, info))
        # Add to XML
        hazc_master.instance.add_service(info)
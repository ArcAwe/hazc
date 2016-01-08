#!/usr/local/bin/python3

#Discover devices and update table

from zeroconf import Zeroconf, ServiceBrowser
import socket
import configparser
import xml.etree.cElementTree as ET
import os.path

# import pdb

class hazc_master:
#     global inst

    def __init__(self): #, ipaddr):
#         global instance
#         instance = self

        #ipaddr = 'localhost'
        self.version = "0.1"
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        #self.ip = ipaddr
        self.MSGLEN = 1024
        self.END_OF_MSG = '*'

        self.port = int(self.config['global']['port'])

        self.xmlpath = self.config['discovery']['xml_location']
        self.checkXML()

#         self.xmlroot = ET.Element("root")

#         global inst
#         inst = self
        #init the XML file
        
    #TODO: validate XML
    def printprettyxml(self):
        tree = ET.parse(self.xmlpath)
        rough_string = ET.tostring(tree, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        
        print('**********************************')
        print(reparsed.toprettyxml(indent="\t"))
        print('**********************************')

    #start searching - THE method to run
    def detectDevices(self):
        self.zeroconf = Zeroconf(("eth0",3))
        self.listener = hazcListener(self)
        self.browser = ServiceBrowser(self.zeroconf, self.config['global']['service_prefix'], self.listener)
        try:
            input("Press enter to exit...\n\n")

#             This allows pdb to work with an input
#             import time
#             while(1):
#                 time.sleep(0.1)
        finally:
            self.zeroconf.close()
#             self.webcontrol.close() #May not be neccesary

        #self.bindConnection() #option2

#     def bindConnection(self):
#         self.webcontrol = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.webcontrol.bind(('localhost', 8796))
#         self.webcontrol.listen(1)

#     TODO: send variable length packets
    def getInfo(self, ip):
        print("Getting info...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip,self.port))

        attr = {}

        self.senddata(s, "version?")
        version = self.recvdata(s)
        attr['version'] = version

        s.close()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip,self.port))

        self.senddata(s, "commands?")
        #retrieve commands as according to README
        commands = self.recvdata(s)
        commandlist = self.parseconfigs(commands.split(';'))
        
        attr['controls'] = commandlist
        
        s.close()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip,self.port))


        #s.connect((ip,int(self.config['global']['port'])))
        #version 1 contains version? commands? status? shutdown!
        self.senddata(s, "status?")
        status = self.recvdata(s)
        
        
        # control surfaces
        stats = status.split(';')

        attr['statuses'] = stats

        try:
            s.shutdown(1)
        finally:
            s.close()

        return attr

    #maybe we don't want to remove the "set-" part
    def parseconfigs(self, cmdlist):
        confs = list()
        for str in cmdlist:
#             str.split(':')[0]
#             if(str[0:4] is "set-"):
#                 confs.append(str[4:])
            confs.append(str)
        return confs

    def fixmsglength(self, msg):
        if len(msg) < self.MSGLEN:
#             print("not long enough")
            while len(msg) < self.MSGLEN:
                msg+=self.END_OF_MSG
            return msg
        else:
#             print("too long")
            return msg[0:self.MSGLEN]

    def senddata(self, sock, msg):
        print(msg)
        bmsg = self.fixmsglength(msg).encode('utf-8')
        totalsent = 0
        while totalsent < self.MSGLEN:
#             print(totalsent)
#             print(msg)
            sent = sock.send(bmsg[totalsent:])
            if sent == 0:
                # closed
                raise RuntimeError("socket connection broken unexpectedly. Was trying:" + str(bmsg.decode('utf-8')))
            totalsent = totalsent + sent

    def recvdata(self, sock):
#         chunks = []
#         bytes_recd = 0
#         while bytes_recd < self.MSGLEN:
#             chunk = sock.recv(self.MSGLEN - bytes_recd)
#         if chunk == b'':
#             raise RuntimeError("Socket connection broken unexpectedly")
#         chunks.append(chunk)
#         bytes_recd += len(chunk)
#
#         msg = b''.join(chunks)

        msgbytes = sock.recv(self.MSGLEN)
        msgstr = msgbytes.decode('utf-8')
        rmsg = msgstr.strip(self.END_OF_MSG)
        print("->" + rmsg)
        return rmsg

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

        cleanname = info.name.split(self.config['global']['service_prefix'])[0]
        newservice = ET.SubElement(devices, cleanname)


#         tree = ET.ElementTree(self.xmlroot)
        deviceAttribs = self.getInfo(socket.inet_ntoa(info.address))

        version = ET.SubElement(newservice, "version")
        version.text = deviceAttribs['version']

#         pdb.set_trace()

        control = ET.SubElement(newservice, "controls")
        
        for controlsurface in deviceAttribs['controls']:
            # import pdb; pdb.set_trace()
            
            controlsplit = controlsurface.split(':')
            
            if len(controlsplit[0]) > 0:
            
                newsurface = ET.SubElement(control, controlsplit[0])
            
                #TODO: fix the various commands that don't take parameters
                if ':' in controlsplit :
                    cparam = ET.SubElement(newsurface, "parameter")
                    cparam.text = controlsplit[1]
            
                    #TODO: implement ENUMs
                    if(cparam.text == "ENUM"):
                        enum = ET.SubElement(type, "enum")
                        enum.text = controlsurface['enum']

        stattree = ET.SubElement(newservice, "statuses")
        
        for stat in deviceAttribs['statuses']:
            statsplit = stat.split(',')
            statname = statsplit[0]
            if len(statname) > 0:
                substattree = ET.SubElement(stattree, statname)
            
                if ',' in stat:
                    statvalue = statsplit[1]
                    statval = ET.SubElement(substattree, "VALUE")
                    statval.text = statvalue
            
            
            


#         devices.append(newdevice)
        tree.write(self.xmlpath)
        
#         self.printprettyxml()

    def remove_service_xml(self, info):
        tree = ET.parse(self.xmlpath)
        devices = tree.getroot()

        cleanname = info.split(self.config['global']['service_prefix'])[0]

        devices.remove(devices.find(cleanname))
        
        #lets make it readable for now
        roughstring = ET.tostring(tree, 'utf-8')
        
        tree.write(self.xmlpath)

class hazcListener(object):
    def __init__(self, hmaster):
        self.hazc_master = hmaster

    def remove_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        self.hazc_master.remove_service_xml(info)
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
#         pdb.set_trace()
        print("Service %s added, service info: %s" % (name, info))
        # Add to XML
        self.hazc_master.add_service_xml(info)
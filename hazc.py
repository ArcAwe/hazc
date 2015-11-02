#!/usr/local/bin/python3

#Discover devices and update table

from zeroconf import Zeroconf, ServiceBrowser
import socket
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class hazc_obj:
    def __init__(self, ipaddr):
        self.ip = ipaddr
        self.MSGLEN = 1024
        self.END_OF_MSG = '*'
        self.create()
    
    def create(self):
    
#     TODO: send variable length packets
    def getInfo(self, s):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((str(ip),int(config['global']['port'])))
        
        self.senddata(s, "version?")
        self.version = recvdata(s)
        self.senddata(s, "commands?")
        #retrieve commands as according to README
        
        s.shutdown(1)
        s.close()
        
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

class MyListener(object):

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print("Service %s added, service info: %s" % (name, info))


zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()
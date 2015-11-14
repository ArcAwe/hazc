#!/usr/local/bin/python3
from zeroconf import Zeroconf, ServiceInfo
import socket
import configparser

class hazc_master:
    def __init__(self, ipaddr):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.MSGLEN = 1024
        self.END_OF_MSG = '*'
        self.ip = ipaddr
        
    def advertise(self):
        postfix = self.config['global']['service_prefix']
        port = int(self.config['global']['port'])
        info = ServiceInfo(postfix, self.config['device']['hostname']+ postfix,
                       socket.inet_aton(self.ip), port, 0, 0,
                       self.config['device']['description'], "hazc.local.")
                       
        zeroconf = Zeroconf()
        zeroconf.register_service(info)
        
        try:
            while True:
                self.listen()
        except KeyboardInterrupt:
            pass
        finally:
            print("Unregistering...")
            zeroconf.unregister_service(info)
            zeroconf.close()
            
    def listen(self):
        
        
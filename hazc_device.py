#!/usr/local/bin/python3
from zeroconf import Zeroconf, ServiceInfo
import socket
import configparser
import const
import hazc_cmd

class hazc_device:
    
    #Forward constants
    NO_PARAM = hazc_cmd.NO_PARAM
    BOOL = hazc_cmd.BOOL
    FLOAT = hazc_cmd.FLOAT
    STRING = hazc_cmd.STRING
    INT = hazc_cmd.INT

    def __init__(self, ipaddr):
        self.version = "0.1"
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.MSGLEN = 1024
        self.END_OF_MSG = '*'
        self.ip = ipaddr
        self.buffer = 20
#         self.commands = {'version?':self.version_cmd,'commands?':self.commands_cmd,'status?':self.status_cmd}
        
        hcvc = hazc_cmd.hazc_cmd('version?',self.version_cmd, NO_PARAM)
        hccc = hazc_cmd.hazc_cmd('commands?', self.commands_cmd, NO_PARAM)
        hcsc = hazc_cmd.hazc_cmd('status?', self.status_cmd, STRING)
        self.commands = {'version?': hcvc, 'commands?': hccc, 'status?': hcsc}
        
        # probably want to add a debug log status
        self.status = {'exec_status': self.exec_status}

    #Adds a function - not as preferred as addControl
    #Does NOT auto add status
    def addFunction(self, name, handler, paramtype):
        #log("This is not the preferred way to add controls, see addControl")
        if not('?' in name or '!' in name):
#            log("Function name requires a '?' or '!', assuming '!'")
            name += '!'
            
        self.commands[name] = hazc_cmd.hazc_cmd(name, handler, paramtype)
            
    #Adds a control vector
    #controlname should just be a name like 'temp' or 'position' - it'll be the same for the status
    def addControl(self, controlname, handler, statushandler, paramtype=NO_PARAM):
        cmd_name = 'set-'+controlname+'?'
        self.commands[cmd_name] = hazc_cmd.hazc_cmd(cmd_name, handler, paramtype)
        self.addStatus(controlname, statushandler)
    
    #adds a unique status not already included in control vector. name is just the name, as in 'temp'
    def addStatus(self, name, handler):
        self.status[name] = handler

    def advertise(self):
        postfix = self.config['global']['service_prefix']
        self.port = int(self.config['global']['port'])
        #print(self.config['device']['hostname']+postfix)
        info = ServiceInfo(postfix, self.config['device']['hostname']+postfix,
                       socket.inet_aton(self.ip), self.port, 0, 0,
                       {'info': self.config['device']['description']}, "hazc.local.")

        self.bindConnection()

        zeroconf = Zeroconf()
        zeroconf.register_service(info)


        try:
            while True:
#                 try:
                print("Ready")
                self.conn, self.addr = self.webcontrol.accept()
                self.listen()
                self.conn.close()
        except KeyboardInterrupt:
            pass
        finally:
            print()
            print("Unregistering...")
            zeroconf.unregister_service(info)
            zeroconf.close()

        try:
            print("Shutting down socket")
            self.webcontrol.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(e)

    def listen(self):
        data = bytes()
        rbytes = 0
        while rbytes < self.MSGLEN:
            d = self.conn.recv(self.buffer)
            if not d: break
            data += d
            rbytes += len(d)

#         print data.decode('utf-8')
        self.handledata(data)

    def handledata(self, data):
        command = self.cleanandstringdata(data)
        param = self.getparam(command)
        
        print('->' + command)

        replystr = "ERROR"

        if len(param) > 0:
            replystr = self.commands[command].execute(param)
        else:
             replystr = self.commands[command].execute()

        print(replystr)
        self.reply(replystr)


    def reply(self, msg):
        longmsg = msg
        while len(longmsg) < self.MSGLEN:
            longmsg += self.END_OF_MSG
#         print(longmsg)
        self.conn.send(longmsg.encode('utf-8'))

    def cleanandstringdata(self, data):
        dstr = data.decode('utf-8')
        return dstr.strip(self.END_OF_MSG)
    
    def getparam(self, data):
        if '?' in data:
            return data.split('?')[-1]
        elif '!' in data:
            return data.split('!')[-1]
        else:
            return ''

    def bindConnection(self):
        try:
            self.webcontrol = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.webcontrol.bind((self.ip, self.port))
            self.webcontrol.listen(1)
        except OSError as e:
            print(e)
            quit()
            
    def exec_status(self):
        return "Running"

    def version_cmd(self):
        return self.version

    def commands_cmd(self):
        rstr = ""
        for key in self.commands:
            rstr += key + ";"
        return rstr

    def status_cmd(self, specific_status=''):
        str = ''
        if len(specific_status > 0):
            str = self.status[specific_status]
        else:
            for st in self.status:
                str += st + ',' + self.status[st]() + ';'
        
        return str[:self.MSGLEN-1]
        
    # Some debugging methods
    def debug_cmds(self):
        print("Commands: " + str(self.commands))
        print("Statuses: " + str(self.status))
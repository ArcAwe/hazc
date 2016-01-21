#!/usr/local/bin/python3
from zeroconf import Zeroconf, ServiceInfo
import socket
import configparser
from . import hazc_cmd

# import pdb

class hazc_device:
    
    #Forward constants
    NO_PARAM = hazc_cmd.NO_PARAM
    BOOL = hazc_cmd.BOOL
    FLOAT = hazc_cmd.FLOAT
    STRING = hazc_cmd.STRING
    INT = hazc_cmd.INT
    
    global running
    running = False

    def __init__(self, ipaddr):
        self.version = "0.1"
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.MSGLEN = 1024
        self.END_OF_MSG = '*'
        self.ip = ipaddr
        self.buffer = 20
#         self.commands = {'version?':self.version_cmd,'commands?':self.commands_cmd,'status?':self.status_cmd}
        
        hcvc = hazc_cmd.hazc_cmd('version?', self.version_cmd, self.NO_PARAM)
        hccc = hazc_cmd.hazc_cmd('commands?', self.commands_cmd, self.NO_PARAM)
        hcsc = hazc_cmd.hazc_cmd('status?', self.status_cmd, self.STRING)
        self.commands = {'version': hcvc, 'commands': hccc, 'status': hcsc}
        
        # probably want to add a debug log status
        self.status = {'exec_status': self.exec_status}

    #Adds a function - not as preferred as addControl
    #Does NOT auto add status
    def addFunction(self, name, handler, paramtype):
#         pdb.settrace()
        #log("This is not the preferred way to add controls, see addControl")
        if not('?' in name or '!' in name):
#            log("Function name requires a '?' or '!', assuming '!'")
            name += '!'
            
        self.commands[name] = hazc_cmd.hazc_cmd(name, handler, paramtype)
            
    #Adds a control vector
    #controlname should just be a name like 'temp' or 'position' - it'll be the same for the status
    def addControl(self, controlname, handler, statushandler, paramtype=NO_PARAM):
        cmd_name = 'set-'+controlname
        self.commands[cmd_name] = hazc_cmd.hazc_cmd(cmd_name+'?', handler, paramtype)
        self.addStatus(controlname, statushandler)
    
    #adds a unique status not already included in control vector. name is just the name, as in 'temp'
    def addStatus(self, name, handler):
        self.status[name] = handler

    def advertise(self):
        postfix = self.config['global']['service_prefix']
        self.port = int(self.config['global']['port'])
        #print(self.config['device']['hostname']+postfix)
        info = ServiceInfo(postfix, self.config['device']['hostname']+"."+postfix,
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
        command, param = self.cleanandstringdata(data)
        print('->' + command + ';' + param)

#         replystr = "ERROR"
        try:
            replystr = self.commands[command].execute(param)
        except KeyError:
            if(command==''):
                command = "(empty string)"
            print("ERROR! Unknown command: " + command)
            replystr = ""
#         replystr = self.commands['version'].execute('')
        
        if(replystr == None):
            print("WARNING! " + command + " should return a string to send to the master. Sending 'NO_REPLY'")
            replystr = 'NO_REPLY'

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
        full = dstr.strip(self.END_OF_MSG)
        if '?' in full:
            li = full.split('?')
            param = li[-1]
            cmd = li[0]
        elif '!' in full:
            li = full.split('!')
            param = li[-1]
            cmd = li[0]
        else:
            param = ''
            cmd = full
        return (cmd, param)

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
        
    def paramtype_tostring(self, paramnum):
        if paramnum == self.BOOL:
            return 'BOOL'
        elif paramnum == self.FLOAT:
            return 'FLOAT'
        elif paramnum == self.STRING:
            return 'STRING'
        elif paramnum == self.INT:
            return 'INT'
        else:
            return 'PARAM_ERROR'

    def commands_cmd(self):
        rstr = ""
        for key in self.commands:
            rstr += key
            if self.commands[key].paramtype is not self.NO_PARAM:
#                 pdb.set_trace()
                rstr += ':' + self.paramtype_tostring(self.commands[key].paramtype)
            rstr += ";"
        return rstr

    def status_cmd(self, specific_status=''):
        str = ''
        if len(specific_status) > 0:
            str = self.status[specific_status]
        else:
            for st in self.status:
                str += st + ',' + self.status[st]() + ';'
        
        return str[:self.MSGLEN-1]
        
    # Some debugging methods
    def debug_cmds(self):
        print("Commands: " + str(self.commands))
        print("Statuses: " + str(self.status))
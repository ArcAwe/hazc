#!/usr/local/bin/python3ß

class hazc_cmd:
    NO_CMD = 1
    BOOL = 2
    FLOAT = 3
    CHAR = 4
    INT = 5
    
    def __init__(self, title, function, paramtype=1):
        self.title = title
        self.function = function
        self.paramtype = paramtype
        
    def execute(self):
        if(self.param == 1):
            self.function()
        else 
            raise Exception()
            
    def execute(self, param):
        if(param == 1):
            self.function()
        elif(param == 2):
            self.function(self.toBool(param))
        elif(param == 3):
            
            
            
    def toBool(self, param):
        p = param.upper()
        if(param == True):
            return True
        elif(param == False):
            return False
        elif(p == 'TRUE'):
            return True
        elif(p == 'FALSE'):
            return False
        elif(p == '1'):
            return True
        elif(p == '0'):
            return False
        else:
            raise Exception()
            
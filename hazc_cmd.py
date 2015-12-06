#!/usr/local/bin/python3

NO_PARAM = 1
BOOL = 2
FLOAT = 3
STRING = 4
INT = 5

class hazc_cmd:
#     NO_PARAM = 1
#     BOOL = 2
#     FLOAT = 3
#     STRING = 4
#     INT = 5
    
    def __init__(self, title, function, paramtype=1):
        self.title = title
        self.function = function
        self.paramtype = paramtype
            
    def execute(self, param):
        if(self.paramtype == 1):
            return self.function()
        elif(self.paramtype == 2):
            return self.function(self.toBool(param))
        elif(self.paramtype == 3):
            return self.function(float(param))
        elif(self.paramtype == 4):
            return self.function(param)
        elif(self.paramtype == 5):
            return self.function(int(param))
        else:
            raise Exception
            
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
            
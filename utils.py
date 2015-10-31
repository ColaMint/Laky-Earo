# -*- coding:utf-8 -*-  

class __Const(object):
    class ConstError(TypeException): pass
    def __setattr__(self, key, value):
        if self.__dict__.has_key(key):
            raise self.ConstError, "Changing const.%s" % key
        else:
            self.__dict__[key] = value

    def __getattr__(self, key):
        if self.__dict__.has_key(key):
            return self.key
        else:
            return None

Const = __Const()

__local = threading.local() 

class __Local(object):

    def __init__(self):
        self.__local = threading.local()

    def __setattr__(self, key, value):
        self.local.__setattr__(key, value)

    def __getattr__(self, key):
        return self.__local.getattr(key, None)

Local = __Local()

# -*- coding:utf-8 -*-  
import os
from utils import Const
from event_manager import EventManager
from configuration import Confituration
from exception import MissingCurrentApp

class EaroApp(object):

    def __init__(self, app_name):
        self.__app_path = os.sys.path[0]
        self.__app_name = app_name
        self.__config = Confituration(app_name) 
        self.__event_manager = EventManager() 
        setCurrentApp(self)

    def app_path(self):
        return self.__app_path 

    def app_name(self):
        return self.__app_name

    def config(self):
        return self.__config

    def __auto_register_event_handlers(self):
        self.__auto_register_event_handlers_recursively(self.__app_path)

    def __auto_register_event_handlers_recursively(self, dirname, pkgname):
        for parent, dirnames, filenames in os.walk(dirname):
            for dn in dirnames:
                self.__auto_register_event_handlers_recursively(
                    os.path.join(dirname, dn), 
                    '%s.%s' % (pkgname, dn)
                )
            for fn in filenames:
                modname = '%s.%s' % (pkgname, fn) 
                mod = __import__(modname) 
                for attr in dir(mod):
                    if attr.startswith('_'):
                        continue
                    __event_handlers__ = mod.getattr(attr, None)
                    if __event_handlers__:
                        for event_handler in __event_handlers__:
                            self.__event_manager.register_event_hanlder(event_handler)
                    


def set_current_app(app):
    Const.CURRENT_APP = app

def get_current_app():
    app = Const.CURRENT_APP
    if not isinstance(app, EaroApp):
        raise MissingCurrentApp()
    else:
        return app

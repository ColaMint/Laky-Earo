# -*- coding:utf-8 -*-  

from utils import Const
import os

class Confituration(object):

    def __init__(self, app):
        self.__app = app
        self.__load_configuration()

    def __load_configuration(self):
        self.__conf_path = '%s.conf.conf.py' % self.__app.app_name()
        self.__conf_module = __import__(self.__conf_path)
        self.__conf = self.__conf_module.getattr('CONF', dict())

    def get(key):
        if key in self.__conf:
            return self.__conf[key]
        else:
            return None

    def set(key, value):
        self.__conf[key] = value


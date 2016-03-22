#!/usr/bin/python
# -*- coding:utf-8 -*-


class Config(object):

    __config__ = {
        'app_name': 'earo'
    }

    def __init__(self, config={}):
        for key, value in config.iteritems():
            self.__setattr__(key, value)

    def __getattr__(self, key):
        if key in self.__config__:
            return self.__config__[key]
        else:
            raise KeyError(key)

    def __setattr__(self, key, value):
        if key in self.__config__:
            self.__config__[key] = value
        else:
            raise KeyError(key)

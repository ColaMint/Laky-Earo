#!/usr/bin/python
# -*- coding:utf-8 -*-
from threading import local
from copy import deepcopy


class Local:

    def __init__(self, **defaults):
        self.__local = local()
        self.__defaults = defaults

    def __getattr__(self, name):
        if name not in self.__local.__dict__:
            default = self.__defaults[
                name] if name in self.__defaults else None
            value = default() if callable(default) else deepcopy(default)
            self.__local.__setattr__(name, value)
        return self.__local.__getattribute__(name)

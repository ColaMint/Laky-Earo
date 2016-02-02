#!/usr/bin/python
# -*- coding:utf-8 -*-
from Queue import Queue
from uuid import uuid1


class EventChannel(object):

    def __init__(self):
        self.id = uuid1()
        self.__broker = None
        self.__channel = Queue()

    def register(self, broker):
        if self.__broker is not None:
            raise AlreadyRegisteredException()
        else:
            broker.register(self)
            self.__broker = broker

    def unregister(self):
        if self.__broker is not None:
            self.__broker.unregister(self)

    def put(self, event, block=True, timeout=None):
        self.__channel.put(event, block, timeout)

    def get(self, block=True, timeout=None):
        return self.__channel.get(block, timeout)


class AlreadyRegisteredException(Exception):

    def __init__(self):
        super(
            AlreadyRegisteredException,
            self).__init__('[The channel has registered.]')

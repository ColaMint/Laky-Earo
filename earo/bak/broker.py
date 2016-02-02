#!/usr/bin/python
# -*- coding:utf-8 -*-
from event_channel import EventChannel
from threading import Thread
from random import choice
import Queue


class Broker(Thread):

    def __init__(self, app):
        super(Broker, self).__init__()
        self.__app = app
        self.__event_channel = EventChannel()
        self.__running = True
        self.__registered_channels = dict()

    def register(self, event_channel):
        self.__registered_channels[event_channel.id] = event_channel
        self.__app.logger.info(
            'EventChannel(%s) registered.' %
            (event_channel.id,))

    def unregister(self, event_channel):
        try:
            self.__registered_channels.pop(event_channel.id)
            self.__app.logger.info(
                'EventChannel(%s) unregistered.' %
                (event_channel.id,))
        except:
            pass

    def put(self, event, block=True, timeout=None):
        self.__event_channel.put(event, block, timeout)

    def run(self):
        self.__app.logger.info('Broker start working.')
        event = None
        while self.__running:
            if event is None:
                try:
                    event = self.__event_channel.get(True, 5)
                except Queue.Empty:
                    pass
            if event is not None:
                event_channel = self.__registered_channels[
                    choice(self.__registered_channels.keys())]
                try:
                    event_channel.put(event, False)
                    event = None
                except Queue.Full:
                    pass
        self.__app.logger.info('Broker stop working.')

    def stop(self):
        self.__running = False

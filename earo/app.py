#!/usr/bin/python
# -*- coding:utf-8 -*-

from mediator import Mediator
from handler import Handler
from context import Context
from config import Config


class App(object):

    def __init__(self, config):
        self.mediator = Mediator()
        self.config = config
        self.__init_with_config()

    def __init_with_config(self):
        pass

    def handler(self, event_cls, emittion_statement=[]):
        def decorator(func):
            handler = Handler(event_cls, func, emittion_statement)
            self.mediator.register_event_handler(handler)
            return func
        return decorator

    def emit(self, event):
        context = Context(self.mediator, event)
        context.process()
        return context

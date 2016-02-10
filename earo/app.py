# -*- coding:utf-8 -*-
from mediator import Mediator
from handler import Handler
from context import Context
from importlib import import_module


class App(object):

    def __init__(self, config):
        self.mediator = Mediator()
        self.config = config
        self._init_app_with_config()

    def _init_app_with_config(self):
        pass

    def handler(self, event_cls, emit_events=[]):
        def decorator(func):
            handler = Handler(event_cls, func, emit_events)
            self.mediator.register_event_handler(handler)
            return func
        return decorator

    def emit(self, event):
        context = Context(self.mediator, event)
        context.process()
        return context

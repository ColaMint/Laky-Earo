# -*- coding:utf-8 -*-
from mediator import Mediator
from handler import Handler
from context import Context


class App(object):

    def __init__(self):
        self.mediator = Mediator()

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

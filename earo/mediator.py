# -*- coding:utf-8 -*-

class Mediator(object):

    def __init__(self):

        self.event_handler_map = {}

    def find_handlers(self, event_cls):
        if event_cls in self.event_handler_map:
            return self.event_handler_map[event_cls]
        else:
            return []

    def register_event_handler(self, *handlers):
        for handler in handlers:
            if handler.event_cls not in self.event_handler_map:
                self.event_handler_map[handler.event_cls] = []
            self.event_handler_map[handler.event_cls].append(handler)

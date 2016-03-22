#!/usr/bin/python
# -*- coding:utf-8 -*-


class Mediator(object):

    def __init__(self):

        self.__event_handler_map = {}

    def find_handlers(self, event_cls):
        if event_cls in self.__event_handler_map:
            return self.__event_handler_map[event_cls]
        else:
            return []

    def register_event_handler(self, *handlers):
        for handler in handlers:
            if handler.event_cls not in self.__event_handler_map:
                self.__event_handler_map[handler.event_cls] = []
            self.__event_handler_map[handler.event_cls].append(handler)

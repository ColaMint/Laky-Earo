#!/usr/bin/python
# -*- coding:utf-8 -*-
from configure import Configure
from util.local import Local
from broker import Broker
from event_processor import EventProcessor
from event_channel import EventChannel
from handler import Handler
from runtime_tree import RuntimeTreeStorage
import logging
import sys


class App(object):

    def __init__(self, name, config={}):
        self.name = name
        self.config = Configure(config)
        self.__init_local_and_global()
        self.__init_logger()
        self.__init_broker_and_processors()
        self.__init_runtime_tree_storage()

    def __init_local_and_global(self):
        local_defaults = {
            'event_handler_map': dict,
        }
        self.__local = Local(**local_defaults)
        self.__global = self
        self.__global.event_handler_map = {}

    def __init_logger(self):
        self.logger = logging.getLogger(self.name)
        self.logger.propagate = 0
        formatter = logging.Formatter(
            '[%(asctime)s: %(levelname)s] %(message)s')
        if self.config.debug:
            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(formatter)
            ch.setLevel(logging.DEBUG)
            self.logger.addHandler(ch)
            self.logger.setLevel(logging.DEBUG)
        else:
            fh = logging.FileHandler(self.config.log_path)
            fh.setFormatter(formatter)
            fh.setLevel(logging.INFO)
            self.logger.addHandler(fh)
            self.logger.setLevel(logging.INFO)

    def __init_broker_and_processors(self):
        self.__broker = Broker(self)
        self.__event_processor = EventProcessor(0, self)
        self.__event_processors = list()
        for i in range(self.config.processor_num):
            id = i + 1
            event_channel = EventChannel()
            event_channel.register(self.__broker)
            event_processor = EventProcessor(id, self, event_channel)
            self.__event_processors.append(event_processor)

    def __init_runtime_tree_storage(self):
        self.runtime_tree_storage = RuntimeTreeStorage(self.config.runtime_db)

    def __load_include_modules(self):
        pass

    def start(self):
        self.__broker.start()
        for event_processor in self.__event_processors:
            event_processor.start()

    def stop(self):
        self.__broker.stop()
        for event_processor in self.__event_processors:
            event_processor.stop()

    def find_handlers(self, event_name):
        handlers = []
        if event_name in self.__global.event_handler_map:
            handlers.extend(self.__global.event_handler_map[event_name])
        if event_name in self.__local.event_handler_map:
            handlers.extend(self.__local.event_handler_map[event_name])
        return handlers

    def on(self, event_name, handler, local=False):
        if local:
            if event_name not in self.__local.event_handler_map:
                self.__local.event_handler_map[event_name] = []
            self.__local.event_handler_map[event_name].append(handler)
        else:
            if event_name not in self.__global.event_handler_map:
                self.__global.event_handler_map[event_name] = []
            self.__global.event_handler_map[event_name].append(handler)

    def fire(self, event, background=True):
        if background:
            self.__broker.put(event)
        else:
            return self.__event_processor.process_event(event)

    def handler(self, event_name, throws_events=list(), local=False):
        def decorator(func):
            self.on(event_name, Handler(func, throws_events), local)
            def wrapper(*args, **kw):
                return func(*args, **kw)
            return wrapper
        return decorator

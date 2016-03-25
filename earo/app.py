#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
Copyright 2016 Everley

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from mediator import Mediator
from handler import Handler
from context import Context


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

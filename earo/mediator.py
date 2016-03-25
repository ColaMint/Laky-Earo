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

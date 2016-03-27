#!/usr/bin/python
# -*- coding:utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   Copyright 2016 Everley                                                    #
#                                                                             #
#   Licensed under the Apache License, Version 2.0 (the "License");           #
#   you may not use this file except in compliance with the License.          #
#   You may obtain a copy of the License at                                   #
#                                                                             #
#       http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                             #
#   Unless required by applicable law or agreed to in writing, software       #
#   distributed under the License is distributed on an "AS IS" BASIS,         #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#   See the License for the specific language governing permissions and       #
#   limitations under the License.                                            #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from mediator import Mediator
from handler import Handler
from context import Context
from processor import Processor


class App(object):

    _default_processor_tag_regex = '.+'

    def __init__(self, config):
        self.mediator = Mediator()
        self.config = config
        self.processors = []
        self._init_with_config()

    def _init_with_config(self):

        self.app_name = self.config.app_name

        for processor_tag_regex in self.config.processors_tag_regex:
            self.processors.append(
                Processor(processor_tag_regex))
        if self._default_processor_tag_regex not in self.processors:
            self.processors.append(
                Processor(self._default_processor_tag_regex))

    def handler(self, event_cls, emittion_statement=[]):
        def decorator(func):
            handler = Handler(event_cls, func, emittion_statement)
            self.mediator.register_event_handler(handler)
            return func
        return decorator

    def emit(self, event):
        matched_processor = self._match_processor(event)
        context = Context(self.mediator, event, matched_processor)
        context.process()
        return context

    def _match_processor(self, event):
        for processor in self.processors:
            if processor.match_event_tag(event):
                return processor

        # should never happens
        raise Exception('no matched processor found')

    def get_processor_by_tag_regex(self, processor_tag_regex):
        for processor in self.processors:
            if processor.tag_regex == processor_tag_regex:
                return processor
        return None


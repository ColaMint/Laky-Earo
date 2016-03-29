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
    """
    The application obejct of earo.
    """

    app_name = None
    """
    The name of this application.
    """

    mediator = None
    """
    An instance of :class:`earo.mediator.Mediator`.
    """

    config = None
    """
    An instance of :class:`earo.config.Config`.
    """

    processors = None
    """
    A list of :class:`earo.processor.Processor`.
    """

    _default_processor_tag_regex = '.+'
    """
    `self.processors` must contains a :class:`earo.processor.Processor` whose
    `tag_regex` is `_default_processor_tag_regex`.
    """

    def __init__(self, config):
        self.mediator = Mediator()
        self.config = config
        self._init_with_config()

    def _init_with_config(self):
        """
        #. Set `self.app_name` according to `self.config.app_name`.
        #. Set `self.processors` according to `self.config.processors_tag_regex`.
        """

        self.app_name = self.config.app_name

        self.processors = []
        for processor_tag_regex in self.config.processors_tag_regex:
            self.processors.append(
                Processor(processor_tag_regex))
        if self._default_processor_tag_regex not in self.processors:
            self.processors.append(
                Processor(self._default_processor_tag_regex))

    def handler(self, event_cls, emittion_statement=[]):
        """
        An decorator to register the function as an event handlers.
        The function's param list must be `(context, event)`.

        :param event_cls: The class of event to listen to.
        :param emittion_statement: a list of classes of events that may be emitted
        by the handler.
        """
        def decorator(func):
            handler = Handler(event_cls, func, emittion_statement)
            self.mediator.register_event_handler(handler)
            return func
        return decorator

    def emit(self, event):
        """
        Emit an event, return A :class:`earo.context.Context`.
        The :class:`earo.processor.ProcessFlow` is processed by a processor in
        `self.processors` whose `tag_regex` match `event.tag`.

        :param event: The event to emit.
        """
        matched_processor = self._match_processor(event)
        context = Context(self.mediator, event, matched_processor)
        context.process()
        return context

    def _match_processor(self, event):
        """
        Find the first processor in `self.processors` whose `tag_regex` match `event.tag`.

        :param event: The event to match.
        """
        for processor in self.processors:
            if processor.match_event_tag(event):
                return processor

        # should never happens
        raise Exception('no matched processor found')

    def get_processor_by_tag_regex(self, processor_tag_regex):
        """
        Find the :class:`earo.processor.Processor` in `self.processors` whose
        `tag_regex` is `processor_tag_regex`

        :param processor_tag_regex: The tag regex to find.
        """
        for processor in self.processors:
            if processor.tag_regex == processor_tag_regex:
                return processor
        return None


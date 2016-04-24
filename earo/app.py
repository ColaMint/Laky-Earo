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
from processor import Processor, ProcessFlow
from diagram import Diagram
from dashboard import Dashboard


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

    _source_event_cls_to_latest_active_process_flow = None
    """
    Record latest active :class:`earo.processor.Processor` for every source event.
    """

    dashboard = None
    """
    :class:`earo.dashboard.Dashboard`.
    """

    def __init__(self, config):

        self.mediator = Mediator()
        self.config = config
        self._source_event_cls_to_latest_active_process_flow = {}
        self._init_with_config()

    def _init_with_config(self):
        """
        #. Set `self.app_name` according to `self.config.app_name`.
        #. Set `self.processors` according to `self.config.processors_tag_regex`.
        """
        self.app_name = self.config.app_name

        if '.*' not in self.config.processors_tag_regex:
            self.config.processors_tag_regex.append('.*')
        self.processors = []
        for processor_tag_regex in self.config.processors_tag_regex:
            self.processors.append(
                Processor(processor_tag_regex))

    def handler(self, event_cls, derivative_events=[]):
        """
        An decorator to register the function as an event handlers.
        The function's param list must be `(context, event)`.

        :param event_cls: The class of event to listen to.
        :param emittion_statement: a list of classes of events that may be emitted
        by the handler.
        """
        def decorator(func):
            handler = Handler(event_cls, func, derivative_events)
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
        event_cls = type(event)

        matched_processor = self._match_processor(event)

        context = Context(self.mediator, event, matched_processor)
        context.process()

        self._source_event_cls_to_latest_active_process_flow[
            event_cls] = context.process_flow

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

    def latest_active_process_flow(self, source_event_cls):
        """
        Return the latest active :class:`earo.processor.ProcessFlow` of `source_event_cls`.

        :param source_event_cls: The class of the source event of the process flow
        """
        return self._source_event_cls_to_latest_active_process_flow.get(
            source_event_cls, None)

    def run_dashboard(self, daemon=True):
        """
        Run dashboard.

        :param daemon: If `True`, run dashboard in daemon thread.
        """
        self.dashboard = Dashboard(self)
        self.dashboard.run(daemon=daemon)

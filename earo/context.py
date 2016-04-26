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

from processor import ProcessFlow

class Context(object):
    """
    :class:`Context` holds some key obejct during processing the event.
    """

    mediator = None
    """
    An instance of :class:`earo.mediator.Mediator`.
    """

    source_event = None
    """
    The event emitted by :class:`earo.app.App`.
    """

    processor = None
    """
    The :class:`earo.processor.Processor` to process `self.source_event`.
    """

    process_flow = None
    """
    The :class:`earo.processor.Processor` maked by `self.processor`.
    """

    def __init__(self, mediator, source_event, processor):

        self.mediator = mediator
        self.source_event = source_event
        self.processor = processor
        self.process_flow = ProcessFlow(mediator, type(source_event))

    def process(self):
        """
        Use `self.processor` to do the process and set `self.process_flow`.
        """
        self.processor.process(self)

    def find_event(self, event_cls):
        """
        A reference to :func:`earo.processor.ProcessFlow.find_event`.
        """
        return self.process_flow.find_event(event_cls)

    def why_no_emittion(self, event_cls):
        """
        A reference to :func:`earo.processor.ProcessFlow.why_no_emittion`.
        """
        return self.process_flow.why_no_emittion(event_cls)

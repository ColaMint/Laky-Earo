# -*- coding:utf-8 -*-
from earo.processor import Processor

class Context(object):

    def __init__(self, mediator, source_event):
        self.mediator = mediator
        self.source_event = source_event
        self.process_flow = None
        self.processor = Processor(self)

    def process(self):
        self.process_flow = self.processor.process(self.source_event)

    def find_event(self, event_cls, return_first=True):
        return self.process_flow.find_event(event_cls, return_first)

#!/usr/bin/python
# -*- coding:utf-8 -*-


class Context(object):

    def __init__(self, mediator, source_event, processor):
        self.mediator = mediator
        self.source_event = source_event
        self.process_flow = None
        self.processor = processor

    def process(self):
        self.process_flow = self.processor.process(self)

    def find_event(self, event_cls):
        return self.process_flow.find_event(event_cls)

    def why_no_emittion(self, event_cls):
        return self.process_flow.why_no_emittion(event_cls)

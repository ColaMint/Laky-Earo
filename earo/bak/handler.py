#!/usr/bin/python
# -*- coding:utf-8 -*-
import traceback
"""
handler should declare what events may it fire.
"""


class Handler(object):

    def __init__(self, event_cls, handle_func, throw_events=list()):
        self.event_cls = event_cls
        self.handle_func = handle_func
        self.name = '%s.%s' % (handle_func.__module__, handle_func.__name__)
        self.throw_events = throw_events

    def handle(self, event, event_processor):
        if not isinstance(event, self.event_cls):
            raise TypeError(
                'Handle unexcepted event %s. Except %s.' %
                (type(event), self.event_cls))
        self.handle_func(
            self=event_processor, event=event)

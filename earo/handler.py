# -*- coding:utf-8 -*-

import inspect


class Handler(object):

    def __init__(self, event_cls, func, throw_events=list()):

        self.event_cls = event_cls
        self._validate_func(func)
        self.func = func
        self.name = '%s.%s' % (func.__module__, func.__name__)
        self.throw_events = throw_events

    def _validate_func(self, handle_func):

        argspec = inspect.getargspec(handle_func)
        if argspec.args != ['context', 'event']:
            raise TypeError(
                'Handler\'s function must be function_name(context, event)')

    def handle(self, context, event):

        if not isinstance(event, self.event_cls):
            raise TypeError(
                'Handle unexcepted event %s. Except %s.' %
                (type(event), self.event_cls))
        self.func(context, event)

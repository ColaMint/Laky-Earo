#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from earo.event import Event, StringField
from earo.handler import Handler
from earo.handler_runtime import HandlerRuntime
from earo.event_processor import EventProcessor
import unittest

names = []


def foo(self, event):
    names.append(event.name)


class AEvent(Event):

    name = StringField(default='earo')


class BEvent(Event):

    name = StringField(default='bbq')


class TestEvent(unittest.TestCase):

    def setUp(self):
        names = []

    def tearDown(self):
        pass

    def test_handler_name(self):
        handler = Handler(AEvent, foo)
        self.assertEqual('__main__.foo', handler.name)

    def test_handle_excepted_event(self):
        handler = Handler(AEvent, foo)
        event = AEvent()
        handler_runtime = HandlerRuntime(handler, event)
        handler.handle(event, handler_runtime)
        self.assertEqual(['earo'], names)

    def test_handle_unexcepted_event(self):
        handler = Handler(AEvent, foo)
        event = BEvent()
        handler_runtime = HandlerRuntime(handler, event)
        with self.assertRaises(TypeError):
            handler.handle(event, handler_runtime)


if __name__ == '__main__':
    unittest.main()

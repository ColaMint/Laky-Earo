#!/usr/bin/python
# -*- coding:utf-8 -*-

from earo.event import Event, Field
from earo.handler import Handler, NoEmittion
import unittest

names = []


class BEvent(Event):

    name = Field(str, 'bbq')


class TestHandler(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_invalid_func(self):

        names = []

        class AEvent(Event):
            name = Field(str, 'earo')

        def foo(event):
            names.append(event.name)

        with self.assertRaises(TypeError):
            Handler(AEvent, foo)

    def test_handle_excepted_event(self):

        names = []

        class AEvent(Event):
            name = Field(str, 'earo')

        def foo(context, event):
            names.append(event.name)

        handler = Handler(AEvent, foo)
        handler_runtime = handler.handle(None, AEvent())

        self.assertEqual(names, ['earo'])
        self.assertIsNotNone(handler_runtime.begin_time)
        self.assertIsNotNone(handler_runtime.end_time)
        self.assertIsNone(handler_runtime.exception)
        self.assertTrue(handler_runtime.succeeded)
        self.assertGreaterEqual(handler_runtime.time_cost, 0)

    def test_handle_unexcepted_event(self):

        names = []

        class AEvent(Event):
            name = Field(str, 'earo')

        class BEvent(Event):
            name = Field(str, 'bbq')

        def foo(context, event):
            names.append(event.name)

        handler = Handler(AEvent, foo)
        with self.assertRaises(TypeError):
            handler.handle(None, BEvent())

    def test_handle_event_with_exception(self):

        names = []

        class AEvent(Event):
            name = Field(str, 'earo')

        def foo(context, event):
            names.append(event.name)
            1 / 0

        handler = Handler(AEvent, foo)
        handler_runtime = handler.handle(None, AEvent())

        self.assertEqual(names, ['earo'])
        self.assertIsNotNone(handler_runtime.begin_time)
        self.assertIsNotNone(handler_runtime.end_time)
        self.assertIsNotNone(handler_runtime.exception)
        self.assertFalse(handler_runtime.succeeded)
        self.assertGreaterEqual(handler_runtime.time_cost, 0)

    def test_no_emittion(self):

        class AEvent(Event):
            pass

        class BEvent(Event):
            pass

        def foo(context, event):
            return NoEmittion(BEvent, 'test reason')

        handler = Handler(AEvent, foo, derivative_events=[BEvent])
        handler_runtime = handler.handle(None, AEvent())
        self.assertEqual(handler_runtime.why_no_emittion(BEvent), 'test reason')

    def test_description(self):

        class AEvent(Event):
            pass

        def foo(context, event):
            return NoEmittion(BEvent, 'test reason')

        handler = Handler(AEvent, foo, description='test handler description')
        self.assertEqual(handler.description, 'test handler description')

if __name__ == '__main__':
    unittest.main()

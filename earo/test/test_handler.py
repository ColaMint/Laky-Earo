# -*- coding:utf-8 -*-

from earo.event import Event, Field
from earo.handler import Handler
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
            handler = Handler(AEvent, foo)

    def test_handler_name(self):

        names = []

        class AEvent(Event):
            name = Field(str, 'earo')

        def foo(context, event):
            names.append(event.name)

        handler = Handler(AEvent, foo)
        self.assertEqual('__main__.foo', handler.name)

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
        self.assertGreater(handler_runtime.time_cost, 0)

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
        self.assertGreater(handler_runtime.time_cost, 0)

if __name__ == '__main__':
    unittest.main()

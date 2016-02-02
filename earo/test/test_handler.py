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

    def test_handler_excepted_event(self):

        names = []

        class AEvent(Event):
            name = Field(str, 'earo')

        def foo(context, event):
            names.append(event.name)

        handler = Handler(AEvent, foo)
        handler.handle(None, AEvent())

        self.assertEqual(names, ['earo'])

    def test_handler_unexcepted_event(self):

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

if __name__ == '__main__':
    unittest.main()

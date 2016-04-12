#!/usr/bin/python
# -*- coding:utf-8 -*-

from earo.event import Event
from earo.app import App
from earo.config import Config
import unittest


class TestApp(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_handler(self):

        config = Config()
        app = App(config)

        class AEvent(Event):
            pass

        @app.handler(AEvent)
        def foo(context, event):
            pass

        handlers = app.mediator.find_handlers(AEvent)
        self.assertTrue(len(handlers) > 0)

    def test_multi_processor(self):

        config = Config(processors_tag_regex=['.+\.event_a','.+\.event_b'])
        app = App(config)

        class EventA(Event):
            __tag__ = 'test.event_a'
            pass

        class EventB(Event):
            __tag__ = 'test.event_b'
            pass

        @app.handler(EventA)
        def fooA(context, event):
            pass

        @app.handler(EventB)
        def fooB(context, event):
            pass

        app.emit(EventA())
        app.emit(EventB())

        self.assertEqual(app.processors[0].tag_regex, '.+\.event_a')
        self.assertEqual(app.processors[1].tag_regex, '.+\.event_b')
        self.assertEqual(app.processors[2].tag_regex, '.+')

        processor_event_a = app.get_processor_by_tag_regex('.+\.event_a')
        processor_event_b = app.get_processor_by_tag_regex('.+\.event_b')
        processor_default = app.get_processor_by_tag_regex('.+')

        self.assertEqual(processor_event_a.process_count, 1)
        self.assertEqual(processor_event_b.process_count, 1)
        self.assertEqual(processor_default.process_count, 0)


if __name__ == '__main__':
    unittest.main()

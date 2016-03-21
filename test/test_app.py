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


if __name__ == '__main__':
    unittest.main()

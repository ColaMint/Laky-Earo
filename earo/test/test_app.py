# -*- coding:utf-8 -*-

from earo.event import Event
from earo.app import App
import unittest


class TestEvent(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_handler(self):
        app = App()

        class AEvent(Event):
            pass

        @app.handler(AEvent)
        def foo(context, event):
            pass

        handlers = app.mediator.find_handlers(AEvent)
        self.assertTrue(len(handlers)>0)

if __name__ == '__main__':
    unittest.main()

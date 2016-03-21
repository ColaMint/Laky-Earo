# -*- coding:utf-8 -*-

import unittest
from earo.mediator import Mediator
from earo.handler import Handler
from earo.event import Event


class TestMediator(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        mediator = Mediator()

        class EventA(Event):
            pass

        class EventB(Event):
            pass

        def foo(context, event):
            pass

        def boo(context, event):
            pass

        handler_1 = Handler(EventA, foo)
        handler_2 = Handler(EventA, boo)

        mediator.register_event_handler(handler_1)
        mediator.register_event_handler(handler_2)

        self.assertSequenceEqual(mediator.find_handlers(EventA), [handler_1, handler_2])
        self.assertSequenceEqual(mediator.find_handlers(EventB), [])

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from earo.handler import Handler
from earo.handler_runtime import HandlerRuntime
import unittest


def foo(name, age=15):
    pass


class TestEvent(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_handler_name(self):
        handler = Handler(foo)
        handler_runtime = HandlerRuntime(handler, None)
        self.assertEqual('__main__.foo', handler.name)

    def test_succeeded(self):
        handler = Handler(foo)
        handler_runtime = HandlerRuntime(handler, None)
        self.assertFalse(handler_runtime.succeeded)
        handler_runtime.record_begin_time()
        self.assertFalse(handler_runtime.succeeded)
        handler_runtime.record_end_time()
        self.assertTrue(handler_runtime.succeeded)
        handler_runtime.record_exception(Exception())
        self.assertFalse(handler_runtime.succeeded)

    def test_time_cost(self):
        handler = Handler(foo)
        handler_runtime = HandlerRuntime(handler, None)
        self.assertLess(handler_runtime.time_cost, 0)
        handler_runtime.record_begin_time()
        self.assertLess(handler_runtime.time_cost, 0)
        handler_runtime.record_end_time()
        self.assertGreater(handler_runtime.time_cost, 0)


if __name__ == '__main__':
    unittest.main()

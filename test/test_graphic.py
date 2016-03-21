#!/usr/bin/python
# -*- coding:utf-8 -*-

from earo.graphic import build_process_flow_html
import unittest


class TestHandler(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        build_process_flow_html(None, '/tmp/test')

if __name__ == '__main__':
    unittest.main()

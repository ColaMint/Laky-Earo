#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from earo.app import App
from earo.handler import Handler
from earo.event import Event
from earo.runtime_tree import RuntimeTree
import unittest
import sys
import time

config = {
    'debug': True,
    'log_path': '/tmp/test.log',
    'runtime_db': '/tmp/earo.db'
}

def foo(names, name):
    names.append('foo-%s' % name)


def boo(names, name):
    names.append('boo-%s' % name)


def eoo(names, name):
    names.append('eoo-%s' % name)
    raise Exception('eoo')


class TestEvent(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_config(self):
        app = App('test_config', config)
        self.assertEqual(True, app.config.debug)
        self.assertEqual('/tmp/test.log', app.config.log_path)
        self.assertEqual(None, app.config.unknown)

    def test_local(self):
        app = App('test_local', config)
        self.assertDictEqual(app._App__local.event_handler_map, dict())
        self.assertEqual(app._App__local.unknown, None)

    def test_on_and_find(self):
        app = App('test_on_and_find', config)
        handlers = app.find_handlers('show')
        self.assertListEqual(handlers, list())
        foo_handler = Handler(foo)
        boo_handler = Handler(boo)
        app.on('show', foo_handler)
        app.on('show', boo_handler, True)
        handlers = app.find_handlers('show')
        self.assertListEqual(handlers, [foo_handler, boo_handler])
        self.assertListEqual(
            app._App__global.event_handler_map['show'],
            [foo_handler])
        self.assertListEqual(
            app._App__local.event_handler_map['show'],
            [boo_handler])

    def test_allowed_fire(self):
        app = App('test_allowed_fire', config)
        def fire(self, names):
            names.append('fire')
            event = Event('display', names=names, name='B')
            self.fire(event)
        foo_handler = Handler(foo)
        boo_handler = Handler(boo)
        eoo_handler = Handler(eoo)
        fire_handler = Handler(fire, ['display'])
        app.on('show', foo_handler)
        app.on('show', boo_handler, True)
        app.on('show', fire_handler, True)
        app.on('display', eoo_handler)
        names = list()
        show_event = Event('show', names=names, name='A')
        runtime_tree = app.fire(show_event, False)
        self.assertListEqual(
            names,
            ['foo-A', 'boo-A', 'fire', 'eoo-B'])
        self.assertEqual(runtime_tree.event_count, 2)
        self.assertEqual(runtime_tree.handler_runtime_count, 4)
        self.assertEqual(runtime_tree.exception_count, 1)
        self.assertNotEqual(runtime_tree.begin_time, None)
        self.assertNotEqual(runtime_tree.end_time, None)
        self.assertNotEqual(runtime_tree.time_cost, -1)

    def test_not_allowed_fire(self):
        app = App('test_not_allowed_fire', config)
        def fire(self, names):
            names.append('fire')
            event = Event('display', names=names, name='B')
            self.fire(event)
        eoo_handler = Handler(eoo)
        fire_handler = Handler(fire)
        app.on('show', fire_handler, True)
        app.on('display', eoo_handler)
        names = list()
        show_event = Event('show', names=names, name='A')
        runtime_tree = app.fire(show_event, False)
        self.assertListEqual(
            names,
            ['fire'])
        self.assertEqual(runtime_tree.event_count, 1)
        self.assertEqual(runtime_tree.handler_runtime_count, 1)
        self.assertEqual(runtime_tree.exception_count, 1)
        self.assertNotEqual(runtime_tree.begin_time, None)
        self.assertNotEqual(runtime_tree.end_time, None)
        self.assertNotEqual(runtime_tree.time_cost, -1)

    def test_handler_decorator(self):
        app = App('test_handler_decorator', config)
        @app.handler('show', ['display'], True)
        def koo(self, names, name):
            names.append('koo-%s' % (name,))
            event = Event('display', names=names, name='B')
            self.fire(event)
        foo_handler = Handler(foo)
        app.on('display', foo_handler)
        names = list()
        show_event = Event('show', names=names, name='A')
        runtime_tree = app.fire(show_event, False)
        self.assertListEqual(
            names,
            ['koo-A', 'foo-B'])
        self.assertEqual(runtime_tree.event_count, 2)
        self.assertEqual(runtime_tree.handler_runtime_count, 2)
        self.assertEqual(runtime_tree.exception_count, 0)
        self.assertNotEqual(runtime_tree.begin_time, None)
        self.assertNotEqual(runtime_tree.end_time, None)
        self.assertNotEqual(runtime_tree.time_cost, -1)


    def test_pickle(self):
        app = App('test_pickle', config)
        def fire(self):
            names.append('fire')
            event = Event('display', names=names, name='B')
            self.fire(event)
        foo_handler = Handler(foo)
        boo_handler = Handler(boo)
        eoo_handler = Handler(eoo)
        fire_handler = Handler(fire, ['display'])
        app.on('show', foo_handler)
        app.on('show', boo_handler, True)
        app.on('show', fire_handler, True)
        app.on('display', eoo_handler)
        names = list()
        show_event = Event('show', names=names, name='A')
        runtime_tree = app.fire(show_event, False)
        self.assertDictEqual(
            RuntimeTree.loads(
                runtime_tree.dumps()),
         runtime_tree.dict)


    def test_start_and_stop(self):
        app = App('test_start_and_stop', config)
        app.start()
        foo_handler = Handler(foo)
        boo_handler = Handler(boo)
        app.on('show', foo_handler)
        app.on('show', boo_handler, True)
        names = list()
        show_event = Event('show', names=names, name='background')
        app.fire(show_event, False)
        time.sleep(2)
        app.stop()
        self.assertListEqual(
            names,
            ['foo-background', 'boo-background'])


if __name__ == '__main__':
    unittest.main()

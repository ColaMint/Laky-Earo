#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from earo.runtime_tree import RuntimeTreeStorage
from earo.app import App
from earo.handler import Handler
from earo.event import Event
import unittest

db_path = '/tmp/earo.db'


def foo(name):
    pass


class TestEvent(unittest.TestCase):

    def setUp(self):
        self.__delete_db()

    def tearDown(self):
        self.__delete_db()

    def __delete_db(self):
        if os.path.exists(db_path):
            os.remove(db_path)

    def test_save_and_find(self):
        storage = RuntimeTreeStorage(db_path)
        app = App('test_save_and_find')
        foo_handler = Handler(foo)
        app.on('show', foo_handler)
        show_event = Event('show', name='A')
        runtime_tree = app.fire(show_event, False)
        storage.save(runtime_tree)
        self.assertEqual(runtime_tree.dict, storage.find(runtime_tree.id))

    def test_remove(self):
        storage = RuntimeTreeStorage(db_path)
        app = App('test_remove')
        foo_handler = Handler(foo)
        app.on('show', foo_handler)
        show_event = Event('show', name='A')
        runtime_tree = app.fire(show_event, False)
        storage.save(runtime_tree)
        storage.remove('test_id')
        self.assertEqual(runtime_tree.dict, storage.find(runtime_tree.id))
        storage.remove(runtime_tree.id)
        self.assertEqual(None, storage.find(runtime_tree.id))

    def test_remove_all(self):
        storage = RuntimeTreeStorage(db_path)
        app = App('test_remove_all')
        foo_handler = Handler(foo)
        app.on('show', foo_handler)
        show_event = Event('show', name='A')
        runtime_tree = app.fire(show_event, False)
        storage.save(runtime_tree)
        storage.remove_all()
        self.assertEqual(None, storage.find(runtime_tree.id))


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from earo.event import Event, StringField, BooleanField, IntegerField, FloatField, ListField, DictField
import unittest


class AEvent(Event):

    str_field = StringField(default='str')
    bool_field = BooleanField(default=True)
    int_field = IntegerField(default=8)
    float_field = FloatField(default=8.8)
    list_field = ListField(default=[3, 6, 8])
    dict_field = DictField(default={8: 8})


class TestEvent(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        event = AEvent()
        self.assertEqual('str', event.str_field)
        event.str_field = 'rts'
        self.assertEqual('rts', event.str_field)
        self.assertEqual(True, event.bool_field)
        event.bool_field = False
        self.assertEqual(False, event.bool_field)
        self.assertEqual(8, event.int_field)
        event.int_field = 9
        self.assertEqual(9, event.int_field)
        self.assertEqual(8.8, event.float_field)
        event.float_field = 9.9
        self.assertEqual(9.9, event.float_field)
        self.assertSequenceEqual([3, 6, 8], event.list_field)
        event.list_field = [2, 4, 6]
        self.assertSequenceEqual([2, 4, 6], event.list_field)
        self.assertDictEqual({8: 8}, event.dict_field)
        event.dict_field = {9: 9}
        self.assertEqual({9: 9}, event.dict_field)


    def test_type_error(self):
        with self.assertRaises(TypeError):
            class BEvent(Event):
                str_field = StringField(default=100)
            BEvent()
        with self.assertRaises(TypeError):
            class BEvent(Event):
                str_field = BooleanField(default=100)
            BEvent()
        with self.assertRaises(TypeError):
            class BEvent(Event):
                str_field = IntegerField(default='test')
            BEvent()
        with self.assertRaises(TypeError):
            class BEvent(Event):
                str_field = FloatField(default=100)
            BEvent()
        with self.assertRaises(TypeError):
            class BEvent(Event):
                str_field = ListField(default=100)
            BEvent()
        with self.assertRaises(TypeError):
            class BEvent(Event):
                str_field = DictField(default=100)
            BEvent()


if __name__ == '__main__':
    unittest.main()

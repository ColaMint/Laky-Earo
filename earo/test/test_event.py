# -*- coding:utf-8 -*-

from earo.event import Event, Field
import unittest


class TestEvent(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):

        class AEvent(Event):
            str_field = Field(str, 'test')
            bool_field = Field(bool, True)
            int_field = Field(int, 8)
            float_field = Field(float, 8.8)
            list_field = Field(list, [3, 6, 8])
            dict_field = Field(dict, {8: 8})

        event = AEvent(float_field=7.7)
        self.assertEqual('test', event.str_field)
        event.str_field = 'rts'
        self.assertEqual('rts', event.str_field)
        self.assertEqual(True, event.bool_field)
        event.bool_field = False
        self.assertEqual(False, event.bool_field)
        self.assertEqual(8, event.int_field)
        event.int_field = 9
        self.assertEqual(9, event.int_field)
        self.assertEqual(7.7, event.float_field)
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
                str_field = Field(str, 100)
            BEvent()
        with self.assertRaises(TypeError):
            class BEvent(Event):
                str_field = Field(bool, 100)
            BEvent()
        with self.assertRaises(TypeError):
            class BEvent(Event):
                str_field = Field(int, 'test')
            BEvent()
        with self.assertRaises(TypeError):
            class BEvent(Event):
                str_field = Field(float, 100)
            BEvent()
        with self.assertRaises(TypeError):
            class BEvent(Event):
                str_field = Field(list, 100)
            BEvent()
        with self.assertRaises(TypeError):
            class BEvent(Event):
                str_field = Field(dict, 100)
            BEvent()

if __name__ == '__main__':
    unittest.main()

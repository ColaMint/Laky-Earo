#!/usr/bin/python
# -*- coding:utf-8 -*-

from earo.config import Config
import unittest


class TestConfig(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_config_with_default_value(self):
        config = Config()
        self.assertEqual(config.app_name, 'earo')
        config.app_name = 'test'
        self.assertEqual(config.app_name, 'test')

    def test_config_with_init_value(self):
        config = Config(app_name='test')
        self.assertEqual(config.app_name, 'test')
        config.app_name = 'money'
        self.assertEqual(config.app_name, 'money')

    def test_config_with_key_error(self):
        with self.assertRaises(KeyError):
            config = Config(
                config={
                    'app_name': 'test',
                    'not_existed_key': 'test'})
        with self.assertRaises(KeyError):
            config = Config()
            config.not_existed_key = 'test'


if __name__ == '__main__':
    unittest.main()

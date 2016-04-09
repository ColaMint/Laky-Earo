#!/usr/bin/python
# -*- coding:utf-8 -*-

import unittest
from earo.event import Event
from earo.app import App
from earo.config import Config
from earo.dashboard import Dashboard
import json


class AEvent(Event):

    __tag__ = 'a.event'

    __description__ = 'This is AEvent\'s description.'


class TestDashboard(unittest.TestCase):

    def setUp(self):

        self.config = Config(
            source_event_cls=(AEvent,),
            processors_tag_regex=('a\..+',)
        )
        self.app = App(self.config)

        @self.app.handler(AEvent)
        def foo(context, event):
            pass

        self.dashboard = Dashboard(self.app)
        self.dashboard.flask_app.debug = True
        self.client = self.dashboard.flask_app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        rv = self.client.get('/')
        self.assertTrue('hello' in rv.data)

    def test_configuration(self):
        rv = self.client.get('/configuration')
        result = json.loads(rv.data)
        self.assertEqual(result['c'], 0)
        self.assertTrue('app_name' in result['d'])

    def test_source_event_cls_list(self):
        rv = self.client.get('/source_event_cls_list')
        result = json.loads(rv.data)
        self.assertEqual(result['c'], 0)
        self.assertDictEqual(
            result['d'][0],
            {'source_event_cls': 'test_dashboard.AEvent',
             'source_event_tag': 'a.event',
             'source_event_description': 'This is AEvent\'s description.'})

    def test_processor_list(self):
        self.app.emit(AEvent())
        rv = self.client.get('/processor_list')
        result = json.loads(rv.data)
        self.assertEqual(result['c'], 0)
        self.assertSequenceEqual(result['d'][0]['tag_regex'], 'a\..+')
        self.assertSequenceEqual(result['d'][1]['tag_regex'], '.+')
        self.assertTrue('process_count' in result['d'][0])
        self.assertTrue('exception_count' in result['d'][0])
        self.assertTrue('event_statistics' in result['d'][0])
        self.assertTrue('test_dashboard.AEvent' in result[
                        'd'][0]['event_statistics'])
        self.assertTrue(
                        'process_count'
                        in
                        result['d'][0]['event_statistics']
                        ['test_dashboard.AEvent'])
        self.assertTrue('exception_count' in result['d'][0][
                        'event_statistics']['test_dashboard.AEvent'])
        self.assertTrue(
                        'min_time_cost'
                        in
                        result['d'][0]['event_statistics']
                        ['test_dashboard.AEvent'])
        self.assertTrue(
                        'max_time_cost'
                        in
                        result['d'][0]['event_statistics']
                        ['test_dashboard.AEvent'])

    def test_preview_process_flow(self):
        rv = self.client.get('/preview_process_flow/test_dashboard.AEvent')
        result = json.loads(rv.data)
        self.assertEqual(result['c'], 0)
        self.assertTrue('title' in result['d'])
        self.assertTrue('color' in result['d'])
        self.assertTrue('body' in result['d'])
        self.assertTrue('footer' in result['d'])

    def test_latest_process_flow(self):
        self.app._source_event_cls_to_latest_active_process_flow.clear()
        rv = self.client.get('/latest_process_flow/test_dashboard.AEvent')
        result = json.loads(rv.data)
        self.assertEqual(result['c'], -1)

        self.app.emit(AEvent())

        rv = self.client.get('/latest_process_flow/test_dashboard.AEvent')
        result = json.loads(rv.data)
        self.assertEqual(result['c'], 0)
        self.assertTrue('title' in result['d'])
        self.assertTrue('color' in result['d'])
        self.assertTrue('body' in result['d'])
        self.assertTrue('footer' in result['d'])


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/python
# -*- coding:utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   Copyright 2016 Everley                                                    #
#                                                                             #
#   Licensed under the Apache License, Version 2.0 (the "License");           #
#   you may not use this file except in compliance with the License.          #
#   You may obtain a copy of the License at                                   #
#                                                                             #
#       http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                             #
#   Unless required by applicable law or agreed to in writing, software       #
#   distributed under the License is distributed on an "AS IS" BASIS,         #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#   See the License for the specific language governing permissions and       #
#   limitations under the License.                                            #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from flask import Flask, jsonify, render_template
from earo.processor import ProcessFlow
from earo.diagram import Diagram
import threading
import os

template_folder = static_folder = os.path.join(
    os.path.dirname(__file__), 'static')


class Dashboard(object):
    """
    A `flask` server to display useful information of :class:`earo.app.App`.
    """

    earo_app = None
    """
    The monitored :class:`earo.app.App`.
    """

    flask_app = None
    """
    The :class:`flask.Flask` odject to serve http requests.
    """

    _source_event_cls_map = None
    """
    A `dict`.
    The `key` is from :func:`earo.event.Event.key`.
    The `value` is the class of :class:`earo.event.Event`'s subclass.
    """

    def __init__(self, earo_app):

        self.earo_app = earo_app
        self.flask_app = Flask('earo',
                               static_folder=static_folder,
                               static_url_path='/static',
                               template_folder=template_folder)
        self._source_event_cls_map = {}
        for source_event_cls in self.earo_app.config.source_event_cls:
            self._source_event_cls_map[
                source_event_cls.key()] = source_event_cls
        self._init_routes()

    def _init_routes(self):
        """
        Initial falsk routes.
        """

        def json_output(code, data=None):
            return jsonify({'c': code, 'd': data})

        @self.flask_app.route('/')
        def index():
            return render_template('dashboard.html')

        @self.flask_app.route('/configuration')
        def configuration():
            config = self.earo_app.config.dict
            config['source_event_cls'] = [
                source_event_cls.key()
                for source_event_cls in self.earo_app.config.source_event_cls]
            return json_output(0, config)

        @self.flask_app.route('/source_event_cls_list')
        def source_event_cls_list():
            source_event_cls_list = [{
                    'source_event_cls': source_event_cls_key,
                    'source_event_tag': source_event_cls.tag(),
                    'source_event_description': source_event_cls.description()
                }
                 for source_event_cls_key,
                 source_event_cls in self._source_event_cls_map.iteritems()]
            return json_output(0, source_event_cls_list)

        @self.flask_app.route('/processor_list')
        def processor_list():
            processor_list = []
            for processor in self.earo_app.processors:
                event_statistics = {}
                for source_event_cls in processor.event_process_list():
                    event_statistics[source_event_cls.key()] = {
                        'process_count': processor.event_process_count(source_event_cls),
                        'exception_count': processor.event_exception_count(source_event_cls),
                        'min_time_cost': processor.event_min_time_cost(source_event_cls),
                        'max_time_cost': processor.event_max_time_cost(source_event_cls)}
                processor_list.append({
                    'tag_regex': processor.tag_regex,
                    'process_count': processor.process_count,
                    'exception_count': processor.exception_count,
                    'event_statistics': event_statistics,
                })
            return json_output(0, processor_list)

        @self.flask_app.route('/preview_process_flow/<source_event_cls_key>')
        def preview_process_flow(source_event_cls_key):
            if source_event_cls_key in self._source_event_cls_map:
                source_event_cls = self._source_event_cls_map[
                                                              source_event_cls_key]
                process_flow = ProcessFlow(
                    self.earo_app.mediator, source_event_cls)
                diagram = Diagram(process_flow)
                return render_template(
                    'process_flow.html',
                    title='Preview Process Flow',
                    diagram=diagram.json)
            else:
                return json_output(-1, 'event not exists')

        @self.flask_app.route('/latest_process_flow/<source_event_cls_key>')
        def latest_process_flow(source_event_cls_key):
            if source_event_cls_key in self._source_event_cls_map:
                source_event_cls = self._source_event_cls_map[
                                                              source_event_cls_key]
                process_flow = self.earo_app.latest_active_process_flow(
                    source_event_cls)
                if process_flow:
                    diagram = Diagram(process_flow)
                    return render_template(
                        'process_flow.html',
                        title='Latest Process Flow',
                        diagram=diagram.json)
                else:
                    return json_output(
                        -1, 'latest active process flow not found')

            else:
                return json_output(-1, 'event not exists')

    def run(self, daemon=False):
        """
        Run flask.

        :param daemon: If `True`, run flask in daemon thread.
        """

        def run_flask():
            self.flask_app.run(
                host=self.earo_app.config.dashboard_host,
                port=self.earo_app.config.dashboard_port)

        if daemon:
            th = threading.Thread(target=run_flask)
            th.daemon = True
            th.start()
        else:
            run_flask()

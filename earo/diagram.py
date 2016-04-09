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

import os
import shutil
import json
from jinja2 import Environment, FileSystemLoader
from earo.processor import NodeType
from enum import Enum

template_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'template')

static_path = os.path.join(template_path, 'static')


class Color(Enum):
    """
    Enum type of colors used by javascript.
    """
    Red = 1
    Blue = 2
    Green = 3
    Yellow = 4
    Grey = 5


class ContentType(Enum):
    """
    Enum type of :class:`Content`
    """
    Text = 1
    Table = 2


class Content(object):
    """
    Help :class:`Diagram` to transfer :class:`earo.processor.ProcessFlow` to
    json.
    """

    content_type = None
    """
    One of :class:`ContentType`.
    """

    __params__ = None
    """
    Store key/value in subclass.
    """

    def __init__(self, content_type, **kwargs):
        self.content_type = content_type
        self.__params__ = {}
        for k, v in kwargs.iteritems():
            self.__params__[k] = v

    def to_json(self):
        """
        Dumps to json string.
        """
        return json.dumps(self.to_dict())

    def to_dict(self):
        """
        Dumps to json.
        """
        content_dict = {
            'content_type': self.content_type,
        }

        for k, v in self.__params__.iteritems():
            content_dict[k] = v

        return content_dict


class TextContent(Content):
    """
    Used to make a text in html.
    """

    def __init__(self, text=''):
        super(TextContent, self).__init__(
            ContentType.Text, text=text)

    @property
    def text(self):
        return self.__params__['text']


class TableContent(Content):
    """
    Used to make a table in html.
    """

    def __init__(self, table_head=None, table_rows=None):
        if table_head is None:
            table_head = []
        if table_rows is None:
            table_rows = []
        super(TableContent, self).__init__(
            ContentType.Table, table_head=table_head, table_rows=table_rows)

    @property
    def table_head(self):
        return self.__params__['table_head']

    @property
    def table_rows(self):
        return self.__params__['table_rows']

    def append_table_row(self, table_row):
        self.__params__['table_rows'].append([str(v) for v in table_row])


class Panel(object):
    """
    Help :class:`Diagram` to transfer :class:`earo.processor.ProcessFlow` to
    json.
    """

    def __init__(self):
        self.color = None
        self.title = None
        self.body = None
        self.footer = None
        self.next_panels = []

    def append_next_panel(self, panel):
        self.next_panels.append(panel)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        panel_dict = {
            'color': self.color,
            'next_panels': []
        }
        panel_dict['title'] = None if self.title is None \
            else self.title.to_dict()
        panel_dict['body'] = None if self.body is None \
            else self.body.to_dict()
        panel_dict['footer'] = None if self.footer is None \
            else self.footer.to_dict()
        for next_panel in self.next_panels:
            panel_dict['next_panels'].append(next_panel.to_dict())
        return panel_dict


class NodePanel(Panel):
    """
    Help :class:`Diagram` to transfer :class:`earo.processor.ProcessFlow` to
    json.
    """

    def __init__(self, process_flow, node):
        super(NodePanel, self).__init__()
        self._parse_node(process_flow, node)

    def _parse_node(self, process_flow, node):
        if node.type == NodeType.Event:
            self._parse_event_node(process_flow, node)
        elif node.type == NodeType.Handler:
            self._parse_handler_node(process_flow, node)
        else:
            raise TypeError('Unknown NodeType: `%s`.' % (node.type,))

    def _parse_event_node(self, process_flow, event_node):
        event_cls = event_node.inactive_item
        self.title = TextContent('%s.%s' % (
            event_cls.__module__,
            event_cls.__name__))

        if process_flow.active:
            if event_node.active:
                event = event_node.active_item
                self.color = Color.Blue
                if event.no_field:
                    pass
                else:
                    self.body = TableContent(table_head=('Field', 'Value'))
                    for k, v in event.params.iteritems():
                        self.body.append_table_row((k, v))
            else:
                event = event_cls()
                self.color = Color.Grey
                if event.no_field:
                    pass
                else:
                    self.body = TableContent(
                        table_head=('Field', 'Default Value'))
                    for k, v in event.params.iteritems():
                        self.body.append_table_row((k, v))
                self.footer = TextContent(
                    'why no emittion: %s' %
                    (process_flow.why_no_emittion(event_cls),))
        else:
            event = event_cls()
            self.color = Color.Blue
            if event.no_field:
                pass
            else:
                self.body = TableContent(table_head=('Field', 'Default Value'))
                for k, v in event.params.iteritems():
                    self.body.append_table_row((k, v))

    def _parse_handler_node(self, process_flow, handler_node):
        handler = handler_node.inactive_item
        self.title = TextContent('%s.%s' % (
            handler.func.__module__,
            handler.func.__name__))

        if process_flow.active:
            if handler_node.active:
                handler_runtime = handler_node.active_item
                if handler_runtime.succeeded:
                    self.color = Color.Green
                    self.body = TableContent(table_head=('Field', 'Value'))
                    self.body.append_table_row(
                        ('time_cost', '%s ms' %
                         handler_runtime.time_cost))
                else:
                    self.color = Color.Red
                    self.body = TextContent(str(handler_runtime.exception))
            else:
                self.color = Color.Grey
                self.body = TableContent(table_head=('Emittion Statement',))
                if handler.no_emittion_statement:
                    pass
                else:
                    self.body = TableContent(table_head=('Field', 'Value',))

                    emittion_statement_str = ', '.join(
                        [event_cls.key()
                         for event_cls in handler.emittion_statement])
                    self.body.append_table_row(
                        ('emittion_statement', emittion_statement_str))
        else:
            self.color = Color.Green
            if handler.no_emittion_statement:
                pass
            else:
                self.body = TableContent(table_head=('Field', 'Value',))

                emittion_statement_str = ', '.join(
                    [event_cls.key() for event_cls in
                     handler.emittion_statement])
                self.body.append_table_row(
                    ('emittion_statement', emittion_statement_str))


class SummaryPanel(Panel):
    """
    Help :class:`Diagram` to transfer :class:`earo.processor.ProcessFlow` to
    json.
    """

    def __init__(self, process_flow):
        super(SummaryPanel, self).__init__()
        self._parse_process_flow(process_flow)

    def _parse_process_flow(self, process_flow):
        self.color = Color.Yellow
        if process_flow.active:
            self.title = TextContent('Processor Flow Summary')
            self.body = TableContent(table_head=('Field', 'Value'))
            self.body.append_table_row(
                ('begin_time', process_flow.begin_time.strftime('%Y-%m-%d %H:%M:%S')))
            self.body.append_table_row(
                ('time_cost', '%d ms' % process_flow.time_cost))
            self.body.append_table_row(
                ('exception_count', process_flow.exception_count))
        else:
            self.title = TextContent('Processor Flow Preview')


class Diagram(object):
    """
    Transfer :class:`earo.processor.ProcessFlow` to html
    """

    json = None
    """
    Used by javascript to build elements to show the
    :class:`earo.processor.ProcessFlow` in html.
    """

    def __init__(self, process_flow=None, json=None):
        """
        Initial from :class:`earo.processor.ProcessFlow` or `json`.

        :param process_flow: :class:`earo.processor.ProcessFlow`.
        :param json: json get from `self.to_json()`.
        """
        self.process_flow = process_flow
        if process_flow:
            self._from_process_flow(process_flow)
        elif json:
            self.json = json
        else:
            raise AttributeError('both `process_flow` and `json` are None')

    def _from_process_flow(self, process_flow):

        def build_node_panel_recursively(node):
            panel = NodePanel(process_flow, node)
            for child_node in node.child_nodes:
                next_panel = build_node_panel_recursively(child_node)
                panel.append_next_panel(next_panel)
            return panel

        summary_panel = SummaryPanel(process_flow)
        root_node_panel = build_node_panel_recursively(
                process_flow.root)
        summary_panel.append_next_panel(root_node_panel)
        self.dict = summary_panel.to_dict()
        self.json = summary_panel.to_json()

    def to_html(self, dest_dir):
        """
        Transfer :class:`earo.processor.ProcessFlow` to html in `dest_dir`.

        :param dest_dir: The directory to save the ouput html.
        """
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir, 0o744)

        env = Environment(loader=FileSystemLoader(template_path))
        template = env.get_template('process_flow.html')
        result = template.render(root_panel=self.json)

        # create process_flow.html
        dest_filepath = os.path.join(dest_dir, 'process_flow.html')
        with open(dest_filepath, 'w') as f:
            f.write(result)

        # copy statc resource
        dest_static_path = os.path.join(dest_dir, 'static')
        if os.path.exists(dest_static_path):
            shutil.rmtree(dest_static_path)
        shutil.copytree(static_path, dest_static_path)

    def to_json(self):
        """
        Dumps to json string, which can be saved and used to reinitial
        :class:`Diagram` next time.
        """
        return self.json

#!/usr/bin/python
# -*- coding:utf-8 -*-

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
    Red     = 1
    Blue    = 2
    Green   = 3
    Yellow  = 4
    Grey    = 5

class ContentType(Enum):
    Text  = 1;
    Table = 2;


class Content(object):

    def __init__(self, content_type, **kwargs):
        self.content_type = content_type
        self.__params__ = {}
        for k, v in kwargs.iteritems():
            self.__params__[k] = v

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        content_dict = {
            'content_type': self.content_type,
        }

        for k, v in self.__params__.iteritems():
            content_dict[k] = v

        return content_dict

class TextContent(Content):

    def __init__(self, text=''):
        super(TextContent, self).__init__(
            ContentType.Text, text=text)

    @property
    def text(self):
        return self.__params__['text']

class TableContent(Content):

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

    def __init__(self, node):
        self.color = None
        self.title = None
        self.body = None
        self.footer = None
        self.next_panels = []
        self.__parse_node(node)

    def __parse_node(self, node):
            if node.type == NodeType.Event:
                self.__parse_event_node(node)
            elif node.type == NodeType.Handler:
                self.__parse_handler_node(node)
            else:
                raise TypeError('Unknown NodeType: `%s`.' % (node.type,))

    def __parse_event_node(self, event_node):
        event_cls = event_node.inactive_item
        self.title = TextContent('%s.%s' % (
            event_cls.__module__,
            event_cls.__name__))

        if event_node.active:
            event = event_node.active_item
            self.color = Color.Blue
            self.body = TableContent(table_head=('Field', 'Value'))
            for k, v in event.params.iteritems():
                self.body.append_table_row((k, v))
        else:
            self.color = Color.Grey

    def __parse_handler_node(self, handler_node):
        handler = handler_node.inactive_item
        self.title = TextContent('%s.%s' % (
            handler.func.__module__,
            handler.func.__name__))

        if handler_node.active:
            handler_runtime = handler_node.active_item
            self.color = Color.Green if handler_runtime.succeeded else Color.Red
            self.body = TableContent(table_head=('Field', 'Value'))
            self.body.append_table_row(('exception', handler_runtime.exception))
            self.body.append_table_row(('no_emittions', handler_runtime.no_emittions))
            self.body.append_table_row(('time_cost', '%s ms' % handler_runtime.time_cost))
        else:
            self.color = Color.Grey

    def append_next_panel(self, panel):
        self.next_panels.append(panel)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        panel_dict = {
            'color': self.color,
            'next_panels': []
        }
        panel_dict['title'] = None if self.title is None else self.title.to_dict()
        panel_dict['body'] = None if self.body is None else self.body.to_dict()
        panel_dict['footer'] = None if self.footer is None else self.footer.to_dict()
        for next_panel in self.next_panels:
            panel_dict['next_panels'].append(next_panel.to_dict())
        return panel_dict


class Diagram(object):

    def __init__(self, process_flow):
        self.process_flow = process_flow
        self.__build_panel()

    def __build_panel(self):

        def build_panel_recursively(node):
            panel = Panel(node)
            for child_node in node.child_nodes:
                next_panel = build_panel_recursively(child_node)
                panel.append_next_panel(next_panel)
            return panel

        self.first_panel = build_panel_recursively(self.process_flow.root)

    def transfer_process_flow_to_html(self, dest_dir):

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir, 0o744)

        env = Environment(loader=FileSystemLoader(template_path))
        template = env.get_template('process_flow.html')
        result = template.render(first_panel=self.first_panel.to_json())

        # create process_flow.html
        dest_filepath = os.path.join(dest_dir, 'process_flow.html')
        with open(dest_filepath, 'w') as f:
            f.write(result)

        # copy statc resource
        dest_static_path = os.path.join(dest_dir, 'static')
        if os.path.exists(dest_static_path):
            shutil.rmtree(dest_static_path)
        shutil.copytree(static_path, dest_static_path)

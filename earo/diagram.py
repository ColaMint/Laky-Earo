#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import shutil
from jinja2 import Environment, FileSystemLoader
from earo.processor import NodeType
from enum import Enum
import json


class Color(Enum):
    Red = 1
    Blue = 2
    Green = 3
    Yellow = 4
    White = 5

template_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'template')

static_path = os.path.join(template_path, 'static')


class Panel(object):

    def __init__(self, color=None, title=None, body=None, footer=None):
        self.color = color
        self.body = body
        self.footer = footer
        self.next_panels = []

    def append_next_panel(self, panel):
        self.next_panels.append(panel)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        panel_dict = {
            'color': self.color,
            'title': self.title,
            'body': self.body,
            'footer': self.footer,
            'next_panels': []
        }
        for next_panel in self.next_panels:
            panel_dict['next_panels'].append(next_panel.to_dict())
        return panel_dict


class Diagram(object):

    def __init__(self, process_flow):
        self.process_flow = process_flow
        self.__build_panel()

    def __build_panel(self):

        def build_panel_recursively(node):
            panel = Panel()
            if node.type == NodeType.Event:
                event_cls = node.inactive_item
                panel.title = '%s.%s' % (
                    event_cls.__module__,
                    event_cls.__name__)

                if node.active:
                    event = node.active_item
                    panel.body = str(event.params)
                    panel.color = Color.Blue
                else:
                    panel.color = Color.White

                for child_node in node.child_nodes:
                    next_panel = build_panel_recursively(child_node)
                    panel.append_next_panel(next_panel)
                return panel
            elif node.type == NodeType.Handler:
                handler = node.inactive_item
                panel.title = '%s.%s' % (
                    handler.func.__module__,
                    handler.func.__name__)

                if node.active:
                    handler_runtime = node.active_item
                    if handler_runtime.succeeded:
                        panel.color = Color.Green
                    else:
                        panel.color = Color.Red
                else:
                    panel.color = Color.White

                for child_node in node.child_nodes:
                    next_panel = build_panel_recursively(child_node)
                    panel.append_next_panel(next_panel)
                return panel
            else:
                raise TypeError('Unknown NodeType: `%s`.' % (node.type,))

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

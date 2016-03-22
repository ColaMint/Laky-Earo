#!/usr/bin/python
# -*- coding:utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import os

template_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'template')


def process_flow_to_html(root, dst_dir):

    os.makedirs(dst_dir, 0444)
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template('process_flow.html')
    print template.render()

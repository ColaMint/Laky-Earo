#!/usr/bin/python
# -*- coding:utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import os


def build_process_flow_html(root, dst_dir):

    os.makedirs(dst_dir, 0o444)
    template_path = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)),
         'template')
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template('process_flow.html')
    print template.render()

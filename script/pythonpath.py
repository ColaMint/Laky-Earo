#!/usr/bin/python
# -*- coding:utf-8 -*-

import os


def find_parent(path, times=1):
    parent = os.path.dirname(path)
    return parent if times <= 1 else find_parent(parent, times-1)

if __name__ == '__main__':
    project_dir = find_parent(os.path.abspath(__file__), 2)
    print 'export PYTHONPATH=$PYTHON_PATH:%s' % (project_dir,)

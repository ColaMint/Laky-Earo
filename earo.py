#!/usr/bin/python
# -*- coding:utf-8 -*-  
from optparse import OptionParser
import os
import sys

def _parse_option () :
    parser = OptionParser()
    parser.add_option('-c', '--create_app', 
                        dest = 'app_name', 
                        help = 'the name of app to be created')
    (options, args) = parser.parse_args()

    if None != options.app_name :
        _create_app(options.app_name)

def _create_app (app_name) :
    app_name = app_name.rstrip('/')
    code = os.system('mkdir %s' % app_name)

    if 0 == code :
        main_src_path = os.path.join(sys.path[0], 'example', 'main_example.py')
        conf_src_path = os.path.join(sys.path[0], 'example', 'conf_example.py')
        main_dest_path = os.path.join(app_name, 'main.py')
        conf_dest_path = os.path.join(app_name, 'conf', 'conf.py')
        conf_path = os.path.join(app_name, 'conf')

        os.system('cp %s %s' % (main_src_path, main_dest_path))
        os.system('mkdir %s' % conf_path)
        os.system('cp %s %s' % (conf_src_path, conf_dest_path))
    

if __name__ == '__main__' :
    _parse_option()

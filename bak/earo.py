#!/usr/bin/python
# -*- coding:utf-8 -*-  
from optparse import OptionParser
import EaroApp
import sys

def __parse_option () :
    parser = OptionParser()
    parser.add_option('-c', '--create_app', 
                        dest = 'app_name', 
                        help = 'the name of app to be created')
    (options, args) = parser.parse_args()

    if None != options.app_name :
        _create_app(options.app_name)

def __create_app (app_name) :
    app_name = app_name.rstrip('/')
    code = os.system('mkdir %s' % app_name)

    if 0 == code :
        main_src_path = os.path.join(Const.CURRENT_PATH, 'example', 'main_example.py')
        conf_src_path = os.path.join(Const.CURRENT_PATH, 'example', 'conf_example.py')
        main_dest_path = os.path.join(app_name, 'main.py')
        conf_dest_path = os.path.join(app_name, 'conf', 'conf.py')
        conf_path = os.path.join(app_name, 'conf')
        handler_path = os.path.join(app_name, 'handler')

        os.system('mkdir %s' % conf_path)
        os.system('mkdir %s' % handler_path)
        os.system('touch %s/__init__.py' % conf_path)
        os.system('touch %s/__init__.py' % handler_path)
        os.system('cp %s %s' % (main_src_path, main_dest_path))
        os.system('cp %s %s' % (conf_src_path, conf_dest_path))

if __name__ == '__main__' :
    __parse_option()

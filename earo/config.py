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

import copy

class Config(object):
    """
    The configration of the earo application.
    """

    __config__ = {
        'app_name': 'earo',
        'source_event_cls': (),
        'processors_tag_regex': [],
        'monitor_host': '0.0.0.0',
        'monitor_port': 9527
    }
    """
    The default configuration.
    """

    def __init__(self, **kwargs):

        for key, value in kwargs.iteritems():
            self.__setattr__(key, value)

    def __getattr__(self, key):

        if key in self.__config__:
            return self.__config__[key]
        else:
            raise KeyError(key)

    def __setattr__(self, key, value):

        if key in self.__config__:
            self.__config__[key] = value
        else:
            raise KeyError(key)

    @property
    def dict(self):
        return copy.deepcopy(self.__config__)

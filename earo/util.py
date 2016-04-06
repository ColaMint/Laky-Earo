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

from datetime import datetime

def datetime_delta_ms(d1, d2):
    """
    Both `d1` and `d2 must be an instance of `datetime.datetime`.
    return the millisecond(s) between `d1` and `d2`.
    """
    if not isinstance (d1, datetime):
        raise TypeError('`d1` must be an instance of `datetime.datetime`.')
    if not isinstance (d2, datetime):
        raise TypeError('`d2` must be an instance of `datetime.datetime`.')

    delta = d1 - d2
    return  delta.days * 24 * 3600 * 1000 + \
            delta.seconds * 1000 + \
            delta.microseconds / 1000;

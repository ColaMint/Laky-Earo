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


class Mediator(object):
    """
    :class:`Mediator` maintains the relationship between :class:`earo.event.Event`'s subclass
    and :class:`earo.handler.Handler`.
    """

    _event_handler_map = None
    """
    A `dict`.
    The `key` is the class of :class:`earo.event.Event`'s subclass.
    The `value` is a `list` of :class:`earo.handler.Handler`.
    """

    def __init__(self):

        self._event_handler_map = {}

    def find_handlers(self, event_cls):
        """
        Find a `list` of :class:`earo.handler.Handler` that register with `event_cls`

        :param event_cls: The class of :class:`earo.event.Event`'s subclass.
        """
        if event_cls in self._event_handler_map:
            return self._event_handler_map[event_cls]
        else:
            return []

    def register_event_handler(self, *handlers):
        """
        Register event handlers.

        :param handlers: one or more :class:`earo.handler.Handler`.
        """
        for handler in handlers:
            if handler.event_cls not in self._event_handler_map:
                self._event_handler_map[handler.event_cls] = []
            self._event_handler_map[handler.event_cls].append(handler)

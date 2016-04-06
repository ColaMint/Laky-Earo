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

import inspect
import traceback
from datetime import datetime
from util import datetime_delta_ms


class NoEmittion(object):
    """
    Returned at :class:`Handler`.func by developer, explains why a event is not emitted.
    """

    event_cls = None
    """
    The class of the event not emitted.
    """

    msg = None
    """
    The reason why the event is not emitted.
    """

    def __init__(self, event_cls, msg):

        self.event_cls = event_cls
        self.msg = msg


class Emittion(object):
    """
    Returned at :class:`Handler`.func by developer, means that an event is emitted.
    """

    event = None
    """
    The emitted event.
    """

    def __init__(self, event):

        self.event = event


class HandlerRuntime(object):
    """
    The execution information of a :class:`Handler`.
    """

    handler = None
    """
    :class:`Handler`.
    """

    event = None
    """
    An instance of :class:`earo.event.Event`'s subclass.
    """

    begin_time = None
    """
    :class:`datetime.datetime`.
    The begining time of the handler's execution.
    """

    end_time = None
    """
    :class:`datetime.datetime`.
    The ending time of the handler's execution.
    """

    exception = None
    """
    The exception raised by :class:`Handler`.func.
    """

    no_emittions = None
    """
    A `dict`.
    The `key` is the class of :class:`earo.event.Event`'s subclass.
    The `value` is :class:`NoEmittion`.
    """

    emittions = None
    """
    A `list`.
    The `elements` are instances of :class:`earo.event.Event`'s subclass.
    """

    def __init__(self, handler, event):

        self.handler = handler
        self.event = event
        self.begin_time = None
        self.end_time = None
        self.exception = None
        self.no_emittions = {}
        self.emittions = []

    @property
    def succeeded(self):
        """
        The handler is executed and no exception is raised.
        """
        return self.begin_time is not None and self.end_time is not None and self.exception is None

    def record_begin_time(self):
        """
        Assign `datetime.now()` to `self.begin_time`.
        """
        self.begin_time = datetime.now()

    def record_end_time(self):
        """
        Assign `datetime.now()` to `self.end_time`.
        """
        self.end_time = datetime.now()

    def record_exception(self, exception):
        """
        Assign `exception` to `self.exception`.

        :param exception: an exception instance.
        """
        self.exception = exception

    def record_emittion(self, emittion):
        """
        Append `emittion.event` to `self.emittions`.

        :param emittion: :class:`Emittion`.
        """
        self.emittions.append(emittion.event)

    def record_no_emittion(self, no_emittion):
        """
        Record `no_emittion` in `self.no_emittions`.

        :param emittion: :class:`NoEmittion`.
        """
        self.no_emittions[no_emittion.event_cls] = no_emittion.msg

    def why_no_emittion(self, event_cls):
        """
        Return the reason why the specific event is not emitted.

        :param event_cls: the class of the event to search.
        """
        return self.no_emittions[event_cls] \
            if event_cls in self.no_emittions else None

    @property
    def time_cost(self):
        """
        The time cost(in milliseconds) of :class:`Handler`.func.
        """
        if self.begin_time is not None and self.end_time is not None:
            return datetime_delta_ms(self.end_time, self.begin_time)
        else:
            return -1


class Handler(object):
    """
    The handler of the event.
    """

    event_cls = None
    """
    The class of :class:`earo.event.Event`'s subclass this handler is interested in.
    """

    func = None
    """
    The handler function of this handler.
    """

    emittion_statement = None
    """
    A `list` of classes of :class:`earo.event.Event`'s subclass that `self.func`
    may emit. If an event is emitted but not in `self.emittion_statement`, `earo`
    will raise an exception. `earo` use `self.emittion_statement` to build
    :class:`earo.processor.ProcessFlow`.
    """

    def __init__(self, event_cls, func, emittion_statement=[]):

        self.event_cls = event_cls
        self.func = func
        self.emittion_statement = emittion_statement
        self._validate_func(func)

    def _validate_func(self, handle_func):
        """
        Validate the `handler_func`'s param list is (context, event).
        """
        argspec = inspect.getargspec(handle_func)
        if argspec.args != ['context', 'event']:
            raise TypeError(
                'Handler\'s function must be function_name(context, event)')

    def handle(self, context, event):
        """
        Hanlde `event` in `context`.

        :param context: :class:`earo.context.Context`.
        :param event: an instance of :class:`earo.event.Event`'s subclass.
        """

        if not isinstance(event, self.event_cls):
            raise TypeError(
                'Handle unexcepted event %s. Except %s.' %
                (type(event), self.event_cls))

        handler_runtime = HandlerRuntime(self, event)
        try:
            handler_runtime.record_begin_time()
            results = self.func(context, event)
            if not hasattr(results, '__iter__'):
                results = (results, )
            for result in results:
                if isinstance(result, NoEmittion):
                    handler_runtime.record_no_emittion(result)
                elif isinstance(result, Emittion):
                    handler_runtime.record_emittion(result)
        except Exception as e:
            e.traceback = traceback.format_exc()
            handler_runtime.record_exception(e)
        finally:
            handler_runtime.record_end_time()
            return handler_runtime

    @property
    def no_emittion_statement(self):
        """
        return True if the handler won't emit any event.
        """
        return len(self.emittion_statement) == 0

    def __eq__(self, obj):
        return isinstance(obj, Handler) \
            and self.event_cls == obj.event_cls \
            and self.func == obj.func \
            and self.emittion_statement == obj.emittion_statement

    def __str__(self):
        return '%s.%s:%s.%s' % (self.event_cls.__module__,
                                self.event_cls.__name__,
                                self.func.__module__,
                                self.func.__name__)

    def __repr__(self):
        return self.__str__()

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

import pickle
from enum import Enum
from util import datetime_delta_ms
import atomic
import re


class NodeType(Enum):
    """
    Enum type of :class:`Node`
    """

    Event = 1
    Handler = 2


class Node(object):
    """
    :class:`Node` holds an `inactive_item` and an `active_item`.
    `inactive_item` should be always not None.
    When `active_item` is None, this :class:`Node` is considered inactive,
    otherwise, it is active.
    :class:`Node` is a node of a tree, so it has `child_nodes`.
    """

    inactive_item = None
    """
    the inactive item.
    """

    active_item = None
    """
    the active item.
    """

    child_nodes = None
    """
    A list of child :class:`None`.
    """

    def __init__(self, inactive_item, child_nodes=None):

        self.inactive_item = inactive_item
        self.active_item = None
        self.child_nodes = [] if child_nodes is None else child_nodes

    @property
    def active(self):
        """
        Whether this node is active or not.
        """
        return self.active_item is not None

    @property
    def type(self):
        """
        One of :class:`NodeType`.
        """
        raise NotImplemented


class EventNode(Node):
    """
    `inactive_item` should be the class of :class:`earo.event.Event`'s subclass.
    `active_item` should be an instance of :class:`earo.event.Event`'s subclass.
    """

    @property
    def type(self):
        """
        Return :class:`NodeType`.Event
        """
        return NodeType.Event


class HandlerNode(Node):
    """
    `inactive_item` should be an instance of :class:`earo.handler.Handler`.
    `active_item` should be an instance of :class:`earo.handler.HandlerRuntime`.
    """

    @property
    def type(self):
        """
        return :class:`NodeType`.Handler
        """
        return NodeType.Handler


class Processor(object):
    """
    :class:`Processor` is responsible for making :class:`ProcessFlow` and the
    statistics of :class:`ProcessFlow`s it processed.
    """

    tag_regex = None
    """
    The regular expression for :class:`earo.event.Event`.__tag__.
    :class:`Processor` only process those events whose tag is match `tag_regex`.
    This feature is implemented by :class:`earo.app.App`.
    """

    _process_count = None
    """
    The number of those :class:`ProcessFlow`s maked by this :class:`Processor`.
    """

    _exception_count = None
    """
    The number of those :class:`ProcessFlow`s maked by this :class:`Processor`
    and have raised exception.
    """

    _event_process_list = None
    """
    A list of event classes that have been processed.
    """

    _event_process_count = None
    """
    A `dict`.
    The `key` is the class of :class:`earo.event.Event`'s subclass.
    The `value` is the number of those :class:`ProcessFlow`
    maked by this :class:`Processor, whose source event is an instance of the `key`.
    """

    _event_exception_count = None
    """
    A `dict`.
    The `key` is the class of :class:`earo.event.Event`'s subclass.
    The `value` is the number of those :class:`ProcessFlow`s
    maked by this :class:`Processor`, whose source event is an instance of the
    `key` and that have raised exception.
    """

    _event_min_time_cost = None
    """
    A `dict`.
    The `key` is the class of :class:`earo.event.Event`'s subclass.
    The `value` is the min time cost(in milliseconds) of those :class:`ProcessFlow`
    maked by this :class:`Processor ab whose source event is an instance of the `key`.
    """

    _event_max_time_cost = None
    """
    A `dict`.
    The `key` is the class of :class:`earo.event.Event`'s subclass.
    The `value` is the min time cost(in milliseconds) of those :class:`ProcessFlow`
    maked by this :class:`Processor, whose source event is an instance of the `key`.
    """

    def __init__(self, tag_regex):

        self.tag_regex = tag_regex
        self._tag_pattern = re.compile(self.tag_regex)
        self._process_count = atomic.AtomicLong(0)
        self._exception_count = atomic.AtomicLong(0)
        self._event_process_list = []
        self._event_process_count = {}
        self._event_exception_count = {}
        self._event_min_time_cost = {}
        self._event_max_time_cost = {}

    def match_event_tag(self, event):
        """
        Determine whether the `event`'s tag match `tag_regex`.
        """
        tag = event.tag()
        return self._tag_pattern.match(tag) is not None \
            if tag is not None \
            else False

    def process(self, context):
        """
        Process the :class:`earo.context.Context`, make a :class:`ProcessFlow` and
        set it at :class:`earo.context.Context`.`process_flow`.

        :param context: a :class:`earo.context.Context`.
        """

        process_flow = ProcessFlow(context.mediator, type(context.source_event))

        def process_node_recursively(node, event):
            if node.type == NodeType.Event:
                node.active_item = event
                for handler_node in node.child_nodes:
                    process_node_recursively(handler_node, event)
            elif node.type == NodeType.Handler:
                handler = node.inactive_item
                handler_runtime = handler.handle(context, event)

                if process_flow.begin_time is None:
                    process_flow.begin_time = handler_runtime.begin_time
                if handler_runtime.exception is not None:
                    process_flow.exception_count += 1
                process_flow.end_time = handler_runtime.end_time

                node.active_item = handler_runtime
                for emitted_event in handler_runtime.emittions:
                    event_cls = type(emitted_event)
                    found = False
                    for event_node in node.child_nodes:
                        if event_node.inactive_item == event_cls:
                            process_node_recursively(
                                event_node, emitted_event)
                            found = True
                            break
                    if not found:
                        raise TypeError(
                            'Unexcepted event `%s` emitted by handler `%s`.' %
                            (event_cls, handler))
            else:
                raise TypeError('Unknown NodeType: `%s`.' % (node.type,))

        process_node_recursively(process_flow.root, context.source_event)

        source_event_cls = type(context.source_event)
        self._process_count += 1
        if source_event_cls not in self._event_process_count:
            self._event_process_count[source_event_cls] = atomic.AtomicLong(0)
        if source_event_cls not in self._event_process_list:
            self._event_process_list.append(source_event_cls)
        self._event_process_count[source_event_cls] += 1
        if source_event_cls not in self._event_exception_count:
            self._event_exception_count[source_event_cls] = atomic.AtomicLong(0)
        if process_flow.exception_count > 0:
            self._exception_count += 1
            self._event_exception_count[source_event_cls] += 1
        if process_flow.time_cost >= 0:
            if source_event_cls not in self._event_min_time_cost \
                    or process_flow.time_cost < self._event_min_time_cost[source_event_cls]:
                self._event_min_time_cost[
                    source_event_cls] = process_flow.time_cost
            if source_event_cls not in self._event_max_time_cost \
                    or process_flow.time_cost > self._event_max_time_cost[source_event_cls]:
                self._event_max_time_cost[
                    source_event_cls] = process_flow.time_cost

        process_flow.after_process()
        return process_flow

    @property
    def process_count(self):
        """
        The number of those :class:`ProcessFlow`s maked by this :class:`Processor`.
        """
        return self._process_count.value

    @property
    def exception_count(self):
        """
        The number of those :class:`ProcessFlow`s maked by this :class:`Processor`
        and have raised exception.
        """
        return self._exception_count.value

    def event_process_list(self):
        """
        Return a list of source event classes that have been processed.
        """
        return self._event_process_list

    def event_process_count(self, source_event_cls):
        """
        The number of those :class:`ProcessFlow` maked by this :class:`Processor,
        whose source event is an instance of the `source_event_cls`.
        """
        return self._event_process_count[source_event_cls].value \
            if source_event_cls in self._event_process_count \
            else 0

    def event_exception_count(self, source_event_cls):
        """
        The number of those :class:`ProcessFlow` maked by this :class:`Processor,
        whose source event is an instance of the `source_event_cls` and that have
        raised exception.
        """
        return self._event_exception_count[source_event_cls].value \
            if source_event_cls in self._event_exception_count \
            else 0

    def event_min_time_cost(self, source_event_cls):
        """
        The min time cost(in milliseconds)  of those :class:`ProcessFlow` maked
        by this :class:`Processor, whose source event is an instance of the
        `source_event_cls`.
        """
        return self._event_min_time_cost[source_event_cls] \
            if source_event_cls in self._event_min_time_cost \
            else -1

    def event_max_time_cost(self, source_event_cls):
        """
        The max time cost(in milliseconds)  of those :class:`ProcessFlow` maked
        by this :class:`Processor, whose source event is an instance of the
        `source_event_cls`.
        """
        return self._event_max_time_cost[source_event_cls] \
            if source_event_cls in self._event_max_time_cost\
            else -1


class ProcessFlow(object):

    root = None
    """
    The root :class:`EventNode`.
    """

    begin_time = None
    """
    An instance of :class:`~datetime.datetime`.
    The time when the process begins.
    """

    end_time = None
    """
    An instance of :class:`~datetime.datetime`.
    The time when the process ends.
    """

    _time_cost = -1
    """
    The time cost(in milliseconds) between self.`begin_time` and self.`end_time`.
    """

    exception_count = 0
    """
    The number of exceptions raised during process.
    """

    _emittions = None
    """
    A `dict` records events emitted during process.
    The `key` is the class of :class:`earo.event.Event`'s subclass.
    The value is an instance of :class:`earo.event.Event`.
    """

    _no_emittions = None
    """
    A `dict` records events which may be emitted but not emitted during process.
    The `key` is the class of :class:`earo.event.Event`'s subclass.
    The value is a `str` that indicates why the event was not emitted.
    """

    def __init__(self, mediator, source_event_cls):

        self._emittions = {}
        self._no_emittions = {}
        self._build_nodes(mediator, source_event_cls)

    def _build_nodes(self, mediator, source_event_cls):
        """
        Build nodes and set self.`root`.
        """
        def build_node_recursively(inactive_item, node_type):
            if node_type == NodeType.Event:
                event_cls = inactive_item
                child_nodes = []
                for handler in mediator.find_handlers(event_cls):
                    handler_node = build_node_recursively(
                        handler, NodeType.Handler)
                    child_nodes.append(handler_node)
                return EventNode(inactive_item, child_nodes)
            elif node_type == NodeType.Handler:
                handler = inactive_item
                child_nodes = []
                for event_cls in handler.emittion_statement:
                    event_node = build_node_recursively(
                        event_cls, NodeType.Event)
                    child_nodes.append(event_node)
                return HandlerNode(inactive_item, child_nodes)
            else:
                raise TypeError('Unknown NodeType: `%s`.' % (node_type,))

        self.root = build_node_recursively(source_event_cls, NodeType.Event)

    def after_process(self):
        """
        Called by :class:`Processor` after process.
        """
        self._build_emittion_index()

    def _build_emittion_index(self):
        """
        Build self.`_emittions` and self.`_no_emittions`.
        """

        def build_emittion_index_recursively(node):
            if node.type == NodeType.Event:
                event = node.active_item
                event_cls = type(event)
                self._emittions[event_cls] = event
                for handler_node in node.child_nodes:
                    build_emittion_index_recursively(handler_node)
            elif node.type == NodeType.Handler:
                if node.active:
                    handler_runtime = node.active_item
                    for event_cls, msg in handler_runtime.no_emittions.iteritems():
                        self._no_emittions[event_cls] = msg
                    for event_node in node.child_nodes:
                        build_emittion_index_recursively(event_node)
            else:
                raise TypeError('Unknown NodeType: `%s`.' % (node.type,))

        build_emittion_index_recursively(self.root)

    @property
    def active(self):
        """
        Whether this :class:`ProcessFlow` is active or not.
        When the root :class:`Node` of this :class:`ProcessFlow` is active, it
        is considered active, otherwise it is inactive.
        """
        return self.root.active

    @property
    def time_cost(self):
        """
        The time cost(in milliseconds) between self.`begin_time` and self.`end_time`.
        """
        if self._time_cost < 0 \
                and self.begin_time is not None \
                and self.end_time is not None:
            self._time_cost = datetime_delta_ms(self.end_time, self.begin_time)
        return self._time_cost

    def find_event(self, event_cls):
        """
        Find the event in self.`_emittions`.
        If the event was not emitted, return None.

        :param event_cls: The class of the event to find.
        """
        return self._emittions[event_cls] \
            if event_cls in self._emittions else None

    def why_no_emittion(self, event_cls):
        """
        return a `str` thiat indicates why the event was not emitted.
        If no reason given, return None.

        :param event_cls: The class of the event to find.
        """
        return self._no_emittions[event_cls] \
            if event_cls in self._no_emittions else None

    def serialize(self):
        """
        Use `pickle` to serialize :class:`ProcessFlow`.
        """
        return pickle.dumps(self)

    @staticmethod
    def unserialize(string):
        """
        Use `pickle` to unserialize :class:`ProcessFlow` from `string`.
        If it fails, return None.

        :param string: The string after serialization.
        """
        try:
            process_flow = pickle.loads(strint)
            if not isinstance(process_flow, ProcessFlow):
                return None
        except Exception:
            return None

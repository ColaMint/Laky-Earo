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
    Event = 1
    Handler = 2


class Node(object):
    """
    Each Node holds an `inactive_item` and an `active_item`.
    `inactive_item` should always not be None.
    When `active_item` is None, this None is considered inactive,
    otherwise, it is active.
    Node is a node of a tree, so it has `child_nodes`.
    """

    def __init__(self, inactive_item, child_nodes=[]):
        self.inactive_item = inactive_item
        self.active_item = None
        self.child_nodes = child_nodes

    @property
    def active(self):
        """
        Whether this node is active or not.
        """
        return self.active_item is not None

    @property
    def type(self):
        """
        This function should be implemented in subclass.
        return one value of :class:`NodeType`.
        """
        raise NotImplemented


class EventNode(Node):
    """
    Subclass of :class:`Node`.
    `inactive_item` should be the class of a :class:`earo.event.Event`'s subclass.
    `active_item` should be the instance of a :class:`earo.event.Event`'s subclass.
    """

    @property
    def type(self):
        return NodeType.Event


class HandlerNode(Node):
    """
    Subclass of :class:`Node`.
    `inactive_item` should be the instance of :class:`earo.handler.Handler`.
    `active_item` should be the instance of :class:`earo.handler.HandlerRuntime`.
    """

    @property
    def type(self):
        return NodeType.Handler


class Processor(object):

    def __init__(self, tag_regex):
        self.tag_regex = tag_regex
        self._tag_pattern = re.compile(self.tag_regex)
        self._process_count = atomic.AtomicLong(0)
        self._exception_count = atomic.AtomicLong(0)
        self._event_process_count = {}
        self._event_exception_count = {}
        self._event_min_time_cost = {}
        self._event_max_time_cost= {}

    def match_event_tag(self, event):
        return self._tag_pattern.match(event.tag) is not None \
                if event.tag is not None \
                else False

    def process(self, context):

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
        self._event_process_count[source_event_cls] += 1
        if source_event_cls not in self._event_exception_count:
            self._event_exception_count[source_event_cls] = atomic.AtomicLong(0)
        if process_flow.exception_count > 0:
            self._exception_count += 1
            self._event_exception_count[source_event_cls] += 1
        if process_flow.time_cost >= 0:
            if source_event_cls not in self._event_min_time_cost \
                    or process_flow.time_cost < self._event_min_time_cost[source_event_cls]:
                self._event_min_time_cost[source_event_cls] = process_flow.time_cost
            if source_event_cls not in self._event_max_time_cost \
                    or process_flow.time_cost > self._event_max_time_cost[source_event_cls]:
                self._event_max_time_cost[source_event_cls] = process_flow.time_cost

        process_flow.after_process()
        return process_flow

    @property
    def process_count(self):
        return self._process_count.value

    @property
    def exception_count(self):
        return self._exception_count.value

    def event_process_count(self, source_event_cls):
        return self._event_process_count[source_event_cls].value \
            if source_event_cls in self._event_process_count \
            else 0

    def event_exception_count(self, source_event_cls):
        return self._event_exception_count[source_event_cls].value \
            if source_event_cls in self._event_exception_count \
            else 0

    def event_min_time_cost(self, source_event_cls):
        return self._event_min_time_cost[source_event_cls] \
            if source_event_cls in self._event_min_time_cost \
            else -1

    def event_max_time_cost(self, source_event_cls):
        return self._event_max_time_cost[source_event_cls] \
            if source_event_cls in self._event_max_time_cost\
            else -1

class ProcessFlow(object):

    def __init__(self, mediator, source_event_cls):
        self.begin_time = None
        self.end_time = None
        self.exception_count = 0
        self._time_cost = -1
        self._build_nodes(mediator, source_event_cls)

    def _build_nodes(self, mediator, source_event_cls):

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
        self._build_emittion_index()

    def _build_emittion_index(self):

        self.__emittions = {}
        self.__no_emittions = {}

        def build_emittion_index_recursively(node):
            if node.type == NodeType.Event:
                event = node.active_item
                event_cls = type(event)
                self.__emittions[event_cls] = event
                for handler_node in node.child_nodes:
                    build_emittion_index_recursively(handler_node)
            elif node.type == NodeType.Handler:
                if node.active:
                    handler_runtime = node.active_item
                    for event_cls, msg in handler_runtime.no_emittions.iteritems():
                        self.__no_emittions[event_cls] = msg
                    for event_node in node.child_nodes:
                        build_emittion_index_recursively(event_node)
            else:
                raise TypeError('Unknown NodeType: `%s`.' % (node.type,))

        build_emittion_index_recursively(self.root)

    @property
    def active(self):
        return self.root.active

    @property
    def time_cost(self):
        if self._time_cost < 0 \
            and self.begin_time is not None \
            and self.end_time is not None:
            self._time_cost = datetime_delta_ms(self.end_time, self.begin_time)
        return self._time_cost

    def find_event(self, event_cls):
        return self.__emittions[event_cls] \
            if event_cls in self.__emittions else None

    def why_no_emittion(self, event_cls):
        return self.__no_emittions[event_cls] \
            if event_cls in self.__no_emittions else None

    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def unserialize(str):
        try:
            process_flow = pickle.loads(str)
            if not isinstance(process_flow, ProcessFlow):
                return None
        except Exception:
            return None

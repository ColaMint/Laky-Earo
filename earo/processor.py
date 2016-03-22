#!/usr/bin/python
# -*- coding:utf-8 -*-

import pickle
from handler import HandlerRuntime
from event import Event
from Queue import Queue
from enum import Enum


class NodeType(Enum):
    Event = 1
    Handler = 2


class Node(object):

    def __init__(self, inactive_item, child_nodes=[]):
        self.inactive_item = inactive_item
        self.active_item = None
        self.child_nodes = child_nodes

    @property
    def active(self):
        return self.active_item is not None

    @property
    def type(self):
        raise NotImplemented


class EventNode(Node):

    @property
    def type(self):
        return NodeType.Event


class HandlerNode(Node):

    @property
    def type(self):
        return NodeType.Handler


class Processor(object):

    def __init__(self):
        pass

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
        process_flow.build_emittion_index()
        return process_flow


class ProcessFlow(object):

    def __init__(self, mediator, source_event_cls):

        self.__build_node(mediator, source_event_cls)

    def __build_node(self, mediator, source_event_cls):

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
                for event_cls in handler.emit_events:
                    event_node = build_node_recursively(
                        event_cls, NodeType.Event)
                    child_nodes.append(event_node)
                return HandlerNode(inactive_item, child_nodes)
            else:
                raise TypeError('Unknown NodeType: `%s`.' % (node_type,))

        self.root = build_node_recursively(source_event_cls, NodeType.Event)

    def build_emittion_index(self):

        self.__emittions = {}
        self.__no_emittions = {}

        def build_emittion_index_recursively(node):
            if not node.active:
                return
            if node.type == NodeType.Event:
                event = node.active_item
                event_cls = type(event)
                self.__emittions[event_cls] = event
                for handler_node in node.child_nodes:
                    build_emittion_index_recursively(handler_node)
            elif node.type == NodeType.Handler:
                handler_runtime = node.active_item
                for event_cls, msg in handler_runtime.no_emittions.iteritems():
                    self.__no_emittions[event_cls] = msg
                for event_node in node.child_nodes:
                    build_emittion_index_recursively(event_node)
            else:
                raise TypeError('Unknown NodeType: `%s`.' % (node.type,))

        build_emittion_index_recursively(self.root)

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

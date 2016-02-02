#!/usr/bin/python
# -*- coding:utf-8 -*-
from handler_runtime import HandlerRuntime
from event import Event
import cPickle as pickle
from uuid import uuid1
from util.kv_database import KVDatabase


class RuntimeNode(object):

    def __init__(self, item):
        self.item = item
        self.child_nodes = list()
        if isinstance(self.item, Event):
            self.type = Event
        elif isinstance(self.item, HandlerRuntime):
            self.type = HandlerRuntime
        else:
            raise TypeError(
                'item should be instance of %s or %s, not %s' %
                (Event, HandlerRuntime, type(item)))

    def add_child_node(self, node):
        self.child_nodes.append(node)

    @property
    def dict(self):
        node = dict()
        node['item'] = self.item.dict
        node['type'] = type(self.item).__name__
        node['child_nodes'] = list()
        for child_node in self.child_nodes:
            node['child_nodes'].append(child_node.dict)
        return node


class RuntimeTree(object):

    def __init__(self, root):
        self.root = root
        self.id = uuid1()
        self.begin_time = None
        self.end_time = None
        self.time_cost = None
        self.event_count = -1
        self.handler_runtime_count = -1
        self.exception_count = -1

    def statistics(self):
        self.event_count = 0
        self.handler_runtime_count = 0
        self.exception_count = 0
        self._statistics(self.root)
        if self.end_time is not None and self.begin_time is not None:
            self.time_cost = (self.end_time - self.begin_time).microseconds
        else:
            self.time_cost = -1

    def _statistics(self, node):
        if node.type == Event:
            self.event_count += 1
        elif node.type == HandlerRuntime:
            handelr_runtime = node.item
            self.handler_runtime_count += 1
            if handelr_runtime.exception is not None:
                self.exception_count += 1
            if self.begin_time is None or (
                    handelr_runtime.begin_time is not None and handelr_runtime.begin_time < self.begin_time):
                self.begin_time = handelr_runtime.begin_time
            if self.end_time is None or (
                    handelr_runtime.end_time is not None and handelr_runtime.end_time < self.end_time):
                self.end_time = handelr_runtime.end_time
        for child_node in node.child_nodes:
            self.__statistics(child_node)

    @property
    def dict(self):
        tree = dict()
        tree['id'] = self.id
        tree['root'] = self._parse_node(self.root)
        tree['begin_time'] = self.begin_time
        tree['end_time'] = self.end_time
        tree['time_cost'] = self.time_cost
        tree['event_count'] = self.event_count
        tree['handler_runtime_count'] = self.handler_runtime_count
        tree['exception_count'] = self.exception_count
        return tree

    def _parse_node(node):
        if node.type == Event:
            event = node.item
            event_dict = dict()
            event_dict['event_name'] = event.name()
            event_dict['params'] = event.params()
            event_dict['child_nodes'] = [
                self._parse_node(n) for x in node.child_nodes]
            return event_dict
        else:
            handler_runtime = node.item
            handler_runtime_dict = dict()
            handler_runtime_dict['begin_time'] = handler_runtime.begin_time
            handler_runtime_dict['end_time'] = handler_runtime.end_time
            handler_runtime_dict['time_cost'] = handler_runtime.time_cost
            handler_runtime_dict['exception'] = {
                'traceback': handler_runtime.exception.traceback,
                'message': handler_runtime.exception.message} if handler_runtime.exception is not None else None
            handler_runtime_dict['handler'] = handler_runtime.handler.name
            handler_runtime_dict['child_nodes'] = [
                self._parse_node(n) for x in node.child_nodes]
            return handler_runtime_dict

    @staticmethod
    def loads(d):
        return pickle.loads(str(d))

    def dumps(self):
        return pickle.dumps(self.dict)


class RuntimeTreeStorage(object):

    def __init__(self, db_path):
        self.__db = KVDatabase(db_path)

    def save(self, runtime_tree):
        self.__db.set(runtime_tree.id, runtime_tree.dumps())

    def find(self, id):
        d = self.__db.get(id)
        return RuntimeTree.loads(d) if d is not None else None

    def remove(self, id):
        self.__db.unset(id)

    def remove_all(self):
        self.__db.clear()

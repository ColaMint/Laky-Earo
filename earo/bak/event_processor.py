#!/usr/bin/python
# -*- coding:utf-8 -*-
from threading import Thread
from event_channel import EventChannel
from runtime_tree import RuntimeNode, RuntimeTree
from handler_runtime import HandlerRuntime
from util.local import Local
import Queue


class EventProcessor(Thread):

    def __init__(self, id, app, event_channel=None):
        super(EventProcessor, self).__init__()
        self.id = id
        self._app = app
        self._event_channel = event_channel
        self._running = True
        self._init_local_and_global()

    def __init_local_and_global(self):
        local_defaults = {
            'handler_runtime_node_queue': Queue.Queue,
            'runtime_tree': None,
            'last_handler_runtime_node': None
        }
        self._local = Local(**local_defaults)

    def run(self):
        self._app.logger.info('EventProcessor(%d) start working.' % (self.id,))
        event = None
        while self._running:
            try:
                event = self._event_channel.get(True, 5)
            except Queue.Empty:
                pass
            if event is not None:
                self.process_event(event)
        self._app.logger.info('EventProcessor(%d) stop working.' % (self.id,))

    def process_event(self, event):
        event_node = Node(event)
        self._local.runtime_tree = RuntimeTree(event_node)
        self._local.last_handler_runtime_node = None
        self._put_handler_runtime_to_queue_and_add_child_node(event_node)
        while self._local.handler_runtime_node_queue.qsize() > 0:
            handler_runtime_node = self._local.handler_runtime_node_queue.get()
            self._local.last_handler_runtime_node = handler_runtime_node
            handler_runtime = handler_runtime_node.item
            handler_runtime.run(self)
            if handler_runtime.exception is not None:
                self._app.logger.error(
                    'runtime_tree.id: %s\n%s' %
                    (self._local.runtime_tree.id,
                        handler_runtime.exception.traceback))
        self._local.runtime_tree.statistics()
        if not self._app.config.debug and self._local.runtime_tree.exception_count > 0:
            self._app.runtime_tree_storage.save(self._local.runtime_tree)
        return self._local.runtime_tree

    def _put_handler_runtime_to_queue_and_add_child_node(self, event_node):
        for handler in self._app.find_handlers(event_node.item.event_name):
            handler_runtime = HandlerRuntime(handler, event_node.item)
            handler_runtime_node = Node(handler_runtime)
            event_node.add_child_node(handler_runtime_node)
            self._local.handler_runtime_node_queue.put(handler_runtime_node)

    def fire(self, event):
        handler = self._local.last_handler_runtime_node.item.handler
        throw_events = handler.throw_events
        if event.event_name not in throw_events:
            raise UnExceptedEventFiredException(event, throw_events)
        event_node = Node(event)
        self._put_handler_runtime_to_queue_and_add_child_node(event_node)
        self._local.last_handler_runtime_node.add_child_node(event_node)

    def stop(self):
        self._running = False


class UnExceptedEventFiredException(Exception):

    def __init__(self, event, throw_events):
        self.event = event
        self.throw_events = throw_events
        super(
            UnExceptedEventFiredException, self).__init__(
            'Unexcepted event `%s` fired. Allowed events is %s.' %
         (event.event_name, throw_events))

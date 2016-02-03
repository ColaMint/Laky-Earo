# -*- coding:utf-8 -*-
import pickle
from event import Event
from handler import HandlerRuntime
from Queue import Queue


class ProcessFlowNode(object):

    def __init__(self, item):
        self.item = item
        self.child_nodes = list()
        if isinstance(self.item, (Event, HandlerRuntime)):
            self.type = type(item)
        else:
            raise TypeError(
                'ProcessFlowNode\'s item should be instance of %s or %s, not %s' %
                (Event, HandlerRuntime, type(item)))

    def append_child_node(self, node):
        self.child_nodes.append(node)


class ProcessFlow(object):

    def __init__(self, root):
        self.root = root

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


class Processor(object):

    def __init__(self, context):

        self.context = context
        self._event_node_queue = Queue()
        self._handler_runtime_node_queue = Queue()
        self.current_handler = None

    def process(self, event):

        root = ProcessFlowNode(event)
        self._event_node_queue.put(root)

        while not self._event_node_queue.empty():
            event_node = self._event_node_queue.get()
            event = event_node.item
            if not self._handler_runtime_node_queue.empty():
                handler_runtime_node = self._handler_runtime_node_queue.get()
                handler_runtime_node.append_child_node(event_node)

            handlers = self.context.mediator.find_handlers(type(event))
            for handler in handlers:
                self.current_handler = handler
                handler_runtime = handler.handle(self.context, event)
                handler_runtime_node = ProcessFlowNode(handler_runtime)
                event_node.append_child_node(handler_runtime_node)
                while self._handler_runtime_node_queue.qsize() < self._event_node_queue.qsize():
                    self._handler_runtime_node_queue.put(handler_runtime_node)

        return ProcessFlow(root)

    def emit(self, event):
        event_cls = type(event)
        if event_cls in self.current_handler.emit_events:
            self._event_node_queue.put(ProcessFlowNode(event))
        else:
            raise TypeError('Unexcepted event `%s` emitted by handler `%s`.' %
                            (event_cls, handler.name))

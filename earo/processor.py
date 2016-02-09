# -*- coding:utf-8 -*-
import pickle
from handler import HandlerRuntime
from Queue import Queue


class ProcessFlowNode(object):

    def __init__(self, item):
        self.item = item
        self.child_nodes = list()
        self.type = type(item)

    def append_child_node(self, node):
        self.child_nodes.append(node)


class ProcessFlow(object):

    def __init__(self, root):
        self.root = root
        self._build_event_index()

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

    def _build_event_index(self):
        self._event_emittion_index = {}
        self._event_no_emittion_index = {}
        self._event_emittion_index[self.root.type] = [self.root.item]
        self._build_event_index_help(self.root)

    def _build_event_index_help(self, node):
        if node.type == HandlerRuntime:
            handler_runtime = node.item
            for event in handler_runtime.emittion:
                event_cls = type(event)
                if event_cls not in self._event_emittion_index:
                    self._event_emittion_index[event_cls] = []
                self._event_emittion_index[event_cls].append(event)
            for event_cls, msg in handler_runtime.no_emittion.iteritems():
                if event_cls not in self._event_no_emittion_index:
                    self._event_no_emittion_index[event_cls] = []
                self._event_no_emittion_index[event_cls].append(msg)

        for child_node in node.child_nodes:
            self._build_event_index_help(child_node)

    def find_event(self, event_cls, return_first=True):
        if event_cls in self._event_emittion_index:
            return (self._event_emittion_index[event_cls][0], None) \
                if return_first \
                else (self._event_emittion_index[event_cls], None)
        else:
            return (None, self._event_no_emittion_index[event_cls][0]) \
                if return_first \
                else (None, self._event_no_emittion_index[event_cls])


class Processor(object):

    def __init__(self, context):

        self.context = context
        self._event_node_queue = Queue()
        self._handler_runtime_node_queue = Queue()

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
                handler_runtime = handler.handle(self.context, event)
                handler_runtime_node = ProcessFlowNode(handler_runtime)
                event_node.append_child_node(handler_runtime_node)
                for emitted_event in handler_runtime.emittion:
                    event_cls = type(emitted_event)
                    if event_cls in handler.emit_events:
                        self._event_node_queue.put(ProcessFlowNode(emitted_event))
                        self._handler_runtime_node_queue.put(handler_runtime_node)
                    else:
                        raise TypeError('Unexcepted event `%s` emitted by handler `%s`.' %
                                        (event_cls, handler))

        return ProcessFlow(root)

class ProcessFlowPreview(object):

    def __init__(self, mediator, source_event_cls):

        self.mediator = mediator
        self._build_process_flow_preview(source_event_cls)

    def _build_process_flow_preview(self, source_event_cls):

        source_event = source_event_cls()
        event_node = ProcessFlowNode(source_event)
        self.root = event_node

        def _build_process_flow_pre_view_help(event_node):
            handlers = self.mediator.find_handlers(event_node.type)
            for handler in handlers:
                handler_node = ProcessFlowNode(handler)
                event_node.append_child_node(handler_node)
                for event_cls in handler.emit_events:
                    new_event = event_cls()
                    new_event_node = ProcessFlowNode(new_event)
                    handler_node.append_child_node(new_event_node)
                    _build_process_flow_pre_view_help(new_event_node)

        _build_process_flow_pre_view_help(self.root)



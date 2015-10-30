# -*- coding:utf-8 -*-  
from call_tree import CallTree
from event_handler import EventHandler

class EventManager(object):

    def __init__(self, conf):
        self.__event_handlers_dict = dict()
        self.__call_tree_dict = dict()
        
    def __gen_event_handler_key(self, event_namespace, event_name):
        return '%s@#@%s' % (event_namespace, event_name)

    def register_event_hanlder(self, event_namespace, event_name, event_handler_func):
        handler_key = self.__gen_event_handler_key(event_namespace, event_name)
        event_handler = EventHandler(self, event_namespace, event_name, event_handler_func) 
        if not handler_key in self.__event_handlers_dict:
            self.__event_handlers_dict[handler_key] = list()
        self.__event_handlers_dict[handler_key].append(event_handler)

    def unregister_event_handler(self, event_namespace, event_name, event_handler_func):
        pass

    def get_event_handlers(self, in_event):
        handler_key = self.__gen_event_handler_key(in_event.event_namespace, in_event.event_name)
        return self.__event_handlers_dict.get(handler_key, list())

    def emit_event(self, in_event):
        event_handlers = self.get_event_handlers(in_event)
        for event_handler in event_handlers:
            call_tree = self.__get_call_tree(in_event.source_id)
            event_handler_runtime = event_handler.execute(in_event)
            call_tree.addNode(event_handler_runtime)
            out_event = event_handler_runtime.getOutEvent()
            if None != out_event:
                self.emit_event(out_event)
    
    def __get_call_tree(self, source_id):
        if not source_id in self.__call_tree_dict:
            self.__call_tree_dict[source_id] = CallTree(event) 
        return self.__call_tree_dict[source_id]

    def __remove_call_tree(self, source_id):
        if source_id in self.__call_tree_dict:
            del self.__call_tree_dict[source_id]
        

class HandlerExistedException(Exception):

    def __init__(self, event_namespace, event_name):
        self.event_namespace = event_namespace
        self.name = event_name 

    def __str__(self):
        return 'handler existed (event_namespace: %s, event_name: %s)' % (self.event_namespace, self.event_name)

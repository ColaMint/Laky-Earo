# -*- coding:utf-8 -*-  
from call_tree import CallTree
from event_handler import EventHandler

class EventManager(object):
    """
    self.__event_handlers_dict_dict[event_key][event_handler_key] => event_handler
    """

    def __init__(self, conf):
        self.__event_handlers_dict_dict = dict()
        self.__call_tree_dict = dict()
        
    def register_event_hanlder(self, event_handler):
        event_key = event_handler.get_event_key() 
        if self.__event_handlers_dict_dict.has_key(event_key):
            self.__event_handlers_dict_dict[handler_key] = dict() 
        event_handlers_dict = self.__event_handlers_dict[handler_key]
        event_handler_key = event_handler.get_event_handler_key()
        event_handlers_dict[event_handler_key] = event_handler

    def unregister_event_handler(self, event_handler):
        if self.__event_handlers_dict_dict.has_key(handler_key):
            event_handlers_dict = self.__event_handlers_dict[handler_key]
            event_handler_key = event_handler.get_event_handler_key()
            if event_handlers_dict.has_key(event_handler_key):
                del event_handlers_dict[event_handler_key]

    def get_event_handlers(self, in_event):
        event_key = event_handler.get_event_key() 
        if self.__event_handlers_dict_dict.has_key(event_key):
            event_handlers = dict()
            for k in self.__event_handlers_dict_dict[event_key]:
                event_handlers.append(self.__event_handlers_dict_dict[event_key][k])
            return tuple(event_handlers)
        else:
            return tuple()

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

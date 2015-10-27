# -*- coding:utf-8 -*-  

class EventManager(object):

    def __init__(self, conf):
        self._event_handlers = dict()
        
    def _gen_event_handler_key(self, event_namespace, event_name):
        return '%s@#@%s' % (event_namespace, event_name)

    def register_event_hanlder(self, event_namespace, event_name, event_handler_func):
        handler_key = self._gen_event_handler_key(event_namespace, event_name)
        if handler_key in self._event_handlers:
            raise HandlerExistedException(event_namespace, event_name)
        else:
            self._event_handlers[handler_key] = event_handler_func 

    def unregister_event_handler(self, event_namespace, event_name, event_handler_func):
        pass

    def emit_event(self, event):
        pass

class HandlerExistedException(Exception):

    def __init__(self, event_namespace, event_name):
        self.event_namespace = event_namespace
        self.name = event_name 

    def __str__(self):
        return 'handler existed (event_namespace: %s, event_name: %s)' % (self.event_namespace, self.event_name)

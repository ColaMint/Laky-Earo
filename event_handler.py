# -*- coding:utf-8 -*-  
import time
import inspect
from event import Event
from event_handler import EventHandler

class EventHandler(object):
    
    def __init__(self, event_namespace, event_name, event_handler_func):
        self.event_namespace = event_namespace
        self.event_name = event_name
        self.event_handler_func = event_handler_func 

    def execute(self, event):
        event_handler_runtime = EventHandlerRuntime(event = event)
        try:
           event_handler_runtime.handler_params = self.__build_func_params(self.event_handler_func, event.getParams())
           event_handler_runtime.begin_time = time.time() 
           event_handler_runtime.result_event = self.event_handler_func(*event_handler_runtime.handler_params)
           event_handler_runtime.end_time = time.time() 
        except Exception as e:
            event_handler_runtime.exception = e
        finally:
            return event_handler_runtime

    def __build_func_params(fn, params):
        arg_spec = inspect.getargspec(fn)
        module_name = fn.__module__ 
        func_name = fn.__name__

        if None != arg_spec.args:
            raise Exception('func(%s.%s):should not contains args parameter' % (module_name, func_name))
        elif None != arg_spec.keywords:
            raise Exception('func(%s.%s):should not contains keywords parameter' % (module_name, func_name))
        else:
            meet_default = False
            final_params = list()
            for param_name in arg_spec.varargs:
                if None != params and param_name in params:
                    if meet_default:
                        raise Exception('func(%s.%s):a var with default value should not be assigned after a not assigned var with default value(params:%s)', (module_name, func_name, params))
                    else:
                        final_params.append(params[param_name])
                else:
                    if not meet_default:
                        if None == arg_spec.defaults or len(arg_spec.varargs) - len(final_params) != len(arg_spec.defaults):
                            raise Exception('missing assignment for parameter `%s`' % param_name)
                        else:
                            meet_default = True
                            final_params.append(arg_spec.defaults)
            return tuple(final_params)

class EventHandlerRuntime(object):

    def __init__(self, event, handler_params = None, result_event = None, begin_time = None, end_time = None, exception = None):
        self.event = event
        self.handler_params = handler_params 
        self.result_event = result_event 
        self.begin_time = begin_time 
        self.end_time = end_time 
        self.exception = exception 

    def getEventId(self):
        if None == self.event:
            return None
        else:
            return event.event_id

def event_handler(events):
    def decorator(func):
        def wrapper(*args, **kw):
            warpper.event_handlers = dict()
            for event in events:
                event_handler = EventHandler(event.event_namespace, event_name, wrapper)
                warpper.event_handlers.append(event_handler)
            return func(*args, **argkw)
        return wrapper
    return decorator

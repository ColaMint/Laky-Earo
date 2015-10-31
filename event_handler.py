# -*- coding:utf-8 -*-  
import time
import inspect
from event import Event, EventBuilder, getCurrentEvent, setCurrentEvent, getEventKey
from event_handler import EventHandler
import threading

class EventHandler(object):
    
    def __init__(self, event_manager, event_namespace, event_name, event_handler_func):
        self.event_manager = event_manager
        self.event_namespace = event_namespace
        self.event_name = event_name
        self.event_handler_func = event_handler_func 

    def execute(self, event):
        event_handler_runtime = EventHandlerRuntime(in_event = event)
        try:
            setCurrentEvent(event)
            event_handler_runtime.set_handler_params(
                self.__build_func_params(
                    self.event_handler_func, 
                    event.getParams()
                )
            )
            event_handler_runtime.mark_begin_time()
            event_handler_runtime.set_out_event(
                self.event_handler_func(
                    *event_handler_runtime.handler_params
                )
            )
            event_handler_runtime.mark_end_time() 
        except Exception as e:
            event_handler_runtime.set_exception(e)
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
    def get_event_key(self):
        if not self.hasattr('__event_key'):
            self.__event_key = genEventKey(self.event_namespace, self.event_name)
        return self.__event_key

    def get_event_handler_key(self):
        if not self.hasattr('__event_key'):
            self.__event_handler_key = '%s#@#%s#@#%s#@#%s' % (
                    self.event_namespace, self.event_name, 
                    self.event_handler_func.__module__, 
                    self.event_handler_func.__name__
                )
        return self.__event_handler_key

class EventHandlerRuntime(object):

    def __init__(self, handler_params = None, in_event = None, out_event = None, begin_time = None, end_time = None, exception = None):
        self.__handler_params = handler_params 
        self.__in_event = in_event
        self.__out_event = out_event 
        self.__begin_time = begin_time 
        self.__end_time = end_time 
        self.__exception = exception 

    def get_handler_params(self):
        return self.__handler_params

    def set_handler_params(self, handler_params):
        self.__handler_params = handler_params

    def get_in_event(self):
        return self.__in_event

    def set_in_event(self, in_event):
        self.__in_event = in_event

    def get_in_event_id(self):
        if None == self.__in_event:
            return None
        else:
            return self.__in_event.event_id

    def get_out_event(self):
        return self.__out_event

    def set_out_event(self, out_event):
        self.__out_event = out_event

    def get_out_event_id(self):
        if None == self.__out_event:
            return None
        else:
            return self.__out_event.event_id

    def mark_begin_time(self):
        self.__begin_time = time.time() 

    def get_begin_time(self):
        return self.__begin_time

    def mark_end_time(self):
        self.__end_time = time.time() 

    def get_end_time(self):
        return self.__end_time

    def get_runtime_duration(self):
        if None == self.__begin_time or None == self.__end_time:
            return -1
        else:
            return self.__end_time - self.__begin_time 

    def is_successful(self):
        return None == self.__exceptionp

    def set_exception(self, exception):
        self.__exception = exception

    def get_exception(self):
        return self.__exception

def event_handler(events):
    def decorator(func):
        def wrapper(*args, **kw):
            result = func(*args, **argkw)
            if isinstance(result, EventBuilder):
                current_event = getCurrentEvent()
                return result.build(current_event.source_id, current_event.event_namespace)
            else:
                return None 
        warpper.__event_handlers__ = dict()
        for event in events:
            event_handler = EventHandler(event.event_namespace, event_name, wrapper)
            warpper.__event_handlers__.append(event_handler)
        return wrapper
    return decorator

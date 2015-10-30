# -*- coding:utf-8 -*-  
import time
import inspect
from event import Event, EventBuilder, getCurrentEvent, setCurrentEvent
from event_handler import EventHandler
import threading

    
class MissingCurrentEvent(Exception):

    def __str__(self):
        return 'Missing current event.'

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
            event_handler_runtime.setHandlerParams(
                self.__build_func_params(
                    self.event_handler_func, 
                    event.getParams()
                )
            )
            event_handler_runtime.markBeginTime()
            event_handler_runtime.setOutEvent(
                self.event_handler_func(
                    *event_handler_runtime.handler_params
                )
            )
            event_handler_runtime.markEndTime() 
        except Exception as e:
            event_handler_runtime.setException(e)
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

    def __init__(self, handler_params = None, in_event = None, out_event = None, begin_time = None, end_time = None, exception = None):
        self.__handler_params = handler_params 
        self.__in_event = in_event
        self.__out_event = out_event 
        self.__begin_time = begin_time 
        self.__end_time = end_time 
        self.__exception = exception 

    def getHandlerParams(self):
        return self.__handler_params

    def setHandlerParams(self, handler_params):
        self.__handler_params = handler_params

    def getInEvent(self):
        return self.__in_event

    def setInEvent(self, in_event):
        self.__in_event = in_event

    def getInEventId(self):
        if None == self.__in_event:
            return None
        else:
            return self.__in_event.event_id

    def getOutEvent(self):
        return self.__out_event

    def setOutEvent(self, out_event):
        self.__out_event = out_event

    def getOutEventId(self):
        if None == self.__out_event:
            return None
        else:
            return self.__out_event.event_id

    def markBeginTime(self):
        self.__begin_time = time.time() 

    def getBeginTime(self):
        return self.__begin_time

    def markEndTime(self):
        self.__end_time = time.time() 

    def getEndTime(self):
        return self.__end_time

    def getRuntimeDuration(self):
        if None == self.__begin_time or None == self.__end_time:
            return -1
        else:
            return self.__end_time - self.__begin_time 

    def isSuccessful(self):
        return None == self.__exceptionp

    def setException(self, exception):
        self.__exception = exception

    def getException(self):
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
        warpper.event_handlers = dict()
        for event in events:
            event_handler = EventHandler(event.event_namespace, event_name, wrapper)
            warpper.event_handlers.append(event_handler)
        return wrapper
    return decorator

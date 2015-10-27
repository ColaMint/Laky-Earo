# -*- coding:utf-8 -*-  
import time
import inspect
from event import Event

class EventHandler(object):
    
    def __init__(self, event_namespace, event_name, event_handler_func):
        self.event_namespace = event_namespace
        self.event_name = event_name
        self.event_handler_func = event_handler_func 

class EventHandlerExecutor(object):

    def __init__(self, event_handler, event):
        self.event_handler = event_handler
        self.event = event
        self.begin_time = None 
        self.end_time = None 

    def execute(self, event):
       try:
           final_params = build_func_params(self.event_handler.event_handler_func, event.getParams())
           self.begin_time = time.time() 
           rtn_params = self.event_handler.event_handler_func(*final_params)
           self.end_time = time.time() 
       except Exception as e:
           pass
       finally:
           pass

def build_func_params(fn, params):
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





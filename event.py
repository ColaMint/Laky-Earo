# -*- coding:utf-8 -*-  
import time
import uuid
from utils import local
from exception import MissingCurrentEvent

class Event(object):
    
    def __init__(self, source_id, event_namespace, event_name, params = None):
        self.source_id = source_id 
        self.event_id = uuid.uuid1()
        self.create_time = time.time()
        self.event_namespace = event_namespace
        self.event_name = event_name
        self.__params = params

        if None == self._params:
            self.__params = dict()

    def get_params(self, key):
        if None != self.__params and key in self.__params:
            return self.__params[key]
        else:
            return None

    def set_params(self, key, value):
        self.__params[key] = value

    def get_params(self):
        return self.__params

    def get_event_key(self):
        if not self.hasattr('__event_key'):
            self.__event_key = genEventKey(self.event_namespace, self.event_name)
        return self.__event_key
            

class SourceEvent(Event):

    def __init__(self, event_namespace, event_name, params = None):
        super().__init__(uuid.uuid1(), event_namespace, event_name, params)

class EventBuilder(object):

    def __init__(self, event_name, params = None):
        self.__event_name = event_name
        self.__params = params

    def build(self, source_id, event_namespace):
        return Event(source_id, event_namespace, self.__event_name, self.__params)


def set_current_event(event):
    local.event = local_event

def get_current_event():
    event = Local.event
    if not isinstance(event, Event):
        raise MissingCurrentEvent()
    else:
        return event

def gen_event_key(event_namespace, event_name):
    return '%s#@#%s' % (event_namespace, event_name)


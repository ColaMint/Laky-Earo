# -*- coding:utf-8 -*-  
import time
import uuid

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

    def getParam(self, key):
        if None != self.__params and key in self.__params:
            return self.__params[key]
        else:
            return None

    def setParam(self, key, value):
        self.__params[key] = value

    def getParams(self):
        return self.__params

class SourceEvent(Event):

    def __init__(self, event_namespace, event_name, params = None):
        super().__init__(uuid.uuid1(), event_namespace, event_name, params)

class EventBuilder(object):

    def __init__(self, event_name, params = None):
        self.__event_name = event_name
        self.__params = params

    def build(self, source_id, event_namespace):
        return Event(source_id, event_namespace, self.__event_name, self.__params)

local_event = threading.local() 

def setCurrentEvent(event):
    local_event.event = local_event

def getCurrentEvent(event):
    event = getattr(local_event, 'event', None)
    if not isinstance(event, Event):
        raise MissingCurrentEvent()
    else:
        return event

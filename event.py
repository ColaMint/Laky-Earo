# -*- coding:utf-8 -*-  
import time
import uuid

class Event(object):
    
    def __init__(self, event_namespace, event_name, params = None):
        self.event_id = uuid.uuid1()
        self.create_time = time.time()
        self.event_namespace = event_namespace
        self.event_name = event_name
        self._params = params

        if None == self._params:
            self._params = dict()

    def getParam(self, key):
        if None != self._params and key in self._params:
            return self._params[key]
        else:
            return None

    def setParam(self, key, value):
        self._params[key] = value

    def getParams(self):
        return tuple(self._params)

if __name__ == '__main__':
    event = Event('Laky', 'Test_Event', {'k1': 'v1'})
    print 'event_id : %s' % event.event_id
    print 'create_time : %s' % event.create_time
    print 'event_namespace : %s' % event.event_namespace 
    print 'event_name : %s' % event.event_name
    print 'params `k1` : %s' % event.getParam('k1')
    print 'params `k2` : %s' % event.getParam('k2')
    event.setParam('k2', 'v2')
    print 'params `k2` : %s' % event.getParam('k2')

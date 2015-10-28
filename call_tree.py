# -*- coding:utf-8 -*-  
from event_handler import EventHandlerRuntime

class CallTreeNode(object):
    
    def __init__(self, parent_node, event_handler_runtime):
        self.parent_node = parent_node
        self.event_handler_runtime = event_handler_runtime
        self.child_nodes = list()

    def addChild(self, child_node):
        child_nodes.parent_node = self
        self.child_nodes.append(child_node)

    def getEvent(self):
        if None == self.event_handler_runtime:
            return None
        else:
            return self.event_handler_runtime.result_event

    def getEventId(self):
        if None == self.event_handler_runtime:
            return 'source_event' 
        else:
            return self.event_handler_runtime.result_event.event_id

    def isRoot(self):
        return None == self.parent_node
    
    def isLeaf(self):
        return 0 == len(self.child_nodes)

class CallTreeRoot(CallTreeNode):

    def __init__(self, source_event):
        super().__init__(None, None)
        self.source_event = source_event

    def getEvent(self):
        return self.source_event

class CallTree(object):

    def  __init__(self, source_event):
       self.root = CallTreeRoot(source_event) 
       self.__node_map = {self.root.getEventId(): self.root}

    def __findParent(self, event_id):
        return self.__node_map.get(event_id, None)

    def addNode(self, event_handler_runtime):
        parent_node = self.__findParent(event_handler_runtime.getEventId())
        if None == parent_node:
            return False
        else:
            new_node = CallTreeNode(parent_node, event_handler_runtime)
            self.__node_map[new_node.getEventId()] = new_node
            return True

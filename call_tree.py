# -*- coding:utf-8 -*-  
from event_handler import EventHandlerRuntime

class CallTreeNode(object):
    
    def __init__(self, parent_node, event_handler_runtime):
        self.__parent_node = parent_node
        self.__event_handler_runtime = event_handler_runtime
        self.__child_nodes = list()

    def addChildNode(self, child_node):
        child_nodes.parent_node = self
        self.__child_nodes.append(child_node)

    def getParentNode(self):
        return self.__parent_node

    def getChildNodes(self):
        return self.__child_nodes

    def getEventHandlerRuntime(self):
        return self.__event_handler_runtime

    def getInEventId(self):
        if None == self.__event_handler_runtime:
            return None
        else:
            return self.__event_handler_runtime.getInEventId()

    def getOutEventId(self):
        if None == self.__event_handler_runtime:
            return None
        else:
            return self.__event_handler_runtime.getOutEventId()

    def isRoot(self):
        return None == self.__parent_node
    
    def isLeaf(self):
        return 0 == len(self.__child_nodes)

class CallTreeRoot(CallTreeNode):

    def __init__(self, source_event):
        super().__init__(None, None)
        self.__source_event = source_event

    def getOutEventId(self):
        self.__source_event.getEventId()

class CallTree(object):

    def  __init__(self, source_event):
        self.__root = CallTreeRoot(source_event) 
        self.__node_map = {self.__root.getOutEventId(): self.__root}

    def __findParent(self, in_event_id):
        return self.__node_map.get(in_event_id, None)

    def addNode(self, event_handler_runtime):
        parent_node = self.__findParent(event_handler_runtime.getInEventId())
        if None == parent_node:
            return False
        else:
            new_node = CallTreeNode(parent_node, event_handler_runtime)
            self.__node_map[new_node.getOutEventId()] = new_node
            return True

    def getRoot(self):
        return self.__root

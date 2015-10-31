# -*- coding:utf-8 -*-  
from event_handler import EventHandlerRuntime

class CallTreeNode(object):
    
    def __init__(self, parent_node, event_handler_runtime):
        self.__parent_node = parent_node
        self.__event_handler_runtime = event_handler_runtime
        self.__child_nodes = list()

    def add_child_node(self, child_node):
        child_nodes.parent_node = self
        self.__child_nodes.append(child_node)

    def get_parent_node(self):
        return self.__parent_node

    def get_child_codes(self):
        return self.__child_nodes

    def get_event_handler_runtime(self):
        return self.__event_handler_runtime

    def get_in_event_id(self):
        if None == self.__event_handler_runtime:
            return None
        else:
            return self.__event_handler_runtime.getInEventId()

    def get_out_event_id(self):
        if None == self.__event_handler_runtime:
            return None
        else:
            return self.__event_handler_runtime.get_out_event_id()

    def is_root(self):
        return None == self.__parent_node
    
    def is_leaf(self):
        return 0 == len(self.__child_nodes)

class CallTreeRoot(CallTreeNode):

    def __init__(self, source_event):
        super().__init__(None, None)
        self.__source_event = source_event

    def get_out_event_id(self):
        self.__source_event.get_event_id()

class CallTree(object):

    def  __init__(self, source_event):
        self.__root = CallTreeRoot(source_event) 
        self.__node_map = {self.__root.get_out_event_id(): self.__root}

    def __find_parent(self, in_event_id):
        return self.__node_map.get(in_event_id, None)

    def add_node(self, event_handler_runtime):
        parent_node = self.__find_parent(event_handler_runtime.get_in_event_id())
        if None == parent_node:
            return False
        else:
            new_node = CallTreeNode(parent_node, event_handler_runtime)
            self.__node_map[new_node.get_out_event_id()] = new_node
            return True

    def get_root(self):
        return self.__root

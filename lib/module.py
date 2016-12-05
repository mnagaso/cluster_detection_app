#!/usr/bin/env python
# coding:utf-8

''' Module class
'''

class Module:
    __module_id = 0 # module ID
    __belongs_to_module_id = 0 # 属するモジュールのID

    def __init__(self, module_id):
#        print("generate module : " + str(module_id))
        self.__module_id = module_id
        self.__node_id_list = []

    def include_node(self, node):
        node.set_module_id(self.__module_id)
        self.__node_id_list.append(node.get_id())
        #self.__node_id_list = node.get_id()
#
#AttributeError: 'Node' object has no attribute '_Module__node_id'
    def get_num_nodes(self):
        """return the number of nodes belonging to this module"""
        return len(self.__node_id_list)

    def get_node_list(self):
        """return node list"""
        return self.__node_id_list

    def __repr__(self):
        """definition for when this class object is printed
        """

        #return "module id %s" % (self.__module_id)
        return "module id %s, including node %s" % (self.__module_id, self.__node_id_list)

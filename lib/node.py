#!/usr/bin/env python
# coding:utf-8


''' Node class
'''

class Node:
    __node_id = -1 # ノードID
    __belongs_to_module_id = -1 # 属するモジュールのID

    def __init__(self, node_id):
        self.__node_id = node_id

    def set_module_id(self, module_id):
        #module_id_past = self.__belongs_to_module_id 
        self.__belongs_to_module_id = module_id

    def get_id(self):
        #print (self.__node_id)
        return self.__node_id

    def get_module_id(self):
        return self.__belongs_to_module_id

    def remove_module_id(self):
        self.__belongs_to_module_id = -1

    def __repr__(self):
        """definition for when this class object is printed
        """
        return "node id %s, belongs to %s" % (self.__node_id, self.__belongs_to_module_id)

#!/usr/bin/env python
# coding:utf-8


''' Node class
'''

class Node:
    __node_id = 0 # ノードID
    __belongs_to_module_id = 0 # 属するモジュールのID
    
    def __init__(self, node_id):
#        print("generate node : " + str(node_id))
        self.__node_id = node_id

    def set_module_id(self, module_id):
        self.__belongs_to_module_id = module_id

    def get_id(self):
        #print (self.__node_id)
        return self.__node_id

    def __repr__(self):
        """definition for when this class object is printed
        """
        return "node id %s, belongs to %s" % (self.__node_id, self.__belongs_to_module_id)

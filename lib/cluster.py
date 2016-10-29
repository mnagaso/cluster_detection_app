#!/usr/bin/env python

'''

cluster
management clustering data

'''

from node import Node
from module import Module

class Cluster:
    __nodes = {} # key: node_id, value: node
    __modules = {} # key: module_id, falue: module

    def __init__(self, number_of_nodes):
        for node_id in range(1, number_of_nodes):
            node = Node(node_id)
            self.__nodes[node_id] = node
            module_id = node_id
            module = Module(module_id)
            self.__modules[module_id] = module
            module.include_node(node)

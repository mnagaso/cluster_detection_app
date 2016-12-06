#!/usr/bin/env python

'''

cluster
management clustering data

here we use modified Louvain method (Rosval2010)
Louvain method may be refered in Blondel 2008

input                    output
nodes -> [clustering] -> two level modules
'''

from node import Node
from module import Module

import numpy as np
import quality as ql
import math

class Cluster:
    __nodes = [] # key: node_id, value: node
    __modules = [] # key: module_id, falue: module

    uncompressed_codelength = 0. # code length by Shannon's source coding theorem

    
    def __init__(self, number_of_nodes, w, p_a):
        # calculate uncompressed code length after Shannon's source coding theorem
        for i, p in enumerate(p_a):
            self.uncompressed_codelength -= p*math.log(p, 2.0)
        print ("uncompressed code length:  ", self.uncompressed_codelength, " bits")
 
        for node_id in range(1, number_of_nodes+1,1):
            node = Node(node_id)
            self.__nodes.append(node)
            module_id = node_id
            module = Module(module_id)
            self.__modules.append(module)
            # cleating one-node one-module state
            module.include_node(node)
        
        # quarity object
        QL = ql.Quality()
        initial_ql_val = QL.get_quality_value(self.__nodes, self.__modules, w, p_a)
        print("compressed code length of initial state: ", initial_ql_val)
    #print("__nodes", __nodes)
    #print("__modules", __modules)




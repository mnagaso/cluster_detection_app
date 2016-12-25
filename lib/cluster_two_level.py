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
import scipy.sparse as spa

import quality as ql
import config as cf

import math
import random
import copy

class Cluster_Two_Level:
    __nodes = [] # key: node_id, value: node
    __modules = [] # key: module_id, falue: module
    
    minimum_codelength = 0. # theoretical limiti of code length by Shannon's source coding theorem
  
    def __init__(self, w, p_a):
        # initialize node/module object list
        self.init_nods_mods(p_a)
         
        # invoke clustring for two-level 
        import cluster_core as cc
        Two_level = cc.Cluster_Core(w, p_a, self.__nodes, self.__modules)
        
        self.__nodes = Two_level.get_nodes()
        self.__modules = Two_level.get_modules()
        pa_merged, w_merged = Two_level.get_merged_pa_w_array(w, p_a, self.__modules)

        print("pa_merged: \n", pa_merged)
        print("w_merged : \n", w_merged)
 

    def init_nods_mods(self, p_a):
        number_of_nodes = len(p_a)
        # calculate uncompressed code length after Shannon's source coding theorem
        for i, p in enumerate(p_a):
            self.minimum_codelength -= p*math.log(p, 2.0)
        print ("minimum code length:  ", self.minimum_codelength, " bits")
 
        for node_id in range(1, number_of_nodes+1,1):
            node = Node(node_id)
            self.__nodes.append(node)
            module_id = node_id
            module = Module(module_id)
            self.__modules.append(module)
            # cleating one-node one-module state
            module.add_node(node)
 


    def get_modules(self):
        """ get module list
        """
        return self.__modules

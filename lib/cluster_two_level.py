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

import cluster_core as cc

class Cluster_Two_Level:
    __nodes = [] # key: node_id, value: node
    __modules = [] # key: module_id, falue: module
  
    def __init__(self, w, p_a):
        
        # invoke clustring for two-level 
        Two_level = cc.Cluster_Core(w, p_a)
        
        # get clustring results
        self.__nodes   = Two_level.get_nodes()
        self.__modules = Two_level.get_modules()
        pa_merged, w_merged = Two_level.get_merged_pa_w_array(w, p_a, self.__modules)

        print("pa_merged: \n", pa_merged)
        print("w_merged : \n", w_merged)

        if cf.modified_louvain == True:
            # invoke submodule movements
            self.build_network_tree(w, p_a, self.__modules)   
            # invoke single-node movements

            pass

    def build_network_tree(self, w, p_a, module_list):
        """ build up a network tree
            this function continuously try to devide a sub*module and go deeper layer
        """

        for i, mod in enumerate(module_list):
                # extract the partial w matrix and pa array
                w_part, pa_part = self.extract_partial_w_pa(w.tocsr(), p_a, mod)
                sub_level = cc.Cluster_Core(w_part, pa_part)

                # set node ids to module objects and vice versa

    def extract_partial_w_pa(self, w, p_a, mod_obj):
        """ extract a partial w matrix and pa array based on nodes belonging to a module
        """
        # get node id list
        node_ids  = mod_obj.get_node_list()
        num_nodes = len(node_ids)
        
        # define partial w/pa matrix
        w_part  = spa.lil_matrix((num_nodes,num_nodes))
        pa_part = np.zeros(num_nodes)

        # get values from original w/pa matrix
        for i in range(num_nodes):
            for j in range(num_nodes):
                w_part[i,j] = w[node_ids[i]-1,node_ids[j]-1]

            pa_part[i] = p_a[node_ids[i]-1]

        return w_part, pa_part

    def get_modules(self):
        """ get module list
        """
        return self.__modules

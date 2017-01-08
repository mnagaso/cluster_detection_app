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
#import cluster_tree as tree

class Cluster_Two_Level:
    __nodes = [] # key: node_id, value: node
    __modules = [] # key: module_id, falue: module
  

    #__Tree = tree.Cluster_tree()

    def __init__(self, w, p_a):
        
        # invoke clustring for two-level 
        Two_level = cc.Cluster_Core(w, p_a)
        
        # get clustring results
        self.__nodes   = Two_level.get_nodes()
        self.__modules = Two_level.get_modules()
        pa_merged, w_merged = Two_level.get_merged_pa_w_array(w, p_a, self.__modules)

        print("pa_merged: \n", pa_merged)
        print("w_merged : \n", w_merged) # these merged w/pa may be used for upper move

        if cf.modified_louvain == True:
            # invoke submodule movements
            pass
#            # set a count for check the hierarchy of modules
#            level = 0 # 0:module, 1:sub-module, 2:subsub-module ...
#            Tree.add_one_level(self.__modules, level)
#            self.build_network_tree(w, p_a, self.__modules, level)   
#            # invoke single-node movements


    def build_network_tree(self, w, p_a, module_list):
        """ build up a network tree
            this function continuously try to devide a sub*module and go deeper layer
        """
        self.one_level_finer(w, p_a, module_list)


#    def one_level_finer(self, w, p_a, module_list, level):
#        tree_part = []
#
#        for i, mod in enumerate(module_list):
#            if mod.get_num_nodes() == 1:
#                print("this module cannot be divided")
#                continue
#            # extract the partial w matrix and pa array
#            w_part, pa_part, id_par_chi = self.extract_partial_w_pa(w.tocsr(), p_a, mod)
#            sub_level = cc.Cluster_Core(w_part, pa_part)
#
#            # set node ids to module objects and vice versa
#            sub_nodes   = sub_level.get_nodes()
#            sub_modules = sub_level.get_modules() 
#            print("sub_modules", sub_modules)
#            tree_part.append([sub_nodes,sub_modules, id_par_chi])
#            
#            if len(sub_modules) == 1 and len(module_list) == 1:
#                print("cannot extend this branch")
#            else: # exists any room for node movement
#                print("go deeper")
#                self.one_level_finer(w_part, pa_part, sub_modules)

    def extract_partial_w_pa(self, w, p_a, mod_obj):
        """ extract a partial w matrix and pa array based on nodes belonging to a module
        """
        # get node id list
        node_ids  = mod_obj.get_node_list()
        num_nodes = len(node_ids)

        # prepare node_id_parent <-> node_id_child list
        id_par_chi = np.zeros((num_nodes),np.int)

        # define partial w/pa matrix
        w_part  = spa.lil_matrix((num_nodes,num_nodes))
        pa_part = np.zeros(num_nodes)

        # get values from original w/pa matrix
        for i in range(num_nodes):
            for j in range(num_nodes):
                w_part[i,j] = w[node_ids[i]-1,node_ids[j]-1]

            pa_part[i] = p_a[node_ids[i]-1]
            #print("i, node_ids", i, node_ids[i])
            id_par_chi[i] = node_ids[i] # i: id in child(this level) module, node_ids[i]: id in parent(1 lever coarser) module

        return w_part, pa_part, id_par_chi

    def get_nodes(self):
        """ get node list
        """
        return self.__nodes

    def get_modules(self):
        """ get module list
        """
        return self.__modules

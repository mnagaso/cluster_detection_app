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
import cluster_tree as tree

class Cluster_Two_Level:
    __nodes = [] # key: node_id, value: node
    __modules = [] # key: module_id, falue: module
  

    __Tree = tree.Cluster_tree()

    def __init__(self, w, p_a):
        
        # invoke clustring for two-level 
        Two_level = cc.Cluster_Core(w, p_a)
        
        # get clustring results
        self.__nodes   = Two_level.get_nodes()
        self.__modules = Two_level.get_modules()
        #pa_merged, w_merged = Two_level.get_merged_pa_w_array(w, p_a, self.__modules)

        #print("pa_merged: \n", pa_merged)
        #print("w_merged : \n", w_merged) # these merged w/pa may be used for upper move

        if cf.modified_louvain == True:
            # advance division till until no further splits are possible.
            self.build_network_tree(w, p_a, self.__modules)   
 
            # single node movement
               
            # submodule movements
            self.submodule_movement(w, p_a, self.__modules)

    def build_network_tree(self, w, p_a, module_list):
        """ build up a network tree
            this function continuously try to devide a sub*module and go deeper layer
        """
        # register clustering result to the Tree object
        initial_parent_id = 0
        self.__Tree.add_one_level(module_list, initial_parent_id)

        print(self.__Tree)

        # start to extend branches 
        self.one_level_finer(w, p_a, module_list)

        print("final state of tree")
        self.__Tree.print_tree()

    def one_level_finer(self, w, p_a, module_list):
        """ this function tries to expand each branch of the tree
            by being called recursively
        """

        for i, mod in enumerate(module_list):
            if mod.get_num_nodes() == 1:
                print("this module cannot be divided")
                continue
            # extract the partial w matrix and pa array
            w_part, pa_part, id_glo_loc = self.extract_partial_w_pa(w.tocsr(), p_a, mod)
            sub_level = cc.Cluster_Core(w_part, pa_part)

            # set global node ids
            sub_level.set_nodes_global_id(id_glo_loc)
            #sub_nodes   = sub_level.get_nodes()
            sub_modules = sub_level.get_modules() 
            print("sub_modules \n", sub_modules)
            
            
            # append a branch of the global tree
            # get the parent id of this branch
            parent_id = mod.get_tree_element_id()

            # register a new branch
            self.__Tree.add_one_level(sub_modules, parent_id)
            
            if len(sub_modules) == 1 and len(module_list) == 1:
                print("cannot extend this branch")
            else: # exists any room for node movement
                print("go deeper")
                self.one_level_finer(w, p_a, sub_modules)

    def extract_partial_w_pa(self, w, p_a, mod_obj):
        """ extract a partial w matrix and pa array based on nodes belonging to a module
        """
        # get node id list
        node_ids  = mod_obj.get_global_node_id_list()
        print("node ids",node_ids)
        num_nodes = len(node_ids)

        # prepare node_id_parent <-> node_id_child list
        id_glo_loc = np.zeros((num_nodes),np.int)

        # define partial w/pa matrix
        w_part  = spa.lil_matrix((num_nodes,num_nodes))
        pa_part = np.zeros(num_nodes)

        # get values from original w/pa matrix
        for i in range(num_nodes):
            for j in range(num_nodes):
                w_part[i,j] = w[node_ids[i]-1,node_ids[j]-1]

            pa_part[i] = p_a[node_ids[i]-1]
            #print("i, node_ids", i, node_ids[i])
            id_glo_loc[i] = node_ids[i] # i+1: local id in child(this level) module, node_ids[i]: global id

        return w_part, pa_part, id_glo_loc

    def submodule_movement(self, w, p_a, module_list):
        # invoke a tree traversal and find element groups to be moved
        ids_parent_of_subtree = self.__Tree.find_subtree_to_be_moved()
        print(ids_parent_of_subtree)
        # -> erase the parent and reconstruct the members of parent's parent child members
        self.__Tree.erase_subtrees(ids_parent_of_subtree[0])

        

    def get_nodes(self):
        """ get node list
        """
        return self.__nodes

    def get_modules(self):
        """ get module list
        """
        return self.__modules


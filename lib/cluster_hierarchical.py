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
import sys
#sys.setrecursionlimit(10000)

import cluster_core as cc
import cluster_tree as tree

class Cluster_Hierarchical:
    __nodes   = []  # store node objects
    __modules = []  # store module objects
  
    __Tree = tree.Cluster_tree()

    final_store = None
    ql_global_best = 99999

    def __init__(self, w, p_a):
        # keep accesses to global w p_a
        self.glob_w  = w
        self.glob_pa = p_a

        # Initially clustring for two-levl
        Two_level = cc.Cluster_Core(w, p_a)
        
        # get clustring results
        self.__nodes   = Two_level.get_nodes()
        self.__modules = Two_level.get_modules()
        
        # get the final quality value
        ql_first_division = Two_level.get_ql_final()
        # advance division till no further splits are possible.
        # then submodule and single node movement are done with Depth-First Searching order.
        self.build_network_tree(w, p_a, self.__modules, ql_first_division)   

    def build_network_tree(self, w, p_a, module_list, ql_init=9999):
        """ build up a network tree
        """
        # initialize quality functions
        QL = ql.Quality()

        # register the initial clustering result to the Tree object
        initial_parent_id = 0
        self.__Tree.add_one_level(module_list, initial_parent_id)

        # indicate the initial tree state
        print("initial state of tree")
        self.__Tree.tree_draw_with_ete3(0)
        # calculate initial ql value
        self.ql_global_best = QL.get_hierarchical_quality_value(self.__Tree.get_tree_list(), self.glob_w, self.glob_pa)
        print("initial global quality value: ", self.ql_global_best)

        # start of recursive extention of branches 
        self.one_level_finer(w, p_a, initial_parent_id, ql_init)

        print("final state of tree")
        #self.__Tree.print_tree()
        self.__Tree.tree_draw_with_ete3(initial_parent_id)

    def one_level_finer(self, w, p_a, grand_parent_id, ql_init):
        """ this function tries to expand each branch of the tree
            by being called recursively


        tree_elements,  level
        :
        .   ------------ grand parent
        | \  
        .   .   -------- parent
        |\  |\
        . . . .    ----- child
        : : : :

        """
        # initiation
        QL = ql.Quality()
        loop_count = 0
        ql_best = ql_init
        ql_now = None
        store_tree = copy.deepcopy(self.__Tree.get_tree_list())

        while loop_count < cf.num_trial:
            # for fast conversion
            if grand_parent_id != 0:
                loop_count = cf.num_trial

            queue_ids = copy.deepcopy(self.__Tree.get_element_object(grand_parent_id).id_child)

            while queue_ids:
                # get the parent id of this branch
                parent_id = queue_ids[0]
                mod = self.__Tree.tree_ele2one_module(parent_id)

                num_nodes = mod.get_num_nodes()
                if num_nodes == 1: # module with only one member may not be divided anymore
                    pass
                else:
                    # extract the partial w matrix and pa array
                    w_part, pa_part, id_glo_loc = self.extract_partial_w_pa(w.tocsr(), p_a, mod)
                    sub_level = cc.Cluster_Core(w_part, pa_part)
    
                    # set global node ids
                    sub_level.set_nodes_global_id(id_glo_loc)
                    sub_modules = sub_level.get_modules() 

                    if len(sub_modules) == 1 or len(sub_modules) == num_nodes:
                        pass
                    else:
                        # get quality value
                        ql_temp = sub_level.get_ql_final()

                        # append a branch to the tree
                        # register a new branch
                        self.__Tree.add_one_level(sub_modules, parent_id)

                        erased_id = self.one_level_finer(w, p_a, parent_id, ql_temp)

                        # get quality value
                        #ql_temp = sub_level.get_ql_final()
                        #ql_temp =  QL.get_hierarchical_quality_value(self.__Tree.get_tree_list(), self.glob_w, self.glob_pa)

                        # modify the queue list
                        if erased_id != None:
                            for i in range(len(queue_ids)):
                                ele_id = queue_ids[i]
                                if ele_id >= erased_id:
                                    queue_ids[i] -= 1
 
                # erase a queue already done
                queue_ids.pop(0)
                
            # reconstruct module_list from subtree
            node_list, module_list = self.__Tree.subtree2modulelist(grand_parent_id)

            # restart clustering
            ql_now = self.restart_clustering(w, p_a, grand_parent_id)

            # if the quality of this subtree is imploved
            if QL.check_network_got_better(ql_best, ql_now) == True:
                ql_best = ql_now
                ## store and replace the state of the entire tree
                store_tree = copy.deepcopy(self.__Tree.get_tree_list())
                #self.final_store = copy.deepcopy(self.__Tree.get_tree_list())
                
            else:
                # go to the next loop
                pass

            loop_count += 1

            #if grand_parent_id == 1: ######## for test
            ql_global_temp = QL.get_hierarchical_quality_value(self.__Tree.get_tree_list(), self.glob_w, self.glob_pa)
            if QL.check_network_got_better(self.ql_global_best, ql_global_temp) == True:
                self.ql_global_best = ql_global_temp
                self.final_store = copy.deepcopy(self.__Tree.get_tree_list())

            if grand_parent_id == 0:
                #print("ql_best", ql_best)
                #print(store_tree)
                self.__Tree.tree_draw_with_ete3(0, ql_now)

            # erase "#" for indicate tree states at each step
            #print( self.__Tree.print_tree())
            self.__Tree.tree_draw_with_ete3(0, ql_global_temp)
 
        ### end while loop

        self.__Tree.set_tree_list(store_tree)
        # reload the best state of tree
        # sub module movement will be invoked
 
        # when extention for one subtree stoped (need to )
        if grand_parent_id != 0:
            #print("finish all branches of this subtree finished")
            #print("id", grand_parent_id, "will be erased")
            self.submodule_movement_onesubtree(grand_parent_id)
            erased_id = grand_parent_id
        else:
            #print("recursive tree branch extention finished")
            self.__Tree.set_tree_list(self.final_store)
            #node_list, module_list = self.__Tree.subtree2modulelist(grand_parent_id)
            #self.__modules = module_list
            print("global optimized tree")
            self.__Tree.tree_draw_with_ete3(0, ql_best)

            erased_id = None
            #print("ql initial ---> best", ql_init, " ---> ",ql_best)
        return erased_id

    def restart_clustering(self, w, p_a, parent_id):
        """ restart network division after the state of submodule movement
            and then restart the recursive clustering after
        """
        QL = ql.Quality()
        #print("##### start re-clustering for node id", parent_id)
        node_list, module_list = self.__Tree.subtree2modulelist(parent_id)

        #print("##### module list before\n",module_list)
        w_part, pa_part, id_glo_loc = self.extract_partial_w_pa(w.tocsr(), p_a, module_list)
        #print("##### w_part pa_part check", w_part, pa_part, id_glo_loc)

        # restart clustering from this state
        restarted_cluster = cc.Cluster_Core(w_part, pa_part, node_list, module_list)
        # take new state of module list
        module_list = restarted_cluster.get_modules()
        restarted_cluster.set_nodes_global_id(id_glo_loc)
        #print("##### module list after\n",module_list)
        
        #modify the tree composition
        self.__Tree.replace_subtree(parent_id,module_list)

        ql_now = restarted_cluster.get_ql_final() 
        #ql_now = QL.get_hierarchical_quality_value(self.__Tree.get_tree_list(), self.glob_w, self.glob_pa)

        return ql_now

    def extract_partial_w_pa(self, w, p_a, mod_obj):
        """ extract a partial w matrix and pa array based on nodes belonging to a module
        """
        
        if isinstance(mod_obj, list) == False: #if input only one module 
            # get node id list
            node_ids  = mod_obj.get_global_node_id_list()
            #print("node ids",node_ids)
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

        else: # manage multiple module objects
            node_ids_pre = []
            for i, mod in enumerate(mod_obj):
                # get node id list
                node_ids_pre.extend(mod.get_global_node_id_list())
                #print("node ids",node_ids_pre)
            
            # eliminate duplicated ids
            seen = set()
            node_ids = [x for x in node_ids_pre if x not in seen and not seen.add(x)]
            node_ids.sort()

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

    def submodule_movement_onesubtree(self, parent_id):
        # -> erase the parent and reconstruct the members of parent's parent child members
        self.__Tree.erase_subtrees(parent_id)
        #print("after submodule movement")
        #self.__Tree.print_tree()

    def get_nodes(self):
        """ get node list
        """
        return self.__nodes

    def get_modules(self):
        """ get module list
        """
        return self.__modules

    def get_tree(self):
        """ get tree module
        """
        return self.__Tree
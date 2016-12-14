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
import random
import copy

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
            module.add_node(node)
        
        # quarity object
        QL = ql.Quality()
        initial_ql_val = QL.get_quality_value(self.__modules, w, p_a)
        print("compressed code length of initial state: ", initial_ql_val)

        # variable for following the change of community quality
        ql_now = initial_ql_val

        # to count the passes
        pass_count = 0
        # initial number of modules
        num_modules = len(self.__modules)
        # prepare for marged w matrix and p_a array for generated network
        w_merged = w
        pa_merged = p_a

######### continue node movement till the code length stops to be improved
        while True:
    
            print("\n\n\n")
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("% ")
            print("Search algorithm: ", pass_count, " pass start\n")
            print("% ")
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("\n\n\n")
            

            # (re-)generate the random order for picking a node to be moved
            random_sequence = np.arange(len(pa_merged))
            np.random.shuffle(random_sequence)
            print("generated random sequence: ",random_sequence)

            ### 1st step --- node movement ###
############# secondary loop for each node movement
            for i in range(len(random_sequence)):
                print("\n\n$$$ node movement loop count:  ", i,"$$$$$$$$$$$$$$$$\n\n")
                # find a module where the quality value become the best score
                
                # set a place of module to be moved in array self.__modules[ ]
                mp_i = random_sequence[i]

                # get a list of neighboring module id
                neighbor_list = self.__modules[mp_i].get_neighbor_list(w_merged[:,mp_i].todense(), self.__nodes)
                # get a list of node id to be moved
                nodes_to_be_moved = self.__modules[mp_i].get_node_list()
                #print ("count: ", pass_count)

                # remove nodes from its module
                self.__modules[mp_i].remove_node_all()
                #print ("nodes in module", self.__modules[i].get_node_list())
 
                # remove module id from node objects
                for j, node_id in enumerate(nodes_to_be_moved):
                    self.__nodes[node_id-1].remove_module_id()

                ql_min = ql_now # dump ql value

                # dump module id for destination
                dump_mod_id = -1

                # array to store module ids without member
                module_id_to_be_erased = []

################# thirdly loop for moving a node to neighboring modules
                for index, mod_id_neigh in enumerate(neighbor_list):
                    # dump the neighbor module object
                    print ("------- index: ", index,"mod_id_neigh: ", mod_id_neigh)
                    dump_module = copy.deepcopy(self.__modules[mod_id_neigh - 1])
                    print ("dumped module when dumped", dump_module)                   
                    # add nodes to one of neighboring module
                    self.__modules[mod_id_neigh - 1].add_node_multi_temp(nodes_to_be_moved)
                    print ("dumped module when origin modified", dump_module)
                    print ("modified module", self.__modules[mod_id_neigh - 1])

                    print ("move nodes id: ", nodes_to_be_moved)
                    # calculate code length
                    ql_trial = QL.get_quality_value(self.__modules, w_merged, pa_merged)
                    print ("ql change, minimum_ql ---> this trial node move: ", ql_min, " ---> ",ql_trial)

                    if QL.check_network_got_better(ql_min, ql_trial) == True: # if the clusting become better
                        ql_min = ql_trial
                        dump_mod_id = mod_id_neigh
                        # return the temporal node movement
                        self.__modules[mod_id_neigh - 1] = dump_module
                    else:
                        # return the temporal node movement
                        self.__modules[mod_id_neigh - 1] = dump_module

                # when any ql improvement happened  
                if ql_min < ql_now:
                    # decide one of a neighbor module as a destination of the movement
                    print ("node destination found at module id: ", dump_mod_id)
                    print ("module id", mp_i+1, "will be erased")

                    # add nodes to one of neighboring module
                    self.__modules[dump_mod_id - 1].add_node_multi_temp(nodes_to_be_moved)
 
                    # add module id to each node object
                    for j, node_id in enumerate(nodes_to_be_moved):
                        self.__nodes[node_id-1].set_module_id(dump_mod_id)

                    # store module ids with no member
                    module_id_to_be_erased.append(mp_i+1)
                    print ("module ids to be erased: ", module_id_to_be_erased)
                    
                    # update ql value
                    ql_now = ql_min

                # if no improvement found
                else:
                    print ("destination not found")
                    # return nodes to its former module
                    # for module object
                    # here the node move is not temporary but we us temp method because 
                    # nodes_to_be_moved list has not node object but id itself in integer
                    self.__modules[mp_i].add_node_multi_temp(nodes_to_be_moved)

                    # for node object
                    for j, node_id in enumerate(nodes_to_be_moved):
                        self.__nodes[node_id-1].set_module_id(mp_i+1)
                
            ### 2nd step --- reconstruct modules and links ###
            # module id rename
            for ind, mod_id in enumerate(module_id_to_be_erased):
                # erase __module objects which has no node member
                print ("before erase module in cluster: ", self.__modules)
                self.__modules.pop(mod_id-1)
                print ("after:                        : ", self.__modules)

                # rename module id
                self.rename_module_id(self.__modules, self.__nodes, mod_id)

            # merge p_a and w array
            pa_merged = np.delete(pa_merged, pa_merged[:], None)
            w_merged = np.delete(w_merged, w_merged[:], None)
            self.construct_merged_pa_w_array(w, p_a, pa_merged, w_merged, self.__modules)
                
            

            # exit the search algorithm when the change of quality value became lower than the threshold
            #if change_quality_value <= threshold_search:
            #    break
            pass_count += 1

        # end of community detection

    def rename_module_id(self, modules, nodes, skip_id):
        """ fill skipped id in module list then rename all"""
        for i, obj in enumerate(modules):
            if i >= skip_id-1:
                new_id = obj.get_module_id()-1
                obj.reset_module_id(new_id)
                node_id_list = obj.get_node_list()
                for j, node_id in enumerate(node_id_list):
                    nodes[node_id-1].set_module_id(new_id)

    def construct_merge_pa_w_array(self, w_node_base, pa_node_base, pa_merged, w_merged, modules):
        for i, mod in enumerate(modules):
            node_list = mod.get_node_list()
            pa_to_add = pa_node_base[node_list].sum()
            print ("sum of pa:", pa_to_add)
            pa_merged = np.append(pa_merged,pa_to_add)
            w_merged = np.append(w_merged,pa_to_add)


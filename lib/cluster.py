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
            print("\nSearch algorithm: ", pass_count, " pass start\n")
            print("% ")
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("\n\n\n")
            

            # (re-)generate the random order for picking a node to be moved
            random_sequence = np.arange(len(pa_merged))
            np.random.shuffle(random_sequence)
            print("generated random sequence: ",random_sequence)

            ### 1st step --- node movement ###

            # array to store module ids without member
            module_id_to_be_erased = []

            # store ql value for checking its change between each pass
            ql_pass = ql_now

############# secondary loop for each node movement
            for i in range(len(random_sequence)):
                # find a module where the quality value become the best score
                
                # set a place of module to be moved in array self.__modules[ ]
                mp_i = random_sequence[i]

                # get a list of neighboring module id
                neighbor_list = self.__modules[mp_i].get_neighbor_list(w_merged[:,mp_i].todense().A1, w_merged[mp_i,:].todense().A1)
                print("module id: ", mp_i + 1," has neiboring module id: ", neighbor_list)
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

################# thirdly loop for moving a node to neighboring modules
                for index, mod_id_neigh in enumerate(neighbor_list):
                    # dump the neighbor module object
                    print ("------- pass: ", pass_count, "n-th node: ", i," move trial: ", index,"mod_id_neigh: ", mod_id_neigh)
                    dump_module = copy.deepcopy(self.__modules[mod_id_neigh - 1])
                    #print ("dumped module when dumped", dump_module)                   
                    # add nodes to one of neighboring module
                    self.__modules[mod_id_neigh - 1].add_node_multi_temp(nodes_to_be_moved)
                    print ("dumped module when origin modified", dump_module)
                    print ("modified module", self.__modules[mod_id_neigh - 1])

                    print ("move nodes id: ", nodes_to_be_moved)
                    # calculate code length
                    #ql_trial = QL.get_quality_value(self.__modules, w_merged, pa_merged)
                    ql_trial = QL.get_quality_value(self.__modules, w, p_a)
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
                if QL.check_network_got_better(ql_now, ql_min) == True: #ql_min < ql_now:
                    # decide one of a neighbor module as a destination of the movement
                    print ("node destination found at module id: ", dump_mod_id)
                    print ("module id", mp_i+1, "will be erased")

                    print ("check node member before: ", self.__modules[dump_mod_id-1])
                    # add nodes to one of neighboring module
                    self.__modules[dump_mod_id - 1].add_node_multi_temp(nodes_to_be_moved)
                    print ("check node member after: ", self.__modules[dump_mod_id-1])
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
            
            print("### pass:", pass_count, ", 1st step end")


            ### 2nd step --- reconstruct modules and links ###

            print("modules before rename,", self.__modules)
            print("we are just removing modules: ", module_id_to_be_erased)
            # module id rename
            module_id_to_be_erased.sort()
            erase_count = 0
            for ind, mod_id in enumerate(module_id_to_be_erased):
                # erase __module objects which has no node member
                #print ("before erase module in cluster: ", self.__modules)
                self.__modules.pop(mod_id-1-erase_count)
                #print ("after:                        : ", self.__modules)
                erase_count += 1
            # rename and sort module id
            self.rename_sort_module_id(self.__modules, self.__nodes)

            print("modules after rename,", self.__modules)
            
            # sort node ids

            
            # merge p_a and w array
            #print("pa_merged before: \n", pa_merged)
            #print("w_merged before: \n", w_merged)
            pa_merged, w_merged = self.construct_merge_pa_w_array(w, p_a, pa_merged, w_merged, self.__modules)
            #print("pa_merged after: \n", pa_merged)
            #print("w_merged after: \n", w_merged)
            #print("pa_ori after: \n", p_a)
            #print("w_ori after: \n", w)
   

            

            # exit the search algorithm when the change of quality value became lower than the threshold
            if QL.check_network_converged(ql_pass, ql_now) == True:
                print("#########################################")
                print("#")
                print("# two level clustring algorithm Converged")
                print("#")
                print("#########################################")
                break
            pass_count += 1

        # end of community detection

    def rename_sort_module_id(self, modules, nodes):
        """ fill skipped module id then rename all
            then sort node ids
        """
        for i, obj in enumerate(modules):
    
            new_id = i+1
            obj.reset_module_id(new_id)
            node_id_list = obj.get_node_list()
            for j, node_id in enumerate(node_id_list):
                nodes[node_id-1].set_module_id(new_id)
            # sort
            obj.sort_node_id_list()

    def construct_merge_pa_w_array(self, w_node_base, pa_node_base, pa_merged, w_merged, modules):
 
        pa_merged = np.delete(pa_merged, pa_merged[:], None)
        
        num_module = len(modules)

        # pa list
        pa_temp = [] # list append is faster than np.append
        # re-construct module-based w matrix
        w_merged = spa.lil_matrix((num_module, num_module))

        for i, mod in enumerate(modules):
            node_list = mod.get_node_list()
            #node_list = np.array(mod.get_node_list())
            #print("node list ", node_list)
            pa_to_add = 0
            for j, node in enumerate(node_list):
                #print ("node, pa", node, pa_node_base[node-1])
                pa_to_add += pa_node_base[node-1]
    
                       
            #print ("sum of pa:", pa_to_add)
            pa_temp.append(pa_to_add)
            #print ("pa to marged", pa_temp)
            
            # secondary module loop for preparing w_merged
            for j, mod_2 in enumerate(modules):
                node_list_2 = mod_2.get_node_list()
                #node_list_2 = np.array(mod_2.get_node_list())
                
                if i == j:
                    # internal link weights become 0
                    w_merged[i,j] = 0
                else: # connection with other modules
                    for k in range(len(node_list)): #np.nditer(node_list):
                        for l in range(len(node_list_2)):#np.nditer(node_list_2):
                            w_merged[i,j] += w_node_base[node_list[k]-1,node_list_2[l]-1] 


        # convert to a numpy array
        pa_merged = np.array(pa_temp)
        #print ("pa_merged", pa_merged)
        print("pa_merged in func: \n", pa_merged)
        print("w_merged  in func: \n", w_merged)
   
        return pa_merged, w_merged

    def get_network(self):
        """ get module list
        """
        return self.__modules

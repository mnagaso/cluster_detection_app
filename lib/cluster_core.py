#!/usr/bin/env python

'''

cluster
management clustering data

here we use Louvain method
Louvain method may be refered in Blondel 2008

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

class Cluster_Core:
    #__nodes = [] # key: node_id, value: node
    #__modules = [] # key: module_id, falue: module
    #minimum_codelength = 0. # theoretical limiti of code length by Shannon's source coding theorem
  
    ql_final = 0.
    
    def __init__(self, w, p_a, *init_nods_mods):
        self.__nodes = [] # key: node_id, value: node
        self.__modules = [] # key: module_id, falue: module
        self.minimum_codelength = 0. # theoretical limiti of code length by Shannon's source coding theorem
 
        keys_for_node_extract = [[-1]]

        if len(init_nods_mods) == 0:# or len(init_nods_mods[1]) == 1:
            # initialize node/module object list from w and p_a
            self.init_nods_mods(p_a)
        else:
            #print("initial state",init_nods_mods)
            # start clustering from already separated modules
            self.__nodes   = init_nods_mods[0]
            self.__modules = init_nods_mods[1]
       
        # quarity object
        QL = ql.Quality()
        ql_initial = QL.get_quality_value(self.__modules, w, p_a)
        #print("initial quality value: ", ql_initial)

        # variable for following the change of community quality
        ql_now = ql_initial

        # conut the number of 1st step attempted times 
        attempt_count = 0
        # initial number of modules
        num_modules = len(self.__modules)
        # total number of nodes
        total_num_nodes = 0
        for i, mod in enumerate(self.__modules):
            total_num_nodes += mod.get_num_nodes()

        #print("num mods", num_modules)
        #print("pa marged", p_a)
        # prepare for marged w matrix and p_a array for generated network
        w_merged = w
        pa_merged = p_a

###-###-# first loop: continue node movement till the code length stops to be improved
        while True:
            #print("\n\n\n")
            #print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            #print("% ")
            #print("\nSearch algorithm: ", attempt_count, " attempt start\n")
            #print("% ")
            #print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            #print("\n\n\n")


            #print("### 1st step --- node movement ###")
    
            # (re-)generate the random order for picking a node to be moved
            #random_sequence = np.arange(len(pa_merged))
            random_sequence = np.arange(num_modules)
            np.random.shuffle(random_sequence)
            #print("generated random sequence: ",random_sequence)

            # array to store module ids without member
            module_id_to_be_erased = []

            # store ql value for checking its change between each pass
            ql_before = ql_now

###-###-###-# second loop: for each node movement
            for i in range(len(random_sequence)):
                # find a module where the quality value become the best score
                
                # set a place of module to be moved in array self.__modules[ ]
                # mp_i starts from 0
                mp_i = random_sequence[i]
                #print("random sequence and mpi", random_sequence, mp_i)
                #print("check the mod state", self.__modules)
                num_nodes = self.__modules[mp_i].get_num_nodes()
                # skip the attempt for modules without member node
                if num_nodes == 0:
                    break

                # get a list of node id to be moved
                # all nodes in one module will be moved to neighbor module
                # this movement is equivalent the movement of re-built nodes after re-construction of network in Louvain method
                node_ids_to_be_moved = self.__modules[mp_i].get_node_list()

                for i_l, id_node_moved in enumerate(node_ids_to_be_moved):
                    # get a list of neighboring module id
                    neighbor_list = self.__modules[mp_i].get_neighbor_list(w_merged, self.__modules, id_node_moved)

                    # remove nodes from its module
                    self.__modules[mp_i].remove_node(id_node_moved)
 
                    # remove module id from node objects
                    #self.__nodes[id_node_moved-1].remove_module_id()

                    ql_min = ql_now # dump ql value

                    # dump module id for destination
                    dump_mod_id = -1

###-###-###-###-# third loop: for moving a node to neighboring modules
                    for index, mod_id_neigh in enumerate(neighbor_list):
                    
                        # dump the neighbor module object
                        #print ("attempt: ", attempt_count, "n-th node: ", i," move trial: ", index,"mod_id_neigh: ", mod_id_neigh)
                        if mod_id_neigh != self.__modules[mod_id_neigh-1].get_module_id():
                            print("neibor module id and list id not matched")
                            sys.exit(1)
                        dump_module = copy.deepcopy(self.__modules[mod_id_neigh - 1])
                        # add nodes to one of neighboring module
                        self.__modules[mod_id_neigh - 1].add_node_temp(id_node_moved)
                        #print ("dumped module when origin modified", dump_module)
                        #print ("modified module", self.__modules[mod_id_neigh - 1])
                        #print ("move nodes id: ", node_ids_to_be_moved)

                        # calculate code length
                        # check if all nodes are in the same module -> in this case map equation is not defined.
                        #num_nodes_in_destination = self.__modules[mod_id_neigh - 1].get_num_nodes()
#                        if num_nodes_in_destination == total_num_nodes:
#                            # return the temporal node movement
#                            self.__modules[mod_id_neigh - 1] = dump_module
#                        else:
                        ql_trial = QL.get_quality_value(self.__modules, w_merged, pa_merged)
                        #print ("ql change, minimum_ql ---> this trial node move: ", ql_min, " ---> ",ql_trial)

                        if QL.check_network_got_better(ql_min, ql_trial) == True: # if the clusting become better
                            ql_min = ql_trial
                            dump_mod_id = mod_id_neigh
                            success_dump = copy.deepcopy(self.__modules[mod_id_neigh - 1])
                            # return the temporal node movement
                            self.__modules[mod_id_neigh - 1] = copy.deepcopy(dump_module)
                        else:
                            # return the temporal node movement
                            self.__modules[mod_id_neigh - 1] = copy.deepcopy(dump_module)

                    # when any ql improvement happened  
                    if QL.check_network_got_better(ql_now, ql_min) == True: 
                        # decide one of a neighbor module as a destination of the movement
                        #print ("node destination found at module id: ", dump_mod_id)
                        #print ("module id", self.__modules[mp_i].get_module_id(), "will be erased")

                        #print ("check node member before: ", self.__modules[dump_mod_id-1])
                        # add nodes to one of neighboring module
                        #self.__modules[dump_mod_id - 1].add_node_temp(id_node_moved)
                        self.__modules[dump_mod_id - 1] = copy.deepcopy(success_dump)
                        #print ("check node member after: ", self.__modules[dump_mod_id-1])
                        # add module id to each node object
                        #self.__nodes[id_node_moved-1].set_module_id(dump_mod_id)

                        # update ql value
                        ql_now = ql_min

                    # if no improvement found
                    else:
                        #print ("\n###destination not found\n\n")
                        # return nodes to its former module
                        # for module object
                        # here the node move is not temporary but we us temp method because 
                        # nodes_to_be_moved list has not node object but id itself in integer
                        self.__modules[mp_i].add_node_temp(id_node_moved)

                        # for node object
                        #for j, node_id in enumerate(node_ids_to_be_moved):
                        #self.__nodes[id_node_moved-1].set_module_id(self.__modules[mp_i].get_module_id())
    

                    # print for indicate node movement of each step
                    #print(self.__modules)
   
                #print("### attempt count:", attempt_count, ", 1st step end")

                #print("modules before rename,", self.__modules)

            module_id_to_be_erased = self.get_module_ids_without_node(self.__modules)
    
            #print("we are just removing modules: ", module_id_to_be_erased)
            # module id rename
            module_id_to_be_erased.sort()
            erase_count = 0
            for ind, mod_id in enumerate(module_id_to_be_erased):
                # erase __module objects which has no node member
                self.__modules.pop(mod_id-1-erase_count)
                erase_count += 1

            # rename and sort module id
            self.rename_sort_module_id(self.__modules, self.__nodes)

            #TODO build summed module list 
            keys_for_node_extract = self.compress_modules(self.__modules, keys_for_node_extract, total_num_nodes)
            #print("check keys", keys_for_node_extract)

            # get summed pa, w matrix      
            pa_merged, w_merged = self.get_merged_pa_w_array(w, p_a, self.__modules, keys_for_node_extract)

            # reset number of modules
            num_modules = len(self.__modules)
            # reset total number of nodes
            total_num_nodes = 0
            for i, mod in enumerate(self.__modules):
                total_num_nodes += mod.get_num_nodes()


            # exit the search algorithm when the change of quality value became lower than the threshold
            if QL.check_network_converged(ql_before, ql_now) == True:
                #print("#########################################")
                #print("#")
                #print("# clustring core algorithm Converged")
                #print("# improved quality value: ", ql_now)
                #print("# difference %: ", ql_now/ql_initial*100)
                #print("#########################################")
                self.ql_final = ql_now

                break
            
            attempt_count+=1
 
            # output for division result of this step with local node ids
            #print("modules divided:\n", self.__modules)


        #list_enter_link, list_exit_link, list_internal_link = 
        
        # rebuild module list
        del self.__modules[:]
        self.rebuild_module_list(keys_for_node_extract)

        # calculate enter/exit/internal link weights
        self.sum_link_weight_and_set(w, p_a, self.__modules)       

        # end of community detection


########################################################################################################
    def rebuild_module_list(self, keys_list):
        for i, nodelist in enumerate(keys_list):
            module_id = i+1
            module = Module(module_id)
            module.add_node_multi_temp(nodelist)
            self.__modules.append(module)

    def compress_modules(self, modules, former_key, total_num_nodes):
        """ compress nodes in a module as one node
            then return a list:
            
            key_list[compressed_node_id] = [included node ids...]
            
            -> [[],[],...]
        """

        if former_key[0][0] == -1:
            del former_key[:]
            for i in range(total_num_nodes):
                add_id = [i+1]
                former_key.append(add_id)

        key_list = []
        for i, mod in enumerate(modules):
            member_ids = list(mod.get_node_list())
            key_list_sub = []
            for j, oneid in enumerate(member_ids):
                key_list_sub.extend(former_key[oneid-1][:])
            key_list_sub.sort()
            key_list.append(key_list_sub)
            mod.remove_node_all()
            mod.add_node_temp(i+1)
        
        return key_list

    def init_nods_mods(self, p_a):
        number_of_nodes = len(p_a)
        # calculate uncompressed code length after Shannon's source coding theorem
        for i, p in enumerate(p_a):
            self.minimum_codelength -= p*math.log(p, 2.0)
        #print ("theoretically minimum code length:  ", self.minimum_codelength, " bits")
 
        for node_id in range(1, number_of_nodes+1,1):
            node = Node(node_id)
            self.__nodes.append(node)
            module_id = node_id
            module = Module(module_id)
            self.__modules.append(module)
            # creating one-node one-module state
            module.add_node(node)

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
                #print("node id:", nodes[node_id-1].get_id(),"  mod id assined: ", nodes[node_id-1].get_module_id())
            # sort
            obj.sort_node_id_list()

    def get_merged_pa_w_array(self, w_node_base, pa_node_base, modules, *key):
        """ this function returns w and pa array, for each module summed over its member nodes
        """
        #pa_merged = np.delete(pa_merged, pa_merged[:], None)

        if len(key) == 0:
            key_list = []
            for i in range(len(pa_node_base)):
                key_list.append([i+1])
        else:
            key_list = key[0]              

        num_module = len(modules)

        # pa list
        pa_temp = [] # list append is faster than np.append
        # re-construct module-based w matrix
        w_merged = spa.lil_matrix((num_module, num_module))

        for i, mod in enumerate(modules):
            node_list = []
            for j, node_id in enumerate(mod.get_node_list()):
                node_list.extend(key_list[node_id-1])
            pa_to_add = 0
            for j, node in enumerate(node_list):
                pa_to_add += pa_node_base[node-1]
    
            pa_temp.append(pa_to_add)
            
            # secondary module loop for preparing w_merged
            for j, mod_2 in enumerate(modules):
                node_list_2 = []
                for k, node_id in enumerate(mod_2.get_node_list()):
                    node_list_2.extend(key_list[node_id-1])
                
                #if i == j: # this value should be kept because it is self-loops
                    # internal link weights become 0
                    #w_merged[i,j] = 0
                #else: # connection with other modules
                for k in range(len(node_list)):
                    for l in range(len(node_list_2)):
                        w_merged[i,j] += w_node_base[node_list[k]-1,node_list_2[l]-1] 


        # convert to a numpy array
        pa_merged = np.array(pa_temp)
        #print("pa_merged in func: \n", pa_merged)
        #print("w_merged  in func: \n", w_merged)
   
        return pa_merged, w_merged

    def sum_link_weight_and_set(self, w_node_base, pa_node_base, modules):
        """ this function calculates link weights:
            enter_link   : link weights of entering links
            exit_link    : link weights of exiting  links
            internal_link: link weights of internal links

            and
            total p_a

            ### in hierarchical map equation's case, every values becomes *_flow
        """
        pa_merged, w_merged = self.get_merged_pa_w_array(w_node_base, pa_node_base, modules)
        w_enters = w_merged.sum(axis=1).getA1()
        w_exits  = w_merged.sum(axis=0).getA1()

        
        if cf.division_type == 1: # map equation
            # calculate pa*wa-b and record as *_link
            #pw_exit, pw_enter, pw_internal = self.calc_pa_dot_w(w_node_base, pa_node_base, modules)
            for i, mod_obj in enumerate(modules):
                internal_flow = pa_merged[i] * w_merged[i,i]
                enter_flow    = 0
                exit_flow     = 0

                for j, mod_obj2 in enumerate(modules):
                    if i != j:
                        enter_flow += pa_merged[j] * w_merged[i,j]
                        exit_flow  += pa_merged[i] * w_merged[j,i]

                mod_obj.set_links_and_pa(exit_flow, enter_flow, internal_flow, pa_merged[i])
            
        elif cf.division_type != 1: # modularity or others
            for i, mod_obj in enumerate(modules):
                internal_link = w_merged[i,i]
                enter_link    = w_enters[i] - internal_link 
                exit_link     = w_exits[i]  - internal_link
                mod_obj.set_links_and_pa(exit_link, enter_link, internal_link, pa_merged[i])


    def get_module_ids_without_node(self, modules):
        """ get module id list which has no member node
        """
        module_id_list = []
        for i, mod in enumerate(modules):
            if mod.get_num_nodes() == 0:
                module_id_list.append(mod.get_module_id())

        return module_id_list

    def get_nodes(self):
        """ get node objects' list
        """
        return self.__nodes

    def get_modules(self):
        """ get module list
        """
        return self.__modules

    def get_ql_final(self):
        """ returns final quality value
        """
        return self.ql_final
#sub_level.set_nodes_global_id(id_glo_loc)
    def set_nodes_global_id(self, id_glo_loc):
        for i, mod_obj in enumerate(self.__modules):
            mod_obj.set_global_node_id_list(id_glo_loc)


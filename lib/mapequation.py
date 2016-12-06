#!/usr/bin/env python

''' function for calculation of map equation
'''

import sys
import config as cf
import quality as ql
import numpy as np
import math

class Map(ql.Quality):
    
    # array for 

    def __init__(self):
        print("map equation class defined")


    def find_link_to_out(self, w_oneline, i_mod):
        """ find links from a node to nodes belonging to other module
            then return the sum of those link weights"""
        ws = 0
        for i, w_ele  in enumerate(w_oneline):
            if i != i_mod :
                ws += w_ele
        return ws

    def calc_exit_flow(self, nodes, modules, w, pa): # rosvall2010 eq.6
        exit_flow = np.zeros(len(modules))
        n = len(nodes) #total number of nodes
        for i_mod in range(len(modules)):
            # number of nodes in module_i
            n_i = modules[i_mod].get_num_nodes()
            
            sum_pa = 0
            sum_pa_dot_w = 0

            for i, node_id in enumerate(modules[i_mod].get_node_list()):
                sum_pa += pa[node_id-1]

                # find links from a node to nodes belonging to outer module
                link_weights_to_out = self.find_link_to_out(w[:,node_id-1].todense(), i_mod)
                sum_pa_dot_w += pa[node_id-1]*link_weights_to_out

            exit_flow[i_mod] = cf.tau * (n - n_i)/n * sum_pa + (1 - cf.tau) * sum_pa_dot_w
        return exit_flow     

    def calc_enter_flow(): # inversed eq.6 of rosvall2010
        pass

    def calc_two_level_map(self, modules, exit_flow, pa):
        """ calculate code length using rosvall2010 eq.4
        """
        term_1 = np.sum(exit_flow)*math.log(np.sum(exit_flow), 2.0)
        term_2 = 0.0 #-2.0 * np.dot(exit_flow, math.log(exit_flow, 2.0))
        term_3 = 0.0 #-1.0 * np.dot(pa, math.log(pa, 2.0))
        term_4 = 0.0

        # calculate 3rd term
        for i_node in range(len(pa)):
            term_3 += -1.0 * pa[i_node] * math.log(pa[i_node], 2.0)

        # calculate 2nd, 4th term
        for i_mod in range(len(modules)):
            # 2nd term
            term_2 += -2.0 * exit_flow[i_mod] * math.log(exit_flow[i_mod], 2.0)

            # 4th term
            nodes_in_this_mod = modules[i_mod].get_node_list()
            # summation pa for nodes belonging this module
            sum_pa = 0.0
            for j_node in range(len(nodes_in_this_mod)):
                sum_pa = pa[j_node]
            term_4 += (exit_flow[i_mod] + sum_pa) * math.log(exit_flow[i_mod] + sum_pa, 2.0)

        return term_1 + term_2 + term_3 + term_4

    def get_quality_value(self, __nodes, __modules, w, p_a):
        ''' return map equation value
            all class for quality evaluation need to have exactly the same name of function
        '''
        
        # calculate exit probability
        exit_flow = self.calc_exit_flow(__nodes, __modules, w, p_a)
        #print ("initial state of exit_flow", exit_flow)
        code_length = self.calc_two_level_map(__modules, exit_flow, p_a)
        
        return code_length

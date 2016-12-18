#!/usr/bin/env python

''' function for calculation of map equation
'''

import sys
import config as cf
import quality as ql
import numpy as np
import math

class Map(ql.Quality):
    

    def __init__(self):
        print("map equation class defined")


    def sum_link_weight_to_out(self, w_oneline, node_id, node_id_in_same_mod):
        """ find links from a node to nodes belonging to other module
            then return the sum of those link weights"""
        ws = 0
        #print("object node:", node_id)

        # fisrtly it calculates weight sum from all linked node
        for i, w_val in enumerate(w_oneline):
            #if i != node_id-1 :
            ws += w_val
        # then subtract link weights with nodes in the same module
        for i, node_id in enumerate(node_id_in_same_mod):
            ws -= w_oneline[node_id-1]
            
            #print ("weights:", w_oneline[node_id-1])
        #print("node:", node_id_in_same_mod)
        #print("ws:",ws)
        return ws

    def calc_exit_flow(self, modules, w, pa): # rosvall2010 eq.6
        exit_flow = np.zeros(len(modules))
        n = len(pa) #total number of nodes
        for i_mod, mod_obj in enumerate(modules):
            # number of nodes in module_i
            n_i = mod_obj.get_num_nodes()
            
            sum_pa = 0
            sum_pa_dot_w = 0

            for i, node_id in enumerate(mod_obj.get_node_list()):
                sum_pa += pa[node_id-1]

                # find links from a node to nodes belonging to outer module
                link_weights_to_out = self.sum_link_weight_to_out(w[:,node_id-1].todense(), node_id, mod_obj.get_node_list())
                sum_pa_dot_w += pa[node_id-1]*link_weights_to_out

            #exit_flow[i_mod] = cf.tau * (n - n_i)/(n - 1) * sum_pa + (1 - cf.tau) * sum_pa_dot_w # rosvall2008 eq.7
            exit_flow[i_mod] = cf.tau * (n - n_i)/n * sum_pa + (1 - cf.tau) * sum_pa_dot_w # rosvall20010 eq.6

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
        for i, pa_val in enumerate(pa):
            term_3 += -1.0 * pa_val * math.log(pa_val, 2.0)

        # calculate 2nd, 4th term
        for i, obj_mod in enumerate(modules):
            # 2nd term
            term_2 += -2.0 * exit_flow[i] * math.log(exit_flow[i], 2.0)

            # 4th term
            nodes_in_this_mod = obj_mod.get_node_list()
            # summation pa for nodes belonging this module
            sum_pa = 0.0
            for j, id_node in enumerate(nodes_in_this_mod):
                sum_pa = pa[j]
            term_4 += (exit_flow[i] + sum_pa) * math.log(exit_flow[i] + sum_pa, 2.0)

        return term_1 + term_2 + term_3 + term_4

    def skip_module_without_node(self, modules):
        """ detect modules which has no node 
            then return a module object list which such modules are excluded """
        
        modified_list = [] 

        for i, mod in enumerate(modules):
            if mod.get_num_nodes() != 0:
                modified_list.append(mod)

        #print ("no member module excluded:", modified_list)
        return modified_list

    def get_quality_value(self, __modules, w, p_a):
        ''' *** THIS FUNCTION IS OBLIGATE FOR ALL QUALITY EVALUATION MODULE***

            return map equation value
            all class for quality evaluation need to have exactly the same name of function
        '''

        #print("modules", __modules)
        # skip a module without any node
        mod_to_calc = self.skip_module_without_node(__modules)
        #print("calculated module", mod_to_calc)
        # calculate exit probability
        exit_flow = self.calc_exit_flow(mod_to_calc, w, p_a)
        #print ("state of exit_flow", exit_flow)
        print("the number of modules: ", len(exit_flow))
        code_length = self.calc_two_level_map(mod_to_calc, exit_flow, p_a)
        
        return code_length

    def check_network_got_better(self, ql_before, ql_after):
        """ *** THIS FUNCTION IS OBLIGATE FOR ALL QUALITY EVALUATION MODULE*** 
        
            check the change of ql score and 
            return true if ql value became better
            in mapequation's case, ql value become smaller 
            when better clustring acquired 
        """

        if ql_before > ql_after:
            return True
        else:
            return False

    def check_network_converged(self, ql_before, ql_after):
        """ *** THIS FUNCTION IS OBLIGATE FOR ALL QUALITY EVALUATION MODULE*** 
        
            check the change of ql score and 
            return true if ql value became better
            in mapequation's case, ql value become smaller 
            when better clustring acquired 
        """

        if fabs(ql_before - ql_after) <= threshold_search:
            return True
        else:
            return False


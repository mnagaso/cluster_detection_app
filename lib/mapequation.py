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
        #print("map equation class defined")
        pass
    def sum_link_weight_to_out(self, w_oneline, node_id_in_same_mod):
        """ find links from a node to nodes belonging to other module
            then return the sum of those link weights"""
        ws = 0

        # fisrtly it calculates weight sum from all linked node
        for i, w_val in enumerate(w_oneline):
            ws += w_val
        # then subtract link weights with nodes in the same module
        for i, node_id in enumerate(node_id_in_same_mod):
            ws -= w_oneline[node_id-1]
            
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
                link_weights_to_out = self.sum_link_weight_to_out( w[:,node_id-1].todense().A1, mod_obj.get_node_list())
                sum_pa_dot_w += pa[node_id-1]*link_weights_to_out

            #exit_flow[i_mod] = cf.tau * (n - n_i)/(n - 1) * sum_pa + (1 - cf.tau) * sum_pa_dot_w # rosvall2008 eq.7
            exit_flow[i_mod] = cf.tau * (n - n_i)/n * sum_pa + (1 - cf.tau) * sum_pa_dot_w # rosvall2010 eq.6

        return exit_flow     

    def calc_enter_flow(): # inversed eq.6 of rosvall2010
        pass

    def calc_two_level_map(self, modules, exit_flow, pa):
        """ calculate code length using rosvall2010 eq.1 2 3
        """
        total_exit = np.sum(exit_flow)

        # index codebook i.e. H(Q) in rosvall2010 eq.1
        index_entropy = 0
        for i, mod in enumerate(modules):
            ratio = exit_flow[i]/total_exit
            index_entropy -= ratio*math.log(ratio, 2.0)
        # 1st term of rosvall2010 eq.1
        term_1 = total_exit*index_entropy


        # module codebook
        term_2 = []
        for i, mod in enumerate(modules):
            nodes = mod.get_node_list()

            pa_sum = 0
            # rosvall2010 eq.3           
            module_entropy = 0
            # rate of using module codebook i i.e. p^i_o in rosvall2010 eq.1
            rate_of_use_module_coodbook = 0


            for j, node_id in enumerate(nodes):
                rate_of_use_module_coodbook += pa[node_id-1]
                pa_sum += pa[node_id-1]                

            # rosvall2010 eq.3 1st term
            ratio = exit_flow[i]/(exit_flow[i]+pa_sum)
            module_entropy -= 1.0 * ratio * math.log(ratio, 2.0)

            # rosvall2010 eq.3 2nd term
            term_3_2 = 0
            for j, node_id in enumerate(nodes):
                ratio2 = pa[node_id-1]/(exit_flow[i]+pa_sum)
                term_3_2 -= ratio2*math.log(ratio2, 2.0)


            rate_of_use_module_coodbook += exit_flow[i]
            
            # append value of each module
            value = rate_of_use_module_coodbook*term_3_2
            term_2.append(value)

        # total code length i.e. L(M) in rosvall2010 eq.1
        code_length = term_1 + np.sum(term_2)
        return code_length

    def calc_two_level_map_witheq4(self, modules, exit_flow, pa):
        """ calculate code length using rosvall2010 eq.4
        """
        term_1 = np.sum(exit_flow)*math.log(np.sum(exit_flow), 2.0)
        term_2 = 0.0 
        term_3 = 0.0 
        term_4 = 0.0

        # calculate 3rd term
        for i, pa_val in enumerate(pa):
            term_3 += -1.0 * pa_val * math.log(pa_val, 2.0)

        # calculate 2nd, 4th term
        for i, obj_mod in enumerate(modules):
            # 2nd term
            if obj_mod.get_num_nodes() != 0:
               term_2 += -2.0 * exit_flow[i] * math.log(exit_flow[i], 2.0)

            # 4th term
            nodes_in_this_mod = obj_mod.get_node_list()
            
            if len(nodes_in_this_mod) != 0:
                # summation pa for nodes belonging this module
                sum_pa = 0.0

                for j, id_node in enumerate(nodes_in_this_mod):
                    sum_pa = pa[id_node-1]
                term_4 += (exit_flow[i] + sum_pa) * math.log(exit_flow[i] + sum_pa, 2.0)

        return term_1 + term_2 + term_3 + term_4

    def skip_module_without_node(self, modules):
        """ detect modules which has no node 
            then return a module object list which such modules are excluded """
        
        modified_list = [] 

        for i, mod in enumerate(modules):
            if mod.get_num_nodes() != 0:
                modified_list.append(mod)

        return modified_list

    def get_quality_value(self, __modules, w, p_a):
        ''' *** THIS FUNCTION IS OBLIGATE FOR ALL QUALITY EVALUATION MODULE***

            return map equation value
            all class for quality evaluation need to have exactly the same name of function
        '''
        #rint("modules in mapequation.py", __modules)
        # skip a module without any node
        mod_to_calc = self.skip_module_without_node(__modules)
        #mod_to_calc = __modules

        # check how many modules has its member node
        count_mod_with_nod = 0
        for i, mod in enumerate(mod_to_calc):
            #print("nod num of this mod", mod.get_num_nodes())
            if mod.get_num_nodes() != 0:
                count_mod_with_nod += 1

        #print("count mod with nod", count_mod_with_nod)
        if len(mod_to_calc) == 1 or count_mod_with_nod <= 1:
            code_length = 9999999. # map equation is not defined for one module state
        else:
           # calculate exit probability
            exit_flow = self.calc_exit_flow(mod_to_calc, w, p_a)

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

        if math.fabs(ql_before - ql_after) <= cf.threshold_search:
            return True
        else:
            return False


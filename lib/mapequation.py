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
    
    def plogp(self, p):
        """ mimic a conditional operator for log calculation of map equation """
        if p > 0.0:
            val_return = p * math.log(p, 2.0)
        else:
            val_return = 0.00000

        return val_return

    def sum_link_weight_to_out(self, w_oneline, node_id_in_same_mod):
        """ find links from a node to nodes belonging to other module
            then return the sum of those link weights"""
        ws = 0

        # fisrtly it calculates weight sum from all linked node
        ws = w_oneline.sum()
        # then subtract link weights with nodes in the same module
        # self loop is also subtracted here
        for i, node_id in enumerate(node_id_in_same_mod):
            ws -= w_oneline[node_id-1]
            
        return ws

    def sum_link_weight_from_out(self, w_oneline, node_id_in_the_mod):
        """ find links from a node to nodes belonging to other module
            then return the sum of those link weights"""
        ws = 0

        for i, w_val in enumerate(w_oneline):
            if i+1 in node_id_in_the_mod:
                ws += w_val
           
        return ws

    def calc_exit_flow(self, modules, w, pa): # rosvall2010 eq.6
        """ this function calculates module-transition rate for the case of exiting a walker from modules
            there are two kind of definition for this term i.e. 
            -   rosvall2010 eq.6 or rosvall2008 eq.6
            -   Bohlin_mapequation_tutorial eq.9
            
        """
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
                link_weights_to_out = self.sum_link_weight_to_out( w[:,node_id-1].todense().getA1(), mod_obj.get_node_list())
                sum_pa_dot_w += pa[node_id-1]*link_weights_to_out
            
            if cf.simple_flow != True:
                #exit_flow[i_mod] = cf.tau * (n - n_i)/(n - 1) * sum_pa + (1 - cf.tau) * sum_pa_dot_w # rosvall2008 eq.7
                exit_flow[i_mod] = cf.tau * (n - n_i)/n * sum_pa + (1 - cf.tau) * sum_pa_dot_w # rosvall2010 eq.6
            elif cf.simple_flow == True:
                exit_flow[i_mod] = sum_pa_dot_w              
            else:
                print("simple_flow value in config.py need to be set to True or False")
                sys.exit(1)

        return exit_flow     

    def calc_enter_flow(self, modules, w, pa):
        """ this function calculates module-transition rate for the case of entering a walker from out of the module
            ref. Bohlin_mapequation_tutorial eq.10
        """
        
        enter_flow = np.zeros(len(modules))
        n = len(pa) #total number of nodes

        for i_mod, mod_obj in enumerate(modules):
            # number of nodes in module_i
            n_i = mod_obj.get_num_nodes()
            # obtain a list of nodes excluded from this module
            node_inside = mod_obj.get_node_list()
            node_outside = set(list(range(1,n+1))) - set(node_inside)

            sum_pa = 0
            sum_pa_dot_w = 0

            for i, node_id in enumerate(node_outside):
                sum_pa += pa[node_id-1]

                # find links from a node to nodes belonging to outer module
                link_weights_from_out = self.sum_link_weight_from_out( w[:,node_id-1].todense().getA1(), node_inside)
                sum_pa_dot_w += pa[node_id-1]*link_weights_from_out
            
            if cf.simple_flow != True:
                enter_flow[i_mod] = cf.tau * (1 - (n - n_i) / n) * sum_pa + (1 - cf.tau) * sum_pa_dot_w # rosvall2010 eq.6
            elif cf.simple_flow == True:
                enter_flow[i_mod] = sum_pa_dot_w              
            else:
                print("simple_flow value in config.py need to be set to True or False")
                sys.exit(1)

        return enter_flow  

    def calc_two_level_map(self, modules, exit_flow, pa):
        """ calculate code length using rosvall2010 eq.1 2 3
        """
        total_exit = np.sum(exit_flow)

        # index codebook i.e. H(Q) in rosvall2010 eq.1
        index_entropy = 0
        for i, mod in enumerate(modules):
            #print("tot flow", total_exit, exit_flow[i])
            ratio = exit_flow[i]/total_exit
            index_entropy -= self.plogp(ratio) #ratio*math.log(ratio, 2.0)
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
            module_entropy -= 1.0 * self.plogp(ratio) #ratio * math.log(ratio, 2.0)

            # rosvall2010 eq.3 2nd term
            term_3_2 = 0
            for j, node_id in enumerate(nodes):
                ratio2 = pa[node_id-1]/(exit_flow[i]+pa_sum)
                term_3_2 -= self.plogp(ratio2) #ratio2*math.log(ratio2, 2.0)


            rate_of_use_module_coodbook += exit_flow[i]
            
            # append value of each module
            value = rate_of_use_module_coodbook*term_3_2
            term_2.append(value)

        # total code length i.e. L(M) in rosvall2010 eq.1
        code_length = term_1 + np.sum(term_2)
        return code_length

    def calc_two_level_map_witheq4(self, modules, exit_flow, pa):
        """ calculate code length using rosvall2010 eq.4
            CAUTION: this function or formulation may includes bug
            Not for use now
        """
        term_1 = self.plogp(np.sum(exit_flow)) #np.sum(exit_flow)*math.log(np.sum(exit_flow), 2.0)
        term_2 = 0.0 
        term_3 = 0.0 
        term_4 = 0.0

        # calculate 3rd term
        for i, pa_val in enumerate(pa):
            term_3 += -1.0 * self.plogp(pa_val) #pa_val * math.log(pa_val, 2.0)

        # calculate 2nd, 4th term
        for i, obj_mod in enumerate(modules):
            # 2nd term
            term_2 += -2.0 * self.plogp(exit_flow[i]) #exit_flow[i] * math.log(exit_flow[i], 2.0)

            # 4th term
            nodes_in_this_mod = obj_mod.get_node_list()
            
            # summation pa for nodes belonging this module
            sum_pa = 0.0

            for j, id_node in enumerate(nodes_in_this_mod):
                sum_pa += pa[id_node-1]
            term_4 += self.plogp((exit_flow[i] + sum_pa))#(exit_flow[i] + sum_pa) * math.log(exit_flow[i] + sum_pa, 2.0)

        return term_1 + term_2 + term_3 + term_4

    def calc_two_level_map_with_simple_flow(self, modules, exit_flow, enter_flow, pa):
        """ this function calculates codelength by Bohlin_mapequation_tutorial eq.11 """
        total_exit  = np.sum(exit_flow)
        total_enter = np.sum(enter_flow)

        # index codebook i.e. H(Q)
        index_entropy = 0
        for i, mod in enumerate(modules):
            #print("tot flow", total_exit, exit_flow[i])
            ratio = enter_flow[i]/total_enter
            index_entropy -= self.plogp(ratio) #ratio*math.log(ratio, 2.0)
        # 1st term of Bohlin eq.11
        term_1 = total_enter*index_entropy


        # module codebook
        term_2 = []
        for i, mod in enumerate(modules):
            nodes = mod.get_node_list()

            pa_sum = 0
               
            module_entropy = 0
            # rate of using module codebook i i.e. p^i_o
            rate_of_use_module_coodbook = 0


            for j, node_id in enumerate(nodes):
                rate_of_use_module_coodbook += pa[node_id-1]
                pa_sum += pa[node_id-1]                
            rate_of_use_module_coodbook += exit_flow[i]

            term_2_1 = 0
            # H(Pi) first term
            ratio = exit_flow[i]/(rate_of_use_module_coodbook)
            term_2_1 -= 1.0 * self.plogp(ratio) #ratio * math.log(ratio, 2.0)

            # H(Pi) 2nd term
            term_2_2 = 0
            for j, node_id in enumerate(nodes):
                ratio2 = pa[node_id-1]/(rate_of_use_module_coodbook)
                term_2_2 -= self.plogp(ratio2) #ratio2*math.log(ratio2, 2.0)
            
            # append value of each module
            value = rate_of_use_module_coodbook*(term_2_1 + term_2_2)
            term_2.append(value)

        # total code length
        code_length = term_1 + np.sum(term_2)
        return code_length


    def skip_module_without_node(self, modules):
        """ detect modules which has no node 
            then return a module object list which such modules are excluded """
        
        modified_list = [] 

        for i, mod in enumerate(modules):
            if mod.get_num_nodes() != 0:
                modified_list.append(mod)

        return modified_list


    def get_hierarchical_quality_value(self, tree_eles, w_glob, pa_glob):
        ''' *** THIS FUNCTION IS OBLIGATE FOR QUALITY FUNCTIONS FOR HIERARCHICAL NETWORK QUALIFY

            return hierarchical map equation value
        '''

        # gathering the code length of each modules with deep-first search
        global_codelength = self.dfs_for_mapequation(tree_eles[0], tree_eles, w_glob, pa_glob)

        return global_codelength

    def dfs_for_mapequation(self, ele, all_ele, w_glob, pa_glob):
        """ this function invoke Depth-first tree search
            to calculate code length from bottoms
        """

        this_code_length = 0
       
        # calculate 2nd term of eq.13 for a tree top or eq.14 for intermediate module in rosvall2011
        if ele.is_leaf() == False:
            total_enter_flow = 0
            qo = 0 # eq.9 rosvall2011

            for i, child in enumerate(ele.id_child):
                #print("think about", child)
                target = all_ele[child]
                # gather the child's code length
                child_code_length = self.dfs_for_mapequation(target, all_ele, w_glob, pa_glob)
                # add to the code length of this module
                this_code_length += child_code_length
                
                total_enter_flow += all_ele[child].enter_link
                qo += target.enter_link

            qo += ele.exit_link                    
            # calculate rosvall2011 eq.13-14 right hand first term
            qHQ = 0
            if ele.id_this == 0: # tree top
                for i, child in enumerate(ele.id_child):
                    child_obj = all_ele[child]
                    qHQ -= self.plogp(child_obj.enter_link/total_enter_flow)
                qHQ = total_enter_flow*qHQ

            else: # intermediate module
                qHQ -= self.plogp(ele.exit_link/qo)
                for i, child in enumerate(ele.id_child):
                    child_obj = all_ele[child]
                    qHQ -= self.plogp(child_obj.enter_link/qo)
                qHQ = qo*qHQ
            
            this_code_length += qHQ

        else: # this module is a leaf (no child)
            # rosvall2011 eq.15
            po = ele.exit_link # eq.11
            for i, node_id in enumerate(ele.id_nodes):
                po += pa_glob[node_id-1]

            pHP = -1.0*self.plogp(ele.exit_link/po)# eq.12 
            for i, node_id in enumerate(ele.id_nodes):
                pHP -= self.plogp(pa_glob[node_id-1]/po)
            pHP = po*pHP

            this_code_length += pHP

        return this_code_length


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
           #print(__modules)
           # calculate exit probability
           exit_flow = self.calc_exit_flow(mod_to_calc, w, p_a)
           #print("exit",exit_flow)

           if cf.simple_flow != True:
               #enter_flow  = self.calc_enter_flow(mod_to_calc, w, p_a)
               code_length = self.calc_two_level_map_witheq4(mod_to_calc, exit_flow, p_a)
               #code_length = self.calc_two_level_map(mod_to_calc, exit_flow, p_a)
               #code_length = self.calc_two_level_map_with_simple_flow(mod_to_calc, exit_flow, enter_flow, p_a)
           else:
               enter_flow  = self.calc_enter_flow(mod_to_calc, w, p_a)
               code_length = self.calc_two_level_map_with_simple_flow(mod_to_calc, exit_flow, enter_flow, p_a)


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
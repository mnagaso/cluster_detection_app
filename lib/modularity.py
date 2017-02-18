#!/usr/bin/env python

''' function for "Modularity" calculation
'''

import sys
import config as cf
import quality as ql
import numpy as np
import math

class Modularity(ql.Quality):
    
    def __init__(self):
        #print("modularity class defined")
        pass
    def get_quality_value(self, pre_modules, w, p_a):
        ''' *** THIS FUNCTION IS OBLIGATE FOR ALL QUALITY EVALUATION MODULE***

            return modularity value
            all class for quality evaluation need to have exactly the same name of function
        '''
        modules = []
        for i, mod in enumerate(pre_modules):
            if mod.get_num_nodes() != 0:
                modules.append(mod)        
        
        modularity = 0.
            
        # calculate total weight of all links in the network (w in eq.8 rosvall2010)
        w_in    = w.sum(axis=1).getA1()
        w_out   = w.sum(axis=0).getA1()
        w_total = w_in.sum(axis=0)
        w_total_square = w_total*w_total
            
        for i, mod in enumerate(modules):
            node_id_list = mod.get_node_list()
            
            modularity_module = 0.
            w_internal_module = 0.
            w_in_total  = 0.       
            w_out_total = 0.       
                
            for j, nod in enumerate(node_id_list):
                for k, nod2 in enumerate(node_id_list):
                    # calculate summed links in a module
                    w_internal_module += w[nod-1,nod2-1]

                w_in_total  += w_in[nod-1] 
                w_out_total += w_out[nod-1]
                    
            w_external_module = w_in_total*w_out_total
                
            modularity_module = w_internal_module/w_total - w_external_module/w_total_square
            modularity += modularity_module    

        return modularity

    def check_network_got_better(self, ql_before, ql_after):
        """ *** THIS FUNCTION IS OBLIGATE FOR ALL QUALITY EVALUATION MODULE*** 
        
            check the change of ql score and 
            return true if ql value became better
            in mapequation's case, ql value become smaller 
            when better clustring acquired 
        """

        if ql_before < ql_after:
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


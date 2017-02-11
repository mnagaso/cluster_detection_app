#!/usr/bin/env python

''' function for "Modularity" calculation
'''

import config as cf
import quality as ql

class someNewMethod(ql.Quality):
    
    def __init__(self):
        #print("someNewMethod class defined")
        pass
    def get_quality_value(self, __modules, w, p_a):
        ''' *** THIS FUNCTION IS OBLIGATE FOR ALL QUALITY EVALUATION MODULE***

            input:
                __modules: a list of module objects
                w: link-weight matrix for all nodes
                p_a: node visit frequencies for all nodes
            output:
                float quality_value <- a float value calculated by your original method
            all class for quality evaluation need to have exactly the same name of function
        '''
        
        #
        # here you may add your original calculation methods
        #

        return someNewQuarityValue # return a quality vaule

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
            return true if ql value got converged
        """

        if math.fabs(ql_before - ql_after) <= cf.threshold_search:
            return True
        else:
            return False


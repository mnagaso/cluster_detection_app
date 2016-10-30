#!/usr/bin/env python

'''

calculate p_alpha values
(p_alpha means the probabilities to visit node alpha)

'''

import config as cf
import numpy as np
import scipy.sparse as spa

def power_method():
    pass


def arnoldi():
#    from scipy.sparse.linalg.eigs import eigs

    pass

def init_transient_matrix(w):
    
    T = spa.csr_matrix((cf.total_nodes, cf.total_nodes))

    # calculate W_out_j
    w_out_j = np.zeros((1, cf.total_nodes))
    # sum over columns
    w_out_j = w.sum(axis=0)
    print (w_out_j.size)
    print (w_out_j)

    #debug
    print (w.sum(axis=None))

    # T[i,j] = W[i,j]/W_out_j  
    #T = W.de
    

    if cf.teleport_type == 1:
        # standard teleoprtation
        pass
    elif cf.teleport_type == 2:
        # smart recorded teleportation
        pass
    elif cf.teleport_type == 3:
        #smart unrecorded teleportation
        pass
    else:
        print ("selected teleport_type in config.py is not implemented yet.")
        print ("please check your teleport_type setting in config.py")
        import sys
        sys.exit(1)
    #return t
    pass


def calc_main(w):
    
    # prepare transient matrix T (lambiotte 2012 eq.)
    init_transient_matrix(w)
    pass

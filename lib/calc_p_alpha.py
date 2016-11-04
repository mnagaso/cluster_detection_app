#!/usr/bin/env python

'''

calculate p_alpha values
(p_alpha means the probabilities to visit node alpha)

'''

import sys
import config as cf
import numpy as np
import scipy.sparse as spa

def power_method(A,n):
    ''' here we calculate  
    p_t+1 = A*p_t
    by power method.
    '''
    
    from numpy import linalg as LA
    import time
    time_start = time.time()

    p = np.ones((n,1))
    # set initial p_alpha values to 1/total_nodes
    p *= 1./n
    #print ("check initial p_alpha",p)
    # read the threshold value for the end of iteration
    threshold = cf.p_conv_threshold 

    diff = 999999.
    step = 0
    # array to store p_alpha in former step
    p_former_step = np.zeros((n,1))

    while diff > threshold:
        p_former_step = p

        dump_A_dot_p = np.zeros(n)           
        dump_norm_A_dot_p = 0.
        # A*p_t
        dump_A_dot_p = A.dot(p)
        # |A*p_t|
        dump_norm_A_dot_p = LA.norm(dump_A_dot_p)
        # calculate p_t+1
        p = dump_A_dot_p / dump_norm_A_dot_p

        diff = LA.norm(p - p_former_step)
        if step % 10 == 0:
            print ("step: ", step," ||p_t+1 - p_t|| -> ", diff)
        step += 1

    time_elapsed = time.time() - time_start
    print ("power method converged at:", step, "step")
    print ("end the power iteration with ||p_t+1 - p_t|| = ",diff)
    print ("elapsed time: ", time_elapsed, " seconds")

    print (p.shape)
    print ("check p_sum: ", p.sum(axis=0))
    return p

def arnoldi_method():
#    from scipy.sparse.linalg.eigs import eigs
    ''' here we calculate  
    p_t+1 = A*p_t
    by arnoldi method.
    '''
    
    import math
    from numpy import linalg as LA
    import time
    time_start = time.time()

    p = np.ones((n,1))
    # set initial p_alpha values as || p_t=0 || (norm) = 1
    p *= 1./sqrt(n)
    #print ("check initial p_alpha",p)
    # read the threshold value for the end of iteration
    # in arnoldi-type method, ||A*p_t - p_t|| < threshold is a condition of
    # its convergence
    threshold = cf.p_conv_threshold 

    diff = 999999.
    step = 0
    # array to store p_alpha in former step
    p_former_step = np.zeros((n,1))

    while diff > threshold:
        p_former_step = p

        dump_A_dot_p = np.zeros(n)           
        dump_norm_A_dot_p = 0.
        # A*p_t
        dump_A_dot_p = A.dot(p)
        # |A*p_t|
        dump_norm_A_dot_p = LA.norm(dump_A_dot_p)
        # calculate p_t+1
        p = dump_A_dot_p / dump_norm_A_dot_p

        diff = LA.norm(p - p_former_step)
        if step % 10 == 0:
            print ("step: ", step," |p_t+1 - p_t| -> ", diff)
        step += 1

    time_elapsed = time.time() - time_start
    print ("power method converged at:", step, "step")
    print ("end the power iteration with |p_t+1 - p_t| = ",diff)
    print ("elapsed time: ", time_elapsed, " seconds")

    print (p.shape)
    print ("check p_sum: ", p.sum(axis=0))
    return p



def init_transient_matrix(w):
    # define Transition matrix    
    t = spa.lil_matrix((w.shape[0],w.shape[1]))

    # calculate W_out_j
    w_out_j = np.zeros(w.shape[1])

    # sum over columns
    w_out_j = w.sum(axis=0)

    w_coo = w.tocoo()
    rows, cols = w_coo.nonzero()

    for i,j in zip(rows, cols):
        #print (i, j)
        t[i,j] = w[i,j] / w_out_j[0,j]

    # check if each column of t = 0
    t_col_sum = np.zeros(cf.total_nodes)
    t_col_sum = t.sum(axis=0)
    #print (t_col_sum)

    return t

def get_iterate_matrix(t, n, w):
    func = np.zeros((n, n))
    #print (t)
    if cf.teleport_type == 1:
        # standard teleoprtation
        func = (1. - cf.tau) * t + cf.tau * 1. / n * np.ones((n,n))
    elif cf.teleport_type == 2:
        # smart recorded teleportation

        # calculate w_in_alpha vector
        w_in_alpha = np.zeros(n)

        # sum over rows
        w_in_alpha = w.sum(axis=1)
        #print ("w in", w_in_alpha)
        
        # prepare w_in matrix
        w_in = np.zeros((n,n))

        for col in range(n):
            w_in[col,:] = w_in_alpha[col] 

        # get sum from all elements of w
        w_total = w_in_alpha.sum(axis=0)

        #TODO should we do something for nodes without links ?
        #     ex. if t[i,j] = 0: func[i,j] = 0
        func = (1. - cf.tau) * t + cf.tau * 1. / w_total[0,0] * w_in

    elif cf.teleport_type == 3:
        #smart unrecorded teleportation
        pass
    else:
        print ("selected teleport_type in config.py is not implemented yet.")
        print ("please check your setting in config.py")
        sys.exit(1)

    #print ("check if sum over each column of the iterate matrix equals one.")
    #print (func.sum(axis=0))

    return func


def calc_main(w):
    # set print mode to indicate all
    #np.set_printoptions(threshold=np.inf)
    #print (w)
    
    # prepare transient matrix T (lambiotte 2012 eq.)
    node_number = w.shape[0]
    T = spa.lil_matrix((node_number, node_number))
    T = init_transient_matrix(w)
    
    # define a matrix to be iterated
    mat_iter = get_iterate_matrix(T, node_number, w)


    # invoke eigen value calculation
    if cf.p_algo_type == 1:
        print ("p_alpha calculation with power method on going...")
        return power_method(mat_iter, node_number) 
    elif cf.p_algo_type == 2:
        print ("p_alpha calculation with arnoldi method on going...")
        return arnoldi_method(mat_iter, node_number)
    else:
        print ("selected p_algo_type in config.py is not implemented yet.")
        print ("please check your setting in config.py")
        sys.exit(1)

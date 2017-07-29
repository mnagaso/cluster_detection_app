#!/usr/bin/env python

'''

calculate p_alpha values
(p_alpha means the probabilities to visit node alpha)

'''

import sys
import config as cf
import numpy as np
import scipy.sparse as spa

class Calc_p_alpha:

    def power_method(self, A, n):
        ''' here we calculate  
        p_t+1 = A*p_t
        by power method.
        '''
        
        from numpy import linalg as LA
        import time
        time_start = time.time()
    
        p = np.ones((n,1),dtype=cf.myfloat)
        # set initial p_alpha values to 1/total_nodes
        p *= 1./n
 
        # read the threshold value for the end of iteration
        threshold = cf.p_conv_threshold 
    
        diff = 999999.
        step = 0
        # array to store p_alpha in former step
        p_former_step = np.zeros((n,1),dtype=cf.myfloat)
    
        while diff > threshold:
            p_former_step = p
    
            dump_A_dot_p = np.zeros(n,dtype=cf.myfloat)           
            dump_norm_A_dot_p = 0.
            # A*p_t
            dump_A_dot_p = np.dot(A,p)
            # |A*p_t|
            dump_norm_A_dot_p = LA.norm(dump_A_dot_p, ord=2)
            # calculate p_t+1
            p = dump_A_dot_p / dump_norm_A_dot_p
            diff = LA.norm(p - p_former_step, ord=1)
    
            if step % 10 == 0:
                print ("step: ", step," ||p_t+1 - p_t||_1 -> ", diff)
            step += 1
    
        time_elapsed = time.time() - time_start
        print ("power method converged at:", step, "step")
        print ("end the power iteration with ||p_t+1 - p_t||_1 = ",diff)
        print ("elapsed time: ", time_elapsed, " seconds")
    
        # normalize 
        lenP = LA.norm(p, ord=1)
        #print ("check p_sum normalized: ", p_sum)
        return (p/lenP).getA1()
    
    def arnoldi_method(self, A, n):
        ''' here we calculate  
        p_t+1 = A*p_t
        by arnoldi method.
        '''

        from scipy import sparse
        import scipy.sparse.linalg as sp_linalg

        vals, vecs = sp_linalg.eigs(A,k=6,which='LM')
        p = vecs[:,0].real
        lenP = p.sum()
        
        return p/lenP

    def init_transient_matrix(self, w, n):
        """prepare T (link-weight or hyper link) matrix.
           T is stochastic."""
        # define Transition matrix    
        t = spa.lil_matrix((n, n),dtype=cf.myfloat)
    
        # calculate W_out_j
        w_out_j = np.zeros(n,dtype=cf.myfloat)
    
        # sum over columns
        w_out_j = w.sum(axis=0)
    
        w_coo = w.tocoo()
        rows, cols = w_coo.nonzero()
    
        for i,j in zip(rows, cols):
            t[i,j] = w[i,j] / w_out_j[0,j]
    
        # check if each column of t = 0
        t_col_sum = np.zeros(n,dtype=cf.myfloat)
        t_col_sum = t.sum(axis=0)
        #print ("t_col_sum: ",t_col_sum)
    
        return t
    
    def get_iterate_matrix(self, t, n, w, d):
        """prepare a matrix to be iterated."""
        #func = np.zeros((n, n),dtype=cf.myfloat)
        func = spa.lil_matrix((n, n),dtype=cf.myfloat)

        if cf.teleport_type == 1:
            # standard teleoprtation
            #func = (1. - cf.tau) * t + (cf.tau * 1. / n) * np.ones((n,n)) \
            #    + ((1. - cf.tau)) / n * np.tile(d,(n,1))
            func = (1. - cf.tau) * t + (cf.tau * 1. / n) * np.eye(n) \
                 + (1. - cf.tau) / n * np.tile(d,(n,1))

        elif cf.teleport_type == 2 or cf.teleport_type == 3:
            # smart recorded teleportation
    
            # calculaate w_in_alpha vector
            w_in_alpha = np.zeros(n,dtype=cf.myfloat)
            w_in_alpha = w.sum(axis=1)
            
            # prepare w_in matrix
            w_in = np.zeros((n,n),dtype=cf.myfloat)
            for col in range(n):
                w_in[col,:] = w_in_alpha[col] 
    
            # get sum from all elements of w
            w_total = w_in_alpha.sum(axis=0)
    
            func = (1. - cf.tau) * t + cf.tau * 1. / w_total[0,0] * w_in \
                 + (1. - cf.tau) * 1. / w_total[0,0] * np.einsum('ij,ij->ij',np.asmatrix(w_in_alpha), np.asmatrix(d))

        else:
            print ("selected teleport_type in config.py is not implemented yet.")
            print ("please check your setting in config.py")
            sys.exit(1)
    
        #print ("check if sum over each column of the iterate matrix equals one.")
        #print (func.sum(axis=0))
        #print (func)
        
        return func
    
    def check_dangling_nodes(self,w,n):
        """ look for dangling nodes fron w and make dangling_node_vector a[]
            a[i] = 1 when node_i equal dangling, otherwise a[i] = 0"""
    
        a = np.zeros(n,dtype=cf.myfloat)
    
        # calculate w_in_alpha vector
        w_in_alpha = np.zeros(n,dtype=cf.myfloat)
        # sum over rows
        w_in_alpha = w.sum(axis=1)
    
        # calculate w_out_alpha vector
        w_out_alpha = np.zeros(n,dtype=cf.myfloat)
        # sum over columns
        w_out_alpha = w.sum(axis=0)
        for i in range(n):
            if w_out_alpha[0,i] == 0 and w_in_alpha[i,0] != 0:
                    # node[i] is dangling
                    a[i] = 1
                    print ("node id: ",i+1," dangling")        
        
        print ("number of dangling node", np.count_nonzero(a))
        #print ("dangling_node_vector",a)
    
        return a
    
    def re_calculate_p_alpha_unrecorded(self, pa, w, n):
        """ re calculate p_alpha values from recorded p_alpha"""
        # define new pa array
        new_pa = np.zeros(n,dtype=cf.myfloat)
        
        # calculaate w_in_alpha vector
        w_in_alpha = np.zeros(n,dtype=cf.myfloat)
        w_in_alpha = w.sum(axis=1)
 
        # calculate w_out_alpha vector
        w_out_alpha = np.zeros(n,dtype=cf.myfloat)
        # sum over columns
        w_out_alpha = w.sum(axis=0)

        # get sum from all elements of w
        w_total = w_in_alpha.sum(axis=0)

        for i in range(n):
            
            # find inflow to node i
            connecting_node = []
            for j in range(n):
                if w[i,j] != 0:
                    connecting_node.append(j)
            for j, id_node in enumerate(connecting_node):
                new_pa[i] += pa[id_node]*w[i,id_node]/w_out_alpha[0,id_node]
        
        return new_pa
        

    def __init__(self, w):
        # set print mode to indicate all
        #np.set_printoptions(threshold=np.inf)
        #print (w)
       
        node_number = w.shape[0]
        
        # check if dangling nodes exists
        dangling_node_vector = np.array(node_number,dtype=cf.myfloat)
        dangling_node_vector = self.check_dangling_nodes(w, node_number)
    
        # prepare transient matrix T (lambiotte 2012) or S matrix (found google logic)
        self.T = self.init_transient_matrix(w, node_number)
    
        # define a matrix to be iterated (equivalent to G(oogle matrix))
        mat_iter = self.get_iterate_matrix(self.T, node_number, w, dangling_node_vector)
    
        # invoke eigen value calculation
        if cf.p_algo_type == 1: # standard teleportation
            print ("p_alpha calculation with power method on going...")
            self.p_alpha = self.power_method(mat_iter, node_number) 
        elif cf.p_algo_type == 2: # recorded link teleportation
            print ("p_alpha calculation with arnoldi method on going...")
            self.p_alpha = self.arnoldi_method(mat_iter, node_number)
            print("check p_alpha", self.p_alpha)
        else:
            print ("selected p_algo_type in config.py is not implemented yet.")
            print ("please check your setting in config.py")
            sys.exit(1)
    
        if cf.teleport_type == 3: # unrecorded link teleportation
            self.p_alpha = self.re_calculate_p_alpha_unrecorded(self.p_alpha, w, node_number)

        print ("p_alpha")
        print (self.p_alpha)

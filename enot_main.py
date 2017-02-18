#!/usr/bin/env python

'''

enot project main function

configure parameters -> config.py
global variables     -> lib/global_vars.py

'''


# inport modules
import sys
sys.path.append('./lib')

import global_var as gv
import config as cf

import numpy as np

if __name__ == '__main__':
    ''' call functions by executing order
    '''
    # initialize
    print("#####################################")
    print("## Initialization start            ##")
    print("#####################################")
    print("\n\n\n")


    # read input and get W (link-weight matrix, lambiotte 2012)
    import csv_import as csim
    gv.W = csim.get_w_from_csv(
        cf.infile_path, cf.infile_directed_type, cf.total_nodes)

    # calculate p_alpha
    import calc_p_alpha as cp

    init_p_alpha = cp.Calc_p_alpha(gv.W)
    gv.P_alpha = init_p_alpha.p_alpha
    # gv.W should be normalized (replace with T matrix)
    gv.W = init_p_alpha.T

    # setup seed value for random node-pick order generation
    if cf.seed_var != 0:
        np.random.seed(cf.seed_var)
    else:
        pass



    # search algorithm for hierarchical mapping starts from here
    if cf.division_type == 1:
        print("\n\n\n")
        print("#####################################")
        print("## Two Level Clustering start      ##")
        print("#####################################")
        print("\n\n\n")

        import cluster_two_level as ct
        cluster = ct.Cluster_Two_Level(gv.W, gv.P_alpha)


    elif cf.division_type == 2:
        print("\n\n\n")
        print("#####################################")
        print("## Hierarchical Clustering start   ##")
        print("#####################################")
        print("\n\n\n")

        import cluster_hierarchical as ch
        cluster = ch.Cluster_Hierarchical(gv.W, gv.P_alpha)

    else:
        print("error: the flag type for clustering method is not implemented")
        print("prease check the setup of division_type in config.py")
        sys.exit(1)

    #print("\n\nclustered network: \n", cluster.get_modules())

    # output
    print("\n\n\n")
    print("############################")
    print("## Post-processing start  ##")
    print("############################")
    print("\n\n\n")

    # re-read w matrix for edge indication
    #gv.W = csim.get_w_from_csv(cf.infile_path, cf.infile_directed_type, cf.total_nodes)

    import json_export as jex
    jex.json_out(gv.W, cluster)

    import csv_export as csx
    csx.export_csv(gv.P_alpha, cluster)
    
 
    # visualize

    ##########################################################
    ## debug functions 
    ## # these function visualize the state of w (link) matrix
    ##########################################################
    #import visualize_tools as vt
    # show W matrix for debug
    # vt.show_matrix(gv.W)

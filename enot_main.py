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

    # search algorithm for hierarchical mapping starts from here
    print("\n\n\n")
    print("#####################################")
    print("## Two Level Clustering start      ##")
    print("#####################################")
    print("\n\n\n")

    import cluster as cl
    cluster = cl.Cluster(cf.total_nodes, gv.W, gv.P_alpha)

    print("clustered network: \n", cluster.get_network())
    # output
    # import csv_export
    # csv_export.export_csv()
    # visualize
    import visualize_tools as vt
    # show W matrix for debug
    # vt.show_matrix(gv.W)

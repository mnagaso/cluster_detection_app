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
# call function by executing order
    #initialize
    #import global_var

    # read input and get W (link-weight matrix, lambiotte 2012)
    import csv_import as csim
    gv.W = csim.get_w_from_csv(cf.infile_path, cf.infile_directed_type, cf.total_nodes)

    # calculate p_alpha
    import calc_p_alpha as cp
    gv.P_alpha = cp.calc_main(gv.W)

    # search algorithm for hierarchical mapping starts from here

    # output 
    #import csv_export
    #csv_export.export_csv()

    # visualize
    import visualize_tools as vt
    # show W matrix for debug
    # vt.show_matrix(gv.W)

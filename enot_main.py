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
    import global_var

    # read input first
    import csv_import as csim
    gv.W = csim.get_w_from_csv(cf.infile_path, cf.infile_directed_type, cf.total_nodes)

    # calculate p_alpha
    import calc_p_alpha as cp
    cp.calc_main()

    # search algorithm for hierarchical mapping starts from here

    # output 
    import csv_export
    csv_export.export_csv()
    # visualize

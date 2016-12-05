#!/usr/bin/env python

'''

csv import

'''

import csv
import sys
import config as cf
import numpy as np
from scipy.sparse import lil_matrix

def get_w_from_csv(infile_path, directed_type, number_of_all_nodes):
    #file read from here

    #test print
    print ('here in csv_import')

    #read input file
    csv_reader = csv.reader(open(infile_path))
    #check if the number of node in config.py is correct
    try:
        w = lil_matrix((number_of_all_nodes, number_of_all_nodes),dtype=cf.myfloat)
        for line in csv_reader:
            # input format
            node_id_from, node_id_to, weight = map(np.float16, line)
            w[node_id_to-1,node_id_from-1] = weight

            ## this line is for mimicing undirected input to directed network
            ## by assuming Wij = Wji
            ## TODO should be modified when appropriate input data will be found
            if directed_type == 2: # undirected case
                w[node_id_from-1,node_id_to-1] = weight
            else:
                pass

        return w
    
    except:
        print ("input file read error")
        print ("total_nodes in config.py is not equal to the actual number of nodes in input csv file.")
        sys.exit(1)


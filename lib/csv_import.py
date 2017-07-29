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
    print ('total number of nodes: ', number_of_all_nodes)

    #read input file
    csv_reader = csv.reader(open(infile_path))
    #check if the number of node in config.py is correct
    try:
        w = lil_matrix((number_of_all_nodes, number_of_all_nodes),dtype=cf.myfloat)
        for line in csv_reader:
            # input format
            node_id_from, node_id_to, weight = map(np.float32, line)
            w[node_id_to-1,node_id_from-1] = weight

            ## this line is for mimicing undirected input to directed network
            ## by assuming Wij = Wji
            if directed_type == 2: # undirected case
                w[node_id_from-1,node_id_to-1] = weight

        return w
    
    except:
        print ("input file read error")
        print ("total_nodes in config.py is not equal to the actual number of nodes in input csv file.")

        sys.exit(1)


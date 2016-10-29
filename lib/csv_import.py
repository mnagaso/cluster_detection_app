#!/usr/bin/env python

'''

csv import

'''

import csv
#sys.path.append('./lib')
import global_var as gv

def read_csv(infile_path, directed_type):
    #file read from here

    #test print
    print ('here in csv_import')

    #read input file
    csv_reader = csv.reader(open(infile_path))

    for line in csv_reader:
        # input format
        # l(ink)_start l_goal weight
        node_id_from, node_id_to, weight = map(int, line)
        #print (ff, tt, ww)
        gv.W[node_id_from,node_id_to] = weight

        ## this line is for mimicing undirected input to directed network
        ## by assuming Wij = Wji
        ## TODO should be modified when appropriate input data will be found
        if directed_type == 2: # undirected case
            gv.W[node_id_to,node_id_from] = weight

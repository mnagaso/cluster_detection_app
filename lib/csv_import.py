#!/usr/bin/env python

'''

csv import

'''

import csv
#sys.path.append('./lib')
import global_var as gv
# actually "import config" has already done in global_var 
# but python has implicitely include guard so we import config here again
# for make it clear
import config as cf


def read_csv():
    #file read from here

    #test print
    print ('here in csv_import')

    #read input file
    csv_reader = csv.reader(open(cf.infile))

    for line in csv_reader:
        # input format
        # l(ink)_start l_goal weight
        ff, tt, ww = map(int, line)
        #print (ff, tt, ww)
        gv.W[ff,tt] = ww

        ## this line is for mimicing undirected input to directed network
        ## by assuming Wij = Wji
        ## TODO should be modified when appropriate input data will be found
        gv.W[tt,ff] = ww

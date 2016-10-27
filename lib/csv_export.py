#!/usr/bin/env python

'''

export results to csv file

'''

import csv, numpy

def export_csv():

    #here implementation for testing csv read - csv export
    
    #test print
    import global_var as gv

    # print as lil-matrix format
    print (gv.W)

    # convert from sparse to dense matrix
    # denseW = gv.W.todense()
    # print as general matrix
    # print (denseW)


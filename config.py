#!/usr/bin/env python

'''

setup parameters definition

'''

# input csv filename
infile_path = 'data/test.csv'
infile_directed_type = 2 # 1 : directed, 2 : undirected
# output csv filename
outfile = 'test_out.csv'

# total number of nodes in input data
total_nodes = 7343

# convergence threshold for p_alpha power method
# on Rosvall_2010 this value is set as "1.0e-15"
p_conv_threshold = 1.0e-15

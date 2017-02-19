#!/usr/bin/env python

'''

setup parameters definition

'''


import numpy as np

# input csv filename
#infile_path = 'data/package4_network.csv'
#infile_path = 'data/debug_no_dangling.csv'  
#infile_path = 'data/sixtriangles_dir.csv'  
#infile_path = 'data/n10.csv'  
infile_path = 'data/n24.csv'  
#infile_path = 'data/new_n24.csv'  
#infile_path = 'data/n48.csv'  
#infile_path = 'data/fs_flow.csv'
#infile_path = 'data/fs_sink.csv'
#infile_path = 'data/n50_hie.csv'

# node id-name list filename
#vertices_file_path = 'data/debug_no_dangling_vertices.csv'
#vertices_file_path = 'data/n10_vertices.csv'
vertices_file_path = 'data/n24_vertices.csv'
#vertices_file_path = 'data/new_n24_vertices.csv'
#vertices_file_path = 'data/n48_vertices.csv'
#vertices_file_path = 'data/fs_flow_vertices.csv'
#vertices_file_path = 'data/fs_sink_vertices.csv'
#vertices_file_path = 'data/n50_hie_vertices.csv'


# total number of nodes in input data
#total_nodes = 128 
#total_nodes = 4
#total_nodes = 18
#total_nodes = 10
total_nodes = 24
#total_nodes = 48
#total_nodes = 16
#total_nodes = 50

infile_directed_type = 1 # 1 : directed, 2 : undirected

# output csv filename
outfile_path = 'output_files/test_out.csv'

# convergence threshold for p_alpha power method
# on Rosvall_2010 this value is set as "1.0e-15"
p_conv_threshold = 1.0e-14

# algorithm for calculation of p_alpha; 1 : power method, 2 : arnoldi method
p_algo_type = 1

# type of equation for transient matrix; 1 : standard teleportation, 2 : smart recorded teleportation, 3 : smart unrecorded teleportation. (ref. lambiotte_2012)
teleport_type = 1

# tau: teleportation probability, tau = 1 - d, where d is damping factor
tau = 0.15

# method for clustering; 1: map equation, 2: modulity
quality_method = 1

# community division type; 1: two-level, 2: hierarchial
division_type = 1

# threshold for loop of search algorithm
threshold_search = 0.000000000000000000000000000000

# numpy accuracy
myfloat = np.float64

# seed number for random node-pick order generation
# set = 0 for totally random generation
seed_var = 1111#1919810 

# set True for modified louvain method (invoke Submodule/Single-node movements in Rosvall_2010 p.22)
modified_louvain =True

# how many times, this code tries to extend a branch of each subtree to find a best clustering.
num_trial = 3

# if True, we use simple exit/enter flow (Bohlin_mapequation_tutorial eq.9). else if False, the definition of rosvall2010 eq.6 is used.
#simple_flow = False#True

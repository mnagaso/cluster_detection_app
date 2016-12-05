#!/usr/bin/env python

'''

cluster
management clustering data

here we use modified Louvain method (Rosval2010)
Louvain method may be refered in Blondel 2008

input                    output
nodes -> [clustering] -> two level modules

input: node, link, weight, p_alpha
output: module_id for each node

necessary arrays
#community id to which each node belongs
n2c[level,node_id] = community_id


'''

from node import Node
from module import Module

import numpy as np
import quality as ql
import math

class Cluster:
    __nodes = [] # key: node_id, value: node
    __modules = [] # key: module_id, falue: module

    uncompressed_codelength = 0. # code length by Shannon's source coding theorem

    
    def __init__(self, number_of_nodes, w, p_a):
        # calculate uncompressed code length after Shannon's source coding theorem
        for i, p in enumerate(p_a):
            self.uncompressed_codelength -= p*math.log(p, 2.0)
        print ("uncompressed code length:  ", self.uncompressed_codelength)
 
        for node_id in range(1, number_of_nodes+1,1):
            node = Node(node_id)
            self.__nodes.append(node)
            module_id = node_id
            module = Module(module_id)
            self.__modules.append(module)
            # cleating one-node one-module state
            module.include_node(node)
        
        # quarity object
        QL = ql.Quality()
        initial_ql_val = QL.get_quality_value(self.__nodes, self.__modules, w, p_a)
    #print("__nodes", __nodes)
    #print("__modules", __modules)


#        # initialize n2c array
#        # n2c[community level,node_id] = community(module)_id
#        n2c = np.zeros([], dtype=np.uint8)
#        num_init_level = 1
#        n2c = np.resize(n2c, (num_init_level, number_of_nodes))
#
#        # make one-node one-module state
#        for index, val in np.ndenumerate(n2c):
#            n2c[num_init_level,index[1]] = index[1]
#        ## array test for add hie
#        #n2c = np.resize(n2c, (num_init_level+1, number_of_nodes))
#        #for index, val in np.ndenumerate(n2c):
#        #    n2c[num_init_level,index[1]] = 99
# 
#        #print("n2c",n2c)
#
#
#        # list of node_ids which will be divided
#        # all nodes are hold initially
#        nodes2div = np.arange(number_of_nodes,dtype=np.int8)
#
#        # two-level clustering
#        initial_two = self.one_level(nodes2div, n2c, w, p_a)
#     
#
#    def summed_weight():
#        ''' prepare an array 
#        '''
#
#    def calc_neighbors(self):
#        ''' calculate set of neighboring node
#        '''
#        
#        pass
#
#
#    def one_pass(self):
#        ''' handle one pass 
#            input: nodes 
#        '''
#        pass
#
#    def one_level(self, nodes, n2c, w, p_a):
#        ''' make two_level clustering
#            by adding one additional level
#
#            call one_pass function while quality(modularity/map equation) value's being improved
#
#            input nodes are actually nodes themselves
#            and also sometimes being modules regarded as nodes
#        '''
#        #print("nodes",nodes)
#        num_nodes = nodes.shape[0]
#
#        # decide the order to pick one node to be moved to a neighboring module
#        np.random.shuffle(nodes)
#        #print("randomized node order", nodes)    
#        import quality as ql
#        aaa = ql.Quality()
#        init_mp = aaa.get_map_value(n2c, w, p_a)
#        print("map val in initial state:", init_mp)
#
#        # node movement continues untill quality value stops to improve
#        #while 
#
#        pass
#
#    #def node move
#
#    #def call quality evaluation
#
#    #def regard community as a node and link summention
#
#
#    #def clean up module_ids without any node then reordering

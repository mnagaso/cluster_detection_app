#!/usr/bin/env python

'''

debug functions

'''

def check_dangling_nodes(w_matrix):
    ''' this module checks if dangling nodes exist in w(link weight) matrix
    '''
    
    import scipy.sparse

    print ("### debug mode")
    print ("### checking dangling nodes")
    print ("### found at row ,col ")
    
    count_dangling_node = 0

    #wdense = w_matrix.todense()
    wcsr = w_matrix.tocsr()
    wcoo = w_matrix.tocoo()
    rows, cols = wcoo.nonzero()
    for i,j in zip(rows, cols):
        print (i,j, wcsr[i,j])
        if wcsr[j,i] == 0:
            print (i+1, j+1) # indicate actual ids starting from 1
            count_dangling_node += 1


    if count_dangling_node == 0:
        print ("### no dangling node found")
    else:
        print ("### total number of dangling nodes: ", count_dangling_node)

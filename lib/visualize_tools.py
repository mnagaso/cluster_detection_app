#!/usr/bin/env python

'''

defs for visualization

'''

def show_matrix(m):
    # image output of W matrix for debug use
    import matplotlib.pyplot as plt
    plt.spy(m, precision=0, markersize=1)
    plt.show()
 

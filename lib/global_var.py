#!/usr/bin/env python

'''

global variables' definitions here

'''

import config as cf

from scipy.sparse import lil_matrix
#from numpy import array
import numpy as np
# sparse matrix for link-weights (Wij in lambiotte 2012)
W = lil_matrix((cf.total_nodes, cf.total_nodes), dtype=cf.myfloat)

# probability to visit node alpha
P_alpha = np.zeros((1,cf.total_nodes), dtype=cf.myfloat)

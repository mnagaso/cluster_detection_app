#!/usr/bin/env python

'''

global variables' definitions here

'''

import config as cf

from scipy.sparse import lil_matrix
from numpy import array

# sparse matrix for link-weights (Wij in lambiotte 2012)
W = lil_matrix((cf.total_nodes, cf.total_nodes))


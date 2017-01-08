#!/usr/bin/env python

'''

this is a module which records the tree structure
node ids have its local ids which is uniform only in each module

module_id,     level
1   ------------ 1
|\  
1 2   ---------- 2
| |\
1 2 3   -------- 3


__module_tree = [module_list_level1, module_list_level2, ...]

'''

class Cluster_tree:
    __modules_tree = []

    def __init__(self):
        print("cluster tree initialized")

    def add_one_level(self, module_list)
        """ add one level to __module_tree
        """

        __modules_tree.append([])
       # __modules_tree[level,].append

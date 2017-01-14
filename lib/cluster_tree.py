#!/usr/bin/env python

'''

this is a module which records the tree structure
node ids have its local ids which is uniform only in each module

module_id,     level
0   ------------ 0
| \  
1   2   -------- 1
|\  |\
3 4 5 6    ----- 2


'''

class Cluster_tree:
    __modules_tree = []

    def __init__(self):
        print("cluster tree initialized")
        # add root node
        self.__modules_tree.append(ele())

    def add_one_level(self, module_list, id_parent):
        """ add one level to __module_tree
        """

        # erase original node ids which parent holds (avoiding double usage of memory space)
        self.__modules_tree[id_parent].delete_nodes()       

        start_id = len(self.__modules_tree)

        for i, obj_mod in enumerate(module_list):
            id_next = -1
            id_previous = -1
            this_id = start_id + i       

            # set an id of next element
            if i != len(module_list)-1:
                id_next = this_id+1         
            # set an id of previous element
            if i != 0:
                id_previous = this_id-1 

            ele_added = ele(id_parent, id_next, id_previous)           
            
            # add id to the parent of this leaf            
            self.__modules_tree[id_parent].set_child(this_id)

            # add original node ids belonging to this element
            ele_added.set_nodes(obj_mod.get_global_node_id_list())

            # add a leaf
            self.__modules_tree.append(ele_added)

            # set element id for module object
            obj_mod.set_tree_element_id(this_id)

    def get_next_element_id(self):
        return len(self.__modules_tree)

    def __repr__(self):
        return "state of tree: \n %s"  % self.__modules_tree

class ele:
    """ store the necessary information of each node/element/module of the tree
        parent   : id of parent module
        child    : ids of child modules
        next     : id of next module in the same branch
        previous : id of previous module in the same branch
    
        ex: for module 1
            parent   = 0
            child    = 3,4
            next     = 2
            previous = -1 (does not exist) 
    
        ex2: for module 2
            parent   = 0
            child    = 5,6
            next     = -1 (does not exist)
            previous = 1
    
    
    """
    def __init__(self, id_parent=-1, id_next=-1, id_previous=-1):
        self.id_parent   = id_parent
        self.id_child    = [] # childs will be added when there are generated
        self.id_next     = id_next
        self.id_previous = id_previous

        self.id_nodes = []

    def set_child(self, id_list_childs):
        self.id_child.append(id_list_childs)

    def set_next(self, id_next):
        self.id_next = id_next

    def set_previous(self, id_previous):
        self.id_previous = id_previous

    def set_nodes(self, list_node_ids):
        self.id_nodes = list_node_ids

    def delete_nodes(self):
        del self.id_nodes[:]

    def __repr__(self):
        """definition for when this class object is printed
        """
        
        return "parent: %s child: %s, next: %s, previous: %s, node members: %s \n" % (self.id_parent, self.id_child, self.id_next, self.id_previous, self.id_nodes)

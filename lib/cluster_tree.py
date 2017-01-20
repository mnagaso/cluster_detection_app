#!/usr/bin/env python

'''

this is a module which records the tree structure
node ids have its local ids which is uniform only in each module

module_id,     level
0   ------------ 0
| \  
1   4   -------- 1
|\  |\
2 3 5 6    ----- 2


'''

class Cluster_tree:
    __modules_tree = []

    def __init__(self):
        print("cluster tree initialized")
        # add root node
        root_id = 0
        self.__modules_tree.append(ele(root_id))

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

            # set id of next element
            if i != len(module_list)-1:
                id_next = this_id+1         
            # set id of previous element
            if i != 0:
                id_previous = this_id-1 
            
            # create a tree element
            ele_added = ele( this_id, id_parent, id_next, id_previous)           
            # add this id to its parent            
            self.__modules_tree[id_parent].set_child(this_id)
            # add original node ids belonging to this element
            ele_added.set_nodes(obj_mod.get_global_node_id_list())
            # add this element to the tree array
            self.__modules_tree.append(ele_added)
            # set element id to module object
            obj_mod.set_tree_element_id(this_id)

    def get_next_element_id(self):
        return len(self.__modules_tree)

    def print_tree(self):
        for i, ele in enumerate(self.__modules_tree):
            print( ele, end="")

    def get_leafs(self):
        """ find leafs (end of a branch) then return those element id
	"""
        element_id_of_leafs = []

        for i, ele in enumerate(self.__modules_tree):
            if len(ele.id_child) == 0:                                                                                  
                element_id_of_leafs.append(i)

        return element_id_of_leafs 

    def find_subtree_to_be_moved(self):
        """ this function searches subtree whose children do not have any grand-child element
            like
            |
            1
            |\
            2 3
            
            then return the parent_id (i.e. 1 in the example)
        """
        # array to store subtrees' parent id
        sub_ids = []

        # invoke depth-first pre-order search
        root = self.__modules_tree[0]
        self.preorder(root,sub_ids)

        #print("found sub trees",sub_ids)
        return sub_ids

    def preorder(self, ele, sub_ids):
        """ this function invoke Depth-first pre-order tree search
        """

        # check if the children has no grand child
        go_deeper_count = 0

        for i, child in enumerate(ele.id_child):
            #print("think about", child)
            target = self.__modules_tree[child]
            if len(target.id_child) != 0:
                self.preorder(target,sub_ids)
                go_deeper_count += 1

        if go_deeper_count == 0:
            # this ele(ment) is the one which should be shrunk
            sub_ids.append(ele.id_this)
            

    def erase_subtrees(self, ids_parent):
        """ erase parent of subtree then elevate its children to the same level of erased parent 
        """
    
        # manage if the input is int
        if isinstance(ids_parent, int):
            ids_parent_of_subtree = []
            ids_parent_of_subtree.append(ids_parent)
        # or list
        else:
            ids_parent_of_subtree = ids_parent

        for i, id_erased in enumerate(ids_parent_of_subtree):
            id_parent_to_be_erased = id_erased - i
            
            # dump ids in parent element 
            grand_parent = self.__modules_tree[id_parent_to_be_erased].id_parent
            id_previous  = self.__modules_tree[id_parent_to_be_erased].id_previous
            id_next      = self.__modules_tree[id_parent_to_be_erased].id_next
            id_children = [] # list requires initializing
            id_children.extend(self.__modules_tree[id_parent_to_be_erased].id_child[:])
  
            #print("id:",id_parent_to_be_erased, "is erased")
            #print("id_children", id_children)
 
            for j, id_child in enumerate(id_children):
                #print("child", id_child)
                # children join to its parent's group
                self.__modules_tree[id_child].set_parent(grand_parent)
                # set grand parent's child ids
                self.__modules_tree[grand_parent].set_child(id_child)

            # reset next/previous id
            if id_previous != -1:
                self.__modules_tree[id_children[0]].set_previous(id_previous)
                self.__modules_tree[id_previous].set_next(id_children[0])
            if id_next != -1:
                self.__modules_tree[id_children[-1]].set_next(id_next)
                self.__modules_tree[id_next].set_previous(id_children[-1])

            # erase a parent
            del(self.__modules_tree[id_parent_to_be_erased])
            for j, id_child_of_grand_parent in enumerate(self.__modules_tree[grand_parent].id_child):
                if id_child_of_grand_parent == id_parent_to_be_erased:
                    del(self.__modules_tree[grand_parent].id_child[j])

            # reset id numbers for all elements after erased id
            self.reset_ids(id_parent_to_be_erased)

            #print("state tree,\n", self.__modules_tree)

    def reset_ids(self, erased_id):
        for i, ele in enumerate(self.__modules_tree):
            if ele.id_this > erased_id:
                ele.id_this -= 1
            if ele.id_parent > erased_id:
                ele.id_parent -= 1
            if ele.id_previous > erased_id:
                ele.id_previous -= 1
            if ele.id_next > erased_id:
                ele.id_next -= 1
            
            modified_children = []
            for i, child in enumerate(ele.id_child):
                if child > erased_id:
                    modified_children.append(child-1)
                else:
                    modified_children.append(child)

            del(ele.id_child[:])
            ele.set_childs_at_once(modified_children[:])
        

    def __repr__(self):
        return "state of tree: \n %s"  % self.__modules_tree

class ele:
    """ store the necessary information of each node/element/module of the tree
        this     : id of this element. this value should be strictly accord with the place in self.__modules_tree array
        
        parent   : id of parent element
        child    : ids of child element
        next     : id of next element in the same branch
        previous : id of previous element in the same branch
    
        ex: for element 1
            parent   = 0
            child    = 2,3
            next     = 4
            previous = -1 (does not exist) 
    
        ex2: for element 4
            parent   = 0
            child    = 5,6
            next     = -1 (does not exist)
            previous = 1

        module_id,     level
        0   ------------ 0
        | \  
        1   4   -------- 1
        |\  |\
        2 3 5 6    ----- 2


    """
    def __init__(self, id_this, id_parent=-1, id_next=-1, id_previous=-1):
        self.id_this = id_this

        self.id_parent   = id_parent
        self.id_child    = [] # childs will be added when there are generated
        self.id_next     = id_next
        self.id_previous = id_previous

        self.id_nodes = []

    def set_parent(self, id_parent):
        self.id_parent = id_parent
    def set_child(self, id_child):
        self.id_child.append(id_child)
    def set_childs_at_once(self, id_list_child):
        self.id_child.extend(id_list_child[:])
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
        
        return "this: %s, parent: %s child: %s, next: %s, previous: %s, node members: %s \n" % (self.id_this, self.id_parent, self.id_child, self.id_next, self.id_previous, self.id_nodes)

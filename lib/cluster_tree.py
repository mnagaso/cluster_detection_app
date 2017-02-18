from __future__ import print_function
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

import sys
import copy
import math

class Cluster_tree:
    __modules_tree = []

    def __init__(self):
        print("cluster tree initialized")
        # add root node
        root_id = 0
        self.__modules_tree.append(ele(root_id))

        # value dump for tree indication
        self.num_str_lines = 0

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

            # set flows
            ele_added.set_exit_link(obj_mod.enter_link)
            ele_added.set_enter_link(obj_mod.exit_link)
            ele_added.set_internal_link(obj_mod.internal_link)
            ele_added.set_sum_pa(obj_mod.sum_pa)

            # add this element to the tree array
            self.__modules_tree.append(ele_added)

            

    def replace_subtree(self, parent_id, module_list):
        """ erase all elements under parent_id then reconstuct entire subtree by module_list"""
        #print(self.__modules_tree)
        # erase subtree
        ## list up all elements under parent_id (only parent_id will be kept)
        ids_to_be_erased = []
        self.find_ele_under_one_ele(self.__modules_tree[parent_id], ids_to_be_erased)
        ids_to_be_erased.pop(0) # erase parent_id
        
        ## erase all then reset element ids
        self.erase_eles_multi(ids_to_be_erased) 
        del self.__modules_tree[parent_id].id_child[:]
        #print(self.__modules_tree)

        # reconstruct a subtree
        self.add_one_level(module_list, parent_id)
        #print(self.__modules_tree)

    def find_ele_under_one_ele(self, ele, sub_ids):
        """ this function invoke Depth-first pre-order tree search
            then returns all elements under
        """

        sub_ids.append(ele.id_this)

        for i, child in enumerate(ele.id_child):
            #print("think about", child)
            target = self.__modules_tree[child]
            self.find_ele_under_one_ele(target,sub_ids)

    def get_next_element_id(self):
        return len(self.__modules_tree)

    def print_tree(self):
        for i, ele in enumerate(self.__modules_tree):
            print( "id: ", i, ele, end="")

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

    def erase_eles_multi(self, ele_ids):
        """ erase multiple elements then re-assigne element ids """
        
        queue = copy.deepcopy(ele_ids)

        while queue:
            ele_id = queue.pop(0)           
            self.__modules_tree.pop(ele_id)
            self.reset_ids(ele_id)
            # modify element ids on the queue list
            for i, one_id in enumerate(queue):
                if one_id > ele_id:
                    queue[i] -= 1

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
        

    def get_element_object(self, ele_id):
        if isinstance(ele_id, int):
            return self.__modules_tree[ele_id]
        else:
            ids = []
            for i, one_id in enumerate(ele_id):
                ids.append(self.__modules_tree[one_id])
            return ids

    def get_element_id_from_object(self, obj_ele):
        return self.__modules_tree.index(obj_ele)

    def get_tree_list(self):
        return self.__modules_tree
    def set_tree_list(self, list_to_copy):
        del self.__modules_tree[:]
        new_list = copy.deepcopy(list_to_copy)
        self.__modules_tree.extend(new_list)

    def tree_ele2one_module(self, ele_id):
        from module import Module
        from node   import Node
 
        nodes = []
        ele_obj = self.__modules_tree[ele_id]
        node_count = 1


        # store global node ids then create local_id <-> global_id list
        store_global_ids = ele_obj.id_nodes
        if len(store_global_ids) == 0:
            print("tree element with no node member was tried to be converted to module object")
            sys.exit(1)

        #print("store_global_ids before seen", store_global_ids)

        # eliminate duplicated ids
        #seen = set()
        #id_glo_loc = [x for x in store_global_ids if x not in seen and not seen.add(x)]
        id_glo_loc = store_global_ids
        id_glo_loc.sort()
        # now node_ids[i] means ==>  i+1: local id in child(this level) module, node_ids[i]: global id

        # get global node ids
        #node_global_ids = ele_obj.id_nodes
        #node_global_ids.sort()
        #node_local_ids = []
        #for j, id_glob in enumerate(node_global_ids):
        #    node_local_ids.append(id_glo_loc.index(id_glob)+1)

        #print("node_ids glo loc", node_global_ids, node_local_ids)

        one_module = Module(1)
        #one_module.add_node_multi_temp(node_local_ids)
        one_module.set_global_node_id_list_for_tree(id_glo_loc)
        one_module.set_local_node_id_list(id_glo_loc)

        for i, node_id_glob in enumerate(id_glo_loc):
            one_node = Node(i+1)
            one_node.set_module_id(1)
            nodes.append(one_node)
            #one_module.add_node_temp(node_count)
            #node_count += 1

        #return nodes, one_module
        #print("module check", one_module)
        return one_module

    def subtree2modulelist(self, parent_id):
        from module import Module
        from node   import Node
        #print("ele id ", parent_id, "will be converted to modules id")

        nodes = []
        modules = []
        parent_tree_ele = self.__modules_tree[parent_id]
        child_tree_ele  = self.get_element_object(parent_tree_ele.id_child)

        #node_count = 1

        # store global node ids then create local_id <-> global_id list
        store_glob_ids = []
        for i, tree_ele in enumerate(child_tree_ele):
            node_global_ids = tree_ele.id_nodes
            if len(node_global_ids) == 0:
                print("tree element with no node member was tried to be converted to module object")
                sys.exit(1)
            store_glob_ids.extend(node_global_ids)

        # eliminate duplicated ids
        seen = set()
        id_glo_loc = [x for x in store_glob_ids if x not in seen and not seen.add(x)]
        id_glo_loc.sort()
        # now node_ids[i] means ==>  i+1: local id in child(this level) module, node_ids[i]: global id


        for i, tree_ele in enumerate(child_tree_ele):
            # get global node ids
            node_global_ids = tree_ele.id_nodes
            node_global_ids.sort()
            node_local_ids = []
            for j, id_glob in enumerate(node_global_ids):
                node_local_ids.append(id_glo_loc.index(id_glob)+1)

            one_module = Module(i+1)
            #one_module.add_node_multi_temp(node_local_ids)
            one_module.set_global_node_id_list_for_tree(node_global_ids)
            one_module.set_local_node_id_list(id_glo_loc)   

            for j, node_id_glob in enumerate(node_global_ids):
                one_node = Node(id_glo_loc.index(node_id_glob)+1)
                one_node.set_module_id(i+1)
                nodes.append(one_node)
                #one_module.add_node_temp(node_count)
                #node_count += 1

            modules.append(one_module)
        #print("nodes modules converted", nodes, "\n",modules)
        return nodes, modules

    def tree_draw_with_ete3(self, root_id, *ql_val):
        """ this function draw a tree state on terminal screen by ete toolkit (ete3)
        """
        from ete3 import Tree

        root_ele = self.__modules_tree[root_id]
        # convert __modules_tree list to ete3 tree compatible string
        str_for_ete3 = self.dfs_for_ete3(root_ele)

        str_final = str_for_ete3 +';'

        #print("check str", str_final)
        # draw
        t = Tree(str_final, format=1)
        #print (t.get_ascii(show_internal=True))
        tree_strings = t.get_ascii(show_internal=True)

        #count "\n" in tree_strings
        num_line = tree_strings.count('\n') + 1
        
        ql_str = "\nql value: " + str(ql_val)

        erase_line = ""
        for i in range(self.num_str_lines):
            erase_line += "\r"

        str_indicate = erase_line + ql_str + tree_strings
        #print(erase_line,ql_str,tree_strings)
        print(str_indicate)
        #sys.stdout.write("%s" % (str_indicate))
        #sys.stdout.flush()

        self.num_str_lines = num_line

    def dfs_for_ete3(self, ele):
        """ this function invoke Depth-first tree search
            to generate a string for ete3 tree ascii drawing
        """

        # check if the children has no grand child
        go_deeper_count = 0

        goback_string = '('

        for i, child in enumerate(ele.id_child):
            #print("think about", child)
            target = self.__modules_tree[child]
            if len(target.id_child) != 0:
                # gather the child id ex. A,B
                child_string = self.dfs_for_ete3(target)
                # add the parent id   ex. A,B -> (A,B)C
                string_to_add = child_string + str(child)
                if i != 0:
                    goback_string += ','
                goback_string += string_to_add
                go_deeper_count += 1
            else:
                if i != 0:
                    goback_string += ','
                node_members = ''
                for j, node_id in enumerate(target.id_nodes):
                    if j != 0:
                        node_members += '..'
                    node_members += str(node_id)  
                goback_string += str(child) + '--node member--' + node_members

        if go_deeper_count == 0:
            # there was no child in this level
            pass
 
        goback_string += ')'
        return goback_string

    def __repr__(self):
        return "state of tree: \n %s"  % self.__modules_tree

class ele:
    """ store the necessary information of each node/element/module of the tree
        
    Tree properties::
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


    Flow(link) properties::
        exit_flow  # sum of out-going links
        enter_flow # sum of out-coming links
        total_flow # sum of internal/out-going/out-coming links

    """
    def __init__(self, id_this, id_parent=-1, id_next=-1, id_previous=-1):
        self.id_this = id_this
        self.id_parent   = id_parent
        self.id_child    = [] # childs will be added when there are generated
        self.id_next     = id_next
        self.id_previous = id_previous

        self.id_nodes = []

        self.exit_link     = 0 
        self.enter_link    = 0
        self.internal_link = 0
        #self.total_flow    = 0
        self.sum_pa        = 0 

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

    def set_exit_link(self, val):
        self.exit_link = val
    def set_enter_link(self, val):
        self.enter_link = val
    #def set_total_flow(self, val):
    #    self.total_flow = val
    def set_internal_link(self, val):
        self.internal_link = val
    def set_sum_pa(self, val):
        self.sum_pa = val

    def is_leaf(self):
        if len(self.id_nodes) == 0:
            return False
        else:
            return True

    def __repr__(self):
        """definition for when this class object is printed
        """
        
        return "this: %s, parent: %s child: %s, next: %s, previous: %s, node members: %s \n" % (self.id_this, self.id_parent, self.id_child, self.id_next, self.id_previous, self.id_nodes)

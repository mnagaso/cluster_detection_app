#!/usr/bin/env python
# coding:utf-8

''' Module class
'''

class Module:

    def __init__(self, module_id):
        self.__module_id = module_id    # local module id
        self.__node_id_list = []        # local  ids of member nodes
        self.__global_node_id_list = [] # global ids of member nodes

        # sum of out-going/in-coming/internal link weights
        self.exit_link = 0. 
        self.enter_link = 0.
        self.internal_link = 0.
        #self.total_link = 0. 
        self.sum_pa = 0.

    def add_node(self, node):
        """ add one node to this module """
        node.set_module_id(self.__module_id)
        self.__node_id_list.append(node.get_id())

    def add_node_multi(self, node_list):
        """ add multiple nodes to a module """
        for i, node_id in enumerate(node_list):
            self.add_node(node_id)

    def add_node_temp(self, node_id):
        """ add node method for inside of the loop
            add one node to this module """
        self.__node_id_list.append(node_id)

    def add_node_multi_temp(self, node_list):
        """ add node multi method for inside of the loop
            add multiple nodes to a module """
        for i, node_id in enumerate(node_list):
            self.add_node_temp(node_id)

    def remove_node(self, node):
        """ remove one node from this module """
        try:
            self.__node_id_list = [ node_id for node_id in self.__node_id_list if node_id != node]
        except ValueError:
            print("trying to remove a node not being exist in this module")

    def remove_node_multi(self, node_list):
        """ remove multiple nodes at the same time  """
        for i, node_id in enumerate(node_list):
            self.remove_node(node_id)

    def remove_node_all(self):
        del self.__node_id_list[:]
 
    def reset_module_id(self, new_id):
        """ reset module id """
        self.__module_id = new_id

    def sort_node_id_list(self):
        """ sort the node id list in this module
        """
        self.__node_id_list = sorted(self.__node_id_list, key=int)

    def get_num_nodes(self):
        """return the number of nodes belonging to this module"""
        return len(self.__node_id_list)

    def get_node_list(self):
        """return node list"""
        return tuple(self.__node_id_list)

    def set_global_node_id_list(self, id_glo_loc):
        """ set a global node id list"""

        for i, node in enumerate(self.__node_id_list):
            self.__global_node_id_list.append(id_glo_loc[node-1])

        self.__global_node_id_list.sort()

    def set_local_node_id_list(self, id_glo_loc):
        """ set a local node id list"""
        del self.__node_id_list[:]
        
        for id_loc, id_glo_in_list in enumerate(id_glo_loc):
            for j, id_glo_in_obj in enumerate(self.__global_node_id_list):
                if id_glo_in_list == id_glo_in_obj:
                    self.__node_id_list.append(id_loc+1)

        self.__node_id_list.sort()

    def set_global_node_id_list_for_tree(self, ids):
       """ set a global node id list"""

       for i, node in enumerate(ids):
           self.__global_node_id_list.append(node)

    def set_links_and_pa(self, exit_link, enter_link, inter_link, pa):
        """ set link values """
        self.exit_link     = exit_link
        self.enter_link    = enter_link
        self.internal_link = inter_link
        self.sum_pa        = pa

    def get_global_node_id_list(self):
        """ return a list of global node ids"""
        
        if len(self.__global_node_id_list) == 0: # works only for firstly divided modules.
            return self.__node_id_list
        else:
            return self.__global_node_id_list
    
    def get_neighbor_list(self, w, module_list, node_id=-1):
        """ return module list which has links with external modules """
        if node_id != -1:
            # this function returns module list which has links with one node_id
            nodes_this = [node_id]
        else:
            # this function returns module list which has links with this module
            nodes_this = self.__node_id_list
        
        neighbor_module_list = []

        list_neighbors = []
        uniq_list_neighbors = []

        for i, node_id in enumerate(nodes_this):
            w_to = w[:,node_id-1].todense().A1
            w_from = w[node_id-1,:].todense().A1
            del list_neighbors[:]
            del uniq_list_neighbors[:]

            #search links
            for i, w_node in enumerate(w_to):
                if w_node != 0:
                    # find module id from w
                    # id count starts 1 but stored at 0-th element of the array
                    list_neighbors.append(i+1)
            for i, w_node in enumerate(w_from):
                if w_node != 0:
                    # find module id from w
                    # id count starts 1 but stored at 0-th element of the array
                    list_neighbors.append(i+1)
            # check duplicate items
            seen = set()
            uniq_list_neighbors = [x for x in list_neighbors if x not in seen and not seen.add(x)]

            neighbor_module_list.extend(self.nodelist2modulelist( uniq_list_neighbors, module_list))

        # check duplicate items
        seen = set()
        uniq_module_neighbors = [x for x in neighbor_module_list if x not in seen and not seen.add(x)]
        # erase the modul_id of this
        uniq_module_neighbors = [x for x in uniq_module_neighbors if x != self.__module_id]

        return uniq_module_neighbors


    def nodelist2modulelist(self, node_list, module_list):
        """ this function returns module ids from node ids
        """
        module_list_pre = []
        for i, node_id in enumerate(node_list):
            for j, module in enumerate(module_list):
                member_nodes = list(module.get_node_list())
                if node_id in member_nodes:
                    module_list_pre.append(module.get_module_id())


        # eliminate duplicated ids
        seen = set()
        module_list_final = [x for x in module_list_pre if x not in seen and not seen.add(x)]
        module_list_final.sort()

        return module_list_final

    def get_module_id(self):
        """ return id of this module """
        return self.__module_id
 
    def __repr__(self):
        """ called when this class object is printed
        """
        node_ids = self.__node_id_list
        node_ids_glob = self.__global_node_id_list
        
        return "module id %s, including node(local id) %s, node(global id) %s \n" % (self.__module_id, node_ids, node_ids_glob)

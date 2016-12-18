#!/usr/bin/env python
# coding:utf-8

''' Module class
'''

class Module:
    __module_id = -1 # module ID
    __belongs_to_module_id = -1 # 属するモジュールのID

    def __init__(self, module_id):
        # print("generate module : " + str(module_id))
        self.__module_id = module_id
        self.__node_id_list = []

    def add_node(self, node):
        """ add one node to this module """
        node.set_module_id(self.__module_id)
        self.__node_id_list.append(node.get_id())
        #self.__node_id_list = node.get_id()

    def add_node_multi(self, node_list):
        """ add multiple nodes to a module """
        for i, node_id in enumerate(node_list):
            self.add_node(node_id)

    def add_node_temp(self, node_id):
        """ add node method for inside of the loop
            add one node to this module """
        #node.set_module_id(self.__module_id)
        #self.__new_node_id_list.append(node.get_id())
        self.__node_id_list.append(node_id)
        #self.__node_id_list = node.get_id()

    def add_node_multi_temp(self, node_list):
        """ add node multi method for inside of the loop
            add multiple nodes to a module """
        for i, node_id in enumerate(node_list):
            self.add_node_temp(node_id)


    def remove_node(self, node):
        """ remove one node from this module """
        #node.set_module_id(-1)
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

    def merge_node_id_lists(self):
        """ merge node_id_list and new_node_id_list """
        self.__node_id_list.append(__new_node_id_list)
        for i, node_id in enumerate(__new_node_id_list):
            node
        del self.__new_node_id_list

    def reset_module_id(self, new_id):
        """ reset module id """
        self.__module_id = new_id

    def sort_node_id_list(self):
        """ sort the node id list in this module
        """
        self.__node_id_list = sorted(self.__node_id_list, key=int)
        #print("sorted", self.__node_id_list)

    def get_num_nodes(self):
        """return the number of nodes belonging to this module"""
        return len(self.__node_id_list)

    def get_node_list(self):
        """return node list"""
        return tuple(self.__node_id_list)

    def get_neighbor_list(self, w_oneline, nodes):
        """ return node(module) list directrly linked from this module"""
        list_neighbors = []
        # search links
        for i, w_node in enumerate(w_oneline):
            if w_node != 0:
                # find module id from node id
                module_id = nodes[i].get_module_id()
                # id count starts 1 but stored at 0-th element of the array
                list_neighbors.append(module_id) 

        # check duplicate items
        seen = set()
        uniq_list_neighbors = [x for x in list_neighbors if x not in seen and not seen.add(x)]

        print ("id ", self.__module_id, "has neighboring module id ", uniq_list_neighbors)
        return uniq_list_neighbors

    def get_module_id(self):
        """ return id of this module """
        return self.__module_id

    def __repr__(self):
        """definition for when this class object is printed
        """
        #return "%s" % (self.__module_id)
        #return "module id %s" % (self.__module_id)
        return "module id %s, including node %s \n" % (self.__module_id, self.__node_id_list)

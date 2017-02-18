#!/usr/bin/env python

'''

export results to csv file

'''

import csv, numpy
import config as cf
import json_export as jex

def export_csv( p_a, cluster_obj):
    """ export clustring result in csv tree format 
    """

    modules  = cluster_obj.get_modules()
    nodes    = cluster_obj.get_nodes()
    tree_obj = cluster_obj.get_tree()

    # get node names
    node_names = jex.get_name_list()

    out_filename = cf.outfile_path
    f = open(out_filename, 'w')
    writer = csv.writer(f, lineterminator='\n')

    # first line: description about used method
    str_first = '#quality_method '
    str_first += str(cf.quality_method) + ' '
    str_first += 'division_type ' + str(cf.division_type) + ' '
    str_first += 'teleport_type ' + str(cf.teleport_type) + ' '
    str_first += 'modified_louvain ' + str(cf.modified_louvain) + ' '
    if cf.modified_louvain == True or cf.division_type == 2:
        str_first += 'num_trial ' + str(cf.num_trial) + ' '
    str_first += 'seed_value ' + str(cf.seed_var)

    writer.writerow(str_first.split())

    # second line: quality value
    str_second = "# final quality value: " + str(cluster_obj.ql_final)
    writer.writerow([str_second])

    # then 1,mod_id,submod_id(or local node id for two level),p_a,node name, global node id
    if cf.division_type == 1: # two level
        # sort modules by node id
        jex.sort_module_ids(nodes, modules)

        for i, mod in enumerate(modules):
            node_member = list(mod.get_node_list())
            for j, node_id in enumerate(node_member):
                global_id = node_id
                local_id  = j+1
                one_line = []
                one_line.append(1) # add 1 to adjust the tree format of infomap
                one_line.append(mod.get_module_id())
                one_line.append(local_id)
                one_line.append(p_a[global_id-1])
                one_line.append(node_names[global_id-1])
                one_line.append(global_id)
            
                writer.writerow(one_line)

    else: # hierarchical  
        pass


    f.close()
#!/usr/bin/env python

'''

convert clustered data to json file
json format is same as gephi json format

'''

import csv
import sys
import json
import numpy as np

import config as cf

def json_out(links, cluster_obj):
    """
        convert nodes/modules object list to json file
    """
   
    list_nodes   = cluster_obj.get_nodes()
    list_modules = cluster_obj.get_modules()
    tree_obj     = cluster_obj.get_tree()

    if cf.division_type == 1: # two level
        sort_module_ids(list_nodes,list_modules)
        # read node name list file
        names = get_name_list()
        # make a dict for jsonize
        dict_pre_jsonize = construct_dict(links, names, list_nodes, list_modules)
        #print("hi jason",dict_pre_jsonize)

    elif cf.division_type == 2: # hierarchical
        # generate 

        # read node name list file
        names = get_name_list()

        dict_pre_jsonize = construct_dict(links, names, tree_obj)


    # output json file
    outfolder = "./vis_html/"

    if cf.quality_method == 1: # out result by map equation
        outfile_header = "result_mapequation.json"
    elif cf.quality_method == 2: # out result by modularity
        outfile_header = "result_modularity.json"

    outfile = outfolder + outfile_header

    f = open(outfile, "w")
    json.dump(dict_pre_jsonize, f, sort_keys=True, cls=numpy_object_to_json_compatible, ensure_ascii=False)

def construct_dict_from_tree(links, names, tree_obj):
    pre_json = {}

    # prepare edges
    edges = []
    nonzero_row, nonzero_col = links.nonzero()
    #print (row,col)
    for i in range(len(nonzero_row)):
        one_edge = {
                "source": nonzero_col[i],
                "target": nonzero_row[i],
                "id": i,
                "attributes": {
                    "Weight": links[nonzero_row[i],nonzero_col[i]]
                    },
                "color": "rgb(229,164,67)",
                "size": 1
        }
        edges.append(one_edge)

    pre_json["edges"] = edges

    # prepare nodes
    nodes = []
    for n, name in enumerate(names):
        one_node = {
                "label": name,
                "x": 1,
                "y": 1,
                "id": n,
                #"attributes": {
                #                    "Module_id": list_nodes[n].get_module_id()
                #                },
                "color": "rgb(0,0,255)",
                "size": 1
        }

        nodes.append(one_node)
    
    pre_json["nodes"] = nodes

    return pre_jso

def construct_dict(links, names, list_nodes, list_modules):
    pre_json = {}

    # prepare edges
    edges = []
    nonzero_row, nonzero_col = links.nonzero()
    #print (row,col)
    for i in range(len(nonzero_row)):
        one_edge = {
                "source": nonzero_col[i],
                "target": nonzero_row[i],
                "id": i,
                "attributes": {
                    "Weight": links[nonzero_row[i],nonzero_col[i]]
                    },
                "color": "rgb(229,164,67)",
                "size": 1
        }
        edges.append(one_edge)

    pre_json["edges"] = edges

    # prepare nodes
    nodes = []
    for n, name in enumerate(names):
        one_node = {
                "label": name,
                "x": 1,
                "y": 1,
                "id": n,
                "attributes": {
                                    "Module_id": list_nodes[n].get_module_id()
                                },
                "color": "rgb(0,0,255)",
                "size": 1
        }

        nodes.append(one_node)
    
    pre_json["nodes"] = nodes

    return pre_json

def get_name_list():
    # read a node id-name list (***_vertices.csv)
    #vertices_file_path = 'data/n24_vertices.csv'
    infile_path = cf.vertices_file_path
    print(infile_path)

    try:
        f = open(infile_path)
        csv_reader = csv.reader(f)
    except:
        print ("vertices file read error")
        print ("please check the filepath for vertices_file_path in config.py")
        sys.exit(1)

    nodes = sum(1 for row in csv_reader)

    f.seek(0) # reset the position to be read

    names = []

    for line in csv_reader:
        node_id, name = map(np.str, line)
        names.append(name)

    names = np.array(names) # convert it to numpy array
    
    return names

def sort_module_ids(node_list, module_list):
    """
        this function modifies module ids
        according to node ids belonging to a module
    """
    total_num_modules = len(module_list)
    youngest_ids = []
    for i, obj_mod in enumerate(module_list):
        # read youngest ids in each module
        youngest_ids.append(min(obj_mod.get_global_node_id_list()))

    print(youngest_ids)
    # reorder
    new_order = sorted(range(len(youngest_ids)), key=lambda i: youngest_ids[i])
    print(new_order)
 
    for i, target in enumerate(new_order):
        new_id = i+1
        module_list[target].reset_module_id(new_id)
        for j, node_id in enumerate(module_list[target].get_global_node_id_list()):
            node_list[node_id-1].set_module_id(new_id)

    # sort orders of modules by module ids
    module_list.sort(key=lambda x: x.get_module_id(), reverse=False)           


class numpy_object_to_json_compatible(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

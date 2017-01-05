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

def json_out(links ,list_nodes, list_modules):
    """
        convert nodes/modules object list to json file
    """

    print("list_moules", list_modules)

    # get name list
    names = get_name_list()
    print(names)

    dict_pre_jsonize = construct_dict(links, names, list_nodes, list_modules)
    #print("hi jason",dict_pre_jsonize)

    # output json file
    f = open("./vis_html/outtest.json", "w")
    json.dump(dict_pre_jsonize, f, sort_keys=True, cls=numpy_object_to_json_compatible
, ensure_ascii=False)

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
                                    "Module_id": list_nodes[n-1].get_module_id()
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

#
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

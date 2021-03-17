
import json
from os import walk
import string
import pprint
from collections import OrderedDict
from graph import *

# load filenames from metabolic-pathways folder
pathways = []
for (dirpath, dirnames, filenames) in walk("metabolic-pathways/"):
    pathways.extend(filenames)
    break

level = -1
letter = 0
dictionary = {}
def add_to_dictionary(path):
    for node in path:
        if not node in dictionary:
            global letter, level
            if letter % 26 == 0:
                level = level + 1            
            dictionary[node] = string.ascii_uppercase[letter % 26] + str(level)
            letter = letter + 1

# return renamed path from dictonary
def renamed_path(path):
    renamed = []
    for node in path:
        renamed.append(dictionary[node])
    return renamed

# load json to Ordered Dictonary, from metabolic-pathways folder
def to_dict_from_json(route):
    dict = {}
    with open('metabolic-pathways/' + pathways[route]) as data_file:    
        dict = json.load(data_file, object_pairs_hook=OrderedDict)
    return dict

def show_dictionary():
    print
    print "Show dictionary (1) yes or (0) no "
    show = int(input("#show: "))
    if show:
        inv_dictionary = {v: k for k, v in dictionary.iteritems()}
        pprint.pprint(inv_dictionary)         

def identify_equality(graph0, graph1, detail):
    for node in graph0.get_nodes():
        for edge in node.get_edges():
            value1 = node.get_value()
            value2 = edge.get_value()
            if graph1.exists_edge(str(value1), str(value2)):
                if detail:
                    print("\t" + str(value1) + " -> " + str(value2))
                else:
                    if value1 in dictionary and value2 in dictionary:
                        print("\t" + str(dictionary[value1]) + " -> " + str(dictionary[value2]))

def identify_differences(graph0, graph1, detail):
    for node in graph0.get_nodes():
        for edge in node.get_edges():
            value1 = node.get_value()
            value2 = edge.get_value()
            if not graph1.exists_edge(str(value1), str(value2)):
                if detail:
                    print("\t" + str(value1) + " -> " + str(value2))
                else:
                    if value1 in dictionary and value2 in dictionary:
                        print("\t" + str(dictionary[value1]) + " -> " + str(dictionary[value2]))           

if __name__ == '__main__':
    print "Available pathways at metabolic-pathways folder"
    for route in range(len(pathways)):
        print("#" + str(route) + ": " + pathways[route])
    print

    print "Enter pathway number"
    pathway0 = int(input("#pathway0: "))
    pathway1 = int(input("#pathway1: "))
    print

    # pathway2 processing
    dict = to_dict_from_json(pathway0)
    graph0 = to_graph_from_dict(dict)

    # pathway1 processing
    dict = to_dict_from_json(pathway1)
    graph1 = to_graph_from_dict(dict)

    #bfs0 = graph0.breadth_first_path()
    bfs0 = graph0.depth_first_path()
    add_to_dictionary(bfs0)
    #bfs1 = graph1.breadth_first_path()
    bfs1 = graph1.depth_first_path()
    add_to_dictionary(bfs1)   

    print "Detail level (1) full or (0) low "
    detail = int(input("#detail: "))    
    print
    #print "Breadth First Paths"
    print "Depth First Paths"
    if detail:     
        print pathways[pathway0]
        pprint.pprint(bfs0)
        print
        print pathways[pathway1]
        pprint.pprint(bfs1)
    else:
        print pathways[pathway0]
        print renamed_path(bfs0)
        print
        print pathways[pathway1]
        print renamed_path(bfs1)

    print
    print "Equality"
    identify_equality(graph0, graph1, detail)
    print
    print "Differences Identified"
    print pathways[pathway0]
    identify_differences(graph0, graph1, detail)
    print
    print pathways[pathway1]
    identify_differences(graph1, graph0, detail)
    print  
    
    show_dictionary()

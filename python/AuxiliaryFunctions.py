import base64
import sys
import os
import string
from graphviz import Digraph
# from local_alignment import local_alignment
# from global_alignment import needleman_wunsch, setValues
# from semiglobal_alignment import semiglobal_alignment
from graph import *
from Bio import pairwise2 as pw

# Global variables
level = -1
letter = 0
LOW = 0
FULL = 1
dictionary = {}


def generateGraphImage(imagesFolderPath, XMLFileName, pathwayCompoundsGraph):
    """
    Function that generates an image of a graph in a specified folder
    :param imagesFolderPath: Folder where the image is going to be stored
    :param XMLFileName: File of the XML
    :param pathwayCompoundsGraph: Graph to be converted to an image
    :return:
    """
    g = Digraph('G', format='png')
    # if(horizontalGraph):
    #    g.attr(rankdir='LR')
    for k in pathwayCompoundsGraph.keys():
        g.node(k)
        for v in pathwayCompoundsGraph[k]:
            g.edge(k, v)
    g.render(imagesFolderPath + XMLFileName)


def addToDictionary(path):
    for node in path:
        if not node in dictionary:
            global letter, level
            if letter % 26 == 0:
                level += 1
            dictionary[node] = string.ascii_uppercase[letter % 26] + str(level)
            letter += 1


def showDictionary():
    inv_dictionary = {v: k for k, v in dictionary.items()}
    sorted_dict = sorted(inv_dictionary.items(), key=operator.itemgetter(0))
    for tuple in sorted_dict:
        print(str(tuple[0]) + "->" + str(tuple[1]))


def renamedPath(path):
    return path  # Todo: decide between using or not the renamed path
    renamed = []
    for node in path:
        renamed.append(dictionary[node])
    return renamed


def identify_equality(graph1, graph2, detail):
    outputList = []
    equality = False
    for node in graph1.get_nodes():
        for edge in node.get_edges():
            value1 = node.get_value()
            value2 = edge.get_value()
            if value1 != '*':
                if graph2.exists_edge(str(value1), str(value2)):
                    equality = True
                    outputList.append(str(value1) + " -> " + str(value2))
    return outputList


def identify_differences(graph1, graph2, detail):
    outputList = []
    differences = False
    for node in graph1.get_nodes():
        for edge in node.get_edges():
            value1 = node.get_value()
            value2 = edge.get_value()
            if value1 != '*':
                if not graph2.exists_edge(str(value1), str(value2)):
                    differences = True
                    outputList.append(str(value1) + " -> " + str(value2))
    return outputList


def needleman_wunsch(seq1, seq2, match, missmatch, gap):
    alns = pw.align.globalms(seq1, seq2, int(match), int(missmatch), int(gap), int(gap), gap_char=['-'],
                             one_alignment_only=True)
    if not alns:
        return [[], [], 0]
    alns = alns[0]
    return [alns[0][alns[3]:alns[4]], alns[1][alns[3]:alns[4]], alns[2]]


def semiglobal_alignment(seq1, seq2, match, missmatch, gap):
    alns = pw.align.globalms(seq1, seq2, int(match), int(missmatch), int(gap), int(gap), penalize_end_gaps=False,
                             gap_char=['-'],
                             one_alignment_only=True)
    if not alns:
        return [[], [], 0]
    alns = alns[0]
    return [alns[0][alns[3]:alns[4]], alns[1][alns[3]:alns[4]], alns[2]]


def local_alignment(seq1, seq2, match, missmatch, gap):
    alns = pw.align.localms(seq1, seq2, int(match), int(missmatch), int(gap), int(gap), gap_char=['-'],
    one_alignment_only = True)
    if not alns:
        return [[], [], 0]
    alns = alns[0]
    return [alns[0][alns[3]:alns[4]], alns[1][alns[3]:alns[4]], alns[2]]

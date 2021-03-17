import json
import operator
from os import walk
import sys
import datetime
import string
import pprint
from collections import OrderedDict

# KGML to JSON
from kgml2Json import SimpleKGML

# Graph
from graph import *

# Aligment Algorithms
from local_alignment import local_alignment
from global_alignment import needleman_wunsch
from semiglobal_alignment import semiglobal_alignment

level = -1
letter = 0
LOW = 0
FULL = 1
dictionary = {}



horizontal_graph = False # Generate horizontal image
file = ""

params = True #Utilizar parametros / Se utiliza en algoritmo 1.4
if(params):
	start0 = 0  #Numero de nodo a iniciar grafo 1
	end0 = 4	#Numero de nodo a finalizar 1
	start1 = 0	#Numero de nodo a iniciar grafo 2
	end1 = 10 	#Numero de nodo a finalizar 2
	n = 2		#Recursion en el grafo en busca de ruta

#Convert a path to a dictionary
def path2Dic(path):
	pDic={}
	for i in range(len(path)-1):
		pDic[path[i].get_value()] = [path[i+1].get_value()]
	return pDic


def generate_graph(dict):
	from graphviz import Digraph
	g = Digraph('G', format='png')
	if(horizontal_graph):
		g.attr(rankdir='LR')
	for k in dict.keys():
		g.node(k)
		for v in dict[k]:
			g.edge(k, v)
	g.render('g')
	import base64

	with open("g.png", "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read())
	return encoded_string


def redirectOut(num):
	global file
	filename   = datetime.datetime.now().strftime("generated/%Y%m%d%H%M%S-v"+str(num)+".html")
	file = open(filename, 'w')
	sys.stdout = file 


def restoreOut():
	global file
	sys.stdout = sys.__stdout__
	file.close()


def reset_dictionary():
	global dictionary,letter,level
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

# return renamed path from dictIonary
def renamed_path(path):
	renamed = []
	for node in path:
		renamed.append(dictionary[node])
	return renamed

def show_dictionary():
	print("<p>" , "Dictionary", "</p>")
	inv_dictionary = {v: k for k, v in dictionary.iteritems()}
	sorted_dict = sorted(inv_dictionary.items(), key=operator.itemgetter(0))
	for tuple in sorted_dict:
		print("<a>" + str(tuple[0]) + " -> " + str(tuple[1]) + "</a><br>")

def identify_equality(graph0, graph1, detail):
	equality = False
	for node in graph0.get_nodes():
		for edge in node.get_edges():
			value1 = node.get_value()
			value2 = edge.get_value()
			if value1 != '*':
				if graph1.exists_edge(str(value1), str(value2)):
					equality = True
					if detail:
						print("<p class='indentify'>" + str(value1) + " -> " + str(value2) + "</p>")
					else:
						if value1 in dictionary and value2 in dictionary:
							print("<p class='indentify'>" + str(dictionary[value1]) + " -> " + str(dictionary[value2]) + "</p>")
	if not equality:
		print("<p>None Found</p>")

def identify_differences(graph0, graph1, detail):
	differences = False
	for node in graph0.get_nodes():
		for edge in node.get_edges():
			value1 = node.get_value()
			value2 = edge.get_value()
			if value1 != '*':
				if not graph1.exists_edge(str(value1), str(value2)):
					differences = True
					if detail:
						print("<p class='indentify'>" + str(value1) + " -> " + str(value2) + "</p>")
					else:
						if value1 in dictionary and value2 in dictionary:
							print("<p class='indentify'>" + str(dictionary[value1]) + " -> " + str(dictionary[value2]) + "</p>")
	if not differences:
		print("<p>None Found</p>"						)


#Algorithm 1
def metabolic_pathways_HTML_alg1(pathway0, pathway1):
	redirectOut(1)
	# graph creation
	g1 = generate_graph(pathway0)
	g2 = generate_graph(pathway1)
	graph0 = to_graph_from_dict(pathway0)
	graph1 = to_graph_from_dict(pathway1)

	bft0 = graph0.breadth_first_traversal()
	dft0 = graph0.depth_first_traversal() 
	add_to_dictionary(bft0)
	add_to_dictionary(dft0)
	bft1 = graph1.breadth_first_traversal()
	dft1 = graph1.depth_first_traversal()
	add_to_dictionary(bft1)
	add_to_dictionary(dft1)

	# Low Detail Output
	globNeed = [needleman_wunsch(renamed_path(bft0), renamed_path(bft1)),needleman_wunsch(renamed_path(dft0), renamed_path(dft1))]
	localAlg = [local_alignment(renamed_path(bft0), renamed_path(bft1)),local_alignment(renamed_path(dft0), renamed_path(dft1))]
	SemilocalAlg = [semiglobal_alignment(renamed_path(bft0), renamed_path(bft1)),semiglobal_alignment(renamed_path(dft0), renamed_path(dft1))]

	redirectOut(1)
	print("<h4>Alignment Algorithms 1</h4>")
	print("<h4>Full Detail Output</h4>")
	print("<p>Breadth First Traversal (BFT)</p>")
	print("<p class='pathway'>Pathway 1: ", ' '.join(bft0), "</p>")
	print("<p class='pathway'>Pathway 2: ", ' '.join(bft1), "</p>")
	print('<br>')
	print("<p>Depth First Traversal (DFT)</p>")
	print("<p class='pathway'>Pathway 1: ", ' '.join(dft0), "</p>")
	print("<p class='pathway'>Pathway 2: ", ' '.join(dft1), "</p>")
	print("<br>")
	print("<h3>G1 ------------------------------------------G2</h3>")
	print('<img src="data:image/png;base64,',g1,'" alt="Red dot" />')
	print('<img src="data:image/png;base64,',g2,'" alt="Red dot" />')
	show_dictionary()
	# Low Detail Output
	print("<h4>Low Detail Output</h4>")
	print("<p>Breadth First Search (BFT)</p>")
	print("<p class='pathway'>Pathway 1: ", ' '.join(renamed_path(bft0)), "</p>")
	print("<p class='pathway'>Pathway 2: ", ' '.join(renamed_path(bft1)), "</p>")
	print("<br>")
	print("<p>Depth First Search (DFT)</p>")
	print("<p class='pathway'>Pathway 1: ", ' '.join(renamed_path(dft0)), "</p>")
	print("<p class='pathway'>Pathway 2: ", ' '.join(renamed_path(dft1)), "</p>")
	print("<h4>Alignment Algorithms</h4>")
	print("<p>Global Alignment (BFT): ",globNeed[0][0] if globNeed[0][0]<=0 else "+"+str(globNeed[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in globNeed[0][1:]]))
	print("<p>Global Alignment (DFT): ",globNeed[1][0] if globNeed[1][0]<=0 else "+"+str(globNeed[1][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in globNeed[0][1:]]))
	print("<br>")
	print("<p>Local Alignment (BFT): ",localAlg[0][0] if localAlg[0][0]<=0 else "+"+str(localAlg[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in localAlg[0][1:]]))
	print("<p>Local Alignment (DFT): ",localAlg[0][0] if localAlg[0][0]<=0 else "+"+str(localAlg[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in localAlg[0][1:]]))
	print("<br>")
	print("<p>Semiglobal Alignment (DFT): ",SemilocalAlg[0][0] if SemilocalAlg[0][0]<=0 else "+"+str(SemilocalAlg[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in SemilocalAlg[0][1:]]))
	print("<p>Semiglobal Alignment (DFT): ",SemilocalAlg[0][0] if SemilocalAlg[0][0]<=0 else "+"+str(SemilocalAlg[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in SemilocalAlg[0][1:]]))
	print("<br>")
	print("<h4>Equality Identified</h4>")
	identify_equality(graph0, graph1, LOW)
	print("<br>")
	print("<h4>Differences Identified (from Pathway 1 to Pathway 2)</h4>")
	identify_differences(graph0, graph1, FULL)
	print("<br>")
	print("<h4>Differences Identified (from Pathway 2 to Pathway 1)</h4>")
	identify_differences(graph1, graph0, FULL)


#Algorithm 2
def metabolic_pathways_HTML_alg12(pathway0, pathway1):
	# graph creation
	g1 = generate_graph(pathway0)
	g2 = generate_graph(pathway1)
	graph0 = to_graph_from_dict(pathway0)
	graph1 = to_graph_from_dict(pathway1)

	
	print("Graph 1")
	for n,i in zip(range(len(graph0.get_nodes())),graph0.get_nodes()):
		print(n," - ",i.get_value()," -> ",[node.get_value() for node in i.get_edges()])
	start0 = input("Start Node Graph 1: ")
	print("")

	print("Graph 2")
	for n,i in zip(range(len(graph1.get_nodes())),graph1.get_nodes()):
		print(n," - ",i.get_value()," -> ",[node.get_value() for node in i.get_edges()])

	start1 = (input("Start Node Graph 2: "))

	bft0 = graph0.breadth_first_traversal(start0)
	dft0 = graph0.depth_first_traversal(start0) 
	add_to_dictionary(bft0)
	add_to_dictionary(dft0)
	bft1 = graph1.breadth_first_traversal(start1)
	dft1 = graph1.depth_first_traversal(start1)
	add_to_dictionary(bft1)
	add_to_dictionary(dft1)


	# Low Detail Output
	globNeed = [needleman_wunsch(renamed_path(bft0), renamed_path(bft1)),needleman_wunsch(renamed_path(dft0), renamed_path(dft1))]
	localAlg = [local_alignment(renamed_path(bft0), renamed_path(bft1)),local_alignment(renamed_path(dft0), renamed_path(dft1))]
	SemilocalAlg = [semiglobal_alignment(renamed_path(bft0), renamed_path(bft1)),semiglobal_alignment(renamed_path(dft0), renamed_path(dft1))]

	# Full Detail Output
	redirectOut(2)
	print("<h4>Full Detail Output</h4>")
	print("<p>Breadth First Traversal (BFT)</p>")
	print("<p class='pathway'>Pathway 1: ", ' '.join(bft0), "</p>")
	print("<p class='pathway'>Pathway 2: ", ' '.join(bft1), "</p>")
	print('<br>')
	print("<p>Depth First Traversal (DFT)</p>")
	print("<p class='pathway'>Pathway 1: ", ' '.join(dft0), "</p>")
	print("<p class='pathway'>Pathway 2: ", ' '.join(dft1), "</p>")
	print("<br>")
	print("<h3>G1 ------------------------------------------G2</h3>")
	print('<img src="data:image/png;base64,',g1,'" alt="Red dot" />')
	print('<img src="data:image/png;base64,',g2,'" alt="Red dot" />')
	show_dictionary()
	# Low Detail Output
	print("<h4>Low Detail Output</h4>")
	print("<p>Breadth First Search (BFT)</p>")
	print("<p class='pathway'>Pathway 1: ", ' '.join(renamed_path(bft0)), "</p>")
	print("<p class='pathway'>Pathway 2: ", ' '.join(renamed_path(bft1)), "</p>")
	print("<br>")
	print("<p>Depth First Search (DFT)</p>")
	print("<p class='pathway'>Pathway 1: ", ' '.join(renamed_path(dft0)), "</p>")
	print("<p class='pathway'>Pathway 2: ", ' '.join(renamed_path(dft1)), "</p>")
	print("<h4>Alignment Algorithms</h4>")
	print("<p>Global Alignment (BFT): ",globNeed[0][0] if globNeed[0][0]<=0 else "+"+str(globNeed[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in globNeed[0][1:]]))
	print("<p>Global Alignment (DFT): ",globNeed[1][0] if globNeed[1][0]<=0 else "+"+str(globNeed[1][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in globNeed[0][1:]]))
	print("<br>")
	print("<p>Local Alignment (BFT): ",localAlg[0][0] if localAlg[0][0]<=0 else "+"+str(localAlg[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in localAlg[0][1:]]))
	print("<p>Local Alignment (DFT): ",localAlg[0][0] if localAlg[0][0]<=0 else "+"+str(localAlg[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in localAlg[0][1:]]))
	print("<br>")
	print("<p>Semiglobal Alignment (DFT): ",SemilocalAlg[0][0] if SemilocalAlg[0][0]<=0 else "+"+str(SemilocalAlg[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in SemilocalAlg[0][1:]]))
	print("<p>Semiglobal Alignment (DFT): ",SemilocalAlg[0][0] if SemilocalAlg[0][0]<=0 else "+"+str(SemilocalAlg[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in SemilocalAlg[0][1:]]))
	print("<br>")
	print("<h4>Equality Identified</h4>")
	identify_equality(graph0, graph1, LOW)
	print("<br>")
	print("<h4>Differences Identified (from Pathway 1 to Pathway 2)</h4>")
	identify_differences(graph0, graph1, FULL)
	print("<br>")
	print("<h4>Differences Identified (from Pathway 2 to Pathway 1)</h4>")
	identify_differences(graph1, graph0, FULL)






#Algorithm 3
def metabolic_pathways_HTML_alg13(pathway0, pathway1):
	# graph creation
	g1 = generate_graph(pathway0)
	g2 = generate_graph(pathway1)
	graph0 = to_graph_from_dict(pathway0)
	graph1 = to_graph_from_dict(pathway1)

	
	print("Graph 1")
	for n,i in zip(range(len(graph0.get_nodes())),graph0.get_nodes()):
		print(n," - ",i.get_value()," -> ",[node.get_value() for node in i.get_edges()])
	start0 = input("Start Node Graph 1: ")
	end0 = input("End Node Graph 1: ")
	print("")

	print("Graph 2")
	for n,i in zip(range(len(graph1.get_nodes())),graph1.get_nodes()):
		print(n," - ",i.get_value()," -> ",[node.get_value() for node in i.get_edges()])

	start1 = (input("Start Node Graph 2: "))
	end1 = (input("End Node Graph 2: "))


	bft0 = graph0.breadth_first_traversal(start0,end0)
	dft0 = graph0.depth_first_traversal(start0,end0) 
	add_to_dictionary(bft0)
	add_to_dictionary(dft0)
	bft1 = graph1.breadth_first_traversal(start1,end1)
	dft1 = graph1.depth_first_traversal(start1,end1)
	add_to_dictionary(bft1)
	add_to_dictionary(dft1)


	# Low Detail Output
	globNeed = [needleman_wunsch(renamed_path(bft0), renamed_path(bft1)),needleman_wunsch(renamed_path(dft0), renamed_path(dft1))]
	localAlg = [local_alignment(renamed_path(bft0), renamed_path(bft1)),local_alignment(renamed_path(dft0), renamed_path(dft1))]
	SemilocalAlg = [semiglobal_alignment(renamed_path(bft0), renamed_path(bft1)),semiglobal_alignment(renamed_path(dft0), renamed_path(dft1))]
	
	# Full Detail Output
	redirectOut(3)
	print("<h4>Alignment Algorithms 1.3</h4>")
	print("<h4>Full Detail Output</h4>")
	print("<p>Breadth First Traversal (BFT)</p>")
	print("<p class='pathway'>Pathway 1: ", ' '.join(bft0), "</p>")
	print("<p class='pathway'>Pathway 2: ", ' '.join(bft1), "</p>")
	print('<br>')
	print("<p>Depth First Traversal (DFT)</p>")
	print("<p class='pathway'>Pathway 1: ", ' '.join(dft0), "</p>")
	print("<p class='pathway'>Pathway 2: ", ' '.join(dft1), "</p>")
	print("<br>")
	print("<h3>G1 ------------------------------------------G2</h3>")
	print('<img src="data:image/png;base64,',g1,'" alt="Red dot" />')
	print('<img src="data:image/png;base64,',g2,'" alt="Red dot" />')
	show_dictionary()
	# Low Detail Output
	print("<h4>Low Detail Output</h4>")
	print("<p>Breadth First Search (BFT)</p>")
	print("<p class='pathway'>Pathway 1: ", ' '.join(renamed_path(bft0)), "</p>")
	print("<p class='pathway'>Pathway 2: ", ' '.join(renamed_path(bft1)), "</p>")
	print("<br>")
	print("<p>Depth First Search (DFT)</p>")
	print("<p class='pathway'>Pathway 1: ", ' '.join(renamed_path(dft0)), "</p>")
	print("<p class='pathway'>Pathway 2: ", ' '.join(renamed_path(dft1)), "</p>")
	print("<h4>Alignment Algorithms</h4>")
	print("<p>Global Alignment (BFT): ",globNeed[0][0] if globNeed[0][0]<=0 else "+"+str(globNeed[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in globNeed[0][1:]]))
	print("<p>Global Alignment (DFT): ",globNeed[1][0] if globNeed[1][0]<=0 else "+"+str(globNeed[1][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in globNeed[0][1:]]))
	print("<br>")
	print("<p>Local Alignment (BFT): ",localAlg[0][0] if localAlg[0][0]<=0 else "+"+str(localAlg[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in localAlg[0][1:]]))
	print("<p>Local Alignment (DFT): ",localAlg[0][0] if localAlg[0][0]<=0 else "+"+str(localAlg[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in localAlg[0][1:]]))
	print("<br>")
	print("<p>Semiglobal Alignment (DFT): ",SemilocalAlg[0][0] if SemilocalAlg[0][0]<=0 else "+"+str(SemilocalAlg[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in SemilocalAlg[0][1:]]))
	print("<p>Semiglobal Alignment (DFT): ",SemilocalAlg[0][0] if SemilocalAlg[0][0]<=0 else "+"+str(SemilocalAlg[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in SemilocalAlg[0][1:]]))
	print("<br>")
	print("<h4>Equality Identified</h4>")
	identify_equality(graph0, graph1, LOW)
	print("<br>")
	print("<h4>Differences Identified (from Pathway 1 to Pathway 2)</h4>")
	identify_differences(graph0, graph1, FULL)
	print("<br>")
	print("<h4>Differences Identified (from Pathway 2 to Pathway 1)</h4>")
	identify_differences(graph1, graph0, FULL)




#Algorithm 4
def metabolic_pathways_HTML_alg14(pathway0, pathway1):
	global start0,start1,end0,end1,n
	# graph creation
	g1 = generate_graph(pathway0)
	g2 = generate_graph(pathway1)
	graph0 = to_graph_from_dict(pathway0)
	graph1 = to_graph_from_dict(pathway1)

	if(not params):
		print("Graph 1")
		for n,i in zip(range(len(graph0.get_nodes())),graph0.get_nodes()):
			print(n," - ",i.get_value(),"->",[node.get_value() for node in i.get_edges()])
		start0 = input("Start Node Graph 1: ")
		end0 = input("End Node Graph 1: ")
		print("")

		print("Graph 2")
		for n,i in zip(range(len(graph1.get_nodes())),graph1.get_nodes()):
			print(n," - ",i.get_value(),"->",[node.get_value() for node in i.get_edges()])

		start1 = (input("Start Node Graph 2: "))
		end1 = (input("End Node Graph 2: "))
		n = (input("Maximum cycles: "))
		paths0 = graph0.get_cyclic_paths(graph0[start0],graph0[end0], [], n)
		paths1 = graph1.get_cyclic_paths(graph1[start1],graph1[end1], [], n)
		
		if(len(paths0)==0):
			print("Not avaliable paths for graph 0")
			return
		if(len(paths1)==0):
			print("Not avaliable paths for graph 1")
			return


		"""
		print("Paths Graph 0:")
		for n,i in zip(range(len(paths0)),paths0):
			out = ""
			for node in i:
				out+=str(node.get_value())+"->"
			out = out[0:-2]
			print(n," - ",out)

		selected_Path0 = input("Select Path of graph 0: ")
		print("")
		print("Paths Graph 1:")
		for n,i in zip(range(len(paths1)),paths1):
			out = ""
			for node in i:
				out+=str(node.get_value())+"->"
			out = out[0:-2]
			print(n," - ",out)

		selected_Path1 = input("Select Path of graph 1: ")
		paths0 = [paths0[selected_Path0]]
		paths1 = [paths1[selected_Path1]]"""
	else:
		paths0 = graph0.get_cyclic_paths(graph0[start0],graph0[end0], [], n)
		paths1 = graph1.get_cyclic_paths(graph1[start1],graph1[end1], [], n)
	
	redirectOut(4)
	print("<h3>Algorithm 1.4</h3>")
	print("Paths Graph 1:<br>")
	for n,i in zip(range(len(paths0)),paths0):
			out = ""
			for node in i:
				out+=str(node.get_value())+"->"
			out = out[0:-2]
			print("".join([str(1),".",str(n)," - ",out]))
			print("<br>")

	print("<br>")
	print("Paths Graph 2:<br>")
	for n,i in zip(range(len(paths1)),paths1):
		out = ""
		for node in i:
			out+=str(node.get_value())+"->"
		out = out[0:-2]
		print("".join([str(2),".",str(n)," - ",out]))
		print("<br>")
	print("<h3>G1 ------------------------------------------G2</h3>")
	print('<img src="data:image/png;base64,',g1,'" alt="Red dot" />')
	print('<img src="data:image/png;base64,',g2,'" alt="Red dot" />')
	maxglobNeed = [[-100]]
	maxlocalAlg = [[-100]]
	maxSemiglobal=[[-100]]
	for p1 in range(len(paths0)):
		path0 = to_graph_from_dict(path2Dic(paths0[p1]))
		for p2 in range(len(paths1)):
			path1 = to_graph_from_dict(path2Dic(paths1[p2]))
			reset_dictionary()
			bft0 = path0.breadth_first_traversal()
			bft1 = path1.breadth_first_traversal()
			add_to_dictionary(bft0)
			add_to_dictionary(bft1)
			# Full Detail Output
			pathStr1 = "<p class='pathway'>Pathway 1."+str(p1)+": "+' '.join(bft0)+"</p>"
			pathStr2 = "<p class='pathway'>Pathway 2"+"."+str(p2)+": "+' '.join(bft1)+ "</p>"
			print("<h4>Full Detail Output - Algorithm 1.4</h4>")
			print(pathStr1)
			print(pathStr2)
			print("<br>")
			show_dictionary()
			# Low Detail Output
			print("<h4>Alignment Algorithms</h4>")
			globNeed = needleman_wunsch(renamed_path(bft0), renamed_path(bft1))
			localAlg = local_alignment(renamed_path(bft0), renamed_path(bft1))
			SemilocalAlg = semiglobal_alignment(renamed_path(bft0), renamed_path(bft1))
			if(globNeed[0]>maxglobNeed[0][0]):
				maxglobNeed = [globNeed,
				pathStr1,
				pathStr2
				]
			if(localAlg[0]>maxlocalAlg[0][0]):
				maxlocalAlg = [localAlg,
				pathStr1,
				pathStr2
				]
			if(SemilocalAlg[0]>maxSemiglobal[0][0]):
				maxSemiglobal = [SemilocalAlg,
				pathStr1,
				pathStr2
				]
			print("<p>Global Alignment (BFT): ",globNeed[0] if globNeed[0]<=0 else "+"+str(globNeed[0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in globNeed[1:]]))
			print("<br>")
			print("<p>Local Alignment (BFT): ",localAlg[0] if localAlg[0]<=0 else "+"+str(localAlg[0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in localAlg[1:]]))
			print("<br>")
			print("<p>Semiglobal Alignment (BFT): ",SemilocalAlg[0] if SemilocalAlg[0]<=0 else "+"+str(SemilocalAlg[0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in SemilocalAlg[1:]]))
			print("<br>")

	print("<h4>MAX Global Alignment</h4>")
	print(maxglobNeed[1])
	print(maxglobNeed[2])
	print("<p>Global Alignment (BFT): ",maxglobNeed[0][0] if maxglobNeed[0][0]<=0 else "+"+str(maxglobNeed[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in maxglobNeed[0][1:]]))
	print("<br>")
	print("<h4>MAX Local Alignment</h4>")
	print(maxlocalAlg[1])
	print(maxlocalAlg[2])
	print("<p>Local Alignment (BFT): ",maxlocalAlg[0][0] if maxlocalAlg[0][0]<=0 else "+"+str(maxlocalAlg[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in maxlocalAlg[0][1:]]))
	print("<br>")
	print("<h4>MAX Semiglobal Alignment</h4>")
	print(maxSemiglobal[1])
	print(maxSemiglobal[2])
	print("<p>Semiglobal Alignment (BFT): ",maxSemiglobal[0][0] if maxSemiglobal[0][0]<=0 else "+"+str(maxSemiglobal[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in maxSemiglobal[0][1:]]))
	print("<br>")


def metabolic_pathways_HTML_alg15(pathway0, pathway1):
	global end0,end1,n
	# graph creation
	g1 = generate_graph(pathway0)
	g2 = generate_graph(pathway1)
	graph0 = to_graph_from_dict(pathway0)
	graph1 = to_graph_from_dict(pathway1)

	if(not params):
		print("Graph 1")
		for n,i in zip(range(len(graph0.get_nodes())),graph0.get_nodes()):
			print(n," - ",i.get_value(),"->",[node.get_value() for node in i.get_edges()])
		end0 = input("End Node Graph 1: ")
		print("")

		print("Graph 2")
		for n,i in zip(range(len(graph1.get_nodes())),graph1.get_nodes()):
			print(n," - ",i.get_value(),"->",[node.get_value() for node in i.get_edges()])

		end1 = (input("End Node Graph 2: "))
		n = (input("Maximum cycles: "))
		paths0 = []
		for node in graph0:
			if(node.get_value()!=graph0[end0].get_value()):
				paths0+= graph0.get_cyclic_paths(node,graph0[end0], [], n)
		
		paths1 = []
		for node1 in graph1:
			if(node1.get_value()!=graph1[end1].get_value()):
				paths1+= graph1.get_cyclic_paths(node1,graph1[end1], [], n)
		
		if(len(paths0)==0):
			print("Not avaliable paths for graph 0")
			return
		if(len(paths1)==0):
			print("Not avaliable paths for graph 1")
			return


		"""
		print("Paths Graph 0:")
		for n,i in zip(range(len(paths0)),paths0):
			out = ""
			for node in i:
				out+=str(node.get_value())+"->"
			out = out[0:-2]
			print(n," - ",out)

		selected_Path0 = input("Select Path of graph 0: ")
		print("")
		print("Paths Graph 1:")
		for n,i in zip(range(len(paths1)),paths1):
			out = ""
			for node in i:
				out+=str(node.get_value())+"->"
			out = out[0:-2]
			print(n," - ",out)

		selected_Path1 = input("Select Path of graph 1: ")
		paths0 = [paths0[selected_Path0]]
		paths1 = [paths1[selected_Path1]]"""
	else:
		paths0 = graph0.get_cyclic_paths(graph0[start0],graph0[end0], [], n)
		paths1 = graph1.get_cyclic_paths(graph1[start1],graph1[end1], [], n)
	
	redirectOut(5)
	print("<h3>Algorithm 1.5</h3>")
	print("Paths Graph 1:<br>")
	for n,i in zip(range(len(paths0)),paths0):
			out = ""
			for node in i:
				out+=str(node.get_value())+"->"
			out = out[0:-2]
			print("".join([str(1),".",str(n)," - ",out]))
			print("<br>")

	print("<br>")
	print("Paths Graph 2:<br>")
	for n,i in zip(range(len(paths1)),paths1):
		out = ""
		for node in i:
			out+=str(node.get_value())+"->"
		out = out[0:-2]
		print("".join([str(2),".",str(n)," - ",out]))
		print("<br>")
	print("<h3>G1 ------------------------------------------G2</h3>")
	print('<img src="data:image/png;base64,',g1,'" alt="Red dot" />')
	print('<img src="data:image/png;base64,',g2,'" alt="Red dot" />')
	maxglobNeed = [[-100]]
	maxlocalAlg = [[-100]]
	maxSemiglobal=[[-100]]
	for p1 in range(len(paths0)):
		path0 = to_graph_from_dict(path2Dic(paths0[p1]))
		for p2 in range(len(paths1)):
			path1 = to_graph_from_dict(path2Dic(paths1[p2]))
			reset_dictionary()
			bft0 = path0.breadth_first_traversal()
			bft1 = path1.breadth_first_traversal()
			add_to_dictionary(bft0)
			add_to_dictionary(bft1)
			# Full Detail Output
			pathStr1 = "<p class='pathway'>Pathway 1."+str(p1)+": "+' '.join(bft0)+"</p>"
			pathStr2 = "<p class='pathway'>Pathway 2"+"."+str(p2)+": "+' '.join(bft1)+ "</p>"
			print("<h4>Full Detail Output - Algorithm 1.4</h4>")
			print(pathStr1)
			print(pathStr2)
			print("<br>")
			show_dictionary()
			# Low Detail Output
			print("<h4>Alignment Algorithms</h4>")
			globNeed = needleman_wunsch(renamed_path(bft0), renamed_path(bft1))
			localAlg = local_alignment(renamed_path(bft0), renamed_path(bft1))
			SemilocalAlg = semiglobal_alignment(renamed_path(bft0), renamed_path(bft1))
			if(globNeed[0]>maxglobNeed[0][0]):
				maxglobNeed = [globNeed,
				pathStr1,
				pathStr2
				]
			if(localAlg[0]>maxlocalAlg[0][0]):
				maxlocalAlg = [localAlg,
				pathStr1,
				pathStr2
				]
			if(SemilocalAlg[0]>maxSemiglobal[0][0]):
				maxSemiglobal = [SemilocalAlg,
				pathStr1,
				pathStr2
				]
			print("<p>Global Alignment (BFT): ",globNeed[0] if globNeed[0]<=0 else "+"+str(globNeed[0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in globNeed[1:]]))
			print("<br>")
			print("<p>Local Alignment (BFT): ",localAlg[0] if localAlg[0]<=0 else "+"+str(localAlg[0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in localAlg[1:]]))
			print("<br>")
			print("<p>Semiglobal Alignment (BFT): ",SemilocalAlg[0] if SemilocalAlg[0]<=0 else "+"+str(SemilocalAlg[0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in SemilocalAlg[1:]]))
			print("<br>")

	print("<h4>MAX Global Alignment</h4>")
	print(maxglobNeed[1])
	print(maxglobNeed[2])
	print("<p>Global Alignment (BFT): ",maxglobNeed[0][0] if maxglobNeed[0][0]<=0 else "+"+str(maxglobNeed[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in maxglobNeed[0][1:]]))
	print("<br>")
	print("<h4>MAX Local Alignment</h4>")
	print(maxlocalAlg[1])
	print(maxlocalAlg[2])
	print("<p>Local Alignment (BFT): ",maxlocalAlg[0][0] if maxlocalAlg[0][0]<=0 else "+"+str(maxlocalAlg[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in maxlocalAlg[0][1:]]))
	print("<br>")
	print("<h4>MAX Semiglobal Alignment</h4>")
	print(maxSemiglobal[1])
	print(maxSemiglobal[2])
	print("<p>Semiglobal Alignment (BFT): ",maxSemiglobal[0][0] if maxSemiglobal[0][0]<=0 else "+"+str(maxSemiglobal[0][0]),"<br>" ,'\n'.join(["<p class='alignment' style='font-family:Courier'>" + str(i) + "</p>" for i in maxSemiglobal[0][1:]]))
	print("<br>")


if __name__ == '__main__':
	if len(sys.argv) == 2:
		params = False
		reset_dictionary()
		filePath = sys.argv[1]
		myKGMLStart = SimpleKGML(filePath)
		myKGML = SimpleKGML(filePath)
		pathway0 = myKGML.getCompoundsGraph()
		pathway0start = myKGMLStart.getWithCentralNodeAsString()
		filePath = sys.argv[2]
		myKGML = SimpleKGML(filePath)
		myKGMLStar = SimpleKGML(filePath)
		pathway1 = myKGML.getCompoundsGraph()
		pathway1start = myKGMLStar.getWithCentralNodeAsString()
		#metabolic_pathways_HTML(pathway0, pathway1)
		while True:
			print("Menu")
			for i in map(lambda x: x + 1, range(4)):
				print(i,"-","Algorithm",i)
			i = input("Option: ")
			if(i==1):
				metabolic_pathways_HTML_alg1(pathway0start, pathway1start)
			if(i==2):
				metabolic_pathways_HTML_alg12(pathway0, pathway1)
			if(i==3):
				metabolic_pathways_HTML_alg13(pathway0, pathway1)
			if(i==4):
				metabolic_pathways_HTML_alg14(pathway0, pathway1)
			restoreOut()
	
	elif len(sys.argv) == 1:
		
		dict1 = {
		    "A":["B","E","C"],
		    "B":["F"],
		    "C":["K"],
		    "D":["H"],
		    "E":["G","D"],
		    "F":["E"],
		    "G":["K","J","I"],
		    "H":["G"],
		    "I":["H"],
		    #"J":[],
		    "K":["J"],
		}


		dict2 = {
		    "A":["B","E","C","H"],
		    "B":["F"],
		    #"C":["L"],
		    "D":["H"],
		    "E":["G","D"],
		    "F":["E"],
		    "G":["L","I"],
		    "H":["G"],
		    "I":["H"],
		    #"J":[],
		    "L":["J"],
		}

		dict3 = {
		    "A":["E"],
		    "M":["A","E","C"],
		    "C":["F","J"],
		    #"D":["H"],
		    "E":["F","G"],
		    "F":["J"],
		    "G":["H"],
		    "H":["I"],
		    "I":["J"],
		    #"J":[],
		    #"L":["J"],
		}
		
		#dict1 = dict2
		dict2 = dict3
		while True:
			print("Menu")
			print(1,"Algoritmo 1.1 y 2.1")
			print(2,"Algoritmo 1.2 y 2.2 ")
			print(3,"Algoritmo 1.3 y 2.3 ")
			print(4,"Algoritmo 1.4 ")
			print(5,"Algoritmo 1.5")
			print(6,"Todos")
			params = False

			i = input("Option: ")
			if(i==1):
				metabolic_pathways_HTML_alg1(dict1,dict2)
			if(i==2):
				metabolic_pathways_HTML_alg12(dict1, dict2)
			if(i==3):
				metabolic_pathways_HTML_alg13(dict1, dict2)
			if(i==4):
				metabolic_pathways_HTML_alg14(dict1, dict2)
			if(i==5):
				metabolic_pathways_HTML_alg15(dict1, dict2)
			if(i==6):
				params = False
				print("Inicio 1")
				metabolic_pathways_HTML_alg1(dict1,dict2)
				restoreOut()
				print("Inicio 2")
				metabolic_pathways_HTML_alg12(dict1,dict2)
				restoreOut()
				print("Inicio 3")
				metabolic_pathways_HTML_alg13(dict1,dict2)
				restoreOut()
				print("Inicio 4")
				metabolic_pathways_HTML_alg14(dict1,dict2)
				restoreOut()
				print("Inicio 5")
				metabolic_pathways_HTML_alg15(dict1,dict2)
			restoreOut()


	else:
		print("Incorrect number of parameters.")
		print("Expected: <path/KGML.xml>")
"""

if __name__ == '__main__':
	if len(sys.argv) > 1:
		filePath = sys.argv[1]
		myKGMLStart = SimpleKGML(filePath)
		myKGML = SimpleKGML(filePath)
		pathway0 = myKGML.getCompoundsGraph()
		pathway0start = myKGMLStart.getWithCentralNodeAsString()
		filePath = sys.argv[2]
		myKGML = SimpleKGML(filePath)
		myKGMLStar = SimpleKGML(filePath)
		pathway1 = myKGML.getCompoundsGraph()
		pathway1start = myKGMLStar.getWithCentralNodeAsString()
		#metabolic_pathways_HTML(pathway0, pathway1)
		while True:
			print("Menu")
			for i in map(lambda x: x + 1, range(4)):
				print(i,"-","Algorithm",i)
			i = input("Option: ")
			if(i==1):
				metabolic_pathways_HTML_alg1(pathway0start, pathway1start)
			if(i==2):
				metabolic_pathways_HTML_alg2(pathway0, pathway1)
			if(i==3):
				metabolic_pathways_HTML_alg3(pathway0, pathway1)
			if(i==4):
				metabolic_pathways_HTML_alg4(pathway0, pathway1)
			restoreOut()		

	else:
		print("Incorrect number of parameters."))
		print("Expected: <path/KGML.xml>"))


"""

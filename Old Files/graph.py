from collections import deque

class Node:
    """ Node data structure """
    def __init__(self, value):
        self.value = value
        self.active = True
        self.edges = []

    def get_value(self):
        return self.value

    def get_edges(self):
        return self.edges

    def deactivate(self):
        self.active = False

    def is_active(self):
        return self.active

    def __eq__(self, value):
        return self.value == value

    def __hash__(self):
        return len(self.value)

class Graph:
    """ Directed Graph data structure """
    def __init__(self):
        self.nodes = []

    def __getitem__(self,i):
    	return self.nodes[i]
    	
    def get_paths(self, initial, final, prev_path =[]):
        """Finds all paths from a node to another"""
        if initial == final:
            return [[final]]
        paths = []
        for edge in initial.get_edges():
            if edge not in prev_path:
                for path in self.get_paths(edge, final, prev_path + [edge]):
                    paths.append( [initial] + path)
        return paths
        
    def get_cyclic_paths(self, initial, final, prev =[], max_cycle = 0):
        """Finds all paths from a node to another, allowing cycles
           where any edge appears at most once"""
        if initial == final:
            return [[final]]
        paths = []
        for edge in initial.get_edges():
            if prev.count(edge) < max_cycle:
                for path in self.get_cyclic_paths(edge, final, prev + [edge], max_cycle):
                    paths.append( [initial] + path)
        return paths

    def get_node(self, value):
        i = self.get_nodes().index(value)
        return self.get_nodes()[i]

    def get_edges(self, value):
        n = self.get_node(value)
        res = []
        for edge in n.get_edges():
            res.append(edge.get_value())
        return res
    
    def get_nodes(self):
        return self.nodes

    def add_value(self, value):
        """ Add node to graph """
        node = Node(value)
        if not node in self.nodes:
            self.nodes.append(node)

    def add_edge(self, value1, value2):
        """ Add connection between node1 and node2 """
        self.add_value(value1)
        self.add_value(value2)
        index1 = self.nodes.index(value1)
        index2 = self.nodes.index(value2)
        node1 = self.nodes[index1]
        node2 = self.nodes[index2]
        node1.edges.append(node2)

    def delete_edge(self, value1, value2):
        """ Delete connection between node1 and node2 """
        index = self.nodes.index(Node(value1))
        node = self.nodes[index]
        index2 = node.edges.index(Node(value2))
        node.edges[index2].deactivate()

    def exists_edge(self, value1, value2):
        """ Verify is exists connection between node1 and node2 """
        if Node(value1) in self.nodes:
            index = self.nodes.index(value1)
            node = self.nodes[index]
            if Node(value2) in node.edges:
                index2 = node.edges.index(Node(value2))
                return node.edges[index2].is_active()
            else:
                return False
        return False

    def breadth_first_traversal(self,selectedNode = 0,endNode=""):
        """ Breadth First Traversal """
        if not self.nodes:
            return []

        result = []
        star = False
        if '*' in self.nodes:
            star = True
            start = self.nodes[self.nodes.index('*')]
        else:
            start = self.nodes[selectedNode]
        
        visited, queue, result = set([start]), deque([start]), []
        while queue:
            node = queue.popleft()
            result.append(node.value)
            if(node.value == endNode):
                break
            for nd in node.edges:
                if nd not in visited:
                    queue.append(nd)
                    visited.add(nd)
    
        return result[1:] if star else result



    def depth_first_traversal(self,selectedNode = 0,endNode=""):
        """ Depth First Traversal """
        if not self.nodes:
            return []

        result = []
        star = False
        if '*' in self.nodes:
            star = True
            start = self.nodes[self.nodes.index('*')]
        else:
            start = self.nodes[selectedNode]
        visited, stack, result = set([start]), [start], []
        while stack:
            node = stack.pop()
            result.append(node.value)
            if(node.value == endNode):
                break
            for nd in node.edges:
                if nd not in visited:
                    stack.append(nd)
                    visited.add(nd)

        return result[1:] if star else result

    def generate_dict(self):
        dict = {}
        for node in self.nodes:
            dict[node.value] = []
            for edge in node.get_edges():
                if edge.is_active():
                    dict[node.value].append(edge.value)
        return dict

def to_graph_from_dict(dict):
    graph = Graph()
    for node1 in dict:
        graph.add_value(node1)
        edges = dict[node1]
        for node2 in edges:
            graph.add_edge(node1, node2)
    return graph

def print_paths(paths):
    for p in paths:
        print_path(p)
        

def print_path(path):
    out = ""
    for node in path:
        out += node.get_value() + "->"
    print out

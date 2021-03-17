import json
from kgml2Json import SimpleKGML
from AuxiliaryFunctions import *

def generateImage(imagesFolderPath, name, graph):
  output = {"Algorithm": "GI"}
  generateGraphImage(imagesFolderPath, name, json.loads(graph))
  return json.dumps(output)

# Code: C1
def createOneCompoundGraph(imagesFolderPath, tempUploadsFolderPath, XMLFileName1):
    output = {"Algorithm": "C1"}
    # simpleKGMLStart1 = SimpleKGML(tempUploadsFolderPath + XMLFileName1)
    simpleKGML1 = SimpleKGML(tempUploadsFolderPath + XMLFileName1)
    pathwayCompoundsGraph1 = simpleKGML1.getCompoundsGraph()
    try:
        generateGraphImage(imagesFolderPath, XMLFileName1.replace(".xml", ""), pathwayCompoundsGraph1)
        output["Compound Graph 1"] = pathwayCompoundsGraph1
    except Exception as e:
        print(e)

    return json.dumps(output)


# Code: C2
def createTwoCompoundGraphs(imagesFolderPath, tempUploadsFolderPath, XMLFileName1, XMLFileName2):
    output = {"Algorithm": "C2"}
    output["Compound Graph 1"] = createOneCompoundGraph(imagesFolderPath, tempUploadsFolderPath, XMLFileName1)[
        "Compound Graph 1"]
    output["Compound Graph 2"] = createOneCompoundGraph(imagesFolderPath, tempUploadsFolderPath, XMLFileName2)[
        "Compound Graph 1"]
    return json.dumps(output)


# Code: S1
def createOneCentralNodeGraph(imagesFolderPath, tempUploadsFolderPath, XMLFileName1):
    output = {"Algorithm": "S1"}
    simpleKGMLStart1 = SimpleKGML(tempUploadsFolderPath + XMLFileName1)
    simpleKGML1 = SimpleKGML(tempUploadsFolderPath + XMLFileName1)
    centralNodeGraph1 = simpleKGML1.getCentralNodeGraph()
    try:
        generateGraphImage(imagesFolderPath, XMLFileName1.replace(".xml", ""), centralNodeGraph1)
        output["Central Node Graph 1"] = centralNodeGraph1
    except Exception as e:
        print(e)

    return json.dumps(output)


# Code: S2
def createTwoCentralNodeGraphs(imagesFolderPath, tempUploadsFolderPath, XMLFileName1, XMLFileName2):
    output = {"Algorithm": "S2"}
    output["Central Node Graph 1"] = createOneCentralNodeGraph(imagesFolderPath, tempUploadsFolderPath, XMLFileName1)[
        "Central Node Graph 1"]
    output["Central Node Graph 2"] = createOneCentralNodeGraph(imagesFolderPath, tempUploadsFolderPath, XMLFileName2)[
        "Central Node Graph 1"]
    return json.dumps(output)


# Code: NIndex
def getGraphNodesIndexes(pathwayGraph):
    output = {"Algorithm": "NIndex", "Nodes indexes": {}}
    graph = to_graph_from_dict(pathwayGraph)
    for n, i in zip(range(len(graph.get_nodes())), graph.get_nodes()):
        output["Nodes indexes"][n] = i.get_value()
    return json.dumps(output)


# Code: GPaths
def getGraphPathsIndexes(pathwayGraph, startNodeGraph, endNodeGraph, maximumCycles):
    output = {"Algorithm": "GPaths", "Graph paths": {}}
    graph = to_graph_from_dict(pathwayGraph)
    paths = graph.get_cyclic_paths(graph[int(startNodeGraph)], graph[int(endNodeGraph)], [], int(maximumCycles))
    for n, i in zip(range(len(paths)), paths):
        temporalPath = []
        for node in i:
            temporalPath.append(node.get_value())
        output["Graph paths"][n] = temporalPath
    return json.dumps(output)


# Code: A1
def alg1Transformation2DtoVector(pathwayGraph1, pathwayGraph2, newMatch, newMismatch, newGap):
    output = {"Algorithm": "A1"}
    graph1 = to_graph_from_dict(pathwayGraph1)
    graph2 = to_graph_from_dict(pathwayGraph2)
    bft1 = graph1.breadth_first_traversal()
    bft2 = graph2.breadth_first_traversal()
    dft1 = graph1.depth_first_traversal()
    dft2 = graph2.depth_first_traversal()
    addToDictionary(bft1)
    addToDictionary(bft2)
    addToDictionary(dft1)
    addToDictionary(dft2)

    output["BFT1"] = renamedPath(bft1)
    output["BFT2"] = renamedPath(bft2)
    output["DFT1"] = renamedPath(dft1)
    output["DFT2"] = renamedPath(dft2)
    output["Global BFT"] = needleman_wunsch(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["Global DFT"] = needleman_wunsch(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)
    output["Local BFT"] = local_alignment(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["Local DFT"] = local_alignment(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)
    output["SemiLocal BFT"] = semiglobal_alignment(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["SemiLocal DFT"] = semiglobal_alignment(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)
    # output["Differences 1-2"] = identify_differences(graph1, graph2, FULL)
    # output["Differences 2-1"] = identify_differences(graph2, graph1, FULL)

    # delete this
    output["params"] = [pathwayGraph1, pathwayGraph2, newMatch, newMismatch, newGap]

    return json.dumps(output)


# Code: A1T1
def alg1_1GraphTraversal_AnyNodeToAnyNode(pathwayGraph1, pathwayGraph2, newMatch, newMismatch, newGap):
    output = {"Algorithm": "A1T1"}
    graph1 = to_graph_from_dict(pathwayGraph1)
    graph2 = to_graph_from_dict(pathwayGraph2)
    bft1 = graph1.breadth_first_traversal()
    bft2 = graph2.breadth_first_traversal()
    dft1 = graph1.depth_first_traversal()
    dft2 = graph2.depth_first_traversal()
    addToDictionary(bft1)
    addToDictionary(bft2)
    addToDictionary(dft1)
    addToDictionary(dft2)

    output["BFT1"] = renamedPath(bft1)
    output["BFT2"] = renamedPath(bft2)
    output["DFT1"] = renamedPath(dft1)
    output["DFT2"] = renamedPath(dft2)
    output["Global BFT"] = needleman_wunsch(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["Global DFT"] = needleman_wunsch(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)
    output["Local BFT"] = local_alignment(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["Local DFT"] = local_alignment(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)
    output["SemiLocal BFT"] = semiglobal_alignment(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["SemiLocal DFT"] = semiglobal_alignment(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)

    # delete this
    output["params"] = [pathwayGraph1, pathwayGraph2, newMatch, newMismatch, newGap]

    return json.dumps(output)


# Code: A1T2
def alg1_2GraphTraversal_GivenNodeToAnyNode(pathwayGraph1, pathwayGraph2, startNodeGraph1, startNodeGraph2, newMatch,
                                            newMismatch, newGap):
    output = {"Algorithm": "A1T2"}
    graph1 = to_graph_from_dict(pathwayGraph1)
    graph2 = to_graph_from_dict(pathwayGraph2)
    bft1 = graph1.breadth_first_traversal(int(startNodeGraph1))
    bft2 = graph2.breadth_first_traversal(int(startNodeGraph2))
    dft1 = graph1.depth_first_traversal(int(startNodeGraph1))
    dft2 = graph2.depth_first_traversal(int(startNodeGraph2))
    addToDictionary(bft1)
    addToDictionary(bft2)
    addToDictionary(dft1)
    addToDictionary(dft2)

    output["BFT1"] = renamedPath(bft1)
    output["BFT2"] = renamedPath(bft2)
    output["DFT1"] = renamedPath(dft1)
    output["DFT2"] = renamedPath(dft2)
    output["Global BFT"] = needleman_wunsch(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["Global DFT"] = needleman_wunsch(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)
    output["Local BFT"] = local_alignment(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["Local DFT"] = local_alignment(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)
    output["SemiLocal BFT"] = semiglobal_alignment(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["SemiLocal DFT"] = semiglobal_alignment(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)

    # delete this
    output["params"] = [pathwayGraph1, pathwayGraph2, startNodeGraph1, startNodeGraph2, newMatch, newMismatch, newGap]

    return json.dumps(output)

# Code: A1T3
def alg1_3GraphTraversal_GivenNodeToGivenNode(pathwayGraph1, pathwayGraph2, startNodeGraph1, startNodeGraph2,
                                              endNodeGraph1, endNodeGraph2, newMatch, newMismatch, newGap):
    output = {"Algorithm": "A1T3"}
    graph1 = to_graph_from_dict(pathwayGraph1)
    graph2 = to_graph_from_dict(pathwayGraph2)
    bft1 = graph1.breadth_first_traversal(int(startNodeGraph1), int(endNodeGraph1))
    bft2 = graph2.breadth_first_traversal(int(startNodeGraph2), int(endNodeGraph2))
    dft1 = graph1.depth_first_traversal(int(startNodeGraph1), int(endNodeGraph1))
    dft2 = graph2.depth_first_traversal(int(startNodeGraph2), int(endNodeGraph2))
    addToDictionary(bft1)
    addToDictionary(bft2)
    addToDictionary(dft1)
    addToDictionary(dft2)

    output["BFT1"] = renamedPath(bft1)
    output["BFT2"] = renamedPath(bft2)
    output["DFT1"] = renamedPath(dft1)
    output["DFT2"] = renamedPath(dft2)
    output["Global BFT"] = needleman_wunsch(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["Global DFT"] = needleman_wunsch(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)
    output["Local BFT"] = local_alignment(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["Local DFT"] = local_alignment(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)
    output["SemiLocal BFT"] = semiglobal_alignment(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["SemiLocal DFT"] = semiglobal_alignment(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)

    # delete this
    output["params"] = [pathwayGraph1, pathwayGraph2, startNodeGraph1, startNodeGraph2, endNodeGraph1, endNodeGraph2,
                        newMatch, newMismatch, newGap]

    return json.dumps(output)

# Code: A1T4
def alg1_4EvalPossiblePaths_GivenNodeToGivenNode(pathwayGraph1, pathwayGraph2, selectedPath1, selectedPath2, newMatch,
                                                 newMismatch, newGap):
    output = {"Algorithm": "A1T4"}
    graph1 = to_graph_from_dict(pathwayGraph1)
    graph2 = to_graph_from_dict(pathwayGraph2)

    bft1 = graph1.breadth_first_traversal(int(selectedPath1))
    bft2 = graph2.breadth_first_traversal(int(selectedPath2))
    dft1 = graph1.depth_first_traversal(int(selectedPath1))
    dft2 = graph2.depth_first_traversal(int(selectedPath2))
    addToDictionary(bft1)
    addToDictionary(bft2)
    addToDictionary(dft1)
    addToDictionary(dft2)

    output["BFT1"] = renamedPath(bft1)
    output["BFT2"] = renamedPath(bft2)
    output["DFT1"] = renamedPath(dft1)
    output["DFT2"] = renamedPath(dft2)
    output["Global BFT"] = needleman_wunsch(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["Global DFT"] = needleman_wunsch(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)
    output["Local BFT"] = local_alignment(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["Local DFT"] = local_alignment(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)
    output["SemiLocal BFT"] = semiglobal_alignment(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["SemiLocal DFT"] = semiglobal_alignment(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)

    # delete this
    output["params"] = [pathwayGraph1, pathwayGraph2, selectedPath1, selectedPath2, newMatch, newMismatch, newGap]

    return json.dumps(output)

# Code: A1T5
def alg1_5GraphTraversal_AnyNodeToGivenNode(pathwayGraph1, pathwayGraph2, endNodeGraph1, endNodeGraph2, newMatch,
                                            newMismatch, newGap):
    output = {"Algorithm": "A1T5"}
    graph1 = to_graph_from_dict(pathwayGraph1)
    graph2 = to_graph_from_dict(pathwayGraph2)
    bft1 = graph1.breadth_first_traversal(endNode=int(endNodeGraph1))
    bft2 = graph2.breadth_first_traversal(endNode=int(endNodeGraph2))
    dft1 = graph1.depth_first_traversal(endNode=int(endNodeGraph1))
    dft2 = graph2.depth_first_traversal(endNode=int(endNodeGraph2))
    addToDictionary(bft1)
    addToDictionary(bft2)
    addToDictionary(dft1)
    addToDictionary(dft2)

    output["BFT1"] = renamedPath(bft1)
    output["BFT2"] = renamedPath(bft2)
    output["DFT1"] = renamedPath(dft1)
    output["DFT2"] = renamedPath(dft2)
    output["Global BFT"] = needleman_wunsch(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["Global DFT"] = needleman_wunsch(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)
    output["Local BFT"] = local_alignment(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["Local DFT"] = local_alignment(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)
    output["SemiLocal BFT"] = semiglobal_alignment(renamedPath(bft1), renamedPath(bft2), newMatch, newMismatch, newGap)
    output["SemiLocal DFT"] = semiglobal_alignment(renamedPath(dft1), renamedPath(dft2), newMatch, newMismatch, newGap)

    # delete this
    output["params"] = [pathwayGraph1, pathwayGraph2, endNodeGraph1, endNodeGraph2, newMatch, newMismatch, newGap]

    return json.dumps(output)

# Code: A2
def alg2_DifferentiationByPairs(pathwayGraph1, pathwayGraph2):
    output = {"Algorithm": "A2"}
    graph1 = to_graph_from_dict(pathwayGraph1)
    graph2 = to_graph_from_dict(pathwayGraph2)

    output["Differences 1-2"] = identify_differences(graph1, graph2, FULL)
    output["Differences 2-1"] = identify_differences(graph2, graph1, FULL)

    # delete this
    output["params"] = [pathwayGraph1, pathwayGraph2]

    return json.dumps(output)


# Code: A3
def alg3_NameTBD():
    return "Ok"

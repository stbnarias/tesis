from AlgorithmsFunctions import *
import json

# Used to get path to temp_uploads folder.
imagesFolderPath = os.getcwd().replace('\\', '/') + "/images/"
tempUploadsFolderPath = os.getcwd().replace('\\', '/') + "/temp_uploads/"

if __name__ == '__main__':
    # Get request code
    requestCode = sys.argv[-1]
    try:
        # Called after loading a KGML
        if requestCode == "C1":
            print(createOneCompoundGraph(imagesFolderPath, tempUploadsFolderPath, sys.argv[1]))
        # Probably it is never gonna be used
        elif requestCode == "C2":
            print(createTwoCompoundGraphs(imagesFolderPath, tempUploadsFolderPath, sys.argv[1], sys.argv[2]))
        #
        elif requestCode == "S1":
            print(createOneCentralNodeGraph(imagesFolderPath, tempUploadsFolderPath, sys.argv[1]))
        elif requestCode == "S2":
            print(createTwoCentralNodeGraphs(imagesFolderPath, tempUploadsFolderPath, sys.argv[1], sys.argv[2]))
        elif requestCode == "NIndex":
            print(getGraphNodesIndexes(sys.argv[1]))
        elif requestCode == "GPaths":
            print(getGraphPathsIndexes(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
        elif requestCode == "A1":
            print(alg1Transformation2DtoVector(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))
        elif requestCode == "A1T1":
            print(
                alg1_1GraphTraversal_AnyNodeToAnyNode(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))
        elif requestCode == "A1T2":
            print(
                alg1_2GraphTraversal_GivenNodeToAnyNode(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5],
                                                        sys.argv[6], sys.argv[7]))
        elif requestCode == "A1T3":
            print(alg1_3GraphTraversal_GivenNodeToGivenNode(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                                                            sys.argv[5],
                                                            sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9]))
        elif requestCode == "A1T4":
            print(
                alg1_4EvalPossiblePaths_GivenNodeToGivenNode(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                                                             sys.argv[5],
                                                             sys.argv[6], sys.argv[7]))
        elif requestCode == "A1T5":
            print(
                alg1_5GraphTraversal_AnyNodeToGivenNode(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5],
                                                        sys.argv[6], sys.argv[7]))
        elif requestCode == "A2":
            print(alg2_DifferentiationByPairs(sys.argv[1], sys.argv[2]))
        elif requestCode == "A3":
            print(alg3_NameTBD())
        elif requestCode == "GI":
            print(generateImage(imagesFolderPath, sys.argv[1],sys.argv[2]))
        else:
            print("ERROR: request code unknown.", sys.argv)
        # print("JSON RECEIVED: ", sys.argv)
    except Exception as e:
        print(e)

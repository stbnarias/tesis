from Bio.KEGG.KGML.KGML_parser import read

class SimpleKGML:
    def __init__(self, filePath):
        self.compoundsGraph = {}
        self.bioKGML = read(open(filePath, 'r'))
        self._fillGraph()

    def _fillGraph(self):
        for reaction in self.bioKGML.reactions:
            substrates, products = reaction.substrates, reaction.products
            for entry in substrates:
                entry = entry.name[4:]
                for product in products:
                    product = product.name[4:]

                    if entry in self.compoundsGraph:
                        self.compoundsGraph[entry].append(product)
                    else:
                        self.compoundsGraph[entry] = [product]

    def getCompoundsGraph(self):
        return self.compoundsGraph

    def getCentralNodeGraph(self):
        centralNodeGraph = self.compoundsGraph
        centralNodeGraph["*"] = [_ for _ in self.compoundsGraph]

        return centralNodeGraph

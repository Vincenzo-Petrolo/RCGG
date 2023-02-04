import networkx as nx

class Graph2Bench(object):
    def __init__(self) -> None:
        pass

    def convert(self, graph, output_file):
        # Get all the nodes in the graph as list of tuples
        # 0 contains node name
        # 1 contains attributes
        graph_nodes = graph.nodes(data=True)
        # Create the file and erase it (in case it is already exisitng)
        f = open(output_file, "w")
        f.close()
        # Iterate over all the nodes in the graph
        for node in graph_nodes:
            # If the node is an input
            if (node[1]['type'] == 'input'):
                # Write it to the file
                self._writeINPUT(node[0], output_file)
            elif(self._isOutput(node[0], graph)):
                # If the node is an output, write to file
                self._writeOUTPUT(node[0], output_file)
                self._writeGATE(node, output_file, graph)
            else:
                self._writeGATE(node, output_file, graph)
            
    
    def _writeINPUT(self, node, filename):
        with open(filename, 'a') as f:
            f.write(f"INPUT({node})\n")

    def _writeGATE(self, node, filename, graph):
        with open(filename, 'a') as f:
            f.write(f"{node[0]} = {node[1]['type']}(")
            # get the inputs to this node
            predecessors = list(graph.predecessors(node[0]))

            for pred in predecessors:
                if (pred == predecessors[-1]):
                    # If last node, close the bracket
                    f.write(f"{pred})\n")
                else:
                    f.write(f"{pred},")

    def _writeOUTPUT(self, node, filename):
        with open(filename, 'a') as f:
            f.write(f"OUTPUT({node})\n")

    def _isOutput(self, node, graph):
        if (len(list(nx.neighbors(graph, node))) == 0):
            return True
        return False 
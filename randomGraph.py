import networkx as nx
import random

possible_gates = ['AND', 'NAND', 'OR', 'NOR', 'XOR', 'XNOR', 'INV', 'BUF']

class RandomGraphGenerator(object):
    def __init__(self, n_inputs, max_nodes_per_level, max_fan_in, max_fan_out, depth) -> None:
        super().__init__()
        self.n_inputs = n_inputs
        self.max_nodes_per_level = max_nodes_per_level
        self.max_fan_in = max_fan_in
        self.max_fan_out = max_fan_out
        self.depth = depth
        self.graph_obj = None

        self._generateGraph()
    
    def getGraph(self):
        # Return a copy of the graph
        return self.graph_obj.copy()
    
    def _generateGraph(self):
        self.graph_obj = nx.DiGraph()
        # Counter is used in the following functions for naming the nodes
        self.counter = 0
        # Create the inputs of the graph
        self._createInputs()
        # Add as many layers as given in the depth
        for i in range(self.depth):
            self._addLayer()
    
    def generateGraph(self):
        self._generateGraph()
        
        return self.getGraph()


    def _createInputs(self):
        for i in range(self.n_inputs):
            self.graph_obj.add_node(self.counter, type='input')
            self.counter += 1
    
    def _addLayer(self):
        # Iterate random number of times depending on the nodes per level
        for i in range(random.randint(1, self.max_nodes_per_level)):
            node_type = random.choice(possible_gates)
            # Add the node to the graph
            self.graph_obj.add_node(self.counter, type=node_type)
            # V is the destination node for the following connections
            v = self.counter
            # Connect to the previous layer
            if (node_type == 'INV' or node_type == 'BUF'):
                # Get a list of possible connections
                connectable_nodes = self._getConnectableNodes()
                # Pick the first (highest priority)
                u = connectable_nodes[0]
                self.graph_obj.add_edge(u,v)
            else:
                # Randomly assign a given number of inputs, at least 2
                for i in range(random.randint(2, self.max_fan_in)):
                    # Get a list of possible connections
                    connectable_nodes = self._getConnectableNodes()
                    # Pick the first (highest priority)
                    u = connectable_nodes[0]
                    # Connect it
                    self.graph_obj.add_edge(u,v)
            self.counter += 1
    
    def _getConnectableNodes(self):
        # Returns nodes that can be connected
        # Sort first those who don't have connections yet
        nodes = nx.nodes(self.graph_obj)
        unconnected_nodes = []
        connected_nodes = []

        # First iterate and insert those nodes who are not connected yet
        for node in nodes:
            # Avoid self-loops
            if (node == self.counter):
                continue
            # Check if node has not reached its maximum fan_out yet
            if (self._hasReachedMaxFanout(node)):
                # Skip, you can't connect it further
                continue
            # Check if the node is not connected to anything
            if (len(list(nx.neighbors(self.graph_obj, node))) == 0):
                unconnected_nodes.append(node)
            else:
                connected_nodes.append(node)
        
        # Join the two lists
        unconnected_nodes += connected_nodes

        # Return the final list
        return unconnected_nodes
    
    def _hasReachedMaxFanout(self, node):
        if (len(list(nx.neighbors(self.graph_obj, node))) >= self.max_fan_out):
            return True

        return False
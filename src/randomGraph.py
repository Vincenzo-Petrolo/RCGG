import networkx as nx
import random
import time

possible_gates = ['AND', 'NAND', 'OR', 'NOR', 'XOR', 'XNOR', 'NOT', 'BUFF']

class RandomGraphGenerator(object):
    def __init__(self, n_inputs = 2, n_outputs = 2, max_nodes_per_level = 2, max_fan_in = 2, max_fan_out = 2, depth = 2, no_redundancy = False) -> None:
        super().__init__()
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.max_nodes_per_level = max_nodes_per_level
        self.max_fan_in = max_fan_in
        self.max_fan_out = max_fan_out
        self.depth = depth
        self.graph_obj = None
        self.redundancy_free = no_redundancy 

        if (self.redundancy_free == True):
            # This avoids creating conflicts
            self.max_fan_out = 1


        self._generateGraph()
    
    def getGraph(self):
        # Return a copy of the graph
        return self.graph_obj.copy()
    
    def _generateGraph(self):
        self.graph_obj = nx.DiGraph()
        # Counter is used in the following functions for naming the nodes
        self.counter = 0
        # Create the inputs of the graph
        if (self.redundancy_free == False):
            self._createInputs()
            # Add as many layers as given in the depth
            for i in range(self.depth):
                self._addLayer()
            # Add the output layer
            self._addOutputLayer()
            # Perform check
            self._check()
        else:
            self._createInputs()

            for i in range(self.depth):
                self._addLayer()

                if (len(self._getConnectableNodes()) == 0):
                    break
            
            self._fix()
    
    def generateGraph(self):
        self._generateGraph()
        
        return self.getGraph()


    def _createInputs(self):
        for i in range(self.n_inputs):
            self.graph_obj.add_node(self.counter, type='input')

            self.counter += 1
    
    
    def _addLayer(self):
        new_nodes = []
        # Iterate random number of times depending on the nodes per level
        for i in range(random.randint(1, self.max_nodes_per_level)):
            connectable_nodes = self._getConnectableNodes()
            for new_node in new_nodes:
                connectable_nodes.remove(new_node)

            fan_in = random.randint(2, self.max_fan_in)

            if (self.redundancy_free and fan_in > len(connectable_nodes)):
                break

            node_type = random.choice(possible_gates)

            # Add the node to the graph
            self.graph_obj.add_node(self.counter, type=node_type)
            # V is the destination node for the following connections
            v = self.counter
            new_nodes.append(v)
            # Connect to the previous layer
            if (node_type == 'NOT' or node_type == 'BUFF'):
                # Get a list of possible connections
                # Pick the first (highest priority)
                u = connectable_nodes[0]
                self.graph_obj.add_edge(u,v)
            else:
                # Randomly assign a given number of inputs, at least 2
                for j in range(fan_in):
                    j = j % len(connectable_nodes)
                    u = connectable_nodes[j]
                    # Connect it
                    self.graph_obj.add_edge(u,v)
            self.counter += 1
    
    def _addOutputLayer(self):
        # Create a temporary graph
        # Create this to get which are the output nodes
        self.output_nodes = []
        tmp_graph = nx.DiGraph()
        for i in range(self.n_outputs):
            node_type = random.choice(possible_gates)
            # Add the node to the graph
            tmp_graph.add_node(self.counter, type=node_type)
            # V is the destination node for the following connections
            v = self.counter
            self.output_nodes.append(v)
            # Get a list of possible connections
            connectable_nodes = self._getConnectableNodes()
            # Connect to the previous layer
            if (node_type == 'NOT' or node_type == 'BUFF'):
                # Get a list of possible connections
                # Pick the first (highest priority)
                u = connectable_nodes[0]
                tmp_graph.add_edge(u,v)
            else:
                # Randomly assign a given number of inputs, at least 2
                for j in range(random.randint(2, self.max_fan_in)):
                    # Pick the first (highest priority)
                    try:
                        u = connectable_nodes[j]
                    except:
                        print("[ERROR] Rules are too strict, can't generate graph")
                        exit(1)


                    # Connect it
                    tmp_graph.add_edge(u,v)
            self.counter += 1
        # Eventually join the final layer to the previous
        self.graph_obj = nx.compose(self.graph_obj, tmp_graph)
    
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
        
        # Add randomness to the nodes
        random.shuffle(connected_nodes) 
        random.shuffle(unconnected_nodes)
        # Join the two lists
        unconnected_nodes += connected_nodes

        # Return the final list
        return unconnected_nodes
    
    def _hasReachedMaxFanout(self, node):
        if (len(list(nx.neighbors(self.graph_obj, node))) >= self.max_fan_out):
            return True

        return False
    
    def _check(self):
        # Check for unconnected nodes and remove them
        nodes = nx.nodes(self.graph_obj)
        for node in list(nodes):
            if (len(list(nx.neighbors(self.graph_obj, node))) == 0 and node not in self.output_nodes):
                print(f"[WARNING] Trying to force given number of outputs, removing nodes")
                self.graph_obj.remove_node(node)
    
    def _fix(self):
        # Don't leave inputs withot being connected
        nodes = nx.nodes(self.graph_obj)
        for node in list(nodes):
            if (self.graph_obj.in_degree(node) == 0 and self.graph_obj.out_degree(node) == 0):
                self.graph_obj.remove_node(node)

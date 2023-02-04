import networkx as nx
import os

class Graph2Verilog(object):
    def __init__(self) -> None:
        pass

    def convert(self, graph, module_name : str):
        self.module_name = module_name.split('/')[-1]
        self.directory = module_name.split('/')[0]
        # Get all the nodes in the graph as list of tuples
        # @0 contains node name
        # @1 contains attributes
        graph_nodes = graph.nodes(data=True)
        # Create the file and erase it (in case it is already exisitng)
        f = open(f"{os.path.join(self.directory, self.module_name)}.v", "w")
        f.close()
        # Write the module
        self._writeModule(graph_nodes, graph)
        # Write the body of the module
        self._writeWires(graph_nodes, graph)
        # Write the always block to perform the assignment
        self._writeAssignments(graph_nodes, graph)
        # Write the end of the module
        self._writeEndModule()



    
    def _writeModule(self, graph_nodes, graph):
        with open(f"{os.path.join(self.directory, self.module_name)}.v","a") as f:
            f.write(f"module {self.module_name} (")
            f.write(self._getInputOfModule(graph_nodes))
            f.write(self._getOutputOfModule(graph_nodes, graph))
    
    def _writeWires(self,graph_nodes, graph):
        final_string = ""

        for node in graph_nodes:
            if (node[1]["type"] != "input" and  not self._isOutput(node[0], graph)):
                final_string += f"\twire n{node[0]};\n"

        with open(f"{os.path.join(self.directory, self.module_name)}.v","a") as f:
            f.write(final_string)

    def _writeAssignments(self, graph_nodes, graph):
        final_string = "\n"

        for node in graph_nodes:
            final_string += self._writeGATE(node, graph=graph)
        
        with open(f"{os.path.join(self.directory, self.module_name)}.v","a") as f:
            f.write(final_string)
    
    def _writeEndModule(self):
        with open(f"{os.path.join(self.directory, self.module_name)}.v","a") as f:
            f.write(f"\nendmodule")

    
            
    
    def _getInputOfModule(self, graph_nodes):

        final_string = "\n"

        for node in graph_nodes:
            if (node[1]["type"] == 'input'):
                final_string += f"\tinput n{node[0]},\n"
        
        return final_string

    def _getOutputOfModule(self, graph_nodes, graph):

        final_string = ""

        for node in graph_nodes:
            if (self._isOutput(node[0], graph)):
                final_string += f"\toutput n{node[0]},\n"
        
        # Remove last comma and add ");"
        final_string = final_string.removesuffix(',\n')
        final_string += "\n);\n"
        
        return final_string
            
    def _writeGATE(self, node, graph):

        if (node[1]['type'] == "input"):
            return ""

        final_string = ""
        negation = ""
        operator = self._mapVerilogOperator(node[1]['type'])

        if (node[1]['type'] in ["NAND", "NOR", "XNOR", "NOT"]):
            negation = "~"

        final_string += f"\tassign n{node[0]} = {negation}("

        # get the inputs to this node
        predecessors = list(graph.predecessors(node[0]))

        for pred in predecessors:
            final_string += f" n{pred} {operator}"
        
        final_string = final_string.removesuffix(operator)
        final_string += ");\n"

        return final_string
    
    def _mapVerilogOperator(self, gate_type):
        if (gate_type in ["AND", "NAND"]):
            return "&"
        elif (gate_type in ["OR", "NOR"]):
            return "|"
        elif (gate_type in ["XOR", "XNOR"]):
            return "^"
        
        return ""

    def _isOutput(self, node, graph):
        if (len(list(nx.neighbors(graph, node))) == 0):
            return True
        return False 
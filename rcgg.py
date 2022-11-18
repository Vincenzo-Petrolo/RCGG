import networkx as nx
import matplotlib.pyplot as plt
from randomGraph import RandomGraphGenerator
from graph2bench import Graph2Bench
import getopt, sys

version = '0.0'

def print_help():
    print(f"Usage: python3 rcgg.py <options>")
    print(f"Available options:")
    print(f"\t--help(-h)\t\t: Show this help")
    print(f"\t--version(-v)\t\t: Show the version of the program")
    print(f"\t--output(-o)\t\t: Name of the final generated bench file")
    print(f"\t--n_inputs=\t\t: Number of inputs to the circuit")
    print(f"\t--n_outputs=\t\t: Number of outputs of the circuit")
    print(f"\t--max_nodes_per_lvl=\t: Maximum #gates in each level of the circuit")
    print(f"\t--max_fan_in=\t\t: Maximum #fan_in in each gate of the circuit")
    print(f"\t--max_fan_out=\t\t: Maximum #fan_out in each gate of the circuit")
    print(f"\t--depth=\t\t: Depth of the circuit")
    print(f"All the parameters are optional, if not specified default values will be used")



def print_version():
    print(f"(R)andom (C)ircuit (G)raph (G)enerator v{version}")

if __name__ == "__main__":
    # Command parsing
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vho:", [   "help", 
                                                            "version",
                                                            "output=", 
                                                            "n_inputs=",
                                                            "n_outputs=",
                                                            "max_nodes_per_lvl=",
                                                            "max_fan_in=",
                                                            "max_fan_out=",
                                                            "depth="])
    except getopt.GetoptError as err:
        print(err)
        print_help()
        exit(2)
    output_filename = None

    gen_parameters = {
        'n_inputs' : None,
        'n_outputs': None,
        'max_nodes_per_lvl' : None,
        'max_fan_in' : None,
        'max_fan_out' : None,
        'depth' : None
    }

    for o,a in opts:
        if o in ['-o', '--output']:
            output_filename = a
        elif o in ['-h', '--help']:
            print_help()
            exit(0)
        elif o in ['-v', '--version']:
            print_version()
        
        # Try to set parameters
        if (o in gen_parameters.keys()):
            gen_parameters[o] = a
            

    # Pass the parameters to the generator
    generator = RandomGraphGenerator(**gen_parameters)

    graph = generator.getGraph()

    converter = Graph2Bench()

    if (output_filename is None):
        # Use the parameters to generate an hash
        hashed_value = hash(gen_parameters.values())
        hashed_value = hashed_value[:(max(3, len(hashed_value)))]
        output_filename = 'c'+ hashed_value + '.bench'
    
    converter.convert(graph, output_filename)

    nx.draw(graph)
    plt.show()
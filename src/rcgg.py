import networkx as nx
import matplotlib.pyplot as plt
from randomGraph import RandomGraphGenerator
from graph2bench import Graph2Bench
from graph2verilog import Graph2Verilog
import getopt, sys
import random
import os

version = '0.0'

def print_help():
    print(f"Usage: python3 rcgg.py <options>")
    print(f"Available options:")
    print(f"\t--help(-h)\t\t: Show this help")
    print(f"\t--version(-v)\t\t: Show the version of the program")
    print(f"\t--output(-o)\t\t: Name of the final generated bench file")
    print(f"\t--n_inputs=\t\t: Number of inputs to the circuit")
    print(f"\t--n_outputs=\t\t: Number of outputs of the circuit")
    print(f"\t--max_nodes_per_level=\t: Maximum #gates in each level of the circuit")
    print(f"\t--max_fan_in=\t\t: Maximum #fan_in in each gate of the circuit")
    print(f"\t--max_fan_out=\t\t: Maximum #fan_out in each gate of the circuit")
    print(f"\t--depth=\t\t: Depth of the circuit")
    print(f"\t--no-redundancy\t\t: Create a redundancy free circuit")
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
                                                            "max_nodes_per_level=",
                                                            "max_fan_in=",
                                                            "max_fan_out=",
                                                            "depth=",
                                                            "no_redundancy",
                                                            "number_faults="
                                                            ])
    except getopt.GetoptError as err:
        print(err)
        print_help()
        exit(2)
    output_filename = None

    gen_parameters = {
        'n_inputs'              : 2,
        'n_outputs'             : 2,
        'max_nodes_per_level'   : 2,
        'max_fan_in'            : 2,
        'max_fan_out'           : 2,
        'depth'                 : 2,
        'no_redundancy'          : False
    }

    number_of_faults = 10

    for o,a in opts:
        if o in ['-o', '--output']:
            output_filename = a
        elif o in ['-h', '--help']:
            print_help()
            exit(0)
        elif o in ['-v', '--version']:
            print_version()
            exit(0)
        elif o in ['--no_redundancy']:
            gen_parameters["no_redundancy"] = True
        elif o in ['--number_faults']:
            number_of_faults = a
        else: 
            # Try to set parameters
            o = o.replace('-','') # remove the -- at the beginning of the option
            if (o in gen_parameters.keys()):
                gen_parameters[o] = int(a)
        

    generator = RandomGraphGenerator(**gen_parameters)

    graph = generator.getGraph()

    converter = Graph2Bench()
    verilog_converter = Graph2Verilog()
    output_filename = None

    if (output_filename is None):
        # Use the parameters to generate an hash
        seed = random.randint(0, 100)
        hashed_value = str( hash(seed * hash(gen_parameters.values())))
        hashed_value = hashed_value[:(min(5, len(hashed_value)))]
        output_filename = 'c'+ hashed_value + '.bench'
    
    # Generate a directory for the circuit with different faults
    general_dir = output_filename.removesuffix('.bench')
    # Create the directory
    os.mkdir(general_dir)
    converter.convert(graph, os.path.join(general_dir, output_filename))
    verilog_converter.convert(graph, os.path.join(general_dir, general_dir))
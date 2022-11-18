import networkx as nx
import matplotlib.pyplot as plt
from randomGraph import RandomGraphGenerator

generator = RandomGraphGenerator(
    n_inputs=2,
    max_nodes_per_level=3,
    max_fan_in=2,
    max_fan_out=2,
    depth=2 
)

graph = generator.getGraph()

nx.draw(graph)
plt.show()
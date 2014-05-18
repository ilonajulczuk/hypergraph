import numpy as np
import networkx as nx
from matplotlib import pyplot as plt

from hypergraph.generators import uniform_hypergraph
from hypergraph.converters import (convert_to_nx_bipartite_graph,
                                   convert_to_custom_hyper_G)
from hypergraph import utils


def show_different_hypergraphs(n=10, k=3, parts=10):
    for fraction in np.linspace(0, 1, parts)[1:]:
        plt.figure(figsize=(6, 6))
        g = uniform_hypergraph(n=n, k=k,
                               number_of_edges=int(n * fraction))
        G = convert_to_nx_bipartite_graph(g.nodes(), g.hyper_edges())
        utils.plot_bipartite_graph(G, *utils.hypergraph_to_bipartite_parts(G))
        hyper_G = convert_to_custom_hyper_G(g.nodes(), g.hyper_edges())

        plt.figure(figsize=(6, 6))
        nx.draw(hyper_G,
                node_size=3000, cmap=plt.cm.Blues, alpha=0.6)

    plt.show()

if __name__ == '__main__':
    show_different_hypergraphs(parts=3)

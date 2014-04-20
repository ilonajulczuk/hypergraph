import networkx as nx
import numpy as np
from hypergraph import converters
from matplotlib import pyplot as plt
from hypergraph.generators import uniform_hypergraph


def create_graph(number_of_nodes, cardinality, fraction_of_hyperedges):
    HG = uniform_hypergraph(
        n=number_of_nodes,
        k=cardinality,
        number_of_edges=int(
            number_of_nodes *
            fraction_of_hyperedges))

    return HG


def draw_bipartite_graph(G, group_1, group_2):
    """Draw graph as bipartite graph (U, V, E).

    Parameters:
        G: a networkx graph
        group_1:  U
        group_2:  V
    """
    pos = {x: (0, float(i % 20) * 2) for i, x in enumerate(group_1)}
    pos.update({node: (18.3, 0 + float(i % 20) * 2) for i,
                node in enumerate(group_2)})

    plt.figure()
    nx.draw(G, pos, node_color='m', node_size=800,
            with_labels=True, width=1.3, alpha=0.4)


def hypergraph_to_bipartite_parts(G):
    """Convert hypergraph to two parts: nodes and edges.
    """
    group_1 = (node for node in G.nodes() if not isinstance(node, tuple))
    group_2 = (node for node in G.nodes() if isinstance(node, tuple))
    return group_1, group_2


def plot_different_representations(nodes, hyperedges):
    print("Drawing different representations of hypergraph")

    print("Bipartite graph")
    nx_bipartite = converters.convert_to_nx_bipartite_graph(nodes, hyperedges)
    draw_bipartite_graph(nx_bipartite,
                         *hypergraph_to_bipartite_parts(nx_bipartite))

    print("Graph of hypereges as nodes")
    custom_hyper_g = converters.convert_to_custom_hyper_G(nodes, hyperedges)
    plt.figure()
    nx.draw(custom_hyper_g)

    print("Clique graph")

    clique_graph = converters.convert_to_clique_graph(nodes, hyperedges)
    plt.figure()
    nx.draw(clique_graph)


def plot_hyperedges_frequencies(most_common, hyperedges, title, normed=True):
    hyperedges_indexes, occurrences = zip(*most_common)
    if normed:
        occurrences /= np.sum(occurrences)
    plt.bar(hyperedges_indexes, occurrences)
    plt.title(title)
    plt.xticks(range(len(hyperedges)), hyperedges)


def get_names_and_occurrences(most_common_nodes, normed=True):
    names_of_nodes = list(most_common_nodes.keys())
    node_occurrences = list(most_common_nodes.values())

    if normed:
        all_occurrences = sum(node_occurrences)
        node_occurrences = [float(oc) / all_occurrences
                            for oc in node_occurrences]
    return names_of_nodes, node_occurrences


def plot_nodes_frequencies(most_common_nodes, title, normed=True):
    names, node_occurrences = get_names_and_occurrences(most_common_nodes,
                                                        normed)
    plt.bar(names,
            node_occurrences,
            alpha=0.7, color='magenta')

    plt.title(title)
    plt.show()
    return node_occurrences

import random
import math
import itertools
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np


def generate_hypergraph(n=6, number_of_edges=None, k=3):
    """Generate hypergraph wiht constant cardinality of edges.

    :n - number of nodes,
    :number_of_edges - how many hyper edges will be created,
    :k - cardinality of hyper edges.
    """
    vertices = range(1, n + 1)

    if number_of_edges is None:
        number_of_edges = int(math.sqrt(n))
    hyper_edges = random.sample(list(itertools.combinations(vertices, k)), number_of_edges)
    return (vertices, hyper_edges)


def convert_to_nx_biparty_graph(vertices, hyper_edges):
    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_nodes_from(hyper_edges)
    for e in hyper_edges:
        for n in e:
            G.add_edge(n, e)
    return G


def draw_bipartite_graph(G, group_1, group_2):
    pos = {x:(0 , float(i % 20) * 2) for i, x in enumerate(group_1)}
    pos.update({node: (18.3, 0 + float(i % 20) * 2) for i, node in enumerate(group_2)})

    nx.draw(G, pos, node_color='m', node_size=800, with_labels=True, width=1.3, alpha=0.4)


def hipergraph_to_bipartite_parts(G):
    group_1 = (node for node in G.nodes() if not isinstance(node, tuple))
    group_2 = (node for node in G.nodes() if isinstance(node, tuple))
    return group_1, group_2


def convert_to_custom_hyper_G(nodes, edges):
    nodes = [node for node in edges if isinstance(node, tuple)]
    edges = [(node_1, node_2) for node_1, node_2 in itertools.combinations(edges, 2) if set(node_1) & set(node_2)]
    hyper_G = nx.Graph()
    hyper_G.add_nodes_from(nodes)
    hyper_G.add_edges_from(edges)
    return hyper_G


def show_different_hipergraphs(n=10, k=3, parts=10):
    for fraction in np.linspace(0, 1, parts)[1:]:
        plt.figure(figsize=(6, 6))
        g = generate_hypergraph(n=n, k=k, number_of_edges=int(n * fraction))
        G = convert_to_nx_biparty_graph(*g)
        draw_bipartite_graph(G, *hipergraph_to_bipartite_parts(G))
        hyper_G = convert_to_custom_hyper_G(*g)

        p=nx.degree(hyper_G)

        plt.figure(figsize=(6, 6))
        nx.draw(hyper_G, node_color=p.values(), node_size=3000, cmap=plt.cm.Blues, alpha=0.6)

print("Hello!")

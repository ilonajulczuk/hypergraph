import netwokx as nx
import itertools


def convert_to_nx_bipartite_graph(vertices, hyper_edges):
    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_nodes_from(hyper_edges)
    for e in hyper_edges:
        for n in e:
            G.add_edge(n, e)
    return G


def convert_to_custom_hyper_G(nodes, edges):
    nodes = [node for node in edges if isinstance(node, tuple)]
    edges = [(node_1, node_2) for node_1, node_2
             in itertools.combinations(edges, 2) if set(node_1) & set(node_2)]
    hyper_G = nx.Graph()
    hyper_G.add_nodes_from(nodes)
    hyper_G.add_edges_from(edges)
    return hyper_G


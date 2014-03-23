import networkx as nx
import itertools


def convert_to_nx_bipartite_graph(nodes, hyper_edges):
    G = nx.Graph()
    G.add_nodes_from(nodes)
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


def convert_to_clique_graph(nodes, hyperedges):
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    edges = []
    for hyperedge in hyperedges:
        for node_1, node_2 in itertools.combinations(hyperedge, 2):
            edges.append((node_1, node_2))
    graph.add_edges_from(edges)
    return graph



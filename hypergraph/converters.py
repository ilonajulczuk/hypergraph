import networkx as nx
import itertools
import pykov


def convert_to_nx_bipartite_graph(nodes, hyper_edges):
    """Convert collections of nodes and hyper_edges to bipartite graph.

    Parameters:
        nodes: collection of nodes
        hyper_edges: collection of hyperedges (subsets of nodes)

    Returns:
        networkx bipartite graph in which every hyper_edge is connected
        to nodes it links as a hyper_edge
    """
    G = nx.Graph()
    G.add_nodes_from(nodes)
    hyper_edges = [tuple(edge) for edge in hyper_edges]
    G.add_nodes_from(hyper_edges)
    for e in hyper_edges:
        for n in e:
            G.add_edge(n, e)
    return G


def convert_to_custom_hyper_G(nodes, hyper_edges):
    """Convert nodes and hyperedges to custom hypergraph represtentation.

    This custom representations is:
        nodes are hyper_edges
        edges are implicit connections between hyper_edges - hyper_edges
            are connected if they have nonempty intersection

    """
    nodes = [node for node in hyper_edges if isinstance(node, tuple)]
    edges = [(tuple(node_1), tuple(node_2)) for node_1, node_2
             in itertools.combinations(hyper_edges, 2)
             if set(node_1) & set(node_2)]
    hyper_G = nx.Graph()
    hyper_G.add_nodes_from(nodes)
    hyper_G.add_edges_from(edges)
    return hyper_G


def convert_to_clique_graph(nodes, hyper_edges):
    """Convert nodes and hyperedges to clique graph.

    In practice clique graph is a graph in which every hyper_edge
        is translated to clique.

    Parameters:
        nodes: collection of nodes (list, tuple or set)
        hyper_edges: collection of subsets of nodes
    """
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    edges = []
    for hyper_edge in hyper_edges:
        for node_1, node_2 in itertools.combinations(hyper_edge, 2):
            edges.append((node_1, node_2))
    graph.add_edges_from(edges)
    return graph


def transition_matrix_to_pykov_chain(matrix):
    chain = pykov.Chain()

    for i, row in enumerate(matrix):
        for j, column in enumerate(row):
            chain[(i, j)] = column
    return chain
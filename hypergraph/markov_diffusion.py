import numpy as np
from collections import defaultdict

from collections import Counter


def create_markov_matrix(edges, count_itself=False):
    """Create transition matrix of Markov chain

    Parameters:
        edges: collection of edges
        count_itself: flag determining if there should be loops

    Algorithm works as follows. Every edge is compared
    with other edges. If they have nonempty intersection,
    appropriate cell in adjacency matrix gets cardinality
    of this intersection.

    If `count_itself` is True, diagonal of adjacency
    matrix has number of nodes in hyperedge that doesn't
    belong to any intersection (leftovers).
    """
    a_matrix = np.zeros((len(edges), len(edges)))

    for i, edge_1 in enumerate(edges):
        not_in_other_edges = set(edge_1)
        for j, edge_2 in enumerate(edges):
            if i != j:
                a_matrix[i][j] = len(set(edge_1) & set(edge_2))
                not_in_other_edges -= set(edge_2)

        if count_itself:
            a_matrix[i][i] = len(not_in_other_edges)

    for i, edge_1 in enumerate(edges):
        a_matrix[i] /= float(sum(a_matrix[i]))

    return a_matrix


def populate_node_hyperedges(hyper_graph):
    """Create a dictionary with nodes V as keys and hyperedges E that E contains V as values"""
    node_hyperedges = defaultdict(list)
    for hyper_edge in hyper_graph.hyper_edges():
        for node in hyper_edge:
            node_hyperedges[node].append(hyper_edge)
    return node_hyperedges


def create_markov_matrix_model_nodes(hyper_graph):

    # create N x N matrix with zeroes
    number_of_nodes = len(hyper_graph.nodes())
    markov_matrix = np.zeros((number_of_nodes, number_of_nodes))

    node_hyper_edges = populate_node_hyperedges(hyper_graph)

    # fill transition matrix with all possible ways to get from V_i to V_j
    for node in hyper_graph.nodes():
        for hyper_edge in node_hyper_edges[node]:
            for node2 in hyper_edge:
                markov_matrix[node - 1, node2 - 1] += 1 / len(hyper_edge) / len(node_hyper_edges[node])

    return markov_matrix


def create_markov_matrix_model_hyper_edges(hyper_graph):

    number_of_edges = len(hyper_graph.hyper_edges())
    node_edges = np.zeros((len(hyper_graph.nodes()), number_of_edges))

    for node in hyper_graph.nodes():
        node_edges[node - 1] = np.array([node in edge for edge in hyper_graph.hyper_edges()])

    markov_matrix = np.zeros((number_of_edges, number_of_edges))

    for i, edge in enumerate(hyper_graph.hyper_edges()):
        for node in edge:
            node_index = node - 1
            for j, contained in enumerate(node_edges[node_index]):
                markov_matrix[i, j] += contained / len(edge) / sum([edge for edge in node_edges[node_index] if edge])

    return markov_matrix


def count_nodes(nodes, edges, occurrences):
    """Given nodes, edges and occurrences of edges,
    return recalculated occurrences of nodes.

    If node is in edge, it get one more occurrence.
    """
    c = Counter()
    for index, count in occurrences:
        for edge in edges[index]:
            c[edge] += count
    for node in nodes:
        if node not in c:
            c[node] = 0
    return c
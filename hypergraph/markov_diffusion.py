import numpy as np

from collections import Counter


def create_markov_matrix(edges, count_itself=False):
    """Create transition matriv of Markov chain

    Parameters:
        edges: collection of edges
        count_itself: flag determining if there should be loops

    Algorithm works as follows. Every edge is compared
    with other edges. If they have nonempty intersection,
    appriopriate cell in adjacency matrix gets cardinality
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
        a_matrix[i] = a_matrix[i] / float(sum(a_matrix[i]))

    return a_matrix


def count_nodes(nodes, edges, occurrences):
    """Given nodes, edges and occurrences of edges,
    return recalculated occurrences of nodes.

    If node is in edge, it get one more occurence.
    """
    c = Counter()
    for index, count in occurrences:
        for edge in edges[index]:
            c[edge] += count
    for node in nodes:
        if node not in c:
            c[node] = 0
    return c



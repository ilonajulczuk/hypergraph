import numpy as np
from collections import Counter
from matplotlib import pyplot as plt
from numpy.random import random_sample
from hypergraph.generators import generate_uniform_hypergraph
from hypergraph.converters import convert_to_nx_bipartite_graph
from hypergraph import utils


def create_balanced_markov_matrix(edges):
    a_matrix = np.zeros([len(edges), len(edges)]) * 10
    for i, edge_1 in enumerate(edges):
        for j, edge_2 in enumerate(edges):
            a_matrix[i][j] = len(set(edge_1) & set(edge_2))
            a_matrix[j][i] = a_matrix[i][j]
    sums = a_matrix.sum(axis=0)
    min_sum = min(sums)
    for i, col_sum in enumerate(sums):
        a_matrix[i][i] -= col_sum - min_sum
    a_matrix *= 1.0 / min_sum
    return a_matrix


def create_markov_matrix(edges):
    a_matrix = np.eye(len(edges))

    for i, edge_1 in enumerate(edges):
        for j, edge_2 in enumerate(edges):
            a_matrix[i][j] = len(set(edge_1) & set(edge_2))
            a_matrix[j][i] = a_matrix[i][j]

    for i, edge_1 in enumerate(edges):
        a_matrix[i] = a_matrix[i] / sum(a_matrix[i]) * 1.1

    return a_matrix


def weighted_values(values, probabilities, size):
    bins = np.add.accumulate(probabilities)
    bins[-1] = max(1, bins[-1])
    index = np.digitize(random_sample(size), bins)
    return values[index]


def step_diffusion(current_state, markov_matrix):
    values_size = len(current_state)
    values = range(values_size)
    probs = markov_matrix.dot(current_state)
    next_state = np.zeros(values_size)
    next_state[weighted_values(values, probs, 1)] = 1

    return next_state


def simulate(current_state, markov_matrix, t_max):
    c = Counter()
    states = []
    for _ in range(t_max):
        current_state = step_diffusion(current_state, markov_matrix)
        visited_hyperedge = current_state.tolist().index(1)
        c[visited_hyperedge] += 1
        states.append(visited_hyperedge)
    return c.most_common(), states


def count_nodes(nodes, edges, occurences):
    c = Counter()
    for index, count in occurences:
        for edge in edges[index]:
            c[edge] += count
    for node in nodes:
        if node not in c:
            c[node] = 0
    return c


def demo():
    n = 20
    k = 3
    fraction = 1.0 / 2
    g = generate_uniform_hypergraph(
        n=n,
        k=k,
        number_of_edges=int(
            n *
            fraction))
    G = convert_to_nx_bipartite_graph(*g)
    plt.figure()
    utils.draw_bipartite_graph(G, *utils.hipergraph_to_bipartite_parts(G))

    markov_matrix = create_markov_matrix(g[1])
    current_state = np.zeros(markov_matrix.shape[0])
    current_state[0] = 1

    t_max = 30

    most_common, states = simulate(current_state, markov_matrix, t_max)

    plt.figure()
    plt.hist(states, normed=True)

    most_common_nodes = count_nodes(g[0], g[1], most_common)

    plt.figure()
    plt.plot(list(most_common_nodes.keys()),
             list(most_common_nodes.values()), 'm:o',
             alpha=0.7, linewidth=5)

    plt.show()


if __name__ == '__main__':
    demo()

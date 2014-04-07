import numpy as np
from scipy import stats

from collections import Counter
from matplotlib import pyplot as plt
from generators import uniform_hypergraph
import converters
import utils


def create_markov_matrix(edges, count_itself=False):
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


def weighted_values(values, probabilities, size):
    custm = stats.rv_discrete(name='custm', values=(values, probabilities))
    R = custm.rvs(size=1)
    return R[0]


def step_diffusion(current_state, markov_matrix):
    values_size = len(markov_matrix)
    values = range(values_size)
    probs = markov_matrix[current_state]
    next_state = weighted_values(values, probs, 1)
    return next_state


def simulate(current_state, markov_matrix, t_max):
    c = Counter()
    states = []
    for _ in range(t_max):
        current_state = step_diffusion(current_state, markov_matrix)
        visited_hyperedge = current_state
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


def compare_hypergraph_with_cliques(number_of_nodes,
                                    cardinality, fraction, t_max,
                                    plot_representations=False):
    HG = uniform_hypergraph(
        n=number_of_nodes,
        k=cardinality,
        number_of_edges=int(
            number_of_nodes *
            fraction))

    nodes = HG.nodes()
    hyperedges = HG.hyper_edges()

    all_nodes = []
    for hyperedge in hyperedges:
        all_nodes += hyperedge
    c = Counter(all_nodes)
    xs, ys = zip(*c.items())
    #plt.bar(xs, ys)

    if plot_representations:
        utils.plot_different_representations(nodes, hyperedges)

    markov_matrix = create_markov_matrix(hyperedges)
    print(markov_matrix)
    current_state = 1
    most_common, states = simulate(current_state, markov_matrix, t_max)

    plt.figure(figsize=(12, 10))
    utils.plot_hyperedges_frequencies(most_common, hyperedges,
                                'Ocurrences of hyperedges in a hypergraph')

    most_common_nodes = count_nodes(nodes, hyperedges, most_common)

    plt.figure(figsize=(12, 10))
    utils.plot_nodes_frequencies(most_common_nodes, 'Nodes in a hypergraph')

    clique_graph = converters.convert_to_clique_graph(nodes, hyperedges)
    clique_markov_matrix = create_markov_matrix(clique_graph.edges())

    print("clique markov matrix")
    print(clique_markov_matrix)
    most_common, states = simulate(current_state, clique_markov_matrix, t_max)

    plt.figure(figsize=(12, 10))
    utils.plot_hyperedges_frequencies(most_common, clique_graph.edges(),
                                'Ocurrences of edges in a graph')

    most_common_nodes = count_nodes(clique_graph.nodes(), clique_graph.edges(),
                                    most_common)
    plt.figure(figsize=(12, 10))
    utils.plot_nodes_frequencies(most_common_nodes, 'Nodes in a graph')


def demo():
    n = 20
    k = 3
    fraction = 2.0 / 3

    for simulation_time in [100]:
        compare_hypergraph_with_cliques(n, k, fraction, simulation_time)


if __name__ == '__main__':
    demo()



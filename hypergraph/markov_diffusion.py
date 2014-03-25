import numpy as np
import networkx as nx
from collections import Counter
from matplotlib import pyplot as plt
from numpy.random import random_sample
from hypergraph.generators import generate_uniform_hypergraph
from hypergraph import converters
from hypergraph import utils


def create_markov_matrix(edges):
    a_matrix = np.zeros((len(edges), len(edges)))

    for i, edge_1 in enumerate(edges):
        for j, edge_2 in enumerate(edges):
            if i != j:
                a_matrix[i][j] = len(set(edge_1) & set(edge_2))

    for i, edge_1 in enumerate(edges):
        a_matrix[i] = a_matrix[i] / float(sum(a_matrix[i]))

    return a_matrix


def weighted_values(values, probabilities, size):
    bins = np.add.accumulate(probabilities)
    bins[-1] = max(1, bins[-1])
    index = np.digitize(random_sample(size), bins)
    return values[index]


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

def plot_nodes_frequencies(most_common_nodes, title):
    plt.figure()
    plt.bar(list(most_common_nodes.keys()),
             list(most_common_nodes.values()),
             alpha=0.7, color='magenta')

    plt.title(title)
    plt.show()


def plot_different_representations(nodes, hyperedges):
    print("Drawing different representations of hypergraph")

    print("Bipartite graph")
    nx_bipartite = converters.convert_to_nx_bipartite_graph(nodes, hyperedges)
    utils.draw_bipartite_graph(nx_bipartite, *utils.hypergraph_to_bipartite_parts(nx_bipartite))

    print("Graph of hypereges as nodes")
    custom_hyper_g = converters.convert_to_custom_hyper_G(nodes, hyperedges)
    plt.figure()
    nx.draw(custom_hyper_g)

    print("Clique graph")
    clique_graph = converters.convert_to_clique_graph(nodes, hyperedges)
    plt.figure()
    nx.draw(clique_graph)


def plot_hyperedges_frequencies(most_common, hyperedges, title):
    plt.figure(figsize=(12, 6))
    hyperedges_indexes, occurences = zip(*most_common)
    plt.bar(hyperedges_indexes, occurences)
    plt.title(title)
    plt.xticks(range(len(hyperedges)), hyperedges)


def compare_hypergraph_with_cliques(number_of_nodes, cardinality, fraction, t_max):
    g = generate_uniform_hypergraph(
        n=number_of_nodes,
        k=cardinality,
        number_of_edges=int(
            number_of_nodes *
            fraction))

    nodes, hyperedges = g

    plot_different_representations(nodes, hyperedges)
    markov_matrix = create_markov_matrix(hyperedges)
    current_state = 1
    most_common, states = simulate(current_state, markov_matrix, t_max)

    plot_hyperedges_frequencies(most_common, hyperedges,
                                'Ocurrences of hyperedges in a hypergraph')

    most_common_nodes = count_nodes(nodes, hyperedges, most_common)

    plot_nodes_frequencies(most_common_nodes, 'Nodes in a hypergraph')

    clique_graph = converters.convert_to_clique_graph(nodes, hyperedges)
    clique_markov_matrix = create_markov_matrix(clique_graph.edges())
    most_common, states = simulate(current_state, clique_markov_matrix, t_max)

    plot_hyperedges_frequencies(most_common, clique_graph.edges(),
                                'Ocurrences of edges in a graph')

    most_common_nodes = count_nodes(clique_graph.nodes(), clique_graph.edges(),
                                    most_common)
    plot_nodes_frequencies(most_common_nodes, 'Nodes in a graph')


def demo():
    n = 20
    k = 3
    fraction = 2.0 / 3

    for simulation_time in [100]:
        compare_hypergraph_with_cliques(n, k, fraction, simulation_time)


if __name__ == '__main__':
    demo()



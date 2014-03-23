import numpy as np
import networkx as nx
from collections import Counter
from matplotlib import pyplot as plt
from numpy.random import random_sample
from hypergraph.generators import generate_uniform_hypergraph
from hypergraph import converters
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

def plot_nodes(most_common_nodes, title):
    plt.figure()
    plt.bar(list(most_common_nodes.keys()),
             list(most_common_nodes.values()),
             alpha=0.7, color='magenta')

    plt.title(title)
    plt.show()

def compare_hypergraph_with_cliques(number_of_nodes, cardinality, fraction, t_max):
    g = generate_uniform_hypergraph(
        n=number_of_nodes,
        k=cardinality,
        number_of_edges=int(
            number_of_nodes *
            fraction))
    G = converters.convert_to_nx_bipartite_graph(*g)

    nodes, hyperedges = g

    print("Drawing different representations of hypergraph")

    print("Bipartite graph")
    utils.draw_bipartite_graph(G, *utils.hipergraph_to_bipartite_parts(G))
    custom_hyper_g = converters.convert_to_custom_hyper_G(*g)

    print("Graph of hypereges as nodes")
    plt.figure()
    nx.draw(custom_hyper_g)

    print("Clique graph")
    clique_graph = converters.convert_to_clique_graph(*g)
    clique_markov_matrix = create_markov_matrix(clique_graph.edges())

    plt.figure()
    nx.draw(clique_graph)


    markov_matrix = create_markov_matrix(g[1])
    current_state = 1
    most_common, states = simulate(current_state, markov_matrix, t_max)

    plt.figure(figsize=(12, 6))
    hyperedges_indexes, occurences = zip(*most_common)
    plt.bar(hyperedges_indexes, occurences)
    plt.title('Ocurrences of hyperedges in a hypergraph')
    plt.xticks(range(len(hyperedges)), hyperedges)

    most_common_nodes = count_nodes(nodes, hyperedges, most_common)

    plot_nodes(most_common_nodes, 'Nodes in a hypergraph')

    most_common, states = simulate(current_state, clique_markov_matrix, t_max)

    plt.figure(figsize=(12, 6))
    edges, occurences = zip(*most_common)
    plt.bar(edges, occurences)
    plt.title('Ocurrences of edges in a graph')
    plt.xticks(range(len(edges)), clique_graph.edges())

    most_common_nodes = count_nodes(clique_graph.nodes(), clique_graph.edges(), most_common)
    plot_nodes(most_common_nodes, 'Nodes in a graph')


def demo():
    plt.xkcd()
    n = 10
    k = 3
    fraction = 2.0 / 3

    for simulation_time in [100, 300, 1000, 10000]:
        compare_hypergraph_with_cliques(n, k, fraction, simulation_time)


if __name__ == '__main__':
    demo()


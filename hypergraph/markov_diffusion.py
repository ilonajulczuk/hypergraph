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


class RandomNextStep():
    def __init__(self, values, probabilities):
        self.prob_density = stats.rv_discrete(name='discrete', values=(values, probabilities))

    def __call__(self):
        return self.prob_density.rvs(size=1)[0]

    def __str__(self):
        return """Next step random variable"""


class DiffusionEngine():
    def __init__(self, markov_matrix):
        self.markov_matrix = markov_matrix
        available_steps = range(len(markov_matrix))
        self.next_steps = {i: RandomNextStep(available_steps,
                                             row) for i, row
                                             in enumerate(markov_matrix[:])}

    def step(self, current_state):
        next_state = self.next_steps[current_state]()
        return next_state

    def simulate(self, current_state, t_max):
        # TODO add multiwalker support
        c = Counter()
        states = []
        for _ in range(t_max):
            current_state = self.step(current_state)
            visited_hyperedge = current_state
            c[visited_hyperedge] += 1
            states.append(visited_hyperedge)
        return c.most_common(), states

    def __str__(self):
        return """DiffusionEngine with transition matrix: %s""" % self.markov_matrix

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
    engine = DiffusionEngine(markov_matrix)
    most_common, states = engine.simulate(current_state, t_max)

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


    engine = DiffusionEngine(markov_matrix)
    most_common, states = engine.simulate(current_state, t_max)

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



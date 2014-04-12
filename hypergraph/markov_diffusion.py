import numpy as np
import random
import pickle
from scipy import stats
import concurrent.futures

from collections import Counter
from matplotlib import pyplot as plt
from hypergraph.generators import uniform_hypergraph
from hypergraph import converters
from hypergraph import utils
import os
import time


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


class RandomNextStep():
    def __init__(self, values, probabilities):
        np.random.seed(os.getpid())
        np.random.seed(os.getpid() + int(time.time() * 100))
        self.prob_density = stats.rv_discrete(name='discrete',
                                              values=(values, probabilities))

    def __call__(self):
        return self.prob_density.rvs(size=1)[0]

    def __str__(self):
        return """Next step random variable"""


class DiffusionEngine():
    def __init__(self, markov_matrix, t_per_walker=None, max_walkers=None):
        self.markov_matrix = markov_matrix
        self.available_steps = range(len(markov_matrix))
        self.next_steps = {i: RandomNextStep(self.available_steps,
                                             row) for i, row
                                             in enumerate(markov_matrix[:])}
        self.t_per_walker = t_per_walker or 10
        self.max_walkers = max_walkers or 4


    def simulate(self, t_max):
        number_of_walkers = t_max / self.t_per_walker
        all_states_per_iteration = []
        all_states = []
        c = Counter()
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_walkers) as executor:
            # Start the load operations and mark each future with its URL

            futures = [executor.submit(_simulate,
                                       pickle.dumps(self.markov_matrix),
                       random.choice(self.available_steps),
                       self.t_per_walker) for _ in range(int(number_of_walkers))]
            for future in concurrent.futures.as_completed(futures):
                states = future.result()
                all_states += states
                all_states_per_iteration.append(states)
        for state in all_states:
            c[state] += 1
        return c.most_common(), all_states_per_iteration


    def __str__(self):
        return """DiffusionEngine with transitions: %s""" % self.markov_matrix


def _simulate(pickled_markov_matrix, current_state, t_max):
    markov_matrix = pickle.loads(pickled_markov_matrix)
    available_steps = range(len(markov_matrix))
    next_steps = {i: RandomNextStep(available_steps,
                                    row) for i, row
                                    in enumerate(markov_matrix[:])}
    def step(current_state):
        next_state = next_steps[current_state]()
        return next_state
    c = Counter()
    states = []
    for _ in range(t_max):
        current_state = step(current_state)
        visited_hyperedge = current_state
        c[visited_hyperedge] += 1
        states.append(visited_hyperedge)
    return states

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



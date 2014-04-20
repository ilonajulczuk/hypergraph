"""
Used definition of entropy:
    S = - k_{\mathrm{B}}\sum_i p_i \ln p_i

"""

import numpy as np

from collections import Counter
from itertools import chain
from hypergraph import utils
from matplotlib import pyplot as plt


from hypergraph.markov_diffusion import (create_markov_matrix,
                                         DiffusionEngine,
                                         count_nodes)


def entropy(pis):
    """Compute entropy given list of stochastic probabilities"""
    return -np.dot(np.log(pis), pis)


def compute_states_per_time(HG, t_max, t_per_walker):
    markov_matrix = create_markov_matrix(HG.hyper_edges())

    engine = DiffusionEngine(markov_matrix, t_per_walker=t_per_walker)

    most_common, states = engine.simulate(t_max)
    plt.show()

    states_per_time = list(zip(*states))

    return states_per_time


def entropy_value(states, nodes, edges):
    """Compute entropy values from states, nodes and edges.

    It recomputes edge occurrences to node occurences.
    It's too much coupled with bipartite model.
    #TODO - decouple it

    """
    cum_states = chain(*states)
    most_common = Counter(cum_states).most_common()
    most_common_nodes = count_nodes(nodes, edges, most_common)
    frequencies = (utils.get_names_and_occurrences(most_common_nodes)[1])
    entropy_value = entropy(frequencies)
    return entropy_value


def compare_entropy(HG, t_max=10000, t_per_walker=100, title=None,
                    filename=None):
    """Simulate diffusion and show how entropy changes in time"""

    nodes = HG.nodes()
    edges = HG.hyper_edges()

    states_per_time = compute_states_per_time(HG, t_max, t_per_walker)
    state_indices = list(range(len(states_per_time))[4:])

    ys = [entropy_value(states_per_time[:i], nodes, edges)
          for i in state_indices]

    plt.plot(state_indices, ys)
    if title:
        plt.title(title)
    if filename:
        plt.savefig(filename)


if __name__ == '__main__':
    k = 3
    f = 1.6

    for n in range(10, 30, 5):
        HG = utils.create_graph(n, k, f)
        filename = 'entropy_h_%s_%s_%s.png' % (n, k, f)
        compare_entropy(HG, filename=filename)


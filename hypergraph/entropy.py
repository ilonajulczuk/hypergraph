import numpy as np

from collections import Counter
from itertools import chain
from hypergraph import utils
from matplotlib import pyplot as plt


from hypergraph.markov_diffusion import (create_markov_matrix,
                                         DiffusionEngine,
                                         count_nodes)


def entropy(pis):
        return -np.dot(np.log(pis), pis)


def compare_entropy(HG, t_max=10000, t_per_walker=100, title=None, filename=None):
    markov_matrix = create_markov_matrix(HG.hyper_edges())
    nodes = HG.nodes()
    edges = HG.hyper_edges()
    engine = DiffusionEngine(markov_matrix, t_per_walker=t_per_walker)

    most_common, states = engine.simulate(t_max)
    most_common_nodes = count_nodes(nodes, edges, most_common)
    plt.show()

    states_per_time = list(zip(*states))


    xs = list(range(len(states_per_time))[4:])
    ys = []
    for i in xs:
        try:
            cum_states = chain(*states_per_time[:i])
            most_common = Counter(cum_states).most_common()
            most_common_nodes = count_nodes(nodes, edges, most_common)
            frequencies = (utils.get_names_and_occurrences(most_common_nodes)[1])
            entropy_value = entropy(frequencies)
            if entropy_value is not float("nan"):
                ys.append(entropy_value)
            else:
                ys.append(-1)

        except:
            ys.append(0)


    plt.plot(xs, ys)
    if title:
        plt.title(title)
    if filename:
        plt.savefig(filename)

# S = - k_{\mathrm{B}}\sum_i p_i \ln p_i \, ,


k = 3
f = 1.6

for n in range(10, 30, 5):
    HG = utils.create_graph(n, k, f)
    filename = 'entropy_h_%s_%s_%s.png' % (n, k, f)
    compare_entropy(HG, filename=filename)

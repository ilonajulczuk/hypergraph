import random
import math
import itertools
from hypergraph.hypergraph_models import HyperGraph


def uniform_hypergraph(n=6, number_of_edges=None, k=3):
    """Generate hypergraph wiht constant cardinality of edges.

    :n - number of nodes,
    :number_of_edges - how many hyper edges will be created,
    :k - cardinality of hyper edges.
    """
    nodes = range(1, n + 1)

    if number_of_edges is None:
        number_of_edges = int(math.sqrt(n))
    hyper_edges = random_combinations(nodes, k, number_of_edges)

    hypergraph = HyperGraph()
    hypergraph.add_nodes_from(nodes)
    hypergraph.add_edges_from(hyper_edges)
    return hypergraph


def random_combinations(set_of_values, cardinality, count):
    all_combinations = list(itertools.combinations(set_of_values,
                                                   cardinality))

    return random.sample(all_combinations, count)


def generic_hypergraph(number_of_nodes, edges_params):
    nodes = range(1, number_of_nodes + 1)

    hyper_edges = []
    for cardinality, count in edges_params:
        edges_subset = random_combinations(nodes, cardinality, count)
        hyper_edges += edges_subset

    hypergraph = HyperGraph()
    hypergraph.add_nodes_from(nodes)
    hypergraph.add_edges_from(hyper_edges)
    return hypergraph






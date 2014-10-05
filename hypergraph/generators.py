import random
import math
from scipy.misc import comb
from hypergraph.hypergraph_models import HyperGraph
from hypergraph.utils import is_connected


def random_combinations(set_of_values, cardinality, count):
    combinations = set()
    if count > comb(len(set_of_values), cardinality):
        raise ValueError('There are less that {count} combinations in {set_of_values} of length {cardinality}'.format(
            count=count, cardinality=cardinality, set_of_values=set_of_values
        ))

    while len(combinations) < count:
        sample = list(set(random.sample(set_of_values, cardinality)))
        sample.sort()
        # sorted and without duplicates
        if len(sample) == cardinality:
            combinations.add(tuple(sample))
    return combinations


def uniform_hypergraph(n=6, number_of_edges=None, k=3, has_to_be_connected=True):
    """Generate hypergraph with constant cardinality of edges.

    :n - number of nodes,
    :number_of_edges - how many hyper edges will be created,
    :k - cardinality of hyper edges.
    """
    nodes = range(1, n + 1)

    if number_of_edges is None:
        number_of_edges = int(math.sqrt(n))

    connected = False

    hypergraph = None
    while not connected and has_to_be_connected:
        hyper_edges = random_combinations(nodes, k, number_of_edges)
        hypergraph = HyperGraph()
        hypergraph.add_nodes_from(nodes)
        hypergraph.add_edges_from(hyper_edges)
        connected = is_connected(hypergraph)

    return hypergraph


def generic_hypergraph(number_of_nodes, edges_params, has_to_be_connected=True):
    nodes = range(1, number_of_nodes + 1)

    connected = False
    hypergraph = None
    while not connected and has_to_be_connected:
        hyper_edges = []
        for cardinality, count in edges_params:
            edges_subset = random_combinations(nodes, cardinality, count)
            hyper_edges += edges_subset

        hypergraph = HyperGraph()

        hypergraph.add_nodes_from(nodes)
        hypergraph.add_edges_from(hyper_edges)
        connected = is_connected(hypergraph)
    return hypergraph






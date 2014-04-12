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
    hyper_edges = random.sample(list(itertools.combinations(nodes, k)),
                                number_of_edges)

    HG = HyperGraph()
    HG.add_nodes_from(nodes)
    HG.add_edges_from(hyper_edges)
    return HG



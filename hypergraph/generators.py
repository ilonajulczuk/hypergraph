import random
import math
import itertools


def generate_uniform_hypergraph(n=6, number_of_edges=None, k=3):
    """Generate hypergraph wiht constant cardinality of edges.

    :n - number of nodes,
    :number_of_edges - how many hyper edges will be created,
    :k - cardinality of hyper edges.
    """
    vertices = range(1, n + 1)

    if number_of_edges is None:
        number_of_edges = int(math.sqrt(n))
    hyper_edges = random.sample(list(itertools.combinations(vertices, k)),
                                number_of_edges)
    return (vertices, hyper_edges)


from matplotlib import pyplot as plt
from collections import Counter


def prediction(graph, model="hypergraph", plot_results=False):
    """Predict diffusion on given graph using `model`.

    Parameters:
        graph: networkx graph or hypergraph
        model: name of model used to compute prediction, currently
        available models are:
            - hypergraph
            - clique
        plot_results: should results be plotted in function?

    Returns:
        list of numbers representing probability of being in given node
    """

    computations = {
        "hypergraph": {
            "prediction": analytical_hypergraph_diffusion,
            "title": "Analytical prediction of diffusion on hypergraph",
        },
        "hypergraph_nodes": {
            "prediction": analytical_hypergraph_diffusion,
            "title": "Analytical prediction of diffusion on hypergraph",
        },
        "hypergraph_edges": {
            "prediction": analytical_hypergraph_edges,
            "title": "Analytical prediction of diffusion on hypergraph using edges",
        },
        "clique": {
            "prediction": analytical_clique_diffusion,
            "title": "Analytical prediction of diffusion on clique",
        }
    }

    if model in computations:
        xs, ys = computations[model]['prediction'](graph)
        title = computations[model]['title']
    else:
        title = None
        xs, ys = [], []
    if plot_results:
        plt.bar(xs, ys)
        plt.title(title)

    return ys


def analytical_clique_diffusion(graph):
    """Predict probabilities of being in a node on graph diffusion

    Parameters:
        graph: networkx graph, should have `degree` method implemented

    Returns:
        tuple of lists: nodes, probabilities
    """
    xs, ys = zip(*graph.degree().items())
    sum_of_ys = sum(ys)
    ys = [float(y) / sum_of_ys for y in ys]
    return xs, ys


def analytical_hypergraph_diffusion(hyper_graph):
    """Predict probabilities of being in a node in a hypergraph

    Parameters:
        hyper_graph: instance of `hypergraph`, should have `nodes` and `hyper_edges`
            methods implemented

    Predict using bipartite model from perspective of nodes.
    """
    nodes = hyper_graph.nodes()
    hyper_edges = hyper_graph.hyper_edges()
    all_nodes = []
    for hyperedge in hyper_edges:
        all_nodes += hyperedge

    c = Counter(all_nodes)
    for node in nodes:
        if node not in all_nodes:
            c[node] = 0

    xs, ys = zip(*c.items())

    sum_of_ys = sum(ys)
    ys = [float(y) / sum_of_ys for y in ys]

    return xs, ys


def analytical_hypergraph_edges(hyper_graph):
    """Predict probabilities for edge model.

    :param hyper_graph to predict diffusion on :
    :return: list of probabilities of ergodic state
    """
    phis = []
    all_phis = 0
    for edge in hyper_graph.hyper_edges():
        edge_cardinality = len(edge)
        phis.append(edge_cardinality)
        all_phis += len(edge_cardinality)

    pis = [phi / all_phis for phi in phis]
    return pis
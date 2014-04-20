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
    if model == "hypergraph":
        xs, ys = analytical_hypergraph_diffusion(graph)
        title = "Analytical prediction on diffusion on hypergraph"
    elif model == "clique":
        xs, ys = analytical_clique_diffusion(graph)
        title = "Analytical prediction of diffusion on clique"
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


def analytical_hypergraph_diffusion(HG):
    """Predict probabilities of being in a node in a hypergraph

    Parameters:
        HG: instance of `hypergraph`, should have `nodes` and `hyper_edges`
            methods implemented

    Predict using bipartite model from perspective of nodes.
    """
    nodes = HG.nodes()
    hyper_edges = HG.hyper_edges()
    all_nodes = []
    for hyperedge in hyper_edges:
        all_nodes += hyperedge

    c = Counter(all_nodes)
    for node in nodes:
        if node not in all_nodes:
            c[node]=0

    xs, ys = zip(*c.items())

    sum_of_ys = sum(ys)
    ys = [float(y) / sum_of_ys for y in ys]

    return xs, ys

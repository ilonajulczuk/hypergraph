from matplotlib import pyplot as plt
from collections import Counter


def prediction(graph, model="hypergraph", plot_results=False):
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


def analytical_clique_diffusion(hypergraph, plot_results=False):
    xs, ys = zip(*hypergraph.degree().items())
    sum_of_ys = sum(ys)
    ys = [float(y) / sum_of_ys for y in ys]
    return xs, ys


def analytical_hypergraph_diffusion(HG):
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


def compute_C(hypergraph):
    nodes = hypergraph.nodes()
    hyper_edges = hypergraph.hyper_edges()

    N = len(nodes)
    M = len(hyper_edges)
    C = np.zeros((N, M))
    for i, node in enumerate(nodes):
        for j, edge in enumerate(hyper_edges):
            if node in edge:
                C[i][j] = 1

    for i in range(N):
        if np.sum(C[i][:]):
            C[i] /= np.sum(C[i][:])
    return C

def compute_D(hypergraph):
    nodes = hypergraph.nodes()
    hyper_edges = hypergraph.hyper_edges()

    N = len(nodes)
    M = len(hyper_edges)
    D = np.zeros((M, N))
    for i, edge in enumerate(hyper_edges):
        for j, node in enumerate(nodes):
            if node in edge:
                D[i][j] = 1
    for i in range(M):
        if np.sum(D[i][:]):
            D[i] /= np.sum(D[i][:])
    return D

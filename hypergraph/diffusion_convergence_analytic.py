import numpy as np
from scipy import stats
from collections import Counter
from matplotlib import pyplot as plt
from generators import uniform_hypergraph
import converters
from markov_diffusion import create_markov_matrix, DiffusionEngine, count_nodes
import utils


def create_graph(number_of_nodes, cardinality, fraction_of_hyperedges):
    HG = uniform_hypergraph(
        n=number_of_nodes,
        k=cardinality,
        number_of_edges=int(
            number_of_nodes *
            fraction_of_hyperedges))

    return HG


def analytical_solution_of_diffusion(nodes, hyperedges, plot_results=False):
    all_nodes = []
    for hyperedge in hyperedges:
        all_nodes += hyperedge

    c = Counter(all_nodes)
    for node in nodes:
        if node not in all_nodes:
            c[node]=0

    xs, ys = zip(*c.items())

    sum_of_ys = sum(ys)
    ys = [float(y) / sum_of_ys for y in ys]

    if plot_results:
        plt.bar(xs, ys)
        plt.title("Analytical prediction on diffusion on hypergraph")

    return ys


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


def simulate_diffusion(hypergraph, markov_matrix, t_max, current_state=1, plot_results=False):
    nodes = hypergraph.nodes()
    hyper_edges = hypergraph.hyper_edges()
    engine = DiffusionEngine(markov_matrix)
    most_common, states = engine.simulate(t_max)
    most_common_nodes = count_nodes(nodes, hyper_edges, most_common)
    if plot_results:
        plt.figure(figsize=(8, 4))
        utils.plot_hyperedges_frequencies(most_common, hyper_edges,
                                'Ocurrences of hyperedges in a hypergraph', normed=True)

        plt.figure(figsize=(8, 4))
        return utils.plot_nodes_frequencies(most_common_nodes, 'Nodes in a hypergraph', normed=True)
    else:
        return utils.get_names_and_occurrences(most_common_nodes)[1]



def diffusion_on_clique(nodes, hyper_edges, t_max, plot_results=False):
    clique_graph = converters.convert_to_clique_graph(nodes, hyper_edges)
    clique_markov_matrix = create_markov_matrix(clique_graph.edges(), count_itself=False)

    engine = DiffusionEngine(clique_markov_matrix)
    most_common, states = engine.simulate(t_max)
    most_common_nodes = count_nodes(clique_graph.nodes(), clique_graph.edges(),
                                    most_common)

    if plot_results:
        plt.figure(figsize=(8, 4))
        utils.plot_hyperedges_frequencies(most_common, clique_graph.edges(),
                                'Ocurrences of edges in a graph')

        plt.figure(figsize=(8, 4))
        return utils.plot_nodes_frequencies(most_common_nodes, 'Nodes in a graph')
    else:
        return utils.get_names_and_occurrences(most_common_nodes)[1]

def analytical_clique_diffusion(hypergraph, plot_results=False):
    xs, ys = zip(*hypergraph.degree().items())
    sum_of_ys = sum(ys)
    ys = [float(y) / sum_of_ys for y in ys]

    if plot_results:
        plt.bar(xs, ys)
        plt.title("Analytical prediction of diffusion on clique")
    return ys


def correct_zero(node):
    if node == 0:
        node += 0.00001
    return node


def compare_to_theory(experimental, theoretical_1, theoretical_2):
    experimental = [correct_zero(node) for node in experimental]
    theoretical_1 = [correct_zero(node) for node in theoretical_1]
    theoretical_2 = [correct_zero(node) for node in theoretical_2]

    return stats.chisquare(experimental, f_exp=[theoretical_1, theoretical_2], axis=1)


def comparing_pipeline(t_max=10000):
    for n in range(5, 6, 5):
        for k in range(3, 4):
            for f in range(80, 81, 10):
                f = float(f) / 100
                # number_of_nodes, cardinality, fraction_of_hyperedges
                print(n, k, f)
                HG = create_graph(n, k, f)
                number_of_nodes = analytical_solution_of_diffusion(HG.nodes(), HG.hyper_edges(), plot_results=False)
                number_of_nodes_clique = analytical_clique_diffusion(HG, plot_results=False)
                markov_matrix_with_itself = create_markov_matrix(HG.hyper_edges(), count_itself=True)
                markov_matrix = create_markov_matrix(HG.hyper_edges(), count_itself=False)

                simulated_n_o_n = simulate_diffusion(HG, markov_matrix, t_max, plot_results=False)
                simulated_n_o_n_i = simulate_diffusion(HG, markov_matrix_with_itself, t_max)

                simulated_n_o_n_c = diffusion_on_clique(HG.nodes(), HG.hyper_edges(), t_max=t_max)

                print(compare_to_theory(simulated_n_o_n, number_of_nodes, number_of_nodes_clique))
                print(compare_to_theory(simulated_n_o_n_i, number_of_nodes, number_of_nodes_clique))
                print(compare_to_theory(simulated_n_o_n_c, number_of_nodes, number_of_nodes_clique))

                print(simulated_n_o_n)
                print(simulated_n_o_n_i)
                print(simulated_n_o_n_c)
                plt.figure(figsize=(12, 10))

                width = 0.15
                plt.bar(HG.nodes(), simulated_n_o_n,
                            width=width, color='crimson',
                            label='Simulated markov hypergraph')

                plt.bar(np.array(HG.nodes()) + width, simulated_n_o_n_i, width,
                            color='burlywood',
                            label='Simulated markov hypergraph with loops')

                plt.bar(np.array(HG.nodes()) + 2 * width, number_of_nodes, width,
                            label='Analytical diffusion model on hypergraph',
                            color="#65df25")

                plt.bar(np.array(HG.nodes()) + 3 * width, simulated_n_o_n_c, width,
                            label='Simulated clique graph')

                plt.bar(np.array(HG.nodes()) + 4 * width, number_of_nodes_clique, width,
                            label='Analytical diffusion model on clique', color="#dcab11")

                plt.legend(loc=0)
                plt.savefig("diffusion.png")
            plt.show()



if __name__ == '__main__':
    comparing_pipeline()

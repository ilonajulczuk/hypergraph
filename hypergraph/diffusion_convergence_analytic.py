import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
from hypergraph import converters
from hypergraph import analytical
from hypergraph.markov_diffusion import (create_markov_matrix,
                                         DiffusionEngine,
                                         count_nodes)
from hypergraph import utils


def diffusion_on_hypergraph(hypergraph, markov_matrix,
                            t_max, plot_results=False):
    """Simulate numerically diffusion on a hypergraph,

    Diffusion is simulated using markov chains.

    """
    nodes = hypergraph.nodes()
    hyper_edges = hypergraph.hyper_edges()

    most_common, most_common_nodes, states = simulate_diffusion(
        nodes, hyper_edges, markov_matrix, t_max)

    if plot_results:
        return plot_diffusion_results(most_common, most_common_nodes,
                               hyper_edges, "hypergraph")
    else:
        return utils.get_names_and_occurrences(most_common_nodes)[1]


def plot_diffusion_results(most_common, most_common_nodes, edges, name):
    plt.figure(figsize=(8, 4))
    utils.plot_hyperedges_frequencies(most_common, edges,
                                      ('Ocurrences of hyperedges in'
                                       ' a {}').format(name),
                                      normed=True)

    plt.figure(figsize=(8, 4))
    return utils.plot_nodes_frequencies(most_common_nodes,
                                        'Nodes in a {}'.format(name),
                                        normed=True)


def simulate_diffusion(nodes, edges, markov_matrix, t_max):
    engine = DiffusionEngine(markov_matrix)
    most_common, states = engine.simulate(t_max)
    most_common_nodes = count_nodes(nodes, edges, most_common)
    return most_common, most_common_nodes, states


def diffusion_on_clique(hypergraph, t_max, plot_results=False):
    nodes = hypergraph.nodes()
    hyper_edges = hypergraph.hyper_edges()
    clique_graph = converters.convert_to_clique_graph(nodes, hyper_edges)
    markov_matrix = create_markov_matrix(clique_graph.edges(),
                                         count_itself=False)
    edges = clique_graph.edges()

    most_common, most_common_nodes, states = simulate_diffusion(
        nodes, edges, markov_matrix, t_max)
    if plot_results:
        return plot_diffusion_results(most_common, most_common_nodes,
                               hyper_edges, "clique")
    else:
        return utils.get_names_and_occurrences(most_common_nodes)[1]


def correct_zero(node):
    if node == 0:
        node += 0.00001
    return node


def compare_to_theory(experimental, theoretical_1, theoretical_2):
    experimental = [correct_zero(node) for node in experimental]
    theoretical_1 = [correct_zero(node) for node in theoretical_1]
    theoretical_2 = [correct_zero(node) for node in theoretical_2]

    return stats.chisquare(experimental,
                           f_exp=[theoretical_1, theoretical_2],
                           axis=1)


def comparing_pipeline(t_max=10000):
    for n in range(30, 31, 5):
        for k in range(4, 5):
            for f in range(90, 101, 10):
                f = float(f) / 100
                # number_of_nodes, cardinality, fraction_of_hyperedges
                print(n, k, f)
                HG = utils.create_graph(n, k, f)
                number_of_nodes = analytical.prediction(HG)
                number_of_nodes_clique = analytical.prediction(HG,
                                                               model="clique")
                markov_matrix_loops = create_markov_matrix(HG.hyper_edges(),
                                                           count_itself=True)
                markov_matrix = create_markov_matrix(HG.hyper_edges(),
                                                     count_itself=False)

                print(markov_matrix)
                print(markov_matrix_loops)
                simulated_n_o_n = diffusion_on_hypergraph(HG, markov_matrix,
                                                          t_max)
                simulated_n_o_n_i = diffusion_on_hypergraph(HG,
                                                       markov_matrix_loops,
                                                       t_max)

                simulated_n_o_n_c = diffusion_on_clique(HG, t_max=t_max)

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

                plt.bar(np.array(HG.nodes()) + 2 * width, number_of_nodes,
                        width,
                        label='Analytical diffusion model on hypergraph',
                        color="#65df25")

                plt.bar(np.array(HG.nodes()) + 3 * width,
                        simulated_n_o_n_c, width,
                        label='Simulated clique graph')

                plt.bar(np.array(HG.nodes()) + 4 * width,
                        number_of_nodes_clique, width,
                        label='Analytical diffusion model on clique',
                        color="#dcab11")

                plt.legend(loc=0)
                plt.savefig("diffusion_%s_%s_%s.png" % (n, k, f))


if __name__ == '__main__':
    comparing_pipeline()

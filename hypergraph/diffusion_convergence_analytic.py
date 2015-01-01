import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
from hypergraph import converters
from hypergraph import analytical
from hypergraph.diffusion_engine import DiffusionEngine
from hypergraph.markov_diffusion import (create_markov_matrix,
                                         count_nodes)
from hypergraph import utils


def diffusion_on_hypergraph(hypergraph, markov_matrix,
                            t_max, plot_results=False):
    """Simulate numerically diffusion on a hypergraph,

    Diffusion is simulated using Markov Chains.

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
    """Plot results of diffusion.

    Parameters:
        most_common: indexes of hyperedges and their frequences
        most_common_nodes: indexes of nodes and their frequences
        edges: names of edge
        name: name of object on which diffusion was simulated, used
            plot title

    Returns:
        probabilities of being in a node

    """
    plt.figure(figsize=(8, 4))
    utils.plot_hyperedges_frequencies(most_common, edges,
                                      ('Occurrences of hyperedges in'
                                       ' a {}').format(name),
                                      normed=True)

    plt.figure(figsize=(8, 4))
    return utils.plot_nodes_frequencies(most_common_nodes,
                                        'Nodes in a {}'.format(name),
                                        normed=True)


def simulate_diffusion(nodes, edges, markov_matrix, t_max):
    """Simulate diffusion using diffusion engine.

    Returns:
        most_common: hyper_edges to their probabilities of occurrences
        most_common_nodes: similar to above, but with nodes
        states: list of states which were visited by workers
    """
    engine = DiffusionEngine(markov_matrix, t_per_walker=100)
    most_common, states = engine.simulate(t_max)
    most_common_nodes = count_nodes(nodes, edges, most_common)
    return most_common, most_common_nodes, states


def diffusion_on_clique(hypergraph, t_max, plot_results=False):
    """Simulate diffusion on corresponding clique graph"""
    nodes = hypergraph.nodes()
    hyper_edges = hypergraph.hyper_edges()
    clique_graph = converters.convert_to_clique_graph(nodes, hyper_edges)

    # TODO change to markov matrix model nodes
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


def correct_zero(value):
    """Add small amount if value is 0.

    Used as workaround of scipy.chisquare bug.
    """
    if value == 0:
        value += 0.00001
    return value


def compare_to_theory(experimental, *theoretical_models):
    """Use chisquare test to evaluate models"""

    # correcting 0 is a workaround of scipy.chisquare bug
    # this bug gives nan in test if there is zero in data
    experimental = [correct_zero(node) for node in experimental]

    for theoretical in theoretical_models:
        theoretical = [correct_zero(node) for node in theoretical]

    return stats.chisquare(experimental,
                           f_exp=theoretical_models,
                           axis=1)


def comparing_pipeline(t_max=10000):
    """Generate various hypergraphs, run diffusion and compare models
    """

    # TODO rewrite to use new hypergraph models with differenty created transition matrices
    for n in range(20, 31, 5):
        for k in range(3, 4):
            for f in range(90, 91, 10):
                f = float(f) / 100
                # number_of_nodes, cardinality, fraction_of_hyperedges
                print(n, k, f)

                HG = utils.create_graph(n, k, f)
                number_of_nodes = analytical.prediction(HG)
                number_of_nodes_clique = analytical.prediction(HG,
                                                               model="clique")

                # TODO change to matrix model nodes
                markov_matrix_loops = create_markov_matrix(HG.hyper_edges(),
                                                           count_itself=True)
                markov_matrix = create_markov_matrix(HG.hyper_edges(),
                                                     count_itself=False)

                simulated_n_o_n = diffusion_on_hypergraph(HG, markov_matrix,
                                                          t_max)
                simulated_n_o_n_i = diffusion_on_hypergraph(HG,
                                                            markov_matrix_loops,
                                                            t_max)

                simulated_n_o_n_c = diffusion_on_clique(HG, t_max=t_max)

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
                plt.savefig("next_diffusion_%s_%s_%s.png" % (n, k, f))


if __name__ == '__main__':
    comparing_pipeline()

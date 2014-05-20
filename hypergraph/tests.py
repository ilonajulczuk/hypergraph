import nose.tools as nt
import os
from IPython.nbformat.current import reads

from hypergraph.markov_diffusion import create_markov_matrix_model_nodes
import hypergraph.generators as generators
from hypergraph.notebook_utils import run_notebook
from hypergraph.diffusion_engine import DiffusionEngine


def test_uniform_generator():
    number_of_nodes = 10
    number_of_edges = 5
    cardinality = 3
    hu = generators.uniform_hypergraph(number_of_nodes, number_of_edges,
                                       cardinality)
    nt.assert_true(hu)
    nt.assert_equals(len(hu.nodes()), number_of_nodes)
    nt.assert_equals(len(hu.hyper_edges()), number_of_edges)
    nt.assert_true(all(len(e) == cardinality for e in hu.hyper_edges()))


def test_generator():
    number_of_nodes = 10
    edges_params = ((2, 3), (3, 4), (4, 8))
    hypergraph = generators.generic_hypergraph(number_of_nodes, edges_params)
    number_of_edges = sum(edge_count for _, edge_count in edges_params)
    nt.assert_equals(number_of_edges, len(hypergraph.hyper_edges()))


def test_notebooks():
    notebooks_path = 'notebooks'
    paths = os.listdir(notebooks_path)
    notebooks_filenames = [notebooks_path + '/' + name
                           for name in paths if name.endswith('.ipynb')]

    for ipynb in notebooks_filenames:
        print("testing %s" % ipynb)
        with open(ipynb) as f:
            nb = reads(f.read(), 'json')
            run_notebook(nb)


def test_diffusion_engine():
    hyper_graph = generators.generic_hypergraph(10, ((3, 2), (4, 3), (5, 3)))

    t_max = 1000
    number_of_walkers = 1
    offset = 10

    markov_matrix = create_markov_matrix_model_nodes(hyper_graph)

    chosen_states = []
    for x in range(10, t_max, offset):
        engine = DiffusionEngine(markov_matrix)
        frequencies, states = engine.simulate(offset)

        chosen_states += states[0]

    nt.assert_equals(len(chosen_states), t_max / number_of_walkers - 10)

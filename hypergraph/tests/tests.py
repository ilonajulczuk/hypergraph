import nose.tools as nt

from hypergraph.markov_diffusion import create_markov_matrix_model_nodes
import hypergraph.generators as generators
from hypergraph.diffusion_engine import DiffusionEngine


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



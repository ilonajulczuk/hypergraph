import pickle
import numpy as np
import nose.tools as nt
from hypergraph.diffusion_engine import (
    simulate, next_value, probabilities_to_distribution
)

from collections import Counter


def test_alternative_diffusion():
    markov_matrix = np.array([[0.2, 0.3, 0.5],
                              [0.1, 0.7, 0.2],
                              [0.2, 0.4, 0.4]])
    pickled_markov_matrix = pickle.dumps(markov_matrix)
    states = simulate(pickled_markov_matrix, 1, 100)
    nt.assert_equals(1, 2)


def test_random_variable():
    probs = [0.2, 0.3, 0.5]

    distribution = probabilities_to_distribution(probs)

    number_of_tries = 100000
    values_count = Counter()
    for _ in range(number_of_tries):
        value = next_value(distribution)
        values_count[value] += 1

    expected_frequencies = {i: probability for i, probability in enumerate(probs)}

    actual_frequencies = {}
    for value, count in values_count.items():
        actual_frequencies[value] = count / number_of_tries

    for x in range(len(probs)):
        nt.assert_almost_equals(actual_frequencies[x], expected_frequencies[x], places=2)

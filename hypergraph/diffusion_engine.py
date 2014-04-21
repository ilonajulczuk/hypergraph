import random
import os
import time
import pickle
import numpy as np
from scipy import stats
import concurrent.futures

from collections import Counter


class RandomNextStep():
    """Abstraction of random next step from given place.

    It's initialized with set of values and their probabilities.
    When called returns one of values with this probability.

    So basically it's a wrapper around discrete random variable.
    """
    def __init__(self, values, probabilities):
        np.random.seed(os.getpid())
        np.random.seed(os.getpid() + int(time.time() * 100))
        self.prob_density = stats.rv_discrete(name='discrete',
                                              values=(values, probabilities))

    def __call__(self):
        return self.prob_density.rvs(size=1)[0]

    def __str__(self):
        return """Next step random variable"""


class DiffusionEngine():
    """DiffusionEngine to simulate diffusion based on Markov Chains
    represent by transition matrix called `markov_matrix`.

    Uses python futures to compute states concurrently.
    """
    def __init__(self, markov_matrix, t_per_walker=None, max_walkers=None):
        self.markov_matrix = markov_matrix
        self.available_steps = range(len(markov_matrix))
        self.next_steps = {i: RandomNextStep(self.available_steps,
                                             row) for i, row
                                             in enumerate(markov_matrix[:])}
        self.t_per_walker = t_per_walker or 10
        self.max_walkers = max_walkers or 4


    def simulate(self, t_max):
        number_of_walkers = t_max / self.t_per_walker
        all_states_per_iteration = []
        all_states = []
        c = Counter()
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_walkers) as executor:
            futures = [executor.submit(_simulate,
                                       pickle.dumps(self.markov_matrix),
                       random.choice(self.available_steps),
                       self.t_per_walker) for _ in range(int(number_of_walkers))]
            for future in concurrent.futures.as_completed(futures):
                states = future.result()
                all_states += states
                all_states_per_iteration.append(states)
        for state in all_states:
            c[state] += 1
        return c.most_common(), all_states_per_iteration


    def __str__(self):
        return """DiffusionEngine with transitions: %s""" % self.markov_matrix


def _simulate(pickled_markov_matrix, current_state, t_max):
    markov_matrix = pickle.loads(pickled_markov_matrix)
    available_steps = range(len(markov_matrix))
    next_steps = {i: RandomNextStep(available_steps,
                                    row) for i, row
                                    in enumerate(markov_matrix[:])}
    def step(current_state):
        next_state = next_steps[current_state]()
        return next_state
    c = Counter()
    states = []
    for _ in range(t_max):
        current_state = step(current_state)
        visited_hyperedge = current_state
        c[visited_hyperedge] += 1
        states.append(visited_hyperedge)
    return states

import random

from collections import Counter


class DiffusionEngine():
    """DiffusionEngine to simulate diffusion based on Markov Chains
    represent by transition matrix called `markov_matrix`.

    Uses python futures to compute states concurrently.
    """
    def __init__(self, markov_matrix):
        self.markov_matrix = markov_matrix
        self.available_steps = range(len(markov_matrix))

    def simulate(self, t_max, current_state=0):
        all_states_per_iteration = []
        all_states = []
        c = Counter()
        states = simulate(self.markov_matrix,
                          current_state,
                          t_max)
        all_states += states
        all_states_per_iteration.append(states)
        for state in all_states:
            c[state] += 1
        return c.most_common(), all_states_per_iteration

    def __str__(self):
        return """DiffusionEngine with transitions: %s""" % self.markov_matrix


def probabilities_to_distribution(discrete_probabilities):
    return [sum(discrete_probabilities[:i]) for i in range(1, len(discrete_probabilities) + 1)]


def simulate(markov_matrix, current_state, t_max):
    state_to_distribution_function = {}
    for i, probabilities in enumerate(markov_matrix):
        state_to_distribution_function[i] = probabilities_to_distribution(probabilities)

    states = []
    state = current_state
    for _ in range(t_max):
        state = next_value(state_to_distribution_function[state])
        states.append(state)

    return states


def next_value(distribution_function):
    prob = random.random()
    return distribution_function.index([x for x in distribution_function if x > prob][0])

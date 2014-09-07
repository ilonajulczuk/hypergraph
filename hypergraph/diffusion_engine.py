import random
import pickle
import concurrent.futures

from collections import Counter


class DiffusionEngine():
    """DiffusionEngine to simulate diffusion based on Markov Chains
    represent by transition matrix called `markov_matrix`.

    Uses python futures to compute states concurrently.
    """
    def __init__(self, markov_matrix, t_per_walker=None, max_walkers=None):
        self.markov_matrix = markov_matrix
        self.t_per_walker = t_per_walker or 10
        self.max_walkers = max_walkers or 4
        self.available_steps = range(len(markov_matrix))

    def simulate(self, t_max):
        #TODO tests and refactor
        number_of_walkers = max(t_max / self.t_per_walker, 1)
        all_states_per_iteration = []
        all_states = []
        c = Counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_walkers) as executor:
            futures = [executor.submit(simulate,
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


def probabilities_to_distribution(discrete_probabilities):
    return [sum(discrete_probabilities[:i]) for i in range(1, len(discrete_probabilities) + 1)]


def simulate(pickled_markov_matrix, current_state, t_max):
    try:
        markov_matrix = pickle.loads(pickled_markov_matrix)
        state_to_distribution_function = {}
        for i, probabilities in enumerate(markov_matrix):
            state_to_distribution_function[i] = probabilities_to_distribution(probabilities)

        states = []
        state = current_state
        for _ in range(t_max):
            state = next_value(state_to_distribution_function[state])
            states.append(state)

        return states
    except:
        import traceback
        traceback.print_exc()
        return []


def next_value(distribution_function):
    prob = random.random()
    return distribution_function.index([x for x in distribution_function if x > prob][0])

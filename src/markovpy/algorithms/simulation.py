from typing import List
import random
from ..chain import Chain


def next_state(chain: Chain, current: str) -> str:
    """
    Return a single next state from `current` according to the chain's
    transition probabilities.

    :param chain: The Markov chain object
    :param current: The current state from which to transition.
    :return: The next state chosen randomly according to probabilities.
    """

    sucs = list(chain.successors(current))
    if not sucs:
        raise ValueError(f"No outgoing transitions from state '{current}'")

    weights = [chain._trans[current][s].get("p", 0) for s in sucs]
    return random.choices(sucs, weights=weights, k=1)[0]


def simulate(chain: Chain, start: str, steps: int) -> List[str]:
    """
    Simulates a path of length 'steps' from 'start'.
    :param chain: The Markov chain object
    :param start: The starting state of the simulation
    :param steps: The number of transitions to simulate
    :return: A list of visited states, including the starting state
    """
    if start not in chain.states:
        raise ValueError(f"State '{start}' is not in the chain")

    route = [start]
    current = start
    for _ in range(steps):
        current = next_state(chain, current)
        route.append(current)
    return route

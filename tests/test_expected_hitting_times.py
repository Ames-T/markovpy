import numpy as np
import markovpy as mp

from markovpy.algorithms import expected_hitting_times


def test_target_state_zero():
    P = [
        [1.0, 0.0],
        [0.5, 0.5],
    ]
    states = ["A", "B"]
    chain = mp.Chain.from_adjacency_matrix(P, states)
    chain.normalise()

    h = expected_hitting_times(chain, target=0)

    assert h[0] == 0.0


def test_two_state_absorbing():
    P = [
        [0.0, 1.0],
        [0.0, 1.0],
    ]
    states = ["A", "B"]
    chain = mp.Chain.from_adjacency_matrix(P, states)
    chain.normalise()

    h = expected_hitting_times(chain, target=1)

    assert np.allclose(h, [1.0, 0.0])


def test_geometric_waiting_time():
    p = 0.75
    P = [
        [p, 1 - p],
        [0.0, 1.0],
    ]
    states = ["A", "B"]
    chain = mp.Chain.from_adjacency_matrix(P, states)
    chain.normalise()

    h = expected_hitting_times(chain, target=1)

    assert np.isclose(h[0], 1 / (1 - p))
    assert h[1] == 0.0


def test_first_step_equation():
    P = [
        [0.2, 0.5, 0.3],
        [0.1, 0.6, 0.3],
        [0.0, 0.0, 1.0],
    ]
    states = ["A", "B", "C"]
    chain = mp.Chain.from_adjacency_matrix(P, states)
    chain.normalise()

    target = 2
    h = expected_hitting_times(chain, target)
    P_np = np.asarray(chain.to_adjacency_matrix())

    for i in range(len(states)):
        if i == target:
            assert h[i] == 0.0
        else:
            rhs = 1 + np.dot(P_np[i], h)
            assert np.isclose(h[i], rhs)

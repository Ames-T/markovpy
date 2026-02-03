import markovpy as mp
from markovpy.algorithms import stationary_distribution
import numpy as np


def test_stationary_linear():
    matrix = [[0.9, 0.1], [0.5, 0.5]]
    chain = mp.Chain.from_adjacency_matrix(matrix)
    pi = stationary_distribution(chain, method="linear")

    # Check that sum is 1
    assert abs(sum(pi.values()) - 1.0) < 1e-12

    # Check stationary property: pi P ≈ pi
    states = list(chain.states)
    P = np.array(chain.to_adjacency_matrix(states=states, dense=True))
    pi_vec = np.array([pi[s] for s in states])
    np.testing.assert_allclose(pi_vec @ P, pi_vec, rtol=1e-12)


def test_stationary_power():

    matrix = [[0.5, 0.5], [0.2, 0.8]]
    chain = mp.Chain.from_adjacency_matrix(matrix)

    # Use power method with reasonable tol and max_iter
    pi = stationary_distribution(chain, method="power", tol=1e-12, max_iter=100000)

    # 1. Probabilities sum to 1
    assert abs(sum(pi.values()) - 1.0) < 1e-12

    # 2. Stationarity: π P ≈ π
    states = list(chain.states)
    P = np.array(chain.to_adjacency_matrix(states=states, dense=True))
    pi_vec = np.array([pi[s] for s in states])
    np.testing.assert_allclose(pi_vec @ P, pi_vec, rtol=1e-10, atol=0)

    # 3. Optional: compare with linear solution
    pi_linear = chain.stationary_distribution(method="linear")
    pi_linear_vec = np.array([pi_linear[s] for s in states])
    np.testing.assert_allclose(pi_vec, pi_linear_vec, rtol=1e-10, atol=0)

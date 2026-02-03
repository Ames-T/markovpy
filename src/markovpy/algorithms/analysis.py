import numpy as np
from markovpy import Chain


def expected_hitting_times(chain: Chain, target: int | str) -> np.ndarray:
    """
    Computes the expected hitting time to a target state.
    :param chain: A normalised MarkovChain object.
    :param target: Target State. Can either be a numerical index or a state label.
    :return: Expected Hitting Times: h[i] = expected steps from i to target
    """

    # Get numerical index
    if isinstance(target, int):
        target_idx = target
    else:
        try:
            target_idx = list(chain.states).index(target)
        except ValueError:
            raise KeyError(f"State {target!r} not in chain")

    # Get adjacency matrix
    P = np.asarray(chain.to_adjacency_matrix())
    n = P.shape[0]

    if not (0 <= target_idx < n):
        raise IndexError("Target index out of range")

    # Build the linear system
    A = np.eye(n)
    b = np.zeros(n)

    for i in range(n):
        if i == target_idx:
            A[i, :] = 0
            A[i, i] = 1
            b[i] = 0
        else:
            # h(i) - sum_j * P[i, j] * h(j) = 1
            A[i, :] = np.eye(n)[i] - P[i, :]
            b[i] = 1.0

    h = np.linalg.solve(A, b)
    return h

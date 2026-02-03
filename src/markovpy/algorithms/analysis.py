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


def stationary_distribution(
    chain: Chain, method: str = "auto", tol: float = 1e-12, max_iter: int = 10000
) -> dict:
    """
    Calculates the stationary distribution of the chain.
    :param chain: A MarkovChain object.
    :param method: "auto", "linear" or "power".
    :param tol: Optional Tolerance.
    :param max_iter: Optional max iterations of Power Method.
    :return: set of stationary distribution.
    """
    n = len(chain.states)
    states = list(chain.states)
    P = np.array(chain.to_adjacency_matrix(states, dense=True), dtype=float)

    if method == "auto":
        if n <= 20:
            method = "linear"
        else:
            method = "power"

    if method == "linear":
        # Solve π P = π  <=> (P.T - I) π^T = 0, sum π_i = 1
        A = P.T - np.eye(n)

        A = np.vstack([A, np.ones(n)])
        b = np.zeros(n + 1)
        b[-1] = 1
        try:
            pi = np.linalg.lstsq(A, b, rcond=None)[0]
            pi = np.clip(pi, 0, None)  # Remove negative small values
            pi /= pi.sum()
        except np.linalg.LinAlgError:
            raise ValueError("Linear algebra soloutio nfailed, try method ='power'")

    elif method == "power":

        row_sums = P.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1
        P = P / row_sums

        pi = np.ones(n) / n
        for _ in range(max_iter):
            pi_next = pi @ P
            if np.linalg.norm(pi_next - pi, 1) < tol:
                pi = pi_next
                break
            pi = pi_next

        pi /= pi.sum()

    return dict(zip(states, pi))

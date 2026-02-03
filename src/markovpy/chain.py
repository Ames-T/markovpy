import numpy as np
from typing import Iterable, Tuple, Any


class Chain:
    """
    A discrete-time Markov chain.

    States are arbitrary hashable python objects.
    Transitions are stored as adjacency dictionaries with attributes, rather than as a matrix.

    This class stores structures only, algorithms are implemented externally.

    :param data: Optional Iterable data, converted to states.
    :param attr: Optional attributes.
    """

    def __init__(self, data: Iterable[str] = None, **attr):
        """
        Entry point for Chain Class.
        :param data: Optional Iterable data, converted to states.
        :param attr: Optional attributes.
        """
        # Chain-Level attributes
        self.chain = dict(attr)

        # State -> state attribute dict
        self._states = {}

        # State -> successor -> transition attribution dict
        self._trans = {}  # Trans Rights

        # Data should be an iterable of state labels
        if data is not None:
            self.add_states_from(data)

    def add_state(self, s, **attr):
        """Add a state to the chain.
        :param s: State to add.
        :param attr: Any other attributes.
        """
        if s not in self._states:
            self._states[s] = {}
            self._trans[s] = {}
        self._states[s].update(attr)

    def add_states_from(self, states: Iterable[str], **attr):
        """Adds multiple states to the chain.
        :param states: Iterable states to add.
        :param attr: Any other attributes.
        """
        for state in states:
            self.add_state(state, **attr)

    def add_transition(self, u, v, p: float | int = None, **attr):
        """Add a transition u -> v to the chain.
        :param u: Transition origin state.
        :param v: Transition target state.
        :param p: Optional probability float.
        :param attr: Any other attributes.
        """
        self.add_state(u)
        self.add_state(v)
        self._trans[u][v] = {"p": p, **attr}  # Optional p value.

    @property
    def states(self) -> set:
        """
        :return: Set of states.
        """
        return self._states.keys()

    def transitions(self, u: str = None):
        """
        Returns transitions from source u.

        If u is none:
            iterate over (u, v, attr).
        Else:
            iterate over (u, v, attr) for fixed u.

        :param u: State to return transitions from (Optional).
        :yields: All transitions v -> u.
        """
        if u is None:
            for u, neighbours in self._trans.items():
                for v, attr in neighbours.items():
                    yield u, v, attr
        else:
            for v, attr in self._trans.get(u, {}).items():
                yield u, v, attr

    def add_transitions_from(self, data: Iterable[Tuple]):
        """
        Adds transitions from an iterable.

        Each element may be:
        (u, v)
        (u, v, p)
        (u, v, attr)
        (u, v, p, attr)

        :param data: Iterable Tuples to add data from.
        :raises ValueError: If not in acceptable form.
        """
        for e in data:
            if len(e) == 2:  # Only (U, V)
                u, v = e
                self.add_transition(u, v)
            elif len(e) == 3:  # Either (U, V, attr or p)
                u, v, third = e
                if isinstance(third, dict):
                    self.add_transition(u, v, **third)
                else:
                    self.add_transition(u, v, p=third)
            elif len(e) == 4:  # (U, V, p, attr)
                u, v, p, attr = e
                self.add_transition(u, v, p=p, **attr)
            else:
                raise ValueError("Invalid transition")

    def successors(self, u: str) -> set:
        """
        Returns all v where u can transition to v.

        :param u: Origin State.
        :return: List of States that u can transition to.
        """
        return self._trans[u].keys()

    def predecessors(self, v: str) -> set:
        """
        Returns all u where u can transition to v.
        :param v: Target state to find transitions.
        :return: List of States that u can transition to.
        """
        return {u for u, neighbors in self._trans.items() if v in neighbors}

    def has_state(self, s: str) -> bool:
        """
        Returns true if s is a state.
        :param s: Possible state to check for.
        :return: If state exists in chain.
        """
        return s in self._states

    def has_transition(self, u: str, v: str) -> bool:
        """
        returns true if u and v are transitions.
        :param u: Origin of transition to find.
        :param v: Target of transition to find.
        :return: If transition exists.
        """
        return u in self._trans and v in self._trans[u]

    def transition_mass(self, u: str, v: str) -> float:
        """
        Return the transition probability from state u to state v

        If there is no outgoing edge from u to v, returns 0
        :param u: Origin of the weight to find
        :param v: Target of the weight to find
        :return:
        """
        return self._trans[u].get(v, 0.0)["p"]

    def out_degree(self, u: str, weight: str = None) -> float:
        """
        Returns the number of outgoing edges if weight is none.
        Else returns the sum of the weight of outgoing edges.
        :param u: State to count weight.
        :param weight: "p" returns sum.
        :return: Sum or count of weights of outgoing edges.
        """
        if weight == "p":
            return sum(attr.get("p", 0) for attr in self._trans[u].values())
        return len(self._trans[u])

    def in_degree(self, v: str, weight: str = None) -> float:
        """
        Returns the number of entering edges if weight is none.
        Else returns the sum of the weight of entering edges.
        :param v: Target state to count weight.
        :param weight: "p" returns sum.
        :return: Sum or count of weight of entering edges.
        """
        deg = 0.0

        for u, neighbours in self._trans.items():
            if v in neighbours:
                if weight == "p":
                    deg += neighbours[v].get("p", 0)
                else:
                    deg += 1

        return deg

    def is_stochastic(self, tol: float = 1e-12) -> bool:
        """
        Returns True if the chain is stochastic.
        :param tol: Optional Tolerance.
        :return: True if chain is stochastic.
        """
        for u, neighbours in self._trans.items():
            if not neighbours:
                continue  # allow absorbing states
            total = sum(attr.get("p", 0) for attr in neighbours.values())
            if abs(total - 1.0) > tol:
                return False
        return True

    def normalise(self):
        """
        Takes the sums of the weights and normalises them to 1
        """
        for u in self._trans:
            total = sum(attr.get("p", 0) for attr in self._trans[u].values())
            if total > 0:
                for v in self._trans[u]:
                    self._trans[u][v]["p"] /= total

    def __len__(self) -> int:
        return len(self._states)

    def __iter__(self) -> Iterable[str]:
        return iter(self._states)

    def __contains__(self, s: str) -> bool:
        return s in self._states

    def __repr__(self) -> str:
        return f"Chain with {len(self)} states and {sum(len(n) for n in self._trans.values())} transitions"

    @classmethod
    def from_adjacency_matrix(
        cls,
        matrix: list[list],
        states: Iterable[str] = None,
        normalise: bool = True,
        validate: bool = True,
    ):
        """
        Constructs a Markov chain from an adjacency matric

        The adjacency matrix is interpreted row-wise

        :param matrix: Sequence of Sequences of non-negative numbers
        :param states: Optional state labels
        :param normalise: Optional, rows of matrix normalised to 1
        :param validate: Optional, validates the matrix for correctness
        :return: Chain
        """
        n = len(matrix)

        if n == 0:
            raise ValueError(f"Matrix {matrix} must be non-empty")

        if validate:
            cls._validate_matrix(matrix, states)

        if states is None:
            states = list(range(n))

        chain = cls()

        for i, row in enumerate(matrix):
            total = sum(row)

            for j, value in enumerate(row):
                if value <= 0:
                    continue

                prob = value / total if normalise else value
                chain.add_transition(states[i], states[j], prob)

        return chain

    @staticmethod
    def _validate_matrix(matrix: list[list], states: list = None):
        """
        Checks if a matrix is valid
        :param matrix: Matrix to check
        :param states: Optional States
        :raises ValueError: if matrix is not valid
        """
        n = len(matrix)

        # Check square
        for row in matrix:
            if len(row) != n:
                raise ValueError(f"Matrix {matrix} must be square")

        # Check states same size as matrix
        if states is not None and len(states) != n:
            raise ValueError(f"Number of states must match matrix dimension")

        # Non-negativity, non-zero
        for row in matrix:
            if any(x < 0 for x in row):
                raise ValueError(f"Matrix entries must be non-negative")
            if sum(row) == 0:
                raise ValueError(f"Matrix rows must be non-zero")

    @staticmethod
    def _validate_transitions(transitions: Iterable, tol: float = 1e-12):
        """
        Validates transitions for validity.
        :param transitions: Iterable of transitions to validate
        :param tol: Optional Tolerance
        :raises ValueError: if transitions is not valid
        """
        for origin, target in transitions.items():
            total = sum(target.values())
            if abs(total - 1.0) > tol:
                raise ValueError(f"Transition {transitions[origin]} must sum to 1")
            if any(p < 0 for p in target.values()):
                raise ValueError(
                    f"Transition {transitions[origin]} must be non-negative"
                )

    def to_adjacency_matrix(
        self, states: list = None, dense: bool = True
    ) -> list[list[float]] | dict[Any, Any]:
        """
        Converts a chain object to an adjacency matrix.
        :param states: Option states.
        :param dense: Bool, if True returns dense matrix.
        :return: Adjacency matrix.
        """
        if states is None:
            states = list(self.states)

        if dense:
            n = len(states)

            matrix = [[0.0 for _ in range(n)] for _ in range(n)]

            state_index = {s: i for i, s in enumerate(states)}

            for i, u in enumerate(states):
                for v in self.successors(u):
                    j = state_index[v]
                    matrix[i][j] = self.transition_mass(u, v)
            return matrix
        else:
            matrix = {}
            for u in states:
                matrix[u] = {v: self.transition_mass(u, v) for v in self.successors(u)}
            return matrix

    @classmethod
    def merge(cls, chain1, chain2, merge_type: str = "add", normalise: bool = True):
        """
        Combines Two chains into a new chain
        :param chain1: First chain to combine.
        :param chain2: Second chain to combine.
        :param merge_type:
        :param normalise:
        :return: New merged Chain.
        """
        merged = cls()

        # add all transitions from chain1
        for u in chain1.states:
            for v in chain1.successors(u):
                merged.add_transition(u, v, chain1.transition_mass(u, v))

        # add all transitions from chain2
        for u in chain2.states:
            for v in chain2.successors(u):
                p2 = chain2.transition_mass(u, v)

                if u not in merged._trans:
                    merged.add_state(u)

                if merge_type == "add":
                    if v in merged.successors(u):
                        # Only sum existing probability
                        merged._trans[u][v]["p"] += p2
                    else:
                        merged.add_transition(u, v, p2)
                else:  # overwrite
                    merged.add_transition(u, v, p2)

        if normalise:
            for u in merged.states:
                total = sum(merged.transition_mass(u, v) for v in merged.successors(u))
                if total > 0:
                    for v in merged.successors(u):
                        merged._trans[u][v]["p"] /= total

        return merged

    def stationary_distribution(
        self, method: str = "auto", tol: float = 1e-12, max_iter: int = 10000
    ) -> set:
        """
        Calculates the stationary distribution of the chain.
        :param method: "auto", "linear" or "power".
        :param tol: Optional Tolerance.
        :param max_iter: Optional max iterations of Power Method.
        :return: set of stationary distribution.
        """
        n = len(self.states)
        states = list(self.states)
        P = np.array(self.to_adjacency_matrix(states, dense=True), dtype=float)

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

class Chain:
    """
    A discrete-time Markov chain.

    States are arbitrary hashable python objects.
    Transitions are stored as adjacency dictionaries with attributes, rather than as a matrix.

    This class stores structures only, algorithms are implemented externally
    """

    def __init__(self, data=None, **attr):
        """
        Entry point for Chain Class
        :param data: Optional data, converted to states.
        :param attr:
        """
        # Chain-Level attributes
        self.chain = dict(attr)

        # State -> state attribute dict
        self._state = {}

        # State -> successor -> transition attribution dict
        self._trans = {}  # Trans Rights

        if data is not None:
            self.add_states_from(data)

    def add_state(self, s, **attr):
        """Add a state to the chain
        :param s: State to add
        :param attr: Any other arguments
        """
        if s not in self._state:
            self._state[s] = {}
            self._trans[s] = {}
        self._state[s].update(attr)

    def add_states_from(self, states, **attr):
        """Adds multiple states to the chain
        :param states: Iterable states to add
        :param attr:  Any other arguments
        """
        for state in states:
            self.add_state(state, **attr)

    def add_transition(self, u, v, p=None, **attr):
        """Add a transition u -> v to the chain
        :param u: Transition origin state
        :param v: Transition target state
        :param p: Probability (optional)
        :param attr: Any other arguments
        """
        self.add_state(u)
        self.add_state(v)
        self._trans[u][v] = {"p": p, **attr}

    @property
    def states(self):
        """
        :return: List of states
        """
        return self._state.keys()

    def transitions(self, u=None):
        """
        Returns transitions

        If u is none:
            iterate over (u, v, attr)
        Else:
            iterate over (u, v, attr) for fixed u

        :param u: State to return transitions of
        """

        if u is None:
            for u, nbrs in self._trans.items():
                for v, attr in nbrs.items():
                    yield u, v, attr
        else:
            for v, attr in self._trans.get(u, {}).items():
                yield u, v, attr

    def add_transitions_from(self, data):
        """
        Adds transitions from an iterable.

        Each element may be:
        (u, v)
        (u, v, p)
        (u, v, attr)
        (u, v, p, attr)

        :param data: Data to convert from
        """

        for e in data:
            if len(e) == 2:
                u, v = e
                self.add_transition(u, v)
            elif len(e) == 3:
                u, v, third = e
                if isinstance(third, dict):
                    self.add_transition(u, v, **third)
                else:
                    self.add_transition(u, v, p=third)
            elif len(e) == 4:
                u, v, p, attr = e
                self.add_transition(u, v, p=p, **attr)
            else:
                raise ValueError("Invalid transition")

    def successors(self, u):
        """
        Returns all v where u can transition to v

        :param u: Origin State
        :return: List of States that u can transition to
        """
        return self._trans[u].keys()

    def predecessors(self, v):
        """
        Returns all u where u can transition to v
        :param v: Target state to find transitions
        """
        for u, nbrs in self._trans.items():
            if v in nbrs:
                yield u

    def has_state(self, s):
        """
        Returns true if s is a state
        :param s: Possible state to check for
        :return: If state exists in chain
        """
        return s in self._state

    def has_transition(self, u, v):
        """
        returns true if u and v are transitions
        :param u: Origin of transition to find
        :param v: Target of transition to find
        :return: If transition exists
        """
        return u in self._trans and v in self._trans[u]

    def transition_mass(self, u, v):
        """
        Return the transition probability from state u to state v

        If there is no outgoing edge from u to v, returns 0
        :param u: Origin of the weight to find
        :param v: Target of the weight to find
        :return:
        """
        return self._trans[u].get(v, 0.0)["p"]

    def out_degree(self, u, weight=None):
        """
        Returns the number of outgoing edges if weight is none.
        Else returns the sum of the weight of outgoing edges
        :param u: State to count weight
        :param weight: "p" returns sum.
        :return: Sum or count of weights of outgoing edges
        """
        if weight == "p":
            return sum(attr.get("p", 0) for attr in self._trans[u].values())
        return len(self._trans[u])

    def in_degree(self, v, weight=None):
        """
        Returns the number of entering edges if weight is none.
        Else returns the sum of the weight of entering edges
        :param v: Target state to count weight
        :param weight: "p" returns sum.
        :return: Sum or count of weight of entering edges
        """
        deg = 0
        for u in self._trans:
            for v in self._trans[u]:
                if weight == "p":
                    deg += self._trans[u][v].get("p", 0)
                else:
                    deg += 1
        return deg

    def is_stochastic(self, tol=1e-12):
        """
        Returns True if the chain is stochastic
        :param tol: Optional Tolerance
        :return: True if chain is stochastic
        """
        for u, nbrs in self._trans.items():
            if not nbrs:
                continue  # allow absorbing states
            total = sum(attr.get("p", 0) for attr in nbrs.values())
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

    def __len__(self):
        return len(self._state)

    def __iter__(self):
        return iter(self._state)

    def __contains__(self, s):
        return s in self._state

    def __repr__(self):
        return f"Chain with {len(self)} states and {sum(len(n) for n in self._trans.values())} transitions"

    @classmethod
    def from_adjacency_matrix(cls, matrix, states=None, normalise=True, validate=True):
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
    def _validate_matrix(matrix, states=None):
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
    def _validate_transitions(transitions, tol=1e-12):
        for origin, target in transitions.items():
            total = sum(target.values())
            if abs(total - 1.0) > tol:
                raise ValueError(f"Transition {transitions[origin]} must sum to 1")
            if any(p < 0 for p in target.values()):
                raise ValueError(
                    f"Transition {transitions[origin]} must be non-negative"
                )

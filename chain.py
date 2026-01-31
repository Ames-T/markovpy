class Chain:
    """
    A discrete-time Markov chain.

    States are arbitrary hashable python objects.
    Transitions are stored as adjacency dictionaries with attributes, rather than as a matrix.

    This class stores structures only, algorithms are implemented externally
    """

    def __init__(self, data=None, **attr):
        # Chain-Level attributes
        self.chain = dict(attr)

        # State -> state attribute dict
        self._state = {}

        # State -> successor -> transition attribution dict
        self._trans = {}  # Trans Rights

        if data is not None:
            self.add_states_from(data)

    def add_state(self, s, **attr):
        """Add a state to the chain"""
        if s not in self._state:
            self._state[s] = {}
            self._trans[s] = {}
        self._state[s].update(attr)

    def add_states_from(self, states, **attr):
        """Adds multiple states to the chain"""
        for state in states:
            self.add_state(state, **attr)

    def add_transition(self, u, v, p=None, **attr):
        """Add a transition u -> v to the chain"""
        self.add_state(u)
        self.add_state(v)
        self._trans[u][v] = {"p": p, **attr}

    @property
    def states(self):
        return self._state.keys()

    def transitions(self, u=None):
        """
        Returns transitions

        If u is none:
            iterate over (u, v, attr)
        Else:
            iterate over (u, v, attr) for fixed u
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
        """
        return self._trans[u].keys()

    def predecessors(self, v):
        """
        Returns all u where u can transition to v
        """
        for u, nbrs in self._trans.items():
            if v in nbrs:
                yield u

    def has_state(self, s):
        """
        Returns true if s is a state
        """
        return s in self._state

    def has_transition(self, u, v):
        """
        returns true if u and v are transitions
        """
        return u in self._trans and v in self._trans[u]

    def out_degree(self, u, weight=None):
        """
        Returns the number of outgoing edges if weight is none.
        Else returns the sum of the weight of outgoing edges
        :param weight: "p" returns sum
        """
        if weight == "p":
            return sum(attr.get("p", 0) for attr in self._trans[u].values())
        return len(self._trans[u])

    def in_degree(self, v, weight=None):
        """
        Returns the number of entering edges if weight is none.
        Else returns the sum of the weight of entering edges
        :param weight: "p" returns sum
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
        """
        for u, nbrs in self._trans.items():
            if not nbrs:
                continue  # allow absorbing states
            total = sum(attr.get("p", 0) for attr in nbrs.values())
            if abs(total - 1.0) > tol:
                return False
        return True

    def normalize(self):
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

MarkovPy
========

A python libray for creating and handling discrete-time markov chains.

This library is heavily inspired by NetworkX

# Installation

A PyPi package is currently in the works, there is an existing library with the name MarkovPy and I will be reaching out to said owner to try to acquire the name.

```pip install MarkovPy```

# Example Usage

The following code snippet creates a empty chain, and populates it with states and transitions, it then normalises it and calculates the communicating classes.

```python
import markovpy as mp
from markovpy.algorithms import communication_classes

c = mp.Chain()

c.add_states_from(["A", "B", "C"])
c.add_transition("A", "B", p=0.5)
c.add_transition("A", "A", p=0.25)
c.add_transition("A", "C", p=0.25)

c.normalise()

print(communication_classes(c))
```
```
[{'A'}, {'B'}, {'C'}]
```

# Current Features

- A Chain class with
  - State and Transition manipulation functions
  - State Accessors and Degree counting functions
  - Stochastic Validation and normalisation

- States algorithms with
  - Absorbing states calculations
  - Transient state calculations
  - Probability weight sum

- Reachability Algorithms with
  - Reachable calculations
  - Communicating calculations
  - Communicating Classes

# Future Features

- Simulation
- Chain generation from historic transitions
- Docs
- PyPi package (Priority)

# Contributing

Contributors welcome

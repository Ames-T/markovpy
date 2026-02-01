MarkovPy
========
[![Tests](https://github.com/Ames-T/markovpy/actions/workflows/wheels.yml/badge.svg)](https://github.com/Ames-T/markovpy/actions/workflows/wheels.yml)

A python libray for creating and handling discrete-time markov chains.

This library is heavily inspired by NetworkX.

# Installation

A PyPi package is currently in the works, there is an existing library with the name MarkovPy and I will be reaching out to the owner to try to acquire the name.

```pip install MarkovPy```

# Example Usage

The following code snippet creates a empty chain, and populates it with states and transitions, it then normalises it and calculates the communicating classes.

```python
import markovpy as mp
from markovpy.algorithms import communication_classes

transition_matrix = [
  [1/2, 1/2, 0.0, 0.0, 0.0, 0.0],
  [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
  [1/3, 0.0, 0.0, 1/3, 0.0, 0.0],
  [0.0, 0.0, 0.0, 1/2, 1/2, 0.0],
  [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
  [0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
]

state_space = ["A", "B", "C", "D", "E", "F"]

c = mp.Chain.from_adjacency_matrix(transition_matrix, state_space)

c.normalise()

print(communication_classes(c))
```
```
[{'C', 'B', 'A'}, {'D'}, {'F', 'E'}]
```

# Current Features

- A Chain class
  - Create, manipulate and access states and transitions.
  - Compute in/out weights and degrees.
  - Validate stochasticity, and normalise probabilities.
  - Create from adjacency matrices.
  - Chain merging, with overlapping or disjoint states.

- States algorithms
  - Absorbing and Transient states calculations.
  - Outgoing probability mass calculations.

- Reachability Algorithms
  - Check reachability between states.
  - Compute communicating states.
  - Identify communicating classes.

- Simulation algorithms:
  - `next_state()` - Sample next state.
  - `simulate()` - Generate path of states

# Future Features

- Chain generation from historic transition data.
- Full documentation
- Publishing to PyPi (Priority)

# Contributing

Contributors welcome!
Please fork the repository, create a feature branch, and submit a pull request.

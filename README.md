MarkovPy
========
[![Tests](https://github.com/Ames-T/markovpy/actions/workflows/wheels.yml/badge.svg)](https://github.com/Ames-T/markovpy/actions/workflows/wheels.yml) ![Trans Rights](https://pride-badges.pony.workers.dev/static/v1?label=Trans+Rights&labelColor=%23555&stripeWidth=8&stripeColors=5BCEFA%2CF5A9B8%2CFFFFFF%2CF5A9B8%2C5BCEFA)

A python libray for creating and handling discrete-time markov chains.

This library is heavily inspired by NetworkX.

# Installation

A PyPI package may be available in future releases. For now, install from source or your own builds.

# Example Usage

The following code snippet creates a empty chain, and populates it with states and transitions, it then normalises it and calculates the communicating classes.

```python
import markovpy as mp
from markovpy.algorithms import communication_classes, stationary_distribution

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
Output:
```python
[{'C', 'B', 'A'}, {'D'}, {'F', 'E'}]
```
Compute the stationary distribution of the chain.
```python
print(c.stationary_distribution())
```
Output:
```python
{'A': 0.0, 'B': 0.0, 'C': 0.0, 'D': 0.0, 'E': 0.5, 'F': 0.5}
```

# Current Features

MarkovPy provides:
- Core Chain representation.
  - Chain class to define states and transitions.
  - Construct Chains from adjacency matrices, or by explicitly adding transitions.
  - Compute weights, degrees and validate or normalise to proper stochastic form.

- State and Reachability.
  - Determine absorbing and transient states.
  - Compute communicating states and communicating classes.
  - Check reachability between states.

- Simulation Algorithms.
  - Sample the next state.
  - Generate sample paths of length.

- Analytic Algorithms.
  - Calculate the stationary distribution.
  - Calculate the expected hitting times.

- Documentation.
  - Dynamic generation of sphinx documentation.


# Future Features

- Extending analytic functions.
- More simulation methods.
- Support for learning transition models from historic data
- Publishing to PyPi (high priority)

# Contributing

Contributors welcome!
Please fork the repository, create a feature branch, and submit a pull request.

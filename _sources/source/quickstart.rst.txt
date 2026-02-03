Quickstart
==========

Install the package locally:

.. code-block:: bash

   pip install markovpy

Create a simple Markov chain:

.. code-block:: python

   import markovpy as mp

   states=["A", "B"]
   transition_matrix=[
        [0.9, 0.1],
        [0.4, 0.6]
   ]
   chain = mp.Chain().from_adjacency_matrix(transition_matrix, state_space)

Simulate a path:

.. code-block:: python

   chain.simulate(start="A", steps=10)

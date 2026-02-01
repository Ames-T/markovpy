import pytest
from markovpy import Chain
from markovpy.algorithms.simulation import next_state, simulate, simulate_until


def test_next_state_randomness():
    c = Chain()
    c.add_states_from(["A", "B"])
    c.add_transition("A", "B", p=0.5)
    c.add_transition("A", "A", p=0.5)
    c.normalise()

    # next_state should return either 'A' or 'B'
    result = next_state(c, "A")
    assert result in {"A", "B"}


def test_next_state_no_outgoing():
    c = Chain()
    c.add_states_from(["A"])
    c.normalise()

    with pytest.raises(ValueError):
        next_state(c, "A")


def test_simulate_trajectory_length():
    c = Chain()
    c.add_states_from(["A", "B"])
    c.add_transition("A", "B", p=1.0)
    c.add_transition("B", "A", p=1.0)
    c.normalise()

    traj = simulate(c, start="A", steps=5)
    # Should include start + steps transitions
    assert len(traj) == 6
    # States should alternate deterministically
    assert traj == ["A", "B", "A", "B", "A", "B"]


def test_simulate_invalid_start():
    c = Chain()
    c.add_states_from(["A"])

    with pytest.raises(ValueError):
        simulate(c, start="B", steps=3)


def test_simulate_until_invalid_start():
    c = Chain()
    c.add_states_from(["A", "B"])

    with pytest.raises(ValueError):
        simulate_until(c, start="A", target="B")


def test_simulate_until_invalid_steps():

    matrix = [
        [0, 1 / 2, 1 / 2],
        [1 / 2, 0, 1 / 2],
        [1 / 2, 1 / 2, 0],
    ]

    c = Chain.from_adjacency_matrix(matrix, states=["A", "B", "C"])
    c.normalise()

    assert len(simulate_until(c, start="A", target="A")) == 1
    assert len(simulate_until(c, start="A", target="B")) >= 1

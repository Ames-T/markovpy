import pytest

from markovpy import Chain
from markovpy.algorithms.states import (
    is_absorbing,
    absorbing_states,
    outgoing_mass,
)


def test_state_with_no_outgoing_transitions_is_absorbing():
    """
    A state with no outgoing transitions should be classified as absorbing.
    """
    c = Chain()
    c.add_state("A")

    assert is_absorbing(c, "A")


def test_self_loop_with_probability_one_is_absorbing():
    """
    A state that transitions only to itself with probability 1
    should be classified as absorbing.
    """
    c = Chain()
    c.add_transition("A", "A", p=1.0)

    assert is_absorbing(c, "A")


def test_self_loop_with_probability_less_than_one_is_not_absorbing():
    """
    A self-loop with probability less than 1 does not define
    an absorbing state if probability mass is missing.
    """
    c = Chain()
    c.add_transition("A", "A", p=0.5)

    assert not is_absorbing(c, "A")


def test_state_with_multiple_successors_is_not_absorbing():
    """
    A state with outgoing transitions to multiple distinct states
    is not absorbing.
    """
    c = Chain()
    c.add_transition("A", "B", p=0.5)
    c.add_transition("A", "A", p=0.5)

    assert not is_absorbing(c, "A")


def test_absorbing_states_collection():
    """
    absorbing_states should return all absorbing states in the chain.
    """
    c = Chain()
    c.add_transition("A", "B", p=1.0)
    c.add_transition("B", "B", p=1.0)
    c.add_state("C")  # isolated state

    result = absorbing_states(c)

    assert result == {"B", "C"}


def test_outgoing_mass_with_probabilities():
    """
    outgoing_mass should return the sum of outgoing transition probabilities.
    """
    c = Chain()
    c.add_transition("A", "B", p=0.3)
    c.add_transition("A", "C", p=0.7)

    assert outgoing_mass(c, "A") == pytest.approx(1.0)


def test_outgoing_mass_missing_probabilities():
    """
    Transitions without explicit probabilities should contribute zero
    to outgoing probability mass.
    """
    c = Chain()
    c.add_transition("A", "B")
    c.add_transition("A", "C")

    assert outgoing_mass(c, "A") == 0.0


def test_outgoing_mass_absent_state():
    """
    outgoing_mass should return zero for states with no outgoing transitions.
    """
    c = Chain()
    c.add_state("A")

    assert outgoing_mass(c, "A") == 0.0


def test_outgoing_mass_mixed_probabilities():
    """
    Only numeric probabilities should contribute to outgoing mass.
    """
    c = Chain()
    c.add_transition("A", "B", p=0.5)
    c.add_transition("A", "C")

    assert outgoing_mass(c, "A") == pytest.approx(0.5)

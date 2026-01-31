import pytest

from markovpy import Chain
from markovpy.algorithms.reachability import (
    reachable,
    communicates,
    communication_classes,
    is_closed,
)


def test_reachable_simple_chain():
    """
    reachable should return all states reachable by directed paths
    from the source state.
    """
    c = Chain()
    c.add_transition("A", "B")
    c.add_transition("B", "C")

    result = reachable(c, "A")

    assert result == {"A", "B", "C"}


def test_reachable_does_not_traverse_against_direction():
    """
    reachable should respect transition direction.
    """
    c = Chain()
    c.add_transition("A", "B")

    result = reachable(c, "B")

    assert result == {"B"}


def test_communicates_true_for_mutual_reachability():
    """
    Two states communicate if each is reachable from the other.
    """
    c = Chain()
    c.add_transition("A", "B")
    c.add_transition("B", "A")

    assert communicates(c, "A", "B")
    assert communicates(c, "B", "A")


def test_communicates_false_for_one_way_reachability():
    """
    Communication requires reachability in both directions.
    """
    c = Chain()
    c.add_transition("A", "B")

    assert not communicates(c, "A", "B")


def test_communication_classes_simple():
    """
    communication_classes should partition the state space into
    communicating equivalence classes.
    """
    c = Chain()
    c.add_transition("A", "B")
    c.add_transition("B", "A")
    c.add_transition("C", "D")
    c.add_transition("D", "D")

    classes = communication_classes(c)
    classes = [set(cls) for cls in classes]

    assert {"A", "B"} in classes
    assert {"C"} in classes
    assert {"D"} in classes


def test_closed_class_true():
    """
    A class is closed if no transitions leave the class.
    """
    c = Chain()
    c.add_transition("A", "B")
    c.add_transition("B", "A")

    cls = {"A", "B"}

    assert is_closed(c, cls)


def test_closed_class_false():
    """
    A class is not closed if any transition leaves the class.
    """
    c = Chain()
    c.add_transition("A", "B")
    c.add_transition("B", "C")

    cls = {"A", "B"}

    assert not is_closed(c, cls)


def test_readme_example():
    c = Chain()

    c.add_states_from(["A", "B", "C"])
    c.add_transition("A", "B", p=0.5)
    c.add_transition("A", "A", p=0.25)
    c.add_transition("A", "C", p=0.25)

    c.normalise()

    assert communication_classes(c) == [{"A"}, {"B"}, {"C"}]

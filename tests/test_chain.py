import pytest

from markovpy import Chain


def test_empty_chain():
    c = Chain()
    assert len(c) == 0
    assert list(c.states) == []
    assert list(c.transitions()) == []


def test_chain_attributes():
    c = Chain(name="test", time_homogeneous=True)
    assert c.chain["name"] == "test"
    assert c.chain["time_homogeneous"] is True


def test_add_state():
    c = Chain()
    c.add_state("A")
    assert "A" in c
    assert c.has_state("A")
    assert len(c) == 1


def test_add_state_with_attributes():
    c = Chain()
    c.add_state("A", absorbing=True)
    assert c._state["A"]["absorbing"] is True


def test_add_states_from():
    c = Chain()
    c.add_states_from(["A", "B", "C"])
    assert set(c.states) == {"A", "B", "C"}


def test_add_transition_adds_states():
    c = Chain()
    c.add_transition("A", "B", p=0.5)

    assert "A" in c
    assert "B" in c
    assert c.has_transition("A", "B")


def test_add_transition_probability():
    c = Chain()
    c.add_transition("A", "B", p=0.25)

    attr = next(attr for _, _, attr in c.transitions())
    assert attr["p"] == 0.25


def test_add_transition_with_attributes():
    c = Chain()
    c.add_transition("A", "B", p=1.0, label="go")

    attr = c._trans["A"]["B"]
    assert attr["p"] == 1.0
    assert attr["label"] == "go"


def test_add_transitions_from_pairs():
    c = Chain()
    c.add_transitions_from(
        [
            ("A", "B"),
            ("B", "C"),
        ]
    )

    assert c.has_transition("A", "B")
    assert c.has_transition("B", "C")


def test_add_transitions_from_weighted():
    c = Chain()
    c.add_transitions_from(
        [
            ("A", "B", 0.3),
            ("A", "C", 0.7),
        ]
    )

    assert c._trans["A"]["B"]["p"] == 0.3
    assert c._trans["A"]["C"]["p"] == 0.7


def test_add_transitions_from_dict_attrs():
    c = Chain()
    c.add_transitions_from(
        [
            ("A", "B", {"p": 1.0, "foo": "bar"}),
        ]
    )

    attr = c._trans["A"]["B"]
    assert attr["p"] == 1.0
    assert attr["foo"] == "bar"


def test_invalid_transition_tuple():
    c = Chain()
    with pytest.raises(ValueError):
        c.add_transitions_from(
            [
                ("A", "B", 0.5, {}, "extra"),
            ]
        )


def test_successors():
    c = Chain()
    c.add_transition("A", "B")
    c.add_transition("A", "C")

    assert set(c.successors("A")) == {"B", "C"}


def test_predecessors():
    c = Chain()
    c.add_transition("A", "C")
    c.add_transition("B", "C")

    assert set(c.predecessors("C")) == {"A", "B"}


def test_out_degree_unweighted():
    c = Chain()
    c.add_transition("A", "B")
    c.add_transition("A", "C")

    assert c.out_degree("A") == 2


def test_out_degree_weighted():
    c = Chain()
    c.add_transition("A", "B", p=0.4)
    c.add_transition("A", "C", p=0.6)

    assert c.out_degree("A", weight="p") == pytest.approx(1.0)


def test_in_degree_unweighted():
    c = Chain()
    c.add_transition("A", "C")
    c.add_transition("B", "C")

    assert c.in_degree("C") == 2


def test_in_degree_weighted():
    c = Chain()
    c.add_transition("A", "C", p=0.25)
    c.add_transition("B", "C", p=0.75)

    assert c.in_degree("C", weight="p") == pytest.approx(1.0)


def test_is_stochastic_true():
    c = Chain()
    c.add_transition("A", "B", p=0.5)
    c.add_transition("A", "C", p=0.5)

    assert c.is_stochastic()


def test_is_stochastic_false():
    c = Chain()
    c.add_transition("A", "B", p=0.3)
    c.add_transition("A", "C", p=0.3)

    assert not c.is_stochastic()


def test_normalize():
    c = Chain()
    c.add_transition("A", "B", p=2.0)
    c.add_transition("A", "C", p=1.0)

    c.normalize()

    assert c._trans["A"]["B"]["p"] == pytest.approx(2 / 3)
    assert c._trans["A"]["C"]["p"] == pytest.approx(1 / 3)
    assert c.is_stochastic()


def test_len_iter_contains():
    c = Chain()
    c.add_states_from(["A", "B"])

    assert len(c) == 2
    assert list(iter(c)) == ["A", "B"]
    assert "A" in c


def test_repr():
    c = Chain()
    c.add_transition("A", "B")
    r = repr(c)

    assert "states" in r
    assert "transitions" in r

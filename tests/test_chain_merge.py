import pytest
from markovpy.chain import Chain


def test_merge_disjoint_chains():
    chain1 = Chain()
    chain1.add_transition("A", "B", p=0.5)
    chain1.add_transition("A", "A", p=0.5)

    chain2 = Chain()
    chain2.add_transition("C", "C", p=1.0)

    merged = Chain.merge(chain1, chain2, merge_type="add")

    # States
    assert set(merged.states) == {"A", "B", "C"}

    # Probabilities
    assert merged.transition_mass("A", "A") == pytest.approx(0.5)
    assert merged.transition_mass("A", "B") == pytest.approx(0.5)
    assert merged.transition_mass("C", "C") == pytest.approx(1.0)


def test_merge_overlapping_add():
    chain1 = Chain()
    chain1.add_transition("X", "Y", p=0.4)
    chain1.add_transition("X", "X", p=0.6)

    chain2 = Chain()
    chain2.add_transition("X", "Y", p=0.5)
    chain2.add_transition("X", "Z", p=0.5)

    merged = Chain.merge(chain1, chain2, merge_type="add", normalise=False)

    # Probabilities should be summed
    assert merged.transition_mass("X", "X") == pytest.approx(0.6)
    assert merged.transition_mass("X", "Y") == pytest.approx(0.9)  # 0.4 + 0.5
    assert merged.transition_mass("X", "Z") == pytest.approx(0.5)


def test_merge_overlapping_overwrite():
    chain1 = Chain()
    chain1.add_transition("A", "B", p=0.3)
    chain1.add_transition("A", "C", p=0.7)

    chain2 = Chain()
    chain2.add_transition("A", "B", p=0.8)
    chain2.add_transition("A", "D", p=0.2)

    merged = Chain.merge(chain1, chain2, merge_type="overwrite", normalise=False)

    # Chain2 should overwrite chain1 for overlapping edges
    assert merged.transition_mass("A", "B") == pytest.approx(0.8)
    assert merged.transition_mass("A", "C") == pytest.approx(0.7)  # still present
    assert merged.transition_mass("A", "D") == pytest.approx(0.2)


def test_merge_normalize():
    chain1 = Chain()
    chain1.add_transition("S", "S", p=2)
    chain1.add_transition("S", "T", p=3)

    chain2 = Chain()
    chain2.add_transition("S", "T", p=5)
    chain2.add_transition("S", "U", p=10)

    merged = Chain.merge(chain1, chain2, merge_type="add", normalise=True)

    total = sum(merged.transition_mass("S", v) for v in merged.successors("S"))
    assert total == pytest.approx(1.0)  # probabilities sum to 1

    # Check relative proportions
    p_S = merged.transition_mass("S", "S")
    p_T = merged.transition_mass("S", "T")
    p_U = merged.transition_mass("S", "U")

    assert p_S == pytest.approx(2 / 20)
    assert p_T == pytest.approx(8 / 20)
    assert p_U == pytest.approx(10 / 20)


def test_merge_sparse_chains():
    chain1 = Chain()
    chain1.add_transition("A", "B", p=1.0)

    chain2 = Chain()
    chain2.add_transition("C", "D", p=1.0)

    merged = Chain.merge(chain1, chain2, merge_type="add")

    # Sparse check
    assert merged.successors("A") == {"B"}
    assert merged.successors("C") == {"D"}

import pytest
from markovpy.chain import Chain


def test_from_adjacency_matrix_basic():
    matrix = [
        [0.2, 0.8],
        [0.5, 0.5],
    ]

    chain = Chain.from_adjacency_matrix(matrix)

    # States
    assert list(chain.states) == [0, 1]

    # Structure
    assert set(chain.successors(0)) == {0, 1}
    assert set(chain.successors(1)) == {0, 1}

    # Probabilities
    assert chain.transition_mass(0, 0) == pytest.approx(0.2)
    assert chain.transition_mass(0, 1) == pytest.approx(0.8)
    assert chain.transition_mass(1, 0) == pytest.approx(0.5)
    assert chain.transition_mass(1, 1) == pytest.approx(0.5)


def test_from_adjacency_matrix_normalises_rows():
    matrix = [
        [1, 3],
        [2, 2],
    ]

    chain = Chain.from_adjacency_matrix(matrix, normalise=True)

    assert set(chain.successors(0)) == {0, 1}
    assert set(chain.successors(1)) == {0, 1}

    assert chain.transition_mass(0, 0) == pytest.approx(0.25)
    assert chain.transition_mass(0, 1) == pytest.approx(0.75)
    assert chain.transition_mass(1, 0) == pytest.approx(0.5)
    assert chain.transition_mass(1, 1) == pytest.approx(0.5)


def test_from_adjacency_matrix_with_states():
    matrix = [
        [0, 1],
        [1, 0],
    ]
    states = ["A", "B"]

    chain = Chain.from_adjacency_matrix(matrix, states=states)

    assert list(chain.states) == ["A", "B"]

    assert set(chain.successors("A")) == {"B"}
    assert set(chain.successors("B")) == {"A"}

    assert chain.transition_mass("A", "B") == 1.0
    assert chain.transition_mass("B", "A") == 1.0


def test_non_square_matrix_raises():
    matrix = [
        [1, 0],
        [0, 1],
        [0, 0],
    ]

    with pytest.raises(ValueError):
        Chain.from_adjacency_matrix(matrix)


def test_negative_entries_raise():
    matrix = [
        [1, -1],
        [0, 1],
    ]

    with pytest.raises(ValueError):
        Chain.from_adjacency_matrix(matrix)


def test_zero_row_raises():
    matrix = [
        [1, 0],
        [0, 0],
    ]

    with pytest.raises(ValueError):
        Chain.from_adjacency_matrix(matrix)


def test_state_length_mismatch_raises():
    matrix = [
        [1, 0],
        [0, 1],
    ]

    with pytest.raises(ValueError):
        Chain.from_adjacency_matrix(matrix, states=["only_one"])

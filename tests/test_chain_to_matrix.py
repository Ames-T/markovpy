import pytest
from markovpy.chain import Chain


def test_matrix_round_trip():
    matrix = [[0.1, 0.9], [0.6, 0.4]]
    chain = Chain.from_adjacency_matrix(matrix)
    round_trip = chain.to_adjacency_matrix()
    assert round_trip == matrix


def test_to_adjacency_matrix_dense():
    matrix = [
        [0.2, 0.8],
        [0.5, 0.5],
    ]
    chain = Chain.from_adjacency_matrix(matrix)

    dense = chain.to_adjacency_matrix()
    # Check shape
    assert len(dense) == 2
    assert all(len(row) == 2 for row in dense)

    # Check values
    assert dense[0][0] == pytest.approx(0.2)
    assert dense[0][1] == pytest.approx(0.8)
    assert dense[1][0] == pytest.approx(0.5)
    assert dense[1][1] == pytest.approx(0.5)


def test_to_adjacency_matrix_sparse():
    matrix = [
        [0.0, 1.0],
        [1.0, 0.0],
    ]
    chain = Chain.from_adjacency_matrix(matrix)

    sparse = chain.to_adjacency_matrix(dense=False)
    # Structure
    assert set(sparse.keys()) == {0, 1}
    assert sparse[0] == {1: 1.0}
    assert sparse[1] == {0: 1.0}


def test_to_adjacency_matrix_custom_order():
    matrix = [
        [0.0, 1.0],
        [1.0, 0.0],
    ]
    states = ["A", "B"]
    chain = Chain.from_adjacency_matrix(matrix, states=states)

    dense_custom = chain.to_adjacency_matrix(states=["B", "A"])
    # Row 0 = B
    assert dense_custom[0][0] == pytest.approx(0.0)  # B→B
    assert dense_custom[0][1] == pytest.approx(1.0)  # B→A
    # Row 1 = A
    assert dense_custom[1][0] == pytest.approx(1.0)  # A→B
    assert dense_custom[1][1] == pytest.approx(0.0)  # A→A

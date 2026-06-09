"""Smoke tests: a tripwire that imports resolve and outputs have the right shape."""

import numpy as np
import pytest

import networkx as nx

from src.connectomes.celegans_cook2019 import load
from src.nulls import (
    random_gaussian,
    erdos_renyi,
    degree_rewire,
    clustering_rewire,
    modularity_rewire,
)
from src.nulls.validation import validate_null
from src.reservoir.weights import apply_weight_scheme
from src.reservoir.build import rescale_spectral_radius


@pytest.fixture(scope="module")
def connectome_adjacency():
    return load().adjacency


def _is_binary(matrix):
    return bool(np.all((matrix == 0) | (matrix == 1)))


def _is_symmetric(matrix):
    return bool(np.allclose(matrix, matrix.T))


def test_load_shape_and_basic_properties(connectome_adjacency):
    assert connectome_adjacency.shape == (300, 300)
    assert _is_binary(connectome_adjacency)
    assert _is_symmetric(connectome_adjacency)
    assert np.all(np.diag(connectome_adjacency) == 0)


@pytest.mark.parametrize(
    "generator",
    [random_gaussian, erdos_renyi, degree_rewire, clustering_rewire, modularity_rewire],
    ids=["random_gaussian", "erdos_renyi", "degree_rewire", "clustering_rewire", "modularity_rewire"],
)
def test_null_returns_symmetric_binary_mask(connectome_adjacency, generator):
    out = generator.generate(connectome_adjacency, seed=0)
    assert out.shape == connectome_adjacency.shape
    assert _is_binary(out)
    assert _is_symmetric(out)
    assert np.all(np.diag(out) == 0)


def test_validate_null_preserved_when_identical(connectome_adjacency):
    result = validate_null(
        connectome_adjacency, connectome_adjacency, "degree_sequence"
    )
    assert result["preserved"] is True


def test_validate_null_flags_violation(connectome_adjacency):
    broken = connectome_adjacency.copy()
    broken[0, :] = 0
    broken[:, 0] = 0
    result = validate_null(connectome_adjacency, broken, "degree_sequence")
    assert result["preserved"] is False


def test_apply_weight_scheme_symmetric_gaussian(connectome_adjacency):
    weighted = apply_weight_scheme(connectome_adjacency, "symmetric_gaussian", seed=0)
    assert weighted.shape == connectome_adjacency.shape
    assert _is_symmetric(weighted)
    assert np.all(np.diag(weighted) == 0)
    nonzero_off_diag = weighted[connectome_adjacency.astype(bool)]
    assert nonzero_off_diag.size > 0
    assert np.any(nonzero_off_diag != 0.0)


def test_clustering_rewire_preserves_degree_and_clustering(connectome_adjacency):
    out = clustering_rewire.generate(connectome_adjacency, seed=0, tolerance=0.05)
    deg_check = validate_null(connectome_adjacency, out, "degree_sequence")
    assert deg_check["preserved"]
    cluster_check = validate_null(connectome_adjacency, out, "clustering", tolerance=0.05)
    assert cluster_check["preserved"]


def test_modularity_rewire_preserves_degree_and_modularity(connectome_adjacency):
    graph = nx.from_numpy_array(connectome_adjacency)
    partition = nx.community.louvain_communities(graph, seed=0)
    out = modularity_rewire.generate(
        connectome_adjacency, seed=0, community_partition=partition
    )
    deg_check = validate_null(connectome_adjacency, out, "degree_sequence")
    assert deg_check["preserved"]
    mod_check = validate_null(
        connectome_adjacency,
        out,
        "modularity",
        tolerance=0.01,
        community_partition=partition,
    )
    assert mod_check["preserved"]


def test_validate_null_modularity_requires_partition(connectome_adjacency):
    with pytest.raises(ValueError):
        validate_null(connectome_adjacency, connectome_adjacency, "modularity")


def test_rescale_spectral_radius(connectome_adjacency):
    weighted = apply_weight_scheme(connectome_adjacency, "symmetric_gaussian", seed=0)
    rescaled = rescale_spectral_radius(weighted, target_spectral_radius=0.95)
    achieved = float(np.max(np.abs(np.linalg.eigvals(rescaled))))
    assert abs(achieved - 0.95) < 1e-9


# ---------------------------------------------------------------------------
# v2b: directed + weighted additions.
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def directed_weighted_adjacency():
    return load(processing="directed_weighted_chemical").adjacency


def test_load_directed_weighted_chemical_shape_and_asymmetry(directed_weighted_adjacency):
    A = directed_weighted_adjacency
    assert A.shape == (300, 300)
    assert not np.allclose(A, A.T), "directed_weighted_chemical must be asymmetric"
    assert np.all(np.diag(A) == 0), "diagonal must be zeroed"
    # Not binarised: should contain values > 1.
    assert (A > 1).sum() > 0, "weights should be raw integer synapse counts, not binarised"
    # Expected directed edge count is in the 3000–5000 range.
    n_directed_edges = int((A != 0).sum())
    assert 3000 <= n_directed_edges <= 5000, (
        f"unexpected directed edge count {n_directed_edges}; expected 3000–5000"
    )


@pytest.mark.parametrize(
    "generator",
    [random_gaussian, erdos_renyi, degree_rewire],
    ids=["random_gaussian", "erdos_renyi", "degree_rewire"],
)
def test_directed_null_returns_asymmetric_binary_mask(directed_weighted_adjacency, generator):
    mask_input = (directed_weighted_adjacency != 0).astype(float)
    out = generator.generate(mask_input, seed=0, directed=True)
    assert out.shape == mask_input.shape
    assert _is_binary(out)
    assert not _is_symmetric(out), f"{generator.__name__} directed=True must be asymmetric"
    assert np.all(np.diag(out) == 0)


def test_directed_degree_rewire_preserves_in_and_out_degree(directed_weighted_adjacency):
    mask_input = (directed_weighted_adjacency != 0).astype(float)
    out = degree_rewire.generate(mask_input, seed=0, directed=True)
    in_check = validate_null(mask_input, out, "in_degree_sequence")
    out_check = validate_null(mask_input, out, "out_degree_sequence")
    assert in_check["preserved"], "in-degree sequence must be preserved by directed rewire"
    assert out_check["preserved"], "out-degree sequence must be preserved by directed rewire"


def test_apply_weight_scheme_asymmetric_empirical(directed_weighted_adjacency):
    mask_input = (directed_weighted_adjacency != 0).astype(float)
    pool = np.array([1.0, 2.0, 5.0, 10.0])
    weighted = apply_weight_scheme(
        mask_input,
        "asymmetric_empirical",
        seed=0,
        empirical_weights=pool,
    )
    assert weighted.shape == mask_input.shape
    assert np.all(np.diag(weighted) == 0)
    # Nonzero pattern matches the mask exactly.
    assert np.array_equal((weighted != 0).astype(float), mask_input)
    # All drawn values are members of the pool.
    drawn = weighted[weighted != 0]
    assert np.all(np.isin(drawn, pool))
    # Likely asymmetric in general (the mask is asymmetric here).
    assert not _is_symmetric(weighted)


# ---------------------------------------------------------------------------
# Directed higher-order nulls (rung 3 + rung 4 extended to directed graphs).
#
# Exercised on a small synthetic directed graph (two communities, each a
# directed circulant carrying directed triangles) so the rewire loops run fast
# and deterministically. The full-scale runs on the C. elegans directed
# connectome happen in the bridge experiment's probe runner.
# ---------------------------------------------------------------------------

_DIRECTED_BLOCK_SIZE = 15


def _two_block_directed_graph() -> np.ndarray:
    """Two 15-node communities, each a directed circulant (i->i+1, i->i+2),
    joined by a few reciprocal inter-block edges. Has directed triangles and
    clear block structure for the rung-3/rung-4 directed tests."""
    block = _DIRECTED_BLOCK_SIZE
    n = 2 * block
    adjacency = np.zeros((n, n))
    for base in (0, block):
        members = [base + k for k in range(block)]
        for position, node in enumerate(members):
            adjacency[node, members[(position + 1) % block]] = 1.0
            adjacency[node, members[(position + 2) % block]] = 1.0
    # A handful of inter-block edges (kept sparse so blocks stay distinct).
    for i, j in [(0, block), (block, 0), (3, block + 5), (block + 6, 4)]:
        adjacency[i, j] = 1.0
    np.fill_diagonal(adjacency, 0)
    return adjacency


def _directed_partition() -> list[set[int]]:
    block = _DIRECTED_BLOCK_SIZE
    return [set(range(block)), set(range(block, 2 * block))]


def test_directed_clustering_rewire_preserves_degree_and_clustering():
    adjacency = _two_block_directed_graph()
    out = clustering_rewire.generate(adjacency, seed=0, directed=True, tolerance=0.05)
    assert out.shape == adjacency.shape
    assert _is_binary(out)
    assert not _is_symmetric(out), "directed rewire output must be asymmetric"
    assert np.all(np.diag(out) == 0)
    in_check = validate_null(adjacency, out, "in_degree_sequence")
    out_check = validate_null(adjacency, out, "out_degree_sequence")
    assert in_check["preserved"], "in-degree sequence must be preserved"
    assert out_check["preserved"], "out-degree sequence must be preserved"
    cluster_check = validate_null(adjacency, out, "directed_clustering", tolerance=0.05)
    assert cluster_check["preserved"], (
        f"directed clustering not preserved within 5% "
        f"(expected={cluster_check['expected']:.4f}, "
        f"actual={cluster_check['actual']:.4f})"
    )


def test_directed_modularity_rewire_preserves_degree_and_block_matrix():
    adjacency = _two_block_directed_graph()
    partition = _directed_partition()
    out = modularity_rewire.generate(
        adjacency, seed=0, directed=True, community_partition=partition
    )
    assert out.shape == adjacency.shape
    assert _is_binary(out)
    assert np.all(np.diag(out) == 0)
    in_check = validate_null(adjacency, out, "in_degree_sequence")
    out_check = validate_null(adjacency, out, "out_degree_sequence")
    assert in_check["preserved"], "in-degree sequence must be preserved"
    assert out_check["preserved"], "out-degree sequence must be preserved"
    block_check = validate_null(
        adjacency, out, "directed_block_matrix", community_partition=partition
    )
    assert block_check["preserved"], "directed block edge-count matrix must be exact"


def test_directed_clustering_rewire_actually_rewires():
    """A sanity check that swaps actually happened (output differs from input)."""
    adjacency = _two_block_directed_graph()
    out = clustering_rewire.generate(adjacency, seed=1, directed=True, tolerance=0.05)
    assert not np.array_equal(out, adjacency), "rewire produced an identical graph"


def test_validate_null_directed_block_matrix_requires_partition():
    adjacency = _two_block_directed_graph()
    with pytest.raises(ValueError):
        validate_null(adjacency, adjacency, "directed_block_matrix")


def test_validate_null_directed_clustering_flags_violation():
    adjacency = _two_block_directed_graph()
    # Identical graphs -> preserved.
    same = validate_null(adjacency, adjacency, "directed_clustering")
    assert same["preserved"] is True
    # Delete every inter-and-intra edge of one node -> clustering changes.
    broken = adjacency.copy()
    broken[0, :] = 0
    broken[:, 0] = 0
    changed = validate_null(adjacency, broken, "directed_clustering", tolerance=0.001)
    assert changed["preserved"] is False

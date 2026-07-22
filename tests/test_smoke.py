"""Smoke tests: a tripwire that imports resolve and outputs have the right shape."""

import numpy as np
import pytest

import networkx as nx

from src.connectomes.celegans_cook2019 import load
from src.connectomes.neurotransmitters import load_neuron_signs, _cell_in_class
from src.nulls import (
    random_gaussian,
    erdos_renyi,
    degree_rewire,
    clustering_rewire,
    modularity_rewire,
)
from src.nulls.validation import validate_null
from src.reservoir.weights import apply_weight_scheme
from src.reservoir.build import rescale_spectral_radius, build_from_adjacency
from src.tasks import narma as narma_task
from src.tasks import mackey_glass as mackey_glass_task
from src.tasks import lorenz as lorenz_task
from src.tasks.memory_capacity import _measure as _mc_measure


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


def test_memory_capacity_downdate_matches_direct(connectome_adjacency):
    """The Gram-down-date MC measure reproduces a direct per-lag recomputation
    (the optimisation must be numerically equivalent, not just faster)."""
    from scipy.stats import pearsonr

    weighted = apply_weight_scheme(connectome_adjacency, "symmetric_gaussian", seed=0)
    reservoir = build_from_adjacency(
        weighted, target_spectral_radius=1.5, leak_rate=1.0, input_scaling=1.0, seed=0
    )
    params = dict(T=600, warmup=100, max_lag=8, ridge_alpha=1e-6, input_scaling=1.0)
    mc_downdate, _, _ = _mc_measure(reservoir, seed=1000, **params)

    # Reference: rebuild the Gram from scratch each lag (the pre-optimisation form).
    rng = np.random.default_rng(1000)
    u = rng.uniform(-1.0, 1.0, size=(params["T"], 1))
    reservoir.reset()
    S = reservoir.run(u)[params["warmup"]:]
    uf = u[params["warmup"]:, 0]
    n, N = S.shape
    mc_direct = 0.0
    for k in range(1, params["max_lag"] + 1):
        X = S[k:]
        y = uf[: n - k]
        w = np.linalg.solve(X.T @ X + params["ridge_alpha"] * np.eye(N), X.T @ y)
        pred = X @ w
        if np.std(pred) >= 1e-12 and np.std(y) >= 1e-12:
            mc_direct += pearsonr(pred, y)[0] ** 2

    assert mc_downdate > 0.0  # a real reservoir has nonzero linear memory
    assert np.isclose(mc_downdate, mc_direct, rtol=1e-7, atol=1e-7)


# ---------------------------------------------------------------------------
# directed_empirical: directed + weighted additions.
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


def test_apply_weight_scheme_asymmetric_empirical_signed(directed_weighted_adjacency):
    mask_input = (directed_weighted_adjacency != 0).astype(float)
    n = mask_input.shape[0]
    pool = np.array([1.0, 2.0, 5.0, 10.0])
    rng = np.random.default_rng(0)
    signs = rng.choice([-1.0, 1.0], size=n)
    weighted = apply_weight_scheme(
        mask_input,
        "asymmetric_empirical_signed",
        seed=0,
        empirical_weights=pool,
        neuron_signs=signs,
    )
    assert weighted.shape == mask_input.shape
    assert np.all(np.diag(weighted) == 0)
    # Nonzero pattern matches the mask exactly.
    assert np.array_equal((weighted != 0).astype(float), mask_input)
    # Magnitudes are drawn from the pool.
    assert np.all(np.isin(np.abs(weighted[weighted != 0]), pool))
    # Dale's principle: every outgoing synapse of neuron j (column j) carries
    # neuron j's sign. Check each column that has any edges.
    for j in range(n):
        col = weighted[:, j]
        nonzero = col[col != 0]
        if nonzero.size:
            assert np.all(np.sign(nonzero) == signs[j]), f"column {j} violates Dale sign"


def test_apply_weight_scheme_asymmetric_empirical_signed_requires_kwargs(
    directed_weighted_adjacency,
):
    mask_input = (directed_weighted_adjacency != 0).astype(float)
    n = mask_input.shape[0]
    with pytest.raises(ValueError):  # missing neuron_signs
        apply_weight_scheme(
            mask_input, "asymmetric_empirical_signed", seed=0,
            empirical_weights=np.array([1.0, 2.0]),
        )
    with pytest.raises(ValueError):  # missing empirical_weights
        apply_weight_scheme(
            mask_input, "asymmetric_empirical_signed", seed=0,
            neuron_signs=np.ones(n),
        )
    with pytest.raises(AssertionError):  # wrong-length sign vector
        apply_weight_scheme(
            mask_input, "asymmetric_empirical_signed", seed=0,
            empirical_weights=np.array([1.0]), neuron_signs=np.ones(n - 1),
        )
    with pytest.raises(AssertionError):  # non +/-1 signs
        apply_weight_scheme(
            mask_input, "asymmetric_empirical_signed", seed=0,
            empirical_weights=np.array([1.0]), neuron_signs=np.zeros(n),
        )


# ---------------------------------------------------------------------------
# NARMA-10 task.
# ---------------------------------------------------------------------------


def test_narma10_matches_reservoirpy():
    """The local generator reproduces reservoirpy.datasets.narma bit-for-bit."""
    from reservoirpy.datasets import narma as rpy_narma

    rng = np.random.default_rng(0)
    order = 10
    length = 600
    u = rng.uniform(0, 0.5, size=(length, 1))
    _, y_rpy = rpy_narma(
        n_timesteps=length - order, order=10, a1=0.3, a2=0.05, b=1.5, c=0.1, u=u
    )
    y_mine = narma_task.narma10(u.ravel())
    assert np.array_equal(y_mine[order:], y_rpy.ravel())


def _narma_test_reservoir():
    conn = load("binary_undirected_chemical").adjacency
    weighted = apply_weight_scheme(conn, "symmetric_gaussian", seed=0)
    return build_from_adjacency(
        weighted, target_spectral_radius=0.9, leak_rate=1.0, input_scaling=0.2, seed=0
    )


def test_narma_evaluate_runs_and_returns_config():
    out = narma_task.evaluate(
        _narma_test_reservoir(), seed=1000, T=1500, washout=200, n_train=900, n_test=400
    )
    assert np.isfinite(out["nrmse"])
    assert 0.0 < out["nrmse"] < 1.5
    for key in ("n_input", "n_train", "n_test", "n_rejected_inputs", "ridge_alpha"):
        assert key in out


def test_narma_evaluate_rejects_oversized_split():
    with pytest.raises(ValueError):
        narma_task.evaluate(
            _narma_test_reservoir(), seed=0, T=1000, washout=200, n_train=700, n_test=200
        )


# ---------------------------------------------------------------------------
# Mackey-Glass task.
# ---------------------------------------------------------------------------


def test_mackey_glass_matches_reservoirpy():
    """The local generator reproduces reservoirpy.datasets.mackey_glass bit-for-bit."""
    from reservoirpy.datasets import mackey_glass as rpy_mackey_glass

    tau = 17
    history_length = int(np.floor(tau / 1.0))
    rng = np.random.default_rng(0)
    history = 1.2 * np.ones(history_length) + 0.2 * (rng.random(history_length) - 0.5)
    # Pass the SAME explicit history to both -> deterministic, RNG-independent
    # bit-exact check (the analogue of NARMA's shared explicit input u).
    y_mine = mackey_glass_task.mackey_glass(2000, history, tau=tau)
    y_rpy = rpy_mackey_glass(2000, tau=tau, history=history).ravel()
    assert np.array_equal(y_mine, y_rpy)
    assert y_mine[0] == 1.2  # first sample is x0, matching reservoirpy's convention


def _mackey_glass_test_reservoir():
    conn = load("binary_undirected_chemical").adjacency
    weighted = apply_weight_scheme(conn, "symmetric_gaussian", seed=0)
    return build_from_adjacency(
        weighted, target_spectral_radius=0.95, leak_rate=0.3, input_scaling=0.5, seed=0
    )


def test_mackey_glass_evaluate_runs_and_returns_config():
    out = mackey_glass_task.evaluate(
        _mackey_glass_test_reservoir(), seed=1000,
        T=1500, washout=200, n_train=900, n_test=400, horizon=84,
    )
    assert np.isfinite(out["nrmse"])
    assert 0.0 < out["nrmse"] < 1.5
    for key in ("n_input", "n_train", "n_test", "horizon", "ridge_alpha"):
        assert key in out
    assert out["horizon"] == 84


def test_mackey_glass_evaluate_rejects_oversized_split():
    with pytest.raises(ValueError):
        mackey_glass_task.evaluate(
            _mackey_glass_test_reservoir(), seed=0,
            T=1000, washout=200, n_train=700, n_test=200,
        )


def test_mackey_glass_sanity_gate_passes():
    """The dormant validate=True gate must run and pass on a working setup."""
    out = mackey_glass_task.evaluate(
        _mackey_glass_test_reservoir(), seed=1000,
        T=1500, washout=200, n_train=900, n_test=400, horizon=84,
        validate=True, sanity_horizon=17, sanity_max_nrmse=0.8,
    )
    assert np.isfinite(out["nrmse"])


# ---------------------------------------------------------------------------
# Lorenz: closed-loop free-running (3-D, two metrics).
# ---------------------------------------------------------------------------
def test_lorenz_rk4_matches_reservoirpy_short_horizon():
    """The local RK4 generator integrates the same Lorenz vector field as
    reservoirpy. Bit-exactness is impossible (reservoirpy uses adaptive
    solve_ivp/RK45 on a non-constant grid, and Lorenz chaos decorrelates any two
    integrators within a few Lyapunov times), so this asserts *short-horizon*
    agreement: matched initial condition and (near-matched) step, close over the
    first ~50 steps before chaos amplifies the integrator difference."""
    from reservoirpy.datasets import lorenz as rpy_lorenz

    mine = lorenz_task.lorenz_rk4(300, x0=[1.0, 1.0, 1.0])
    # Large n so reservoirpy's grid step n*h/(n-1) ~ h; compare the first slice.
    rpy = rpy_lorenz(10000, x0=[1.0, 1.0, 1.0], h=0.03)[:300]
    diff = np.linalg.norm(mine - rpy, axis=1)
    assert np.allclose(mine[0], [1.0, 1.0, 1.0])  # row 0 is the initial condition
    # First few steps agree very tightly (correct vector field + integration);
    # the RK4-vs-RK45 truncation difference then settles to ~0.2 and stays there
    # until chaos decorrelates the two integrators well past this window. State
    # scale is ~20, so these are ~0.05% / ~1% relative.
    assert diff[:6].max() < 0.01
    assert diff[:200].max() < 0.3


def _lorenz_test_reservoir():
    conn = load("binary_undirected_chemical").adjacency
    weighted = apply_weight_scheme(conn, "symmetric_gaussian", seed=0)
    return build_from_adjacency(
        weighted, target_spectral_radius=0.95, leak_rate=1.0, input_scaling=0.1,
        seed=0, input_dim=3,
    )


# A tiny but non-trivial closed-loop protocol for the smoke tests.
_LORENZ_SMOKE = dict(
    n_transient=200, washout=100, n_train=1500, sync_len=100, n_windows=3,
    window_spacing=300, free_run_len=400, climate_len=1000, climate_washout=200,
)


def test_lorenz_evaluate_runs_and_returns_both_metrics():
    out = lorenz_task.evaluate(_lorenz_test_reservoir(), seed=1000, **_LORENZ_SMOKE)
    assert np.isfinite(out["vpt"]) and out["vpt"] >= 0.0
    # vpt is bounded by the roll-out length (in Lyapunov time); never blows up.
    assert out["vpt"] <= _LORENZ_SMOKE["free_run_len"] * 0.03 * lorenz_task.LAMBDA_MAX + 1e-6
    # climate is finite-or-inf; a working canonical reservoir stays bounded here.
    assert np.isfinite(out["climate_error"])
    for key in ("vpt", "climate_error", "n_train", "epsilon", "free_run_len"):
        assert key in out


def test_lorenz_sanity_gate_passes():
    """The validate=True gate must run and pass on a working closed-loop setup."""
    out = lorenz_task.evaluate(
        _lorenz_test_reservoir(), seed=1000, validate=True, sanity_min_vpt=0.3,
        **_LORENZ_SMOKE,
    )
    assert np.isfinite(out["vpt"])


# ---------------------------------------------------------------------------
# directed_empirical_dale (Dale): per-neuron Dale sign vector.
# ---------------------------------------------------------------------------

_CANONICAL_GABA = (
    [f"DD0{i}" for i in range(1, 7)]
    + [f"VD{i:02d}" for i in range(1, 14)]
    + ["RMED", "RMEL", "RMER", "RMEV", "AVL", "DVB", "RIS"]
)


def test_cell_in_class_membership():
    # positives
    assert _cell_in_class("DD01", "DD")
    assert _cell_in_class("VD13", "VD")
    assert _cell_in_class("RMED", "RME")
    assert _cell_in_class("AVL", "AVL")
    assert _cell_in_class("ADFL", "ADF")
    # negatives: cholinergic look-alikes must NOT match the GABA classes
    assert not _cell_in_class("VB01", "VD")
    assert not _cell_in_class("DA01", "DD")
    assert not _cell_in_class("AVAL", "AVL")
    assert not _cell_in_class("RMDL", "RME")


def test_load_neuron_signs_canonical_gaba():
    labels = load(processing="directed_weighted_chemical").node_labels
    signs, coverage = load_neuron_signs(labels)
    assert signs.shape == (len(labels),)
    assert set(np.unique(signs).tolist()) <= {-1.0, 1.0}
    # The inhibitory set is exactly the 26 canonical GABA-synthesizing cells.
    assert coverage["n_inhibitory"] == 26
    assert set(coverage["inhibitory_labels"]) == set(_CANONICAL_GABA)
    assert coverage["n_excitatory"] == len(labels) - 26
    # Signs align to node order.
    for label in _CANONICAL_GABA:
        assert signs[labels.index(label)] == -1.0


def test_neuron_signs_feed_signed_weight_scheme():
    conn = load(processing="directed_weighted_chemical")
    signs, _ = load_neuron_signs(conn.node_labels)
    mask = (conn.adjacency != 0).astype(float)
    pool = np.array([1.0, 2.0, 5.0])
    weighted = apply_weight_scheme(
        mask, "asymmetric_empirical_signed", seed=0,
        empirical_weights=pool, neuron_signs=signs,
    )
    # Inhibitory neurons' out-columns are non-positive; excitatory non-negative.
    for j, s in enumerate(signs):
        col = weighted[:, j]
        nz = col[col != 0]
        if nz.size:
            assert np.all(np.sign(nz) == s)


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


# ---------------------------------------------------------------------------
# Spectral analysis (src/analysis/spectral.py).
# ---------------------------------------------------------------------------


def test_spectral_metrics_shape_and_scale_invariance():
    from src.analysis import spectral

    rng = np.random.default_rng(0)
    W = rng.standard_normal((50, 50))
    m = spectral.spectral_metrics(W)
    for key in ("spectral_radius", "lambda2_ratio", "bulk95_ratio", "mean_ratio",
                "participation_ratio", "n_critical"):
        assert key in m
    assert 0.0 <= m["bulk95_ratio"] <= 1.0
    assert 0.0 <= m["lambda2_ratio"] <= 1.0
    # The ratio metrics are scale-invariant (the reservoir rescales W); only the
    # raw spectral_radius scales with the matrix.
    m2 = spectral.spectral_metrics(3.0 * W)
    assert np.isclose(m2["bulk95_ratio"], m["bulk95_ratio"])
    assert np.isclose(m2["mean_ratio"], m["mean_ratio"])
    assert np.isclose(m2["spectral_radius"], 3.0 * m["spectral_radius"])


def test_spectral_metrics_compression_ordering():
    """A one-dominant-mode matrix is more compressed than a full random one."""
    from src.analysis import spectral

    rng = np.random.default_rng(1)
    full = rng.standard_normal((40, 40))
    v = rng.standard_normal((40, 1))
    dominant = 5.0 * (v @ v.T) + 0.01 * rng.standard_normal((40, 40))
    assert (spectral.spectral_metrics(dominant)["bulk95_ratio"]
            < spectral.spectral_metrics(full)["bulk95_ratio"])


def test_spectral_normalized_eigenvalues_and_decay():
    from src.analysis import spectral

    rng = np.random.default_rng(2)
    W = rng.standard_normal((30, 30))
    assert np.isclose(np.abs(spectral.normalized_eigenvalues(W)).max(), 1.0)
    decay = spectral.magnitude_decay(W)
    assert np.isclose(decay[0], 1.0)
    assert np.all(np.diff(decay) <= 1e-12)  # descending


# ---------------------------------------------------------------------------
# Divergence-robust statistics (src/experiment/stats.py).
# ---------------------------------------------------------------------------


def test_robustify_caps_blowups_and_flags_divergence():
    from src.experiment import stats

    vals = np.array([0.4, 0.5, np.inf, 7.0, 0.45])
    capped, diverged = stats._robustify(vals, cap=2.0, lower_is_better=True)
    assert np.all(np.isfinite(capped)) and capped.max() <= 2.0
    assert diverged.tolist() == [False, False, True, True, False]
    assert np.isclose(diverged.mean(), 0.4)
    # with no cap, only non-finite counts as divergence
    _, div_nocap = stats._robustify(vals, cap=None, lower_is_better=True)
    assert div_nocap.tolist() == [False, False, True, False, False]


def test_cliffs_delta_robust_to_blowup():
    from src.experiment import stats

    connectome = np.array([0.5, 0.5, 0.5, 0.5])
    worse = np.array([0.9, 0.9, 0.9, 0.9])
    assert stats.cliffs_delta(connectome, worse, lower_is_better=True) == 1.0
    # a blown-up null (capped) is still strictly worse -> connectome wins on ranks
    capped, _ = stats._robustify(np.array([7.0, np.inf, 5.0, 9.0]), 2.0, True)
    assert stats.cliffs_delta(connectome, capped, lower_is_better=True) == 1.0


def test_rank_permutation_pvalue_separated_vs_overlapping():
    from src.experiment import stats

    rng = np.random.default_rng(0)
    a = np.array([0.10, 0.12, 0.11, 0.13, 0.10])
    b = np.array([0.50, 0.52, 0.51, 0.49, 0.53])  # cleanly separated
    assert stats.rank_permutation_pvalue(a, b, 2000, rng) < 0.05
    assert stats.rank_permutation_pvalue(a, a.copy(), 2000, rng) > 0.5

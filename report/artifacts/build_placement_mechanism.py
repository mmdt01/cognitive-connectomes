"""Pre-registered placement-mechanism analysis: freeze the three measurements of
``report/PREREG_PLACEMENT_MECHANISM.md`` §2 as parquets.

    python -m report.artifacts.build_placement_mechanism

**Read-only.** Nothing here runs a simulation, regenerates an existing artifact or
touches a published number. The only inputs are two frozen files:

    report/artifacts/substrate_edges.parquet          adjacency, written once by
                                                      build_substrate_graphs.py
    eigenspectrum/results/scale_448/spectra_per_seed.parquet   |lambda_1|, the gate

**The reconstruction gate runs first and stops the build if it fails.** Every weighted
adjacency is rebuilt from the edge list and its ``|lambda_1|`` checked against
``lambda_max_raw`` for the same ``(variant, seed)`` in the frozen spectra. The edge list
was written from the same builder the spectra were computed from, so a deviation beyond
float32 storage precision means the two files are not describing the same matrices and
nothing downstream can be read.

Four files are written, one per measurement, because their shapes differ:

    placement_mechanism_masking.parquet           one row per (cell, k)
    placement_mechanism_strength.parquet          one row per cell
    placement_mechanism_degree_weight.parquet     one row per (cell, degree-product bin)
    placement_mechanism_rank_correlation.parquet  one row per cell

All four are ``*.parquet`` and therefore gitignored, as every parquet in this repository
is; **the script is what is committed**, and re-running it reproduces them exactly (the
only randomness is the edge-order control and the bootstrap, both on fixed seeds).
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from threadpoolctl import threadpool_limits

OUT_DIR = Path(__file__).resolve().parent
REPO_ROOT = OUT_DIR.parents[1]
EDGES_PATH = OUT_DIR / "substrate_edges.parquet"
SPECTRA_PATH = (REPO_ROOT / "experiments/human/analysis/eigenspectrum/results"
                / "scale_448/spectra_per_seed.parquet")

CONDITION = "human_empirical"
LADDER = ["connectome", "connectome_weight_permuted", "degree_rewire", "erdos_renyi"]
N_NODES = 448
EDGE_COUNT = 5323

# The gate's tolerance. The edge list stores weights as float64 but the prereg fixes the
# bar at float32 storage precision, which is the loosest rounding either file could have
# been through; anything above it is a mismatch of matrices, not of arithmetic.
FLOAT32_EPS = float(np.finfo(np.float32).eps)

# Masking grid: log-spaced from 1% to 100% of the edges, dense at the low end where the
# curve moves, with the four masks the prereg reports at forced in exactly.
REPORT_FRACTIONS = (0.05, 0.10, 0.25, 0.50)
N_GRID = 60

# The random-order control: the connectome's own edges kept in random order rather than
# heaviest-first, ten independent orderings, reported as a band.
N_ORDERINGS = 10
ORDER_SEED = 0

# Degree-product binning: equal-count (quantile) bins over the edge list, so every bin
# carries the same number of edges and the shape is not set by a few extreme products.
N_BINS = 20
N_BOOTSTRAP = 10000
BOOTSTRAP_SEED = 0


# =============================================================================
# Reconstruction and the gate
# =============================================================================
def reconstruct(cell: pd.DataFrame) -> np.ndarray:
    """The symmetric weighted adjacency of one (variant, seed), from its edge rows."""
    matrix = np.zeros((N_NODES, N_NODES), dtype=np.float64)
    i = cell.i.to_numpy(dtype=np.intp)
    j = cell.j.to_numpy(dtype=np.intp)
    weight = cell.weight.to_numpy(dtype=np.float64)
    matrix[i, j] = weight
    matrix[j, i] = weight
    return matrix


def spectral_radius(matrix: np.ndarray) -> float:
    """``|lambda_1|`` of a symmetric matrix, as the largest eigenvalue in modulus."""
    return float(np.abs(np.linalg.eigvalsh(matrix)).max())


def load_cells() -> dict:
    edges = pd.read_parquet(EDGES_PATH)
    assert set(edges.variant.unique()) == set(LADDER), (
        f"substrate_edges.parquet carries {sorted(edges.variant.unique())}, not the "
        f"ladder {LADDER}.")
    counts = edges.groupby(["variant", "seed"]).size()
    wrong = counts[counts != EDGE_COUNT]
    assert wrong.empty, f"edge count is not {EDGE_COUNT} for {dict(wrong)}"
    assert (edges.weight > 0).all(), (
        "the edge list carries a non-positive weight, so the masked matrices are not "
        "non-negative and the Perron argument the masking curve rests on does not hold.")
    return {key: frame for key, frame in edges.groupby(["variant", "seed"], sort=True)}


def reconstruction_gate(cells: dict) -> tuple:
    """Every reconstructed ``|lambda_1|`` against ``lambda_max_raw`` for the same cell."""
    spectra = pd.read_parquet(SPECTRA_PATH)
    spectra = spectra[(spectra.condition == CONDITION) & spectra.variant.isin(LADDER)]
    published = spectra.set_index(["variant", "seed"]).lambda_max_raw

    rows, matrices = [], {}
    for key, frame in sorted(cells.items()):
        matrices[key] = reconstruct(frame)
        recomputed = spectral_radius(matrices[key])
        reference = float(published.loc[key])
        rows.append(dict(variant=key[0], seed=key[1], lambda1_reconstructed=recomputed,
                         lambda_max_raw=reference,
                         absolute_deviation=abs(recomputed - reference),
                         relative_deviation=abs(recomputed - reference) / reference))
    gate = pd.DataFrame(rows)
    worst = gate.loc[gate.relative_deviation.idxmax()]
    print(f"[gate] reconstruction, {len(gate)} cells: max absolute deviation "
          f"{gate.absolute_deviation.max():.3e}, max relative deviation "
          f"{gate.relative_deviation.max():.3e} "
          f"({worst.variant}, seed {int(worst.seed)}); float32 eps {FLOAT32_EPS:.3e}")
    if gate.relative_deviation.max() > FLOAT32_EPS:
        sys.exit("[gate] FAILED: the reconstructed matrices are not the matrices the "
                 "frozen spectra were computed from. Stopping before any measurement.")
    print("[gate] PASSED")
    return matrices, gate


# =============================================================================
# (1) Heaviest-edge masking curve
# =============================================================================
def mask_grid() -> np.ndarray:
    dense = np.logspace(np.log10(0.01), 0.0, N_GRID)
    forced = np.array(REPORT_FRACTIONS)
    k = np.round(np.concatenate([dense, forced]) * EDGE_COUNT).astype(int)
    return np.unique(np.clip(k, 1, EDGE_COUNT))


def masking_curve(cell: pd.DataFrame, order: np.ndarray, grid: np.ndarray,
                  lambda1_full: float) -> pd.DataFrame:
    """``lambda_1`` of the matrix holding only the first ``k`` edges of ``order``."""
    i = cell.i.to_numpy(dtype=np.intp)[order]
    j = cell.j.to_numpy(dtype=np.intp)[order]
    weight = cell.weight.to_numpy(dtype=np.float64)[order]

    matrix = np.zeros((N_NODES, N_NODES), dtype=np.float64)
    rows, placed = [], 0
    for k in grid:
        head = slice(placed, k)
        matrix[i[head], j[head]] = weight[head]
        matrix[j[head], i[head]] = weight[head]
        placed = k
        rows.append(dict(k=int(k), fraction_edges=k / EDGE_COUNT,
                         lambda1_masked=spectral_radius(matrix)))
    frame = pd.DataFrame(rows)
    assert (frame.lambda1_masked.diff().dropna() >= -FLOAT32_EPS * lambda1_full).all(), (
        "the masking curve decreases in k. Masking entries of a non-negative matrix "
        "downward cannot raise its spectral radius, so this is a bug, not a finding.")
    frame["lambda1_full"] = lambda1_full
    frame["fraction_retained"] = frame.lambda1_masked / lambda1_full
    return frame


def build_masking(cells: dict, matrices: dict) -> pd.DataFrame:
    grid = mask_grid()
    print(f"[1] masking grid: {len(grid)} values of k from {grid[0]} "
          f"({grid[0] / EDGE_COUNT:.2%}) to {grid[-1]} (100%)")

    blocks = []
    for key, frame in sorted(cells.items()):
        lambda1_full = spectral_radius(matrices[key])
        order = np.argsort(-frame.weight.to_numpy(dtype=np.float64), kind="stable")
        curve = masking_curve(frame, order, grid, lambda1_full)
        curve.insert(0, "block", "heaviest_first")
        curve.insert(1, "variant", key[0])
        curve.insert(2, "seed", key[1])
        curve.insert(3, "ordering", 0)
        blocks.append(curve)

    # The internal control the prereg requires: the same sweep on the connectome with
    # edges kept in random order. Without it the panel is about sparsification.
    key = ("connectome", 0)
    connectome, lambda1_full = cells[key], spectral_radius(matrices[key])
    rng = np.random.default_rng(ORDER_SEED)
    for ordering in range(N_ORDERINGS):
        order = rng.permutation(EDGE_COUNT)
        curve = masking_curve(connectome, order, grid, lambda1_full)
        curve.insert(0, "block", "random_order")
        curve.insert(1, "variant", "connectome")
        curve.insert(2, "seed", 0)
        curve.insert(3, "ordering", ordering)
        blocks.append(curve)

    print(f"[1] monotone non-decreasing in k on all "
          f"{len(cells) + N_ORDERINGS} curves")
    return pd.concat(blocks, ignore_index=True)


# =============================================================================
# (2) The strength sandwich
# =============================================================================
def build_strength(cells: dict, matrices: dict) -> pd.DataFrame:
    rows = []
    for key, matrix in sorted(matrices.items()):
        strength = matrix.sum(axis=1)
        rows.append(dict(variant=key[0], seed=key[1],
                         mean_strength=float(strength.mean()),
                         max_strength=float(strength.max()),
                         lambda1=spectral_radius(matrix)))
    frame = pd.DataFrame(rows)

    violation = frame[~((frame.mean_strength <= frame.lambda1)
                        & (frame.lambda1 <= frame.max_strength))]
    assert violation.empty, (
        "mean_strength <= lambda_1 <= max_strength fails on "
        f"{len(violation)} cell(s); the sandwich is a theorem for a symmetric "
        "non-negative matrix, so this is a bug.")
    print(f"[2] sandwich mean <= |lambda_1| <= max holds on all {len(frame)} cells")

    connectome = float(frame.query("variant == 'connectome'").mean_strength.iloc[0])
    control = float(frame.query("variant == 'connectome_weight_permuted'")
                    .mean_strength.iloc[0])
    assert abs(connectome - control) <= FLOAT32_EPS * connectome, (
        f"mean strength differs between connectome ({connectome!r}) and control "
        f"({control!r}); the permutation preserves the weight multiset exactly, so a "
        "difference is a broken control.")
    print(f"[2] mean strength identical, connectome vs control: "
          f"{connectome:.17g} vs {control:.17g} "
          f"(|difference| {abs(connectome - control):.3e})")
    return frame


# =============================================================================
# (3) Weight against endpoint degree product
# =============================================================================
def build_degree_weight(cells: dict, matrices: dict) -> tuple:
    """Connectome and control only: they share one binary graph, so the degree products
    are identical between them and only which edge carries which weight differs."""
    pair = [("connectome", 0), ("connectome_weight_permuted", 0)]
    bin_rows, correlation_rows = [], []
    for key in pair:
        frame, matrix = cells[key], matrices[key]
        degree = (matrix != 0).sum(axis=1)
        i = frame.i.to_numpy(dtype=np.intp)
        j = frame.j.to_numpy(dtype=np.intp)
        weight = frame.weight.to_numpy(dtype=np.float64)
        product = (degree[i] * degree[j]).astype(np.float64)

        # Equal-count bins on the degree product. Bins are cut on the CONNECTOME's own
        # products, which are the control's products too (one binary graph), so both
        # rows are binned identically and the two curves are comparable bin for bin.
        codes, edges_of_bin = pd.qcut(product, N_BINS, labels=False, retbins=True,
                                      duplicates="drop")
        for index in range(int(codes.max()) + 1):
            member = codes == index
            bin_rows.append(dict(
                variant=key[0], seed=key[1], bin_index=index,
                bin_lower=float(edges_of_bin[index]),
                bin_upper=float(edges_of_bin[index + 1]),
                n_edges=int(member.sum()),
                median_degree_product=float(np.median(product[member])),
                mean_weight=float(weight[member].mean()),
                sem_weight=float(weight[member].std(ddof=1) / np.sqrt(member.sum()))))

        rho = float(spearmanr(weight, product).statistic)
        rng = np.random.default_rng(BOOTSTRAP_SEED)
        draws = np.empty(N_BOOTSTRAP)
        for step in range(N_BOOTSTRAP):
            pick = rng.integers(0, weight.size, weight.size)
            draws[step] = spearmanr(weight[pick], product[pick]).statistic
        low, high = np.percentile(draws, [2.5, 97.5])
        correlation_rows.append(dict(
            variant=key[0], seed=key[1], n_edges=int(weight.size),
            spearman_rho=rho, ci_low=float(low), ci_high=float(high),
            n_bootstrap=N_BOOTSTRAP, bootstrap_seed=BOOTSTRAP_SEED))
        print(f"[3] {key[0]}: Spearman rho = {rho:+.4f}, 95% bootstrap CI "
              f"[{low:+.4f}, {high:+.4f}]")

    return pd.DataFrame(bin_rows), pd.DataFrame(correlation_rows)


# =============================================================================
def main() -> None:
    # The whole analysis is a few thousand 448x448 symmetric eigendecompositions, which
    # is a size where the threaded BLAS spends all its time in the pool: 3.45 s per call
    # against 7 ms on one thread here. The limiter is entered after numpy is imported,
    # which is the only order in which it takes effect.
    with threadpool_limits(limits=1):
        run()


def run() -> None:
    cells = load_cells()
    print(f"loaded {len(cells)} (variant, seed) cells from {EDGES_PATH.name}\n")
    matrices, gate = reconstruction_gate(cells)
    print()
    masking = build_masking(cells, matrices)
    print()
    strength = build_strength(cells, matrices)
    print()
    bins, correlation = build_degree_weight(cells, matrices)

    written = {
        "placement_mechanism_gate.parquet": gate,
        "placement_mechanism_masking.parquet": masking,
        "placement_mechanism_strength.parquet": strength,
        "placement_mechanism_degree_weight.parquet": bins,
        "placement_mechanism_rank_correlation.parquet": correlation,
    }
    print()
    for name, frame in written.items():
        frame.to_parquet(OUT_DIR / name, index=False)
        print(f"[write] {name}: {frame.shape[0]} rows x {frame.shape[1]} columns")


if __name__ == "__main__":
    main()

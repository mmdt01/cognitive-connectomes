"""Freeze the four Act I substrates as graphs: the edge lists and four binary statistics.

    python -m report.artifacts.build_substrate_graphs

**Why this exists.** Every other figure in the sweep reads a frozen parquet, but no frozen
parquet in the repository holds *adjacency*. The spectra files carry eigenvalues, the
criticality-matched files carry task scores, and the substrates themselves are rebuilt on
demand from ``HumanSubstrateBuilder``. F19 draws the four substrates as matrices, so it
needs the edges; this script writes them once, and the figure reads them like any other
source.

**A one-off, and additive.** Nothing here regenerates or reads-then-rewrites an existing
artifact. It builds the same four ``(condition, variant, seed)`` cells the rest of Act I
builds, from the same builder, and writes new files under ``report/artifacts/`` (two
originally, and a third added for S4, described below):

    substrate_edges.parquet     one row per undirected edge per variant per seed
                                [variant, seed, i, j, weight], i < j
    substrate_topology.parquet  one row per variant per seed
                                [variant, seed, mean_clustering,
                                 modularity_fixed_partition, degree_assortativity,
                                 global_efficiency]

Both are ``*.parquet`` and therefore gitignored, as every parquet in this repository is;
**the script is what is committed**, and re-running it reproduces them exactly (the
builder is deterministic given the seed, and so is the partition below).

**All four statistics are computed on the BINARY graph, with weights discarded.** That is
the point of the figure it feeds: no measure of the binary graph can separate the
connectome from its weight-permuted control, because the two *are* the same binary graph.

**The partition is detected ONCE, on the connectome, and applied unchanged to every
variant.** Method: ``networkx.community.louvain_communities`` on the binary connectome
graph, at the networkx default resolution ``1.0``, seed ``0``
(``experiments.human.matrix_config.LOUVAIN_SEED``). It is not re-detected per variant:
``modularity_fixed_partition`` asks how much of *the connectome's* block structure each
variant retains, which is only a comparison if the blocks are held fixed. Running Louvain
on Erdős–Rényi would return whatever partition best fits that draw and report a
respectable modularity for a graph with no community structure at all.

The partition is taken from ``HumanSubstrateBuilder.partition``, which is the same object
the null ladder's ``modularity_rewire`` rung is built against, so this script cannot be
detecting a different partition from the rest of the pipeline.

**A second output, added 1 September 2026 for S4**, which draws all seven substrates
rather than the ladder's four:

    substrate_edges_full.parquet   the same five columns, all seven variants

``substrate_edges.parquet`` is written exactly as before, byte for byte, and the full
family goes to a file of its own. The reason is F19: its builder takes its columns from
``edges.variant.unique()``, so three extra variants in that file would silently widen a
four-column figure to seven. The full file carries the four ladder variants' rows
unchanged, appended to from the very frame the four-variant file is written from, and
adds ``clustering_rewire``, ``modularity_rewire`` and ``random_gaussian`` at all ten
seeds.

**No topology statistics are computed for the three additional variants.**
``substrate_topology.parquet`` and ``TIER0`` 3.13 belong to the four-substrate ladder
and are unchanged; S4 carries no statistics strip.

**Rung 0 is the one variant whose edge count is not 5,323.** ``random_gaussian`` draws
every pair independently at the connectome's density, so its count is Binomial rather
than fixed, and the exact-count assertion is exempted for that variant alone. It is
checked against the binomial expectation to five standard deviations instead, and its
ten per-seed counts are printed so the variation is on the record. ``clustering_rewire``
and ``modularity_rewire`` match the count exactly, by construction, and are asserted
exactly.

**All seven are non-negative at ``human_empirical``.** Every randomised graph, rung 0
included, takes its weights by drawing with replacement from the connectome's own
weight pool, so no substrate in this family carries a signed weight. The build asserts
it rather than assuming it.

**Two verifications run before anything is written**, and either failing raises:

1. every ``(variant, seed)`` carries exactly 5,323 undirected edges, the frozen count of
   the N = 448 consensus;
2. every ``degree_rewire`` seed reproduces the connectome's sorted degree sequence
   exactly, which is what a double-edge-swap rewire preserves by construction.

**Then the reproduction gate**: the connectome and the weight-permuted control must
return byte-identical binary adjacency and *exactly* equal values on all four statistics
-- exact equality, not a tolerance. Permuting which edge carries which weight cannot move
a measure of the binary graph, so a nonzero difference on any of the four would be a
defect in the permutation rather than a finding, and the gate stops the build.
"""

import sys
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

from experiments.human import matrix_config as config
from experiments.human.substrates import HumanSubstrateBuilder
from report.figlib.sources import SOURCES

OUT_DIR = Path(__file__).resolve().parent
SCALE = 448
CONDITION = "human_empirical"
N_SEEDS = config.N_SEEDS
EDGE_COUNT = 5323          # the frozen count of the N = 448 self-built consensus

# The ladder, in the contract's order. The first two are single graphs: the connectome is
# one fixed matrix, and the control is that same graph with its own weights reordered, so
# neither has a binary graph that varies with the seed. The two randomised variants are
# resampled per seed and are written at all ten.
VARIANTS = ["connectome", "connectome_weight_permuted", "degree_rewire", "erdos_renyi"]
SINGLE_GRAPH = ("connectome", "connectome_weight_permuted")

# The seed the single-graph variants are stored at. The connectome ignores it; the
# control's permutation does not, and F1 draws the control at the seed whose bulk95 is
# nearest the median of its ten. That seed is derived below from the frozen spectra by
# F1's own rule rather than written down here, so the one weighted matrix this file
# carries for the control is the one F1 already draws.
CONNECTOME_SEED = 0

# The three rungs outside the ladder, written to the full-family file only. Order as
# `report/thesis` `tab:methods-preservation` lists them, most preserved first, which is
# also the column order S4 draws; the four ladder variants keep their own order above.
EXTRA_VARIANTS = ["clustering_rewire", "modularity_rewire", "random_gaussian"]

# Rung 0 fixes the density in EXPECTATION rather than the edge count, so its count is
# Binomial(PAIR_COUNT, density) and an exact assertion would fail on a null that is
# behaving exactly as designed. It is checked to five binomial standard deviations
# instead: 71.0 edges at N = 448, so the band is +/- 355 and admits 4,968 to 5,678. The
# ten observed counts run 5,180 to 5,439, which is -2.0 to +1.6 standard deviations.
# **The exemption is rung 0's alone**: clustering_rewire and modularity_rewire are
# double-edge-swap rewires and match the count exactly, and their assertion is exact.
PAIR_COUNT = SCALE * (SCALE - 1) // 2
RUNG0_TOLERANCE_SIGMA = 5.0


def rung0_edge_band() -> tuple:
    """``(expectation, standard deviation, half-width)`` of rung 0's edge-count check."""
    density = EDGE_COUNT / PAIR_COUNT
    deviation = float(np.sqrt(PAIR_COUNT * density * (1.0 - density)))
    return EDGE_COUNT, deviation, RUNG0_TOLERANCE_SIGMA * deviation


def representative_seed(variant: str) -> int:
    """F1's rule: the seed whose ``bulk95`` is nearest the median of that variant's ten.

    Read off the same frozen source F1 reads (``spectra_448``) and applied the same way,
    so a reader comparing F19 against F1 sees the same matrices rather than two different
    draws of the same null.
    """
    frame = SOURCES["spectra_448"].load()
    sub = frame[frame.variant == variant]
    return int(sub.loc[(sub.bulk95 - sub.bulk95.median()).abs().idxmin()].seed)


def binary_statistics(graph: nx.Graph, partition) -> dict:
    """The four statistics, all on the binary graph, weights discarded.

    ``weight=None`` is passed wherever networkx would otherwise reach for an edge
    ``weight`` attribute. ``nx.from_numpy_array`` writes one on every edge, and although
    it is 1.0 on a binary matrix and so cannot change any of these values, the call sites
    say what they mean rather than relying on that.
    """
    return dict(
        mean_clustering=float(nx.average_clustering(graph, weight=None)),
        modularity_fixed_partition=float(
            nx.community.modularity(graph, partition, weight=None, resolution=1.0)),
        degree_assortativity=float(nx.degree_assortativity_coefficient(graph, weight=None)),
        global_efficiency=float(nx.global_efficiency(graph)),
    )


def build() -> tuple:
    """The four ladder variants. The builder is returned so `build_full` can reuse it."""
    builder = HumanSubstrateBuilder(scale=SCALE)
    partition = builder.partition          # Louvain, resolution 1.0, seed 0, connectome
    control_seed = representative_seed("connectome_weight_permuted")
    print(f"substrate: N = {SCALE}, condition = {CONDITION!r}, "
          f"partition = {len(partition)} communities "
          f"(Louvain, resolution 1.0, seed {config.LOUVAIN_SEED}, detected on the "
          f"connectome)")
    print(f"single-graph variants stored at seed: connectome {CONNECTOME_SEED}, "
          f"weight-permuted {control_seed} (F1's representative seed)\n")

    # The empirical pool has no zero, so `weighted != 0` recovers the edge set exactly
    # and the binary graph below is the real one rather than a thresholded one.
    assert (builder.empirical_pool > 0).all(), (
        "the empirical weight pool contains a zero, so a nonzero test cannot recover the "
        "edge set; the binary graphs below would silently lose edges.")

    edge_rows, topology_rows, binary = [], [], {}
    for variant in VARIANTS:
        seeds = ([CONNECTOME_SEED if variant == "connectome" else control_seed]
                 if variant in SINGLE_GRAPH else list(range(N_SEEDS)))
        for seed in seeds:
            weighted = builder.weighted(CONDITION, variant, seed)
            adjacency = (weighted != 0).astype(np.uint8)
            graph = nx.from_numpy_array(adjacency)
            edge_rows.append(edge_frame(weighted, variant, seed))
            topology_rows.append(dict(variant=variant, seed=seed,
                                      **binary_statistics(graph, partition)))
            binary[(variant, seed)] = adjacency

    edges = pd.concat(edge_rows, ignore_index=True)
    topology = pd.DataFrame(topology_rows)
    return builder, binary, edges, topology


def edge_frame(weighted, variant: str, seed: int):
    """One cell's upper-triangle edge list, in the columns both files carry."""
    upper_i, upper_j = np.triu_indices_from(weighted, k=1)
    keep = weighted[upper_i, upper_j] != 0
    return pd.DataFrame(dict(
        variant=variant, seed=seed,
        i=upper_i[keep].astype(np.int16), j=upper_j[keep].astype(np.int16),
        weight=weighted[upper_i, upper_j][keep]))


def build_full(builder, edges):
    """The seven-substrate family: the ladder's own rows, plus the three off-ladder rungs.

    The ladder's rows are not rebuilt. ``edges`` is the frame
    ``substrate_edges.parquet`` is written from, and it is concatenated unchanged, so the
    four variants cannot differ by so much as a row between the two files. Only the three
    additional rungs are built here, at all ten seeds each, from the same builder, the
    same condition and the same weight pool.
    """
    rows = [edges]
    for variant in EXTRA_VARIANTS:
        for seed in range(N_SEEDS):
            rows.append(edge_frame(builder.weighted(CONDITION, variant, seed),
                                   variant, seed))
    return pd.concat(rows, ignore_index=True)


def verify(binary, edges) -> None:
    """Edge count and degree sequence, checked against the frozen spectra's substrate."""
    counts = edges.groupby(["variant", "seed"]).size()
    wrong = counts[counts != EDGE_COUNT]
    assert wrong.empty, (
        f"edge count is not {EDGE_COUNT} for {len(wrong)} cell(s): {dict(wrong)}. Every "
        "variant matches the connectome's edge count exactly by construction, so this is "
        "a broken null, not a finding.")
    print(f"[ok] edge count = {EDGE_COUNT} for all {len(counts)} (variant, seed) cells")

    reference = np.sort(binary[("connectome", CONNECTOME_SEED)].sum(1))
    for seed in range(N_SEEDS):
        degrees = np.sort(binary[("degree_rewire", seed)].sum(1))
        assert np.array_equal(degrees, reference), (
            f"degree_rewire seed {seed}: sorted degree sequence differs from the "
            "connectome's. Double-edge swaps preserve it by construction; a difference "
            "is a broken rewire.")
    print(f"[ok] degree sequence of all {N_SEEDS} degree_rewire seeds equals the "
          f"connectome's exactly (min {reference.min()}, median "
          f"{int(np.median(reference))}, max {reference.max()})")


def reproduction_gate(binary, topology) -> None:
    """Connectome against its control: same binary graph, therefore the same four values.

    Byte-identical adjacency and exact equality on all four statistics. A nonzero
    difference is a defect in the permutation, not a finding, so it stops the build.
    """
    control_seed = int(topology[topology.variant == "connectome_weight_permuted"]
                       .seed.iloc[0])
    left = binary[("connectome", CONNECTOME_SEED)]
    right = binary[("connectome_weight_permuted", control_seed)]
    assert left.tobytes() == right.tobytes(), (
        "the weight-permuted control's binary adjacency is not byte-identical to the "
        "connectome's. The permutation reorders which edge carries which weight and must "
        "leave the edge set untouched; this is a defect in the permutation.")
    print("[ok] connectome and weight-permuted control: byte-identical binary adjacency")

    columns = ["mean_clustering", "modularity_fixed_partition", "degree_assortativity",
               "global_efficiency"]
    a = topology[topology.variant == "connectome"].iloc[0]
    b = topology[topology.variant == "connectome_weight_permuted"].iloc[0]
    differing = {c: (a[c], b[c]) for c in columns if a[c] != b[c]}
    assert not differing, (
        f"the control differs from the connectome on {sorted(differing)}: {differing}. "
        "These are measures of the binary graph and the two graphs are byte-identical, so "
        "any nonzero difference is a defect in the permutation, not a finding.")
    print("[ok] connectome and control: exactly equal on all four statistics "
          "(exact equality, no tolerance)\n")


def verify_full(edges, full) -> None:
    """The full family: the ladder's rows untouched, the counts, and the signs.

    Three checks, and the first is the one the separate file exists for. The four ladder
    variants must come through the concatenation exactly as ``substrate_edges.parquet``
    carries them, because F19 reads that file and S4 reads this one and the two figures
    have to be drawing the same four graphs.
    """
    ladder = full[full.variant.isin(VARIANTS)].reset_index(drop=True)
    assert ladder.equals(edges), (
        "the four ladder variants' rows differ between the full family and "
        "substrate_edges.parquet. The full file appends to that frame and must not alter "
        "a row of it; F19 and S4 would otherwise be drawing different graphs.")
    print(f"[ok] the four ladder variants' {len(ladder):,} rows come through the full "
          "family unchanged")

    exact = full[full.variant.isin(("clustering_rewire", "modularity_rewire"))]
    counts = exact.groupby(["variant", "seed"]).size()
    wrong = counts[counts != EDGE_COUNT]
    assert wrong.empty, (
        f"edge count is not {EDGE_COUNT} for {len(wrong)} cell(s): {dict(wrong)}. Both "
        "rewires are double-edge swaps and preserve the count exactly by construction, "
        "so this is a broken null rather than a finding. The exemption below is rung 0's "
        "alone and is not widened to cover these.")
    print(f"[ok] edge count = {EDGE_COUNT} exactly for all {len(counts)} "
          "clustering_rewire and modularity_rewire cells")

    expectation, deviation, half_width = rung0_edge_band()
    rung0 = full[full.variant == "random_gaussian"].groupby("seed").size()
    outside = rung0[(rung0 - expectation).abs() > half_width]
    assert outside.empty, (
        f"random_gaussian edge count is outside {RUNG0_TOLERANCE_SIGMA:g} binomial "
        f"standard deviations of {expectation} (band +/-{half_width:.0f}) for "
        f"{len(outside)} seed(s): {dict(outside)}. Rung 0 matches the density in "
        "expectation, so its count varies by design, but a draw this far out is a "
        "broken density rather than a Binomial tail.")
    worst = float((rung0 - expectation).abs().max() / deviation)
    print(f"[ok] all {len(rung0)} random_gaussian seeds within "
          f"{RUNG0_TOLERANCE_SIGMA:g} binomial sd of {expectation} "
          f"(sd {deviation:.1f}, band +/-{half_width:.0f}; worst seed {worst:.2f} sd)")

    negative = full[full.weight < 0]
    assert negative.empty, (
        f"{len(negative)} edges carry a negative weight. At condition {CONDITION!r} every "
        "randomised graph is painted from the connectome's own weight pool, which has no "
        "zero and no negative, so all seven substrates are non-negative; a signed weight "
        "here means a variant has been built at the wrong condition.")
    print(f"[ok] all {len(full):,} edges of all seven substrates are non-negative "
          f"(min {full.weight.min():.3e}, max {full.weight.max():.3e})\n")


def report_full(full) -> None:
    """Rung 0's ten per-seed edge counts, printed so the variation is on the record."""
    expectation, deviation, _ = rung0_edge_band()
    rung0 = full[full.variant == "random_gaussian"].groupby("seed").size()
    print("random_gaussian edge count per seed. Rung 0 fixes the density in expectation, "
          "not the\ncount, so this is the one variant of the seven whose edge count "
          f"varies. Expectation\n{expectation}, binomial sd {deviation:.1f}.\n")
    print("seed  " + "".join(f"{seed:7d}" for seed in rung0.index))
    print("edges " + "".join(f"{count:7d}" for count in rung0.values))
    print("sd    " + "".join(f"{(count - expectation) / deviation:+7.2f}"
                             for count in rung0.values))
    print(f"\nmean {rung0.mean():.1f}, min {rung0.min()}, max {rung0.max()}, "
          f"relative sd {rung0.std() / rung0.mean():.4f}\n")


def report(topology) -> None:
    """The four statistics for all four variants, printed before anything is rendered."""
    columns = ["mean_clustering", "modularity_fixed_partition", "degree_assortativity",
               "global_efficiency"]
    print("Binary-graph statistics. Median over the ten seeds for the two randomised "
          "variants;\nthe connectome and the control are single graphs.\n")
    print(f"{'variant':28s}" + "".join(f"{c:>28s}" for c in columns))
    for variant in VARIANTS:
        sub = topology[topology.variant == variant]
        print(f"{variant:28s}" + "".join(f"{sub[c].median():28.6f}" for c in columns))
    print()


def main() -> int:
    builder, binary, edges, topology = build()
    verify(binary, edges)
    reproduction_gate(binary, topology)
    report(topology)

    full = build_full(builder, edges)
    verify_full(edges, full)
    report_full(full)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    edges.to_parquet(OUT_DIR / "substrate_edges.parquet", index=False)
    topology.to_parquet(OUT_DIR / "substrate_topology.parquet", index=False)
    full.to_parquet(OUT_DIR / "substrate_edges_full.parquet", index=False)
    print(f"wrote {len(edges):,} edge rows -> {OUT_DIR / 'substrate_edges.parquet'}")
    print(f"wrote {len(topology)} topology rows -> "
          f"{OUT_DIR / 'substrate_topology.parquet'}")
    print(f"wrote {len(full):,} edge rows -> "
          f"{OUT_DIR / 'substrate_edges_full.parquet'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

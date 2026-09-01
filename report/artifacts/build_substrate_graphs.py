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
builds, from the same builder, and writes two new files under ``report/artifacts/``:

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
            upper_i, upper_j = np.triu_indices_from(weighted, k=1)
            keep = weighted[upper_i, upper_j] != 0
            edge_rows.append(pd.DataFrame(dict(
                variant=variant, seed=seed,
                i=upper_i[keep].astype(np.int16), j=upper_j[keep].astype(np.int16),
                weight=weighted[upper_i, upper_j][keep])))
            topology_rows.append(dict(variant=variant, seed=seed,
                                      **binary_statistics(graph, partition)))
            binary[(variant, seed)] = adjacency

    edges = pd.concat(edge_rows, ignore_index=True)
    topology = pd.DataFrame(topology_rows)
    return binary, edges, topology


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
    binary, edges, topology = build()
    verify(binary, edges)
    reproduction_gate(binary, topology)
    report(topology)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    edges.to_parquet(OUT_DIR / "substrate_edges.parquet", index=False)
    topology.to_parquet(OUT_DIR / "substrate_topology.parquet", index=False)
    print(f"wrote {len(edges):,} edge rows -> {OUT_DIR / 'substrate_edges.parquet'}")
    print(f"wrote {len(topology)} topology rows -> "
          f"{OUT_DIR / 'substrate_topology.parquet'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

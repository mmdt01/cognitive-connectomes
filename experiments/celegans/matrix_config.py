"""Shared matrix config for all C. elegans experiments.

The connectome x null-ladder x spectral-radius x seeds structure and the
substrate/stats settings are identical across tasks (NARMA-10, Mackey-Glass,
...). This module is the single source of truth for those choices; each task's
``task_config.py`` adds only the task-specific pieces. ``SubstrateBuilder``
reads its construction settings from here, and ``shared()`` supplies the
connectome-level fields of the ``ExperimentConfig``.
"""

import numpy as np

# ---------------------------------------------------------------------------
# Conditions: each fixes a (topology, weight-scheme) substrate. The first four
# form a topology x weight-distribution 2x2 factorial that dissociates
# non-normality (undirected/normal vs directed/non-normal) from weight
# heterogeneity (gaussian/homogeneous vs empirical/heavy-tailed); v2d is the
# orthogonal Dale-sign extension on top of the directed-empirical cell.
#
#                | gaussian weights | empirical (heavy-tailed) weights
#   -------------+------------------+---------------------------------
#   undirected   | v2a              | v2ae
#   directed     | v2bg             | v2b   (+ Dale signs -> v2d)
# ---------------------------------------------------------------------------
CONDITIONS = ["v2a", "v2ae", "v2bg", "v2b", "v2d"]

CONDITION_SPEC = {
    "v2a": {
        "topology": "undirected",
        "weight_scheme": "symmetric_gaussian",
        "label": "Undirected · gaussian weights",
    },
    "v2ae": {
        "topology": "undirected",
        "weight_scheme": "symmetric_empirical",
        "label": "Undirected · empirical weights",
    },
    "v2bg": {
        "topology": "directed",
        "weight_scheme": "asymmetric_gaussian",
        "label": "Directed · gaussian weights",
    },
    "v2b": {
        "topology": "directed",
        "weight_scheme": "asymmetric_empirical",
        "label": "Directed · empirical weights",
    },
    "v2d": {
        "topology": "directed",
        "weight_scheme": "asymmetric_empirical_signed",
        "label": "Directed · empirical weights (signed)",
    },
}

# The topology x weight-distribution 2x2 factorial (the first four conditions),
# laid out for the factorial figure: rows = topology, cols = weight scheme.
# v2d (signed) is the orthogonal Dale extension and is excluded from the grid.
FACTORIAL_2X2 = {
    "grid": [["v2a", "v2ae"], ["v2bg", "v2b"]],
    "row_labels": ["Undirected\n(normal)", "Directed\n(non-normal)"],
    "col_labels": ["Gaussian weights", "Empirical weights"],
}

# The connectome, a weight-placement control, and the five-rung null ladder.
# "connectome_weight_permuted" keeps the connectome's exact topology AND its
# exact weight multiset but permutes which edge carries which weight (per seed),
# isolating weight PLACEMENT from topology -- it resolves the topology-vs-weights
# confound (connectome keeps real weights while rung nulls resample). It is a
# control, not a ladder rung (rung = -1); in v2a, whose weights are already a
# random Gaussian draw, the permutation is distribution-preserving, so there it
# is a negative control that should match the connectome.
VARIANTS = [
    "connectome",
    "connectome_weight_permuted",  # placement control (not a rung)
    "random_gaussian",   # rung 0
    "erdos_renyi",       # rung 1
    "degree_rewire",     # rung 2
    "clustering_rewire", # rung 3
    "modularity_rewire", # rung 4
]
NULL_VARIANTS = VARIANTS[1:]

VARIANT_RUNG = {
    "connectome_weight_permuted": -1,  # control, not a ladder rung
    "random_gaussian": 0,
    "erdos_renyi": 1,
    "degree_rewire": 2,
    "clustering_rewire": 3,
    "modularity_rewire": 4,
}

# Full 39-point spectral-radius sweep from 0.0 to 4.0 (Suarez-width). Preserves
# the prior 0.105 spacing (4/38 == 2/19), so this grid is a strict SUPERSET of the
# old linspace(0, 2, 20): the first 20 points reproduce the earlier runs bit-for-
# bit, and the new tail (sr 2.1 -> 4.0) extends coverage into the regime where the
# connectome's compressed bulk finally reaches criticality (bulk95/|l1| ~ 0.30 ->
# bulk critical at top ~ 3.3) and beyond. Top-eigenvalue matching is unchanged; the
# wider sweep is what stops it from silently under-covering directed non-normal
# connectomes whose bulk decouples from the top (cf. Suarez et al. 2021, alpha->3.5).
SPECTRAL_RADII = [round(float(sr), 4) for sr in np.linspace(0.0, 4.0, 39)]
SUPERCRITICAL_RADII = [sr for sr in SPECTRAL_RADII if sr >= 1.25]

N_SEEDS = 10

# ---------------------------------------------------------------------------
# Substrate weighting / null construction
# ---------------------------------------------------------------------------
# "raw"  -> connectome's integer synapse counts directly; "sqrt" -> sqrt first.
# Only affects v2b/v2d (v2a is always symmetric Gaussian).
WEIGHT_TRANSFORM = "raw"
CLUSTERING_TOLERANCE = 0.05  # rung 3 clustering band
LOUVAIN_SEED = 0             # fixed partition for rung 4 (per topology family)
SWAP_MULTIPLIER = 10         # accepted swaps per edge for the rewire nulls

# The construction seed drives mask/weights/Win; the task input uses
# construction_seed + INPUT_SEED_OFFSET, pairing connectome and null per seed.
INPUT_SEED_OFFSET = 1000

# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------
N_PERMUTATIONS = 10000
PERMUTATION_SEED = 0
ALPHA = 0.05  # Holm-corrected significance threshold


def shared() -> dict:
    """Connectome-level fields of the ExperimentConfig (merged with task())."""
    return dict(
        conditions=CONDITIONS,
        condition_spec=CONDITION_SPEC,
        factorial_2x2=FACTORIAL_2X2,
        variants=VARIANTS,
        null_variants=NULL_VARIANTS,
        variant_rung=VARIANT_RUNG,
        spectral_radii=SPECTRAL_RADII,
        supercritical_radii=SUPERCRITICAL_RADII,
        n_seeds=N_SEEDS,
        weight_transform=WEIGHT_TRANSFORM,
        clustering_tolerance=CLUSTERING_TOLERANCE,
        louvain_seed=LOUVAIN_SEED,
        swap_multiplier=SWAP_MULTIPLIER,
        input_seed_offset=INPUT_SEED_OFFSET,
        n_permutations=N_PERMUTATIONS,
        permutation_seed=PERMUTATION_SEED,
        alpha=ALPHA,
    )

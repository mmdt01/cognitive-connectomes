"""Stage-0 configuration for the C. elegans NARMA-10 bridge experiment.

Single source of truth for every methodological choice — the audit trail.
Importing this module tells a reader exactly what was run.

The experiment evaluates the C. elegans connectome across three biological-
realism conditions on the NARMA-10 emulation task, each compared against its
full five-rung null ladder (rungs 0-4), over a spectral-radius sweep.
"""

from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
EXPERIMENT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = EXPERIMENT_DIR / "results"
FIGURES_DIR = EXPERIMENT_DIR / "figures"

RESULTS_PARQUET = RESULTS_DIR / "results.parquet"
NULL_DIAGNOSTICS_PARQUET = RESULTS_DIR / "null_diagnostics.parquet"
STATS_PARQUET = RESULTS_DIR / "stats.parquet"
MANIFEST_JSON = RESULTS_DIR / "manifest.json"

# ---------------------------------------------------------------------------
# The matrix: conditions x variants x spectral radii x seeds
# ---------------------------------------------------------------------------
# Each condition fixes a (topology, weight-scheme) substrate. The realism
# column walks: undirected signed-Gaussian -> directed empirical -> + Dale sign.
CONDITIONS = ["v2a", "v2b", "v2d"]

CONDITION_SPEC = {
    "v2a": {
        "topology": "undirected",
        "weight_scheme": "symmetric_gaussian",
        "label": "v2a · undirected signed-Gaussian",
    },
    "v2b": {
        "topology": "directed",
        "weight_scheme": "asymmetric_empirical",
        "label": "v2b · directed empirical",
    },
    "v2d": {
        "topology": "directed",
        "weight_scheme": "asymmetric_empirical_signed",
        "label": "v2d · directed empirical + Dale sign",
    },
}

# The connectome plus its five-rung null ladder.
VARIANTS = [
    "connectome",
    "random_gaussian",   # rung 0
    "erdos_renyi",       # rung 1
    "degree_rewire",     # rung 2
    "clustering_rewire", # rung 3
    "modularity_rewire", # rung 4
]
NULL_VARIANTS = VARIANTS[1:]

VARIANT_RUNG = {
    "random_gaussian": 0,
    "erdos_renyi": 1,
    "degree_rewire": 2,
    "clustering_rewire": 3,
    "modularity_rewire": 4,
}

# Full 20-point spectral-radius sweep from 0.0 to 2.0 (comprehensive overview
# spanning sub-critical, the canonical edge-of-chaos, and the supercritical
# regime where the memory-capacity effect lived).
SPECTRAL_RADII = [round(float(sr), 4) for sr in np.linspace(0.0, 2.0, 20)]
SUPERCRITICAL_RADII = [sr for sr in SPECTRAL_RADII if sr >= 1.25]

N_SEEDS = 10

# ---------------------------------------------------------------------------
# Substrate weighting
# ---------------------------------------------------------------------------
# "raw"  -> use the connectome's integer synapse counts directly (current).
# "sqrt" -> sqrt-transform first (mitigates heavy tails; deferred for now).
# Only affects v2b/v2d (v2a is always symmetric Gaussian).
WEIGHT_TRANSFORM = "raw"

CLUSTERING_TOLERANCE = 0.05  # rung 3 directed/undirected clustering band
LOUVAIN_SEED = 0             # fixed partition for rung 4 (per topology family)
SWAP_MULTIPLIER = 10         # accepted swaps per edge for the rewire nulls

# ---------------------------------------------------------------------------
# Frozen reservoir hyperparameters (tuned once on the v2a rung-0 baseline,
# then held fixed across every condition and variant; only sr is swept).
# ---------------------------------------------------------------------------
INPUT_SCALING = 0.2
LEAK_RATE = 1.0

# ---------------------------------------------------------------------------
# NARMA-10 task (frozen). The construction seed drives mask/weights/Win; the
# task input stream uses construction_seed + INPUT_SEED_OFFSET, so the
# connectome and each null are paired on an identical input at every seed.
# ---------------------------------------------------------------------------
NARMA_PARAMS = dict(
    T=3000,
    washout=200,
    n_train=2000,
    n_test=800,
    ridge_alpha=1e-8,
    readout_bias=True,
    u_low=0.0,
    u_high=0.5,
    divergence_bound=10.0,
    max_input_tries=50,
)
INPUT_SEED_OFFSET = 1000

# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------
# NRMSE is lower-is-better, so Cohen's d is defined on the performance
# direction: d > 0 means the connectome BEATS the null (lower NRMSE).
N_PERMUTATIONS = 10000
PERMUTATION_SEED = 0
ALPHA = 0.05  # Holm-corrected significance threshold


def as_dict() -> dict:
    """Flat, JSON-serialisable snapshot of the configuration for the manifest."""
    return {
        "conditions": CONDITIONS,
        "condition_spec": CONDITION_SPEC,
        "variants": VARIANTS,
        "spectral_radii": SPECTRAL_RADII,
        "n_seeds": N_SEEDS,
        "weight_transform": WEIGHT_TRANSFORM,
        "clustering_tolerance": CLUSTERING_TOLERANCE,
        "louvain_seed": LOUVAIN_SEED,
        "swap_multiplier": SWAP_MULTIPLIER,
        "input_scaling": INPUT_SCALING,
        "leak_rate": LEAK_RATE,
        "narma_params": NARMA_PARAMS,
        "input_seed_offset": INPUT_SEED_OFFSET,
        "n_permutations": N_PERMUTATIONS,
        "permutation_seed": PERMUTATION_SEED,
        "alpha": ALPHA,
    }

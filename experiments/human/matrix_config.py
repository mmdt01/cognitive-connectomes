"""Shared matrix config for the human macro-scale connectome experiments.

The **undirected sub-factorial** of the C. elegans sign x tail x topology design,
instantiated on the human structural connectome (Suárez 2021 dMRI SC). The human
SC is symmetric (normal) + non-negative + heavy-tailed = the ``undirected_empirical``
cell of the C. elegans factorial, so only the three UNDIRECTED conditions apply:

    human_gaussian          symmetric gaussian weights on the SC topology
                            (homogeneous, balanced ±) -> tail/normal baseline
    human_empirical_signed  the SC's real magnitudes with a balanced random sign
                            -> the one-variable SIGN control (load-bearing)
    human_empirical         the real SC weights (non-negative, heavy-tailed)
                            -> the "connectome" substrate

Reading gaussian -> signed-empirical isolates the heavy TAIL (sign held balanced);
signed-empirical -> empirical isolates SIGN (tail held heavy). The C. elegans
result predicts the effect lives in the SIGN step (human_empirical holds while its
all-positive nulls Perron-collapse; signing the weights removes it).

Reuses the C. elegans 7-variant null ladder + placement control VERBATIM -- same
variant names, so ``src/experiment`` plots/stats work unchanged -- plus the wide
``[0, 4]`` sweep. SCALE + SUBJECT select the single-subject substrate (smoke).
"""

import numpy as np

# Substrate source + scale. SOURCE "consensus" = the self-built group consensus
# (the scientific substrate; cached, cortical N=448/1000, built by
# experiments/human/build_consensus.py); "single_subject" = one subject's SC (used
# only for the plumbing smoke). SUBJECT applies only when SOURCE=="single_subject".
SOURCE = "consensus"
SCALE = 448
SUBJECT = 0

CONDITIONS = ["human_gaussian", "human_empirical_signed", "human_empirical"]

CONDITION_SPEC = {
    "human_gaussian": {
        "topology": "undirected",
        "weight_scheme": "symmetric_gaussian",
        "label": "Human SC · gaussian weights",
    },
    "human_empirical_signed": {
        "topology": "undirected",
        "weight_scheme": "symmetric_empirical_randsign",
        "label": "Human SC · empirical weights (balanced ± sign)",
    },
    "human_empirical": {
        "topology": "undirected",
        "weight_scheme": "symmetric_empirical",
        "label": "Human SC · empirical weights",
    },
}

# The undirected sign x tail row (gaussian -> signed-empirical -> empirical).
# Set to None for now: plots.plot_factorial_grid hardcodes a C. elegans *directed*
# narrative in its suptitle, so the factorial figure is skipped rather than
# rendered misleadingly. A small plots.py edit can add a proper undirected 1x3
# later.
FACTORIAL_GRID = None

# The connectome, a weight-placement control, and the five-rung null ladder --
# identical names to the C. elegans design so the generic plots/stats (which
# hardcode these variant strings) work unchanged. All UNDIRECTED here.
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

# Wide 39-point [0, 4] sweep (Suarez-width), identical to the C. elegans runs.
SPECTRAL_RADII = [round(float(sr), 4) for sr in np.linspace(0.0, 4.0, 39)]
SUPERCRITICAL_RADII = [sr for sr in SPECTRAL_RADII if sr >= 1.25]

N_SEEDS = 10

# SC weights are already normalized fractions; project default is "raw".
WEIGHT_TRANSFORM = "raw"
CLUSTERING_TOLERANCE = 0.05
LOUVAIN_SEED = 0
SWAP_MULTIPLIER = 10

INPUT_SEED_OFFSET = 1000

N_PERMUTATIONS = 10000
PERMUTATION_SEED = 0
ALPHA = 0.05


def shared() -> dict:
    """Connectome-level fields of the ExperimentConfig (merged with task())."""
    return dict(
        conditions=CONDITIONS,
        condition_spec=CONDITION_SPEC,
        factorial_grid=FACTORIAL_GRID,
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

"""Shared scaffolding for the sign-composition x spectral-radius phase diagram.

The grid (``PHASE_DIAGRAM_EXPERIMENT.md`` sec 4), the scale-tagged output dirs, and
small reproducible code maps for the flip RNG. Reuses the manifold probe package's
``common`` module for the per-task capture spec (``build_specs``), the fork-parallel
cell harness (``run_cells``), and CLI ``flag`` parsing, so this file adds only the
phase-diagram-specific configuration.
"""

from pathlib import Path

import numpy as np

from experiments.human import matrix_config
from experiments.human.analysis.manifold import common as manifold_common

# Re-export the reused manifold-package helpers so the phase-diagram driver imports
# them from one place.
build_specs = manifold_common.build_specs
run_cells = manifold_common.run_cells
flag = manifold_common.flag
DEFAULT_TASKS = manifold_common.DEFAULT_TASKS
CONDITION_COLOR = manifold_common.CONDITION_COLOR
TASK_TITLE = manifold_common.TASK_TITLE

_PD_DIR = Path(__file__).resolve().parent          # .../analysis/phase_diagram
FIGURES_DIR = _PD_DIR / "figures"
RESULTS_DIR = _PD_DIR / "results"

# --- the grid ---------------------------------------------------------------
# Sign fraction f: the primary (negative-weight-fraction) axis, 11 values.
F_GRID = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
# Spectral radius: 16 points evenly over [0, 6] (a phase diagram needs a smooth
# boundary, not the full 58-point task sweep). Independent of the committed grid --
# these are new flipped-sign substrates with no committed rows to join against; the
# order parameters are computed within the phase-diagram parquet itself. f=0 shares
# sr=0 and sr=6 with the committed grid, which the f=0 validation gate exploits.
SR_POINTS = 16
SR_MAX = 6.0

# The all-positive base the flip transform acts on, and the three variants both
# order parameters need (connectome and ER; degree_rewire the intermediate rung).
BASE_CONDITION = "human_empirical"
VARIANTS = ["connectome", "degree_rewire", "erdos_renyi"]
CONTRAST_VARIANT = "erdos_renyi"        # order parameter is connectome - ER

# Sequencing: the stratified (placement-neutral) primary is the headline; hub_first
# / periphery_first are the secondary placement study. Dale is deferred (it breaks
# the undirected/normal substrate -- see PHASE_DIAGRAM_EXPERIMENT.md flagged notes).
DEFAULT_TARGETINGS = ["stratified"]
ALL_TARGETINGS = ["stratified", "hub_first", "periphery_first"]

N_SEEDS = matrix_config.N_SEEDS         # 10
N_DRAWS = 3                             # a few stratified draws per cell, averaged
N_STRATA = 10                           # score deciles for stratified flipping
SCORE_MODE = "degree"                   # endpoint-degree product (primary)

# Reproducible integer codes for the flip RNG entropy (default_rng([...])), so the
# flip pattern is a deterministic function of (seed, f, draw, targeting, variant)
# and is independent of Python hash randomisation.
TARGETING_CODE = {"stratified": 0, "hub_first": 1, "periphery_first": 2}
VARIANT_CODE = {"connectome": 0, "degree_rewire": 1, "erdos_renyi": 2,
                "connectome_weight_permuted": 3, "random_gaussian": 4,
                "clustering_rewire": 5, "modularity_rewire": 6}

# Smoke sub-grid (PHASE_DIAGRAM_EXPERIMENT.md sec 4: 3x3, 2 seeds, stratified). Two
# variants (connectome + ER) so the full capture -> analyse -> plots chain,
# including the connectome-vs-ER contrast, can be smoked end to end.
SMOKE_F_GRID = [0.0, 0.25, 0.5]
SMOKE_SR = [0.0, 0.95, 3.0]
SMOKE_VARIANTS = ["connectome", "erdos_renyi"]
SMOKE_SEEDS = 2
# mc + narma10 (both fast) exercise the per-task order-parameter resolution; Lorenz
# (heavy teacher-forcing) is left to the full run.
SMOKE_TASKS = ["mc", "narma10"]


def sr_grid(n: int = SR_POINTS, sr_max: float = SR_MAX) -> list:
    """The evenly-spaced [0, sr_max] spectral-radius grid for the phase diagram."""
    return [round(float(s), 6) for s in np.linspace(0.0, sr_max, n)]


def scale_dirs(scale: int) -> tuple[Path, Path]:
    """Scale-tagged (results_dir, figures_dir)."""
    return RESULTS_DIR / f"scale_{scale}", FIGURES_DIR / f"scale_{scale}"


def resolve_grid(smoke: bool) -> dict:
    """The capture grid (full or smoke) as a single dict of axes."""
    if smoke:
        return dict(f_grid=SMOKE_F_GRID, sweep=SMOKE_SR, variants=SMOKE_VARIANTS,
                    n_seeds=SMOKE_SEEDS, n_draws=1, tasks=SMOKE_TASKS)
    return dict(f_grid=F_GRID, sweep=sr_grid(), variants=VARIANTS,
                n_seeds=N_SEEDS, n_draws=N_DRAWS, tasks=DEFAULT_TASKS)

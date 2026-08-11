"""Shared scaffolding for E0.2 (effective-criticality-matched memory panel).

Output dirs, the three axes the panel can be indexed on, and the pre-registered
analysis choices. Provenance helpers are reused from the E0.4 package rather than
duplicated, so both experiments stamp artifacts the same way.

The whole experiment is a reanalysis of frozen parquets: no reservoir is simulated
and no existing artifact is written.
"""

from pathlib import Path

from experiments.human import matrix_config
from experiments.human.analysis.manifold import common as manifold_common
from experiments.human.analysis.eigenspectrum import common as e04_common

flag = manifold_common.flag
code_version = e04_common.code_version
write_manifest = e04_common.write_manifest

_DIR = Path(__file__).resolve().parent
_ROOT = Path(__file__).resolve().parents[4]
RESULTS_DIR = _DIR / "results"
FIGURES_DIR = _DIR / "figures"
VERDICT_PATH = RESULTS_DIR / "E02_verdict.md"

SCALE = 448
N_SEEDS = matrix_config.N_SEEDS

# The f=0 cut: the non-negative substrate, where the real macro connectome sits and
# where the memory result is stated. The sign transform is the identity at f=0, so
# every draw and both sign modes are the same matrix -- asserted, not assumed.
F_CUT = 0.0
TASK = "mc"
TARGETING = "stratified"
SIGN_MODE = "edge"
DRAW = 0

CONN = "connectome"
CONTRAST = "erdos_renyi"                     # the null dD is defined against
# The weight-permuted placement control is present in the Task B extension but not in
# the frozen phase capture, so it is listed here and simply absent when the source is
# the frozen file.
VARIANTS = [CONN, "connectome_weight_permuted", "degree_rewire", CONTRAST]

# The three candidate x-axes.
#   nominal    -- what the original panel used; does NOT match effective criticality
#   effective  -- sr * bulk95: PRIMARY. Monotone in sr (bulk95 is a per-cell
#                 constant), purely structural, computable from E0.4 alone.
#   sigma_eff  -- bulk95 * sr * <1-x^2>: SECONDARY, and NON-MONOTONE in sr (the tanh
#                 gain collapses faster than sr grows), so it cannot serve as a
#                 matching grid. Shown as a parametric trajectory, fold retained.
AXES = {
    "nominal": dict(column="spectral_radius", label=r"nominal spectral radius $\sigma$",
                    monotone=True),
    "effective": dict(column="_x_effective",
                      label=r"effective criticality  $\sigma \cdot \mathrm{bulk}_{95}$",
                      monotone=True),
    "sigma_eff": dict(column="effective_radius",
                      label=r"$\sigma_{eff} = \mathrm{bulk}_{95}\,\sigma\,\langle 1-x^2\rangle$",
                      monotone=False),
}
PRIMARY_AXIS = "effective"

N_GRID = 121                     # points on the common matched grid
INTERP_METHODS = ["linear", "cubic"]
PRIMARY_INTERP = "linear"
# Agreement between the two d_eff sources, as a RELATIVE tolerance at sigma > 0.
#
# `d_eff = sum_i g_i/(g_i + alpha)` has a noise floor set by how many Gram eigenvalues
# sit near `alpha`, not by the precision of the states -- so two runs of the identical
# code on different hardware agree to ~1e-5 relative, not to machine epsilon. The
# frozen phase capture (ada) and this laptop are such a pair. 1e-4 sits an order above
# the observed level and four orders below anything that could move a conclusion (dD
# is ~10^2, so 1e-4 on d_eff ~ 400 is ~0.04). A genuine pipeline disagreement -- a
# different alpha or a different design matrix -- produces O(1) relative differences
# and is still caught.
SOURCE_AGREEMENT_TOL = 1e-4

VARIANT_TITLE = {
    "connectome": "Connectome",
    "connectome_weight_permuted": "Weight-permuted",
    "degree_rewire": "Degree-matching",
    "erdos_renyi": "Erdős–Rényi",
}
VARIANT_COLOR = {                # Okabe-Ito, matching E0.4's Figure 1
    "connectome": "#000000",
    "connectome_weight_permuted": "#D55E00",
    "degree_rewire": "#0072B2",
    "erdos_renyi": "#009E73",
}


def extended_sweep_path(scale: int = SCALE):
    """Task B's extended MC sweep (a superset of the frozen phase capture at f=0)."""
    return RESULTS_DIR / f"taskB_extended_sweep_scale_{scale}.parquet"


def phase_cells_path(scale: int = SCALE) -> Path:
    """The frozen phase-diagram capture -- read-only, the primary d_eff source."""
    return (_ROOT / "experiments" / "human" / "analysis" / "phase_diagram" / "results"
            / f"scale_{scale}" / "phase_cells.parquet")


def probe3_path(scale: int = SCALE) -> Path:
    """The manifold package's d_eff table -- read-only, the cross-check source."""
    return (_ROOT / "experiments" / "human" / "analysis" / "results"
            / f"scale_{scale}" / "probe3_deff.parquet")


def eigenspectrum_summary(scale: int) -> Path:
    """E0.4's per-seed spectra, for the N=1000 handoff numbers."""
    return (_ROOT / "experiments" / "human" / "analysis" / "eigenspectrum" / "results"
            / f"scale_{scale}" / "bulk95_summary.csv")

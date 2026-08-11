"""Shared scaffolding for E0.4 (eigenspectra, ``bulk95`` and ``sr_crit``).

Scale-tagged output dirs, the colourblind-safe publication palette, and the
provenance record every artifact carries. Reuses the manifold package's
fork-parallel cell harness (``run_cells``) and CLI ``flag`` parser, and the
phase-diagram package's grid constants, so this module adds only what is specific
to E0.4.

**One ``bulk95``, one ``d_eff``, one null ladder.** Nothing here re-implements a
spectral quantity: every number descends from
``src.analysis.spectral.recurrent_spectrum`` via
``experiments.human.analysis.manifold.spectra.capture_w_spectra``, and every
substrate from ``HumanSubstrateBuilder`` + ``src.analysis.sign_composition``.
"""

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from experiments.human import matrix_config
from experiments.human.analysis.manifold import common as manifold_common
from experiments.human.analysis.phase_diagram import common as pd_common

# Reused helpers, re-exported so the E0.4 modules import them from one place.
flag = manifold_common.flag
run_cells = manifold_common.run_cells

_DIR = Path(__file__).resolve().parent
_ROOT = Path(__file__).resolve().parents[4]
RESULTS_DIR = _DIR / "results"
FIGURES_DIR = _DIR / "figures"

# The two parcellations E0.4 must characterise (roadmap sec 2b item 4).
SCALES = [448, 1000]
# The parcellation Figure 1 is drawn at -- every panel uses this one scale, so the
# figure never mixes parcellations within or across panels.
PRIMARY_SCALE = 448

CONDITIONS = matrix_config.CONDITIONS          # 3 weight schemes
VARIANTS = matrix_config.VARIANTS              # connectome + control + 5 rungs
N_SEEDS = matrix_config.N_SEEDS                # 10, the phase-diagram seeds
BASE_CONDITION = "human_empirical"             # the non-negative substrate (f=0 biology)

# The four variants Figure 1 contrasts: connectome vs its weight-permuted control
# (same topology, same weight multiset -> isolates PLACEMENT) vs degree-preserving
# vs ER (isolates topology, then edge count).
FIGURE_VARIANTS = ["connectome", "connectome_weight_permuted", "degree_rewire",
                   "erdos_renyi"]

# bulk95-vs-f grid: exactly the phase-diagram capture grid, so the N=448 values must
# reproduce the `bulk95` column already persisted in phase_cells.parquet.
F_GRID = pd_common.F_GRID                      # 11 points, [0, 0.5]
F_VARIANTS = ["connectome", "connectome_weight_permuted", "degree_rewire",
              "erdos_renyi"]
F_TARGETING = "stratified"                     # the placement-neutral primary
F_SIGN_MODES = ["edge", "dale"]
F_SCORE_MODE = pd_common.SCORE_MODE            # "degree"
N_DRAWS = pd_common.N_DRAWS                    # 3
N_STRATA = pd_common.N_STRATA                  # 10

VARIANT_TITLE = {
    "connectome": "connectome",
    "connectome_weight_permuted": "weight-permuted",
    "random_gaussian": "rung 0 · random",
    "erdos_renyi": "rung 1 · Erdős–Rényi",
    "degree_rewire": "rung 2 · degree",
    "clustering_rewire": "rung 3 · clustering",
    "modularity_rewire": "rung 4 · modularity",
}

# Okabe-Ito: colourblind-safe under deuteranopia, protanopia and tritanopia, and
# distinguishable in greyscale by luminance ordering.
VARIANT_COLOR = {
    "connectome": "#000000",                   # black
    "connectome_weight_permuted": "#D55E00",   # vermillion
    "degree_rewire": "#0072B2",                # blue
    "erdos_renyi": "#009E73",                  # bluish green
    "clustering_rewire": "#56B4E9",            # sky blue
    "modularity_rewire": "#E69F00",            # orange
    "random_gaussian": "#CC79A7",              # reddish purple
}

# The single definition every bulk95 in this package descends from, quoted into
# every manifest so an artifact can never drift from the code that made it.
BULK95_DEFINITION = (
    "bulk95 = percentile(|lambda|, 95) / |lambda_1|, over the FULL spectrum of the "
    "un-rescaled recurrent matrix W (the Perron outlier is included in the "
    "percentile population). Computed by src.analysis.spectral.recurrent_spectrum "
    "as `bulk95_radius` on the normalised base W / |lambda_1|; identical formula to "
    "spectral_metrics' `bulk95_ratio`."
)

# One convention, stated once, used everywhere (E0.4 and E0.2 previously differed).
#
# `1/x` is convex, so aggregating with the MEAN does not commute with inverting:
# mean(1/bulk95) > 1/mean(bulk95) by Jensen, and the per-seed version is therefore
# **biased upward** (by up to 0.087 at N=1000 for random_gaussian, whose bulk95 is
# the most dispersed). The MEDIAN commutes with any monotone transform, so the two
# computation orders agree to <= 0.0014 here (the residual is only the even-n
# average of the two middle order statistics). We therefore aggregate bulk95 with
# the median and invert that, which also lets a reader reproduce sr_crit from the
# reported central bulk95 by hand.
SR_CRIT_CONVENTION = (
    "sr_crit = 1 / median_over_seeds(bulk95). The median is used rather than the "
    "mean because 1/x is convex: mean(1/bulk95) > 1/mean(bulk95) (Jensen), so a "
    "per-seed mean of 1/bulk95 is biased UPWARD -- by up to 0.087 at N=1000. Under "
    "the median the two computation orders agree to <= 0.0014, so sr_crit can be "
    "reproduced by inverting the reported central bulk95."
)


def scale_dirs(scale: int) -> tuple[Path, Path]:
    """Scale-tagged (results_dir, figures_dir)."""
    return RESULTS_DIR / f"scale_{scale}", FIGURES_DIR / f"scale_{scale}"


def committed_w_spectra(scale: int) -> Path:
    """The manifold package's committed ``w_spectra.parquet`` -- read-only here, used
    as the reproduction reference at N=448."""
    return (_ROOT / "experiments" / "human" / "analysis" / "results"
            / f"scale_{scale}" / "w_spectra.parquet")


def committed_phase_cells(scale: int) -> Path:
    """The frozen phase-diagram capture -- read-only, the ``bulk95(f)`` reference."""
    return (_ROOT / "experiments" / "human" / "analysis" / "phase_diagram"
            / "results" / f"scale_{scale}" / "phase_cells.parquet")


# ---------------------------------------------------------------------------
# Provenance
# ---------------------------------------------------------------------------
def _git(*args) -> str | None:
    try:
        out = subprocess.run(["git", *args], cwd=_ROOT, capture_output=True,
                             text=True, timeout=10)
        return out.stdout.strip() if out.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def code_version() -> dict:
    """Git commit + working-tree cleanliness of the code that produced an artifact.

    The repo's ``ExperimentConfig.manifest_dict`` records the config but not the
    code version; E0.4 and E0.2 add this so a result can be traced to a commit.
    """
    dirty = _git("status", "--porcelain")
    return {
        "git_commit": _git("rev-parse", "HEAD"),
        "git_branch": _git("rev-parse", "--abbrev-ref", "HEAD"),
        "git_dirty": None if dirty is None else bool(dirty),
        "git_dirty_files": None if dirty is None else sorted(
            line[3:] for line in dirty.splitlines()),
    }


def write_manifest(path: Path, experiment: str, scale: int, **config) -> dict:
    """Write the provenance + config record that accompanies every E0.4 artifact."""
    manifest = {
        "experiment": experiment,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "scale": scale,
        "code_version": code_version(),
        "bulk95_definition": BULK95_DEFINITION,
        "config": config,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, default=str) + "\n")
    print(f"Saved {path}")
    return manifest

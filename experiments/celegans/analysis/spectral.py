"""Spectral analysis of the C. elegans connectome and its null ladder.

Characterises each substrate's recurrent matrix ``W`` (before rescaling) across
the three realism conditions x the 7-variant ladder, using the generic
``src.analysis.spectral`` tools. This materialises "Diagnostic 1" -- the spectral
basis of the prediction-task results: the connectome's heavy weights, placed on
its real (hub-concentrated) edges, compress its eigenvalue bulk relative to the
dominant mode, so at a matched nominal spectral radius its effective dynamics are
the mildest (least memory). Permuting the weights (the control) relaxes the
compression; degree/random nulls spread it further.

    python -m experiments.celegans.analysis.spectral

Outputs (here):
  figures/eigenvalue_spectra.png    normalized eigenvalues (lambda/|lambda_1|) in the complex plane
  figures/spectral_compression.png  bulk-compression bars (bulk95/|l1|, mean|l|/|l1|)
  figures/magnitude_decay.png       sorted |lambda|/|lambda_1| curves
  results/spectral_metrics.csv      seed-averaged metrics (all variants x conditions)
  results/spectral_metrics.md       compact markdown table (for slides)
"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np
import pandas as pd

from src.reservoir import blas  # noqa: F401  (limit BLAS threads; import early)
from src.analysis import spectral
from experiments.celegans.substrates import SubstrateBuilder
from experiments.celegans import matrix_config

_DIR = Path(__file__).resolve().parent
FIGURES_DIR = _DIR / "figures"
RESULTS_DIR = _DIR / "results"

CONDITIONS = matrix_config.CONDITIONS          # v2a, v2b, v2d
VARIANTS = matrix_config.VARIANTS              # all 7
# The scatter grid uses the four most informative variants (the decomposition:
# connectome -> control isolates placement; control -> degree isolates topology;
# degree -> random is the baseline) so the panels stay legible.
KEY_VARIANTS = ["connectome", "connectome_weight_permuted",
                "degree_rewire", "random_gaussian"]
N_SEEDS = 10
REPRESENTATIVE_SEED = 0  # eigenvalue positions aren't averageable; show one graph

CONDITION_TITLE = {
    "v2a": "v2a · undirected gaussian",
    "v2ae_randsign": "v2ae_randsign · undirected empirical ±",
    "v2ae": "v2ae · undirected empirical",
    "v2bg": "v2bg · directed gaussian",
    "v2b_randsign": "v2b_randsign · directed empirical ±",
    "v2b": "v2b · directed empirical",
    "v2d": "v2d · directed signed",
}
# Slide-clean condition labels (no v2a/v2b/... prefix) used for the eigenvalue
# spectra figure; the bars/decay figures and the table keep the prefixed labels.
CONDITION_TITLE_DISPLAY = {
    "v2a": "Undirected Gaussian",
    "v2ae_randsign": "Undirected Empirical ±",
    "v2ae": "Undirected Empirical",
    "v2bg": "Directed Gaussian",
    "v2b_randsign": "Directed Empirical ±",
    "v2b": "Directed Empirical",
    "v2d": "Directed Signed (Dale)",
}
VARIANT_TITLE = {
    "connectome": "connectome",
    "connectome_weight_permuted": "control (perm. wts)",
    "random_gaussian": "rung 0 (random)",
    "erdos_renyi": "rung 1 (ER)",
    "degree_rewire": "rung 2 (degree)",
    "clustering_rewire": "rung 3 (clustering)",
    "modularity_rewire": "rung 4 (modularity)",
}
VARIANT_COLOR = {
    "connectome": "black",
    "connectome_weight_permuted": "#9467bd",
    "random_gaussian": "#bbbbbb",
    "erdos_renyi": "#88aadd",
    "degree_rewire": "#e377c2",
    "clustering_rewire": "#2ca02c",
    "modularity_rewire": "#ff7f0e",
}

METRIC_KEYS = ["bulk95_ratio", "mean_ratio"]
METRIC_TITLES = ["bulk₉₅ / |λ₁|\n(lower = more compressed)",
                 "mean|λ| / |λ₁|\n(lower = more compressed)"]
# Columns shown in the compact markdown table for slides.
TABLE_COLS = ["spectral_radius", "lambda2_ratio", "bulk95_ratio",
              "mean_ratio", "participation_ratio", "n_critical"]


def _write_markdown_table(metrics_mean: dict, path: Path) -> None:
    lines = ["# C. elegans spectral metrics (seed-averaged)\n",
             "Scale-invariant ratios of the eigenvalue bulk to the dominant mode "
             "|λ₁|. Lower bulk₉₅/mean = more compressed bulk = milder effective "
             "dynamics at matched spectral radius.\n"]
    header = "| condition | variant | " + " | ".join(TABLE_COLS) + " |"
    sep = "|" + "---|" * (2 + len(TABLE_COLS))
    for cond in CONDITIONS:
        lines += [f"\n## {CONDITION_TITLE[cond]}\n", header, sep]
        for v in VARIANTS:
            m = metrics_mean[(cond, v)]
            cells = []
            for c in TABLE_COLS:
                cells.append(f"{m[c]:.0f}" if c in ("spectral_radius", "n_critical")
                             else f"{m[c]:.3f}")
            lines.append(f"| {cond} | {VARIANT_TITLE[v]} | " + " | ".join(cells) + " |")
    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    builder = SubstrateBuilder()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # --- seed-averaged scalar metrics for every (condition, variant) ----------
    rows, metrics_mean = [], {}
    for cond in CONDITIONS:
        for v in VARIANTS:
            per_seed = [spectral.spectral_metrics(builder.weighted(cond, v, s))
                        for s in range(N_SEEDS)]
            keys = list(per_seed[0])
            mean = {k: float(np.mean([m[k] for m in per_seed])) for k in keys}
            sem = {k: float(np.std([m[k] for m in per_seed]) / np.sqrt(N_SEEDS))
                   for k in keys}
            metrics_mean[(cond, v)] = mean
            row = dict(condition=cond, variant=v)
            for k in keys:
                row[k], row[f"{k}_sem"] = mean[k], sem[k]
            rows.append(row)

    pd.DataFrame(rows).to_csv(RESULTS_DIR / "spectral_metrics.csv", index=False)
    _write_markdown_table(metrics_mean, RESULTS_DIR / "spectral_metrics.md")
    print(f"Saved {RESULTS_DIR / 'spectral_metrics.csv'}")
    print(f"Saved {RESULTS_DIR / 'spectral_metrics.md'}")

    # --- representative spectra + decay curves (one seed) ---------------------
    spectra, decays = {}, {}
    for cond in CONDITIONS:
        for v in VARIANTS:
            W = builder.weighted(cond, v, REPRESENTATIVE_SEED)
            decays[(cond, v)] = spectral.magnitude_decay(W)
            if v in KEY_VARIANTS:
                spectra[(cond, v)] = spectral.normalized_eigenvalues(W)

    # --- figures --------------------------------------------------------------
    spectral.plot_eigenvalue_grid(
        spectra, CONDITIONS, KEY_VARIANTS, CONDITION_TITLE_DISPLAY, VARIANT_TITLE,
        VARIANT_COLOR, FIGURES_DIR / "eigenvalue_spectra.png",
        suptitle="Normalized eigenvalue spectra (λ / |λ₁|): connectome vs nulls",
    )
    print(f"Saved {FIGURES_DIR / 'eigenvalue_spectra.png'}")

    spectral.plot_metric_bars(
        metrics_mean, METRIC_KEYS, METRIC_TITLES, CONDITIONS, CONDITION_TITLE,
        VARIANTS, VARIANT_TITLE, VARIANT_COLOR,
        FIGURES_DIR / "spectral_compression.png",
        suptitle="Spectral bulk compression by variant (lower = milder effective dynamics)",
    )
    print(f"Saved {FIGURES_DIR / 'spectral_compression.png'}")

    spectral.plot_magnitude_decay(
        decays, CONDITIONS, CONDITION_TITLE, VARIANTS, VARIANT_TITLE,
        VARIANT_COLOR, FIGURES_DIR / "magnitude_decay.png",
        suptitle="Eigenvalue-magnitude decay: |λ| / |λ₁| (steeper = more compressed)",
    )
    print(f"Saved {FIGURES_DIR / 'magnitude_decay.png'}")

    # --- headline glance to stdout -------------------------------------------
    print("\nbulk95/|λ₁| (lower = more compressed bulk):")
    for cond in CONDITIONS:
        cells = "  ".join(f"{VARIANT_TITLE[v].split(' (')[0]}="
                          f"{metrics_mean[(cond, v)]['bulk95_ratio']:.3f}"
                          for v in KEY_VARIANTS)
        print(f"  [{cond}] {cells}")
    print("\nDone.")


if __name__ == "__main__":
    main()

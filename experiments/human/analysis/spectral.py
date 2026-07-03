"""Spectral analysis of the human SC and its undirected null ladder.

Characterises each substrate's recurrent matrix ``W`` (before rescaling) across
the three undirected conditions x the 7-variant ladder, using the generic
``src.analysis.spectral`` tools. Confirms the sign precondition on the REAL human
graph: ``human_empirical`` should be bulk-compressed (Perron spike over a crushed
bulk, n_critical ~ 1) and ``human_empirical_signed`` should de-compress it (signing
removes the Perron structure) -- the spectral basis of the predicted sign-primary
robustness crossover.

    python -m experiments.human.analysis.spectral

Outputs (here):
  figures/eigenvalue_spectra.png    normalized eigenvalues (lambda/|lambda_1|) in the complex plane
  figures/spectral_compression.png  bulk-compression bars (bulk95/|l1|, mean|l|/|l1|)
  figures/magnitude_decay.png       sorted |lambda|/|lambda_1| curves
  results/spectral_metrics.csv      seed-averaged metrics (all variants x conditions)
  results/spectral_metrics.md       compact markdown table
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
from experiments.human.substrates import HumanSubstrateBuilder
from experiments.human import matrix_config

_DIR = Path(__file__).resolve().parent
FIGURES_DIR = _DIR / "figures"
RESULTS_DIR = _DIR / "results"

CONDITIONS = matrix_config.CONDITIONS          # the 3 undirected conditions
VARIANTS = matrix_config.VARIANTS              # all 7
KEY_VARIANTS = ["connectome", "connectome_weight_permuted",
                "degree_rewire", "random_gaussian"]
N_SEEDS = 10
REPRESENTATIVE_SEED = 0  # eigenvalue positions aren't averageable; show one graph

CONDITION_TITLE = {
    "human_gaussian": "Human · gaussian",
    "human_empirical_signed": "Human · empirical ±",
    "human_empirical": "Human · empirical",
}
CONDITION_TITLE_DISPLAY = {
    "human_gaussian": "Human Gaussian",
    "human_empirical_signed": "Human Empirical ±",
    "human_empirical": "Human Empirical",
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
TABLE_COLS = ["spectral_radius", "lambda2_ratio", "bulk95_ratio",
              "mean_ratio", "participation_ratio", "n_critical"]


def _write_markdown_table(metrics_mean: dict, path: Path) -> None:
    lines = ["# Human SC spectral metrics (seed-averaged)\n",
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
    builder = HumanSubstrateBuilder()
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
        suptitle="Human SC normalized eigenvalue spectra (λ / |λ₁|): connectome vs nulls",
    )
    print(f"Saved {FIGURES_DIR / 'eigenvalue_spectra.png'}")

    spectral.plot_metric_bars(
        metrics_mean, METRIC_KEYS, METRIC_TITLES, CONDITIONS, CONDITION_TITLE,
        VARIANTS, VARIANT_TITLE, VARIANT_COLOR,
        FIGURES_DIR / "spectral_compression.png",
        suptitle="Human SC spectral bulk compression by variant (lower = milder effective dynamics)",
    )
    print(f"Saved {FIGURES_DIR / 'spectral_compression.png'}")

    spectral.plot_magnitude_decay(
        decays, CONDITIONS, CONDITION_TITLE, VARIANTS, VARIANT_TITLE,
        VARIANT_COLOR, FIGURES_DIR / "magnitude_decay.png",
        suptitle="Human SC eigenvalue-magnitude decay: |λ| / |λ₁| (steeper = more compressed)",
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

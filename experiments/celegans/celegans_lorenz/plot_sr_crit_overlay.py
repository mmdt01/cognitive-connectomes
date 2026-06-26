"""Overlay each variant's bulk-critical spectral radius on the Lorenz sweep figures.

``sr_crit = 1 / bulk95_ratio`` is where a variant's 95th-percentile eigenvalue
magnitude reaches the unit circle under top-eigenvalue rescaling -- i.e. where its
compressed bulk finally becomes critical. This driver overlays those markers on the
wide-sweep VPT and climate-vs-spectral-radius curves, materialising the C. elegans
"effective-criticality robustness layer": each variant enters the Lorenz-
reconstructing regime around its own ``sr_crit``, and the connectome's
(``sr_crit ~ 3.3`` vs ``~2.2-2.7`` for the nulls) sits *beyond* the old sweep's max
of 2.0 -- which is why the narrow sweep manufactured an artefactual supercritical
deficit. Top-eigenvalue matching is unchanged; the marker just reads where, under
that same matching, the bulk goes critical.

Reads the Lorenz ``results.parquet`` (performance) and the committed
``analysis/results/spectral_metrics.csv`` (``bulk95_ratio``); no recomputation.

    python -m experiments.celegans.celegans_lorenz.plot_sr_crit_overlay
"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

from experiments.celegans import matrix_config

_DIR = Path(__file__).resolve().parent
RESULTS = _DIR / "results" / "results.parquet"
SPECTRAL = _ROOT / "experiments/celegans/analysis/results/spectral_metrics.csv"
OUT = _DIR / "figures" / "sr_crit_overlay.png"

OLD_SWEEP_MAX = 2.0  # the previous linspace(0, 2, 20) ceiling

# Match the main figures' palette/labels (kept local so this script touches no
# generic module).
VARIANT_COLOR = {
    "connectome": "black",
    "connectome_weight_permuted": "#9467bd",
    "random_gaussian": "#bbbbbb",
    "erdos_renyi": "#88aadd",
    "degree_rewire": "#e377c2",
    "clustering_rewire": "#2ca02c",
    "modularity_rewire": "#ff7f0e",
}
VARIANT_LABEL = {
    "connectome": "connectome",
    "connectome_weight_permuted": "connectome · perm. weights",
    "random_gaussian": "rung 0 · random",
    "erdos_renyi": "rung 1 · ER",
    "degree_rewire": "rung 2 · degree",
    "clustering_rewire": "rung 3 · clustering",
    "modularity_rewire": "rung 4 · modularity",
}
VARIANTS = list(VARIANT_COLOR)

# (metric, ymax, lower_is_better, y-label)
METRICS = [
    ("vpt", 6.0, False, "VPT (Lyapunov times)  ↑ better"),
    ("climate_error", 10.0, True, "climate error ($W_1$)  ↓ better"),
]


def main() -> None:
    results = pd.read_parquet(RESULTS)
    spectral = pd.read_csv(SPECTRAL)
    sr_crit = {
        (r.condition, r.variant): 1.0 / r.bulk95_ratio
        for r in spectral.itertuples()
        if r.bulk95_ratio > 1e-9
    }

    conditions = [c for c in matrix_config.CONDITIONS
                  if c in results.condition.unique()]
    grouped = (results.groupby(["condition", "variant", "spectral_radius"])
               .agg(mean_vpt=("vpt", "mean"), sem_vpt=("vpt", "sem"),
                    mean_climate_error=("climate_error", "mean"),
                    sem_climate_error=("climate_error", "sem"))
               .reset_index())

    nrows, ncols = len(METRICS), len(conditions)
    fig, axes = plt.subplots(nrows, ncols, figsize=(6 * ncols, 4.6 * nrows),
                             squeeze=False, sharex=True)

    for i, (metric, ymax, lower_better, ylabel) in enumerate(METRICS):
        for j, condition in enumerate(conditions):
            ax = axes[i][j]
            xmax = max(matrix_config.SPECTRAL_RADII)
            # Light-green shade = the CONNECTOME's own supercritical region: where
            # its compressed bulk has reached/passed criticality (sr >= its sr_crit),
            # i.e. its genuine operating regime -- not the generic top-eigenvalue
            # supercritical band (sr > 1), which is misleading for a spiked spectrum.
            src_c = sr_crit.get((condition, "connectome"))
            if src_c is not None and src_c < xmax:
                ax.axvspan(src_c, xmax, color="#2e7d32", alpha=0.10, zorder=0)
            ax.axvline(1.0, color="grey", lw=0.8, ls=":", zorder=1)
            # old narrow-sweep ceiling -- the truncation that hid the recovery
            ax.axvline(OLD_SWEEP_MAX, color="firebrick", lw=1.3, ls="-", zorder=2,
                       alpha=0.7)

            for v in VARIANTS:
                sub = grouped[(grouped.condition == condition)
                              & (grouped.variant == v)].sort_values("spectral_radius")
                if sub.empty:
                    continue
                color = VARIANT_COLOR[v]
                mean, sem = sub[f"mean_{metric}"], sub[f"sem_{metric}"]
                lw = 2.4 if v == "connectome" else 1.5
                ax.plot(sub.spectral_radius, mean, color=color, lw=lw,
                        marker="o" if v == "connectome" else None, ms=3,
                        label=VARIANT_LABEL[v], zorder=5 if v == "connectome" else 4)
                ax.fill_between(sub.spectral_radius, mean - sem, mean + sem,
                                color=color, alpha=0.12, zorder=3)
                # sr_crit marker for this variant (where its bulk goes critical)
                src = sr_crit.get((condition, v))
                if src is not None and src <= max(matrix_config.SPECTRAL_RADII):
                    ax.axvline(src, color=color, lw=1.4, ls="--",
                               alpha=0.9 if v == "connectome" else 0.45, zorder=2)

            # annotate the connectome's sr_crit prominently
            src_c = sr_crit.get((condition, "connectome"))
            if src_c is not None:
                y_txt = ymax * (0.92 if not lower_better else 0.92)
                ax.text(src_c + 0.05, y_txt,
                        f"connectome\n$sr_{{crit}}$={src_c:.2f}", fontsize=7.5,
                        color="black", va="top", ha="left")

            ax.set_ylim(0, ymax)
            ax.set_xlim(0, max(matrix_config.SPECTRAL_RADII))
            ax.grid(alpha=0.25)
            if i == 0:
                ax.set_title(matrix_config.CONDITION_SPEC[condition]["label"],
                             fontsize=10)
            if i == nrows - 1:
                ax.set_xlabel("spectral radius (top-eigenvalue target)")
            if j == 0:
                ax.set_ylabel(ylabel, fontsize=10)

    # one shared legend; note the marker semantics
    handles, labels = axes[0][0].get_legend_handles_labels()
    extra = [
        plt.Line2D([0], [0], color="firebrick", lw=1.3, label=f"old sweep max ({OLD_SWEEP_MAX:g})"),
        plt.Line2D([0], [0], color="grey", lw=1.4, ls="--", label="$sr_{crit}=1/$bulk$_{95}$ (per variant)"),
        mpatches.Patch(color="#2e7d32", alpha=0.10,
                       label="connectome supercritical (sr ≥ $sr_{crit}$)"),
    ]
    axes[0][0].legend(handles + extra, labels + [h.get_label() for h in extra],
                      fontsize=7.5, framealpha=0.92, loc="upper right", ncol=1)

    fig.suptitle("Lorenz wide sweep: performance vs spectral radius, with each "
                 "variant's bulk-critical $sr_{crit}$ overlaid\n"
                 "(dashed verticals = where each variant's 95th-pct |λ| reaches the "
                 "unit circle; recovery tracks $sr_{crit}$)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {OUT}")

    # stdout: sr_crit table + connectome recovery check
    print("\nsr_crit = 1/bulk95_ratio per variant:")
    for condition in conditions:
        cells = "  ".join(f"{v.split('_')[0]}={sr_crit[(condition, v)]:.2f}"
                          for v in VARIANTS if (condition, v) in sr_crit)
        print(f"  [{condition}] {cells}")


if __name__ == "__main__":
    main()

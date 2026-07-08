"""Routing-specific figures.

The generic ``src/experiment/plots.py`` is single-metric and KeyErrors on unknown
variants, so the routing thread renders its own **per-aperture MC-vs-sr grid** --
one panel per readout aperture (pooled cortex + each Yeo network), connectome vs the
key nulls + placement controls, each curve's peak-sr marked. Shows whether the
connectome-vs-null crossover survives a restricted readout and where each aperture
peaks. (The Suárez-style presentation figure lives in ``plot_routing_summary.py``.)
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Local styles (the generic dict lacks the routing control variants).
_STYLE = {
    "connectome": dict(color="black", lw=2.4, marker="o", ms=3, zorder=5),
    "connectome_random_readout": dict(color="#d62728", lw=1.8, ls="-.",
                                      marker="^", ms=3, zorder=4),
    "connectome_dense_input": dict(color="#17becf", lw=1.8, ls=":",
                                   marker="D", ms=3, zorder=4),
    "connectome_weight_permuted": dict(color="#9467bd", lw=1.5, ls="-."),
    "degree_rewire": dict(color="#e377c2", lw=1.6),
    "random_gaussian": dict(color="#bbbbbb", lw=1.3, ls="--"),
    "erdos_renyi": dict(color="#88aadd", lw=1.3, ls="--"),
    "clustering_rewire": dict(color="#2ca02c", lw=1.4),
    "modularity_rewire": dict(color="#ff7f0e", lw=1.4),
}
_LABEL = {
    "connectome": "connectome (anatomical I/O)",
    "connectome_random_readout": "connectome · random cortical readout",
    "connectome_dense_input": "connectome · dense input",
    "connectome_weight_permuted": "connectome · perm. weights",
    "degree_rewire": "rung 2 · degree",
    "random_gaussian": "rung 0 · random",
    "erdos_renyi": "rung 1 · ER",
    "clustering_rewire": "rung 3 · clustering",
    "modularity_rewire": "rung 4 · modularity",
}


def _mean_curve(results, variant, metric):
    sub = (results[results.variant == variant]
           .groupby("spectral_radius")[metric].mean().reset_index()
           .sort_values("spectral_radius"))
    return sub.spectral_radius.values, sub[metric].values


def _peak_sr(srs, vals):
    if len(vals) == 0 or not np.isfinite(vals).any():
        return np.nan, np.nan
    i = int(np.nanargmax(vals))
    return float(srs[i]), float(vals[i])


def plot_aperture_curves(results, apertures, aperture_sizes, path,
                         variants=("connectome", "connectome_dense_input",
                                   "connectome_random_readout", "degree_rewire",
                                   "random_gaussian")):
    n = len(apertures)
    ncols = 4
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.6 * ncols, 3.8 * nrows),
                             squeeze=False)
    axes_flat = axes.flatten()
    for ax, aperture in zip(axes_flat, apertures):
        metric = f"mc_{aperture}"
        for variant in variants:
            if variant not in results.variant.unique():
                continue
            srs, vals = _mean_curve(results, variant, metric)
            style = _STYLE[variant]
            ax.plot(srs, vals, label=_LABEL[variant], **style)
            psr, pval = _peak_sr(srs, vals)
            if np.isfinite(psr):
                ax.axvline(psr, color=style["color"], lw=0.7, ls=":", alpha=0.6)
        ax.axvline(1.0, color="grey", lw=0.8, ls=":", zorder=0)
        ax.set_title(f"readout: {aperture}  (n={aperture_sizes[aperture]})", fontsize=10)
        ax.set_xlabel("spectral radius")
        ax.set_ylabel("memory capacity")
        ax.grid(alpha=0.25)
    for ax in axes_flat[n:]:
        ax.axis("off")
    axes_flat[0].legend(fontsize=7, framealpha=0.9, loc="upper right")
    fig.suptitle("MC vs spectral radius per readout aperture "
                 "(dotted verticals = each curve's peak-sr)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def run(cfg, apertures, aperture_sizes) -> None:
    cfg.figures_dir.mkdir(parents=True, exist_ok=True)
    results = pd.read_parquet(cfg.results_parquet)
    curves = cfg.figures_dir / "mc_vs_sr_per_aperture.png"
    plot_aperture_curves(results, apertures, aperture_sizes, curves)
    print(f"Saved {curves}")

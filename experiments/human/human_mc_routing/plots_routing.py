"""Routing-specific figures.

The generic ``src/experiment/plots.py`` is single-metric and KeyErrors on unknown
variants, so the routing thread renders its own:

  1. **Per-aperture MC-vs-sr grid** -- one panel per readout aperture (pooled cortex
     + each Yeo network), connectome vs the key nulls + the random-placement
     control, each curve's peak-sr marked. Shows whether the connectome-vs-null
     crossover survives a restricted readout and where each aperture peaks.
  2. **Peak-sr vs aperture size** -- the Suárez readout-aperture story: does the MC
     peak walk from supercritical (full readout) down toward the edge of chaos
     (sr~1) as the readout shrinks, and does anatomical placement change that.
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


def plot_peak_shift(results, apertures, aperture_sizes, path,
                    variants=("connectome", "connectome_dense_input",
                              "degree_rewire")):
    fig, (ax_sr, ax_mc) = plt.subplots(1, 2, figsize=(12, 5))
    for variant in variants:
        if variant not in results.variant.unique():
            continue
        sizes, peak_srs, peak_mcs = [], [], []
        for aperture in apertures:
            srs, vals = _mean_curve(results, variant, f"mc_{aperture}")
            psr, pmc = _peak_sr(srs, vals)
            sizes.append(aperture_sizes[aperture])
            peak_srs.append(psr)
            peak_mcs.append(pmc)
        order = np.argsort(sizes)
        sizes = np.asarray(sizes)[order]
        peak_srs = np.asarray(peak_srs)[order]
        peak_mcs = np.asarray(peak_mcs)[order]
        style = _STYLE[variant]
        ax_sr.plot(sizes, peak_srs, marker="o", label=_LABEL[variant],
                   color=style["color"], lw=1.8)
        ax_mc.plot(sizes, peak_mcs, marker="o", label=_LABEL[variant],
                   color=style["color"], lw=1.8)
    for ax in (ax_sr, ax_mc):
        ax.set_xscale("log")
        ax.set_xlabel("readout aperture size (# nodes, log)")
        ax.grid(alpha=0.25)
    ax_sr.axhline(1.0, color="grey", lw=0.9, ls="--")
    ax_sr.set_ylabel("peak-MC spectral radius")
    ax_sr.set_title("Where MC peaks vs readout aperture")
    ax_mc.set_ylabel("peak memory capacity")
    ax_mc.set_title("Peak MC vs readout aperture")
    ax_sr.legend(fontsize=8)
    fig.suptitle("Operating point (peak-MC spectral radius) per readout aperture: "
                 "anatomical subcortical input vs dense-input reference", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def run(cfg, apertures, aperture_sizes) -> None:
    cfg.figures_dir.mkdir(parents=True, exist_ok=True)
    results = pd.read_parquet(cfg.results_parquet)
    curves = cfg.figures_dir / "mc_vs_sr_per_aperture.png"
    shift = cfg.figures_dir / "peak_sr_vs_aperture.png"
    plot_aperture_curves(results, apertures, aperture_sizes, curves)
    plot_peak_shift(results, apertures, aperture_sizes, shift)
    print(f"Saved {curves}")
    print(f"Saved {shift}")

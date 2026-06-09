"""Figures for the NARMA-10 bridge.

1. NRMSE vs spectral radius: one panel per condition, the connectome and all
   five nulls as separate lines (mean +/- SEM over seeds), supercritical region
   shaded. Lower is better.
2. Effect-size summary: Cohen's d (connectome vs each null, performance
   direction) across the sweep, one panel per condition. d > 0 => connectome
   beats the null.

Saved to ``figures/`` at 300 dpi.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import config

_VARIANT_STYLE = {
    "connectome": dict(color="black", lw=2.4, zorder=5, marker="o", ms=4),
    "random_gaussian": dict(color="#bbbbbb", lw=1.3, ls="--"),
    "erdos_renyi": dict(color="#88aadd", lw=1.3, ls="--"),
    "degree_rewire": dict(color="#e377c2", lw=1.6),
    "clustering_rewire": dict(color="#2ca02c", lw=1.6),
    "modularity_rewire": dict(color="#ff7f0e", lw=1.6),
}
_VARIANT_LABEL = {
    "connectome": "connectome",
    "random_gaussian": "rung 0 · random",
    "erdos_renyi": "rung 1 · ER",
    "degree_rewire": "rung 2 · degree",
    "clustering_rewire": "rung 3 · clustering",
    "modularity_rewire": "rung 4 · modularity",
}


def _supercritical_span(ax):
    lo = min(config.SUPERCRITICAL_RADII)
    ax.axvspan(lo, max(config.SPECTRAL_RADII), color="#fff3e0", zorder=0)
    ax.axvline(1.0, color="grey", lw=0.8, ls=":", zorder=1)


def plot_nrmse_vs_sr(results: pd.DataFrame, path: Path) -> None:
    conditions = [c for c in config.CONDITIONS if c in results.condition.unique()]
    fig, axes = plt.subplots(1, len(conditions), figsize=(6 * len(conditions), 5),
                             sharey=True, squeeze=False)
    axes = axes[0]
    grouped = (results.groupby(["condition", "variant", "spectral_radius"])["nrmse"]
               .agg(["mean", "sem"]).reset_index())
    for ax, condition in zip(axes, conditions):
        for variant in config.VARIANTS:
            sub = grouped[(grouped.condition == condition) & (grouped.variant == variant)]
            sub = sub.sort_values("spectral_radius")
            if sub.empty:
                continue
            style = _VARIANT_STYLE[variant]
            ax.plot(sub.spectral_radius, sub["mean"], label=_VARIANT_LABEL[variant], **style)
            ax.fill_between(sub.spectral_radius, sub["mean"] - sub["sem"],
                            sub["mean"] + sub["sem"], color=style["color"], alpha=0.15)
        _supercritical_span(ax)
        ax.set_title(config.CONDITION_SPEC[condition]["label"], fontsize=11)
        ax.set_xlabel("spectral radius")
        ax.grid(alpha=0.25)
    axes[0].set_ylabel("NARMA-10 NRMSE  (lower = better)")
    axes[-1].legend(fontsize=8, framealpha=0.9, loc="upper right")
    fig.suptitle("NARMA-10 emulation: connectome vs null ladder", fontsize=13)
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_effect_sizes(stats: pd.DataFrame, path: Path) -> None:
    conditions = [c for c in config.CONDITIONS if c in stats.condition.unique()]
    fig, axes = plt.subplots(1, len(conditions), figsize=(6 * len(conditions), 5),
                             sharey=True, squeeze=False)
    axes = axes[0]
    for ax, condition in zip(axes, conditions):
        cond = stats[stats.condition == condition]
        for variant in config.NULL_VARIANTS:
            sub = cond[cond.null_variant == variant].sort_values("spectral_radius")
            if sub.empty:
                continue
            style = _VARIANT_STYLE[variant]
            ax.plot(sub.spectral_radius, sub.cohens_d, label=_VARIANT_LABEL[variant],
                    color=style["color"], lw=style.get("lw", 1.5),
                    ls=style.get("ls", "-"))
            sig = sub[sub.significant]
            ax.scatter(sig.spectral_radius, sig.cohens_d, color=style["color"],
                       s=40, zorder=5, edgecolor="black", linewidth=0.5)
        _supercritical_span(ax)
        ax.axhline(0.0, color="black", lw=1.0)
        ax.set_title(config.CONDITION_SPEC[condition]["label"], fontsize=11)
        ax.set_xlabel("spectral radius")
        ax.grid(alpha=0.25)
    axes[0].set_ylabel("Cohen's d  (>0 ⇒ connectome better)")
    axes[-1].legend(fontsize=8, framealpha=0.9, loc="best")
    fig.suptitle("Connectome vs null: effect size across the sweep "
                 "(filled markers = Holm-significant)", fontsize=12)
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    results = pd.read_parquet(config.RESULTS_PARQUET)
    plot_nrmse_vs_sr(results, config.FIGURES_DIR / "nrmse_vs_spectral_radius.png")
    print(f"Saved {config.FIGURES_DIR / 'nrmse_vs_spectral_radius.png'}")
    if config.STATS_PARQUET.exists():
        stats = pd.read_parquet(config.STATS_PARQUET)
        plot_effect_sizes(stats, config.FIGURES_DIR / "effect_sizes_vs_spectral_radius.png")
        print(f"Saved {config.FIGURES_DIR / 'effect_sizes_vs_spectral_radius.png'}")


if __name__ == "__main__":
    main()

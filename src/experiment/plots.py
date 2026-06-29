"""Generic figures: metric-vs-spectral-radius panels + effect-size summary.

Task-agnostic; reads everything it needs from ``cfg`` (metric column/label,
no-skill reference line, y-cap, condition labels, supercritical region). One
panel per condition, the connectome and all nulls overlaid.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

_VARIANT_STYLE = {
    "connectome": dict(color="black", lw=2.4, zorder=5, marker="o", ms=4),
    "connectome_weight_permuted": dict(color="#9467bd", lw=1.8, ls="-.",
                                       marker="s", ms=3, zorder=4),
    "random_gaussian": dict(color="#bbbbbb", lw=1.3, ls="--"),
    "erdos_renyi": dict(color="#88aadd", lw=1.3, ls="--"),
    "degree_rewire": dict(color="#e377c2", lw=1.6),
    "clustering_rewire": dict(color="#2ca02c", lw=1.6),
    "modularity_rewire": dict(color="#ff7f0e", lw=1.6),
}
_VARIANT_LABEL = {
    "connectome": "connectome",
    "connectome_weight_permuted": "connectome · perm. weights",
    "random_gaussian": "rung 0 · random",
    "erdos_renyi": "rung 1 · ER",
    "degree_rewire": "rung 2 · degree",
    "clustering_rewire": "rung 3 · clustering",
    "modularity_rewire": "rung 4 · modularity",
}


_SUPERCRITICAL_COLOR = "#fff3e0"


def _supercritical_span(ax, cfg, condition=None):
    # Shade where the connectome's eigenvalue bulk is supercritical (sr >= its
    # sr_crit = 1/bulk95_ratio), per condition, when the run supplies it; else
    # fall back to the fixed nominal-supercritical threshold.
    span = getattr(cfg, "supercritical_span", None)
    start = span.get(condition) if (span and condition in span) else None
    if start is None:
        start = min(cfg.supercritical_radii)
    ax.axvspan(start, max(cfg.spectral_radii), color=_SUPERCRITICAL_COLOR, zorder=0)
    ax.axvline(1.0, color="grey", lw=0.8, ls=":", zorder=1)


def _supercritical_legend_handle(cfg):
    """Legend proxy explaining the shaded band."""
    if getattr(cfg, "supercritical_span", None):
        label = "connectome eigenvalue-bulk\nsupercritical (sr ≥ $sr_{crit}$)"
    else:
        label = f"supercritical (sr ≥ {min(cfg.supercritical_radii):g})"
    return mpatches.Patch(facecolor=_SUPERCRITICAL_COLOR, edgecolor="none", label=label)


def plot_metric_vs_sr(results: pd.DataFrame, cfg, path: Path) -> None:
    metric = cfg.metric
    conditions = [c for c in cfg.conditions if c in results.condition.unique()]
    fig, axes = plt.subplots(1, len(conditions), figsize=(6 * len(conditions), 5),
                             sharey=True, squeeze=False)
    axes = axes[0]
    grouped = (results.groupby(["condition", "variant", "spectral_radius"])[metric]
               .agg(["mean", "sem"]).reset_index())
    for ax, condition in zip(axes, conditions):
        for variant in cfg.variants:
            sub = grouped[(grouped.condition == condition)
                          & (grouped.variant == variant)].sort_values("spectral_radius")
            if sub.empty:
                continue
            style = _VARIANT_STYLE[variant]
            ax.plot(sub.spectral_radius, sub["mean"], label=_VARIANT_LABEL[variant], **style)
            ax.fill_between(sub.spectral_radius, sub["mean"] - sub["sem"],
                            sub["mean"] + sub["sem"], color=style["color"], alpha=0.15)
        _supercritical_span(ax, cfg, condition)
        if cfg.metric_no_skill is not None:
            ax.axhline(cfg.metric_no_skill, color="grey", lw=0.9, ls="--", zorder=1)
        if cfg.metric_ymax is not None:
            ax.set_ylim(0, cfg.metric_ymax)
        ax.set_title(cfg.condition_spec[condition]["label"], fontsize=11)
        ax.set_xlabel("spectral radius")
        ax.grid(alpha=0.25)
    axes[0].set_ylabel(cfg.metric_label)
    if cfg.metric_no_skill is not None:
        axes[0].text(0.04, cfg.metric_no_skill + 0.02 * (cfg.metric_ymax or 1.0),
                     f"no skill ({metric} = {cfg.metric_no_skill:g})",
                     fontsize=7, color="grey")
    handles, labels = axes[-1].get_legend_handles_labels()
    patch = _supercritical_legend_handle(cfg)
    axes[-1].legend(handles + [patch], labels + [patch.get_label()],
                    fontsize=8, framealpha=0.9, loc="upper left",
                    bbox_to_anchor=(1.02, 1.0))
    fig.suptitle(f"{cfg.task_name}: connectome vs null ladder", fontsize=13)
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_effect_sizes(stats: pd.DataFrame, cfg, path: Path) -> None:
    conditions = [c for c in cfg.conditions if c in stats.condition.unique()]
    fig, axes = plt.subplots(1, len(conditions), figsize=(6 * len(conditions), 5),
                             sharey=True, squeeze=False)
    axes = axes[0]
    for ax, condition in zip(axes, conditions):
        cond = stats[stats.condition == condition]
        for variant in cfg.null_variants:
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
        _supercritical_span(ax, cfg, condition)
        ax.axhline(0.0, color="black", lw=1.0)
        ax.set_title(cfg.condition_spec[condition]["label"], fontsize=11)
        ax.set_xlabel("spectral radius")
        ax.grid(alpha=0.25)
    axes[0].set_ylabel("Cohen's d  (>0 ⇒ connectome better)")
    handles, labels = axes[-1].get_legend_handles_labels()
    patch = _supercritical_legend_handle(cfg)
    axes[-1].legend(handles + [patch], labels + [patch.get_label()],
                    fontsize=8, framealpha=0.9, loc="upper left",
                    bbox_to_anchor=(1.02, 1.0))
    fig.suptitle("Connectome vs null: effect size across the sweep "
                 "(filled markers = Holm-significant)", fontsize=12)
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def run(cfg) -> None:
    cfg.figures_dir.mkdir(parents=True, exist_ok=True)
    results = pd.read_parquet(cfg.results_parquet)
    metric_fig = cfg.figures_dir / f"{cfg.metric}_vs_spectral_radius.png"
    plot_metric_vs_sr(results, cfg, metric_fig)
    print(f"Saved {metric_fig}")
    if cfg.stats_parquet.exists():
        stats = pd.read_parquet(cfg.stats_parquet)
        # Metric-tagged so a two-metric task (Lorenz) doesn't overwrite one
        # metric's effect-size figure with the other's.
        effect_fig = cfg.figures_dir / f"effect_sizes_{cfg.metric}_vs_spectral_radius.png"
        plot_effect_sizes(stats, cfg, effect_fig)
        print(f"Saved {effect_fig}")

"""Act III, memory arm -- chapter 6, contribution 3.

The crossing, the scale-invariant supercritical margin, peak parity, and the rescue
from Perron domination.

Owned by session 3 (`report/act3a_memory.md`).
"""

import numpy as np
import matplotlib.pyplot as plt

from report.figlib import style
from report.figlib.figures.common import N_NODES

OVERLAP_TOP = 2.599          # top of the four-variant overlap on the matched axis


def f7_the_crossing(ctx):
    """Peaks lowest, retains most. The crossing, not the peak, is the result."""
    frame = ctx.frame("taskb")
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0),
                             gridspec_kw=dict(width_ratios=[1.7, 1]))

    retained = {}
    for variant in style.ordered_variants(frame.variant.unique()):
        curve = (frame[frame.variant == variant]
                 .groupby("spectral_radius")
                 .agg(x=("x", "median"), d_eff=("d_eff", "median"))
                 .sort_values("x"))
        axes[0].plot(curve.x, curve.d_eff, **style.variant_kwargs(variant))
        peak = curve.d_eff.max()
        at_top = float(np.interp(OVERLAP_TOP, curve.x, curve.d_eff))
        retained[variant] = (peak, at_top, at_top / peak)
        axes[0].plot([curve.x[curve.d_eff.idxmax()]], [peak], marker="o", ms=4,
                     color=style.VARIANT_COLOUR[variant], zorder=6)

    style.draw_ceiling(axes[0], N_NODES)
    axes[0].axvline(OVERLAP_TOP, color=style.ANNOTATION_COLOUR, lw=0.8, ls="--")
    axes[0].text(OVERLAP_TOP, 0.98, " top of overlap ", transform=axes[0].get_xaxis_transform(),
                 fontsize=style.TICK_SIZE, va="top", color=style.ANNOTATION_COLOUR)
    axes[0].set_xlim(0, OVERLAP_TOP * 1.12)
    axes[0].set_xlabel(style.AXIS_LABEL["effective"])
    axes[0].set_ylabel(r"$d_{\rm eff}$")
    style.legend(axes[0], loc="lower left", fontsize=style.LEGEND_SIZE - 1)

    variants = list(retained)
    positions = np.arange(len(variants))
    axes[1].bar(positions, [100 * retained[v][2] for v in variants],
                color=[style.VARIANT_COLOUR[v] for v in variants],
                edgecolor="white", linewidth=0.5)
    for position, variant in zip(positions, variants):
        axes[1].text(position, 100 * retained[variant][2] + 1,
                     f"{100 * retained[variant][2]:.0f}%", ha="center",
                     fontsize=style.TICK_SIZE)
    axes[1].set_xticks(positions)
    axes[1].set_xticklabels([style.VARIANT_LABEL[v].replace(" · ", "\n") for v in variants],
                            fontsize=style.TICK_SIZE - 1)
    axes[1].set_ylabel(f"% of own peak retained\nat $\\sigma\\cdot$bulk95 = {OVERLAP_TOP}")
    axes[1].grid(axis="x", visible=False)
    for ax, letter in zip(axes, "ab"):
        style.panel_label(ax, letter, dx=-0.10)
    fig.tight_layout()
    return fig


def f9_scale_invariance(ctx):
    """The supercritical margin is not an N=448 accident."""
    frame = ctx.frame("n1000")
    from report.figlib.sources import SR_CRIT
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.8))

    # Supercritical = sigma >= the CONNECTOME's sr_crit, applied to every variant.
    variants = style.ordered_variants(frame.variant.unique())
    positions = np.arange(len(variants))
    width = 0.36
    margins = {}
    for offset, scale, alpha in ((-width / 2, 448, 1.0), (width / 2, 1000, 0.45)):
        threshold = SR_CRIT[scale]["connectome"]
        values = [frame[(frame.variant == v) & (frame.n_nodes == scale)
                        & (frame.spectral_radius >= threshold)].mc.median()
                  for v in variants]
        axes[0].bar(positions + offset, values, width, alpha=alpha,
                    color=[style.VARIANT_COLOUR[v] for v in variants],
                    edgecolor="white", linewidth=0.5)
        lookup = dict(zip(variants, values))
        if "connectome" in lookup and "erdos_renyi" in lookup:
            margins[scale] = lookup["connectome"] / lookup["erdos_renyi"]
    axes[0].set_xticks(positions)
    axes[0].set_xticklabels([style.VARIANT_LABEL[v].replace(" · ", "\n") for v in variants],
                            fontsize=style.TICK_SIZE - 1)
    axes[0].set_ylabel("supercritical MC (median)")
    axes[0].grid(axis="x", visible=False)
    axes[0].set_title(r"$\sigma \geq$ the connectome's $sr_{\rm crit}$",
                      fontsize=style.TITLE_SIZE - 1)

    for scale, dash in ((448, "-"), (1000, "--")):
        for variant in ("connectome", "erdos_renyi"):
            curve = (frame[(frame.variant == variant) & (frame.n_nodes == scale)]
                     .groupby("spectral_radius").mc.median())
            axes[1].plot(curve.index, curve.values, ls=dash,
                         color=style.VARIANT_COLOUR[variant],
                         lw=style.VARIANT_LINEWIDTH[variant],
                         label=f"{style.VARIANT_LABEL[variant]}, N = {scale}")
    axes[1].set_xlabel(r"nominal $\sigma$")
    axes[1].set_ylabel("MC")
    text = "  ".join(f"N={s}: {m:.2f}x" for s, m in sorted(margins.items()))
    axes[1].set_title(f"connectome / ER margin   {text}", fontsize=style.TITLE_SIZE - 1)
    style.legend(axes[1], loc="upper right", fontsize=style.LEGEND_SIZE - 2)
    for ax, letter in zip(axes, "ab"):
        style.panel_label(ax, letter, dx=-0.10)
    fig.tight_layout()
    return fig


def f10_peak_parity(ctx):
    """Parity at the peak, with the CIs that forbid writing "always worst"."""
    frame = ctx.frame("peak_parity").copy()
    frame["null"] = frame.contrast.str.replace("connectome - ", "", regex=False)
    alphas = sorted(frame.alpha.unique())
    nulls = [n for n in style.VARIANT_ORDER if n in set(frame.null)]
    fig, ax = plt.subplots(figsize=(5.4, 3.2))

    offsets = np.linspace(-0.26, 0.26, len(nulls))
    for offset, null in zip(offsets, nulls):
        sub = frame[frame.null == null].set_index("alpha").reindex(alphas)
        y = np.arange(len(alphas)) + offset
        ax.errorbar(sub.mean_diff, y,
                    xerr=[sub.mean_diff - sub.ci_lo, sub.ci_hi - sub.mean_diff],
                    fmt="o", ms=4, lw=1.2, capsize=2.5,
                    color=style.VARIANT_COLOUR[null], label=style.VARIANT_LABEL[null])
    ax.axvline(0, color=style.ANNOTATION_COLOUR, lw=0.9)
    ax.set_yticks(np.arange(len(alphas)))
    ax.set_yticklabels([f"$\\alpha$ = {a:g}" for a in alphas])
    ax.invert_yaxis()
    ax.set_xlabel("paired peak MC difference  (connectome $-$ null)")
    ax.grid(axis="y", visible=False)
    style.legend(ax, loc="lower left", fontsize=style.LEGEND_SIZE - 1)
    style.panel_label(ax, "a", dx=-0.06)
    fig.tight_layout()
    return fig


def f11_perron_rescue(ctx):
    """The advantage is resistance to Perron domination, and bulk95 only partly explains it."""
    extension = ctx.frame("f_extension")
    matched = ctx.frame("mechanism_matched")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.8))

    memory = extension[(extension.task == "mc")
                       & (np.isclose(extension.spectral_radius, 6.0))]
    for variant in style.ordered_variants(memory.variant.unique()):
        curve = (memory[memory.variant == variant]
                 .groupby("f").mean_state.median().abs())
        axes[0].plot(curve.index, curve.values, marker="o", ms=3,
                     **style.variant_kwargs(variant))
    axes[0].set_xlabel("sign fraction $f$")
    axes[0].set_ylabel(r"$|\overline{x}|$  at $\sigma$ = 6")
    axes[0].set_ylim(0, 1.05)
    style.legend(axes[0], loc="upper right", fontsize=style.LEGEND_SIZE - 1)

    axes[1].plot(matched.f, matched.median_abs_gap_matched_sigma, marker="o", ms=3,
                 color="#1f77b4", label="matched on nominal $\\sigma$")
    axes[1].plot(matched.f, matched.median_abs_gap_matched_x, marker="s", ms=3,
                 color="#c44e52", label=r"matched on $\sigma\cdot$bulk95")
    if len(matched):
        first = matched.iloc[0]
        absorbed = 1 - first.median_abs_gap_matched_x / first.median_abs_gap_matched_sigma
        axes[1].annotate(f"bulk95 absorbs {100 * absorbed:.0f}% at $f$ = 0",
                         xy=(first.f, first.median_abs_gap_matched_x),
                         xytext=(0.30, 0.78), textcoords="axes fraction",
                         fontsize=style.TICK_SIZE - 1, color=style.ANNOTATION_COLOUR,
                         arrowprops=dict(arrowstyle="->", lw=0.7))
    axes[1].set_xlabel("sign fraction $f$")
    axes[1].set_ylabel("median |connectome $-$ ER| MC gap")
    style.legend(axes[1], loc="upper right")
    for ax, letter in zip(axes, "ab"):
        style.panel_label(ax, letter)
    fig.tight_layout()
    return fig

"""Act III, prediction arm -- chapter 6, contributions 4 and 2.

F12 to F14 carry contribution 4 (generation is gated, not graded; `sigma_eff` is a
locator). F16 carries contribution 2 -- the unifying claim -- and is a cross-act figure:
it needs both arms, so **session 4 renders it** once session 3's memory arm is
validated.

Owned by session 4 (`report/act3b_prediction.md`).
"""

import numpy as np
import matplotlib.pyplot as plt

from report.figlib import style

CURVATURE_GAP = (0.6, 2.2)   # the empty band between the two curvature modes
COLLAPSE_BIT = 1.0           # sits in that empty band; not a tuned threshold


def f12_curvature_is_bimodal(ctx):
    """Generation is gated, not graded: the figure that licenses the switch framing."""
    frame = ctx.frame("jacobian")
    curvature = frame.mean_curvature.to_numpy(float)
    vpt = frame.vpt.to_numpy(float)
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.8))

    axes[0].hist(curvature, bins=np.linspace(0, np.pi, 160), color="0.35")
    axes[0].axvspan(*CURVATURE_GAP, color="#c44e52", alpha=0.12, lw=0)
    axes[0].set_yscale("log")
    axes[0].set_xlabel("mean curvature (rad)")
    axes[0].set_ylabel(f"cells  (n = {len(curvature):,})")
    between = ((curvature >= CURVATURE_GAP[0]) & (curvature <= CURVATURE_GAP[1])).sum()
    axes[0].annotate(f"{between} cells\n({100 * between / len(curvature):.2f}%)",
                     xy=(np.mean(CURVATURE_GAP), 0.55), xycoords=("data", "axes fraction"),
                     ha="center", fontsize=style.TICK_SIZE - 1, color="#c44e52")

    finite = np.isfinite(curvature) & np.isfinite(vpt)
    bit = (curvature[finite] > COLLAPSE_BIT).astype(float)
    r2_bit = np.corrcoef(bit, vpt[finite])[0, 1] ** 2
    r2_continuous = np.corrcoef(curvature[finite], vpt[finite])[0, 1] ** 2
    axes[1].scatter(curvature[finite], vpt[finite], s=1.2, alpha=0.08,
                    color="0.35", rasterized=True, linewidths=0)
    axes[1].set_xlabel("mean curvature (rad)")
    axes[1].set_ylabel("VPT (Lyapunov times)")
    axes[1].set_title(f"binary bit $R^2$ = {r2_bit:.3f}   "
                      f"continuous $R^2$ = {r2_continuous:.3f}",
                      fontsize=style.TITLE_SIZE - 1)
    for ax, letter in zip(axes, "ab"):
        style.panel_label(ax, letter)
    fig.tight_layout()
    return fig


def f13_generation_as_vpt(ctx):
    """Read as VPT the generative advantage is real, and it exists at f = 0 too."""
    frontier = ctx.frame("frontier")
    paired = ctx.frame("frontier_paired")
    loci = ctx.frame("collapse_loci")
    fig, axes = plt.subplots(1, 3, figsize=(8.0, 2.7),
                             gridspec_kw=dict(width_ratios=[1.15, 1.15, 0.9]))

    near_critical = frontier[(frontier.metric == "vpt")
                             & (np.isclose(frontier.spectral_radius, 2.0))]
    for variant in style.ordered_variants(near_critical.variant.unique()):
        curve = near_critical[near_critical.variant == variant].sort_values("f")
        axes[0].plot(curve.f, curve["median"], marker="o", ms=3,
                     **style.variant_kwargs(variant))
    axes[0].set_xlabel("sign fraction $f$")
    axes[0].set_ylabel(r"VPT (Lyapunov times), $\sigma$ = 2")
    style.legend(axes[0], loc="upper right", fontsize=style.LEGEND_SIZE - 2)

    contrasts = paired[(paired.metric == "vpt")
                       & (np.isclose(paired.spectral_radius, 2.0))]
    for null in [n for n in style.VARIANT_ORDER if n in set(contrasts.null)]:
        sub = contrasts[contrasts.null == null].sort_values("f")
        axes[1].plot(sub.f, sub.mean_diff, marker="o", ms=3,
                     color=style.VARIANT_COLOUR[null], label=style.VARIANT_LABEL[null])
        axes[1].fill_between(sub.f, sub.ci_lo, sub.ci_hi, alpha=0.15,
                             color=style.VARIANT_COLOUR[null], lw=0)
    axes[1].axhline(0, color=style.ANNOTATION_COLOUR, lw=0.9)
    axes[1].set_xlabel("sign fraction $f$")
    axes[1].set_ylabel("paired VPT advantage\n(connectome $-$ null)")
    style.legend(axes[1], loc="upper left", fontsize=style.LEGEND_SIZE - 2)

    at_zero = loci[np.isclose(loci.f, 0.0)]
    variants = [v for v in style.VARIANT_ORDER if v in set(at_zero.variant)]
    counts = [int(at_zero[at_zero.variant == v].n_seeds_collapsed.iloc[0]) for v in variants]
    totals = [int(at_zero[at_zero.variant == v].n_seeds.iloc[0]) for v in variants]
    axes[2].bar(np.arange(len(variants)), counts,
                color=[style.VARIANT_COLOUR[v] for v in variants],
                edgecolor="white", linewidth=0.5)
    for i, (count, total) in enumerate(zip(counts, totals)):
        axes[2].text(i, count + 0.15, f"{count}/{total}", ha="center",
                     fontsize=style.TICK_SIZE)
    axes[2].set_xticks(np.arange(len(variants)))
    axes[2].set_xticklabels([style.VARIANT_LABEL[v].replace(" · ", "\n") for v in variants],
                            fontsize=style.TICK_SIZE - 1)
    axes[2].set_ylabel("seeds collapsed to period-2")
    axes[2].set_title(r"$f$ = 0, $\sigma \leq$ 11.2", fontsize=style.TITLE_SIZE - 1)
    axes[2].grid(axis="x", visible=False)
    for ax, letter in zip(axes, "abc"):
        style.panel_label(ax, letter, dx=-0.12)
    fig.tight_layout()
    return fig


def f14_sigma_eff_is_a_locator(ctx):
    """A locator, not a criterion. No line is drawn at 1, because 1 is withdrawn."""
    invariance = ctx.frame("threshold_invariance")
    table = ctx.frame("threshold_table")
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.8),
                             gridspec_kw=dict(width_ratios=[1, 1.25]))

    scope = invariance[invariance.scope == "f > 0"].copy()
    short = {"nominal sigma": r"nominal $\sigma$",
             "sigma * bulk95  (linear negative-mode gain)": r"$\sigma\cdot$bulk95",
             "sigma_eff = bulk95 * sigma * <1-x^2>": r"$\sigma_{\rm eff}$"}
    scope["label"] = scope.criterion.map(lambda c: short.get(c, c))
    colours = ["#1f77b4", "#7f7f7f", "#c44e52"]
    axes[0].bar(np.arange(len(scope)), scope.cv, color=colours[:len(scope)],
                edgecolor="white", linewidth=0.5)
    for i, value in enumerate(scope.cv):
        axes[0].text(i, value + 0.012, f"{value:.3f}", ha="center", fontsize=style.TICK_SIZE)
    axes[0].set_xticks(np.arange(len(scope)))
    axes[0].set_xticklabels(scope.label, fontsize=style.TICK_SIZE)
    axes[0].set_ylabel("CV of the criterion's value\nat the transition  (lower = better)")
    axes[0].set_title(r"scope: $f > 0$,  n = " + f"{int(scope.n.iloc[0]) if len(scope) else 0}",
                      fontsize=style.TITLE_SIZE - 1)
    axes[0].grid(axis="x", visible=False)

    for variant in style.ordered_variants(table.variant.unique()):
        sub = table[table.variant == variant].sort_values("f")
        mid = (sub.effective_radius_lo + sub.effective_radius_hi) / 2
        axes[1].plot(sub.f, mid, marker="o", ms=3, **style.variant_kwargs(variant))
        axes[1].fill_between(sub.f, sub.effective_radius_lo, sub.effective_radius_hi,
                             alpha=0.13, color=style.VARIANT_COLOUR[variant], lw=0)
    axes[1].axhspan(0.77, 0.90, color="#c44e52", alpha=0.10, lw=0)
    axes[1].text(0.02, 0.835, "0.77 to 0.90", fontsize=style.TICK_SIZE - 1,
                 color="#c44e52", va="center")
    axes[1].set_xlabel("sign fraction $f$")
    axes[1].set_ylabel(r"$\sigma_{\rm eff}$ at the transition")
    style.legend(axes[1], loc="lower right", fontsize=style.LEGEND_SIZE - 2)
    for ax, letter in zip(axes, "ab"):
        style.panel_label(ax, letter, dx=-0.12)
    fig.tight_layout()
    return fig


def _first_crossing(memory, generative, limit):
    """First x below ``limit`` where the two boundaries swap order, or None.

    Computed from the data rather than hard-coded, so the figure follows if a number
    moves. Gaps (NaN ``f_star``) are dropped before interpolation, never bridged.
    """
    memory = memory.dropna(subset=["f_star"]).sort_values("x")
    generative = generative.dropna(subset=["f_star"]).sort_values("x")
    if memory.empty or generative.empty:
        return None
    grid = np.union1d(memory.x.to_numpy(), generative.x.to_numpy())
    grid = grid[grid <= limit]
    if grid.size < 2:
        return None
    upper = np.interp(grid, memory.x, memory.f_star)
    lower = np.interp(grid, generative.x, generative.f_star)
    sign = np.sign(upper - lower)
    for i in range(1, len(grid)):
        if sign[i - 1] * sign[i] < 0:
            return grid[i], (upper[i] + lower[i]) / 2
    return None


def f16_phase_boundaries(ctx):
    """The crossing, with its axis and its coverage. Contribution 2's own figure.

    The memory and generative boundaries on both matching axes. On the matched-bulk
    axis they cross inside full coverage; on the nominal axis they do not cross at all
    once the sweep passes sigma = 6. Everything past the all-replicates coverage edge
    is drawn hatched, because the boundary there rests on a bulk95-selected subsample
    and crosses repeatedly (TIER0 §6.10) -- that region is the reason the published
    crossing has to be identified as the first one inside coverage, not just "a"
    crossing.
    """
    boundaries = ctx.frame("boundaries")
    coverage = ctx.frame("coverage")
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.0))

    for ax, axis in zip(axes, ("effective", "nominal")):
        sub = boundaries[boundaries.axis == axis]
        x_max = float(sub.x.max())
        for panel in ("dD", "dStraight"):
            curve = sub[sub.panel == panel].sort_values("x")
            ax.plot(curve.x, curve.f_star, color=style.BOUNDARY_COLOUR[panel],
                    lw=1.6, label=style.BOUNDARY_LABEL[panel])

        limit = x_max
        if axis == "effective":
            # Coverage edge is f-dependent; shade to the right of x_hi(f). The nominal
            # axis needs no mask -- every nominal cell carries all 30 replicates.
            edge = coverage.sort_values("f")
            ax.fill_betweenx(edge.f, edge.x_hi, x_max, color=style.UNCOVERED_COLOUR,
                             alpha=0.28, lw=0, hatch="///", edgecolor="white", zorder=0)
            limit = float(edge.x_hi.min())
            ax.axvline(limit, color=style.UNCOVERED_COLOUR, lw=0.9, ls="--")
            ax.text(limit, 0.985, " not all 30 replicates ",
                    transform=ax.get_xaxis_transform(), fontsize=style.TICK_SIZE - 1,
                    va="top", ha="left", color="0.35")
        else:
            ax.axvline(6.0, color=style.ANNOTATION_COLOUR, lw=0.9, ls=":")
            ax.text(6.0, 0.985, " old sweep limit ", transform=ax.get_xaxis_transform(),
                    fontsize=style.TICK_SIZE - 1, va="top", ha="left",
                    color=style.ANNOTATION_COLOUR)

        crossing = _first_crossing(sub[sub.panel == "dD"], sub[sub.panel == "dStraight"],
                                   limit)
        if crossing is not None:
            ax.plot([crossing[0]], [crossing[1]], marker="o", ms=6, mfc="none",
                    mec="black", mew=1.4, zorder=6)
            ax.annotate(f"({crossing[0]:.3f}, {crossing[1]:.3f})", xy=crossing,
                        xytext=(6, 10), textcoords="offset points",
                        fontsize=style.TICK_SIZE, color=style.ANNOTATION_COLOUR)
        else:
            ax.text(0.5, 0.06, "no crossing", transform=ax.transAxes, ha="center",
                    fontsize=style.TICK_SIZE, color=style.ANNOTATION_COLOUR,
                    style="italic")

        ax.set_xlabel(style.AXIS_LABEL[axis])
        ax.set_xlim(0, x_max)
        ax.set_ylim(0, 0.5)
    axes[0].set_ylabel("sign fraction $f$")
    style.legend(axes[0], loc="upper left")
    for ax, letter in zip(axes, "ab"):
        style.panel_label(ax, letter, dx=-0.10)
    fig.tight_layout()
    return fig

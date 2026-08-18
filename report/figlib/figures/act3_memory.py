"""Act III, memory arm -- chapter 6, contribution 3.

The crossing, the supercritical margin across a 2.2x change in N, peak parity, and the
rescue from Perron domination.

Owned by session 3 (`report/act3a_memory.md`).

**The one aggregation rule this whole act turns on: per seed, then across seeds.**
`bulk95` is a per-seed quantity for the three resampling nulls -- an extreme-value
statistic, with a 0.41 to 0.61 spread across ten degree-rewire seeds -- so on the matched
axis `x = sigma * bulk95` every seed sits on its own grid. E0.2 therefore reindexes each
seed's curve onto a common grid and aggregates afterwards (`E02_verdict` sec 4.4), and
`TIER0` sec 1.2's crossing table is that statistic. Medianing `d_eff` at fixed nominal
sigma and calling `sigma * median(bulk95)` the x coordinate collapses ten different x
values into one; it moves the published peak locations by up to 0.15 on x and the
retained fractions by a point. `_matched_axis_curves` is the correct rule, in one place.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from report.figlib import style
from report.figlib.figures.common import N_NODES

OVERLAP_TOP = 2.599          # top of the four-variant overlap on the matched axis
N_GRID = 121                 # E0.2's common grid, reused so the numbers are its numbers

# TIER0 sec 1.2's crossing table, as published. The builder asserts against it, so a
# figure that stops reproducing the table it is captioned with fails the build.
PUBLISHED_CROSSING = {
    "connectome": (432.4, 204.9),
    "connectome_weight_permuted": (445.7, 126.8),
    "degree_rewire": (444.7, 96.4),
    "erdos_renyi": (446.6, 49.5),
}

# TIER0 sec 2.4. Both filters are published and the result depends on which is used, so
# F9 draws both rather than picking one.
SR_CRIT = {448: {"connectome": 3.078, "connectome_weight_permuted": 1.922,
                 "degree_rewire": 1.873, "erdos_renyi": 1.807},
           1000: {"connectome": 3.985, "connectome_weight_permuted": 2.395,
                  "degree_rewire": 2.301, "erdos_renyi": 2.438}}


def _matched_axis_curves(frame):
    """Per-seed `d_eff` curves on the matched-bulk axis, then the median across seeds.

    Returns ``(grid, curves)``. The grid runs over the interval every (variant, seed)
    covers, so nothing is extrapolated -- the same clip E0.2 applies, which is what puts
    the top of the overlap at 2.599 rather than at the connectome's own reach.
    """
    span = frame.groupby(["variant", "seed"]).x.agg(["min", "max"])
    grid = np.linspace(float(span["min"].max()), float(span["max"].min()), N_GRID)
    curves = {}
    for variant in style.ordered_variants(frame.variant.unique()):
        stack = [np.interp(grid, seed.sort_values("x").x.to_numpy(float),
                           seed.sort_values("x").d_eff.to_numpy(float))
                 for _, seed in frame[frame.variant == variant].groupby("seed")]
        curves[variant] = np.median(np.vstack(stack), axis=0)
    return grid, curves


def f7_the_crossing(ctx):
    """The crossing: the connectome peaks lowest and retains most.

    **The figure is the crossing, not the peak.** Read as a capacity result the panel
    says the connectome is the worst substrate here, and at N = 448 that reading is not
    even resolvable -- every variant peaks within 3.5% of the hard `d_eff = N` ceiling
    (b), which is why `TIER0` sec 1.2 calls peak capacity unresolvable at this size. What
    is resolvable is the decay: at the top of the four-variant overlap the connectome
    still holds 47% of its own peak against 28 / 22 / 11% (c), a four-fold spread that no
    ceiling can manufacture. A ceiling can clip curves; it cannot invert an ordering.

    (b) is a dot plot and (c) a bar chart, deliberately. (b)'s axis does not start at
    zero -- it cannot, since the whole content is the last 5% below the ceiling -- and
    bars on a cropped baseline would read as a large difference. Dots carry no area, so
    the crop is honest. (c) is zero-based and therefore drawn as bars.
    """
    frame = ctx.frame("taskb")
    grid, curves = _matched_axis_curves(frame)
    peak = {v: float(c.max()) for v, c in curves.items()}
    at_top = {v: float(c[-1]) for v, c in curves.items()}
    retained = {v: at_top[v] / peak[v] for v in curves}
    variants = list(curves)

    # The claim, asserted rather than trusted: lowest peak, highest retention, and the
    # published table reproduced. Content assertions are skipped on placeholder data.
    if not ctx.placeholder:
        assert min(peak, key=peak.get) == "connectome", (
            f"F7: the connectome no longer peaks lowest ({peak}). That is the first half "
            "of the crossing; if it has moved, TIER0 sec 1.2 has moved with it.")
        assert max(retained, key=retained.get) == "connectome", (
            f"F7: the connectome no longer retains most ({retained}).")
        for variant, (published_peak, published_top) in PUBLISHED_CROSSING.items():
            assert abs(peak[variant] - published_peak) < 0.1, (
                f"F7: {variant} peak {peak[variant]:.2f} against TIER0's {published_peak}")
            assert abs(at_top[variant] - published_top) < 0.1, (
                f"F7: {variant} at overlap top {at_top[variant]:.2f} against "
                f"TIER0's {published_top}")

    fig, axes = plt.subplots(1, 3, figsize=(7.8, 3.2),
                             gridspec_kw=dict(width_ratios=[1.95, 0.95, 0.95]))

    # -- (a) the decay on the matched axis ------------------------------------------
    for variant in variants:
        axes[0].plot(grid, curves[variant],
                     **style.variant_kwargs(variant,
                                            label=style.VARIANT_TITLE[variant]))
        peak_at = grid[curves[variant].argmax()]
        axes[0].plot([peak_at], [peak[variant]], marker="o", ms=3.5,
                     color=style.VARIANT_COLOUR[variant], zorder=6)
    # Ceiling label on the left: the top-of-overlap rule stands at the right-hand edge
    # (unlabelled, named in the caption), and at the default placement that rule is
    # drawn straight through the label.
    style.draw_ceiling(axes[0], N_NODES, side="left")
    axes[0].axvline(grid[-1], color=style.ANNOTATION_COLOUR, lw=0.8, ls="--", zorder=1)
    axes[0].set_xlim(0, grid[-1] * 1.02)
    axes[0].set_ylim(0, 1.10 * N_NODES)
    axes[0].set_xlabel(style.AXIS_LABEL["effective"], fontsize=style.AXIS_LABEL_SIZE - 1)
    axes[0].set_ylabel(r"$d_{\rm eff}$  (ridge effective rank)")

    # -- (b) the peaks, against the ceiling that makes them unreadable ---------------
    positions = np.arange(len(variants))
    axes[1].axhline(1.0, color=style.CEILING_COLOUR, lw=0.9, ls=":", zorder=1)
    axes[1].text(0.02, 1.0, r"$d_{\rm eff} = N$", transform=axes[1].get_yaxis_transform(),
                 ha="left", va="bottom", fontsize=style.TICK_SIZE - 1,
                 color=style.CEILING_COLOUR)
    for position, variant in zip(positions, variants):
        height = peak[variant] / N_NODES
        axes[1].plot([position], [height], marker="o", ms=6,
                     color=style.VARIANT_COLOUR[variant], zorder=4)
        axes[1].vlines(position, 0.950, height, lw=0.8,
                       color=style.VARIANT_COLOUR[variant], alpha=0.45, zorder=3)
    axes[1].set_ylim(0.950, 1.013)
    axes[1].set_ylabel("peak $d_{\\rm eff}\\,/\\,N$")

    # -- (c) the retention, which is the resolvable half -----------------------------
    axes[2].bar(positions, [100 * retained[v] for v in variants],
                color=[style.VARIANT_COLOUR[v] for v in variants],
                edgecolor="white", linewidth=0.5)
    for position, variant in zip(positions, variants):
        axes[2].text(position, 100 * retained[variant] + 1.2,
                     f"{100 * retained[variant]:.0f}%", ha="center",
                     fontsize=style.TICK_SIZE - 1)
    axes[2].set_ylim(0, 56)
    axes[2].set_ylabel("% of own peak retained\nat the top of the overlap")

    for ax in axes[1:]:
        ax.set_xticks(positions)
        ax.set_xticklabels([style.VARIANT_TITLE[v] for v in variants],
                           fontsize=style.TICK_SIZE - 1, rotation=30, ha="right",
                           rotation_mode="anchor")
        ax.grid(axis="x", visible=False)
    for ax, letter in zip(axes, "abc"):
        style.panel_label(ax, letter, dx=-0.12)
    # One figure-level legend under all three panels. In (a) there is nowhere inside the
    # axes a four-entry box fits: the curves rise through the lower left, run along the
    # ceiling across the top, and the nulls' tails occupy the lower right, so every
    # in-panel placement measured put a label on a curve. (b) and (c) name the same four
    # substrates on their x axes, so one legend serves the figure. F5's treatment.
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4,
               fontsize=style.LEGEND_SIZE - 1, bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.075, 1, 1))
    return fig


def f9_scale_invariance(ctx):
    """The supercritical margin across a 2.2x change in N -- under **both** filters.

    `TIER0` sec 2.4 publishes two supercritical MC tables and says to report both,
    because the answer depends on which one is used: with the threshold set at the
    connectome's `sr_crit` for every variant the margin is flat (4.40 -> 4.42), and with
    each variant's own it grows (3.56 -> 3.85). Drawing one panel would make a filter
    choice look like a property of the data, which is the same failure the two-axis
    discipline of sec 1.1 exists to prevent, one axis over.

    Neither reading is a null result and the claim survives both, which is the point.
    """
    frame = ctx.frame("n1000")
    variants = style.ordered_variants(frame.variant.unique())
    positions = np.arange(len(variants))
    fig, axes = plt.subplots(1, 3, figsize=(8.0, 2.9),
                             gridspec_kw=dict(width_ratios=[1.5, 1.0, 1.0]))

    # -- (a) where the two thresholds cut ---------------------------------------------
    for scale, dash in ((448, "-"), (1000, "--")):
        for variant in ("connectome", "erdos_renyi"):
            curve = (frame[(frame.variant == variant) & (frame.n_nodes == scale)]
                     .groupby("spectral_radius").mc.median())
            axes[0].plot(curve.index, curve.values, ls=dash,
                         color=style.VARIANT_COLOUR[variant],
                         lw=style.VARIANT_LINEWIDTH[variant])
        # Rules unlabelled: the two sit 0.9 sigma apart, so a label on each -- rotated
        # or not -- lands on the other's line or on a curve. The caption names them.
        axes[0].axvline(SR_CRIT[scale]["connectome"], color=style.ANNOTATION_COLOUR,
                        lw=0.8, ls=":", zorder=1)
    axes[0].set_xlabel(style.AXIS_LABEL["nominal"], fontsize=style.AXIS_LABEL_SIZE - 1)
    axes[0].set_ylabel("MC  (median over seeds)")
    # Headroom bought on purpose: every curve peaks below 16, so lifting the limit to 21
    # opens a strip across the top that no curve enters and the four-entry legend has
    # somewhere to sit. Inside the data region there is no such place -- the connectome's
    # N=1000 curve runs at 11 to 15.5 across the whole supercritical half of the panel.
    axes[0].set_ylim(bottom=0)
    # Substrate in one column, scale in the other, rather than four "name, N = x"
    # entries: with the real substrate names a crossed legend is nearly twice as wide as
    # the panel. Column-major fill puts the two substrates left and the two scales right.
    # Placed **below the axes**, under the x label: inside them the only gap wide enough
    # was a strip across the top that had to be bought with 3 units of empty y, which
    # cost the curves a fifth of the panel. It is anchored to (a) rather than to the
    # figure -- unlike F7's and F10's -- because it names two of the four substrates and
    # a dash encoding that (b) and (c) do not use; a figure-wide legend would read as
    # applying to all three panels.
    scale_handles = [Line2D([], [], color=style.VARIANT_COLOUR[v], lw=1.7)
                     for v in ("connectome", "erdos_renyi")]
    scale_handles += [Line2D([], [], color="0.35", ls=d, lw=1.4) for d in ("-", "--")]
    axes[0].legend(scale_handles,
                   [style.VARIANT_TITLE["connectome"], style.VARIANT_TITLE["erdos_renyi"],
                    "N = 448", "N = 1000"],
                   loc="upper center", bbox_to_anchor=(0.5, -0.30), borderaxespad=0.0,
                   ncol=2, fontsize=style.LEGEND_SIZE - 2,
                   columnspacing=1.2, handlelength=1.8)

    # -- (b, c) the same margin under the two published thresholds --------------------
    panels = ((1, r"$\sigma \geq$ the connectome's $sr_{\rm crit}$",
               lambda scale, variant: SR_CRIT[scale]["connectome"]),
              (2, r"$\sigma \geq$ each variant's own $sr_{\rm crit}$",
               lambda scale, variant: SR_CRIT[scale][variant]))
    width = 0.36
    for index, title, threshold_of in panels:
        ax, margins = axes[index], {}
        for offset, scale, alpha in ((-width / 2, 448, 1.0), (width / 2, 1000, 0.45)):
            values = [frame[(frame.variant == v) & (frame.n_nodes == scale)
                            & (frame.spectral_radius >= threshold_of(scale, v))].mc.median()
                      for v in variants]
            ax.bar(positions + offset, values, width, alpha=alpha,
                   color=[style.VARIANT_COLOUR[v] for v in variants],
                   edgecolor="white", linewidth=0.5,
                   label=f"N = {scale}" if index == 1 else None)
            lookup = dict(zip(variants, values))
            margins[scale] = lookup["connectome"] / lookup["erdos_renyi"]
        # The margins left the panels for the caption, so they are asserted instead of
        # drawn: a caption number with nothing on the figure checking it is a number that
        # can go stale silently.
        if not ctx.placeholder:
            published = {1: {448: 4.40, 1000: 4.42}, 2: {448: 3.56, 1000: 3.85}}[index]
            for scale, value in margins.items():
                assert abs(value - published[scale]) < 0.005, (
                    f"F9 panel {'bc'[index - 1]}: connectome/ER margin at N={scale} is "
                    f"{value:.4f}, against TIER0 sec 2.4's {published[scale]}")
        ax.set_xticks(positions)
        ax.set_xticklabels([style.VARIANT_TITLE[v] for v in variants],
                           fontsize=style.TICK_SIZE - 1, rotation=30, ha="right",
                           rotation_mode="anchor")
        ax.grid(axis="x", visible=False)
        ax.set_title(title, fontsize=style.TITLE_SIZE - 1)
        ax.set_ylabel("supercritical MC (median)" if index == 1 else None)
        # Enough headroom for the scale legend to clear the connectome bars, which reach
        # 13.93 of the 14-unit range the axes would otherwise set themselves.
        ax.set_ylim(0, 16.5)
    axes[2].sharey(axes[1])
    axes[2].tick_params(labelleft=False)
    # The solid/faded pair is the scale, and it is the same pair in both panels, so one
    # legend serves; it goes on (b) because (c) shares (b)'s axis. Placed under the
    # margin text rather than upper-left, where the connectome bars reach the top.
    handles = [plt.Rectangle((0, 0), 1, 1, fc="0.35", alpha=a) for a in (1.0, 0.45)]
    axes[1].legend(handles, ["N = 448", "N = 1000"], loc="upper right",
                   fontsize=style.LEGEND_SIZE - 2)
    # Offsets in points, not axes fractions, and one per panel: (a) and (b) each have to
    # clear a long rotated y label plus its tick labels, (c) has neither, and (a) is half
    # again as wide as the others -- so a shared fraction puts the three letters at three
    # different distances from what they have to clear. Equal panel heights keep them in
    # line vertically.
    for ax, letter, dx_points in zip(axes, "abc", (-44, -44, -14)):
        style.panel_label(ax, letter, offset_points=(dx_points, 2))
    fig.tight_layout()
    return fig


def f10_peak_parity(ctx):
    """Parity at the peak, with the CIs that forbid writing "always worst".

    The figure exists to stop a sentence being written. Point estimates alone say the
    connectome's peak MC is below every null at every alpha, which reads as "always
    worst"; the intervals say the effect is 2 to 6% and that against degree-matching it
    excludes zero at **one** alpha of five. So the defensible wording is parity at the
    peak (`TIER0` sec 3.4), and the figure has to carry the uncertainty for that wording
    to be readable off it rather than taken on trust.

    (b) is the same statistic as a percentage of the null it is measured against, because
    "2 to 6%" is the form the claim is written in and a reader should not have to divide
    by a peak that is not on the page.

    **Reliability is drawn on the marker, not written in a corner.** A filled marker is a
    CI that excludes zero and an open one a CI that does not, so the four open blue
    markers *are* the "1 of 5 against degree-matching" clause. A text box saying so had
    to sit somewhere, and every placement measured landed on an interval -- the panels
    are intervals nearly edge to edge.
    """
    frame = ctx.frame("peak_parity").copy()
    frame["null"] = frame.contrast.str.replace("connectome - ", "", regex=False)
    # pct_of_null is 100 * mean_diff / (the null's own peak MC), so the same linear
    # factor carries the interval across. The null's peak is not in this file; the ratio
    # recovers it without needing a second source.
    frame["scale"] = frame.pct_of_null / frame.mean_diff
    alphas = sorted(frame.alpha.unique())
    nulls = [n for n in style.VARIANT_ORDER if n in set(frame.null)]

    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0), sharey=True)
    offsets = np.linspace(-0.26, 0.26, len(nulls))
    for index, (column, lo, hi) in enumerate(
            (("mean_diff", "ci_lo", "ci_hi"), ("pct_of_null", "ci_lo", "ci_hi"))):
        ax = axes[index]
        if index == 1:
            ax.axvspan(-6, -2, color=style.SUPERCRITICAL_COLOUR, zorder=0)
            ax.text(-4, -0.62, "2 to 6%", ha="center", va="center",
                    fontsize=style.TICK_SIZE - 1, color=style.ANNOTATION_COLOUR)
        for offset, null in zip(offsets, nulls):
            sub = frame[frame.null == null].set_index("alpha").reindex(alphas)
            factor = sub.scale if index == 1 else 1.0
            centre, low, high = sub[column], sub[lo] * factor, sub[hi] * factor
            rows = np.arange(len(alphas)) + offset
            ax.errorbar(centre, rows, xerr=[centre - low, high - centre],
                        fmt="none", lw=1.2, capsize=2.5,
                        color=style.VARIANT_COLOUR[null])
            reliable = sub.ci_excludes_zero.to_numpy(bool)
            ax.scatter(centre[reliable], rows[reliable], s=22, zorder=4,
                       color=style.VARIANT_COLOUR[null],
                       label=style.VARIANT_TITLE[null])
            ax.scatter(centre[~reliable], rows[~reliable], s=22, zorder=4,
                       facecolor="white", linewidths=1.1,
                       edgecolor=style.VARIANT_COLOUR[null])
        ax.axvline(0, color=style.ANNOTATION_COLOUR, lw=0.9)
        ax.grid(axis="y", visible=False)
    axes[0].set_yticks(np.arange(len(alphas)))
    axes[0].set_yticklabels([f"$\\alpha$ = {a:g}" for a in alphas])
    axes[0].invert_yaxis()
    axes[0].set_xlabel("paired peak MC difference\n(connectome $-$ null)")
    axes[1].set_xlabel("the same, as % of the null's own peak\n"
                       "(open marker: 95% CI includes zero)")
    for ax, letter in zip(axes, "ab"):
        style.panel_label(ax, letter, dx=-0.06)
    # Figure-level legend, for F7's reason: both panels are intervals nearly edge to
    # edge, and every in-axes placement measured sat on one.
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3,
               fontsize=style.LEGEND_SIZE - 1, bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.075, 1, 1))
    return fig


def f11_perron_rescue(ctx):
    """The advantage is resistance to Perron domination, and `bulk95` only partly explains it.

    **`|.|` comes before the median and the builder asserts it.** `mean_state` is signed
    with a sign set by the input realisation, so a median taken first cancels seeds
    against each other: at sigma = 6, `f` = 0 it reports 0.638 for the connectome and
    0.575 for the weight-permuted null, putting the null *below* the connectome and
    arguing against this figure's own caption. Act II caught the identical defect in F4b
    (`report/act2_manifold.md` audit item 1); the assertion below is why it cannot come
    back here.

    Panel (b) is the controlled half of `TIER0` sec 3.7 and the only half that
    adjudicates. The correlation half is confounded -- `|mean_state|` and
    `sigma * bulk95` are collinear by construction -- and sec 3.7 says in terms that its
    pooled contrast must not be quoted. It is not plotted.
    """
    extension = ctx.frame("f_extension")
    matched = ctx.frame("mechanism_matched")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9))

    memory = extension[(extension.task == "mc")
                       & (np.isclose(extension.spectral_radius, 6.0))]
    curves = {}
    for variant in style.ordered_variants(memory.variant.unique()):
        curve = (memory[memory.variant == variant]
                 .assign(abs_mean_state=lambda d: d.mean_state.abs())
                 .groupby("f").abs_mean_state.median())
        curves[variant] = curve
        axes[0].plot(curve.index, curve.values, marker="o", ms=3,
                     **style.variant_kwargs(variant,
                                            label=style.VARIANT_TITLE[variant]))
    if not ctx.placeholder:
        at_zero = {v: float(c.loc[0.0]) for v, c in curves.items()}
        assert min(at_zero, key=at_zero.get) == "connectome", (
            f"F11a: the connectome is not the least common-mode dominated substrate at "
            f"f = 0 ({at_zero}). Under median-then-abs it is not -- see the docstring; "
            "check the aggregation before believing the data moved.")
    axes[0].set_xlabel("sign fraction $f$")
    axes[0].set_ylabel("common-mode amplitude")
    axes[0].set_ylim(0, 1.05)
    axes[0].set_title(r"at $\sigma$ = 6 (supercritical)", fontsize=style.TITLE_SIZE - 1)
    style.legend(axes[0], loc="upper right", fontsize=style.LEGEND_SIZE - 1)

    axis_label = {"nominal": r"matched on nominal $\sigma$",
                  "effective": r"matched on $\sigma\cdot$bulk95"}
    for axis, column, marker in (("nominal", "median_abs_gap_matched_sigma", "o"),
                                 ("effective", "median_abs_gap_matched_x", "s")):
        axes[1].plot(matched.f, matched[column], marker=marker, ms=3, lw=1.5,
                     color=style.AXIS_COLOUR[axis], label=axis_label[axis])
    # The 26% moved to the caption with the annotation that carried it, so it is
    # asserted instead of drawn -- F9's reasoning: a caption number with nothing on the
    # figure checking it can go stale silently.
    if not ctx.placeholder:
        first = matched.iloc[0]
        absorbed = 1 - first.median_abs_gap_matched_x / first.median_abs_gap_matched_sigma
        assert abs(100 * absorbed - 26) < 0.5, (
            f"F11b: matching on sigma*bulk95 absorbs {100 * absorbed:.1f}% of the f = 0 "
            "gap, against TIER0 sec 3.7's 26%")
    axes[1].set_xlabel("sign fraction $f$")
    axes[1].set_ylabel("$\\Delta$MC:  |Connectome $-$ Erdős–Rényi|")
    axes[1].set_ylim(0, None)
    style.legend(axes[1], loc="upper right")
    # Both panels carry a long rotated y label, so the panel letters are placed a fixed
    # distance from the axes corner in points rather than in axes fractions: at the
    # default dx the 'b' landed on top of its own y label.
    for ax, letter in zip(axes, "ab"):
        style.panel_label(ax, letter, offset_points=(-40, 2))
    fig.tight_layout()
    return fig

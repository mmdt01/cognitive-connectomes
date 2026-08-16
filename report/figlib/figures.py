"""One builder per entry on ``report/FIGURE_LIST.md``. No figure exists outside this file.

Each builder takes a ``sources.Context`` and returns a matplotlib figure. It reads named
frames, never paths, and applies no filter of its own: the filter lives on the source, so
the claim, the filter and the figure stay together. Builders must work unchanged against
placeholder frames, which is what the smoke entry point checks.

Figure IDs match ``FIGURE_LIST.md``. **F8 is retired** (merged into F3, the two-axis
methods figure); the ID is left unused rather than renumbering, so every reference
elsewhere still resolves.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

from report.figlib import style

N_NODES = 448
OVERLAP_TOP = 2.599          # top of the four-variant overlap on the matched axis
CURVATURE_GAP = (0.6, 2.2)   # the empty band between the two curvature modes
COLLAPSE_BIT = 1.0           # sits in that empty band; not a tuned threshold


# =============================================================================
# Chapter 4 -- Act I: structure sets the spectrum
# =============================================================================
def f1_spectrum(ctx):
    """F1 at the primary parcellation, N = 448."""
    return _spectrum_figure(ctx, "spectra_448")


def s1_spectrum_n1000(ctx):
    """S1 -- F1 rebuilt at N = 1000, the scale replicate for the appendix.

    Same builder, same frozen artifact family, different parcellation. Nothing here is
    a second implementation: if the figure changes, both scales change with it.
    """
    return _spectrum_figure(ctx, "spectra_1000")


def _spectrum_figure(ctx, source_name):
    """The spectral gap: four substrates stacked in raw units, then the normalised view.

    Parameterised by source so F1 (N = 448) and S1 (N = 1000) are one builder. Every
    axis limit, bin width and tick set below is derived from the data rather than
    written for one parcellation -- at N = 1000 the spectrum runs to +/-0.266 rather
    than +/-0.215 and carries 1000 eigenvalues rather than 448, and the earlier
    hard-coded x ticks and decade ticks happened to survive that only by luck.

    Layout descends from the committed E0.4 Figure 1 (small multiples, an ECDF, a
    per-seed strip) with every axis re-pointed. That figure was titled "Connectome
    weight placement compresses the eigenvalue bulk" and drew all six panels in units of
    ``|lambda_1|``, which is what makes the connectome's band look narrow: each substrate
    is divided by its own Perron root, and the Perron root is the only thing that differs.

    Here (a-d) are **stacked vertically on one shared raw-units axis**, so the four bulk
    bands sit at literally the same page coordinate and the gap out to ``lambda_1`` is
    the part that visibly grows. That stacking is what carries the claim, and it is why
    the raw ECDF the earlier draft used as panel (e) is no longer needed -- it was making
    the same point less directly. Panel (e) is therefore the **normalised** ECDF, which
    does a job nothing else in the figure does: it shows the substrates in the units the
    rest of the thesis matches on, and lets ``bulk95`` be read off the axis at the
    95th-percentile crossing. Panels a-d and panel e are the same spectra one division
    apart, and the caption has to say so.

    Panels a-d draw ONE seed per null -- the seed whose ``bulk95`` is nearest the median
    -- so all four show 448 eigenvalues and the shapes are compared at equal sampling
    noise. The connectome is a single fixed graph. Panels e and f use all 10 seeds.
    """
    frame = ctx.frame(source_name)
    variants = style.ordered_variants(frame.variant.unique())

    fig = plt.figure(figsize=(7.6, 5.8))
    # Left column wider than the right, so four stacked panels stay landscape rather
    # than turning the figure portrait. hspace carries the row titles: they sit in the
    # white space between panels rather than inside them.
    outer = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.25], wspace=0.34)
    left_grid = outer[0].subgridspec(len(variants), 1, hspace=0.45)
    right_grid = outer[1].subgridspec(2, 1, hspace=0.42)
    stack = [fig.add_subplot(left_grid[i, 0]) for i in range(len(variants))]
    for ax in stack[1:]:
        ax.sharex(stack[0])
        ax.sharey(stack[0])
    ax_ecdf = fig.add_subplot(right_grid[0, 0])
    ax_strip = fig.add_subplot(right_grid[1, 0])

    # -- per-variant medians, the aggregation TIER0 §3.1's table uses ----------------
    stat = {}
    for variant in variants:
        sub = frame[frame.variant == variant]
        bulk95 = float(sub.bulk95.median())
        lam1 = float(sub.lambda_max_raw.median())
        stat[variant] = dict(bulk95=bulk95, lam1=lam1, abs_bulk=bulk95 * lam1,
                             gap_ratio=1.0 / bulk95)

    limit = 1.14 * max(s["lam1"] for s in stat.values())

    # Representative seed per row: bulk95 nearest the median. A stated rule, not a pick.
    #
    # Scaled by the MEDIAN |lambda_1|, not by that seed's own. `eig_w_real` is stored
    # normalised (max |lambda| = 1), so the largest bar then lands exactly on the
    # lambda_1 rule -- which is what lambda_1 means. Using the seed's own scale instead
    # puts the two on different aggregations: the seed is chosen for bulk95, which says
    # nothing about its lambda_1, and the mismatch was visible (the ER row's largest
    # eigenvalue overshot the rule by 0.0063, the degree row's fell 0.0076 short). It
    # also strips the seed-to-seed lambda_1 jitter that F3 measures at 6 to 9% relative
    # s.d., which has no business moving a panel whose every drawn number is a median.
    spectra = {}
    for variant in variants:
        sub = frame[frame.variant == variant]
        pick = sub.loc[(sub.bulk95 - sub.bulk95.median()).abs().idxmin()]
        spectra[variant] = np.asarray(pick.eig_w_real, float) * stat[variant]["lam1"]
        assert np.isclose(np.abs(spectra[variant]).max(), stat[variant]["lam1"]), (
            f"{variant}: the drawn spectrum's largest |lambda| must sit exactly on the "
            "lambda_1 rule; eig_w_real is expected to be stored normalised.")

    # Each row is binned over exactly [-lambda_1, +lambda_1] rather than over one shared
    # grid. lambda_1 IS the largest modulus, so that interval contains every eigenvalue
    # by definition and the histogram's support is exactly the shaded region -- no bar
    # can extend past the lambda_1 rule. On a shared grid the bar *containing* the
    # extreme eigenvalue spans a whole bin whose outer edge falls wherever the grid
    # happens to put it: the weight-permuted and degree rows overhung by 91% and 93% of
    # a bin width, and the ER row overhung on the negative side too. The eigenvalues were
    # in the right places; their bars were not.
    #
    # Bin COUNT varies per row so the bin WIDTH stays near-constant (within ~0.3%), which
    # keeps bar widths comparable down the column and the densities on the same footing.
    target_bin_width = 2.0 * limit / 120.0
    row_bins = {}
    for variant in variants:
        lam1 = stat[variant]["lam1"]
        n_bins = max(1, int(round(2.0 * lam1 / target_bin_width)))
        edges = np.linspace(-lam1, lam1, n_bins + 1)
        counts, _ = np.histogram(spectra[variant], bins=edges)
        assert counts.sum() == spectra[variant].size, (
            f"{variant}: {spectra[variant].size - counts.sum()} eigenvalue(s) fell "
            "outside [-lambda_1, lambda_1], so a bar would be drawn outside the shaded "
            "gap. lambda_1 is the largest modulus; this cannot happen unless the "
            "spectrum and the median used to scale it have come apart.")
        row_bins[variant] = edges

    # The shared density axis, derived rather than guessed. `density=True` integrates to
    # 1 over the bins, so a bin holding exactly one of the N eigenvalues sits at
    # 1/(N * bin width) -- put the floor just under the smallest such value and single
    # eigenvalues out in the gap stay visible as bars rather than clipped into the spine.
    n_eigenvalues = len(next(iter(spectra.values())))
    single_count_density = min(
        1.0 / (n_eigenvalues * float(edges[1] - edges[0])) for edges in row_bins.values())
    peak_density = max(
        float(np.histogram(spectra[v], bins=row_bins[v], density=True)[0].max())
        for v in variants)

    # -- (a-d) one substrate per row, raw units, one shared x-axis -------------------
    for ax, variant in zip(stack, variants):
        spectrum = spectra[variant]
        colour = style.VARIANT_COLOUR[variant]
        abs_bulk, lam1 = stat[variant]["abs_bulk"], stat[variant]["lam1"]

        # The gap first, so the bulk band and the histogram draw over it.
        ax.axvspan(abs_bulk, lam1, color=style.ANNOTATION_COLOUR, alpha=0.10, lw=0)
        ax.axvspan(-lam1, -abs_bulk, color=style.ANNOTATION_COLOUR, alpha=0.10, lw=0)
        ax.axvspan(-abs_bulk, abs_bulk, color=colour, alpha=0.16, lw=0)
        ax.hist(spectrum, bins=row_bins[variant], density=True, color=colour, lw=0)
        for edge in (-abs_bulk, abs_bulk):
            ax.axvline(edge, color=colour, lw=0.9, ls="--")
        for root in (-lam1, lam1):
            ax.axvline(root, color=colour, lw=1.1, ls=":")
        ax.set_yscale("log")
        y_lo, y_hi = 0.5 * single_count_density, 2.0 * peak_density
        ax.set_ylim(y_lo, y_hi)
        # Whole decades strictly inside the range, so the ticks follow the data instead
        # of assuming one parcellation's density scale.
        ax.set_yticks([10.0 ** k for k in range(-4, 5) if y_lo < 10.0 ** k < y_hi])
        ax.set_xlim(-limit, limit)
        ax.set_ylabel("density (log)", fontsize=style.AXIS_LABEL_SIZE - 1)
        # Substrate on the left, its gap ratio on the right, both set above the panel in
        # the row gap rather than inside it. Two `loc` titles instead of in-panel text:
        # nothing overlaps the histogram or the lambda_1 rule, and no backing boxes.
        # Full TITLE_SIZE. The longest pair ("Weight-permuted" against
        # "gap ratio = 1.92") is what constrains this: at a 1:1.5 column split it closed
        # to under a pixel and both titles had to drop a step; at 1:1.25 the left column
        # is wide enough to carry them at full size. Clearance is measured from the
        # rendered text extents, not judged by eye -- see the act file.
        ax.set_title(style.VARIANT_TITLE[variant], loc="left",
                     fontsize=style.TITLE_SIZE, pad=4)
        ax.set_title(f"gap ratio = {stat[variant]['gap_ratio']:.2f}", loc="right",
                     fontsize=style.TITLE_SIZE, color=style.ANNOTATION_COLOUR, pad=4)
    for ax in stack[:-1]:
        ax.tick_params(labelbottom=False)
    stack[-1].set_xlabel(r"$\lambda$  (raw units of $W$)")
    # Symmetric about zero and derived from the range: the spectrum reaches +/-0.215 at
    # N = 448 and +/-0.266 at N = 1000, so a fixed tick list either clips or crowds.
    step = 0.1 if limit < 0.35 else 0.2
    n_steps = int(np.floor(limit / step))
    stack[-1].set_xticks(np.round(step * np.arange(-n_steps, n_steps + 1), 10))
    # The bulk band, the gap band and the lambda_1 rule are named in the caption, not
    # on the panel: with four rows the labels repeat visually and crowd the histogram.

    # -- (e) ECDF in NORMALISED units: the axis the rest of the thesis matches on -----
    def ecdf(values):
        values = np.sort(np.abs(np.asarray(values, float)))
        return values, np.arange(1, values.size + 1) / values.size

    for variant in variants:
        sub = frame[frame.variant == variant]
        pooled = np.concatenate([np.asarray(row.eig_w_real, float)
                                 for row in sub.itertuples()])
        x, y = ecdf(pooled)
        # Labelled with VARIANT_TITLE, matching the row titles in a-d. VARIANT_LABEL's
        # rung numbering would name the same four substrates a second way inside one
        # figure.
        ax_ecdf.plot(x, y, label=style.VARIANT_TITLE[variant],
                     **{k: v for k, v in style.variant_kwargs(variant).items()
                        if k in ("color", "lw")})
    ax_ecdf.axhline(0.95, color=style.ANNOTATION_COLOUR, lw=0.8, ls=":")
    for variant in variants:
        ax_ecdf.axvline(stat[variant]["bulk95"], color=style.VARIANT_COLOUR[variant],
                        lw=0.8, ls="--", ymax=0.95 / 1.04)
    ax_ecdf.set_xlim(0, 1.0)
    ax_ecdf.set_ylim(0, 1.04)
    ax_ecdf.set_xlabel(r"$|\lambda| \, / \, |\lambda_1|$")
    ax_ecdf.set_ylabel("cumulative fraction\nof modes")
    # The level, labelled discreetly above its own rule, as in the committed E0.4
    # figure. The crossings ARE bulk95 by definition; the caption says so, and the
    # values are on the right-hand axis of (f), so no per-curve numbers are drawn here.
    ax_ecdf.annotate("95th percentile", xy=(0.02, 0.95),
                     xycoords=("axes fraction", "data"), xytext=(0, 2),
                     textcoords="offset points", ha="left", va="bottom",
                     fontsize=style.TICK_SIZE - 1, color=style.ANNOTATION_COLOUR)
    # Lower right is the empty wedge under the plateau; the curves are all above 0.97
    # there. This is the figure's only legend -- (f) names the substrates on its axis
    # and a-d in their titles.
    style.legend(ax_ecdf, loc="lower right", fontsize=style.LEGEND_SIZE - 1)

    # -- (f) per-seed gap ratio, with bulk95 on the right ----------------------------
    rng = np.random.default_rng(0)         # jitter only; nothing statistical
    for position, variant in enumerate(variants):
        values = 1.0 / frame[frame.variant == variant].bulk95.to_numpy(float)
        jitter = position + rng.uniform(-0.13, 0.13, values.size)
        ax_strip.plot(jitter, values, ls="none", marker="o", ms=3.2, alpha=0.55,
                      color=style.VARIANT_COLOUR[variant])
        median = 1.0 / frame[frame.variant == variant].bulk95.median()
        ax_strip.plot([position - 0.28, position + 0.28], [median, median],
                      color=style.VARIANT_COLOUR[variant], lw=2.2, solid_capstyle="butt")
    ax_strip.set_xticks(range(len(variants)))
    # VARIANT_TITLE_TICK: the same names as the row titles in a-d and the legend in e.
    # The rung-numbered VARIANT_TICK was used while the right column was narrow, which
    # named the same four substrates a third way inside one figure; at 1:1.5 there is
    # room for the real names.
    ax_strip.set_xticklabels([style.VARIANT_TITLE_TICK[v] for v in variants],
                             fontsize=style.TICK_SIZE - 1)
    ax_strip.set_xlim(-0.5, len(variants) - 0.5)
    ax_strip.set_ylabel("gap ratio\n" r"$|\lambda_1| \, / \,$abs. bulk",
                        fontsize=style.AXIS_LABEL_SIZE - 1)
    # Vertical rules at the category marks. Kept here, unlike the bar panels of F2 and
    # F3 where they sit behind the bars and read as noise: this is a jittered strip, so
    # a rule per substrate ties each cloud to its own tick.
    ax_strip.grid(axis="x", visible=True)
    # bulk95 is the reciprocal, so one strip carries both readings and the identity
    # gap ratio == 1/bulk95 == sr_crit needs no second panel.
    secondary = ax_strip.secondary_yaxis(
        "right", functions=(lambda v: 1.0 / np.where(v == 0, np.nan, v),
                            lambda v: 1.0 / np.where(v == 0, np.nan, v)))
    secondary.set_ylabel("bulk95", fontsize=style.AXIS_LABEL_SIZE - 1)
    secondary.tick_params(labelsize=style.TICK_SIZE)

    # Absolute offsets, not axes fractions: the stacked rows are 91.8 px tall against
    # e and f's 203.0 px, so a shared `dy` fraction put the 'e' 21.5 px higher on the
    # page than the 'a' level with it. One vertical offset for all six (matching the row
    # titles' pad, so a-d's letters sit level with their own titles); the horizontal one
    # differs by column because each must clear its own y-label and tick labels, which
    # are wider on the right.
    for ax, letter in zip(stack, "abcd"):
        style.panel_label(ax, letter, offset_points=(-9, 4))
    style.panel_label(ax_ecdf, "e", offset_points=(-30, 4))
    style.panel_label(ax_strip, "f", offset_points=(-30, 4))
    return fig


def f2_gap_not_bulk(ctx):
    """The difference is a gap, not a bulk, and it holds at both N."""
    frame = ctx.frame("spectra_both")
    variants = style.ordered_variants(frame.variant.unique())
    fig, axes = plt.subplots(1, 3, figsize=(7.6, 2.6))
    width = 0.36
    positions = np.arange(len(variants))

    panels = [
        ("abs_bulk", "absolute bulk radius", "prod_of_medians", None),
        ("lambda_max_raw", r"$|\lambda_1|$ (raw units)", "median", None),
        ("gap_ratio", r"gap ratio $|\lambda_1| \, / \,$abs. bulk", "sr_crit", None),
    ]
    for ax, (column, label, kind, _) in zip(axes, panels):
        for offset, scale in ((-width / 2, 448), (width / 2, 1000)):
            if kind == "sr_crit":
                # CONVENTIONS: sr_crit = 1 / median_over_seeds(bulk95). The gap ratio,
                # the inverse bulk and the critical scale are the same number.
                values = [1.0 / frame[(frame.variant == v) & (frame.scale == scale)]
                          .bulk95.median() for v in variants]
            elif kind == "prod_of_medians":
                # TIER0 §3.1's aggregation: median(bulk95) x median(|lambda_1|), NOT
                # the median of the per-seed products. The two agree at N=448 (4.4%
                # spread either way) and differ at N=1000 (6.4% against 6.9%), and
                # only this one satisfies the identity panel c draws on:
                # |lambda_1| / abs_bulk == 1 / median(bulk95) == sr_crit. Taking the
                # median of the products instead breaks it by up to 0.055 at N=1000,
                # so panels a, b and c would no longer divide into one another.
                values = [
                    frame[(frame.variant == v) & (frame.scale == scale)].bulk95.median()
                    * frame[(frame.variant == v) & (frame.scale == scale)]
                    .lambda_max_raw.median() for v in variants]
            else:
                values = [frame[(frame.variant == v) & (frame.scale == scale)]
                          [column].median() for v in variants]
            ax.bar(positions + offset, values, width,
                   color=[style.VARIANT_COLOUR[v] for v in variants],
                   alpha=1.0 if scale == 448 else 0.45, edgecolor="white", linewidth=0.5,
                   label=f"N = {scale}")
        ax.set_xticks(positions)
        # No per-axis substrate labels. Three panels at 198 px carry the same four
        # categories in the same colours, so naming them three times costs the space
        # three times over -- and the plain names (as F1) do not fit: they collide by
        # up to 12.4 px at the contract's 8pt and only clear at 5pt, which is not
        # legible. Named once in the figure legend below instead.
        ax.tick_params(labelbottom=False)
        ax.set_ylabel(label)
        ax.grid(axis="x", visible=False)

    # No panel titles. All three panels are zero-based, so "near-identical" in a and
    # "separated" in b is a comparison the reader makes directly rather than one an axis
    # crop has arranged -- but a zero-based axis hides the 4.4%, so the spread, the 1.78x
    # Perron ratio and the sr_crit identity have to be stated somewhere. They are all in
    # the caption (act1_structure.md, F2), which keeps the panels clean. **If the caption
    # is ever trimmed, those three numbers must survive the trim**: without them panel a
    # reads as identity rather than near-identity.
    handles = [plt.Rectangle((0, 0), 1, 1, color="0.35", alpha=a) for a in (1.0, 0.45)]
    axes[2].legend(handles, ["N = 448", "N = 1000"], loc="upper right")
    for ax, letter in zip(axes, "abc"):
        style.panel_label(ax, letter, dx=-0.14)
    # Two legends, each carrying one thing: colour is substrate, alpha is scale. The
    # substrate legend is figure-level because all three panels share those categories.
    substrate_handles = [plt.Rectangle((0, 0), 1, 1, color=style.VARIANT_COLOUR[v])
                         for v in variants]
    fig.legend(substrate_handles, [style.VARIANT_TITLE[v] for v in variants],
               loc="lower center", ncol=len(variants), frameon=False,
               fontsize=style.LEGEND_SIZE, handlelength=1.1, handleheight=0.9,
               columnspacing=1.6, borderpad=0.0, bbox_to_anchor=(0.5, 0.0))
    fig.tight_layout(rect=(0, 0.10, 1, 1))
    return fig


# =============================================================================
# Chapter 3 -- methods: the comparison problem (contribution 5)
# =============================================================================
def f3_two_axes(ctx):
    """Neither matching axis is neutral, shown one axis per panel.

    **Grouped by axis, not by substrate.** ``dD`` is a between-substrate quantity at
    fixed x, so putting both substrates in one panel makes the vertical gap between the
    curves *be* the delta: it collapses from (a) to (b) in front of the reader. Grouping
    by substrate instead would put the two curves that need comparing in different
    panels, leaving the reader to reconstruct across panels the one quantity the figure
    is about.

    **(a) and (b) do not subtract to (c), and the caption says so.** ``dD_median`` is the
    median over seeds of the per-seed difference; ``d_eff_connectome`` and
    ``d_eff_erdos_renyi`` are the medians of each substrate separately, and the median of
    differences is not the difference of medians (they part by up to 9.4 at nominal, 8.3
    on the matched axis; at the peak, +343.3 against +338.1). The paired per-seed
    statistic is the right one for a paired comparison and is what `TIER0` §2.2 publishes,
    so (c) keeps it and the discrepancy is stated rather than engineered away.

    The claim rests on F1 and F2: the four substrates differ *only* in ``|lambda_1|``,
    their absolute bulk radii agreeing to 4.4%. One degree of freedom, so normalising by
    ``|lambda_1|`` pins the Perron root and forces the bulks apart, and matching on
    ``sigma*bulk95`` does the reverse. Both cannot hold, and the mechanism under test is
    the Perron mode itself.
    """
    panel = ctx.frame("e02_panel")
    summary = ctx.frame("e02_axis_summary")
    fig, axes = plt.subplots(1, 3, figsize=(7.8, 2.9))

    axis_style = {"nominal": dict(color="#1f77b4"), "effective": dict(color="#c44e52")}
    pair = ("connectome", "erdos_renyi")

    # -- (a), (b): both substrates, one panel per matching coordinate -----------------
    for ax, axis in zip(axes[:2], ("nominal", "effective")):
        curve = panel[panel.axis == axis].sort_values("x")
        connectome = curve["d_eff_connectome"].to_numpy(float)
        erdos = curve["d_eff_erdos_renyi"].to_numpy(float)
        # The shaded band between the curves is what panel c plots. Neutral grey, so it
        # reads as "the gap" rather than as a third substrate.
        ax.fill_between(curve.x, connectome, erdos, color=style.ANNOTATION_COLOUR,
                        alpha=0.13, lw=0, zorder=1)
        for variant, values in zip(pair, (connectome, erdos)):
            # VARIANT_TITLE, not variant_kwargs' VARIANT_LABEL: F1 and F2 name the
            # substrates plainly and the rung numbering would reappear here alone.
            ax.plot(curve.x, values, zorder=2, label=style.VARIANT_TITLE[variant],
                    **{k: v for k, v in style.variant_kwargs(variant).items()
                       if k in ("color", "lw", "ls")})
        ax.set_xlabel(style.AXIS_LABEL[axis], fontsize=style.AXIS_LABEL_SIZE - 1)
        ax.set_xlim(0, curve.x.max())
        ax.set_ylim(0, 1.06 * N_NODES)
    axes[1].sharey(axes[0])
    axes[1].tick_params(labelleft=False)
    axes[0].set_ylabel(r"$d_{\rm eff}$  (ridge effective rank)")
    # CONVENTIONS: every memory figure draws the d_eff = N ceiling. ER runs along it.
    style.draw_ceiling(axes[0], N_NODES)
    axes[1].axhline(N_NODES, color=style.CEILING_COLOUR, lw=0.9, ls=":", zorder=1)
    style.legend(axes[0], loc="lower right", fontsize=style.LEGEND_SIZE - 1)

    # -- (c): the two deltas, the published statistic --------------------------------
    for axis in ("nominal", "effective"):
        curve = panel[panel.axis == axis].sort_values("x")
        colour = axis_style[axis]["color"]
        axes[2].plot(curve.x, curve.dD_median, label=style.AXIS_SHORT[axis], lw=1.6,
                     color=colour)
        axes[2].fill_between(curve.x, curve.dD_q25, curve.dD_q75, alpha=0.15,
                             color=colour, lw=0)
        row = summary[summary.axis == axis].iloc[0]
        axes[2].plot([row.peak_x], [row.peak_dD], marker="o", ms=4, color=colour)
        axes[2].annotate(f"{row.peak_dD:+.0f}", xy=(row.peak_x, row.peak_dD),
                         xytext=(4, 4), textcoords="offset points",
                         fontsize=style.TICK_SIZE, color=colour)
        axes[2].plot([row.min_x], [row.min_dD], marker="v", ms=4, color=colour)
        axes[2].annotate(f"{row.min_dD:+.0f}", xy=(row.min_x, row.min_dD),
                         xytext=(4, -10), textcoords="offset points",
                         fontsize=style.TICK_SIZE, color=colour)
    axes[2].axhline(0, color="0.5", lw=0.8)
    axes[2].set_xlabel("matching coordinate\n(nominal $\\sigma$, or $\\sigma\\cdot$bulk95)",
                       fontsize=style.AXIS_LABEL_SIZE - 1)
    axes[2].set_ylabel(r"$\Delta d_{\rm eff}$  (connectome $-$ ER)")
    style.legend(axes[2], loc="lower right", title="axis",
                 title_fontsize=style.LEGEND_SIZE - 1, fontsize=style.LEGEND_SIZE - 1)

    for ax, letter in zip(axes, "abc"):
        style.panel_label(ax, letter, offset_points=(-6, 4))
    fig.tight_layout()
    return fig


# =============================================================================
# Chapter 5 -- Act II: the spectrum decomposes the manifold
# =============================================================================
def f4_perron_carries_the_mean(ctx):
    """The Perron mode is a common mode: it carries the mean and time-centring removes it."""
    alignment = ctx.frame("alignment")
    saturation = ctx.frame("saturation")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.7))

    sub = alignment[(alignment.condition == "human_empirical")
                    & (alignment.variant == "connectome") & (alignment.task == "mc")]
    operating_point = sub.spectral_radius.max()
    sub = sub[sub.spectral_radius == operating_point]
    basis_style = {"wmodes": ("#d62728", "-"), "harmonics": ("#1f77b4", "-"),
                   "random": ("#999999", "--")}
    for basis, (colour, dash) in basis_style.items():
        curve = sub[sub.basis == basis].groupby("k").captured.median()
        axes[0].plot(curve.index, curve.values, color=colour, ls=dash, label=basis)
    axes[0].set_xscale("log")
    axes[0].set_xlabel("top-$k$ basis vectors")
    axes[0].set_ylabel("fraction of time-centred\nstate variance captured")
    axes[0].set_title(f"all-positive substrate, $\\sigma$ = {operating_point:.2f}")
    style.legend(axes[0], loc="upper left")

    memory = saturation[(saturation.task == "mc")
                        & (saturation.condition == "human_empirical")]
    for variant in style.ordered_variants(memory.variant.unique()):
        curve = (memory[memory.variant == variant]
                 .groupby("spectral_radius").mean_state.median().abs())
        axes[1].plot(curve.index, curve.values, **style.variant_kwargs(variant))
    axes[1].set_xlabel(r"nominal $\sigma$")
    axes[1].set_ylabel(r"$|\overline{x}|$  (common-mode amplitude)")
    axes[1].set_ylim(0, 1.05)
    style.legend(axes[1], loc="lower right", fontsize=style.LEGEND_SIZE - 1)
    for ax, letter in zip(axes, "ab"):
        style.panel_label(ax, letter)
    fig.tight_layout()
    return fig


def f5_sign_selects_the_basis(ctx):
    """Sign composition decides which structural basis the fluctuations occupy."""
    alignment = ctx.frame("alignment")
    task = "lorenz"
    conditions = [c for c in ("human_empirical", "human_empirical_signed", "human_gaussian")
                  if c in set(alignment.condition)]
    fig, axes = plt.subplots(1, len(conditions), figsize=(7.6, 2.6), sharey=True)
    axes = np.atleast_1d(axes)
    basis_style = {"harmonics": ("#1f77b4", "-"), "wmodes": ("#d62728", "-"),
                   "random": ("#999999", "--")}
    for ax, condition in zip(axes, conditions):
        sub = alignment[(alignment.condition == condition) & (alignment.task == task)
                        & (alignment.variant == "connectome")]
        operating_point = sub.spectral_radius.max()
        sub = sub[sub.spectral_radius == operating_point]
        for basis, (colour, dash) in basis_style.items():
            curve = sub[sub.basis == basis].groupby("k").captured.median()
            ax.plot(curve.index, curve.values, color=colour, ls=dash, label=basis)
        ax.set_xscale("log")
        ax.set_xlabel("top-$k$ basis vectors")
        ax.set_title(f"{style.CONDITION_LABEL.get(condition, condition)}\n"
                     f"$\\sigma$ = {operating_point:.2f}", fontsize=style.TITLE_SIZE - 1)
    axes[0].set_ylabel("fraction of variance captured")
    style.legend(axes[0], loc="upper left")
    for ax, letter in zip(axes, "abc"):
        style.panel_label(ax, letter, dx=-0.10)
    fig.tight_layout()
    return fig


def f6_pr_misses_readout_structure(ctx):
    """Variance-weighted dimensionality discounts the directions memory lives in."""
    frame = ctx.frame("probe3")
    medians = frame.groupby("variant")[["d_eff", "pr", "mc"]].median()
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8))

    for ax, column, label in ((axes[0], "d_eff", r"$d_{\rm eff}$  (ridge effective rank)"),
                              (axes[1], "pr", "PR  (participation ratio)")):
        for variant, row in medians.iterrows():
            ax.scatter(row[column], row.mc, s=42, zorder=3,
                       color=style.VARIANT_COLOUR.get(variant, "0.4"),
                       edgecolor="white", linewidth=0.6,
                       label=style.VARIANT_LABEL.get(variant, variant))
        rho = spearmanr(medians[column], medians.mc).statistic
        ax.set_xlabel(label)
        ax.set_ylabel("memory capacity (MC)")
        ax.set_title(f"ladder ordering  $r_s$ = {rho:+.2f}   (n = {len(medians)} rungs)")
    axes[0].axvline(N_NODES, color=style.CEILING_COLOUR, lw=0.9, ls=":")
    axes[0].text(N_NODES, 0.02, f" N = {N_NODES}", transform=axes[0].get_xaxis_transform(),
                 fontsize=style.TICK_SIZE, color=style.CEILING_COLOUR, va="bottom")
    style.legend(axes[1], loc="center left", bbox_to_anchor=(1.02, 0.5),
                 fontsize=style.LEGEND_SIZE - 1)
    for ax, letter in zip(axes, "ab"):
        style.panel_label(ax, letter)
    fig.tight_layout()
    return fig


# =============================================================================
# Chapter 6 -- Act III, memory arm
# =============================================================================
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


# =============================================================================
# Chapter 6 -- Act III, prediction arm
# =============================================================================
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


# =============================================================================
# Chapter 7 -- Act IV, minimal
# =============================================================================
def f15_yeo_loads_the_perron_mode(ctx):
    """Which intrinsic networks carry the common mode the rest of the thesis is about."""
    frame = ctx.frame("perron_yeo").sort_values("perron_mass", ascending=False)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.6))

    positions = np.arange(len(frame))
    axes[0].bar(positions, frame.perron_mass, color="#c44e52",
                edgecolor="white", linewidth=0.5)
    axes[0].set_xticks(positions)
    axes[0].set_xticklabels(frame.network, fontsize=style.TICK_SIZE)
    axes[0].set_ylabel("Perron-mode mass\n(sums to 1 over the cortex)")
    axes[0].grid(axis="x", visible=False)

    axes[1].bar(positions, 1e3 * frame.mass_per_node, color="#4c72b0",
                edgecolor="white", linewidth=0.5)
    axes[1].set_xticks(positions)
    axes[1].set_xticklabels(frame.network, fontsize=style.TICK_SIZE)
    axes[1].set_ylabel(r"mass per node ($\times 10^{-3}$)")
    axes[1].set_title("size-corrected", fontsize=style.TITLE_SIZE - 1)
    axes[1].grid(axis="x", visible=False)
    for ax, letter in zip(axes, "ab"):
        style.panel_label(ax, letter, dx=-0.12)
    fig.tight_layout()
    return fig


# =============================================================================
# Registry -- the 14 rendered figures. F8 is retired into F3.
# =============================================================================
FIGURES = {
    "F1": (4, "spectrum: a large real Perron root over everyone's bulk", f1_spectrum),
    "F2": (4, "gap not bulk, at both N", f2_gap_not_bulk),
    "F3": (3, "neither matching axis is neutral", f3_two_axes),
    "F4": (5, "the Perron mode carries the mean", f4_perron_carries_the_mean),
    "F5": (5, "sign selects the basis", f5_sign_selects_the_basis),
    "F6": (5, "PR misses readout-relevant structure", f6_pr_misses_readout_structure),
    "F7": (6, "the crossing: peaks lowest, retains most", f7_the_crossing),
    "F9": (6, "the supercritical margin is scale-invariant", f9_scale_invariance),
    "F10": (6, "peak parity, with CIs", f10_peak_parity),
    "F11": (6, "rescue from Perron domination", f11_perron_rescue),
    "F12": (6, "curvature is bimodal", f12_curvature_is_bimodal),
    "F13": (6, "generation read as VPT", f13_generation_as_vpt),
    "F14": (6, "sigma_eff as locator, not criterion", f14_sigma_eff_is_a_locator),
    "F15": (7, "which Yeo networks load the Perron mode", f15_yeo_loads_the_perron_mode),
    "F16": (6, "the crossing, with its axis and its coverage", f16_phase_boundaries),
}

# The workshop subset (5pp, ~4 figures), marked W on FIGURE_LIST.md. F16 is the first
# reserve if a fifth slot appears.
WORKSHOP = ("F1", "F2", "F7", "F12")

# Cap raised from 14 to 15 in session 0 to give contribution 2 a figure of its own.
assert len(FIGURES) == 15, f"cap is 15 figures, registry holds {len(FIGURES)}"

# ---------------------------------------------------------------------------------
# Supplementary figures -- appendix only, NOT part of the numbered main-text list.
#
# Separate namespace on purpose. `FIGURE_LIST.md` caps the main text at 15 and the
# assertion above enforces it; a scale replicate of an existing figure is not a new
# claim and must not consume a main-text slot or quietly raise that cap. The rule that
# no figure exists outside `FIGURE_LIST.md` still binds, so S-figures are listed there
# in their own section.
#
# The bar for an S-figure: it makes NO claim the main text does not already make, and
# it is built by an EXISTING builder at different parameters. Anything that needs its
# own builder is a new figure and goes through the cap.
SUPPLEMENTARY = {
    "S1": (None, "F1 at N = 1000 (appendix scale replicate)", s1_spectrum_n1000),
}
for _id, (_chapter, _name, _builder) in SUPPLEMENTARY.items():
    assert _id.startswith("S") and _id not in FIGURES, (
        f"{_id}: supplementary IDs are S-prefixed and must not collide with the "
        "numbered main-text list.")

# What the entry point renders. FIGURES stays the cap-checked main-text list.
ALL_FIGURES = {**FIGURES, **SUPPLEMENTARY}

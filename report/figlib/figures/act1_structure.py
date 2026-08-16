"""Act I -- structure sets the spectrum.  Chapters 3 and 4.

F1 and F2 carry contribution 1 (the difference is a gap, not a bulk); F3 carries
contribution 5 (neither matching axis is neutral) and **prints in chapter 3**, but it
is Act I's figure and Session 1 owns it -- `FIGURE_LIST` is explicit that Session 3
must not re-render it. S1 is F1 at N=1000, for the appendix, and shares F1's builder so
the two scales cannot drift.

Owned by session 1 (`report/act1_structure.md`).
"""

import numpy as np
import matplotlib.pyplot as plt

from report.figlib import style
from report.figlib.figures.common import N_NODES


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

"""Act I -- structure sets the spectrum.  Chapters 3 and 4.

F1 and F2 carry contribution 1 (the difference is a gap, not a bulk); F3 carries
contribution 5 (neither matching axis is neutral) and **prints in chapter 3**, but it
is Act I's figure and Session 1 owns it -- `FIGURE_LIST` is explicit that Session 3
must not re-render it. S1 is F1 at N=1000, for the appendix, and shares F1's builder so
the two scales cannot drift. F19 draws the same four substrates as graphs, in chapter 4's
first section, which `act1_structure.md` registers as carrying **no results**: it is the
ladder's design shown rather than argued, and it carries no claim. S4 is that same
picture widened from the ladder's four substrates to the whole family of seven, for the
appendix; it shares F19's node ordering and its seed rule, makes no comparison, and
TIER0 3.1(b)'s scope guard on the three off-ladder rungs holds over it.

Owned by session 1 (`report/act1_structure.md`).
"""

import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from report.figlib import style
from report.figlib.figures.common import N_NODES

# Act-local. The frozen edge count of the N = 448 self-built consensus, which every rung
# of the ladder matches exactly by construction -- Erdos-Renyi included, since the null
# fixes the edge count rather than the density in expectation.
EDGE_COUNT = 5323


def f1_spectrum(ctx):
    """F1 at the primary parcellation, N = 448."""
    return _spectrum_figure(ctx, "spectra_448")


def s1_spectrum_n1000(ctx):
    """S1 -- F1 rebuilt at N = 1000, the scale replicate for the appendix.

    Same builder, same frozen artifact family, different parcellation. Nothing here is
    a second implementation: if the figure changes, both scales change with it.
    """
    return _spectrum_figure(ctx, "spectra_1000")


def _representative_row(frame, variant):
    """The one seed a figure draws for a resampled null: ``bulk95`` nearest the median.

    A stated rule, not a pick. Held here rather than inline because **two** figures now
    draw it -- F1's panels a-d and F19's four columns -- and the whole point of F19
    naming the same seed is that a reader comparing the two sees the same matrices. Two
    copies of the rule could drift; one cannot.
    """
    sub = frame[frame.variant == variant]
    return sub.loc[(sub.bulk95 - sub.bulk95.median()).abs().idxmin()]


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
        pick = _representative_row(frame, variant)
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


# =============================================================================
# F19 -- the four substrates as graphs. Chapter 4, section 1. NO results.
# =============================================================================
# Sequential maps for the two matrix rows. **Not variant colours**: a matrix cell is an
# edge, not a substrate, and the Okabe-Ito palette is spent where substrate identity is
# actually carried -- the column titles and the degree marginals. Both maps are
# colourblind-safe and monotone in luminance: `Greys` trivially, and `magma` is one of
# matplotlib's perceptually uniform maps, whose luminance ramp stays monotone when
# reversed. Reversed is the one that reads correctly here -- zero is white, so a matrix's
# density is read off the page, and a heavier edge is a darker cell.
BINARY_CMAP = "Greys"
WEIGHT_CMAP = "magma_r"

# The magnified block, selected by a stated rule rather than picked: of the **diagonal
# blocks of the drawn ordering** (hemisphere x community), the one with the highest
# within-block binary edge density among blocks of BLOCK_SIZE_RANGE nodes.
#
# **Blocks, not communities, and the reason is the ordering.** Hemisphere is the outer
# key, so a community that spans both hemispheres occupies two non-contiguous diagonal
# blocks. Magnifying a whole community would magnify a node set that is not contiguous in
# the drawn ordering, and the indicator on (e-h) would have to mark two squares and the
# rectangle between them. The diagonal blocks are the squares a reader already sees in
# the full panels, so those are what the zoom row magnifies. The size range keeps the
# magnified panel legible: at 22 nodes a cell is large enough to read a colour off.
BLOCK_SIZE_RANGE = (15, 40)

# **The four binary-graph statistics are no longer drawn here.** They moved out of the
# figure and into a LaTeX table in the chapter (`tab:act1-topology`) on 1 September 2026,
# where four rows of numbers read as numbers rather than as a fifth band of the figure.
# `substrate_topology.parquet` and `TIER0` 3.13 are unchanged and remain their source;
# only the rendering moved.


def _drawn_seed(edges, spectra, variant):
    """Which seed of ``variant`` this figure draws.

    The two randomised variants are drawn at **the seed F1 draws** -- ``bulk95`` nearest
    the median, taken through `_representative_row` so there is one implementation of the
    rule -- so a reader setting F19 beside F1 sees the same two matrices rather than two
    different draws of the same null.

    The connectome and the weight-permuted control are single graphs and the artifact
    carries one seed each, so there is nothing to choose: the rule would be answering a
    question that does not arise. The assertion is what makes that a statement rather
    than an assumption.
    """
    seeds = sorted(edges[edges.variant == variant].seed.unique())
    if len(seeds) == 1:
        return int(seeds[0])
    seed = int(_representative_row(spectra, variant).seed)
    assert seed in seeds, (
        f"{variant}: F1 draws seed {seed}, which substrate_edges.parquet does not carry "
        f"(it has {seeds}). The two figures must draw the same graph.")
    return seed


def _densest_block(binary, bounds):
    """The diagonal block the zoom row magnifies, and the candidates it was chosen from.

    Returns ``(start, stop, chosen, candidates)`` where each candidate is a dict of the
    block's hemisphere, community, size, internal edge count and within-block density.
    Ties on density break on the earlier block, so the rule is total.

    Raises if no block falls in the size range rather than widening it: the range is part
    of the rule, and a silent widening would make the selection unstatable.
    """
    lo_size, hi_size = BLOCK_SIZE_RANGE
    candidates = []
    for start, stop in zip(bounds[:-1], bounds[1:]):
        size = int(stop - start)
        if not lo_size <= size <= hi_size:
            continue
        internal = int(binary[start:stop, start:stop].sum() // 2)
        candidates.append(dict(start=int(start), stop=int(stop), size=size,
                               internal_edges=internal,
                               density=internal / (size * (size - 1) / 2)))
    assert candidates, (
        f"no diagonal block of the drawn ordering has between {lo_size} and {hi_size} "
        f"nodes (sizes: {[int(b - a) for a, b in zip(bounds[:-1], bounds[1:])]}). The "
        "size range is part of the selection rule and is not widened here.")
    chosen = max(candidates, key=lambda c: (c["density"], -c["start"]))
    return chosen["start"], chosen["stop"], chosen, candidates


def _dense(rows, order):
    """One cell's edge rows as a symmetric matrix, permuted into the drawn ordering.

    Split out of `_adjacency` so S4 can reuse the assembly without inheriting the exact
    edge-count assertion, which one of its seven substrates does not satisfy by design.
    """
    matrix = np.zeros((N_NODES, N_NODES))
    matrix[rows.i.to_numpy(int), rows.j.to_numpy(int)] = rows.weight.to_numpy(float)
    matrix += matrix.T
    return matrix[np.ix_(order, order)]


def _adjacency(edges, variant, seed, order):
    """One cell's weighted adjacency, symmetrised and permuted into the drawn ordering."""
    rows = edges[(edges.variant == variant) & (edges.seed == seed)]
    assert len(rows) == EDGE_COUNT, (
        f"{variant} seed {seed}: {len(rows)} edges, not {EDGE_COUNT}. Every rung matches "
        "the connectome's edge count exactly by construction.")
    return _dense(rows, order)


def f19_substrates_as_graphs(ctx):
    """The four substrates drawn as graphs, under one node ordering.

    **This figure sits in chapter 4's first section, which carries no results.** It shows
    what the ladder *is*: the design facts of four substrates that share a node count, an
    edge count and a density, drawn so the differences between them are visible rather
    than asserted. Nothing here is a claim. The four binary-graph statistics that were
    drawn beneath the columns until 1 September 2026 are now a LaTeX table in the chapter
    (`tab:act1-topology`); `substrate_topology.parquet` and `TIER0` 3.13 are unchanged.

    **One node ordering for all eight panels** -- hemisphere, then community, then
    descending connectome degree within community -- so the four substrates are compared
    cell for cell rather than each shown in whatever order suits it. The communities are
    detected once, on the connectome, and reused; separator lines mark their boundaries.

    **The zoom row magnifies one diagonal block of the drawn ordering**, chosen by
    `_densest_block`: the densest block of 15 to 40 nodes, on the binary connectome. It
    is drawn on the **same** colour scale as (e-h) and is marked on them, so (i) against
    (j) is the same comparison (e) against (f) makes, at a size where a single cell's
    colour can be read. Rescaling the zoom panels to their own range would make (i)
    against (j) a comparison of two different scales and say nothing.

    **Panels (i) and (j) fill exactly the same cells, and the builder asserts it.** The
    permutation reorders which edge carries which weight, so within any set of nodes the
    filled cells are the same cells; what differs is the weight sitting in each, drawn
    from the whole graph's multiset rather than from this block's.

    **Panels (a) and (b) are the same image, and the builder asserts it.** The
    weight-permuted control is the connectome's own graph with its own weights reordered
    across the edges, so its binary adjacency is byte-identical and its degree marginal
    is the same marginal. That is the reproduction gate
    `report/artifacts/build_substrate_graphs.py` runs before it writes anything, restated
    here so a figure that has quietly come apart from it fails the build. The two part
    company in (e) and (f), where the weights are drawn, and the only difference between
    those two panels is which edge carries which weight.
    """
    edges = ctx.frame("substrate_edges")
    ordering = ctx.frame("substrate_order").sort_values("position")
    spectra = ctx.frame("spectra_448")
    variants = style.ordered_variants(edges.variant.unique())
    order = ordering.node.to_numpy(int)

    weighted = {v: _adjacency(edges, v, _drawn_seed(edges, spectra, v), order)
                for v in variants}
    binary = {v: (m > 0) for v, m in weighted.items()}
    degree = {v: b.sum(1) for v, b in binary.items()}

    # The live ordering against the frozen edge list. `substrate_order` computes the
    # degree itself, from `HumanSubstrateBuilder.mask`; `substrate_edges` is a file
    # written months apart from any figure. If the two ever describe different graphs --
    # a re-parcellation, a re-ordered consensus -- every panel would still render, and
    # every panel would be permuted wrongly. This is the check that catches it.
    assert np.array_equal(degree["connectome"], ordering.degree.to_numpy(int)), (
        "the node ordering's degree column is not the connectome's degree in "
        "substrate_edges.parquet: the two sources describe different graphs, so the "
        "permutation applied to every panel is wrong.")
    assert np.array_equal(binary["connectome"], binary["connectome_weight_permuted"]), (
        "the weight-permuted control's binary adjacency is not identical to the "
        "connectome's. Panels (a) and (b) are supposed to be the same image; a "
        "difference is a defect in the permutation, not a finding.")

    # Community boundaries in the drawn ordering. A community that spans the hemispheres
    # appears as two blocks, one in each half, because hemisphere is the outer key. The
    # hemisphere split is itself one of these boundaries and is drawn heavier.
    block = ordering.hemisphere.to_numpy() * 100 + ordering.community.to_numpy()
    boundaries = np.flatnonzero(block[1:] != block[:-1]) + 1
    hemisphere_cut = np.flatnonzero(
        ordering.hemisphere.to_numpy()[1:] != ordering.hemisphere.to_numpy()[:-1]) + 1

    # The magnified block, by the stated rule. Its bounds are block boundaries, so the
    # magnified square is one of the squares the reader already sees in (e-h).
    zoom_lo, zoom_hi, _, _ = _densest_block(
        binary["connectome"], np.concatenate([[0], boundaries, [N_NODES]]))
    assert np.array_equal(binary["connectome"][zoom_lo:zoom_hi, zoom_lo:zoom_hi],
                          binary["connectome_weight_permuted"][zoom_lo:zoom_hi,
                                                               zoom_lo:zoom_hi]), (
        "panels (i) and (j) do not fill the same cells. The permutation moves weights "
        "between edges and leaves the edge set alone, so within any set of nodes the "
        "filled cells are identical; a difference is a defect in the permutation.")

    # ---------------------------------------------------------------- layout
    # Four equal columns and nothing else, so the colourbar spanning them is exactly as
    # wide as the four adjacency panels. The row y-labels sit in the left margin the
    # gridspec reserves; they belong to the panels, not to a column of their own.
    fig = plt.figure(figsize=(7.6, 7.0))
    outer = fig.add_gridspec(3, 1, height_ratios=[1.37, 1.00, 1.24], hspace=0.13,
                             left=0.055, right=0.995, top=0.955, bottom=0.020)
    top = outer[0].subgridspec(2, 4, height_ratios=[0.32, 1.0], hspace=0.08, wspace=0.10)
    middle = outer[1].subgridspec(1, 4, wspace=0.10)
    lower = outer[2].subgridspec(2, 4, height_ratios=[1.0, 0.075], hspace=0.30,
                                 wspace=0.10)

    marginals = [fig.add_subplot(top[0, k]) for k in range(len(variants))]
    binary_axes = [fig.add_subplot(top[1, k]) for k in range(len(variants))]
    weight_axes = [fig.add_subplot(middle[0, k]) for k in range(len(variants))]
    zoom_axes = [fig.add_subplot(lower[0, k]) for k in range(len(variants))]
    ax_colourbar = fig.add_subplot(lower[1, :])

    # ------------------------------------------------- (a-d) binary, with the marginal
    degree_ceiling = 1.08 * max(d.max() for d in degree.values())
    for k, variant in enumerate(variants):
        colour = style.VARIANT_COLOUR[variant]
        ax = marginals[k]
        ax.fill_between(np.arange(N_NODES), 0, degree[variant], step="mid",
                        color=colour, lw=0)
        ax.set_xlim(-0.5, N_NODES - 0.5)
        ax.set_ylim(0, degree_ceiling)
        ax.set_xticks([])
        ax.grid(False)
        # The name in the substrate's own colour, so the column is identified once and
        # the marginal, the two matrices and the strip column below all inherit it.
        ax.set_title(style.VARIANT_TITLE[variant], fontsize=style.TITLE_SIZE,
                     color=colour, pad=3)
        if k:
            ax.set_yticks([])
        else:
            ax.set_yticks([0, 60])
            ax.set_ylabel("degree", fontsize=style.AXIS_LABEL_SIZE - 1)
            ax.tick_params(labelsize=style.TICK_SIZE - 1)

        _draw_matrix(binary_axes[k], binary[variant].astype(float), BINARY_CMAP,
                     None, boundaries, hemisphere_cut)
    binary_axes[0].set_ylabel("binary adjacency", fontsize=style.AXIS_LABEL_SIZE - 1)

    # ----------------------------------------------------- (e-h) weighted, on a log scale
    # One scale across the four, because the four draw from the same weight multiset --
    # the connectome's own, permuted in (f) and resampled with replacement in (g) and
    # (h). Four private scales would make four different pictures of the same numbers.
    positive = np.concatenate([m[m > 0] for m in weighted.values()])
    norm = LogNorm(vmin=float(positive.min()), vmax=float(positive.max()))
    cmap = mpl.colormaps[WEIGHT_CMAP].with_extremes(bad="white")
    for k, variant in enumerate(variants):
        # All four share `norm` and `cmap`, so the colourbar below can be taken from
        # whichever image the loop ends on: it describes every panel in the row.
        image = _draw_matrix(weight_axes[k], weighted[variant], cmap, norm,
                             boundaries, hemisphere_cut)
    weight_axes[0].set_ylabel("weighted adjacency", fontsize=style.AXIS_LABEL_SIZE - 1)

    # ------------------------------------------- (i-l) one diagonal block, magnified
    # Same norm, same cmap, same node ordering, same columns: only the extent changes.
    # The indicator is drawn a cell outside the block so it marks the square without
    # covering any of its cells, and unclipped so the two sides that fall on the panel
    # edge are still visible. ANNOTATION_ACCENT is the one non-variant accent this
    # figure has not already spent on the separator furniture.
    for k, variant in enumerate(variants):
        _draw_matrix(zoom_axes[k], weighted[variant][zoom_lo:zoom_hi, zoom_lo:zoom_hi],
                     cmap, norm, np.array([], int), np.array([], int))
        marker = plt.Rectangle((zoom_lo - 1.5, zoom_lo - 1.5),
                               zoom_hi - zoom_lo + 2.0, zoom_hi - zoom_lo + 2.0,
                               fill=False, lw=1.0, color=style.ANNOTATION_ACCENT,
                               clip_on=False, zorder=5)
        weight_axes[k].add_patch(marker)
    zoom_axes[0].set_ylabel("magnified block", fontsize=style.AXIS_LABEL_SIZE - 1)

    bar = fig.colorbar(image, cax=ax_colourbar, orientation="horizontal")
    bar.ax.tick_params(labelsize=style.TICK_SIZE - 1)
    bar.outline.set_linewidth(0.4)
    # **The whole colourbar assembly is kept inside the width of the adjacency panels.**
    # The title goes ABOVE the bar rather than beside it: beside it, the name hangs off
    # the left of column (e) and the figure reads as though the bar belonged to
    # something further left. Above it, the assembly's horizontal extent is the bar's
    # own, which is the four panels' combined width by construction.
    bar.set_label("edge weight (logarithmic)", fontsize=style.AXIS_LABEL_SIZE - 1,
                  labelpad=4)
    bar.ax.xaxis.set_label_position("top")
    _keep_ticks_inside(bar, norm)

    for row, letters in ((marginals, "abcd"), (weight_axes, "efgh"),
                         (zoom_axes, "ijkl")):
        for ax, letter in zip(row, letters):
            style.panel_label(ax, letter, offset_points=(-3, 2))
    return fig


def _keep_ticks_inside(bar, norm) -> None:
    """Anchor the outermost decade labels to the bar's ends so neither overhangs.

    The largest weight is 0.1044 and the top decade therefore sits at 0.996 of the bar's
    length, so a label centred on that tick hangs off the right-hand edge of panel (h)
    and the assembly is wider than the panels it describes. Anchoring the end labels
    rather than dropping the decade keeps the reader's top reference point. Positions are
    read straight off the norm, so no draw is needed to decide which labels to move.
    """
    decades = range(int(np.ceil(np.log10(norm.vmin))),
                    int(np.floor(np.log10(norm.vmax))) + 1)
    ticks = [10.0 ** power for power in decades]
    bar.set_ticks(ticks)
    for tick, text in zip(ticks, bar.ax.get_xticklabels()):
        position = float(norm(tick))
        if position > 0.97:
            text.set_horizontalalignment("right")
        elif position < 0.03:
            text.set_horizontalalignment("left")


def _draw_matrix(ax, matrix, cmap, norm, boundaries, hemisphere_cut):
    """One 448 x 448 panel: zeros white, community separators over the image."""
    masked = np.ma.masked_where(matrix <= 0, matrix) if norm is not None else matrix
    kwargs = dict(cmap=cmap, interpolation="nearest", rasterized=True)
    image = (ax.imshow(masked, norm=norm, **kwargs) if norm is not None
             else ax.imshow(masked, vmin=0.0, vmax=1.0, **kwargs))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.4)
        spine.set_color(style.CEILING_COLOUR)
    for cut in boundaries:
        heavy = cut in hemisphere_cut
        for line in (ax.axvline, ax.axhline):
            line(cut - 0.5, color=style.ANNOTATION_COLOUR if heavy
                 else style.CEILING_COLOUR,
                 lw=0.7 if heavy else 0.35, alpha=0.9 if heavy else 0.55)
    return image


# =============================================================================
# S4 -- the full substrate family as graphs. Appendix. NO results, NO comparison.
# =============================================================================
# **Columns run in `tab:methods-preservation`'s order, most preserved first.** That is
# NOT the ladder's order and the ladder is not contiguous in it: the two off-ladder
# rewires take columns three and four, and the ladder's degree rewire and Erdos-Renyi
# take five and six. Preservation order is the order a reader of that table already has,
# and this figure's whole subject is what each substrate keeps, so it is worth more here
# than contiguity; the caption names the ladder's columns by number rather than calling
# them leftmost.
#
# **Seven substrates is not a seven-rung ladder.** TIER0 3.1(b) puts the three rungs
# outside the criticality-matched ladder on the record and guards their scope, and that
# guard holds over this figure: it draws them and compares nothing.
FULL_FAMILY_ORDER = ["connectome", "connectome_weight_permuted", "clustering_rewire",
                     "modularity_rewire", "degree_rewire", "erdos_renyi",
                     "random_gaussian"]

# Rung 0 is the one substrate of the seven whose edge count is not fixed.
# `random_gaussian` draws each pair independently at the connectome's density, so its
# count is Binomial(_PAIR_COUNT, density) rather than EDGE_COUNT exactly, and the exact
# assertion `_adjacency` carries would fail on a null behaving as designed. Five binomial
# standard deviations is the band, which is 71.0 edges at N = 448 and so admits 4,968 to
# 5,678; the ten seeds run 5,180 to 5,439. The same rule and the same band are applied to
# the same cells by `report/artifacts/build_substrate_graphs.py`, which prints the ten
# counts. The exemption is rung 0's alone: every other variant is exact.
# **S4 is placed full page and rotated, so it is the one figure in the sweep whose
# printed width is `\textheight` rather than `\textwidth`.** That changes two things,
# and both are handled here rather than by scaling the include.
#
# The canvas is drawn AT the printed width, so the figure prints at scale 1.0 and its
# 300 dpi raster is 300 dpi on the page. Every other figure here is a 7.6 in canvas
# reduced to `\textwidth`, where 300 dpi becomes 358 on the page; the same canvas
# magnified to `\textheight` would fall to 244, which is the wrong direction for seven
# columns of 448 x 448 matrices.
#
# Type is then set at `TYPE_SCALE` times the contract's sizes, because the contract's
# sizes are a statement about the PRINTED page. A 9pt label in a figure reduced to 0.84
# prints at 7.5pt; the same 9pt label in a figure printed at 1.0 would print at 9pt,
# larger than the same label anywhere else in the thesis. `TYPE_SCALE` is that reduction
# factor, so S4's printed type lands exactly where F1's, F2's and F19's does. Every size
# is written relative to a contract constant and none as a literal, so they follow any
# change to the contract. This is S3's arrangement, which sets two sizes one point below
# the contract with the reason stated, at a different factor and for a different reason.
_TEXTWIDTH_IN = 6.37          # `\textwidth`: hscale 0.77 on A4
_TEXTHEIGHT_IN = 9.35         # `\textheight` = 676.04 pt, a rotated figure's printed width
_STANDARD_CANVAS_IN = 7.6     # the canvas width of F1, F2 and F19
FIGURE_WIDTH = _TEXTHEIGHT_IN
TYPE_SCALE = _TEXTWIDTH_IN / _STANDARD_CANVAS_IN


def _type(size: float) -> float:
    """One contract type size, scaled for this figure's rotated full-page placement."""
    return round(size * TYPE_SCALE, 2)


def _panel_label(ax, letter: str, offset_points: tuple) -> None:
    """`style.panel_label`, then the one property this figure has to override: the size.

    The helper takes no size argument and `style.py` is not this session's module to
    change, so the size is set on the artist it has just added rather than by
    reimplementing its placement. The placement therefore stays in one place, and the
    letter prints at the size every other figure's letter prints at.
    """
    style.panel_label(ax, letter, offset_points=offset_points)
    ax.texts[-1].set_fontsize(_type(style.PANEL_LABEL_SIZE))


_PAIR_COUNT = N_NODES * (N_NODES - 1) // 2
_RUNG0_DENSITY = EDGE_COUNT / _PAIR_COUNT
RUNG0_EDGE_SD = float(np.sqrt(_PAIR_COUNT * _RUNG0_DENSITY * (1.0 - _RUNG0_DENSITY)))
RUNG0_TOLERANCE_SIGMA = 5.0


def _family_adjacency(edges, variant, seed, order):
    """One cell of the seven-substrate family, with rung 0's count checked its own way."""
    if variant != "random_gaussian":
        return _adjacency(edges, variant, seed, order)
    rows = edges[(edges.variant == variant) & (edges.seed == seed)]
    band = RUNG0_TOLERANCE_SIGMA * RUNG0_EDGE_SD
    assert abs(len(rows) - EDGE_COUNT) <= band, (
        f"{variant} seed {seed}: {len(rows)} edges, more than "
        f"{RUNG0_TOLERANCE_SIGMA:g} binomial standard deviations from {EDGE_COUNT} "
        f"(band +/-{band:.0f}). Rung 0 matches the density in expectation, so its count "
        "varies by design, but a draw this far out is a broken density.")
    return _dense(rows, order)


def s4_full_substrate_family(ctx):
    """All seven substrates drawn as graphs, under F19's node ordering. Appendix.

    **This figure shows what the substrates look like and makes no comparison among
    them.** It is F19 widened from the ladder's four columns to the whole family, and it
    sits in the appendix for the reason TIER0 3.1(b) gives: three of the seven are not
    rungs of the criticality-matched ladder, that section's scope guard holds, and
    nothing here merges them into a ladder table or recomputes a published quantity
    across the wider set. No spectral quantity is quoted and no statistics strip is
    drawn. The four binary-graph statistics are the ladder's, in `tab:act1-topology`, and
    the three additional rungs' spectra are in `tab:act1-offladder`.

    **One node ordering for all fourteen panels**, F19's: hemisphere, then community,
    then descending connectome degree within community, with the communities detected
    once on the connectome and reused throughout. Separator lines mark the community
    boundaries and the hemisphere split is drawn heavier. The randomised substrates are
    drawn at the representative seed F1's rule picks, through the same `_drawn_seed`, so
    the four columns this figure shares with F19 are the same four matrices.

    **No zoom row.** F19's magnified block is chosen from the connectome's own partition
    and carries an argument about the weight-permuted control. Neither transfers to a
    figure that makes no comparison, so the row is not drawn rather than drawn emptier.

    **All seven weighted panels share one logarithmic colour scale, under one colour
    bar.** Every randomised graph, rung 0 included, takes its weights by drawing with
    replacement from the connectome's own pool, so all seven substrates are non-negative
    and a single positive scale describes every panel. The builder asserts that rather
    than assuming it: an earlier draft of this figure's caption had rung 0 on a diverging
    scale of its own, on the belief that its weights were signed, and the assertion is
    what would catch the belief returning.

    **Rung 0 is the one substrate whose edge count is not 5,323**, matching the density
    in expectation rather than the count, so its check is a band and the other six stay
    exact.

    **Placed full page and rotated a quarter turn**, so its printed width is
    `\textheight` and not `\textwidth`. That is why the canvas is `FIGURE_WIDTH` wide and
    every type size is `TYPE_SCALE` times the contract's; see those constants.
    """
    edges = ctx.frame("substrate_edges_full")
    ordering = ctx.frame("substrate_order").sort_values("position")
    spectra = ctx.frame("spectra_448_full")
    order = ordering.node.to_numpy(int)
    variants = FULL_FAMILY_ORDER

    # The drawn order against the source's own contents. `FULL_FAMILY_ORDER` is a column
    # order held in this module and `substrate_edges_full` is written by a script months
    # apart from it; if the two ever name different substrates, every panel would still
    # render and one of them would be the wrong graph or missing.
    assert set(variants) == set(edges.variant.unique()), (
        f"substrate_edges_full carries {sorted(edges.variant.unique())}, and this figure "
        f"draws {sorted(variants)}. The column order and the source must name the same "
        "seven substrates.")

    weighted = {v: _family_adjacency(edges, v, _drawn_seed(edges, spectra, v), order)
                for v in variants}
    binary = {v: (m > 0) for v, m in weighted.items()}
    degree = {v: b.sum(1) for v, b in binary.items()}

    # **Every substrate here is non-negative**, because at `human_empirical` each
    # randomised graph is painted from the connectome's own weight pool, which has no
    # zero and no negative. One logarithmic scale over all seven panels depends on it,
    # and so does the caption's last clause about the family.
    assert (edges.weight > 0).all(), (
        f"{int((edges.weight <= 0).sum())} edges are not strictly positive. All seven "
        "substrates draw their weights from the connectome's own pool, so the family is "
        "non-negative and one logarithmic colour scale describes every panel; a signed "
        "or zero weight means a variant was built at the wrong condition.")
    assert np.array_equal(degree["connectome"], ordering.degree.to_numpy(int)), (
        "the node ordering's degree column is not the connectome's degree in "
        "substrate_edges_full.parquet: the two sources describe different graphs, so the "
        "permutation applied to every panel is wrong.")
    assert np.array_equal(binary["connectome"], binary["connectome_weight_permuted"]), (
        "the weight-permuted control's binary adjacency is not identical to the "
        "connectome's. Columns one and two of the top row are supposed to be the same "
        "image; a difference is a defect in the permutation, not a finding.")

    block = ordering.hemisphere.to_numpy() * 100 + ordering.community.to_numpy()
    boundaries = np.flatnonzero(block[1:] != block[:-1]) + 1
    hemisphere_cut = np.flatnonzero(
        ordering.hemisphere.to_numpy()[1:] != ordering.hemisphere.to_numpy()[:-1]) + 1

    # ---------------------------------------------------------------- layout
    # Seven equal columns and nothing else, so the colourbar spanning them is exactly as
    # wide as the seven adjacency panels, as it is in F19. The canvas is the printed
    # width, `FIGURE_WIDTH`, for the reason given with that constant.
    fig = plt.figure(figsize=(FIGURE_WIDTH, 3.90))
    outer = fig.add_gridspec(2, 1, height_ratios=[1.0, 0.040], hspace=0.16,
                             left=0.049, right=0.996, top=0.892, bottom=0.062)
    # **Both gaps are wider than F19's 0.10, and the fourteen panel labels are the
    # reason.** F19 has eight labels and four columns; seven columns put fourteen of them
    # in the inter-column and inter-row gaps, and at F19's spacing a gap is narrower than
    # the letter that has to sit in it, so each label lands on the panel above or to its
    # left. The two gaps here are about 11 pt against a letter some 6 pt tall and wide,
    # which puts every label clear of every panel.
    grid = outer[0].subgridspec(3, len(variants), height_ratios=[0.34, 1.0, 1.0],
                                hspace=0.19, wspace=0.15)

    marginals = [fig.add_subplot(grid[0, k]) for k in range(len(variants))]
    binary_axes = [fig.add_subplot(grid[1, k]) for k in range(len(variants))]
    weight_axes = [fig.add_subplot(grid[2, k]) for k in range(len(variants))]
    ax_colourbar = fig.add_subplot(outer[1])

    # ------------------------------------------- top row: binary, with the marginal
    # **One marginal ceiling across all seven.** The degree marginal is a count on the
    # binary graph and is the same measurement in every column, so seven private ceilings
    # would flatten the connectome's tail into Erdos-Renyi's and show the substrates as
    # more alike than they are. F19 shares one ceiling across its four for the same
    # reason and the maximum is the same 69, so the two figures' marginals are drawn at
    # the same scale as well as in the same order.
    degree_ceiling = 1.08 * max(d.max() for d in degree.values())
    for k, variant in enumerate(variants):
        colour = style.VARIANT_COLOUR[variant]
        ax = marginals[k]
        ax.fill_between(np.arange(N_NODES), 0, degree[variant], step="mid",
                        color=colour, lw=0)
        ax.set_xlim(-0.5, N_NODES - 0.5)
        ax.set_ylim(0, degree_ceiling)
        ax.set_xticks([])
        ax.grid(False)
        # The wrapped names, not `VARIANT_TITLE`: seven columns at this width leave about
        # 69pt a column and "Modularity-matching" is wider than that at 9pt. Same names
        # and the same naming scheme as F19's titles, broken over two lines, so the
        # contract's type sizes hold rather than being shaved to fit.
        ax.set_title(style.VARIANT_TITLE_TICK[variant], fontsize=_type(style.TITLE_SIZE),
                     color=colour, pad=3, linespacing=1.0)
        if k:
            ax.set_yticks([])
        else:
            ax.set_yticks([0, 60])
            ax.set_ylabel("degree", fontsize=_type(style.AXIS_LABEL_SIZE - 1))
            ax.tick_params(labelsize=_type(style.TICK_SIZE - 1))

        _draw_matrix(binary_axes[k], binary[variant].astype(float), BINARY_CMAP,
                     None, boundaries, hemisphere_cut)
    binary_axes[0].set_ylabel("binary\nadjacency",
                              fontsize=_type(style.AXIS_LABEL_SIZE - 1), linespacing=1.0)

    # -------------------------------------- bottom row: weighted, one logarithmic scale
    # **One scale across all seven, and one colour bar.** The seven draw from the same
    # weight multiset, the connectome's own: permuted in column two and resampled with
    # replacement in the other five. Seven private scales would make seven different
    # pictures of the same numbers, and a second scale for any one column would invite
    # exactly the comparison this figure does not make.
    positive = np.concatenate([m[m > 0] for m in weighted.values()])
    norm = LogNorm(vmin=float(positive.min()), vmax=float(positive.max()))
    cmap = mpl.colormaps[WEIGHT_CMAP].with_extremes(bad="white")
    for k, variant in enumerate(variants):
        # All seven share `norm` and `cmap`, so the colourbar below can be taken from
        # whichever image the loop ends on: it describes every panel in the row.
        image = _draw_matrix(weight_axes[k], weighted[variant], cmap, norm,
                             boundaries, hemisphere_cut)
    weight_axes[0].set_ylabel("weighted\nadjacency",
                              fontsize=_type(style.AXIS_LABEL_SIZE - 1), linespacing=1.0)

    bar = fig.colorbar(image, cax=ax_colourbar, orientation="horizontal")
    bar.ax.tick_params(labelsize=_type(style.TICK_SIZE - 1))
    bar.outline.set_linewidth(0.4)
    bar.set_label("edge weight (logarithmic), shared by all seven panels",
                  fontsize=_type(style.AXIS_LABEL_SIZE - 1), labelpad=4)
    bar.ax.xaxis.set_label_position("top")
    _keep_ticks_inside(bar, norm)

    # Labels attach as F19's do: the top row's to the marginal above its matrix, the
    # bottom row's to the matrix itself, both at the top-left corner in the gap to the
    # column's left. The offset is a little larger than F19's so the letter sits nearer
    # the middle of the gap than hard against the panel edge. `hspace`, `wspace` and this
    # offset are set together, and were fixed by measuring the drawn figure rather than
    # by eye: every letter's box clears every panel by at least 2.5 pt, the tightest
    # being the 'm', whose glyph is the widest of the fourteen.
    for row, letters in ((marginals, "abcdefg"), (weight_axes, "hijklmn")):
        for ax, letter in zip(row, letters):
            _panel_label(ax, letter, offset_points=(-3, 3))
    return fig

def s3_weight_against_degree_product(ctx):
    """S3 -- mean edge weight against endpoint degree product, connectome and control.

    **The registered prediction, drawn where it fails.** `PREREG_PLACEMENT_MECHANISM.md`
    registered a **positive** correlation between edge weight and the product of the two
    endpoints' binary degrees in the connectome, which is what a weighted rich club would
    put there, and approximately zero in the weight-permuted control. The control half
    holds. The connectome half fails in the opposite direction. `TIER0` 3.14(b) carries
    both correlations, their intervals and the binning rule; this panel is that
    measurement drawn, and it adds no claim to it.

    **Read the frozen bins; nothing here recomputes them.** The twenty equal-count bins
    are cut on the **connectome's** degree products and applied to both substrates, so the
    two series are comparable bin for bin, and the control's degree products are the
    connectome's because the control is the same binary graph. The builder asserts both
    halves of that below.

    **Why the shared mean is drawn.** The permutation holds the weight multiset exactly
    fixed, so the mean over all 5,323 edges is identical for the two substrates to
    4.34e-19. Drawing it once gives the control's scatter a level to be flat about, which
    is what makes "the control shows no trend" something a reader can see rather than
    something the caption asserts. It is one line and it is the same line for both.

    Log x because the bins are equal-count on a heavy-tailed product: on a linear axis
    half the bins pile into the left third of the panel, which is where the connectome's
    fall happens. The rank correlation the caption quotes is invariant to the transform.
    """
    bins = ctx.frame("placement_degree_weight")
    correlation = ctx.frame("placement_rank_correlation").set_index("variant")
    variants = style.ordered_variants(bins.variant.unique())
    per_variant = {v: bins[bins.variant == v].sort_values("bin_index") for v in variants}

    connectome, control = per_variant["connectome"], per_variant["connectome_weight_permuted"]
    # The two substrates are one binary graph, so they are one set of degree products and
    # therefore one set of bin edges. If that ever stops holding, the two series are being
    # read against different x-values and the panel is a comparison of nothing.
    assert np.allclose(connectome.bin_lower.to_numpy(), control.bin_lower.to_numpy()) \
        and np.allclose(connectome.bin_upper.to_numpy(), control.bin_upper.to_numpy()), (
        "the connectome and its weight-permuted control do not share bin edges. The bins "
        "are cut on the connectome's degree products and the control is the same binary "
        "graph, so a difference is a defect in the binning, not a finding.")
    pooled = {v: float(np.average(f.mean_weight, weights=f.n_edges))
              for v, f in per_variant.items()}
    assert abs(pooled["connectome"] - pooled["connectome_weight_permuted"]) < 1e-12, (
        f"the two substrates do not share a mean edge weight: {pooled}. The permutation "
        "holds the weight multiset exactly fixed, so the mean over all edges is the same "
        "number twice; a difference is a defect in the permutation.")

    # Landscape, at the width every other full-width figure in the sweep is built to.
    # The class puts `hscale=0.77` on A4, so \textwidth is 6.37 in and a 7.4 in figure
    # placed at full width prints at 0.86 scale, which is the same scale factor F1, F2
    # and F19 print at: the fonts land at the same size on the page as the rest of the
    # thesis. Twenty x-points and a three-row legend both want the width.
    fig, ax = plt.subplots(figsize=(7.4, 3.4))

    # The shared mean, under the series. Grey and dotted, so it reads as the reference it
    # is rather than as a third substrate, and named in the legend rather than beside the
    # line itself: the band immediately above and below it is the busiest part of the
    # panel, and a label there sits on somebody's uncertainty band at every x tried.
    ax.axhline(pooled["connectome"], color=style.CEILING_COLOUR, lw=0.9, ls=":", zorder=1,
               label="mean over all 5,323 edges, identical for both")

    # The rank correlation goes in the legend beside the series it belongs to. It is the
    # statistic the caption quotes and the one the registered prediction is about, so the
    # panel should carry it rather than making the reader hold two numbers from the
    # caption against two curves. Minus signs in mathtext, so the interval and the rho
    # print the same character.
    #
    # **Both series are drawn SOLID, overriding the contract's dash for the control**, and
    # the uncertainty is a shaded band rather than capped bars. Two dashed-and-capped
    # series crossing each other twenty times read as a thicket; a solid line over a soft
    # band reads as a trend, which is what the panel is about. The colours are untouched,
    # so the substrate encoding is the thesis-wide one, and the redundancy the contract
    # asks for is carried by MARKER SHAPE (circle against square) plus the luminance gap
    # between black and vermillion, which survives greyscale and all three dichromacies.
    for variant, marker in zip(variants, ("o", "s")):
        frame = per_variant[variant]
        row = correlation.loc[variant]
        ax.fill_between(frame.median_degree_product,
                        frame.mean_weight - frame.sem_weight,
                        frame.mean_weight + frame.sem_weight,
                        color=style.VARIANT_COLOUR[variant], alpha=0.15, lw=0, zorder=2)
        ax.plot(frame.median_degree_product, frame.mean_weight, marker=marker, ms=3.6,
                zorder=3,
                **style.variant_kwargs(
                    variant, ls="-",
                    label=(f"{style.VARIANT_LABEL[variant]}:   "
                           rf"$\rho$ = {_signed(row.spearman_rho)}   "
                           f"[{_signed(row.ci_low)}, {_signed(row.ci_high)}]")))

    ax.set_xscale("log")
    ax.set_xlabel("endpoint degree product  (equal-count bin median)",
                  fontsize=style.AXIS_LABEL_SIZE - 1)
    # The band is one standard error of the bin mean and is named on the axis, because the
    # caption's "95% percentile intervals" are the BOOTSTRAP intervals on the two
    # correlations, which are the bracketed pairs in the legend. Two intervals in one
    # panel have to be told apart where each is drawn.
    ax.set_ylabel(r"mean edge weight   (band: $\pm$1 s.e.m.)",
                  fontsize=style.AXIS_LABEL_SIZE - 1)
    ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"{v:.0f}"))
    ax.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
    ax.set_xticks([200, 300, 500, 700, 1000, 1500, 2000])
    ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"{v:.4f}"))

    # Room at the foot of the panel for the three-row legend. The ticks stop at the data,
    # so the reserved band does not read as an empty stretch of the weight axis.
    lowest = float((bins.mean_weight - bins.sem_weight).min())
    highest = float((bins.mean_weight + bins.sem_weight).max())
    span = highest - lowest
    ax.set_ylim(lowest - 0.34 * span, highest + 0.05 * span)
    ax.set_yticks(np.arange(0.0025, 0.00451, 0.0005))
    style.legend(ax, loc="lower left", handlelength=2.4, borderaxespad=0.4,
                 labelspacing=0.32, fontsize=style.LEGEND_SIZE - 1)
    fig.tight_layout()
    return fig


def _signed(value: float) -> str:
    """A signed four-decimal number with a typographic minus, not a hyphen.

    Mathtext would set the same string with binary-operator spacing after the comma of an
    interval, printing "[-0.1507,  - 0.0979]"; plain text with U+2212 sets it as one
    number and matches the minus mathtext gives the rho beside it.
    """
    return f"{value:+.4f}".replace("-", "\u2212")

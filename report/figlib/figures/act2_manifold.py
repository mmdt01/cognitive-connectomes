"""Act II -- the spectrum decomposes the manifold.  Chapter 5.

F4 and F5 are Act II's own claims (the Perron mode is a common mode; sign selects the
basis); F6 carries contribution 6 (PR misses readout-relevant structure).

Owned by session 2 (`report/act2_manifold.md`).

Two conventions this module holds to, both learned from Act I:

* **Aggregate absolutely, then take the median.** `mean_state` is signed with an
  arbitrary sign (`TIER0` §3.12), so `|.|` comes first. The session-0 draft of F4b did
  `.median().abs()` and that inverted the ordering the panel exists to show; see
  `act2_manifold.md` audit item 1.
* **Never mix a median into a per-cell panel.** F6a draws one cell and everything on it
  is that cell's. This is Act I audit item 13, applied before rather than after.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

from report.figlib import style
from report.figlib.figures.common import N_NODES

# Probe 2's supercritical operating point on the all-positive substrate: the grid point
# nearest the connectome's own sr_crit (1 / 0.3249 = 3.078). The other two conditions
# have their own, and F5 reads each from the data rather than naming it here.
ALL_POSITIVE_SR = 3.0526
# sr_crit for the connectome (TIER0 §2.1) -- where F4b starts shading supercritical.
CONNECTOME_SR_CRIT = 3.078
# The k at which TIER0 §3.12's basis-swap table is quoted.
SWAP_K = 10
# The bases, in the order the legends list them.
BASES = ("harmonics", "wmodes", "random")


def _operating_point(alignment, condition, task):
    """Probe 2 captured a canonical and a supercritical point per condition; the
    supercritical one is the larger. Taken from the data so no sigma is hard-coded."""
    sub = alignment[(alignment.condition == condition) & (alignment.task == task)
                    & (alignment.variant == "connectome")]
    return sub[sub.spectral_radius == sub.spectral_radius.max()]


# Captured variance runs over four decades across the k grid, so both axes are
# logarithmic. The floor is DERIVED from the smallest median any panel draws rather than
# fixed: a constant floor silently clipped F5a's W-eigenmode curve, whose first three
# points sit at 1e-4 to 2e-4 -- the very values that panel exists to show.
CAPTURE_TOP = 1.8
CAPTURE_FLOOR_MARGIN = 0.5


def _capture_floor(cells) -> float:
    """The y floor for a set of basis-alignment panels sharing an axis."""
    smallest = min(float(cell.groupby(["basis", "k"]).captured.median().min())
                   for cell in cells)
    return smallest * CAPTURE_FLOOR_MARGIN


def _plot_bases(ax, cell):
    """The three captured-variance curves for one (condition, task, sigma) cell.

    The random band is the **across-seed range** of the per-seed 20-basis mean, not the
    across-basis s.d. within a seed. That is deliberate: the comparison the panel makes
    is paired per seed against the chance *mean*, so the relevant spread is that mean's,
    and it is narrow (0.0014 to 0.0032 at k = 1). The spread of a *single* random
    direction is much wider -- s.d. 0.0029 against a mean of 0.0025 at k = 1, which is
    simply what one direction out of 448 does -- and drawing it would answer a question
    nobody asked while making the band unplottable on a log axis.
    """
    for basis in BASES:
        by_k = cell[cell.basis == basis].groupby("k").captured
        curve = by_k.median()
        ax.plot(curve.index, curve.values, label=style.BASIS_LABEL[basis],
                **style.BASIS_STYLE[basis])
        if basis == "random":
            ax.fill_between(curve.index, by_k.min(), by_k.max(),
                            color=style.BASIS_BAND_COLOUR, alpha=0.20, lw=0)
    ax.set_xscale("log")
    ax.set_yscale("log")


def _captured_at(cell, basis, k):
    return float(cell[(cell.basis == basis) & (cell.k == k)].captured.median())


def _assert_legend_clear(ax, curves, label: str, pad_points: float = 2.0):
    """Assert the rendered legend box covers none of the drawn data.

    Legend placement is a geometric claim *about the data*, and the data moves. Fixing a
    corner by eye and writing a comment about it keeps neither honest: the comment
    survives the change that invalidates it. This measures the legend's bounding box
    after a draw, converts it to data coordinates, and checks every plotted point
    against it -- so a curve that grows into the legend fails the build instead of
    quietly sitting under it. Session 1 settled F1's typography from rendered text
    extents the same way.

    ``curves`` is ``{name: (x, y)}`` for the series actually drawn, passed explicitly
    rather than read off the axes so furniture (the sigma_crit rule, shading) is not
    mistaken for data.
    """
    figure = ax.figure
    figure.canvas.draw()
    legend = ax.get_legend()
    if legend is None:
        return
    box = legend.get_window_extent().expanded(1.0, 1.0)
    corners = ax.transData.inverted().transform(
        [[box.x0 - pad_points, box.y0 - pad_points],
         [box.x1 + pad_points, box.y1 + pad_points]])
    (xlo, ylo), (xhi, yhi) = corners
    offenders = {}
    for name, (xs, ys) in curves.items():
        xs, ys = np.asarray(xs, float), np.asarray(ys, float)
        hit = (xs >= xlo) & (xs <= xhi) & (ys >= ylo) & (ys <= yhi)
        if hit.any():
            offenders[name] = int(hit.sum())
    assert not offenders, (
        f"{label}: the legend box (x {xlo:.2f} to {xhi:.2f}, y {ylo:.3f} to {yhi:.3f}) "
        f"covers drawn data -- {offenders}. Move it, or make room; a legend must not "
        "sit on the curves it names.")


# =============================================================================
# F4 -- the Perron mode is a common mode
# =============================================================================
def f4_perron_carries_the_mean(ctx):
    """The Perron mode carries the mean; the fluctuations it leaves are orthogonal to it.

    (a) After time-centring, the dominant `W` eigenmodes capture *less* than a random
    orthonormal direction out to k = 5 (10/10 seeds), and only reach chance by k = 20.
    (b) The complementary half: the common-mode amplitude, where the connectome is the
    least dominated substrate despite carrying much the largest Perron root.
    """
    alignment = ctx.frame("alignment")
    saturation = ctx.frame("saturation")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9))

    # ---- (a) basis alignment against chance, all-positive substrate, MC.
    cell = _operating_point(alignment, "human_empirical", "mc")
    operating_point = float(cell.spectral_radius.iloc[0])
    assert abs(operating_point - ALL_POSITIVE_SR) < 1e-3, (
        f"F4a expects the all-positive supercritical point {ALL_POSITIVE_SR}, "
        f"got {operating_point}")
    _plot_bases(axes[0], cell)
    axes[0].set_ylim(_capture_floor([cell]), CAPTURE_TOP)
    axes[0].set_xlabel("$k$  (basis vectors, ordered)")
    axes[0].set_ylabel("fraction of time-centred\nstate variance captured")
    axes[0].set_title(f"all-positive substrate, MC, $\\sigma$ = {operating_point:.2f}")
    # Lower right is the one empty corner: the W-mode curve runs along the bottom left
    # and the harmonics curve along the top.
    style.legend(axes[0], loc="lower right", fontsize=style.LEGEND_SIZE - 1)

    # The claim is a shortfall against chance, so assert the direction rather than
    # trusting the eye: the W-modes must sit below the random curve at every k <= 5.
    # Content assertions are skipped on placeholder data, which carries no claim.
    if not ctx.placeholder:
        for k in (1, 2, 3, 5):
            assert _captured_at(cell, "wmodes", k) < _captured_at(cell, "random", k), (
                f"F4a: W-eigenmodes are not below chance at k={k}; the panel's claim "
                "no longer holds and the caption is wrong.")

    # ---- (b) common-mode amplitude across the ladder.
    memory = saturation[(saturation.task == "mc")
                        & (saturation.condition == "human_empirical")]
    endpoints, drawn = {}, {}
    for variant in style.ordered_variants(memory.variant.unique()):
        # |.| BEFORE the median: mean_state is signed with an arbitrary sign, and a
        # signed median does not merely shrink the connectome, it reorders the ladder.
        curve = (memory[memory.variant == variant]
                 .assign(common_mode=lambda frame: frame.mean_state.abs())
                 .groupby("spectral_radius").common_mode.median())
        # All four solid, overriding the contract's per-variant dashes. The four curves
        # are well separated vertically over most of the sweep, so the dashes were
        # encoding a distinction the geometry already makes, and they broke up the two
        # curves that matter most -- the connectome's and the envelope of the nulls it
        # sits below. Colour still carries the identity. See the act file for the
        # greyscale cost this incurs and why it is bounded.
        # `VARIANT_TITLE`'s plain names, not `VARIANT_LABEL`'s rung numbering. Two
        # reasons, and the second is measured. This panel contrasts the substrates
        # themselves rather than their position on the ladder, which is the case F2
        # already established plain names for. And the legend has to fit: at
        # `VARIANT_LABEL` widths the box is 3.85 sigma-units across -- two thirds of the
        # panel -- and there is nowhere inside the axes it does not cover a curve.
        axes[1].plot(curve.index, curve.values,
                     **style.variant_kwargs(variant, ls="-",
                                            label=style.VARIANT_TITLE[variant]))
        endpoints[variant] = float(curve.iloc[-1])
        drawn[variant] = (curve.index.to_numpy(), curve.to_numpy())
    axes[1].set_xlabel(r"nominal $\sigma$")
    axes[1].set_ylabel("common-mode amplitude")
    axes[1].set_ylim(0, 1.05)
    axes[1].set_xlim(float(memory.spectral_radius.min()),
                     float(memory.spectral_radius.max()))
    style.shade_supercritical(axes[1], CONNECTOME_SR_CRIT)
    axes[1].axvline(CONNECTOME_SR_CRIT, color=style.CEILING_COLOUR, lw=0.8, ls=":")
    # Rotated hard against its own rule, which costs almost no width -- the same idiom
    # F6b uses for the d_eff ceiling. The label is short because the lower-right box is
    # now the legend's, and the full name goes in the caption.
    axes[1].text(CONNECTOME_SR_CRIT, 0.03, r" $\sigma_{\rm crit}$",
                 transform=axes[1].get_xaxis_transform(), fontsize=style.TICK_SIZE,
                 color=style.CEILING_COLOUR, va="bottom", ha="left", rotation=90)
    # Lower right, measured rather than judged. Two regions of this panel are genuinely
    # empty: the strip below sigma = 1.35 (every curve under 0.002, but far too narrow
    # for these labels) and the box right of sigma = 3.2 below 0.373, where the
    # connectome runs lowest. The legend takes the second. `_assert_legend_clear` below
    # checks the rendered box against the drawn data rather than trusting this comment.
    style.legend(axes[1], loc="lower right", fontsize=style.LEGEND_SIZE - 1)

    # The whole point of (b) is that the connectome sits lowest. If it ever does not,
    # the figure argues the opposite of its caption -- which is exactly what the
    # session-0 signed-median aggregation did.
    if not ctx.placeholder:
        assert endpoints["connectome"] == min(endpoints.values()), (
            f"F4b: the connectome is not the least common-mode dominated substrate at "
            f"the top of the sweep: {endpoints}. Check the |.|-before-median step.")

    for ax, letter in zip(axes, "ab"):
        style.panel_label(ax, letter)
    fig.tight_layout()
    # After tight_layout, so the box measured is the one that ships. Frozen data only:
    # the placeholder curves have a different shape and would occupy a different corner,
    # which is a fact about the placeholder and not a defect in the figure.
    if not ctx.placeholder:
        _assert_legend_clear(axes[1], drawn, "F4b")
    return fig


# =============================================================================
# F5 -- sign composition selects the basis
# =============================================================================
def f5_sign_selects_the_basis(ctx):
    """Which structural basis the fluctuations occupy is set by the weight signs.

    Three conditions, each at its own supercritical operating point. The claim is the
    **swap** in which basis leads, not the amount either captures: on the all-positive
    substrate neither captures much (`TIER0` §3.12).
    """
    alignment = ctx.frame("alignment")
    task = "lorenz"
    conditions = [c for c in ("human_empirical", "human_empirical_signed",
                              "human_gaussian") if c in set(alignment.condition)]
    fig, axes = plt.subplots(1, len(conditions), figsize=(7.6, 2.8), sharey=True)
    axes = np.atleast_1d(axes)

    cells = [_operating_point(alignment, c, task) for c in conditions]
    leaders = {}
    for ax, condition, cell in zip(axes, conditions, cells):
        operating_point = float(cell.spectral_radius.iloc[0])
        _plot_bases(ax, cell)
        ax.set_title(f"{style.CONDITION_LABEL.get(condition, condition)}\n"
                     f"$\\sigma$ = {operating_point:.2f}", fontsize=style.TITLE_SIZE - 1)

        # Mark the k the swap table is quoted at, and give the two values there. The
        # comparison the figure exists to make therefore sits on the figure and not only
        # in the caption.
        harmonics = _captured_at(cell, "harmonics", SWAP_K)
        wmodes = _captured_at(cell, "wmodes", SWAP_K)
        leaders[condition] = "harmonics" if harmonics > wmodes else "wmodes"
        ax.axvline(SWAP_K, color=style.ANNOTATION_COLOUR, lw=0.7, ls=":", zorder=1)
        for value, marker in ((harmonics, "o"), (wmodes, "s")):
            ax.plot([SWAP_K], [value], marker=marker, ms=5.5, mfc="white",
                    mec=style.ANNOTATION_COLOUR, mew=1.0, zorder=4)
        # The numbers go in the bottom-right corner rather than beside their markers.
        # Every curve converges on 1.0 by k = N, so that corner is empty in all three
        # panels, while the space beside a marker is on a steeply rising curve in at
        # least one of them -- and a label that clears the curve in panel (a) lands on
        # it in panel (b).
        ax.text(0.97, 0.04,
                f"at $k$ = {SWAP_K}\nharmonics   {harmonics:.3f}\n"
                f"$W$-modes   {wmodes:.3f}",
                transform=ax.transAxes, ha="right", va="bottom",
                fontsize=style.TICK_SIZE - 1, linespacing=1.35, zorder=5)

    floor = _capture_floor(cells)
    for ax in axes:
        ax.set_ylim(floor, CAPTURE_TOP)
    axes[0].set_ylabel("fraction of time-centred\nstate variance captured")
    # One x label under the middle panel and one figure-level legend below, rather than
    # three copies of each: at this panel width an in-panel legend collides with the
    # k = 10 annotations it sits beside. F2's treatment, for the same reason.
    axes[len(axes) // 2].set_xlabel("$k$  (basis vectors, ordered)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=len(BASES),
               bbox_to_anchor=(0.5, -0.04), fontsize=style.LEGEND_SIZE)
    for ax, letter in zip(axes, "abc"):
        style.panel_label(ax, letter, dx=-0.10)

    # The swap IS the claim: harmonics ahead only where the weights are non-negative.
    if not ctx.placeholder:
        assert leaders.get("human_empirical") == "harmonics", (
            f"F5: harmonics should lead on the all-positive substrate, got {leaders}")
        assert all(leaders[c] == "wmodes"
                   for c in conditions if c != "human_empirical"), (
            f"F5: W-eigenmodes should lead wherever signs are balanced, got {leaders}")

    fig.tight_layout()
    return fig


# =============================================================================
# F6 -- variance-weighted dimensionality misses readout-relevant structure
# =============================================================================
def _per_direction_weights(spectra):
    """The two measures as what they exactly are: sums of per-direction weights.

    `d_eff = sum_i g_i / (g_i + alpha)` over the design-Gram spectrum, and
    `PR = sum_i p_i / sum_j p_j^2` with `p = lambda / sum(lambda)` over the covariance
    spectrum -- the second identity because
    `sum_i p_i / sum_j p_j^2 = 1 / sum_j p_j^2 = PR`. Both sums are exact, so the area
    under each curve in F6a *is* the number that panel names.
    """
    gram = spectra.eig_gram.to_numpy(float)
    alpha = float(spectra.alpha.iloc[0])
    ridge_weight = gram / (gram + alpha)

    eig = spectra.eig_cov.to_numpy(float)
    p = eig / eig.sum()
    variance_weight = p / (p ** 2).sum()
    return ridge_weight, variance_weight


def f6_pr_misses_readout_structure(ctx):
    """Two ways of counting how many directions the activity uses, on the same data.

    (a) is the mechanism and carries the figure: both measures are sums of a weight per
    direction, so each curve's area is its own count. The ridge weight is ~1 for some
    four hundred directions; the variance weight has collapsed by the fifth. (b) and (c)
    are the consequence -- only one of the two counts tracks measured memory.
    """
    spectra = ctx.frame("gram_spectra")
    probe3 = ctx.frame("probe3")
    # Panel widths 40 : 30 : 30, and the two gaps set independently. A plain
    # `subplots(1, 3)` has a single `wspace`, so the b|c gap cannot be tightened without
    # also tightening a|b; the spacer columns below buy that control. The gaps are not
    # symmetric because they carry different furniture: a|b must clear panel b's y label
    # *and* its tick labels, while b|c carries neither -- (c) shares (b)'s y axis and
    # draws no tick labels -- so closing it to a sliver is what makes the shared axis
    # read as shared rather than as two unrelated panels that happen to sit side by side.
    fig = plt.figure(figsize=(7.8, 3.0))
    grid = fig.add_gridspec(1, 5, width_ratios=[40, 11, 30, 3, 30], wspace=0.0)
    axes = [fig.add_subplot(grid[0, 0]), fig.add_subplot(grid[0, 2])]
    axes.append(fig.add_subplot(grid[0, 4], sharey=axes[1]))

    # ---- (a) the mechanism, on ONE cell. Nothing median is drawn here.
    ridge_weight, variance_weight = _per_direction_weights(spectra)
    rank = spectra["rank"].to_numpy()
    d_eff, pr = ridge_weight.sum(), variance_weight.sum()

    # The two fills overlap -- the variance weight lives entirely inside the ridge
    # weight's footprint -- so they are separated by opacity rather than by hue: the
    # ridge area is a pale wash and the variance area is solid, which keeps its sliver
    # visible against the wash instead of vanishing into it.
    def draw_weights(ax):
        for weight, key, label, alpha in (
                (ridge_weight, "d_eff", r"ridge weight $g_i/(g_i+\alpha)$", 0.13),
                (variance_weight, "pr", r"variance weight $p_i/\sum_j p_j^2$", 0.60)):
            ax.fill_between(rank, 0, weight, step="mid", zorder=2,
                            color=style.MEASURE_FILL[key], alpha=alpha, lw=0)
            ax.step(rank, weight, where="mid", label=label, zorder=3,
                    **style.MEASURE_STYLE[key])

    draw_weights(axes[0])
    axes[0].set_xlim(0, N_NODES)
    axes[0].set_ylim(0, 1.35)
    axes[0].set_xlabel("direction $i$  (ordered, largest first)")
    axes[0].set_ylabel("weight the measure\ngives direction $i$")
    # "one cell", not "Connectome, MC, sigma = 3.05". The substrate and task are the
    # whole figure's and are in the caption; what this title has to carry is the one
    # thing a reader cannot recover from the panel -- that (a) is a SINGLE reservoir
    # while (b, c) are medians over fifty. The two disagree visibly (431 here, 413 in
    # (b), same substrate), so the caveat belongs in the figure and not only in a caption
    # that may be trimmed. A more descriptive title was tried and reverted for exactly
    # this reason; see the act file's F6 block.
    axes[0].set_title("one connectome cell", fontsize=style.TITLE_SIZE)
    axes[0].annotate(f"area = $d_{{\\rm eff}}$ = {d_eff:.0f}", xy=(0.26, 0.80),
                     xycoords="axes fraction", fontsize=style.TICK_SIZE,
                     color=style.MEASURE_FILL["d_eff"], zorder=5)

    # The variance weight has collapsed by the fifth direction, so at the scale that
    # shows d_eff's four hundred it is a sliver a pixel wide -- which reads as a missing
    # curve, not a small one. The inset is the same two quantities over the first twelve
    # directions on the same linear axes, so "area is the measure" still holds inside it
    # and PR's entire mass is visible where it actually lives. No zoom connectors: the
    # region being magnified sits on the y axis, so they would sweep across the panel to
    # point at its own left-hand edge.
    inset = axes[0].inset_axes([0.36, 0.15, 0.58, 0.42])
    draw_weights(inset)
    inset.set_xlim(0.5, 12.5)
    inset.set_ylim(0, 1.42)
    inset.set_xticks([1, 5, 10])
    inset.set_yticks([0, 1])
    inset.tick_params(labelsize=style.TICK_SIZE - 2)
    inset.grid(False)
    inset.set_facecolor("white")
    inset.patch.set_alpha(0.95)
    for spine in inset.spines.values():          # rcParams drop top/right; a zoom needs
        spine.set_visible(True)                  # a closed box to read as an inset
        spine.set_linewidth(0.6)
    inset.text(0.96, 0.94, f"PR = {pr:.2f}", transform=inset.transAxes,
               ha="right", va="top", fontsize=style.TICK_SIZE - 1)

    # The identity is the panel's whole licence. Check it against the frozen scalars.
    frozen = probe3[(probe3.variant == spectra.variant.iloc[0])
                    & (probe3.seed == int(spectra.seed.iloc[0]))
                    & np.isclose(probe3.spectral_radius,
                                 float(spectra.spectral_radius.iloc[0]))]
    assert len(frozen) == 1, f"F6a: expected one frozen cell, found {len(frozen)}"
    assert abs(d_eff - float(frozen.d_eff.iloc[0])) < 1e-3, (
        f"F6a: area under the ridge weight ({d_eff:.5f}) is not the frozen d_eff "
        f"({float(frozen.d_eff.iloc[0]):.5f}); the panel's 'area = the measure' "
        "reading is void.")
    assert abs(pr - float(frozen.pr.iloc[0])) < 1e-3, (
        f"F6a: area under the variance weight ({pr:.5f}) is not the frozen PR "
        f"({float(frozen.pr.iloc[0]):.5f}).")

    # ---- (b), (c) the consequence: per-variant medians against measured MC.
    medians = probe3.groupby("variant")[["d_eff", "pr", "mc"]].median()
    panels = ((axes[1], "d_eff", r"$d_{\rm eff}$   (ridge effective rank)"),
              (axes[2], "pr", "PR   (participation ratio)"))
    for ax, column, label in panels:
        for variant in style.ordered_variants(medians.index):
            row = medians.loc[variant]
            # Plain names, matching F4b and Act I's F2. Here it is more than
            # consistency: `VARIANT_LABEL` numbers the substrates by **rung index**, and
            # the rung index is precisely the variable this figure must not be read
            # against -- correlating against it gives -0.18 and -0.54 rather than the
            # +1.000 and +0.107 the panels report, which is why `TIER0` §3.12 flags it as
            # the number not to quote. Printing a rung number beside every point invites
            # exactly that misreading.
            ax.scatter(row[column], row.mc, s=44, zorder=3,
                       color=style.VARIANT_COLOUR.get(variant, "0.4"),
                       edgecolor="white", linewidth=0.6,
                       label=style.VARIANT_TITLE.get(variant, variant))
        rho = spearmanr(medians[column], medians.mc).statistic
        # Both x axes are zero-based, so the horizontal spread of the seven points is
        # directly comparable between the panels: that comparison IS the
        # 5.5-fold-against-16% claim, and an axis crop would hide it. Same reasoning as
        # F2's zero-based bars.
        ax.set_xlim(0, medians[column].max() * 1.12)
        ax.set_xlabel(label)
        ax.set_title(f"ladder $r_s$ = {rho:+.2f}", fontsize=style.TITLE_SIZE)
        ax.set_ylim(0, medians.mc.max() * 1.15)
    axes[1].set_ylabel("memory capacity (MC)")
    # `sharey` already ties the limits; this drops the duplicate tick labels so the two
    # panels read as one axis rather than two that happen to agree.
    axes[2].tick_params(labelleft=False)
    # CONVENTIONS: the ceiling on every memory figure. It is on x here, and it also sets
    # panel b's limit -- a count of directions is read against the ambient dimension.
    axes[1].set_xlim(0, N_NODES * 1.12)
    style.draw_ceiling(axes[1], N_NODES, on="x")
    # PR's whole range is 1.19 to 1.38, so without explicit ticks the panel shows one
    # labelled gridline and the cluster reads as a plotting failure rather than a result.
    axes[2].set_xticks([0.0, 0.5, 1.0, 1.5])

    # Two figure-level legends under the panels -- measures for (a), substrates for
    # (b, c) -- so neither sits over the data. F2's treatment.
    measure_handles, measure_labels = axes[0].get_legend_handles_labels()
    variant_handles, variant_labels = axes[1].get_legend_handles_labels()
    fig.legend(measure_handles, measure_labels, loc="lower left", ncol=1,
               bbox_to_anchor=(0.02, -0.20), fontsize=style.LEGEND_SIZE)
    fig.legend(variant_handles, variant_labels, loc="lower right", ncol=3,
               bbox_to_anchor=(0.99, -0.22), fontsize=style.LEGEND_SIZE - 1)

    for ax, letter in zip(axes, "abc"):
        style.panel_label(ax, letter)
    fig.tight_layout()
    return fig

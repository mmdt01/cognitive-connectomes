"""Act II -- the spectrum decomposes the manifold.  Chapter 5.

F4 and F5 are Act II's own claims (the Perron mode is a common mode; sign selects the
basis); F6 carries contribution 6 (PR misses readout-relevant structure). F20 opens the
chapter and carries no claim at all: it defines the object the chapter then measures.

Owned by session 2 (`report/act2_manifold.md`).

Two conventions this module holds to, both learned from Act I:

* **Aggregate absolutely, then take the median.** `mean_state` is signed with an
  arbitrary sign (`TIER0` §3.12), so `|.|` comes first. The session-0 draft of F4b did
  `.median().abs()` and that inverted the ordering the panel exists to show; see
  `act2_manifold.md` audit item 1.
* **Never mix a median into a per-cell panel.** F6a draws one cell and everything on it
  is that cell's. This is Act I audit item 13, applied before rather than after.

**F20 is the one figure in the sweep that re-runs a reservoir rather than reading a
frozen artifact**, because `CONVENTIONS` working rule 5 forbids persisting state
matrices and F20 draws one. The re-run is the evaluators' opt-in `collect_states` path,
it costs 0.3 s, it writes nothing, and `act2_manifold.md` §2.7 is the reproduction gate
that licenses it -- eigenvalues of `A^T A` from the re-run against the frozen
`eig_gram`, worst relative deviation 3.4e-07 over the 438 directions above the ridge
floor. The builder re-asserts a cheaper form of that gate on every build.
"""

from types import SimpleNamespace

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
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

# --------------------------------------------------------------- F18, the ridge floor
# TIER0 §3.6's supercritical cut, applied by F18a. The probe capture's grid steps
# unevenly, and >= 3.05 selects five points from 3.0526 up.
FLOOR_SUPERCRITICAL_SR = 3.05
# Where F18b's argmin window starts: past the low-sigma limb, which every variant is on
# by 1.2632. The window exists because floor sensitivity vanishes at BOTH ends of the
# spectrum -- a dead reservoir has almost nothing above the floor to lose -- so the
# minimum the claim is about is the interior dip between the two humps and not the
# global minimum, which for every variant is sigma = 0.
# See `report/checks/floor_sensitivity_check.md` §3.2.
FLOOR_INTERIOR_FROM_SR = 1.2632
# TIER0 §3.6's published supercritical medians, which F18 asserts against.
PUBLISHED_FLOOR_SENSITIVITY = {"connectome": 8.85, "connectome_weight_permuted": 18.09,
                               "degree_rewire": 17.75, "erdos_renyi": 10.26}
# The interior argmin the check file reproduces per variant. The connectome's is a
# single grid point; each null's is one of two adjacent ones, which is where the
# per-seed split sits (7/3, 7/3 and 5/5 over ten seeds).
PUBLISHED_INTERIOR_ARGMIN = {"connectome": (3.5789,),
                             "connectome_weight_permuted": (1.5789, 2.0),
                             "degree_rewire": (1.5789, 2.0),
                             "erdos_renyi": (1.5789, 2.0)}
# F18a's four position bins, top of the panel first. Labelled in maths rather than in
# prose because the bins ARE the inequalities: "more than a decade below the floor" is
# four words for `g_i <= alpha/10` and reads less exactly. The caption gives the words.
FLOOR_BINS = (("n_far_above", r"$g_i \geq 10\alpha$"),
              ("n_within_decade", r"$\alpha/10 < g_i < 10\alpha$"),
              ("n_far_below", r"$0 < g_i \leq \alpha/10$"),
              ("n_zero", r"$g_i = 0$"))


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


# =============================================================================
# F18 -- the Gram spectrum against the ridge floor
# =============================================================================
def _floor_sensitivity_curves(floor):
    """Seed-median floor sensitivity against sigma, per variant, over the WHOLE grid.

    No sigma filter: the panel has to show the curve falling to zero at sigma = 0, or
    the interior dip it marks reads as a global minimum, which it is not.
    """
    return {variant: (floor[floor.variant == variant]
                      .groupby("spectral_radius").floor_sensitivity.median())
            for variant in style.ordered_variants(floor.variant.unique())}


def _interior_minimum(curve):
    """The dip between the two humps: the argmin taken past the low-sigma limb."""
    interior = curve[curve.index >= FLOOR_INTERIOR_FROM_SR]
    return float(interior.idxmin()), float(interior.min())


def f18_gram_spectrum_against_the_floor(ctx):
    """Where each substrate's design-Gram spectrum sits relative to the ridge floor.

    (a) is the claim: the connectome holds almost all of its directions well clear of
    the floor while Erdos-Renyi has already lost most of its own, which is what the two
    `d_eff` values in the legend are counting. (b) puts the same quantity on the
    operating axis, and (c) shows the measured ridge optimum landing on each substrate's
    own interior dip.
    """
    floor = ctx.frame("floor_mass")
    peaks = ctx.frame("alpha_peaks")
    variants = style.ordered_variants(floor.variant.unique())

    # ---- structural assertions: true of the arithmetic, so they run on both paths.
    binned = floor[[column for column, _ in FLOOR_BINS]].sum(axis=1)
    assert (binned == floor.n_directions).all(), (
        "F18a: the four position bins do not partition the spectrum. They are the "
        "complement of `n_within_decade` taken at the same boundaries, so a cell whose "
        "bins do not sum to n_directions means a mode has been double counted or lost, "
        f"and the panel's percentages are meaningless. Worst cell off by "
        f"{int((binned - floor.n_directions).abs().max())}.")
    assert (floor.floor_sensitivity >= 0).all(), (
        "F18b: floor sensitivity is a sum of non-negative terms and cannot be negative.")
    grid = sorted(floor.spectral_radius.unique())
    assert grid[0] == 0.0, (
        f"F18b draws the whole sigma curve and its caption rests on the curve reaching "
        f"zero at sigma = 0, but the lowest radius present is {grid[0]}. Check the "
        "`floor_mass` source has not acquired a sigma filter at load.")
    assert len(peaks) == len(variants) * peaks.alpha.nunique(), (
        f"F18c: expected one peak per (alpha, variant), got {len(peaks)} rows for "
        f"{peaks.alpha.nunique()} alpha and {len(variants)} variants.")

    # Widths 36 : 38 : 26. (a) carries four long maths tick labels and four bars per
    # group; (b) is the only panel with thirteen x points and needs the room to keep the
    # two humps apart; (c) is five points and a legend-free axis, so it gives width up.
    #
    # The gap is left to `tight_layout` rather than set on the gridspec, unlike F6. F6
    # needs two DIFFERENT gaps because its (b) and (c) share a y axis and the gap between
    # them carries no furniture, which a single `wspace` cannot express; here all three
    # panels carry their own y label and tick labels, so one symmetric gap is right, and
    # an explicit `wspace` would only be overridden by `tight_layout` with a warning.
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 3.1),
                             gridspec_kw=dict(width_ratios=[36, 38, 26]))
    axes = list(axes)

    # ---- (a) where the spectrum sits, supercritically.
    #
    # GROUPED bars, not stacked, and the reason is arithmetic rather than taste. The
    # bars are per-bin medians over the 50 supercritical cells, and four medians taken
    # separately are not constrained to sum to their own total (the connectome's four
    # come to 102.1%). A stacked bar would assert a sum that is not there; grouped bars
    # assert nothing of the kind, and the exactness that IS true -- the bins partition
    # every individual cell -- is asserted above instead of drawn.
    supercritical = floor[floor.spectral_radius >= FLOOR_SUPERCRITICAL_SR]
    positions = np.arange(len(FLOOR_BINS))[::-1]     # first bin at the TOP of the panel
    bar_height = 0.78 / len(variants)
    d_eff_median = {}
    for index, variant in enumerate(variants):
        cells = supercritical[supercritical.variant == variant]
        d_eff_median[variant] = float(cells.d_eff.median())
        shares = [100.0 * float((cells[column] / cells.n_directions).median())
                  for column, _ in FLOOR_BINS]
        offset = (index - (len(variants) - 1) / 2) * bar_height
        # `d_eff` rides in the legend label rather than sitting beside a bar. It is a
        # property of the whole spectrum, not of any one bin, and annotating it against
        # the top bin would read as an identity: the connectome's 398.5 directions more
        # than a decade clear are close to its d_eff of 413 but are not it.
        axes[0].barh(positions - offset, shares, height=bar_height * 0.92,
                     color=style.VARIANT_COLOUR[variant], zorder=3,
                     edgecolor="white", linewidth=0.4,
                     label=f"{style.VARIANT_TITLE[variant]}  "
                           f"($d_{{\\rm eff}}$ = {d_eff_median[variant]:.0f})")
    axes[0].set_yticks(positions)
    axes[0].set_yticklabels([label for _, label in FLOOR_BINS])
    axes[0].set_xlabel("% of the 448 directions")
    axes[0].set_xlim(0, 100)
    axes[0].set_ylim(positions.min() - 0.6, positions.max() + 0.6)
    axes[0].grid(axis="y", visible=False)
    # The title names the OBJECT as well as the filter. Nothing else on the panel says
    # what `g_i` is, and the whole figure turns on its being the Gram the ridge solver
    # inverts rather than the covariance PR is taken on.
    axes[0].set_title(r"design-Gram spectrum, $\sigma \geq 3.05$",
                      fontsize=style.TITLE_SIZE)

    # ---- (b) the same quantity along the operating axis, whole curve.
    curves = _floor_sensitivity_curves(floor)
    interior = {}
    for variant in variants:
        curve = curves[variant]
        axes[1].plot(curve.index, curve.values,
                     **style.variant_kwargs(variant, label="_nolegend_"))
        argmin_sr, minimum = _interior_minimum(curve)
        interior[variant] = (argmin_sr, minimum)
        axes[1].plot([argmin_sr], [minimum], ls="none", marker="v", ms=6.5, mfc="white",
                     mec=style.VARIANT_COLOUR[variant], mew=1.4, zorder=6)
    # The excluded limb is shaded rather than cropped away. Cropping would hide the one
    # fact that stops the marked dips being read as global minima.
    axes[1].axvspan(0, FLOOR_INTERIOR_FROM_SR, color=style.CEILING_COLOUR, alpha=0.10,
                    zorder=0, lw=0)
    # The label runs up the LEFT edge of the shaded strip, not its right edge: every
    # curve is still near zero at sigma = 0.13 and all four peak against the strip's
    # right edge, so a label there sits on the tallest thing in the panel. Measured on
    # the first render, which had it exactly there.
    axes[1].text(0.13, 0.97, r"low-$\sigma$ limb",
                 transform=axes[1].get_xaxis_transform(), ha="center", va="top",
                 rotation=90, fontsize=style.TICK_SIZE - 2, color=style.CEILING_COLOUR)
    axes[1].set_xlabel(r"nominal $\sigma$   (probe grid)")
    axes[1].set_ylabel("floor sensitivity\n"
                       r"$-\,\mathrm{d}d_{\rm eff}/\mathrm{d}\log\alpha$")
    axes[1].set_xlim(0, float(max(grid)))
    axes[1].set_ylim(0, None)
    # An OPEN triangle, matching the markers. A filled glyph here would name a marker the
    # panel does not draw.
    axes[1].set_title(r"$\triangledown$ interior minimum", fontsize=style.TITLE_SIZE)

    # ---- (c) the measured ridge optimum against alpha, with (b)'s dips as rules.
    # The three nulls' optima are IDENTICAL at every alpha, so their curves superimpose
    # exactly and the panel would appear to draw two substrates rather than four. The
    # marker shrinks down the legend order so the coincident points nest concentrically
    # and all three remain visible. Nothing is offset: an offset would draw a
    # disagreement that is not in the data, which is the one thing this panel must not do.
    for index, variant in enumerate(variants):
        axes[2].axhline(interior[variant][0], color=style.VARIANT_COLOUR[variant],
                        lw=0.8, ls=":", alpha=0.55, zorder=1)
        sub = peaks[peaks.variant == variant].sort_values("alpha")
        axes[2].plot(sub.alpha, sub.peak_spectral_radius, marker="o",
                     ms=6.6 - 0.9 * index, zorder=3 + index,
                     **style.variant_kwargs(variant, label="_nolegend_"))
    axes[2].set_xscale("log")
    axes[2].set_xlim(4e-9, 3e-3)
    axes[2].set_xticks([1e-8, 1e-6, 1e-4])
    axes[2].set_xlabel(r"ridge $\alpha$")
    axes[2].set_ylabel(r"ridge-optimal $\sigma$   (Task B grid)")
    axes[2].set_title("dotted: (b)'s dip", fontsize=style.TITLE_SIZE)

    # One figure-level legend for all three panels: (a)'s labels carry the `d_eff`
    # values as well as the substrate names, so they are far too wide for any in-panel
    # box, and (b) and (c) name the same four substrates. F2's treatment, F2's reason.
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=len(variants),
               bbox_to_anchor=(0.5, -0.05), fontsize=style.LEGEND_SIZE - 1)

    # ---- content assertions: claims about the frozen result, so frozen data only.
    if not ctx.placeholder:
        for variant, published in PUBLISHED_FLOOR_SENSITIVITY.items():
            measured = float(supercritical[supercritical.variant == variant]
                             .floor_sensitivity.median())
            assert abs(measured - published) < 0.01, (
                f"F18: supercritical median floor sensitivity for {variant} is "
                f"{measured:.4f} against TIER0 §3.6's {published}. The figure no longer "
                "reproduces the table it is captioned with.")
        for variant, allowed in PUBLISHED_INTERIOR_ARGMIN.items():
            argmin_sr = interior[variant][0]
            assert any(abs(argmin_sr - value) < 1e-3 for value in allowed), (
                f"F18b: {variant}'s interior minimum sits at sigma = {argmin_sr}, not at "
                f"{allowed}. The panel's whole point is that the connectome's dip is at "
                "3.58 and every null's at 1.58 or 2.00.")
        # The honesty clause of the caption, checked rather than trusted: these are
        # INTERIOR minima. Every curve is lower at sigma = 0 than at its own dip, and
        # the connectome is already lower at the first non-zero grid point.
        for variant in variants:
            curve = curves[variant]
            assert float(curve.loc[0.0]) < interior[variant][1], (
                f"F18b: {variant}'s sensitivity at sigma = 0 is not below its interior "
                "minimum, so 'interior' has stopped meaning anything and the caption's "
                "qualification is wrong.")
        connectome_first = float(curves["connectome"].iloc[1])
        assert connectome_first < interior["connectome"][1], (
            f"F18b: the connectome's sensitivity at the first non-zero radius "
            f"({connectome_first:.3f}) is no longer below its interior minimum "
            f"({interior['connectome'][1]:.3f}); the caption says it is.")
        migration = peaks.sort_values("alpha").groupby("variant").peak_spectral_radius
        assert migration.last()["connectome"] > migration.first()["connectome"], (
            "F18c: the connectome's ridge-optimal sigma no longer rises with alpha, "
            "which is the migration the panel exists to show.")

    for ax, letter in zip(axes, "abc"):
        style.panel_label(ax, letter)
    fig.tight_layout()
    return fig


# =============================================================================
# F20 -- from a driven network to a Gram spectrum
# =============================================================================
# **The cell is F6a's cell, and it is taken from F6a's own source rather than
# re-derived.** `gram_spectra` already applies the selection rule -- the connectome at
# the supercritical operating point, MC, all-positive, and the one seed whose `d_eff` is
# nearest the median of the ten -- and returns the resolved seed in a column. Copying
# that rule into a second place is how two figures captioned as "the same cell" quietly
# come apart, so nothing below re-implements it.
F20_SEED = 7                      # what the rule resolves to. ASSERTED, never selected on.
F20_WINDOW = 200                  # timesteps drawn in (b) and (c)
F20_UNIT_PERCENTILES = (0.10, 0.50, 0.90)
# The trace split measured in `act2_manifold.md` §2.7, unrounded. The caption quotes
# 51.3%; this is the number it is rounded from and the builder asserts the render
# against it, so the caption cannot outlive the datum.
F20_RANK_ONE_TRACE_FRACTION = 0.513185
# `leak_rate` is 1.0 for every task here, so the state is exactly `tanh(.)` and lives in
# (-1, 1). Panels (b), (c) and (d) therefore all use the same [-1, 1] box: it is the
# activity's own bound rather than a choice, it is shared across the three panels by
# construction, and it is what lets (b) and (c) sit on one vertical scale without either
# being cropped. It is also every entry of (e) divided by T_eff -- see F20_GRAM_LIMIT.
F20_ACTIVITY_LIMIT = 1.0
# One diverging map for every signed quantity in the figure -- the state matrix in (a)
# and the three Gram matrices in (e) -- so a reader learns the encoding once. Not a
# substrate, basis, regime or unit colour: a heatmap scale is its own channel, and this
# figure draws no substrate comparison for it to be confused with.
F20_SIGNED_CMAP = "RdBu_r"
# The linear window around zero for panel (e)'s symmetric-log scale. Set below the
# median |entry| of the smallest of the three matrices (83) so that every one of them
# is drawn on the logarithmic part rather than half-flattened into the linear core.
F20_GRAM_LINTHRESH = 20.0


def _f20_units(edges):
    """The three highlighted units, by the rule the caption states.

    Node strength on the connectome -- the sum of the weights on a node's edges -- at the
    10th, 50th and 90th percentiles, nearest-rank, ordered ascending with ties broken on
    the lowest node index. **On this substrate all 448 strengths are distinct, so the tie
    rule never binds**; it is stated because a rule with an unresolved tie is not a rule,
    not because it does any work here.

    Read off `substrate_edges`, which is F19's own frozen edge list, rather than off a
    live substrate load: the selection is then reproducible from an artifact, and the
    units are chosen on the same graph the node ordering and panel (e) are drawn under.
    The variant is filtered explicitly rather than taken from `edges.variant.unique()`,
    which is the trap `FIGURE_LIST`'s S4 note records against F19.
    """
    connectome = edges[edges.variant == "connectome"]
    connectome = connectome[connectome.seed == connectome.seed.min()]
    strength = np.zeros(N_NODES)
    weight = connectome.weight.to_numpy(float)
    np.add.at(strength, connectome.i.to_numpy(int), weight)
    np.add.at(strength, connectome.j.to_numpy(int), weight)
    assert np.unique(strength).size == N_NODES, (
        f"node strength is not unique across the {N_NODES} nodes "
        f"({np.unique(strength).size} distinct values), so the 'ties broken on the "
        "lowest node index' clause of the caption is now load-bearing rather than "
        "vacuous. Check the caption still describes what the rule does.")
    order = np.lexsort((np.arange(N_NODES), strength))
    units = [int(order[int(round(q * (N_NODES - 1)))]) for q in F20_UNIT_PERCENTILES]
    assert len(set(units)) == 3, f"the three percentiles collapsed onto {units}"
    return units, strength


def _f20_capture(ctx, cell):
    """The drive and the state matrix for one cell, re-run through `collect_states`.

    Returns ``(drive, states)`` -- the retained white-noise input, one value per row, and
    the ``T_eff x N`` post-warmup state matrix the MC solver forms as its design matrix
    ``A``. Nothing is written and nothing is cached: `CONVENTIONS` working rule 5 forbids
    persisting states, which is the whole reason this figure re-runs.

    **The drive is redrawn rather than returned by the evaluator**, which is a coupling
    to `memory_capacity._measure`'s first RNG call, so it is checked rather than assumed:
    a lag-1 readout fit on the redrawn input has to reproduce the evaluator's own
    `mc_per_lag[0]`. If the redrawn series were not the series that drove these states
    that number would collapse to chance, so the assertion is a real gate on the one
    trace in panel (a) that could otherwise be silently wrong.
    """
    if ctx.placeholder:
        return _f20_placeholder_capture(cell)

    from src.reservoir import blas          # noqa: F401  BLAS cap; numpy is already in
    from src.reservoir.build import build_from_adjacency
    from experiments.human.substrates import HumanSubstrateBuilder
    from experiments.human import matrix_config
    from experiments.human.human_mc import task_config as mc_task_config

    spec = mc_task_config.task()
    params = spec["task_params"]
    builder = HumanSubstrateBuilder(scale=N_NODES)
    reservoir = build_from_adjacency(
        weighted_adjacency=builder.weighted("human_empirical", "connectome", cell.seed),
        target_spectral_radius=cell.spectral_radius, leak_rate=spec["leak_rate"],
        input_scaling=spec["input_scaling"], seed=cell.seed, input_dim=1)
    out = spec["task_evaluate"](reservoir, seed=cell.seed + matrix_config.INPUT_SEED_OFFSET,
                                collect_states=True, **params)
    states = np.asarray(out["states"], dtype=float)
    drive = np.random.default_rng(
        cell.seed + matrix_config.INPUT_SEED_OFFSET).uniform(
            -params["input_scaling"], params["input_scaling"],
            size=(params["T"], 1))[params["warmup"]:, 0]

    assert states.shape == (cell.t_effective, N_NODES), (
        f"the re-run returned a {states.shape} state matrix against the frozen cell's "
        f"({cell.t_effective}, {N_NODES}). The figure and the artifact are no longer "
        "describing the same reservoir.")
    assert drive.size == states.shape[0], (
        f"{drive.size} retained input samples against {states.shape[0]} retained "
        "timesteps; panel (a) draws them on one time axis.")
    design = states[1:]
    target = drive[:-1]
    weights = np.linalg.solve(
        design.T @ design + params["ridge_alpha"] * np.eye(N_NODES), design.T @ target)
    measured = float(np.corrcoef(design @ weights, target)[0, 1] ** 2)
    reference = float(np.asarray(out["mc_per_lag"])[0])
    assert abs(measured - reference) < 1e-6, (
        f"the input series panel (a) draws does not reconstruct from these states: a "
        f"lag-1 readout scores {measured:.6f} against the evaluator's own "
        f"{reference:.6f}. The drive is redrawn from `default_rng(seed + "
        "INPUT_SEED_OFFSET)` and that redraw has come apart from "
        "`memory_capacity._measure`, so the trace is not this reservoir's input.")
    return drive, states


def _f20_placeholder_capture(cell):
    """A layout-only stand-in with the real thing's shape, bounds and time structure.

    Nothing is read off a smoke render, so the only requirements are that it is
    ``T_eff x N``, that it lives in (-1, 1) as a tanh state does, that it carries a
    spread of per-unit offsets so (b) and (c) have something to separate, and that it is
    temporally continuous so (d) is a trajectory rather than a cloud of independent
    points.
    """
    rng = np.random.default_rng(20)
    drive = rng.uniform(-1.0, 1.0, cell.t_effective)
    innovation = rng.standard_normal((cell.t_effective, N_NODES))
    walk = np.empty_like(innovation)
    walk[0] = innovation[0]
    for step in range(1, cell.t_effective):          # AR(1): a continuous trajectory
        walk[step] = 0.55 * walk[step - 1] + innovation[step]
    offsets = np.linspace(-1.6, 0.1, N_NODES)[rng.permutation(N_NODES)]
    return drive, np.tanh(offsets + 1.3 * walk / walk.std())


def _f20_ring(ordering):
    """Node positions for panel (a)'s network glyph, and the drawn-order lookup.

    A ring in the **same node ordering panel (e) uses** -- hemisphere, then community,
    then descending degree -- so a community is a contiguous arc and the two matrices
    and the glyph are all one permutation of the same 448 nodes. The layout is schematic;
    the ordering, the edges and the nodes are not.
    """
    order = ordering.node.to_numpy(int)
    position = np.empty(N_NODES, int)
    position[order] = np.arange(N_NODES)
    angle = 2.0 * np.pi * np.arange(N_NODES) / N_NODES
    return order, position, np.cos(angle), np.sin(angle)


def _f20_chords(ax, position, x, y, index_i, index_j, **kwargs):
    """Edges as straight chords of the ring, drawn as one collection."""
    start = np.column_stack([x[position[index_i]], y[position[index_i]]])
    end = np.column_stack([x[position[index_j]], y[position[index_j]]])
    ax.add_collection(LineCollection(np.stack([start, end], axis=1), **kwargs))


def _f20_block_edges(ordering):
    """Community boundaries in the drawn ordering, and the heavier hemisphere cut.

    F19's construction, reproduced here because the two figures share the ordering: a
    community spanning the hemispheres appears as two arcs, one per half, since
    hemisphere is the outer key.
    """
    block = ordering.hemisphere.to_numpy() * 100 + ordering.community.to_numpy()
    hemisphere = ordering.hemisphere.to_numpy()
    return (np.flatnonzero(block[1:] != block[:-1]) + 1,
            np.flatnonzero(hemisphere[1:] != hemisphere[:-1]) + 1)


def f20_driven_network_to_gram(ctx):
    """What a readout sees: one driven reservoir, its state matrix, and its Gram split.

    **Carries no claim, deliberately.** It prints first in chapter 5 and defines the
    object the rest of the chapter measures -- a `T_eff x N` state matrix and the
    decomposition of `A^T A` the later sections quantify. One substrate, one cell, no
    null, no comparison. Three units are highlighted so the reader has something to
    follow from a trace, through a trajectory, into a matrix; **three units on one cell
    support no claim about which units do what**, and the caption says so rather than
    leaving the panels to imply otherwise.

    **What this figure must not pre-empt.** How much of the trace the rank-one term
    consumes, and whether substrates differ in it, is section 5.2's finding (A2.1, A2.2,
    F4). Nothing here says or implies that the fixed pattern dominates the activity: (b)
    and (c) sit on one vertical scale so centring is visibly a shift rather than a
    magnification, (d)'s two sub-panels share one box for the same reason, and (e) is on
    one shared scale with no inset to make either term look larger than it is.
    """
    spectra = ctx.frame("gram_spectra")
    edges = ctx.frame("substrate_edges")
    ordering = ctx.frame("substrate_order").sort_values("position")
    cell = SimpleNamespace(seed=int(spectra.seed.iloc[0]),
                           spectral_radius=float(spectra.spectral_radius.iloc[0]),
                           alpha=float(spectra.alpha.iloc[0]),
                           t_effective=int(spectra.T_effective.iloc[0]))

    units, _ = _f20_units(edges)
    drive, states = _f20_capture(ctx, cell)
    order, position, ring_x, ring_y = _f20_ring(ordering)
    boundaries, hemisphere_cut = _f20_block_edges(ordering)

    # ---- the decomposition the figure is about, computed once.
    mean_state = states.mean(0)
    centred = states - mean_state
    gram = states.T @ states
    gram_fluctuation = centred.T @ centred
    gram_rank_one = cell.t_effective * np.outer(mean_state, mean_state)
    trace_total = float(np.trace(gram))
    rank_one_fraction = float(np.trace(gram_rank_one)) / trace_total

    # ---- structural assertions: true of the arithmetic, so they run on both paths.
    residual = np.abs(gram - gram_fluctuation - gram_rank_one).max()
    assert residual / np.abs(gram).max() < 1e-10, (
        f"panel (e) draws an equation that does not hold: the worst entry of "
        f"A^T A - (At^T At + T m m^T) is {residual:.3e}. Every '=' and '+' on the panel "
        "is a claim about these three arrays.")
    assert abs(rank_one_fraction
               + float(np.trace(gram_fluctuation)) / trace_total - 1.0) < 1e-12, (
        "the two trace fractions do not sum to one, so the caption's percentage is not "
        "a share of anything.")
    # Every entry of all three matrices is bounded by T_eff, because |x| < 1 and
    # Cauchy-Schwarz. That is what makes +/- T_eff a shared scale with NO clipping
    # anywhere rather than a percentile chosen to look right, so it is checked.
    gram_limit = float(cell.t_effective)
    for name, matrix in (("A^T A", gram), ("At^T At", gram_fluctuation),
                         ("T m m^T", gram_rank_one)):
        assert np.abs(matrix).max() <= gram_limit * (1 + 1e-9), (
            f"an entry of {name} ({np.abs(matrix).max():.1f}) exceeds T_eff "
            f"({gram_limit:.0f}), so panel (e)'s shared colour scale clips it. The bound "
            "is |x| < 1 plus Cauchy-Schwarz; if it fails, the states are not tanh.")
    assert np.abs(states).max() < F20_ACTIVITY_LIMIT, (
        "a state lies outside (-1, 1), so panels (b) to (d) are cropping data. leak_rate "
        "is 1.0 and the activation is tanh; this cannot happen unless one of those has "
        "changed.")

    # ---- content assertions: claims about the frozen cell, so frozen data only.
    if not ctx.placeholder:
        assert cell.seed == F20_SEED, (
            f"`gram_spectra`'s median-d_eff rule now resolves to seed {cell.seed}, not "
            f"{F20_SEED}. `act2_manifold.md` §2.7's reproduction gate is on seed "
            f"{F20_SEED}, so the figure and its gate are no longer the same cell.")
        assert units == [119, 346, 262], (
            f"the strength percentiles now select {units}, not [119, 346, 262]. The "
            "figure block and §2.7 name those three nodes and the caption's selection "
            "rule is quoted against them.")
        assert abs(rank_one_fraction - F20_RANK_ONE_TRACE_FRACTION) < 5e-6, (
            f"the rank-one term carries {rank_one_fraction:.6f} of the trace against "
            f"§2.7's {F20_RANK_ONE_TRACE_FRACTION}. The caption quotes 51.3% and is "
            "sourced to that number alone.")
        # The §2.7 gate, in its cheap form: the re-run's Gram must still be the frozen
        # cell's Gram. A full eigenvalue comparison is the act file's; `d_eff` is one
        # scalar summarising all 448 and costs one eigensolve.
        recomputed = np.linalg.eigvalsh(gram)
        frozen = spectra.eig_gram.to_numpy(float)
        d_eff = float((np.clip(recomputed, 0.0, None)
                       / (np.clip(recomputed, 0.0, None) + cell.alpha)).sum())
        d_eff_frozen = float((frozen / (frozen + cell.alpha)).sum())
        assert abs(d_eff - d_eff_frozen) < 1e-3, (
            f"the re-run's design-Gram gives d_eff {d_eff:.6f} against the frozen "
            f"spectrum's {d_eff_frozen:.6f}. §2.7's gate no longer holds and every panel "
            "is drawing a different reservoir from the one the chapter cites.")

    # ------------------------------------------------------------------ layout
    # Five stacked bands, because every panel is either full width by nature (a's flow,
    # b and c's time axis, e's three matrices) or is a pair that has to share a scale
    # (d). (b) and (c) share one inner grid so they sit tight against a common x axis;
    # everything else is separated by the outer hspace.
    fig = plt.figure(figsize=(7.6, 9.0))
    outer = fig.add_gridspec(4, 1, height_ratios=[1.62, 2.12, 1.92, 2.16], hspace=0.54,
                             left=0.085, right=0.925, top=0.968, bottom=0.040)
    band_a = outer[0].subgridspec(1, 5, width_ratios=[1.20, 0.26, 1.15, 0.26, 2.55],
                                  wspace=0.07)
    band_bc = outer[1].subgridspec(2, 1, hspace=0.34)
    band_d = outer[2].subgridspec(1, 4, width_ratios=[0.02, 1.0, 1.0, 0.02], wspace=0.02)
    band_e = outer[3].subgridspec(2, 5, height_ratios=[1.0, 0.062],
                                  width_ratios=[1.0, 0.20, 1.0, 0.20, 1.0],
                                  hspace=0.26, wspace=0.05)

    ax_drive = fig.add_subplot(band_a[0, 0])
    ax_network = fig.add_subplot(band_a[0, 2])
    ax_states = fig.add_subplot(band_a[0, 4])
    ax_raw = fig.add_subplot(band_bc[0])
    ax_centred = fig.add_subplot(band_bc[1], sharex=ax_raw, sharey=ax_raw)
    ax_cloud_raw = fig.add_subplot(band_d[0, 1], projection="3d")
    ax_cloud_centred = fig.add_subplot(band_d[0, 2], projection="3d")
    ax_gram = [fig.add_subplot(band_e[0, column]) for column in (0, 2, 4)]
    ax_colourbar = fig.add_subplot(band_e[1, :])
    for column, symbol in ((1, "="), (3, "+")):
        spacer = fig.add_subplot(band_e[0, column])
        spacer.axis("off")
        spacer.text(0.5, 0.5, symbol, transform=spacer.transAxes, ha="center",
                    va="center", fontsize=15, color=style.ANNOTATION_COLOUR)
    for column in (1, 3):
        arrow = fig.add_subplot(band_a[0, column])
        arrow.axis("off")
        arrow.annotate("", xy=(0.95, 0.5), xytext=(0.05, 0.5),
                       xycoords="axes fraction", textcoords="axes fraction",
                       arrowprops=dict(arrowstyle="-|>", lw=1.0,
                                       color=style.ANNOTATION_COLOUR))

    timestep = np.arange(cell.t_effective)
    window = (cell.t_effective - F20_WINDOW) // 2
    drawn = slice(window, window + F20_WINDOW)

    # ---------------------------------------------- (a) the drive, the network, and A
    # The whole retained drive, with the 200 steps (b) and (c) draw picked out on it, so
    # the window is placed rather than asserted. Time runs DOWNWARD here and in the state
    # matrix beside it: they are the same 2500 rows and a reader should be able to sight
    # across from one to the other.
    # All 2500 retained samples, at the density 2500 samples actually have. The window
    # (b) and (c) draw is marked by a band rather than by a darker overlay of the same
    # trace: 200 samples in a tenth of an inch is a solid bar, which marks the window
    # but stops looking like a signal.
    ax_drive.plot(drive, timestep, lw=0.10, color=style.CEILING_COLOUR, alpha=0.55)
    ax_drive.axhspan(window, window + F20_WINDOW, color=style.ANNOTATION_ACCENT,
                     alpha=0.22, lw=0, zorder=2)
    ax_drive.annotate("(b, c)", xy=(0.04, window - 45), va="bottom", ha="left",
                      xycoords=("axes fraction", "data"),
                      fontsize=style.TICK_SIZE - 1, color=style.ANNOTATION_ACCENT)
    # Both this panel and the state matrix beside it run 0 to T_eff top to bottom, so
    # the two are one time axis and a reader can sight straight across from an input
    # sample to the row it produced. Only this panel carries the ticks.
    ax_drive.set_ylim(cell.t_effective, 0)
    ax_drive.set_xlim(-1.15, 1.15)
    ax_drive.set_xticks([-1, 0, 1])
    ax_drive.set_yticks([0, 1250, 2500])
    ax_drive.set_xlabel("input $u(t)$")
    ax_drive.set_ylabel("retained timestep $t$")
    ax_drive.set_title("white-noise drive", fontsize=style.TITLE_SIZE)

    connectome = edges[edges.variant == "connectome"]
    connectome = connectome[connectome.seed == connectome.seed.min()]
    index_i = connectome.i.to_numpy(int)
    index_j = connectome.j.to_numpy(int)
    _f20_chords(ax_network, position, ring_x, ring_y, index_i, index_j,
                colors=style.ANNOTATION_COLOUR, lw=0.12, alpha=0.045, zorder=1)
    for unit, colour in zip(units, style.UNIT_COLOURS):
        incident = (index_i == unit) | (index_j == unit)
        _f20_chords(ax_network, position, ring_x, ring_y, index_i[incident],
                    index_j[incident], colors=colour, lw=0.45, alpha=0.55, zorder=2)
    ax_network.plot(ring_x, ring_y, ls="none", marker="o", ms=0.6,
                    color=style.CEILING_COLOUR, zorder=3)
    for unit, colour in zip(units, style.UNIT_COLOURS):
        ax_network.plot([ring_x[position[unit]]], [ring_y[position[unit]]], ls="none",
                        marker="o", ms=5.0, color=colour, mec="white", mew=0.7, zorder=5)
    ax_network.annotate("", xy=(-0.86, 0.0), xytext=(-1.55, 0.0), xycoords="data",
                        textcoords="data", annotation_clip=False,
                        arrowprops=dict(arrowstyle="-|>", lw=1.0,
                                        color=style.ANNOTATION_COLOUR))
    ax_network.set_xlim(-1.12, 1.12)
    ax_network.set_ylim(-1.12, 1.12)
    ax_network.set_aspect("equal")
    ax_network.axis("off")
    ax_network.set_title("reservoir", fontsize=style.TITLE_SIZE)

    ax_states.imshow(states[:, order], aspect="auto", cmap=F20_SIGNED_CMAP,
                     vmin=-F20_ACTIVITY_LIMIT, vmax=F20_ACTIVITY_LIMIT,
                     interpolation="nearest", rasterized=True)
    for unit, colour in zip(units, style.UNIT_COLOURS):
        ax_states.plot([position[unit]], [1.0], marker="v", ms=4.2, color=colour,
                       clip_on=False, transform=ax_states.get_xaxis_transform(),
                       zorder=5)
    ax_states.set_yticks([])
    ax_states.set_xlabel(f"one column per unit  ($N$ = {N_NODES}, ordered as Fig. 19)")
    # On the right, so it does not sit in the arrow's way, and phrased as the axis
    # rather than as a range: the tick numbers are the drive panel's, which this shares.
    ax_states.yaxis.set_label_position("right")
    ax_states.set_ylabel(f"one row per retained timestep\n"
                         f"($T_{{\\rm eff}}$ = {cell.t_effective})",
                         fontsize=style.AXIS_LABEL_SIZE - 1)
    ax_states.set_title("state matrix $A$", fontsize=style.TITLE_SIZE)
    ax_states.grid(False)

    # ------------------------------------------- (b, c) three units, one vertical scale
    # ONE scale across both panels, and it is the activity's own bound rather than a
    # choice: leak_rate is 1.0, so a state is exactly tanh(.) and lies in (-1, 1). On a
    # shared scale centring is visibly a SHIFT -- each trace slides to zero and keeps its
    # shape -- which is the whole content of (c) and the reason there is no magnification
    # factor to annotate.
    traces = states[:, units]
    for index, (unit, colour) in enumerate(zip(units, style.UNIT_COLOURS)):
        ax_raw.plot(timestep[drawn], traces[drawn, index], lw=0.8, color=colour,
                    label=f"unit {unit}")
        ax_raw.axhline(traces[:, index].mean(), color=colour, ls="--", lw=0.9,
                       alpha=0.85, zorder=1)
        ax_centred.plot(timestep[drawn], traces[drawn, index] - traces[:, index].mean(),
                        lw=0.8, color=colour)
    ax_centred.axhline(0.0, color=style.ANNOTATION_COLOUR, lw=0.7, zorder=1)
    ax_raw.set_ylim(-1.05, 1.05)
    ax_raw.set_xlim(timestep[drawn][0], timestep[drawn][-1])
    ax_raw.set_yticks([-1, 0, 1])
    ax_raw.set_ylabel("activity $x_i(t)$")
    ax_centred.set_ylabel("$x_i(t) - $ mean")
    ax_centred.set_xlabel("retained timestep $t$")
    ax_raw.tick_params(labelbottom=False)
    # The legend sits ABOVE (b) and does the work a title would, with the dashed rule
    # named as a fourth entry: there is nowhere inside these axes a three-column box does
    # not cover a trace, since the three units between them span most of the (-1, 1) box.
    # F4b's `_assert_legend_clear` found the same thing the expensive way.
    mean_proxy = plt.Line2D([], [], ls="--", lw=0.9, color=style.ANNOTATION_COLOUR)
    handles, labels = ax_raw.get_legend_handles_labels()
    ax_raw.legend(handles + [mean_proxy],
                  labels + [f"mean over all {cell.t_effective} retained steps"],
                  loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=4,
                  fontsize=style.LEGEND_SIZE - 1, columnspacing=1.6, handlelength=1.8)

    # ------------------------------------ (d) the same three units, as one trajectory
    # Both sub-panels in the SAME (-1, 1) box and at the same viewing angle, so the two
    # clouds are directly comparable and centring is a translation the reader can see
    # rather than a rescaling they have to take on trust. Nothing is fitted to the cloud
    # and nothing is drawn through it.
    cloud_mean = traces.mean(0)
    for ax, cloud, title in (
            (ax_cloud_raw, traces, "raw"),
            (ax_cloud_centred, traces - cloud_mean, "time-centred")):
        ax.plot(cloud[:, 0], cloud[:, 1], cloud[:, 2], lw=0.22,
                color=style.ANNOTATION_COLOUR, alpha=0.55)
        ax.set_xlim(-F20_ACTIVITY_LIMIT, F20_ACTIVITY_LIMIT)
        ax.set_ylim(-F20_ACTIVITY_LIMIT, F20_ACTIVITY_LIMIT)
        ax.set_zlim(-F20_ACTIVITY_LIMIT, F20_ACTIVITY_LIMIT)
        ax.view_init(elev=20, azim=-58)
        # `zoom` fills the axes with the cube: a 3-D axes reserves a wide margin by
        # default, and at this panel size that margin is most of the panel. **1.25 is a
        # ceiling, not a taste**: past about 1.3 the projected cube overflows its own
        # axes and the x and y labels land in panel (e)'s titles, which is where 1.45
        # put them. Measured on the render.
        ax.set_box_aspect((1, 1, 1), zoom=1.25)
        ax.set_title(title, fontsize=style.TITLE_SIZE, pad=-4)
        for axis, colour in zip((ax.xaxis, ax.yaxis, ax.zaxis), style.UNIT_COLOURS):
            axis.label.set_color(colour)
        ax.set_xlabel(f"$x_{{{units[0]}}}$", labelpad=-3)
        ax.set_ylabel(f"$x_{{{units[1]}}}$", labelpad=-3)
        ax.set_zlabel(f"$x_{{{units[2]}}}$", labelpad=-3)
        ax.tick_params(labelsize=style.TICK_SIZE - 3, pad=-1)
        ax.set_xticks([-1, 0, 1])
        ax.set_yticks([-1, 0, 1])
        ax.set_zticks([-1, 0, 1])
    ax_cloud_raw.quiver(0.0, 0.0, 0.0, *cloud_mean, color=style.ANNOTATION_ACCENT,
                        lw=1.8, arrow_length_ratio=0.16, zorder=6)
    ax_cloud_raw.text2D(0.0, 0.88, "arrow: the mean point",
                        transform=ax_cloud_raw.transAxes, ha="left", va="top",
                        fontsize=style.TICK_SIZE - 1, color=style.ANNOTATION_ACCENT)

    # ------------------------------------------------- (e) the split, as three matrices
    # One shared symmetric scale at +/- T_eff, which clips nothing (asserted above) and
    # is not a percentile chosen to flatter either term. No inset and no second scale:
    # a magnified fluctuation term would say something about the relative size of the two
    # that this figure does not measure and section 5.2 does.
    #
    # **The scale is symmetric-logarithmic, and that is a correctness requirement rather
    # than a preference.** On a linear scale the two right-hand panels are drawn at
    # wildly different apparent strengths: the rank-one term is an outer product and so
    # is heavy-tailed (median |entry| 83, 99th percentile 2088), while the fluctuation
    # term is comparatively even (median 435, 99th percentile 618). A linear scale set
    # to the shared bound therefore renders the rank-one term as strong structure and
    # the fluctuation term as a near-blank wash -- a picture that says the fixed pattern
    # dominates, which is a claim this figure must not make (whether it does, and whether
    # substrates differ in it, is section 5.2's finding) and which is false of the
    # quantity the caption quotes: the two terms carry 51.3% and 48.7% of the trace.
    # SymLog shows both terms' structure at once, still on ONE scale under ONE bar, and
    # still with no clipping. `linthresh` is the linear window around zero.
    norm = mpl.colors.SymLogNorm(linthresh=F20_GRAM_LINTHRESH, linscale=0.6,
                                 vmin=-gram_limit, vmax=gram_limit, base=10)
    labels = (r"$A^{\mathsf{T}}\!A$", r"$\tilde{A}^{\mathsf{T}}\!\tilde{A}$",
              r"$T_{\rm eff}\,m\,m^{\mathsf{T}}$")
    for ax, matrix, label in zip(ax_gram, (gram, gram_fluctuation, gram_rank_one),
                                 labels):
        image = ax.imshow(matrix[np.ix_(order, order)], cmap=F20_SIGNED_CMAP, norm=norm,
                          interpolation="nearest", rasterized=True)
        for cut, width in ((boundaries, 0.25), (hemisphere_cut, 0.6)):
            for edge in cut:
                ax.axhline(edge - 0.5, color="0.35", lw=width, alpha=0.45)
                ax.axvline(edge - 0.5, color="0.35", lw=width, alpha=0.45)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(label, fontsize=style.TITLE_SIZE + 1)
        ax.grid(False)
    ax_gram[0].set_ylabel("unit  (ordered as Fig. 19)",
                          fontsize=style.AXIS_LABEL_SIZE - 1)
    ax_gram[1].set_xlabel(r"$m$: each unit's mean over time;   "
                          r"$\tilde{A} = A - \mathbf{1}m^{\mathsf{T}}$",
                          fontsize=style.AXIS_LABEL_SIZE - 1, labelpad=2)
    bar = fig.colorbar(image, cax=ax_colourbar, orientation="horizontal",
                       ticks=[-1000, -100, 0, 100, 1000])
    bar.ax.tick_params(labelsize=style.TICK_SIZE - 1)
    bar.outline.set_linewidth(0.4)
    bar.set_label("matrix entry   (one shared symmetric-log scale, no clipping)",
                  fontsize=style.AXIS_LABEL_SIZE - 1, labelpad=3)

    for ax, letter in ((ax_drive, "a"), (ax_raw, "b"), (ax_centred, "c"),
                       (ax_cloud_raw, "d"), (ax_gram[0], "e")):
        style.panel_label(ax, letter, offset_points=(-6, 3))
    return fig

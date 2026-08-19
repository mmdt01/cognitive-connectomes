"""Act III, prediction arm -- chapter 6, contributions 4 and 2.

F12 to F14 carry contribution 4 (generation is gated, not graded; `sigma_eff` is a
locator). F16 carries contribution 2 -- the unifying claim -- and is a cross-act figure:
it needs both arms, so **session 4 renders it** once session 3's memory arm is
validated.

**Substrate naming.** These builders use ``VARIANT_TITLE`` / ``VARIANT_TITLE_TICK`` --
the real null-model names -- matching F1 to F11. They were the last on the rung-numbered
``VARIANT_LABEL`` / ``VARIANT_TICK`` scheme; session 3 changed F7, F9, F10 and F11 and
left this module for its owner (`report/act3a_memory.md` audit item 11). Left alone,
chapter 6's prediction half would have named three substrates differently from every
other figure in the thesis.

Owned by session 4 (`report/act3b_prediction.md`).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

from report.figlib import style

# The empty band between the two curvature modes. A *descriptive* window: it is what
# TIER0 §3.10 counts cells in, and it is wider than the separator below.
CURVATURE_GAP = (0.6, 2.2)
# The straight/collapsed separator, and the "has it collapsed" bit. 1.0 sits inside the
# empty band; it is `extend_f.CURV_COLLAPSE`, the repo's canonical value, and it is the
# ONLY split that returns TIER0 §3.10's published n = 15,866 and +0.145. Reproducing
# those numbers at the band edges instead gives n = 15,761 and +0.155.
COLLAPSE_BIT = 1.0
# TIER0 §3.10's published pair, asserted below so the figure fails rather than the reader.
R2_BIT, R2_CONTINUOUS = 0.364, 0.371
# The transition band. NOT a criterion: 1 is withdrawn and is never drawn (TIER0 §3.10).
TRANSITION_BAND = (0.77, 0.90)
# TIER0 §2.3's published crossing, on `sigma * bulk95`. The builder solves for its own
# root and asserts against this rather than annotating a hard-coded coordinate.
PUBLISHED_CROSSING = (2.938, 0.153)
# The published nominal crossing. It CANNOT be drawn from the extension boundaries --
# it comes from re-running the boundary operator on the sigma <= 6 sub-panel -- so it is
# quoted as a TIER0 number and never implied to come from these curves.
PUBLISHED_NOMINAL_CROSSING = (4.392, 0.1309)


def f12_curvature_is_bimodal(ctx):
    """Generation is gated, not graded: the figure that licenses the switch framing.

    Without this the whole switch account reads as asserted, so it leads the arm.
    Three panels, each closing off one reading:

    (a) the distribution is two spikes with an empty band between them, so "how curved"
        is not a quantity this substrate takes intermediate values of;
    (b) a binary collapsed-or-not bit explains as much of VPT as the continuous
        quantity does, so the 0.25 -> 3.14 rad range is worth 0.7 percentage points
        beyond the bit;
    (c) *within* the straight cluster the residual rank correlation is POSITIVE, the
        opposite sign to a graded straightness account -- which is why roadmap §1 lists
        that account under "what must NOT be claimed".

    Curvature here is measured on the **teacher-forced** state trajectory in R^448
    (turning angle between successive velocity vectors, pi = antiparallel), while VPT
    is a **free-run** outcome. The figure relates a driven-manifold diagnostic to a
    closed-loop capacity; that is the claim, and the caption says so.
    """
    frame = ctx.frame("jacobian")
    curvature = frame.mean_curvature.to_numpy(float)
    vpt = frame.vpt.to_numpy(float)
    finite = np.isfinite(curvature) & np.isfinite(vpt)
    curvature, vpt = curvature[finite], vpt[finite]
    n_cells = curvature.size

    fig, axes = plt.subplots(1, 3, figsize=(8.4, 2.7),
                             gridspec_kw=dict(width_ratios=[1.1, 1.15, 0.95]))

    # --- (a) the two spikes and the empty band ------------------------------------
    axes[0].hist(curvature, bins=np.linspace(0, np.pi, 160), color="0.35")
    axes[0].axvspan(*CURVATURE_GAP, color=style.ANNOTATION_ACCENT, alpha=0.13, lw=0)
    axes[0].axvline(COLLAPSE_BIT, color=style.ANNOTATION_ACCENT, lw=0.9, ls="--")
    axes[0].set_yscale("log")
    axes[0].set_xlabel("mean curvature (rad)")
    axes[0].set_ylabel(f"cells  (n = {n_cells:,})")
    between = int(((curvature >= CURVATURE_GAP[0])
                   & (curvature <= CURVATURE_GAP[1])).sum())
    axes[0].annotate(f"{between} cells in\n[0.6, 2.2] rad\n"
                     f"({100 * between / n_cells:.2f}%)",
                     xy=(1.42, 0.60), xycoords=("data", "axes fraction"),
                     ha="left", fontsize=style.TICK_SIZE - 1,
                     color=style.ANNOTATION_ACCENT)
    axes[0].annotate("smooth", xy=(0.26, 0.93), xycoords=("data", "axes fraction"),
                     ha="center", fontsize=style.TICK_SIZE - 1, color="0.25")
    axes[0].annotate(r"period-2 ($\approx \pi$)", xy=(2.90, 0.93),
                     xycoords=("data", "axes fraction"), ha="right",
                     fontsize=style.TICK_SIZE - 1, color="0.25")

    # --- (b) the bit explains as much as the quantity ------------------------------
    bit = (curvature > COLLAPSE_BIT).astype(float)
    r2_bit = _r_squared(bit, vpt)
    r2_continuous = _r_squared(curvature, vpt)
    # TIER0 quotes both to three decimals, so that is the precision the gate holds to:
    # recomputed here they are 0.3636 and 0.3705. Content assertions are skipped on
    # placeholder data, which carries no claim (act2_manifold.md audit item 14).
    assert ctx.placeholder or (
        abs(r2_bit - R2_BIT) < 1e-3 and abs(r2_continuous - R2_CONTINUOUS) < 1e-3), (
        f"F12: binary-bit R2 {r2_bit:.4f} / continuous {r2_continuous:.4f} against "
        f"TIER0 §3.10's {R2_BIT} / {R2_CONTINUOUS}. The published pair is reproduced by "
        "splitting at CURV_COLLAPSE = 1.0; do not adjust the threshold to fit.")
    axes[1].hexbin(curvature, vpt, gridsize=(60, 34), bins="log",
                   cmap="Greys", mincnt=1, linewidths=0, rasterized=True)
    axes[1].axvspan(*CURVATURE_GAP, color=style.ANNOTATION_ACCENT, alpha=0.13, lw=0)
    axes[1].set_xlabel("mean curvature (rad)")
    axes[1].set_ylabel("VPT (Lyapunov times)")
    axes[1].set_title(f"collapsed-or-not bit  $R^2$ = {r2_bit:.3f}\n"
                      f"continuous curvature  $R^2$ = {r2_continuous:.3f}",
                      fontsize=style.TITLE_SIZE - 1)
    floor = float((vpt == 0).mean())
    axes[1].annotate(f"{100 * floor:.0f}% of cells at VPT = 0",
                     xy=(0.97, 0.06), xycoords="axes fraction", ha="right",
                     fontsize=style.TICK_SIZE - 1, color="0.35")

    # --- (c) within the straight cluster the residual runs the WRONG way -----------
    # Shown as curvature deciles, not as a scatter: 99% of the smooth cluster sits in a
    # ~0.05 rad column, so a hexbin of it is one dark stripe and the sign of the trend --
    # which is the entire claim -- is invisible. Deciles put the rank statistic on the
    # page as something a reader can see running upward.
    straight = curvature < COLLAPSE_BIT
    rho = float(spearmanr(curvature[straight], vpt[straight]).statistic)
    assert ctx.placeholder or rho > 0, (
        "F12: the within-straight residual is expected POSITIVE "
        "(TIER0 §3.10: +0.145), the opposite sign to a graded account.")
    edges = np.quantile(curvature[straight], np.linspace(0, 1, 11))
    index = np.clip(np.searchsorted(edges, curvature[straight], side="right") - 1, 0, 9)
    centres = np.array([np.median(curvature[straight][index == k]) for k in range(10)])
    medians = np.array([np.median(vpt[straight][index == k]) for k in range(10)])
    q25 = np.array([np.quantile(vpt[straight][index == k], 0.25) for k in range(10)])
    q75 = np.array([np.quantile(vpt[straight][index == k], 0.75) for k in range(10)])
    axes[2].fill_between(centres, q25, q75, color="0.75", alpha=0.5, lw=0)
    axes[2].plot(centres, medians, marker="o", ms=4, color=style.ANNOTATION_ACCENT, lw=1.6)
    axes[2].set_xlabel("mean curvature (rad), by decile")
    axes[2].set_ylabel("VPT (Lyapunov times)")
    axes[2].set_title("within the smooth cluster, median and IQR\n"
                      r"Spearman $\rho$ = " + f"+{rho:.3f}  (n = {int(straight.sum()):,})",
                      fontsize=style.TITLE_SIZE - 1)
    axes[2].annotate("straighter is not better", xy=(0.5, 0.90),
                     xycoords="axes fraction", ha="center",
                     fontsize=style.TICK_SIZE - 1, color=style.ANNOTATION_ACCENT)

    for ax, letter in zip(axes, "abc"):
        style.panel_label(ax, letter, dx=-0.16)
    fig.tight_layout()
    return fig


def _r_squared(predictor, response) -> float:
    """R^2 of the least-squares fit of ``response`` on ``predictor`` plus an intercept."""
    design = np.column_stack([np.ones_like(predictor), predictor])
    beta, *_ = np.linalg.lstsq(design, response, rcond=None)
    residual = response - design @ beta
    return float(1.0 - residual @ residual
                 / ((response - response.mean()) @ (response - response.mean())))


def f13_generation_as_vpt(ctx):
    """Read as VPT the generative advantage is real -- and it exists at f = 0 too.

    Panel (c) is the one that matters most and the one a draft would drop: the f = 0
    collapse rates are what move the generative advantage into the **biologically real**
    regime, since macro dMRI weights are non-negative by construction. Without it the
    whole arm reads as a statement about an f > 0 counterfactual.

    The unit in (c) is the **seed**, never the replicate: the three draws of a seed share
    its mask, `Win` and input series, and at f = 0 the sign transform is the identity, so
    the draws are literal duplicates (TIER0 §2.3). "5 of 10 seeds", not "50% of
    replicates".
    """
    frontier = ctx.frame("frontier")
    paired = ctx.frame("frontier_paired")
    loci = ctx.frame("collapse_loci")
    fig, axes = plt.subplots(1, 3, figsize=(8.4, 2.8),
                             gridspec_kw=dict(width_ratios=[1.2, 1.2, 0.72]))

    # --- (a) absolute VPT at sigma = 2, near every variant's own peak ---------------
    near_critical = frontier[(frontier.metric == "vpt")
                             & (np.isclose(frontier.spectral_radius, 2.0))]
    for variant in style.ordered_variants(near_critical.variant.unique()):
        curve = near_critical[near_critical.variant == variant].sort_values("f")
        axes[0].plot(curve.f, curve["median"], marker="o", ms=3,
                     **style.variant_kwargs(variant, label=style.VARIANT_TITLE[variant]))
    axes[0].axhline(0, color=style.ANNOTATION_COLOUR, lw=0.8)
    axes[0].set_xlabel("sign fraction $f$")
    axes[0].set_ylabel(r"VPT (Lyapunov times), $\sigma$ = 2")
    style.legend(axes[0], loc="upper right", fontsize=style.LEGEND_SIZE - 2)

    # --- (b) the paired advantage, which is where every claim comes from ------------
    contrasts = paired[(paired.metric == "vpt")
                       & (np.isclose(paired.spectral_radius, 2.0))]
    for null in [n for n in style.VARIANT_ORDER if n in set(contrasts.null)]:
        sub = contrasts[contrasts.null == null].sort_values("f")
        axes[1].plot(sub.f, sub.mean_diff, marker="o", ms=3,
                     color=style.VARIANT_COLOUR[null], label=style.VARIANT_TITLE[null])
        axes[1].fill_between(sub.f, sub.ci_lo, sub.ci_hi, alpha=0.15,
                             color=style.VARIANT_COLOUR[null], lw=0)
    axes[1].axhline(0, color=style.ANNOTATION_COLOUR, lw=0.9)
    # The +1.0 to +2.2 band holds against ALL THREE nulls from f = 0.25, not 0.20: at
    # f = 0.20 the degree-matching contrast is +0.28 (see act3b_prediction.md §2).
    axes[1].axvspan(0.25, float(contrasts.f.max()), color=style.SUPERCRITICAL_COLOUR,
                    zorder=0)
    axes[1].annotate("all three nulls\ncleared", xy=(0.375, 0.06),
                     xycoords=("data", "axes fraction"), ha="center",
                     fontsize=style.TICK_SIZE - 1, color="0.35")
    axes[1].set_xlabel("sign fraction $f$")
    axes[1].set_ylabel("paired VPT advantage\n(connectome $-$ null)")
    style.legend(axes[1], loc="upper left", fontsize=style.LEGEND_SIZE - 2)

    # --- (c) f = 0: the biologically real cut ---------------------------------------
    at_zero = loci[np.isclose(loci.f, 0.0)]
    variants = [v for v in style.VARIANT_ORDER if v in set(at_zero.variant)]
    counts = [int(at_zero[at_zero.variant == v].n_seeds_collapsed.iloc[0])
              for v in variants]
    totals = [int(at_zero[at_zero.variant == v].n_seeds.iloc[0]) for v in variants]
    axes[2].bar(np.arange(len(variants)), counts,
                color=[style.VARIANT_COLOUR[v] for v in variants],
                edgecolor="white", linewidth=0.5)
    for i, (count, total) in enumerate(zip(counts, totals)):
        axes[2].text(i, count + 0.15, f"{count}/{total}", ha="center",
                     fontsize=style.TICK_SIZE)
    axes[2].set_xticks(np.arange(len(variants)))
    axes[2].set_xticklabels([style.VARIANT_TITLE_TICK[v] for v in variants],
                            fontsize=style.TICK_SIZE - 1)
    axes[2].set_ylim(0, max(totals) * 0.72)
    axes[2].set_ylabel("seeds collapsed\nto period-2")
    axes[2].set_title(r"$f$ = 0,  $\sigma \leq$ 11.2" "\n"
                      "Fisher exact $p$ = 0.033", fontsize=style.TITLE_SIZE - 1)
    axes[2].grid(axis="x", visible=False)
    # Fixed point offsets, not axes fractions: (c) is narrower than (a) and (b), so the
    # same fractional dx puts its label a smaller absolute distance out and straight
    # through the y label.
    for ax, letter in zip(axes, "abc"):
        style.panel_label(ax, letter, offset_points=(-34, 4))
    fig.tight_layout()
    return fig


def f14_sigma_eff_is_a_locator(ctx):
    """A locator, not a criterion. No line is drawn at 1, because 1 is withdrawn.

    Panel (a)'s statistic is a **robust** CV -- ``IQR / median``, not ``sd / mean``
    (`criticality_matched/threshold.py`). The axis says so, because the two disagree by
    enough to matter: under sd/mean the three read 0.256 / 0.540 / 0.589, so `sigma_eff`
    still wins but by ~2.3x rather than ~3x. Quoting 0.209 without the definition invites
    a reader to recompute the wrong thing.

    The two aggregation units must not be read against each other: 0.209 is per
    (variant, f) with under-half-transitioning cells dropped (n = 37). The seed-level
    unit (n = 378) gives 0.304 against the exact Jacobian's 0.152, and TIER0 §3.11 says
    explicitly not to read 0.209 against 0.152. Only the §3.10 comparison is drawn here.

    Three panels because the claim has three parts and they have different scopes:
    (a) `sigma_eff` is the most invariant of the three candidates; (b) where each
    substrate transitions, per `f`, with the out-of-scope cells shown but not joined;
    (c) the **variant-dependent offset predicted in advance**, which is a statement
    about each substrate's median bracket. It needs its own panel because the per-`f`
    curves in (b) cross -- the connectome is the lowest on the median and is *not* the
    lowest at every `f`, and a title on (b) asserting the ordering would be read as the
    stronger claim.
    """
    invariance = ctx.frame("threshold_invariance")
    table = ctx.frame("threshold_table")
    fig, axes = plt.subplots(1, 3, figsize=(9.0, 2.9),
                             gridspec_kw=dict(width_ratios=[0.72, 1.25, 0.78]))

    scope = invariance[invariance.scope == "f > 0"].copy()
    short = {"nominal sigma": r"nominal $\sigma$",
             "sigma * bulk95  (linear negative-mode gain)": r"$\sigma\cdot$bulk95",
             "sigma_eff = bulk95 * sigma * <1-x^2>": r"$\sigma_{\rm eff}$"}
    scope["label"] = scope.criterion.map(lambda c: short.get(c, c))
    # sigma_eff is the winner and is the only bar that carries a claim, so it is the
    # only one in an accent colour; the two alternatives are furniture.
    colours = ["0.62" if r"\sigma_{\rm eff}" not in label else style.ANNOTATION_ACCENT
               for label in scope.label]
    axes[0].bar(np.arange(len(scope)), scope.cv, color=colours,
                edgecolor="white", linewidth=0.5)
    for i, value in enumerate(scope.cv):
        axes[0].text(i, value + 0.016, f"{value:.3f}", ha="center", fontsize=style.TICK_SIZE)
    axes[0].set_xticks(np.arange(len(scope)))
    # The three criterion names are wider than a one-unit category spacing, so they are
    # rotated rather than shrunk below the contract's sizes -- session 3's rule for F7's
    # and F9's substrate ticks, applied here for the same reason.
    axes[0].set_xticklabels(scope.label, fontsize=style.TICK_SIZE, rotation=20,
                            ha="right", rotation_mode="anchor")
    axes[0].set_ylabel("robust CV (IQR / median)\nof the value at the transition\n"
                       "(lower = better locator)")
    axes[0].set_ylim(0, float(scope.cv.max()) * 1.24)
    axes[0].set_title(r"scope: $f > 0$,  n = "
                      + f"{int(scope.n.iloc[0]) if len(scope) else 0}",
                      fontsize=style.TITLE_SIZE - 1)
    axes[0].grid(axis="x", visible=False)

    # Panel (b) must carry panel (a)'s scope, or the figure sets two populations side by
    # side and lets the reader compare them. The CV of 0.209 is computed on f > 0 cells
    # where at least half the seeds transition (n = 37); the rest are drawn as open grey
    # markers, not joined, because the locator is not claimed to hold there. The f = 0
    # column is the sharpest case: ER transitions at sigma_eff = 0.014, two orders of
    # magnitude below its own peak and on the DESCENDING branch, and the connectome never
    # transitions at all. Joining those points to the f > 0 curve would draw a locator
    # through the regime TIER0 §3.10 names as open.
    table = table.dropna(subset=["effective_radius_lo", "effective_radius_hi"])
    in_scope = (table.f > 0) & (table.frac_seeds_collapsed >= 0.5)
    # Content, not layout: on placeholders the invariance frame and the threshold table
    # are independent fakes and cannot agree on a count.
    assert ctx.placeholder or int(in_scope.sum()) == int(scope.n.iloc[0]), (
        f"F14: panel (b) holds {int(in_scope.sum())} cells against panel (a)'s "
        f"n = {int(scope.n.iloc[0])}. Both panels must be the same population.")
    ordered = style.ordered_variants(table.variant.unique())
    for variant in ordered:
        sub = table[in_scope & (table.variant == variant)].sort_values("f")
        mid = (sub.effective_radius_lo + sub.effective_radius_hi) / 2
        axes[1].plot(sub.f, mid, marker="o", ms=3, zorder=4,
                     **style.variant_kwargs(variant, label=style.VARIANT_TITLE[variant]))
        axes[1].fill_between(sub.f, sub.effective_radius_lo, sub.effective_radius_hi,
                             alpha=0.13, color=style.VARIANT_COLOUR[variant], lw=0)
        out = table[~in_scope & (table.variant == variant)]
        mid_out = (out.effective_radius_lo + out.effective_radius_hi) / 2
        axes[1].plot(out.f, mid_out, ls="none", marker="o", ms=4.5, mfc="none",
                     mec=style.VARIANT_COLOUR[variant], mew=1.0, alpha=0.8, zorder=3)
    axes[1].axhspan(*TRANSITION_BAND, color=style.ANNOTATION_ACCENT, alpha=0.10, lw=0,
                    zorder=0)
    # The band is shaded here but labelled only in (c), where it has the room and where
    # the numbers belong; labelling it twice put the text across the curves.
    axes[1].annotate("open markers: under half the seeds\n"
                     "transition. At $f$ = 0 the locator does\nnot apply at all.",
                     xy=(0.03, 0.97), xycoords="axes fraction", ha="left", va="top",
                     fontsize=style.TICK_SIZE - 1, color="0.35")
    # There is deliberately NO line at 1: the unit crossing is withdrawn (TIER0 §3.10),
    # and drawing it would reinstate the criterion the figure exists to retire.
    assert not any(np.isclose(line.get_ydata(), 1.0).all()
                   for line in axes[1].get_lines() if line.get_ydata().size), \
        "F14: no reference line may be drawn at sigma_eff = 1; the criterion is withdrawn."
    axes[1].set_xlabel("sign fraction $f$")
    axes[1].set_ylabel(r"$\sigma_{\rm eff}$ at the transition")
    axes[1].set_ylim(0, 1.12)
    style.legend(axes[1], loc="lower right", fontsize=style.LEGEND_SIZE - 2, ncol=2,
                 columnspacing=0.9, handlelength=1.5)

    # Panel (c): the offset that was predicted in advance, on the medians it is a claim
    # about. Ordered by spectral gap -- the connectome, which has much the largest gap,
    # transitions at the LOWEST sigma_eff.
    medians = []
    for variant in ordered:
        sub = table[in_scope & (table.variant == variant)]
        medians.append((variant, float(sub.effective_radius_lo.median()),
                        float(sub.effective_radius_hi.median())))
    assert ctx.placeholder or (
        medians[0][0] == "connectome"
        and medians[0][1] == min(m[1] for m in medians)), \
        "F14: the connectome must carry the lowest median bracket (TIER0 §3.10)."
    for row, (variant, lo, hi) in enumerate(medians):
        y = len(medians) - 1 - row
        axes[2].plot([lo, hi], [y, y], lw=5, solid_capstyle="butt",
                     color=style.VARIANT_COLOUR[variant])
        axes[2].annotate(f"[{lo:.2f}, {hi:.2f}]", xy=(hi + 0.012, y), va="center",
                         fontsize=style.TICK_SIZE - 1, color="0.3")
    axes[2].axvspan(*TRANSITION_BAND, color=style.ANNOTATION_ACCENT, alpha=0.10, lw=0,
                    zorder=0)
    axes[2].set_yticks(np.arange(len(medians)))
    axes[2].set_yticklabels([style.VARIANT_TITLE[v] for v, _, _ in medians][::-1],
                            fontsize=style.TICK_SIZE)
    axes[2].set_xlim(0.62, 1.06)
    axes[2].set_xlabel(r"median $\sigma_{\rm eff}$ bracket")
    axes[2].set_title("the offset, ordered by spectral gap",
                      fontsize=style.TITLE_SIZE - 1)
    axes[2].grid(axis="y", visible=False)
    for ax, letter in zip(axes, "abc"):
        style.panel_label(ax, letter, offset_points=(-36, 4))
    fig.tight_layout()
    return fig


def _segments(frame, column):
    """Contiguous runs of a boundary, split wherever the contour is undefined.

    ``f_star`` is NaN where no contour exists -- 37 of 121 points on the effective axis
    and 75 of 121 on the nominal one. Joining across a gap would draw a boundary through
    a region where none was found, so the runs are yielded separately and the line is
    broken between them (`FIGURE_LIST`, "F16 -- the boundaries have gaps").
    """
    frame = frame.sort_values("x")
    x_all = frame.x.to_numpy(float)
    step = float(np.median(np.diff(x_all))) if x_all.size > 1 else 1.0
    defined = frame.dropna(subset=[column])
    x, y = defined.x.to_numpy(float), defined[column].to_numpy(float)
    if x.size == 0:
        return
    cuts = np.flatnonzero(np.diff(x) > 1.5 * step) + 1
    for piece_x, piece_y in zip(np.split(x, cuts), np.split(y, cuts)):
        yield piece_x, piece_y


def _crossings(memory, generative, column="f_star"):
    """Every x where the two boundaries swap order, as ``(x, f)`` pairs.

    The root is **solved for** between the bracketing grid points rather than snapped to
    the right-hand one. Snapping returns TIER0 §2.3's six recomputed values exactly
    (2.943, 3.525, 3.598, 3.670, 3.743, 4.361); solving returns 2.938 for the first,
    which is the published coordinate of record. The 0.005 TIER0 attributes to
    interpolation is that snap, so solving removes it rather than competing with it.
    """
    memory = memory.dropna(subset=[column]).sort_values("x")
    generative = generative.dropna(subset=[column]).sort_values("x")
    if memory.empty or generative.empty:
        return []
    lo = max(memory.x.min(), generative.x.min())
    hi = min(memory.x.max(), generative.x.max())
    grid = np.union1d(memory.x.to_numpy(), generative.x.to_numpy())
    grid = grid[(grid >= lo) & (grid <= hi)]
    if grid.size < 2:
        return []
    upper = np.interp(grid, memory.x, memory[column])
    lower = np.interp(grid, generative.x, generative[column])
    gap = upper - lower
    out = []
    for i in range(1, grid.size):
        if np.sign(gap[i - 1]) * np.sign(gap[i]) < 0:
            t = gap[i - 1] / (gap[i - 1] - gap[i])
            x_root = grid[i - 1] + t * (grid[i] - grid[i - 1])
            out.append((float(x_root), float(np.interp(x_root, grid, upper))))
    return out


def f16_phase_boundaries(ctx):
    """The crossing, with its axis and its coverage. Contribution 2's own figure.

    This is the ONLY figure carrying contribution 2 -- the memory and generative
    advantages are one axis read with opposite sign -- and the claim is that the two
    advantage regions occupy **opposite regions of the (f, sigma) plane**, which no pair
    of 1-D slices can show. F7 is memory against sigma*bulk95 at f = 0 and F13 is VPT
    against f at sigma = 2; neither sees the plane.

    Four things the figure has to get right, all of them places a defensible-looking
    version would be wrong:

    * **The coverage mask is the point, not decoration.** Past each f's own ``x_hi`` the
      panel is populated only by the replicates whose own ``bulk95`` reached that far, so
      the boundary rests on a selected subsample and oscillates. Hatched, the published
      crossing is visibly the first and the clean one; quoted bare it looks like a unique
      feature, and a reader who recomputes finds six.
    * **``f_star`` is the convention.** ``f_star_level_on_subrange`` agrees with it on the
      effective axis; ``f_star_level_raw_max`` -- the level set by a cell backed by 1
      replicate of 30 -- gives no crossing at all, which is precisely what TIER0 §2.3
      reports. The other two columns are the robustness check, not alternatives to plot.
    * **The published nominal crossing cannot be drawn from this file.** It needs the
      boundary operator re-run on the sigma <= 6 sub-panel. It is annotated as a quoted
      TIER0 number and marked as such.
    * **The boundaries have gaps and they are broken, never bridged** (see
      ``_segments``).
    """
    boundaries = ctx.frame("boundaries")
    coverage = ctx.frame("coverage")
    fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.2))

    for ax, axis in zip(axes, ("effective", "nominal")):
        sub = boundaries[boundaries.axis == axis]
        x_max = float(sub.x.max())
        memory = sub[sub.panel == "dD"]
        generative = sub[sub.panel == "dStraight"]

        if axis == "effective":
            # Coverage is f-dependent, so the mask is a region, not a vertical line.
            # The nominal axis needs none: every nominal cell carries all 30 replicates.
            edge = coverage.sort_values("f")
            ax.fill_betweenx(edge.f, edge.x_hi, x_max, facecolor="none", lw=0,
                             hatch="////", edgecolor=style.UNCOVERED_COLOUR, zorder=0)
            ax.plot(edge.x_hi, edge.f, color=style.UNCOVERED_COLOUR, lw=1.0, ls="-",
                    zorder=1)
            floor = float(edge.x_hi.min())
            ax.axvline(floor, color=style.UNCOVERED_COLOUR, lw=0.9, ls="--", zorder=1)
            ax.annotate("hatched: beyond each $f$'s own coverage edge,\n"
                        "where not all 30 replicates reach",
                        xy=(0.985, 0.985), xycoords="axes fraction",
                        fontsize=style.TICK_SIZE - 1, va="top", ha="right", color="0.4")
        else:
            ax.axvline(6.0, color=style.ANNOTATION_COLOUR, lw=0.9, ls=":", zorder=1)
            ax.annotate("old sweep limit", xy=(6.0 - 0.2, 0.40),
                        xycoords=("data", "axes fraction"), fontsize=style.TICK_SIZE - 1,
                        va="center", ha="right", rotation=90,
                        color=style.ANNOTATION_COLOUR)

        for panel, frame in (("dD", memory), ("dStraight", generative)):
            label = style.BOUNDARY_LABEL[panel]
            for piece_x, piece_y in _segments(frame, "f_star"):
                ax.plot(piece_x, piece_y, color=style.BOUNDARY_COLOUR[panel], lw=1.7,
                        label=label, zorder=4)
                label = None                      # one legend entry per boundary

        found = _crossings(memory, generative)
        if axis == "effective":
            assert found, "F16: the effective axis must show the published crossing."
            x_root, f_root = found[0]
            assert ctx.placeholder or abs(x_root - PUBLISHED_CROSSING[0]) < 5e-3, (
                f"F16: first crossing at x = {x_root:.4f} against TIER0 §2.3's "
                f"{PUBLISHED_CROSSING[0]}.")
            ax.plot([x_root], [f_root], marker="o", ms=7, mfc="none",
                    mec="black", mew=1.5, zorder=6)
            ax.annotate(f"({x_root:.3f}, {f_root:.3f})\nfirst crossing,\ninside coverage",
                        xy=(x_root, f_root), xytext=(-8, 14),
                        textcoords="offset points", ha="right",
                        fontsize=style.TICK_SIZE, color=style.ANNOTATION_COLOUR)
            # The remaining crossings are drawn, faintly, and not labelled: they are the
            # oscillation TIER0 §6.10 says must not be read, and hiding them would make
            # the first look unique when a reader who recomputes will find six.
            for x_other, f_other in found[1:]:
                ax.plot([x_other], [f_other], marker="o", ms=4, mfc="none",
                        mec="0.45", mew=0.9, zorder=5)
            # NOT "in the unreadable region": the coverage edge is f-dependent and runs
            # straight through this band, so two of the five sit inside their own f's
            # coverage and one sits inside even the minimum edge. What is true of all
            # five, and what makes them unreadable, is that they are one oscillation of
            # the generative boundary crossing zero repeatedly -- see
            # `report/act3b_prediction.md` §5, where the arithmetic is logged.
            others = [x for x, _ in found[1:]]
            if others:
                ax.annotate(f"{len(found) - 1} further crossings,\n"
                            f"{min(others):.1f} to {max(others):.1f}: one oscillation\n"
                            "of the generative boundary,\nnot to be read",
                            xy=(np.mean(others), max(f for _, f in found[1:])),
                            xytext=(0.985, 0.80), textcoords="axes fraction",
                            ha="right", va="top", fontsize=style.TICK_SIZE - 1,
                            color="0.45",
                            arrowprops=dict(arrowstyle="-", color="0.6", lw=0.7,
                                            shrinkA=2, shrinkB=4))
        else:
            assert ctx.placeholder or not found, (
                "F16: the nominal axis must show NO crossing on f_star over the "
                "extended sweep (TIER0 §2.3).")
            ax.annotate("the two boundaries never meet", xy=(0.5, 0.985),
                        xycoords="axes fraction", ha="center", va="top",
                        fontsize=style.TICK_SIZE, color=style.ANNOTATION_COLOUR,
                        style="italic")
            # Quoted, not drawn: this point comes from re-running the boundary operator
            # on the sigma <= 6 sub-panel, which these curves are not.
            ax.plot(*PUBLISHED_NOMINAL_CROSSING, marker="x", ms=6, color="0.45",
                    mew=1.2, zorder=5)
            ax.annotate(f"published ({PUBLISHED_NOMINAL_CROSSING[0]}, "
                        f"{PUBLISHED_NOMINAL_CROSSING[1]}), quoted:\n"
                        r"from re-running the operator on the $\sigma \leq$ 6"
                        "\nsub-panel, not from these curves",
                        xy=PUBLISHED_NOMINAL_CROSSING, xytext=(0.985, 0.72),
                        textcoords="axes fraction", ha="right", va="top",
                        fontsize=style.TICK_SIZE - 1, color="0.45",
                        arrowprops=dict(arrowstyle="-", color="0.6", lw=0.7,
                                        shrinkA=2, shrinkB=5))

        ax.set_xlabel(style.AXIS_LABEL[axis])
        ax.set_xlim(0, x_max)
        ax.set_ylim(0, 0.42)
    axes[0].set_ylabel("sign fraction $f$")
    style.legend(axes[0], loc="upper left")
    for ax, letter in zip(axes, "ab"):
        style.panel_label(ax, letter, dx=-0.11)
    fig.tight_layout()
    return fig

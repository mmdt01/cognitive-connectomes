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
    """One large real Perron root, over a bulk that is essentially everyone's."""
    frame = ctx.frame("spectra_448")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.7))

    bins_full = np.linspace(-1.05, 1.05, 121)
    bins_bulk = np.linspace(-0.7, 0.7, 121)
    for ax, bins, title in ((axes[0], bins_full, "full real axis"),
                            (axes[1], bins_bulk, "bulk, magnified")):
        for variant in style.ordered_variants(frame.variant.unique()):
            pooled = np.concatenate(frame[frame.variant == variant].eig_w_real.to_list())
            ax.hist(pooled, bins=bins, density=True, histtype="step",
                    **{k: v for k, v in style.variant_kwargs(variant).items()
                       if k in ("color", "label", "lw")})
        ax.set_xlabel(r"eigenvalue (units of $|\lambda_1|$)")
        ax.set_title(title)
    axes[0].set_ylabel("density")
    axes[0].set_yscale("log")
    axes[0].annotate(r"$\lambda_1$", xy=(1.0, 1e-2), xytext=(0.62, 3e-1),
                     fontsize=style.TICK_SIZE, color=style.ANNOTATION_COLOUR,
                     arrowprops=dict(arrowstyle="->", lw=0.7))

    # bulk95 per variant: the 95th percentile of |lambda| in these normalised units.
    for variant in style.ordered_variants(frame.variant.unique()):
        bulk95 = frame[frame.variant == variant].bulk95.median()
        axes[1].axvline(bulk95, color=style.VARIANT_COLOUR[variant], lw=0.9, ls=":")
    axes[1].set_ylabel("density")

    style.legend(axes[0], loc="upper left", fontsize=style.LEGEND_SIZE - 1)
    for ax, letter in zip(axes, "ab"):
        style.panel_label(ax, letter)
    fig.tight_layout()
    return fig


def f2_gap_not_bulk(ctx):
    """The difference is a gap, not a bulk, and it holds at both N."""
    frame = ctx.frame("spectra_both")
    variants = style.ordered_variants(frame.variant.unique())
    fig, axes = plt.subplots(1, 3, figsize=(7.6, 2.6))
    width = 0.36
    positions = np.arange(len(variants))

    panels = [
        ("abs_bulk", "absolute bulk radius", "median", None),
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
            else:
                values = [frame[(frame.variant == v) & (frame.scale == scale)]
                          [column].median() for v in variants]
            ax.bar(positions + offset, values, width,
                   color=[style.VARIANT_COLOUR[v] for v in variants],
                   alpha=1.0 if scale == 448 else 0.45, edgecolor="white", linewidth=0.5,
                   label=f"N = {scale}")
        ax.set_xticks(positions)
        ax.set_xticklabels([style.VARIANT_LABEL[v].replace(" · ", "\n") for v in variants],
                           rotation=0, fontsize=style.TICK_SIZE - 1)
        ax.set_ylabel(label)
        ax.grid(axis="x", visible=False)

    handles = [plt.Rectangle((0, 0), 1, 1, color="0.35", alpha=a) for a in (1.0, 0.45)]
    axes[2].legend(handles, ["N = 448", "N = 1000"], loc="upper right")
    for ax, letter in zip(axes, "abc"):
        style.panel_label(ax, letter, dx=-0.14)
    fig.tight_layout()
    return fig


# =============================================================================
# Chapter 3 -- methods: the comparison problem (contribution 5)
# =============================================================================
def f3_two_axes(ctx):
    """Neither axis is neutral: the same data, read two ways, and why the normaliser bites.

    Merged from the draft list's F3 and F8. Panel a is the same E0.2 data on both
    matching axes; panel b is the extreme-value forensics that explains why the
    normalisation is not a free choice.
    """
    panel = ctx.frame("e02_panel")
    summary = ctx.frame("e02_axis_summary")
    spectra = ctx.frame("spectra_both")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9))

    axis_style = {"nominal": dict(color="#1f77b4", ls="-"),
                  "effective": dict(color="#c44e52", ls="-")}
    for axis in ("nominal", "effective"):
        curve = panel[panel.axis == axis].sort_values("x")
        kwargs = axis_style[axis]
        axes[0].plot(curve.x, curve.dD_median, label=style.AXIS_SHORT[axis], lw=1.6, **kwargs)
        axes[0].fill_between(curve.x, curve.dD_q25, curve.dD_q75, alpha=0.15,
                             color=kwargs["color"], lw=0)
        row = summary[summary.axis == axis].iloc[0]
        axes[0].plot([row.peak_x], [row.peak_dD], marker="o", ms=4, color=kwargs["color"])
        axes[0].annotate(f"{row.peak_dD:+.0f}", xy=(row.peak_x, row.peak_dD),
                         xytext=(4, 4), textcoords="offset points",
                         fontsize=style.TICK_SIZE, color=kwargs["color"])
        axes[0].plot([row.min_x], [row.min_dD], marker="v", ms=4, color=kwargs["color"])
        axes[0].annotate(f"{row.min_dD:+.0f}", xy=(row.min_x, row.min_dD),
                         xytext=(4, -10), textcoords="offset points",
                         fontsize=style.TICK_SIZE, color=kwargs["color"])
    axes[0].axhline(0, color="0.5", lw=0.8)
    axes[0].set_xlabel("matching coordinate\n(nominal $\\sigma$, or $\\sigma\\cdot$bulk95)")
    axes[0].set_ylabel(r"$\Delta d_{\rm eff}$  (connectome $-$ ER)")
    style.legend(axes[0], loc="lower right", title="axis", title_fontsize=style.LEGEND_SIZE)

    # Panel b: |lambda_1| is a non-concentrating order statistic for the resampling
    # nulls. weight-permuted permutes the exact weight multiset, so its maximum is
    # identical every seed -- the control that shows the effect is the resampling.
    variants = style.ordered_variants(spectra.variant.unique())
    positions = np.arange(len(variants))
    width = 0.36
    for offset, scale, alpha in ((-width / 2, 448, 1.0), (width / 2, 1000, 0.45)):
        spread = [spectra[(spectra.variant == v) & (spectra.scale == scale)]
                  .lambda_max_raw.std(ddof=1)
                  / spectra[(spectra.variant == v) & (spectra.scale == scale)]
                  .lambda_max_raw.mean() for v in variants]
        axes[1].bar(positions + offset, spread, width,
                    color=[style.VARIANT_COLOUR[v] for v in variants], alpha=alpha,
                    edgecolor="white", linewidth=0.5)
    axes[1].set_xticks(positions)
    axes[1].set_xticklabels([style.VARIANT_LABEL[v].replace(" · ", "\n") for v in variants],
                            fontsize=style.TICK_SIZE - 1)
    axes[1].set_ylabel(r"relative s.d. of $|\lambda_1|$ across seeds")
    axes[1].grid(axis="x", visible=False)
    axes[1].annotate("permuted multiset:\nidentical maximum every seed",
                     xy=(1, 0.002), xytext=(0.30, 0.86), textcoords="axes fraction",
                     fontsize=style.TICK_SIZE - 1, color=style.ANNOTATION_COLOUR,
                     arrowprops=dict(arrowstyle="->", lw=0.7))
    for ax, letter in zip(axes, "ab"):
        style.panel_label(ax, letter, dx=-0.12)
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
    "F3": (3, "neither axis is neutral (merged F3 + F8)", f3_two_axes),
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
}

# The workshop subset (5pp, ~4 figures), marked W on FIGURE_LIST.md.
WORKSHOP = ("F1", "F2", "F7", "F12")

assert len(FIGURES) == 14, f"hard cap is 14 figures, registry holds {len(FIGURES)}"

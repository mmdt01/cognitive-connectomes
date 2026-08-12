"""E0.2 figures: the memory panel on both axes, the ceiling, and the sigma_eff fold.

Three figures, vector PDF + 300 dpi PNG, Okabe-Ito palette (matching E0.4's Figure 1):

``fig_panelA_matched``
    Panel A recomputed on effective criticality, **side by side with the original
    nominal-sr version**, so the change is legible. Median across seeds with the
    inter-quartile band; the region outside the overlap is not drawn at all, and the
    effective panel carries an explicit marker where the analysis is censored by the
    end of the swept range.

``fig_absolute_deff``
    Absolute ``d_eff`` per variant on both axes -- not only the difference -- with
    ``d_eff / N`` on the right-hand axis and **the hard ceiling at N drawn**. Every
    memory figure has to show distance-from-ceiling, because all three variants run
    close to it and a shrinking difference can mean the null is saturating rather
    than the connectome degrading.

``fig_sigma_eff``
    The secondary axis, kept honest: (left) ``sigma_eff`` against ``sr`` per variant,
    which shows the fold directly -- it rises, turns over and falls as the tanh gain
    collapses faster than ``sr`` grows; (right) ``d_eff`` against ``sigma_eff`` as a
    *parametric* trajectory traced by ``sr``, with the turning point marked. No
    matched differencing is done on this axis: it is not invertible, so a matched
    grid would be ill-posed.
"""

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from experiments.human.analysis.criticality_matched import common

_INK, _MUT, _GRID = "#111111", "#8a8a8a", "#dddddd"
_POS, _NEG = "#0072B2", "#D55E00"
_RC = {
    "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8.5,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
    "axes.linewidth": 0.7, "xtick.major.width": 0.7, "ytick.major.width": 0.7,
    "axes.edgecolor": _INK, "axes.labelcolor": _INK, "text.color": _INK,
    "xtick.color": _INK, "ytick.color": _INK,
    "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.bbox": "tight",
}


def _save(fig, path_stem) -> None:
    for suffix, kwargs in ((".pdf", {}), (".png", {"dpi": 300})):
        path = path_stem.with_suffix(suffix)
        fig.savefig(path, **kwargs)
        print(f"Saved {path}")
    plt.close(fig)


def _style(ax) -> None:
    ax.grid(True, color=_GRID, lw=0.5, alpha=0.8)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def _label(ax, letter) -> None:
    ax.text(-0.16, 1.10, letter, transform=ax.transAxes, fontsize=10,
            fontweight="bold", va="top", ha="left", color=_INK)


# ---------------------------------------------------------------------------
def fig_panel_a(frames: dict, summaries: dict, path_stem) -> None:
    """Nominal vs effective-criticality Panel A, side by side."""
    order = ["nominal", "effective"]
    with plt.rc_context(_RC):
        fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1), squeeze=False)
        ymax = max(float(np.nanmax(frames[a].dD_q75)) for a in order)
        ymin = min(float(np.nanmin(frames[a].dD_q25)) for a in order)
        pad = 0.08 * (ymax - ymin)
        for ax, axis, letter in zip(axes[0], order, "ab"):
            frame, summary = frames[axis], summaries[axis]
            x = frame.x.to_numpy(float)
            med = frame.dD_median.to_numpy(float)
            ax.axhline(0.0, color=_MUT, lw=0.9, ls="-")
            ax.fill_between(x, frame.dD_q25, frame.dD_q75, color=_INK, alpha=0.15, lw=0)
            ax.fill_between(x, 0, np.clip(med, 0, None), color=_POS, alpha=0.20, lw=0)
            ax.fill_between(x, np.clip(med, None, 0), 0, color=_NEG, alpha=0.20, lw=0)
            ax.plot(x, med, color=_INK, lw=1.6, solid_capstyle="round")
            ax.set_xlabel(common.AXES[axis]["label"], labelpad=1)
            ax.set_ylim(ymin - pad, ymax + pad)
            ax.set_xlim(x[0], x[-1])
            _style(ax)
            _label(ax, letter)
            peak = summary["peak_dD"]
            ax.plot([summary["peak_x"]], [peak], marker="o", ms=4, color=_INK,
                    zorder=5, ls="none")
            if summary.get("peak_at_upper_edge"):
                # The analysis stops before the effect does -- say so on the figure.
                ax.annotate("peak is at the edge of\nthe overlap — still rising",
                            xy=(summary["peak_x"], peak),
                            xytext=(0.40, 0.90), textcoords="axes fraction",
                            fontsize=6.4, color=_NEG, ha="left", va="top",
                            arrowprops=dict(arrowstyle="->", lw=0.7, color=_NEG))
                ax.axvspan(x[-1], x[-1] + 0.02 * (x[-1] - x[0]), color=_NEG,
                           alpha=0.30, lw=0)
            else:
                ax.annotate(f"peak {peak:+.0f}", xy=(summary["peak_x"], peak),
                            xytext=(6, -2), textcoords="offset points", fontsize=6.4,
                            color=_INK)
            title = ("original: matched on nominal $\\sigma$" if axis == "nominal"
                     else "corrected: matched on effective criticality")
            ax.set_title(title, pad=4)
        axes[0][0].set_ylabel(r"$\Delta d_{eff}$ (connectome $-$ ER)", labelpad=2)
        note = (f"Overlap {summaries['effective']['overlap_lo']:.2f}–"
                f"{summaries['effective']['overlap_hi']:.2f} "
                f"({summaries['effective']['fraction_of_full_range']:.0%} of the swept "
                "range); nothing extrapolated. Median of per-seed paired differences, "
                "IQR shaded.")
        fig.text(0.5, -0.10, note, ha="center", va="top", fontsize=6.4, color=_MUT)
        fig.suptitle("Does the memory advantage survive effective-criticality "
                     "matching?", fontsize=9.5, y=1.04)
        fig.tight_layout()
        _save(fig, path_stem)


# ---------------------------------------------------------------------------
def fig_absolute(frames: dict, n_nodes: int, path_stem) -> None:
    """Absolute d_eff per variant on both axes, with the hard ceiling at N."""
    order = ["nominal", "effective"]
    with plt.rc_context(_RC):
        fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1), squeeze=False, sharey=True)
        for ax, axis, letter in zip(axes[0], order, "ab"):
            frame = frames[axis]
            x = frame.x.to_numpy(float)
            for variant in common.VARIANTS:
                col = f"d_eff_{variant}"
                if col not in frame:
                    continue
                ax.plot(x, frame[col], color=common.VARIANT_COLOR[variant], lw=1.5,
                        label=common.VARIANT_TITLE[variant], solid_capstyle="round")
            ax.axhline(n_nodes, color=_NEG, lw=1.1, ls="--")
            ax.text(0.02, n_nodes, f" hard ceiling $d_{{eff}} = N = {n_nodes}$",
                    transform=ax.get_yaxis_transform(), fontsize=6.4, color=_NEG,
                    va="bottom", ha="left")
            ax.set_xlabel(common.AXES[axis]["label"], labelpad=1)
            ax.set_xlim(x[0], x[-1])
            ax.set_ylim(0, n_nodes * 1.12)
            _style(ax)
            _label(ax, letter)
        axes[0][0].set_ylabel(r"$d_{eff}$ (seed median)", labelpad=2)
        secondary = axes[0][1].secondary_yaxis(
            "right", functions=(lambda v: v / n_nodes, lambda v: v * n_nodes))
        secondary.set_ylabel(r"$d_{eff} / N$", labelpad=2)
        secondary.spines["right"].set_visible(True)
        axes[0][0].legend(loc="lower right", frameon=False, handlelength=1.3)
        fig.suptitle("Absolute readout dimensionality and distance from the ceiling",
                     fontsize=9.5, y=1.03)
        fig.tight_layout()
        _save(fig, path_stem)


# ---------------------------------------------------------------------------
def fig_heatmaps(results: dict, path_stem) -> None:
    """The (f, sigma) panels on both axes, with the cross-panel overlay.

    Rows are axes (nominal control on top, effective correction below); columns are
    Panel A (memory), Panel B (generation) and the boundary overlay. The nominal row
    exists to show the pipeline reproduces the published crossing, so that the
    corrected row can be read as a change in the result rather than a change in the
    method. Regions without coverage for every compared variant are left unpainted,
    and the coverage edge is drawn explicitly -- on the extension it is the swept
    sigma_max, no longer the inherited sigma = 6 censoring edge.
    """
    from matplotlib.colors import TwoSlopeNorm
    from experiments.human.analysis.criticality_matched import heatmaps as H

    axes_order = [a for a in ("nominal", "effective") if a in results]
    panel_order = ["dD", "dStraight"]
    with plt.rc_context(_RC):
        fig, axes = plt.subplots(len(axes_order), 3, figsize=(7.4, 2.7 * len(axes_order)),
                                 squeeze=False)
        for row, axis_name in enumerate(axes_order):
            res = results[axis_name]
            xlabel = (r"nominal $\sigma$" if axis_name == "nominal"
                      else r"effective criticality  $\sigma\cdot\mathrm{bulk}_{95}$")
            for col, panel in enumerate(panel_order):
                ax = axes[row][col]
                op = res["ops"].get(panel)
                if op is None:
                    ax.set_visible(False)
                    continue
                piv = op.pivot_table(index="f", columns="spectral_radius", values=panel)
                Z = piv.to_numpy(float)
                fv, xv = piv.index.to_numpy(float), piv.columns.to_numpy(float)
                vmax = float(np.nanmax(np.abs(Z))) or 1e-9
                dx = (xv[1] - xv[0]) if xv.size > 1 else 1.0
                df_ = (fv[1] - fv[0]) if fv.size > 1 else 0.05
                im = ax.imshow(
                    np.ma.masked_invalid(Z), origin="lower", aspect="auto",
                    cmap="RdBu_r", norm=TwoSlopeNorm(vmin=-vmax, vcenter=0.0, vmax=vmax),
                    extent=[xv[0] - dx / 2, xv[-1] + dx / 2,
                            fv[0] - df_ / 2, fv[-1] + df_ / 2])
                fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
                bound = res["bounds"].get(panel, {})
                bx = np.array(sorted(bound), float)
                by = np.array([bound[x] for x in sorted(bound)], float)
                ax.plot(bx, by, color=_INK, lw=1.8, solid_capstyle="round")
                if axis_name == "effective":
                    cov = res["coverage"]
                    ax.plot(cov.x_hi, cov.f, color=_NEG, lw=1.2, ls="--")
                ax.set_xlabel(xlabel, labelpad=1)
                if col == 0:
                    ax.set_ylabel("negative-weight fraction $f$", labelpad=2)
                ax.set_title(("Panel A — memory" if panel == "dD"
                              else "Panel B — generation"), pad=4)
                _style(ax)
                _label(ax, "abcdef"[row * 3 + col])

            ax = axes[row][2]
            for panel, colour, name in (("dD", _POS, "memory $f^*$"),
                                        ("dStraight", _NEG, "generation $f^*$")):
                bound = res["bounds"].get(panel, {})
                bx = np.array(sorted(bound), float)
                by = np.array([bound[x] for x in sorted(bound)], float)
                ok = np.isfinite(by)
                ax.plot(bx[ok], by[ok], color=colour, lw=1.9, label=name,
                        solid_capstyle="round")
            cross = res["crossing"]
            if cross.get("crosses"):
                ax.plot([cross["x"]], [cross["f"]], marker="o", ms=6, color=_INK,
                        ls="none", zorder=5)
                ax.annotate(f"cross\n({cross['x']:.2f}, {cross['f']:.3f})",
                            xy=(cross["x"], cross["f"]), xytext=(6, 8),
                            textcoords="offset points", fontsize=6.4, color=_INK)
            else:
                ax.text(0.5, 0.94, "no crossing within coverage", transform=ax.transAxes,
                        ha="center", va="top", fontsize=6.8, color=_NEG)
            ax.set_xlabel(xlabel, labelpad=1)
            ax.set_ylabel("critical $f^*$", labelpad=2)
            ax.set_ylim(-0.02, 0.52)
            ax.legend(loc="lower right", frameon=False, handlelength=1.3, fontsize=6.4)
            ax.set_title("cross-panel overlay", pad=4)
            _style(ax)
            _label(ax, "abcdef"[row * 3 + 2])

        source = next((res.get("source") for res in results.values()
                       if res.get("source")), "frozen")
        sigma_max = max(
            (float(res["coverage"].sigma_max.max()) for res in results.values()
             if "coverage" in res and "sigma_max" in res["coverage"]), default=6.0)
        if source == "extension":
            caption = (
                "Top row: nominal σ. Bottom row: effective criticality. Both over the "
                f"extended sweep (σ ≤ {sigma_max:g} at every f); dashed red = coverage "
                "edge σ_max·bulk95(f), the limit of the sweep — not extended further. "
                "Contour level = 25% of the largest fully covered cell. The published "
                "nominal crossing (σ = 4.39, f = 0.130) returns when the level is "
                "pinned to σ ≤ 6; over the full sweep the generative panel's own "
                "maximum — f ≈ 0–0.1, σ ≈ 7–11, where ER collapses and the connectome "
                "does not — raises the level and the boundaries no longer meet on that "
                "axis. Unpainted = no coverage for every compared variant.")
        else:
            caption = (
                "Top row: nominal σ (control — reproduces the published crossing). "
                "Bottom row: effective criticality. Dashed red = coverage edge, which "
                "for f > 0 is the σ = 6 censoring edge (the σ = 8 extension was f = 0 "
                "only). Unpainted = no coverage for every compared variant.")
        fig.text(0.5, -0.04, caption, ha="center", va="top", fontsize=6.2, color=_MUT)
        fig.suptitle("Does the memory/generation dissociation survive "
                     "effective-criticality matching?", fontsize=9.5, y=1.02)
        fig.tight_layout()
        _save(fig, path_stem)


def fig_alpha_sweep(peak: pd.DataFrame, ladder: pd.DataFrame, source: pd.DataFrame,
                    frozen_alpha: float, n_nodes: int, path_stem) -> None:
    """Task A: is `d_eff` saturated at the frozen ridge, and where does the ladder live?

    (a) peak ``d_eff/N`` against ``alpha`` with the ceiling drawn -- the saturation
    question; (b) ladder ordering against ``alpha`` per sigma region -- whether the
    ordering is a ridge artifact; (c) ladder ordering along sigma at the frozen alpha
    -- which part of the axis actually carries it.
    """
    region_colour = {"subcritical": "#CC79A7", "near_peak": "#E69F00",
                     "supercritical": "#0072B2", "all_sigma": _INK}
    with plt.rc_context(_RC):
        fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.7), squeeze=False)

        ax = axes[0][0]
        for variant in common.VARIANTS + ["connectome_weight_permuted"]:
            sub = peak[peak.variant == variant].sort_values("alpha")
            if sub.empty:
                continue
            colour = common.VARIANT_COLOR.get(variant, "#D55E00")
            ax.plot(sub.alpha, sub.d_eff_norm, color=colour, lw=1.5,
                    label=common.VARIANT_TITLE.get(variant, "Weight-permuted"))
        ax.axhline(1.0, color=_NEG, lw=1.0, ls="--")
        ax.text(0.02, 1.0, " ceiling $d_{eff}=N$", transform=ax.get_yaxis_transform(),
                fontsize=6.2, color=_NEG, va="bottom", ha="left")
        ax.axvline(frozen_alpha, color=_MUT, lw=1.0, ls=":")
        ax.text(frozen_alpha, 0.03, r" frozen $\alpha$", fontsize=6.2, color=_MUT,
                rotation=90, va="bottom", ha="left")
        ax.set_xscale("log")
        ax.set_xlabel(r"ridge $\alpha$", labelpad=1)
        ax.set_ylabel(r"peak $d_{eff}/N$", labelpad=2)
        ax.set_ylim(0, 1.12)
        ax.legend(loc="lower left", frameon=False, handlelength=1.2, fontsize=6.2)
        ax.set_title("saturation at the peak", pad=4)
        _style(ax)
        _label(ax, "a")

        ax = axes[0][1]
        for region in ["subcritical", "near_peak", "supercritical"]:
            sub = ladder[ladder.region == region].sort_values("alpha")
            if sub.empty:
                continue
            ax.plot(sub.alpha, -sub.spearman_vs_rank, lw=1.5,
                    color=region_colour[region], label=region.replace("_", " "))
        ax.axhline(0.0, color=_MUT, lw=0.9)
        ax.axvline(frozen_alpha, color=_MUT, lw=1.0, ls=":")
        ax.set_xscale("log")
        ax.set_xlabel(r"ridge $\alpha$", labelpad=1)
        ax.set_ylabel("ladder ordering\n(+1 = connectome highest)", labelpad=2)
        ax.set_ylim(-1.1, 1.1)
        ax.legend(loc="lower left", frameon=False, handlelength=1.2, fontsize=6.2)
        ax.set_title(r"ordering vs $\alpha$", pad=4)
        _style(ax)
        _label(ax, "b")

        ax = axes[0][2]
        ax.plot(source.spectral_radius, -source.spearman_vs_rank, color=_INK, lw=1.6,
                marker="o", ms=2.8)
        ax.axhline(0.0, color=_MUT, lw=0.9)
        ax.axvline(3.08, color=_POS, lw=1.0, ls="--")
        ax.text(3.08, -1.02, r" $sr_{crit}$", fontsize=6.2, color=_POS, ha="left")
        ax.set_xlabel(r"spectral radius $\sigma$", labelpad=1)
        ax.set_ylabel("ladder ordering\n(+1 = connectome highest)", labelpad=2)
        ax.set_ylim(-1.1, 1.1)
        ax.set_title(r"ordering vs $\sigma$ (frozen $\alpha$)", pad=4)
        _style(ax)
        _label(ax, "c")

        fig.text(0.5, -0.10,
                 "The published ladder ordering lives only in the supercritical decay "
                 "region: at the peak every variant is at the ceiling and the ordering "
                 "is absent; subcritically it is inverted.",
                 ha="center", va="top", fontsize=6.4, color=_MUT)
        fig.suptitle(r"Task A: $d_{eff}(\alpha)$ — the ceiling is $N$ relative to "
                     r"$\alpha$", fontsize=9.5, y=1.05)
        fig.tight_layout()
        _save(fig, path_stem)


def fig_sigma_eff(traj: pd.DataFrame, path_stem) -> None:
    """The secondary axis: the fold, and d_eff as a parametric trajectory."""
    with plt.rc_context(_RC):
        fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1), squeeze=False)
        ax = axes[0][0]
        for variant, group in traj.groupby("variant"):
            group = group.sort_values("spectral_radius")
            colour = common.VARIANT_COLOR.get(variant, _INK)
            ax.plot(group.spectral_radius, group.sigma_eff, color=colour, lw=1.5,
                    marker="o", ms=2.6, label=common.VARIANT_TITLE.get(variant, variant))
            peak = group[group.is_sigma_eff_peak]
            ax.plot(peak.spectral_radius, peak.sigma_eff, marker="v", ms=5,
                    color=colour, ls="none", zorder=5)
        ax.axhline(1.0, color=_NEG, lw=1.0, ls="--")
        ax.text(0.02, 1.0, r" $\sigma_{eff} = 1$ (never reached on MC states)",
                transform=ax.get_yaxis_transform(), fontsize=6.4, color=_NEG,
                va="bottom", ha="left")
        ax.set_xlabel(r"nominal spectral radius $\sigma$", labelpad=1)
        ax.set_ylabel(r"$\sigma_{eff}$", labelpad=2)
        ax.set_ylim(0, 1.18)
        ax.legend(loc="lower right", frameon=False, handlelength=1.3)
        ax.set_title(r"$\sigma_{eff}$ folds: it is not monotone in $\sigma$", pad=4)
        _style(ax)
        _label(ax, "a")

        ax = axes[0][1]
        for variant, group in traj.groupby("variant"):
            group = group.sort_values("spectral_radius")
            colour = common.VARIANT_COLOR.get(variant, _INK)
            rising = group[group.branch == "rising"]
            folded = group[group.branch == "folded"]
            ax.plot(rising.sigma_eff, rising.d_eff, color=colour, lw=1.6,
                    solid_capstyle="round")
            ax.plot(folded.sigma_eff, folded.d_eff, color=colour, lw=1.4,
                    ls=(0, (4, 2)), solid_capstyle="round")
            peak = group[group.is_sigma_eff_peak]
            ax.plot(peak.sigma_eff, peak.d_eff, marker="v", ms=5, color=colour,
                    ls="none", zorder=5)
        ax.set_xlabel(common.AXES["sigma_eff"]["label"], labelpad=1)
        ax.set_ylabel(r"$d_{eff}$ (seed median)", labelpad=2)
        ax.set_title(r"parametric in $\sigma$: two branches per variant", pad=4)
        _style(ax)
        _label(ax, "b")
        handles = [Line2D([0], [0], color=_MUT, lw=1.6, label="rising branch"),
                   Line2D([0], [0], color=_MUT, lw=1.4, ls=(0, (4, 2)),
                          label="folded branch"),
                   Line2D([0], [0], color=_MUT, marker="v", ms=5, ls="none",
                          label=r"$\sigma_{eff}$ turning point")]
        ax.legend(handles=handles, loc="upper left", frameon=False, handlelength=1.5)
        fig.text(0.5, -0.08,
                 r"$\sigma_{eff}$ is non-monotone in $\sigma$, so it cannot index a "
                 "matched grid: each value is reached twice per variant. Shown "
                 "parametrically, with the fold retained.",
                 ha="center", va="top", fontsize=6.4, color=_MUT)
        fig.suptitle(r"Secondary axis: the nonlinearity-corrected radius $\sigma_{eff}$",
                     fontsize=9.5, y=1.03)
        fig.tight_layout()
        _save(fig, path_stem)


def fig_cross_scale(frames: dict, ladder: pd.DataFrame, path_stem) -> None:
    """N=448 vs N=1000, the three things the finite-size question turns on.

    ``frames`` maps scale -> (matched-axis frame from ``analysis.paired_difference``,
    n_nodes). ``ladder`` is the supercritical per-variant MC table.

    (a) the matched memory advantage at both N -- does the peak stay interior and does
    the advantage hold; (b) ``d_eff/N`` against the hard ceiling -- the point being that
    it is *not* escaped at either N, which is why the decay region rather than the peak
    is what gets read; (c) the supercritical MC ladder, which carries both the margin
    that held (4.40 -> 4.42) and the degree/ER pair that did not swap.
    """
    scales = sorted(frames)
    style = {448: dict(ls="-", lw=1.7), 1000: dict(ls=(0, (4, 2)), lw=1.7)}
    with plt.rc_context(_RC):
        fig, axes = plt.subplots(1, 3, figsize=(7.6, 2.8), squeeze=False)

        # (a) matched memory advantage, normalised by N so the scales are comparable
        ax = axes[0][0]
        for scale in scales:
            frame, n = frames[scale]
            y = frame.dD_median.to_numpy(float) / n
            x = frame.x.to_numpy(float)
            ax.plot(x, y, color=_INK, **style[scale], label=f"N = {n}")
            i = int(np.nanargmax(y))
            ax.plot([x[i]], [y[i]], marker="o", ms=4, color=_INK, ls="none", zorder=5)
        ax.axhline(0.0, color=_MUT, lw=0.9)
        ax.set_xlabel(r"effective criticality  $\sigma\cdot\mathrm{bulk}_{95}$", labelpad=1)
        ax.set_ylabel(r"$\Delta d_{eff}\,/\,N$ (connectome $-$ ER)", labelpad=2)
        ax.legend(loc="upper left", frameon=False, handlelength=1.8)
        ax.set_title("matched advantage, both scales", pad=4)
        _style(ax); _label(ax, "a")

        # (b) distance from the ceiling -- the reason the peak is not the place to read
        ax = axes[0][1]
        for scale in scales:
            frame, n = frames[scale]
            for variant in common.VARIANTS:
                col = f"d_eff_{variant}"
                if col not in frame:
                    continue
                ax.plot(frame.x, frame[col] / n, color=common.VARIANT_COLOR[variant],
                        **style[scale])
        ax.axhline(1.0, color=_NEG, lw=1.1, ls="--")
        ax.text(0.02, 1.0, r" ceiling $d_{eff}=N$", transform=ax.get_yaxis_transform(),
                fontsize=6.2, color=_NEG, va="bottom", ha="left")
        ax.set_ylim(0, 1.15)
        ax.set_xlabel(r"$\sigma\cdot\mathrm{bulk}_{95}$", labelpad=1)
        ax.set_ylabel(r"$d_{eff}\,/\,N$", labelpad=2)
        ax.set_title("the ceiling is not escaped", pad=4)
        _style(ax); _label(ax, "b")

        # (c) supercritical MC ladder at both scales
        ax = axes[0][2]
        variants = [v for v in common.VARIANTS if v in set(ladder.variant)]
        offs = np.linspace(-0.16, 0.16, len(scales))
        for scale, off in zip(scales, offs):
            sub = ladder[ladder.scale == scale].set_index("variant")
            for i, variant in enumerate(variants):
                if variant not in sub.index:
                    continue
                ax.plot([i + off], [sub.loc[variant, "mc"]], marker="o" if scale == 448
                        else "s", ms=5, color=common.VARIANT_COLOR[variant],
                        ls="none", mec="black", mew=0.5)
        for i, variant in enumerate(variants):
            vals = [ladder[(ladder.scale == s) & (ladder.variant == variant)].mc
                    for s in scales]
            vals = [float(v.iloc[0]) for v in vals if len(v)]
            if len(vals) == 2:
                ax.plot([i + offs[0], i + offs[1]], vals, color=_MUT, lw=0.8, zorder=0)
        ax.set_xticks(range(len(variants)))
        ax.set_xticklabels([common.VARIANT_TITLE[v].replace("-", "-\n")
                            for v in variants], fontsize=6.2)
        ax.set_ylabel("supercritical MC (median)", labelpad=2)
        ax.set_title("MC ladder: margin holds", pad=4)
        handles = [Line2D([0], [0], marker="o" if s == 448 else "s", ls="none",
                          color=_MUT, ms=4, label=f"N = {s}") for s in scales]
        ax.legend(handles=handles, loc="upper right", frameon=False, handlelength=1.0)
        _style(ax); _label(ax, "c")

        fig.text(0.5, -0.10,
                 "Solid = N 448, dashed/squares = N 1000. The supercritical margin "
                 "(connectome/ER) is 4.40 at N=448 and 4.42 at N=1000; degree and ER do "
                 "NOT swap, contrary to what bulk95 predicts.",
                 ha="center", va="top", fontsize=6.2, color=_MUT)
        fig.suptitle("Does the memory advantage survive the finite-size question?",
                     fontsize=9.5, y=1.04)
        fig.tight_layout()
        _save(fig, path_stem)


def fig_frontier(front: pd.DataFrame, crit: pd.DataFrame, path_stem) -> None:
    """E0.3: absolute MC and VPT per substrate across the negative-weight sweep.

    Rows are the two metrics, columns the four-variant ladder; one curve per ``f``,
    against **nominal** sigma. Absolute curves need no matched axis -- each substrate is
    shown on its own sigma with its own ``sr_crit(f=0)`` marked -- which is why this
    figure sidesteps the axis question the delta panels cannot (TIER0 §1.1).

    Two things are drawn that a plain curve plot would hide: the metric's hard ceiling
    (so "flat" can be read as saturated or genuinely flat), and the sigma region where
    most seeds sit at the metric's floor, where a difference between substrates is not
    a measurement.
    """
    from matplotlib.cm import ScalarMappable
    from matplotlib.colors import Normalize

    metrics = [m for m in ("mc", "vpt") if m in set(front.metric)]
    ladder = ["connectome", "connectome_weight_permuted", "degree_rewire",
              "erdos_renyi"]
    variants = [v for v in ladder if v in set(front.variant)]
    fvals = np.sort(front.f.unique())
    norm = Normalize(vmin=float(fvals.min()), vmax=float(fvals.max()))
    cmap = plt.get_cmap("viridis")
    label = {"mc": "memory capacity", "vpt": "valid prediction time (Lyapunov)"}

    with plt.rc_context(_RC):
        fig, axes = plt.subplots(len(metrics), len(variants),
                                 figsize=(2.0 * len(variants) + 0.6, 2.5 * len(metrics)),
                                 squeeze=False, sharex=True)
        for row, metric in enumerate(metrics):
            sub_m = front[front.metric == metric]
            ymax = float(sub_m["median"].max()) * 1.08
            for col, variant in enumerate(variants):
                ax = axes[row][col]
                sub = sub_m[sub_m.variant == variant]

                # Where most seeds sit at the floor, a between-substrate difference is
                # not a measurement -- shade it rather than let a curve imply signal.
                floored = (sub.groupby("spectral_radius").frac_at_floor.median() >= 0.5)
                if floored.any():
                    sr = floored.index.to_numpy(float)
                    ax.fill_between(sr, 0, ymax, where=floored.to_numpy(),
                                    color=_MUT, alpha=0.13, lw=0, step="mid")

                for f in fvals:
                    curve = sub[sub.f == f].sort_values("spectral_radius")
                    if curve.empty:
                        continue
                    ax.plot(curve.spectral_radius, curve["median"],
                            color=cmap(norm(f)), lw=1.25, solid_capstyle="round")

                row_crit = crit[(crit.variant == variant) & (crit.f == 0.0)]
                if not row_crit.empty:
                    value = float(row_crit.sr_crit.iloc[0])
                    ax.axvline(value, color=_INK, lw=0.8, ls=":")
                    if row == 0:
                        ax.text(value, ymax * 0.99, r" $sr_{crit}$", fontsize=6,
                                color=_INK, ha="left", va="top")
                ax.set_ylim(0, ymax)
                if row == len(metrics) - 1:
                    ax.set_xlabel(r"nominal $\sigma$", labelpad=1)
                if col == 0:
                    ax.set_ylabel(label.get(metric, metric), labelpad=2)
                if row == 0:
                    ax.set_title(common.VARIANT_TITLE.get(variant, variant), pad=4)
                _style(ax)
                _label(ax, "abcdefgh"[row * len(variants) + col])

        smap = ScalarMappable(norm=norm, cmap=cmap)
        cbar = fig.colorbar(smap, ax=axes, fraction=0.02, pad=0.015)
        cbar.set_label("negative-weight fraction $f$", fontsize=7)
        cbar.ax.tick_params(labelsize=6.5)
        fig.text(0.5, -0.02,
                 "Absolute within-substrate levels — no matched axis and no "
                 "differencing. Dotted line = each substrate's own $sr_{crit}=1/$"
                 r"bulk$_{95}$ at $f=0$; grey band = $\sigma$ where the majority of "
                 "seeds sit at the metric's floor, so a between-substrate difference "
                 "there is not a measurement. Median over 10 seeds (draws averaged "
                 "within a seed).",
                 ha="center", va="top", fontsize=6.2, color=_MUT)
        fig.suptitle("Absolute memory and generation across the negative-weight sweep",
                     fontsize=9.5, y=1.01)
        _save(fig, path_stem)

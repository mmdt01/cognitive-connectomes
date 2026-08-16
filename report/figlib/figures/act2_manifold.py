"""Act II -- the spectrum decomposes the manifold.  Chapter 5.

F4 and F5 are Act II's own claims (the Perron mode is a common mode; sign selects the
basis); F6 carries contribution 6 (PR misses readout-relevant structure).

Owned by session 2 (`report/act2_manifold.md`).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

from report.figlib import style
from report.figlib.figures.common import N_NODES


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

"""Performance comparison plots for v2a-style results frames."""

import pathlib

import matplotlib.figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.reservoir.build import rescale_spectral_radius
from src.reservoir.weights import apply_weight_scheme


_PALETTE = {
    "random_gaussian": "#4c72b0",
    "erdos_renyi": "#dd8452",
    "degree_rewire": "#55a467",
    "connectome": "#c44e52",
}
_LABELS = {
    "random_gaussian": "random Gaussian",
    "erdos_renyi": "Erdős–Rényi",
    "degree_rewire": "degree-preserving rewire",
    "connectome": "C. elegans connectome",
}


def results_comparison(results_df, save_path=None):
    """MC by condition × spectral radius, mean ± std over seeds."""
    spectral_radii = sorted(results_df["spectral_radius"].unique())
    conditions = list(_PALETTE.keys())

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    for condition in conditions:
        sub = results_df[results_df["condition"] == condition]
        if sub.empty:
            continue
        agg = sub.groupby("spectral_radius")["mc"].agg(["mean", "std"]).reset_index()
        ax.errorbar(
            agg["spectral_radius"],
            agg["mean"],
            yerr=agg["std"],
            marker="o",
            capsize=3,
            lw=2,
            color=_PALETTE[condition],
            label=_LABELS[condition],
        )
    ax.set_xlabel("spectral radius")
    ax.set_ylabel("memory capacity")
    ax.set_title("Memory capacity across reservoir topologies")
    ax.set_xticks(spectral_radii)
    ax.legend(loc="best")
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig


def mc_per_lag(results_df, spectral_radius, save_path=None):
    """Mean per-lag squared correlation by condition at one spectral radius."""
    conditions = list(_PALETTE.keys())

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    for condition in conditions:
        sub = results_df[
            (results_df["condition"] == condition)
            & (results_df["spectral_radius"] == spectral_radius)
        ]
        if sub.empty:
            continue
        stacked = np.vstack(sub["mc_per_lag"].values)
        mean = stacked.mean(axis=0)
        std = stacked.std(axis=0)
        lags = np.arange(1, stacked.shape[1] + 1)
        ax.plot(lags, mean, color=_PALETTE[condition], lw=2, label=_LABELS[condition])
        ax.fill_between(
            lags, mean - std, mean + std, color=_PALETTE[condition], alpha=0.18, lw=0
        )
    ax.set_xlabel("lag $k$")
    ax.set_ylabel(r"$r^2$")
    ax.set_title(f"Memory decay by lag (spectral radius = {spectral_radius})")
    ax.legend(loc="upper right")
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig


def mc_vs_spectral_radius(
    results_df: pd.DataFrame,
    save_path: pathlib.Path | None = None,
) -> matplotlib.figure.Figure:
    """Mean MC vs spectral radius per condition, with +/- 1 std seed band.

    One line per condition. Markers at each spectral_radius value in
    the data. Shaded band of width +/- 1 std around each line. Linear
    on both axes. Headline figure for the extended-sweep v2a notebook.
    """
    conditions = [c for c in _PALETTE if c in set(results_df["condition"].unique())]
    spectral_radii = sorted(results_df["spectral_radius"].unique())

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    for condition in conditions:
        sub = results_df[results_df["condition"] == condition]
        if sub.empty:
            continue
        agg = (
            sub.groupby("spectral_radius")["mc"]
            .agg(["mean", "std"])
            .reindex(spectral_radii)
            .reset_index()
        )
        color = _PALETTE[condition]
        ax.plot(
            agg["spectral_radius"],
            agg["mean"],
            marker="o",
            color=color,
            lw=2,
            label=_LABELS[condition],
        )
        ax.fill_between(
            agg["spectral_radius"],
            agg["mean"] - agg["std"],
            agg["mean"] + agg["std"],
            color=color,
            alpha=0.18,
            lw=0,
        )
    ax.set_xlabel("Spectral radius")
    ax.set_ylabel("Memory capacity")
    ax.set_title("Memory capacity vs spectral radius")
    ax.legend(loc="lower right")
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig


def eigenvalue_spectra(
    conditions: dict[str, np.ndarray],
    weight_scheme: str,
    target_spectral_radius: float,
    seed: int,
    save_path: pathlib.Path | None = None,
) -> matplotlib.figure.Figure:
    """Overlay eigenvalue spectra of each condition's W after weight scheme + rescaling.

    Two-panel diagnostic. Left: full spectrum as step histograms (density=True),
    one curve per condition, dashed verticals at +/- target_spectral_radius. Right:
    zoom on the upper-edge region [0.5 * target, 1.05 * target] where the
    depressed-bulk + hub-outlier story shows up — broad-degree conditions
    have a clear gap between bulk and outlier; narrow-degree do not.
    """
    ordered = [c for c in _PALETTE if c in conditions]
    extras = [c for c in conditions if c not in _PALETTE]
    ordered.extend(extras)

    spectra = {}
    for condition in ordered:
        mask = conditions[condition]
        weighted = apply_weight_scheme(mask, weight_scheme, seed=seed)
        rescaled = rescale_spectral_radius(weighted, target_spectral_radius)
        spectra[condition] = np.sort(np.linalg.eigvalsh(rescaled))

    fig, (ax_full, ax_zoom) = plt.subplots(1, 2, figsize=(11, 4.5))

    full_bins = np.linspace(-target_spectral_radius * 1.05, target_spectral_radius * 1.05, 80)
    for condition in ordered:
        color = _PALETTE.get(condition, "#444444")
        label = _LABELS.get(condition, condition)
        ax_full.hist(
            spectra[condition],
            bins=full_bins,
            density=True,
            histtype="step",
            lw=1.6,
            color=color,
            label=label,
        )
    ax_full.axvline(target_spectral_radius, color="black", ls="--", lw=1, alpha=0.6)
    ax_full.axvline(-target_spectral_radius, color="black", ls="--", lw=1, alpha=0.6)
    ax_full.set_xlabel("Eigenvalue")
    ax_full.set_ylabel("Density")
    ax_full.set_title(f"Full spectrum (sr = {target_spectral_radius})")
    ax_full.legend(loc="upper left", fontsize=9)

    top_k = 30
    ranks = np.arange(1, top_k + 1)
    for condition in ordered:
        color = _PALETTE.get(condition, "#444444")
        label = _LABELS.get(condition, condition)
        eigs = spectra[condition]
        top_eigs = np.sort(eigs)[::-1][:top_k]
        ax_zoom.plot(ranks, top_eigs, marker="o", ms=4, lw=1.6, color=color, label=label)
    ax_zoom.axhline(target_spectral_radius, color="black", ls="--", lw=1, alpha=0.6)
    ax_zoom.set_xlabel("Rank (1 = largest)")
    ax_zoom.set_ylabel("Eigenvalue")
    ax_zoom.set_title(f"Top-{top_k} eigenvalues per condition")
    ax_zoom.legend(loc="lower left", fontsize=9)

    fig.suptitle(
        f"Eigenvalue spectra of W after {weight_scheme} weights, rescaled to sr = {target_spectral_radius} (seed = {seed})",
        fontsize=12,
    )
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig


def connectome_vs_null(results_df, spectral_radius, save_path=None):
    """Null-ladder view: connectome vs all three nulls at one spectral radius."""
    conditions = ["connectome", "random_gaussian", "erdos_renyi", "degree_rewire"]
    positions = np.arange(len(conditions))
    jitter_rng = np.random.default_rng(0)

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    for pos, condition in zip(positions, conditions):
        sub = results_df[
            (results_df["condition"] == condition)
            & (results_df["spectral_radius"] == spectral_radius)
        ]
        if sub.empty:
            continue
        values = sub["mc"].values
        color = _PALETTE[condition]
        ax.scatter(
            np.full_like(values, pos, dtype=float) + jitter_rng.uniform(-0.08, 0.08, size=len(values)),
            values,
            color=color,
            alpha=0.7,
            s=40,
            edgecolor="white",
            linewidth=0.5,
            label=_LABELS[condition],
        )
        ax.errorbar(
            pos,
            values.mean(),
            yerr=values.std(),
            fmt="_",
            color="black",
            markersize=22,
            capsize=6,
            lw=1.5,
            zorder=3,
        )
    ax.set_xticks(positions)
    ax.set_xticklabels([])
    ax.tick_params(axis="x", length=0)
    ax.set_ylabel("memory capacity")
    ax.set_title(f"Connectome vs null models (spectral radius = {spectral_radius})")
    ax.legend(loc="lower right")
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig

"""Value/sign structure of weighted recurrent matrices across weight realizations.

Connectome-agnostic companion to ``src.analysis.spectral`` (the spectrum) and
``src.analysis.null_models`` (the binary topology): this module characterises the
**weights themselves** -- their sign pattern, symmetry, and magnitude
distribution -- so a realism ladder of weight schemes (e.g. undirected gaussian ->
directed empirical -> + Dale signs) is legible at a glance.

Every function takes a plain weighted adjacency ``W`` (reservoir convention
``W[i, j]`` = weight j->i), so the same tools apply to any connectome or scheme.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# Diverging palette anchors (shared so the matrix fills and the legend agree).
POSITIVE_COLOR = "#b2182b"  # excitatory (+)
NEGATIVE_COLOR = "#2166ac"  # inhibitory (−)


def plot_weighted_matrices(matrices, condition_keys, condition_titles,
                           node_orders, path, boundaries=None, mode="sign",
                           percentile=98.0, panel_captions=None, suptitle=""):
    """Weighted adjacency heatmaps side by side (red = +, blue = −).

    ``matrices[condition]`` -> weighted 2D array (original node indexing);
    ``node_orders[condition]`` reorders rows/cols (e.g. by community) so block
    structure shows. ``mode="sign"`` (default) colours every edge at full
    saturation by sign -- the right choice for revealing *structure* (symmetry
    across the diagonal ⇒ undirected; a one-colour column ⇒ a Dale-signed neuron)
    without heavy-tailed magnitudes washing sparse edges to near-white.
    ``mode="magnitude"`` instead scales each panel to its own ``percentile`` of
    ``|w|`` (magnitudes otherwise live on the distribution figure).
    """
    n_panels = len(condition_keys)
    fig, axes = plt.subplots(1, n_panels, figsize=(4.0 * n_panels, 4.8),
                             squeeze=False)
    for ax, condition in zip(axes[0], condition_keys):
        weighted = matrices[condition]
        order = node_orders[condition]
        reordered = weighted[np.ix_(order, order)]
        if mode == "sign":
            field, vmax = np.sign(reordered), 1.0
        else:
            nonzero = np.abs(reordered[reordered != 0])
            field = reordered
            vmax = float(np.percentile(nonzero, percentile)) if nonzero.size else 1.0
        ax.imshow(field, cmap="RdBu_r", vmin=-vmax, vmax=vmax,
                  interpolation="nearest")
        if boundaries and boundaries.get(condition):
            for boundary in boundaries[condition]:
                ax.axhline(boundary - 0.5, color="0.5", lw=0.4, alpha=0.4)
                ax.axvline(boundary - 0.5, color="0.5", lw=0.4, alpha=0.4)
        title = condition_titles[condition]
        if panel_captions and panel_captions.get(condition):
            title += f"\n{panel_captions[condition]}"
        ax.set_title(title, fontsize=11)
        ax.set_xticks([])
        ax.set_yticks([])
    legend = [Patch(facecolor=POSITIVE_COLOR, label="excitatory (+)"),
              Patch(facecolor=NEGATIVE_COLOR, label="inhibitory (−)")]
    fig.legend(handles=legend, loc="lower center", ncol=2, fontsize=11,
               frameon=False, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle(suptitle, fontsize=14)
    fig.tight_layout(rect=[0, 0.05, 1, 0.94])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_weight_distributions(weight_arrays, condition_keys, condition_titles,
                              condition_colors, path, bins=60,
                              panel_captions=None, suptitle=""):
    """Per-condition histograms of the nonzero edge weights (log count axis).

    ``weight_arrays[condition]`` -> 1D array of nonzero weights. The log y-axis
    exposes heavy tails; the dashed zero line and per-panel captions make the
    sign balance explicit (symmetric ± vs all-positive vs sparse signed).
    """
    n_panels = len(condition_keys)
    fig, axes = plt.subplots(1, n_panels, figsize=(4.2 * n_panels, 3.7),
                             squeeze=False)
    for ax, condition in zip(axes[0], condition_keys):
        weights = weight_arrays[condition]
        ax.hist(weights, bins=bins, color=condition_colors[condition], alpha=0.85)
        ax.axvline(0, color="0.4", lw=0.9, ls="--")
        ax.set_yscale("log")
        ax.set_title(condition_titles[condition], fontsize=12)
        ax.set_xlabel("edge weight")
        ax.grid(alpha=0.25, which="both")
        if panel_captions and panel_captions.get(condition):
            ax.text(0.97, 0.95, panel_captions[condition], transform=ax.transAxes,
                    ha="right", va="top", fontsize=9,
                    bbox=dict(boxstyle="round", fc="white", ec="0.7", alpha=0.85))
    axes[0][0].set_ylabel("edge count (log)")
    fig.suptitle(suptitle, fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)

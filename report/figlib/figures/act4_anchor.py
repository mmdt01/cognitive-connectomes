"""Act IV -- the anchor.  Chapter 7.

Minimal Act IV: which Yeo networks load the Perron mode. Computed live from the
consensus rather than from a frozen parquet, which is why this is the one figure with no
`sources` entry.
"""

import numpy as np
import matplotlib.pyplot as plt

from report.figlib import style


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

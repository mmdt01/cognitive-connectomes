"""Multi-panel topology overview for a connectome."""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from src.connectomes import ConnectomeData


def connectome_overview(connectome_data: ConnectomeData, save_path=None):
    """Three-panel overview: heatmap, degree distribution, summary stats.

    Returns the ``matplotlib.figure.Figure``.
    """
    adjacency = connectome_data.adjacency
    n_nodes = adjacency.shape[0]
    n_edges = int(adjacency.sum() // 2)
    density = n_edges / (n_nodes * (n_nodes - 1) / 2)
    degrees = adjacency.sum(axis=1)
    mean_degree = degrees.mean()

    graph = nx.from_numpy_array(adjacency)
    clustering = nx.average_clustering(graph)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(adjacency, cmap="binary", interpolation="nearest")
    axes[0].set_title("Adjacency (binary, undirected)")
    axes[0].set_xlabel("neuron index")
    axes[0].set_ylabel("neuron index")

    axes[1].hist(degrees, bins=30, color="#4c72b0", edgecolor="white")
    axes[1].set_yscale("log")
    axes[1].set_title("Degree distribution")
    axes[1].set_xlabel("degree")
    axes[1].set_ylabel("count (log)")

    stats_lines = [
        f"N            : {n_nodes}",
        f"edges        : {n_edges}",
        f"density      : {density:.3%}",
        f"mean degree  : {mean_degree:.2f}",
        f"clustering C : {clustering:.4f}",
    ]
    axes[2].axis("off")
    axes[2].text(
        0.0,
        0.95,
        "\n".join(stats_lines),
        family="monospace",
        fontsize=12,
        va="top",
    )
    axes[2].set_title("Summary")

    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig

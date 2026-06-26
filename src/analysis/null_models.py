"""Graph-structural analysis of binary topologies and their null ladder.

Connectome-agnostic companion to ``src.analysis.spectral``: where that module
characterises the *weighted* recurrent matrix's spectrum, this one characterises
the *binary topology* (the mask, before any weights) on classical graph
descriptors -- degree, clustering, modularity, reciprocity, path structure. The
point is to make legible **what each null rung preserves vs destroys** relative
to the connectome, so the ladder's logic is readable at a glance: rung 0 (random)
destroys everything, and each higher rung restores one more descriptor.

Every function takes a plain binary adjacency ``mask`` (reservoir convention
``mask[i, j] != 0`` = an edge j->i), so the same tools apply to any connectome or
null. Directed graphs are built with ``nx.from_numpy_array(mask, DiGraph)`` -- the
*same* construction the null generators and ``validate_null`` use -- so the
clustering / block quantities computed here are exactly the ones the rungs claim
to preserve.

Scalar metrics (``structural_metrics``):

========================= ====================================================
``n_edges``               directed edge count (self-loops excluded).
``density``               ``n_edges / (N (N-1))``.
``clustering_global``     transitivity of the undirected projection.
``clustering_directed_mean`` mean Fagiolo (2007) directed clustering.
``modularity_q``          directed modularity Q under a fixed partition.
``reciprocity``           fraction of edges that are bidirectional.
``mean_path_length``      mean geodesic over reachable ordered pairs.
``global_efficiency``     mean inverse geodesic over all ordered pairs.
========================= ====================================================

Degree *sequences* (for distribution plots) come from ``degree_sequences``;
they are not seed-averageable, so the driver shows a representative seed.
"""

import networkx as nx
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def degree_sequences(mask: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """``(in_degree, out_degree)`` integer sequences for a binary mask.

    Matches ``validate_null``'s convention: in-degree of node ``i`` is the row
    sum (edges into ``i``); out-degree of node ``j`` is the column sum.
    """
    binary = (mask != 0)
    return binary.sum(axis=1).astype(int), binary.sum(axis=0).astype(int)


def _directed_graph(mask: np.ndarray) -> nx.DiGraph:
    return nx.from_numpy_array((mask != 0).astype(int), create_using=nx.DiGraph)


def _path_metrics(graph: nx.DiGraph, n_nodes: int) -> tuple[float, float]:
    """``(mean_path_length, global_efficiency)`` from one all-pairs BFS pass.

    ``mean_path_length`` averages the geodesic distance over reachable ordered
    pairs (robust to a not-strongly-connected graph); ``global_efficiency``
    averages ``1/distance`` over *all* ordered pairs (unreachable -> 0).
    """
    total_distance = 0.0
    total_inverse = 0.0
    reachable_pairs = 0
    for _source, lengths in nx.all_pairs_shortest_path_length(graph):
        for distance in lengths.values():
            if distance > 0:
                total_distance += distance
                total_inverse += 1.0 / distance
                reachable_pairs += 1
    denom = n_nodes * (n_nodes - 1)
    mean_path = total_distance / reachable_pairs if reachable_pairs else 0.0
    efficiency = total_inverse / denom if denom else 0.0
    return mean_path, efficiency


def structural_metrics(mask: np.ndarray,
                       community_partition: list | None = None) -> dict:
    """Scalar graph-structural descriptors for a binary directed mask."""
    binary = (mask != 0).astype(int)
    n_nodes = binary.shape[0]
    n_edges = int(binary.sum())
    graph = _directed_graph(binary)

    reciprocal_edges = int((binary & binary.T).sum())
    undirected_projection = nx.from_numpy_array(binary)  # OR-symmetrised

    modularity_q = (
        float(nx.community.modularity(graph, community_partition))
        if community_partition is not None else float("nan")
    )
    mean_path, efficiency = _path_metrics(graph, n_nodes)

    return dict(
        n_edges=n_edges,
        density=n_edges / (n_nodes * (n_nodes - 1)),
        clustering_global=float(nx.transitivity(undirected_projection)),
        clustering_directed_mean=float(nx.average_clustering(graph)),
        modularity_q=modularity_q,
        reciprocity=reciprocal_edges / n_edges if n_edges else 0.0,
        mean_path_length=mean_path,
        global_efficiency=efficiency,
    )


def normalize_to_ladder(metric_value: float, connectome_value: float,
                        random_value: float) -> float:
    """Map a metric onto ``0`` = as-random, ``1`` = matches-connectome.

    ``(value - random) / (connectome - random)``, sign-agnostic. Degenerate
    when the connectome and the random reference coincide (returns ``nan``).
    """
    span = connectome_value - random_value
    if abs(span) < 1e-12:
        return float("nan")
    return (metric_value - random_value) / span


# ---------------------------------------------------------------------------
# Plots (generic over keys; the driver supplies titles + colours)
# ---------------------------------------------------------------------------
def _ccdf(degrees: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Complementary CDF: sorted degrees and ``P(K >= k)``."""
    ordered = np.sort(degrees)
    ccdf = 1.0 - np.arange(ordered.size) / ordered.size
    return ordered, ccdf


def plot_degree_distributions(degree_data, variant_keys, variant_titles,
                              variant_colors, connectome_key, path, suptitle=""):
    """In/out-degree CCDFs (log-log), connectome vs each variant overlaid.

    ``degree_data[variant]`` -> ``(in_degree_array, out_degree_array)``. Variants
    that preserve the degree sequence (rungs 2-4) trace the connectome curve
    exactly -- the overlay makes that preservation visible.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    for axis, (channel, title) in zip(axes, enumerate(["in-degree", "out-degree"])):
        for variant in variant_keys:
            degrees = degree_data[variant][channel]
            positive = degrees[degrees > 0]
            if positive.size == 0:
                continue
            values, ccdf = _ccdf(positive)
            is_connectome = variant == connectome_key
            # Connectome drawn thick and *underneath* so the degree-preserving
            # rungs (2-4) visibly trace its tail on top, confirming preservation.
            axis.step(
                values, ccdf, where="post", color=variant_colors[variant],
                lw=3.2 if is_connectome else 1.3,
                alpha=1.0 if is_connectome else 0.85,
                zorder=1 if is_connectome else 2,
                label=variant_titles[variant],
            )
        axis.set_xscale("log")
        axis.set_yscale("log")
        axis.set_xlabel(f"{title} k")
        axis.set_title(title, fontsize=10)
        axis.grid(alpha=0.25, which="both")
    axes[0].set_ylabel("P(K ≥ k)")
    axes[1].legend(fontsize=7, framealpha=0.9, loc="lower left")
    fig.suptitle(suptitle, fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_metric_bars(seed_values, metric_keys, metric_titles, variant_keys,
                     variant_titles, variant_colors, connectome_key, path,
                     ncols=4, suptitle=""):
    """One panel per metric; bars = variants, height = seed-mean.

    ``seed_values[(metric, variant)]`` -> 1D array of per-seed values (the
    connectome's is length 1). Nulls get an error bar (std) and scattered seed
    points; the connectome is drawn as a distinct bar plus a dashed reference
    line across the panel, so each null's deviation from it is immediate.
    """
    nrows = int(np.ceil(len(metric_keys) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(3.3 * ncols, 3.0 * nrows),
                             squeeze=False)
    flat_axes = axes.ravel()
    x = np.arange(len(variant_keys))
    for index, mkey in enumerate(metric_keys):
        ax = flat_axes[index]
        means = np.array([seed_values[(mkey, v)].mean() for v in variant_keys])
        stds = np.array([seed_values[(mkey, v)].std() for v in variant_keys])
        colors = [variant_colors[v] for v in variant_keys]
        ax.bar(x, means, color=colors, yerr=stds, capsize=2,
               error_kw=dict(lw=0.8, alpha=0.6))
        for xi, v in zip(x, variant_keys):
            points = seed_values[(mkey, v)]
            if points.size > 1:
                ax.scatter(np.full(points.size, xi), points, s=5,
                           color="0.2", alpha=0.4, zorder=3)
        connectome_value = seed_values[(mkey, connectome_key)].mean()
        ax.axhline(connectome_value, color="black", lw=0.9, ls="--", alpha=0.7,
                   zorder=1)
        ax.set_xticks(x)
        ax.set_xticklabels([variant_titles[v] for v in variant_keys],
                           rotation=45, ha="right", fontsize=7)
        ax.set_title(metric_titles[index], fontsize=9)
        ax.grid(axis="y", alpha=0.25)
    for spare in flat_axes[len(metric_keys):]:
        spare.axis("off")
    fig.suptitle(suptitle, fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_preservation_heatmap(normalized, metric_keys, metric_titles,
                              column_keys, column_titles, path, suptitle="",
                              figsize=None, annotation_fontsize=7,
                              label_fontsize=8, title_fontsize=11,
                              cbar_fontsize=8):
    """Rung x metric staircase, coloured ``0`` = as-random, ``1`` = connectome.

    ``normalized[(metric, column)]`` -> float in roughly ``[0, 1]`` (the output
    of ``normalize_to_ladder``). Reading left->right, cells turn green as each
    rung restores another descriptor; rows that stay pale flag features the
    ladder never recovers. The font/size kwargs let a driver render both a
    compact tier figure and a projection-ready slide variant from one helper.
    """
    matrix = np.array([[normalized[(m, c)] for c in column_keys]
                       for m in metric_keys])
    if figsize is None:
        figsize = (1.15 * len(column_keys) + 2.2, 0.6 * len(metric_keys) + 1.8)
    fig, ax = plt.subplots(figsize=figsize)
    image = ax.imshow(matrix, cmap="RdYlGn", vmin=0.0, vmax=1.0, aspect="auto")
    ax.set_xticks(np.arange(len(column_keys)))
    ax.set_xticklabels([column_titles[c] for c in column_keys], rotation=45,
                       ha="right", fontsize=label_fontsize)
    ax.set_yticks(np.arange(len(metric_keys)))
    ax.set_yticklabels([metric_titles[i] for i in range(len(metric_keys))],
                       fontsize=label_fontsize)
    for i in range(len(metric_keys)):
        for j in range(len(column_keys)):
            value = matrix[i, j]
            label = "—" if np.isnan(value) else f"{value:.2f}"
            ax.text(j, i, label, ha="center", va="center",
                    fontsize=annotation_fontsize, color="0.15")
    cbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("preserved (0 = random, 1 = connectome)",
                   fontsize=cbar_fontsize)
    cbar.ax.tick_params(labelsize=cbar_fontsize)
    ax.set_title(suptitle, fontsize=title_fontsize)
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def community_order(community_partition) -> tuple[np.ndarray, list[int]]:
    """Node ordering that makes communities contiguous, + block boundaries.

    ``community_partition`` is a list of sets/iterables of node indices (e.g. a
    Louvain partition). Returns ``(order, boundaries)`` where ``order`` lists node
    indices grouped community-by-community (largest community first) and
    ``boundaries`` holds the cumulative block edges (for drawing module dividers).
    """
    blocks = sorted((sorted(int(n) for n in block) for block in community_partition),
                    key=len, reverse=True)
    order = np.array([node for block in blocks for node in block], dtype=int)
    boundaries, running = [], 0
    for block in blocks[:-1]:
        running += len(block)
        boundaries.append(running)
    return order, boundaries


def plot_adjacency_ladder(masks, variant_keys, variant_titles, node_order,
                          path, boundaries=None, suptitle="", edge_color="black"):
    """Community-ordered adjacency spy-plots, side by side -- the "ladder of pictures".

    ``masks[variant]`` -> binary 2D array (original node indexing); ``node_order``
    reorders rows/cols so a fixed partition's communities are contiguous, so the
    connectome's diagonal blocks are visible and one can watch them dissolve
    (random) and snap back (modularity). ``boundaries`` (optional) draws faint
    module dividers. The most intuitive single view of the ladder -- no axes to
    read, just the wiring.
    """
    n_panels = len(variant_keys)
    fig, axes = plt.subplots(1, n_panels, figsize=(3.1 * n_panels, 3.5),
                             squeeze=False)
    cmap = matplotlib.colors.ListedColormap(["white", edge_color])
    for ax, variant in zip(axes[0], variant_keys):
        reordered = (masks[variant] != 0).astype(int)[np.ix_(node_order, node_order)]
        ax.imshow(reordered, cmap=cmap, vmin=0, vmax=1, interpolation="nearest")
        if boundaries:
            for boundary in boundaries:
                ax.axhline(boundary - 0.5, color="#d62728", lw=0.5, alpha=0.45)
                ax.axvline(boundary - 0.5, color="#d62728", lw=0.5, alpha=0.45)
        ax.set_title(variant_titles[variant], fontsize=11)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle(suptitle, fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)

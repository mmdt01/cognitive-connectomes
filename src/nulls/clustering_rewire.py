"""Clustering-preserving rewire (rung 3).

Preserves N, edge count, AND each node's exact degree (configuration-model
class), AND constrains the global clustering coefficient (triangle density)
to stay within ``tolerance`` of the input's. Implemented via constrained
double-edge swaps with incremental triangle counting.

For each proposed swap (u,v),(x,y) -> (u,y),(x,v):
    triangles_destroyed = |N(u) ∩ N(v)| + |N(x) ∩ N(y)|   (pre-swap)
    triangles_created   = |N(u) ∩ N(y)| + |N(x) ∩ N(v)|   (post-swap)
    delta = triangles_created - triangles_destroyed

The swap is accepted iff the resulting cumulative triangle count stays
within ``tolerance`` of the initial count; otherwise reverted.

Endpoint orientations are randomised per draw so that the simple
"v-y same-block / triangle-balanced" check covers all four endpoint
matchings symmetrically across draws — same convention as
``modularity_rewire``.
"""

import warnings

import networkx as nx
import numpy as np


def _count_common_neighbors(graph: nx.Graph, a: int, b: int) -> int:
    """Triangles through edge (a, b) — counted as |N(a) ∩ N(b)|."""
    return len(set(graph[a]) & set(graph[b]))


def generate(
    adjacency: np.ndarray,
    seed: int,
    tolerance: float = 0.05,
    n_swaps_multiplier: int = 10,
    max_attempts_multiplier: int = 100,
    return_diagnostics: bool = False,
    **kwargs,
) -> np.ndarray | tuple[np.ndarray, dict]:
    """Degree-preserving rewire that also preserves the global clustering
    coefficient (triangle density) within ``tolerance``.

    Parameters
    ----------
    adjacency
        Binary symmetric matrix to rewire (zero diagonal).
    seed
        Seed for the rewire RNG.
    tolerance
        Maximum allowed relative drift in total triangle count from the
        initial count; per-swap acceptance criterion is
        ``abs(T_current + delta - T_initial) / T_initial <= tolerance``.
    n_swaps_multiplier
        Target accepted swaps as a multiple of edge count (default 10,
        matching ``degree_rewire``).
    max_attempts_multiplier
        Hard cap on attempted swaps as a multiple of the swap target.
    return_diagnostics
        If True, return ``(adjacency, diagnostics_dict)``.

    Notes
    -----
    Expected acceptance rate on biological networks: ~5–20%. A warning is
    issued if it drops below 1% (the constraint may be too tight at this
    tolerance); the function still returns whatever swaps were accepted.
    """
    graph = nx.from_numpy_array(adjacency)
    n_edges = graph.number_of_edges()
    n_swaps_target = n_swaps_multiplier * n_edges
    max_attempts = max_attempts_multiplier * n_swaps_target

    triangles_dict = nx.triangles(graph)
    T_initial = sum(triangles_dict.values()) // 3
    if T_initial == 0:
        raise ValueError(
            "Input has zero triangles; clustering-preserving rewire is not "
            "meaningful for triangle-free graphs."
        )
    T_current = T_initial

    rng = np.random.default_rng(seed)
    edges = list(graph.edges())

    n_accepted = 0
    n_attempted = 0

    while n_accepted < n_swaps_target and n_attempted < max_attempts:
        n_attempted += 1

        i, j = (int(k) for k in rng.choice(len(edges), size=2, replace=False))
        a, b = edges[i]
        c, d = edges[j]
        if rng.random() < 0.5:
            a, b = b, a
        if rng.random() < 0.5:
            c, d = d, c
        u, v, x, y = a, b, c, d

        if len({u, v, x, y}) != 4:
            continue
        if graph.has_edge(u, y) or graph.has_edge(x, v):
            continue

        T_destroyed = (
            _count_common_neighbors(graph, u, v)
            + _count_common_neighbors(graph, x, y)
        )

        graph.remove_edge(u, v)
        graph.remove_edge(x, y)
        graph.add_edge(u, y)
        graph.add_edge(x, v)

        T_created = (
            _count_common_neighbors(graph, u, y)
            + _count_common_neighbors(graph, x, v)
        )

        delta = T_created - T_destroyed
        T_new = T_current + delta

        if abs(T_new - T_initial) / T_initial <= tolerance:
            edges[i] = (u, y)
            edges[j] = (x, v)
            T_current = T_new
            n_accepted += 1
        else:
            graph.remove_edge(u, y)
            graph.remove_edge(x, v)
            graph.add_edge(u, v)
            graph.add_edge(x, y)

    acceptance_rate = n_accepted / max(n_attempted, 1)
    if acceptance_rate < 0.01:
        warnings.warn(
            f"clustering_rewire: acceptance rate {acceptance_rate:.4f} "
            f"below 1% — constraint may be too tight at tolerance={tolerance}. "
            f"Accepted {n_accepted}/{n_swaps_target} target swaps.",
            RuntimeWarning,
            stacklevel=2,
        )

    result = nx.to_numpy_array(graph)

    if return_diagnostics:
        diagnostics = {
            "acceptance_rate": acceptance_rate,
            "n_accepted": n_accepted,
            "n_attempted": n_attempted,
            "T_initial": int(T_initial),
            "T_final": int(T_current),
        }
        return result, diagnostics

    return result

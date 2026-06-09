"""Clustering-preserving rewire (rung 3).

Preserves N, edge count, AND each node's exact degree (configuration-model
class), AND constrains the global clustering coefficient (triangle density)
to stay within ``tolerance`` of the input's. Implemented via constrained
double-edge swaps with incremental triangle counting.

Two modes (selected by the ``directed`` kwarg, mirroring ``degree_rewire``):

* ``directed=False`` (default, v2a): undirected double-edge swaps; preserves
  the undirected degree sequence and the global clustering coefficient
  (transitivity) within ``tolerance``.
* ``directed=True`` (v2b/v2d): directed two-edge "head-swaps"
  ``a->b, c->d  =>  a->d, c->b`` that preserve every node's in- and
  out-degree, accepted only if the mean Fagiolo (2007) directed clustering
  coefficient stays within ``tolerance`` of the input's. Only nodes adjacent
  (in either direction) to the four swap endpoints can change clustering, so
  the per-swap update recomputes clustering for that affected set and
  periodically resyncs against a full recompute.

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
    directed: bool = False,
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
        Binary matrix to rewire (zero diagonal). Symmetric for the
        undirected mode; may be directed (asymmetric) for ``directed=True``.
        Treated as binary via ``adjacency != 0``.
    seed
        Seed for the rewire RNG.
    directed
        If False (default), undirected mode (preserves the undirected degree
        sequence and transitivity). If True, directed mode (preserves in- and
        out-degree sequences and mean Fagiolo directed clustering).
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
    if directed:
        return _generate_directed(
            adjacency,
            seed,
            tolerance,
            n_swaps_multiplier,
            max_attempts_multiplier,
            return_diagnostics,
        )

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


def _generate_directed(
    adjacency: np.ndarray,
    seed: int,
    tolerance: float,
    n_swaps_multiplier: int,
    max_attempts_multiplier: int,
    return_diagnostics: bool,
) -> np.ndarray | tuple[np.ndarray, dict]:
    """Directed clustering-preserving rewire.

    Two-edge head-swaps ``a->b, c->d  =>  a->d, c->b`` preserve every node's
    in- and out-degree exactly. A swap is accepted only if the mean Fagiolo
    (2007) directed clustering coefficient stays within ``tolerance`` of the
    input's. Only nodes adjacent (in either direction) to {a, b, c, d} can
    change clustering, so each accepted/proposed swap recomputes clustering
    for that affected set; a full recompute every ``n_edges`` accepted swaps
    resyncs the running mean against ``nx.average_clustering`` to guard
    against drift.
    """
    binary = (adjacency != 0).astype(int)
    graph = nx.from_numpy_array(binary, create_using=nx.DiGraph)
    n_nodes = graph.number_of_nodes()
    n_edges = graph.number_of_edges()
    n_swaps_target = n_swaps_multiplier * n_edges
    max_attempts = max_attempts_multiplier * n_swaps_target

    clustering = nx.clustering(graph)  # node -> Fagiolo directed clustering
    sum_clustering = sum(clustering.values())
    mean_initial = sum_clustering / n_nodes
    if mean_initial == 0:
        raise ValueError(
            "Input has zero directed clustering; clustering-preserving rewire "
            "is not meaningful for triangle-free graphs."
        )

    rng = np.random.default_rng(seed)
    edges = list(graph.edges())
    resync_interval = max(n_edges, 1)

    n_accepted = 0
    n_attempted = 0
    since_resync = 0

    while n_accepted < n_swaps_target and n_attempted < max_attempts:
        n_attempted += 1

        i, j = (int(k) for k in rng.choice(len(edges), size=2, replace=False))
        a, b = edges[i]  # directed edge a -> b
        c, d = edges[j]  # directed edge c -> d

        if len({a, b, c, d}) != 4:
            continue
        if graph.has_edge(a, d) or graph.has_edge(c, b):
            continue

        # Affected nodes: the four endpoints plus everything adjacent to them
        # (in either direction), collected both before and after the swap so
        # newly-formed adjacencies are included. A superset of the truly
        # affected set is fine — unaffected nodes recompute to the same value.
        affected = {a, b, c, d}
        for node in (a, b, c, d):
            affected.update(graph.succ[node])
            affected.update(graph.pred[node])

        graph.remove_edge(a, b)
        graph.remove_edge(c, d)
        graph.add_edge(a, d)
        graph.add_edge(c, b)

        for node in (a, b, c, d):
            affected.update(graph.succ[node])
            affected.update(graph.pred[node])

        clustering_new = nx.clustering(graph, affected)
        delta = sum(clustering_new[node] - clustering[node] for node in affected)
        mean_new = (sum_clustering + delta) / n_nodes

        if abs(mean_new - mean_initial) / mean_initial <= tolerance:
            for node in affected:
                clustering[node] = clustering_new[node]
            sum_clustering += delta
            edges[i] = (a, d)
            edges[j] = (c, b)
            n_accepted += 1
            since_resync += 1
            if since_resync >= resync_interval:
                clustering = nx.clustering(graph)
                sum_clustering = sum(clustering.values())
                since_resync = 0
        else:
            graph.remove_edge(a, d)
            graph.remove_edge(c, b)
            graph.add_edge(a, b)
            graph.add_edge(c, d)

    acceptance_rate = n_accepted / max(n_attempted, 1)
    if acceptance_rate < 0.01:
        warnings.warn(
            f"clustering_rewire(directed=True): acceptance rate "
            f"{acceptance_rate:.4f} below 1% — constraint may be too tight at "
            f"tolerance={tolerance}. Accepted {n_accepted}/{n_swaps_target} "
            f"target swaps.",
            RuntimeWarning,
            stacklevel=2,
        )

    result = nx.to_numpy_array(graph, dtype=float)
    mean_final = float(nx.average_clustering(graph))

    if return_diagnostics:
        diagnostics = {
            "directed": True,
            "acceptance_rate": acceptance_rate,
            "n_accepted": n_accepted,
            "n_attempted": n_attempted,
            "clustering_initial": float(mean_initial),
            "clustering_final": mean_final,
        }
        return result, diagnostics

    return result

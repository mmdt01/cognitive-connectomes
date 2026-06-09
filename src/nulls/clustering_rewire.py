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


def _directed_triangle_counts(symmetrised: np.ndarray) -> np.ndarray:
    """Per-node directed-triangle counts ``(S^3)_ii`` for ``S = A + A.T``.

    This is exactly networkx's directed-triangle count (the set-intersection
    count in ``_directed_triangles_and_degree_iter`` equals ``(S^3)_ii`` with
    reciprocal edges weighted by their multiplicity in ``S``).
    """
    s_squared = symmetrised @ symmetrised
    return np.einsum("ik,ik->i", symmetrised, s_squared).astype(np.int64)


def _directed_clustering_vector(
    triangle_counts: np.ndarray, deg_term: np.ndarray, reciprocal: np.ndarray
) -> np.ndarray:
    """Per-node Fagiolo directed clustering from triangle counts and degrees.

    ``C_i = (S^3)_ii / (2 * (d_tot_i*(d_tot_i - 1) - 2*d_recip_i))``, matching
    networkx (zero where the denominator is non-positive). ``deg_term`` is the
    constant ``d_tot*(d_tot - 1)``; ``reciprocal`` is the per-node reciprocal
    degree (the only degree term a swap changes).
    """
    denominator = 2 * (deg_term - 2 * reciprocal)
    return np.where(denominator > 0, triangle_counts / denominator, 0.0)


def _generate_directed(
    adjacency: np.ndarray,
    seed: int,
    tolerance: float,
    n_swaps_multiplier: int,
    max_attempts_multiplier: int,
    return_diagnostics: bool,
) -> np.ndarray | tuple[np.ndarray, dict]:
    """Directed clustering-preserving rewire (incremental, numpy).

    Two-edge head-swaps ``a->b, c->d  =>  a->d, c->b`` preserve every node's
    in- and out-degree exactly. A swap is accepted only if the mean Fagiolo
    (2007) directed clustering coefficient stays within ``tolerance`` of the
    input's.

    Maintains the symmetrised matrix ``S = A + A.T`` and the per-node triangle
    counts ``t = (S^3)_ii`` incrementally. A head-swap toggles four symmetric
    ``S`` pairs; toggling pair ``{p, q}`` by ``delta`` changes triangle counts
    by exactly ``delta * (S^2)_pq`` at ``p`` and ``q`` and ``delta * S_pw*S_wq``
    at each common neighbour ``w`` (here scaled by 2 because ``t`` stores the
    un-halved ``(S^3)_ii``). The denominator changes only for the four
    endpoints (via their reciprocal degree; total degree is swap-invariant),
    so each proposed swap costs a handful of O(N) vector operations rather than
    a per-node clustering recompute. A full recompute every ``n_edges``
    accepted swaps resyncs the running mean and guards against drift.
    """
    A = (adjacency != 0).astype(np.int64)
    np.fill_diagonal(A, 0)
    n_nodes = A.shape[0]
    n_edges = int(A.sum())
    n_swaps_target = n_swaps_multiplier * n_edges
    max_attempts = max_attempts_multiplier * n_swaps_target

    symmetrised = A + A.T  # entries in {0, 1, 2}
    total_degree = symmetrised.sum(axis=1)  # in + out; invariant under swaps
    deg_term = total_degree * (total_degree - 1)  # constant
    reciprocal = (A * A.T).sum(axis=1)  # per-node reciprocal degree; varies

    triangle_counts = _directed_triangle_counts(symmetrised)
    clustering = _directed_clustering_vector(triangle_counts, deg_term, reciprocal)
    sum_clustering = float(clustering.sum())
    mean_initial = sum_clustering / n_nodes
    if mean_initial == 0:
        raise ValueError(
            "Input has zero directed clustering; clustering-preserving rewire "
            "is not meaningful for triangle-free graphs."
        )

    rng = np.random.default_rng(seed)
    edges = [(int(u), int(v)) for u, v in np.argwhere(A > 0)]
    resync_interval = max(n_edges, 1)

    n_accepted = 0
    n_attempted = 0
    since_resync = 0
    max_drift = 0.0

    while n_accepted < n_swaps_target and n_attempted < max_attempts:
        n_attempted += 1

        i, j = (int(k) for k in rng.choice(len(edges), size=2, replace=False))
        a, b = edges[i]  # directed edge a -> b
        c, d = edges[j]  # directed edge c -> d

        if len({a, b, c, d}) != 4:
            continue
        if A[a, d] or A[c, b]:
            continue

        # Snapshot everything a reverted swap must restore.
        s_cells = [(a, b), (b, a), (c, d), (d, c), (a, d), (d, a), (c, b), (b, c)]
        s_backup = [int(symmetrised[p, q]) for p, q in s_cells]
        recip_backup = (
            int(reciprocal[a]),
            int(reciprocal[b]),
            int(reciprocal[c]),
            int(reciprocal[d]),
        )
        triangle_backup: dict[int, int] = {}
        touched: set[int] = set()

        # Apply the four S-pair toggles, updating S and the triangle counts.
        for p, q, delta in ((a, b, -1), (c, d, -1), (a, d, 1), (c, b, 1)):
            contributions = symmetrised[p] * symmetrised[:, q]  # S_pw * S_wq
            s_squared_pq = int(contributions.sum())  # (S^2)_pq
            for node in (p, q):
                if node not in triangle_backup:
                    triangle_backup[node] = int(triangle_counts[node])
            triangle_counts[p] += 2 * delta * s_squared_pq
            triangle_counts[q] += 2 * delta * s_squared_pq
            touched.add(p)
            touched.add(q)
            for w in np.nonzero(contributions)[0]:
                w = int(w)
                if w not in triangle_backup:
                    triangle_backup[w] = int(triangle_counts[w])
                triangle_counts[w] += 2 * delta * int(contributions[w])
                touched.add(w)
            symmetrised[p, q] += delta
            symmetrised[q, p] += delta

        # Reciprocal-degree update. The reverse edges (b->a, d->c, d->a, b->c)
        # are not among the swapped cells, so their presence in A is stable.
        if A[b, a]:
            reciprocal[a] -= 1
            reciprocal[b] -= 1
        if A[d, c]:
            reciprocal[c] -= 1
            reciprocal[d] -= 1
        if A[d, a]:
            reciprocal[a] += 1
            reciprocal[d] += 1
        if A[b, c]:
            reciprocal[c] += 1
            reciprocal[b] += 1
        touched.update((a, b, c, d))

        touched_idx = np.fromiter(touched, dtype=np.int64, count=len(touched))
        clustering_touched = _directed_clustering_vector(
            triangle_counts[touched_idx], deg_term[touched_idx], reciprocal[touched_idx]
        )
        sum_new = sum_clustering - float(clustering[touched_idx].sum()) + float(
            clustering_touched.sum()
        )
        mean_new = sum_new / n_nodes

        if abs(mean_new - mean_initial) / mean_initial <= tolerance:
            clustering[touched_idx] = clustering_touched
            sum_clustering = sum_new
            A[a, b] = 0
            A[c, d] = 0
            A[a, d] = 1
            A[c, b] = 1
            edges[i] = (a, d)
            edges[j] = (c, b)
            n_accepted += 1
            since_resync += 1
            if since_resync >= resync_interval:
                triangle_counts = _directed_triangle_counts(symmetrised)
                clustering = _directed_clustering_vector(
                    triangle_counts, deg_term, reciprocal
                )
                resynced = float(clustering.sum())
                max_drift = max(max_drift, abs(resynced - sum_clustering))
                sum_clustering = resynced
                since_resync = 0
        else:
            for (p, q), value in zip(s_cells, s_backup):
                symmetrised[p, q] = value
            for node, value in triangle_backup.items():
                triangle_counts[node] = value
            reciprocal[a], reciprocal[b], reciprocal[c], reciprocal[d] = recip_backup

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
    if max_drift > 1e-6 * n_nodes:
        warnings.warn(
            f"clustering_rewire(directed=True): incremental running mean drifted "
            f"from the full recompute by {max_drift:.3e} (sum over {n_nodes} "
            f"nodes) — the incremental update may be inconsistent.",
            RuntimeWarning,
            stacklevel=2,
        )

    result = A.astype(float)
    triangle_counts = _directed_triangle_counts(A + A.T)
    mean_final = float(
        _directed_clustering_vector(triangle_counts, deg_term, reciprocal).sum()
        / n_nodes
    )

    if return_diagnostics:
        diagnostics = {
            "directed": True,
            "acceptance_rate": acceptance_rate,
            "n_accepted": n_accepted,
            "n_attempted": n_attempted,
            "clustering_initial": float(mean_initial),
            "clustering_final": mean_final,
            "max_running_mean_drift": float(max_drift),
        }
        return result, diagnostics

    return result

"""Modularity-preserving rewire (rung 4).

Preserves N, edge count, AND each node's exact degree, AND the
intra-/inter-community edge counts of a fixed partition (the "block
structure"). Implemented via block-constrained double-edge swaps.

Two modes (selected by the ``directed`` kwarg, mirroring ``degree_rewire``):

* ``directed=False`` (default, v2a): undirected double-edge swaps. A swap
  (u,v),(x,y) -> (u,y),(x,v) preserves the per-block-pair edge count iff
  ``block(v) == block(y)``. With random endpoint orientation per draw, all
  four single-equality matchings ({b(v)==b(y), b(u)==b(x), b(v)==b(x),
  b(u)==b(y)}) are sampled across draws — each is a valid swap orientation
  under its corresponding implicit relabelling.
* ``directed=True`` (v2b/v2d): directed two-edge "head-swaps"
  ``a->b, c->d  =>  a->d, c->b`` that preserve every node's in- and
  out-degree. Such a swap preserves the *directed* block edge-count matrix
  exactly iff the two tails share a block (``block(a) == block(c)``) or the
  two heads share a block (``block(b) == block(d)``); accepting only those
  swaps preserves directed modularity Q (Leicht–Newman 2008) by
  construction, given the fixed partition.

If ``community_partition`` is None, a partition is detected once on the
input — undirected Louvain for the undirected mode, directed Louvain for the
directed mode — seeded by ``louvain_seed``. For methodological consistency
the caller should pre-compute the partition once per experiment and pass it
explicitly to every call so the null's *definition* is fixed across rewire
seeds.
"""

import warnings

import networkx as nx
import numpy as np


def generate(
    adjacency: np.ndarray,
    seed: int,
    directed: bool = False,
    community_partition: list[set[int]] | None = None,
    louvain_seed: int = 0,
    n_swaps_multiplier: int = 10,
    max_attempts_multiplier: int = 100,
    return_diagnostics: bool = False,
    **kwargs,
) -> np.ndarray | tuple[np.ndarray, dict]:
    """Degree- and block-structure-preserving rewire of a binary mask.

    Parameters
    ----------
    adjacency
        Binary matrix to rewire (zero diagonal). Symmetric for the undirected
        mode; may be directed (asymmetric) for ``directed=True``. Treated as
        binary via ``adjacency != 0``.
    seed
        Seed for the rewire RNG (independent of partition detection).
    directed
        If False (default), undirected mode. If True, directed mode
        (preserves in- and out-degree sequences and the directed block
        edge-count matrix).
    community_partition
        Optional pre-computed partition as a list of node-id sets. If
        None, detected here via Louvain with ``louvain_seed`` (directed
        Louvain when ``directed=True``).
    louvain_seed
        Seed for Louvain detection when ``community_partition`` is None.
    n_swaps_multiplier
        Target accepted swaps as a multiple of edge count.
    max_attempts_multiplier
        Hard cap on attempted swaps as a multiple of the swap target.
    return_diagnostics
        If True, return ``(adjacency, diagnostics_dict)`` including the
        partition's modularity Q on the input and output.
    """
    if directed:
        return _generate_directed(
            adjacency,
            seed,
            community_partition,
            louvain_seed,
            n_swaps_multiplier,
            max_attempts_multiplier,
            return_diagnostics,
        )

    graph = nx.from_numpy_array(adjacency)
    n_edges = graph.number_of_edges()
    n_swaps_target = n_swaps_multiplier * n_edges
    max_attempts = max_attempts_multiplier * n_swaps_target

    if community_partition is None:
        community_partition = nx.community.louvain_communities(
            graph, seed=louvain_seed
        )

    node_to_block: dict[int, int] = {}
    for block_id, members in enumerate(community_partition):
        for node in members:
            node_to_block[int(node)] = block_id

    Q_initial = nx.community.modularity(graph, community_partition)

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
        if node_to_block[v] != node_to_block[y]:
            continue

        graph.remove_edge(u, v)
        graph.remove_edge(x, y)
        graph.add_edge(u, y)
        graph.add_edge(x, v)

        edges[i] = (u, y)
        edges[j] = (x, v)
        n_accepted += 1

    acceptance_rate = n_accepted / max(n_attempted, 1)
    if acceptance_rate < 0.05:
        warnings.warn(
            f"modularity_rewire: acceptance rate {acceptance_rate:.4f} "
            f"below 5% — the partition's structure may be very fragmented or "
            f"dense within blocks. Accepted {n_accepted}/{n_swaps_target} "
            f"target swaps.",
            RuntimeWarning,
            stacklevel=2,
        )

    result = nx.to_numpy_array(graph)
    Q_final = nx.community.modularity(graph, community_partition)

    if return_diagnostics:
        diagnostics = {
            "acceptance_rate": acceptance_rate,
            "n_accepted": n_accepted,
            "n_attempted": n_attempted,
            "n_communities": len(community_partition),
            "Q_initial": float(Q_initial),
            "Q_final": float(Q_final),
        }
        return result, diagnostics

    return result


def _generate_directed(
    adjacency: np.ndarray,
    seed: int,
    community_partition: list[set[int]] | None,
    louvain_seed: int,
    n_swaps_multiplier: int,
    max_attempts_multiplier: int,
    return_diagnostics: bool,
) -> np.ndarray | tuple[np.ndarray, dict]:
    """Directed modularity-preserving rewire.

    Two-edge head-swaps ``a->b, c->d  =>  a->d, c->b`` preserve every node's
    in- and out-degree. The swap leaves the directed block edge-count matrix
    unchanged iff the two tails share a block (``block(a) == block(c)``) or
    the two heads share a block (``block(b) == block(d)``): in either case the
    multiset of (tail-block, head-block) pairs is identical before and after.
    Accepting only those swaps preserves the directed block matrix exactly,
    and hence directed modularity Q given the fixed partition. No rejection
    sampling on a continuous statistic is needed.
    """
    binary = (adjacency != 0).astype(int)
    graph = nx.from_numpy_array(binary, create_using=nx.DiGraph)
    n_edges = graph.number_of_edges()
    n_swaps_target = n_swaps_multiplier * n_edges
    max_attempts = max_attempts_multiplier * n_swaps_target

    partition_method = "provided"
    if community_partition is None:
        community_partition = nx.community.louvain_communities(
            graph, seed=louvain_seed
        )
        partition_method = f"directed_louvain(seed={louvain_seed})"

    node_to_block: dict[int, int] = {}
    for block_id, members in enumerate(community_partition):
        for node in members:
            node_to_block[int(node)] = block_id

    Q_initial = nx.community.modularity(graph, community_partition)

    rng = np.random.default_rng(seed)
    edges = list(graph.edges())

    n_accepted = 0
    n_attempted = 0

    while n_accepted < n_swaps_target and n_attempted < max_attempts:
        n_attempted += 1

        i, j = (int(k) for k in rng.choice(len(edges), size=2, replace=False))
        a, b = edges[i]  # directed edge a -> b
        c, d = edges[j]  # directed edge c -> d

        if len({a, b, c, d}) != 4:
            continue
        if graph.has_edge(a, d) or graph.has_edge(c, b):
            continue
        if (
            node_to_block[a] != node_to_block[c]
            and node_to_block[b] != node_to_block[d]
        ):
            continue

        graph.remove_edge(a, b)
        graph.remove_edge(c, d)
        graph.add_edge(a, d)
        graph.add_edge(c, b)

        edges[i] = (a, d)
        edges[j] = (c, b)
        n_accepted += 1

    acceptance_rate = n_accepted / max(n_attempted, 1)
    if acceptance_rate < 0.05:
        warnings.warn(
            f"modularity_rewire(directed=True): acceptance rate "
            f"{acceptance_rate:.4f} below 5% — the partition's block structure "
            f"may be very fragmented or dense within blocks. Accepted "
            f"{n_accepted}/{n_swaps_target} target swaps.",
            RuntimeWarning,
            stacklevel=2,
        )

    result = nx.to_numpy_array(graph, dtype=float)
    Q_final = nx.community.modularity(graph, community_partition)

    if return_diagnostics:
        diagnostics = {
            "directed": True,
            "partition_method": partition_method,
            "acceptance_rate": acceptance_rate,
            "n_accepted": n_accepted,
            "n_attempted": n_attempted,
            "n_communities": len(community_partition),
            "Q_initial": float(Q_initial),
            "Q_final": float(Q_final),
        }
        return result, diagnostics

    return result

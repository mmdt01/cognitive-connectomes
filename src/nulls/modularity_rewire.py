"""Modularity-preserving rewire (rung 4).

Preserves N, edge count, AND each node's exact degree, AND the
intra-/inter-community edge counts of a fixed partition (the "block
structure"). Implemented via block-constrained double-edge swaps.

A swap (u,v),(x,y) -> (u,y),(x,v) preserves the per-block-pair edge
count iff ``block(v) == block(y)`` (the prompt's specified sufficient
condition). With random endpoint orientation per draw, all four
single-equality matchings ({b(v)==b(y), b(u)==b(x), b(v)==b(x),
b(u)==b(y)}) are sampled across draws — each one is a valid swap
orientation under its corresponding implicit relabelling.

If ``community_partition`` is None, a partition is detected once on the
input via ``nx.community.louvain_communities(G, seed=louvain_seed)``.
For methodological consistency the caller should pre-compute the
partition once per experiment and pass it explicitly to every call so
the null's *definition* is fixed across rewire seeds.
"""

import warnings

import networkx as nx
import numpy as np


def generate(
    adjacency: np.ndarray,
    seed: int,
    community_partition: list[set[int]] | None = None,
    louvain_seed: int = 0,
    n_swaps_multiplier: int = 10,
    max_attempts_multiplier: int = 100,
    return_diagnostics: bool = False,
    **kwargs,
) -> np.ndarray | tuple[np.ndarray, dict]:
    """Degree- and block-structure-preserving rewire of a binary symmetric mask.

    Parameters
    ----------
    adjacency
        Binary symmetric matrix to rewire (zero diagonal).
    seed
        Seed for the rewire RNG (independent of partition detection).
    community_partition
        Optional pre-computed partition as a list of node-id sets. If
        None, detected here via Louvain with ``louvain_seed``.
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

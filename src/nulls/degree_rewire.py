"""Degree-preserving rewire (configuration-model class).

Default (``directed=False``, v2a-compatible): preserves N, undirected
edge count, AND each node's exact undirected degree. Implemented via
repeated double-edge swaps: pick two edges (u,v) and (x,y); if no
collision, replace them with (u,y) and (x,v). Each swap rearranges
*which* nodes connect while preserving every degree.

Directed (``directed=True``, v2b): preserves N, directed edge count,
AND each node's exact in-degree AND out-degree separately. Implemented
via ``nx.directed_edge_swap``.

The swap multiplier (default 10) follows v1; sufficient to decorrelate
at N=300 for this density.
"""

import networkx as nx
import numpy as np


def generate(
    adjacency: np.ndarray,
    seed: int,
    directed: bool = False,
    n_swaps_multiplier: int = 10,
    **kwargs,
) -> np.ndarray:
    """Degree-preserving rewire of a binary adjacency.

    Parameters
    ----------
    adjacency
        Reference matrix to rewire. Treated as binary via
        ``adjacency != 0``.
    seed
        Seed forwarded to the swap routine.
    directed
        If False (default), undirected — preserves the (sorted) degree
        sequence. If True, directed — preserves both in- and out-degree
        sequences separately.
    n_swaps_multiplier
        Number of swaps as a multiple of edge count (v1 default: 10).
    """
    binary_mask = (adjacency != 0).astype(int)

    if not directed:
        graph = nx.from_numpy_array(binary_mask.astype(float))
        n_edges_local = graph.number_of_edges()
        n_swaps = n_swaps_multiplier * n_edges_local
        nx.double_edge_swap(
            graph,
            nswap=n_swaps,
            max_tries=n_swaps * 10,
            seed=seed,
        )
        return nx.to_numpy_array(graph)

    graph = nx.from_numpy_array(binary_mask.astype(float), create_using=nx.DiGraph)
    n_edges_local = graph.number_of_edges()
    n_swaps = n_swaps_multiplier * n_edges_local
    nx.directed_edge_swap(
        graph,
        nswap=n_swaps,
        max_tries=n_swaps * 10,
        seed=seed,
    )
    return nx.to_numpy_array(graph, dtype=float)

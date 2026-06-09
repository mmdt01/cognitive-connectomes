"""Erdős–Rényi G(N, M) random graph: matched exact edge count.

Default (``directed=False``, v2a-compatible): undirected.
Preserves N and exact undirected edge count. Built by picking M of the
C(N, 2) possible undirected edges uniformly at random.

Directed (``directed=True``, v2b): preserves N and exact directed
edge count. Built via ``nx.gnm_random_graph(..., directed=True)`` which
picks M of the N * (N - 1) possible directed edges uniformly at random.
"""

import networkx as nx
import numpy as np


def generate(
    adjacency: np.ndarray,
    seed: int,
    directed: bool = False,
    **kwargs,
) -> np.ndarray:
    """Generate an Erdős–Rényi G(N, M) graph with M matched to the input.

    Parameters
    ----------
    adjacency
        Reference matrix; only N and edge count are read. Treated as
        binary via ``adjacency != 0``.
    seed
        Seed forwarded to ``networkx.gnm_random_graph``.
    directed
        If False (default), undirected (matches v2a). If True, directed.
    """
    n = adjacency.shape[0]
    if not directed:
        n_edges = int((adjacency != 0).sum() // 2)
        graph = nx.gnm_random_graph(n, n_edges, seed=seed)
        return nx.to_numpy_array(graph)

    n_directed_edges = int((adjacency != 0).sum())
    graph = nx.gnm_random_graph(n, n_directed_edges, directed=True, seed=seed)
    return nx.to_numpy_array(graph, dtype=float)

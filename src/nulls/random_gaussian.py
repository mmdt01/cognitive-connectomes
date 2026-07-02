"""Density-matched random binary mask, no self-loops.

Default (``directed=False``): symmetric.
Each off-diagonal upper-triangle pair is an independent Bernoulli draw
at the input's undirected density; the result is mirrored to the lower
triangle. Edge count is Binomial-distributed across seeds.

Directed (``directed=True``): asymmetric. Each off-diagonal
directed entry ``(i, j)`` and ``(j, i)`` is an independent Bernoulli
draw at the input's directed density (no mirroring).

This corrects v1's incidental asymmetry: v1's ``random_gaussian``
sampled all N*N entries independently, producing an asymmetric matrix.
the undirected conditions use symmetric masks (see plan Section 2).
"""

import numpy as np


def generate(
    adjacency: np.ndarray,
    seed: int,
    directed: bool = False,
    **kwargs,
) -> np.ndarray:
    """Generate a density-matched binary mask.

    Parameters
    ----------
    adjacency
        Reference matrix; only its density is read. Treated as binary
        via ``adjacency != 0``.
    seed
        Seed for ``np.random.default_rng``.
    directed
        If False (default), output is symmetric: density matched to the
        undirected edge count. If True, output is asymmetric: each
        directed entry sampled independently at the directed density.
    """
    n = adjacency.shape[0]
    rng = np.random.default_rng(seed)

    if not directed:
        n_edges_upper = int(np.triu(adjacency, k=1).sum())
        possible_upper = n * (n - 1) // 2
        density = n_edges_upper / possible_upper

        upper = rng.random((n, n)) < density
        upper = np.triu(upper, k=1)
        mask = (upper | upper.T).astype(float)
        return mask

    # Directed: sample every off-diagonal entry independently.
    n_directed_edges = int((adjacency != 0).sum())
    possible_directed = n * (n - 1)
    density = n_directed_edges / possible_directed

    draws = rng.random((n, n)) < density
    np.fill_diagonal(draws, False)
    return draws.astype(float)

"""Apply a weight scheme to a binary topology mask."""

import numpy as np


def apply_weight_scheme(
    adjacency_mask: np.ndarray,
    scheme: str,
    seed: int,
    **kwargs,
) -> np.ndarray:
    """Apply a weight scheme to a binary topology mask.

    Parameters
    ----------
    adjacency_mask
        Binary ({0, 1}-valued), zero-diagonal mask of shape (N, N).
        Must be symmetric for ``symmetric_gaussian``; may be asymmetric
        (directed) for ``asymmetric_empirical``.
    scheme
        ``"symmetric_gaussian"`` (v2a): one N(0, 1) draw per undirected
        upper-triangle edge present in the mask; the same value is
        written to both ``W[i, j]`` and ``W[j, i]``. Diagonal stays
        zero.

        ``"asymmetric_empirical"`` (v2b): one independent draw per
        nonzero entry of the mask, sampled with replacement from the
        empirical weight pool passed via the ``empirical_weights``
        kwarg. ``W[i, j]`` and ``W[j, i]`` are independent even when
        the mask is symmetric. Diagonal stays zero.
    seed
        Seed for ``np.random.default_rng``.
    empirical_weights
        Required for ``asymmetric_empirical``. 1D array of positive
        weight values to sample from (with replacement).

    Returns
    -------
    np.ndarray
        Weighted W with zero diagonal.
    """
    assert adjacency_mask.ndim == 2 and adjacency_mask.shape[0] == adjacency_mask.shape[1], \
        f"mask must be square 2D; got {adjacency_mask.shape}"
    assert np.all((adjacency_mask == 0) | (adjacency_mask == 1)), \
        "mask must be {0,1}-valued"
    assert np.all(np.diag(adjacency_mask) == 0), "mask must have zero diagonal"

    if scheme == "symmetric_gaussian":
        assert np.allclose(adjacency_mask, adjacency_mask.T), \
            "symmetric_gaussian requires a symmetric mask"
        rng = np.random.default_rng(seed)
        upper_mask = np.triu(adjacency_mask, k=1).astype(bool)
        weighted = np.zeros_like(adjacency_mask, dtype=float)
        draws = rng.normal(0.0, 1.0, size=upper_mask.sum())
        weighted[upper_mask] = draws
        weighted = weighted + weighted.T
        return weighted

    if scheme == "asymmetric_empirical":
        empirical_weights = kwargs.get("empirical_weights")
        if empirical_weights is None:
            raise ValueError(
                "asymmetric_empirical requires the `empirical_weights` kwarg "
                "(1D array of values to sample from with replacement)."
            )
        empirical_weights = np.asarray(empirical_weights, dtype=float).ravel()
        assert empirical_weights.size > 0, "empirical_weights must be non-empty"
        rng = np.random.default_rng(seed)
        nonzero_mask = adjacency_mask.astype(bool)
        weighted = np.zeros_like(adjacency_mask, dtype=float)
        draws = rng.choice(
            empirical_weights, size=int(nonzero_mask.sum()), replace=True
        )
        weighted[nonzero_mask] = draws
        return weighted

    raise NotImplementedError(f"Unknown weight scheme: {scheme!r}")

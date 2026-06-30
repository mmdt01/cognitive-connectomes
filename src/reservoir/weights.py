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

        ``"symmetric_empirical"`` (v2ae): the undirected, *normal*
        analogue of ``asymmetric_empirical``. One draw per undirected
        upper-triangle edge, sampled with replacement from
        ``empirical_weights``, written to both ``W[i, j]`` and
        ``W[j, i]`` so W is exactly symmetric (hence normal). Requires a
        symmetric mask. Same symmetric topology treatment as
        ``symmetric_gaussian`` (v2a) but with real heavy-tailed
        empirical magnitudes instead of Gaussian draws -- it isolates
        weight heterogeneity from non-normality. Diagonal stays zero.

        ``"asymmetric_gaussian"`` (v2bg): the directed, *non-normal*
        analogue of ``symmetric_gaussian``. One independent N(0, 1)
        draw per nonzero (directed) entry of the mask, so ``W[i, j]``
        and ``W[j, i]`` are independent (asymmetric, non-normal) but the
        magnitude distribution is homogeneous (Gaussian, no heavy tail).
        Same directed topology as ``asymmetric_empirical`` (v2b) but
        homogeneous weights -- the fourth cell of the
        topology x weight-distribution 2x2. Diagonal stays zero.

        ``"asymmetric_empirical_signed"`` (v2d): the v2b magnitude
        pipeline followed by a per-neuron Dale sign. Magnitudes are
        sampled from ``abs(empirical_weights)``; the per-neuron sign
        vector ``neuron_signs`` (one entry per node, +1 excitatory / -1
        inhibitory) is applied column-wise, so every outgoing synapse of
        a presynaptic neuron shares that neuron's sign. In reservoir
        convention ``W[i, j]`` is the weight from ``j`` to ``i``, so
        neuron ``j``'s out-synapses are column ``j``: ``W[:, j] *=
        neuron_signs[j]``. Diagonal stays zero.
    seed
        Seed for ``np.random.default_rng``.
    empirical_weights
        Required for ``asymmetric_empirical`` and
        ``asymmetric_empirical_signed``. 1D array of weight magnitudes to
        sample from (with replacement); for the signed scheme the
        absolute value is used.
    neuron_signs
        Required for ``asymmetric_empirical_signed``. 1D array of length
        N with entries in {+1, -1}, the Dale sign of each presynaptic
        neuron (applied to its out-column).

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

    if scheme == "asymmetric_empirical_signed":
        empirical_weights = kwargs.get("empirical_weights")
        neuron_signs = kwargs.get("neuron_signs")
        if empirical_weights is None:
            raise ValueError(
                "asymmetric_empirical_signed requires the `empirical_weights` "
                "kwarg (1D array of magnitudes to sample from with replacement)."
            )
        if neuron_signs is None:
            raise ValueError(
                "asymmetric_empirical_signed requires the `neuron_signs` kwarg "
                "(1D array of per-neuron signs, one per node)."
            )
        # Magnitudes are sampled exactly as in asymmetric_empirical; the sign is
        # supplied solely by neuron_signs, so abs() guards against a signed pool.
        magnitudes = np.abs(np.asarray(empirical_weights, dtype=float).ravel())
        assert magnitudes.size > 0, "empirical_weights must be non-empty"
        neuron_signs = np.asarray(neuron_signs, dtype=float).ravel()
        n_nodes = adjacency_mask.shape[0]
        assert neuron_signs.shape == (n_nodes,), (
            f"neuron_signs must have one entry per node; got "
            f"{neuron_signs.shape} for an {n_nodes}-node mask"
        )
        assert np.all(np.isin(neuron_signs, (-1.0, 1.0))), (
            "neuron_signs must be +1 (excitatory) or -1 (inhibitory)"
        )
        rng = np.random.default_rng(seed)
        nonzero_mask = adjacency_mask.astype(bool)
        weighted = np.zeros_like(adjacency_mask, dtype=float)
        draws = rng.choice(magnitudes, size=int(nonzero_mask.sum()), replace=True)
        weighted[nonzero_mask] = draws
        # Dale's principle: a presynaptic neuron signs all its outgoing synapses.
        # In reservoir convention W[i, j] is the weight from j to i, so neuron j's
        # out-synapses are column j; scale each column by its presynaptic sign.
        weighted = weighted * neuron_signs[np.newaxis, :]
        return weighted

    if scheme == "symmetric_empirical":
        empirical_weights = kwargs.get("empirical_weights")
        if empirical_weights is None:
            raise ValueError(
                "symmetric_empirical requires the `empirical_weights` kwarg "
                "(1D array of magnitudes to sample from with replacement)."
            )
        assert np.allclose(adjacency_mask, adjacency_mask.T), \
            "symmetric_empirical requires a symmetric mask"
        empirical_weights = np.asarray(empirical_weights, dtype=float).ravel()
        assert empirical_weights.size > 0, "empirical_weights must be non-empty"
        rng = np.random.default_rng(seed)
        upper_mask = np.triu(adjacency_mask, k=1).astype(bool)
        weighted = np.zeros_like(adjacency_mask, dtype=float)
        # one draw per undirected edge, mirrored -> exactly symmetric (normal)
        weighted[upper_mask] = rng.choice(
            empirical_weights, size=int(upper_mask.sum()), replace=True
        )
        weighted = weighted + weighted.T
        return weighted

    if scheme == "asymmetric_gaussian":
        rng = np.random.default_rng(seed)
        nonzero_mask = adjacency_mask.astype(bool)
        weighted = np.zeros_like(adjacency_mask, dtype=float)
        # one independent N(0, 1) draw per directed edge -> asymmetric (non-normal)
        weighted[nonzero_mask] = rng.normal(0.0, 1.0, size=int(nonzero_mask.sum()))
        return weighted

    raise NotImplementedError(f"Unknown weight scheme: {scheme!r}")

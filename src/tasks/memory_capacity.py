"""Jaeger 2001/2002 memory capacity.

Feed uniform white noise into the reservoir; for each lag k in 1..max_lag,
train a separate ridge readout to reconstruct u(t - k) from the reservoir
state x(t). Sum the squared Pearson correlations across lags.
"""

import numpy as np
from scipy.stats import pearsonr

from src.reservoir.build import build_from_adjacency
from src.reservoir.weights import apply_weight_scheme


def _measure(
    reservoir,
    seed: int,
    T: int,
    warmup: int,
    max_lag: int,
    ridge_alpha: float,
    input_scaling: float,
    collect_states: bool = False,
) -> tuple[float, np.ndarray, np.ndarray | None]:
    """Run the MC measurement loop. Returns ``(mc_total, mc_per_lag, states)``.

    ``states`` is the post-warmup driven state matrix ``(T - warmup, N)`` when
    ``collect_states`` (the additive, opt-in manifold-probe capture path), else
    ``None``. The metric computation is untouched, so the default path is
    byte-identical.

    Per lag ``k`` the design matrix is ``X_k = states[k:]`` and the ridge readout
    needs the Gram ``X_k.T @ X_k`` (the dominant cost: ``O((n-k) N^2)`` per lag).
    The ``X_k`` are **nested** -- each drops the first row of the previous -- so
    the Gram is computed once for ``k=1`` and **down-dated** by a rank-1 update
    thereafter, ``gram_{k+1} = gram_k - outer(states[k], states[k])``, turning the
    total Gram cost from ``O(max_lag * (n-k) N^2)`` into ``O(n N^2)`` (the rest --
    one ``N x N`` solve per lag -- then dominates). Numerically identical to
    rebuilding each Gram up to float round-off: with ``max_lag << n`` the down-date
    removes only ~2% of the Gram's mass, so there is no meaningful cancellation.
    """
    rng = np.random.default_rng(seed)
    u = rng.uniform(-input_scaling, input_scaling, size=(T, 1))

    if getattr(reservoir, "state", None) is not None:
        reservoir.reset()
    states = reservoir.run(u)  # (T, N)

    states_after_warmup = states[warmup:]
    u_flat = u[warmup:, 0]
    n_after_warmup = states_after_warmup.shape[0]
    n_units = states_after_warmup.shape[1]

    ridge_eye = ridge_alpha * np.eye(n_units)
    # gram holds X_k.T @ X_k (no ridge); initialise at k=1 and down-date per lag.
    gram = states_after_warmup[1:].T @ states_after_warmup[1:]

    mc_per_lag = np.zeros(max_lag)
    for k in range(1, max_lag + 1):
        X = states_after_warmup[k:]
        y = u_flat[: n_after_warmup - k]
        w = np.linalg.solve(gram + ridge_eye, X.T @ y)
        pred = X @ w
        if np.std(pred) < 1e-12 or np.std(y) < 1e-12:
            mc_per_lag[k - 1] = 0.0
        else:
            r, _ = pearsonr(pred, y)
            mc_per_lag[k - 1] = r ** 2
        # Down-date for the next lag: drop row k (the first row of the current X).
        if k < max_lag:
            row = states_after_warmup[k]
            gram = gram - np.outer(row, row)
    captured = states_after_warmup if collect_states else None
    return float(mc_per_lag.sum()), mc_per_lag, captured


def evaluate(
    reservoir,
    seed: int,
    T: int,
    warmup: int,
    max_lag: int,
    ridge_alpha: float,
    input_scaling: float,
    validate: bool = False,
    collect_states: bool = False,
    **kwargs,
) -> dict:
    """Memory-capacity evaluator.

    Parameters
    ----------
    reservoir
        A configured ReservoirPy ``Reservoir`` node.
    seed
        Seed for the white-noise input stream. v1 used ``construction_seed + 1000``
        so the input is decorrelated from construction.
    T, warmup, max_lag, ridge_alpha
        MC hyperparameters; v1 pinned values are T=3000, warmup=500,
        max_lag=50, ridge_alpha=1e-6.
    input_scaling
        Maximum amplitude of the uniform input; v1 used 1.0.
    validate
        If True, build a canonical density-matched symmetric-Gaussian
        reservoir at sr=0.95 first and assert its MC lands in
        ``(5, 50)``. Tighter [10, 30] is the published expectation;
        the undirected symmetric-weight regime can land slightly outside [10, 30]
        so the gate uses the v1-compatible [5, 50] window.
    collect_states
        If True, also return the post-warmup driven state matrix under the
        ``"states"`` key (the additive, opt-in manifold-probe capture path). Off
        by default, so the committed task runs are byte-identical.

    Returns
    -------
    dict
        ``{"mc": float, "mc_per_lag": np.ndarray of shape (max_lag,)}``, plus
        ``"states"`` (``(T - warmup, N)``) when ``collect_states``.
    """
    if validate:
        _run_sanity_gate(seed, T, warmup, max_lag, ridge_alpha, input_scaling)

    mc, mc_per_lag, states = _measure(
        reservoir, seed, T, warmup, max_lag, ridge_alpha, input_scaling,
        collect_states=collect_states,
    )
    result = {"mc": mc, "mc_per_lag": mc_per_lag}
    if collect_states:
        result["states"] = states
    return result


def _run_sanity_gate(
    seed: int,
    T: int,
    warmup: int,
    max_lag: int,
    ridge_alpha: float,
    input_scaling: float,
) -> None:
    """Build a canonical sanity reservoir; assert MC in (5, 50)."""
    from src.nulls import random_gaussian

    n_nodes = 300
    density = 0.067
    rng = np.random.default_rng(seed)
    upper = rng.random((n_nodes, n_nodes)) < density
    upper = np.triu(upper, k=1)
    sanity_mask = (upper | upper.T).astype(float)

    weighted = apply_weight_scheme(sanity_mask, "symmetric_gaussian", seed=seed)
    sanity_reservoir = build_from_adjacency(
        weighted_adjacency=weighted,
        target_spectral_radius=0.95,
        leak_rate=1.0,
        input_scaling=input_scaling,
        seed=seed,
    )
    mc_sanity, _, _ = _measure(
        sanity_reservoir,
        seed=seed + 1000,
        T=T,
        warmup=warmup,
        max_lag=max_lag,
        ridge_alpha=ridge_alpha,
        input_scaling=input_scaling,
    )
    print(f"[MC sanity] symmetric-Gaussian random reservoir at sr=0.95: MC = {mc_sanity:.2f}")
    assert 5.0 < mc_sanity < 50.0, (
        f"MC sanity check failed: got {mc_sanity:.2f}, expected ~10-30 (gate: 5-50). "
        "Indexing in memory_capacity is likely wrong."
    )

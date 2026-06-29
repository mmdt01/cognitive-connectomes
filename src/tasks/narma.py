"""NARMA-10 system-emulation task.

Drive the reservoir with i.i.d. ``Uniform[u_low, u_high]`` (default
``[0, 0.5]``) input; train a single ridge readout to reproduce the tenth-order
NARMA target from the reservoir state, and score it out-of-sample. Report NRMSE
(lower is better).

This is the bridge from memory capacity (passive linear recall) to a task that
demands nonlinear temporal computation, while keeping the input-driven,
readout-only paradigm. It is *system emulation* (input-driven identification),
not autonomous free-running forecasting — the tightest one-variable step from
memory capacity.

NARMA-10 recurrence (order ``n = 10``):

    u(t) ~ Uniform[0, 0.5]                                   i.i.d.
    y(t+1) = a1*y(t)
           + a2*y(t)*sum(y[t-n : t])                         n terms, y[t-n]..y[t-1]
           + b*u(t-n)*u(t)
           + c
    with a1=0.3, a2=0.05, b=1.5, c=0.1.

Convention note: this matches ``reservoirpy.datasets.narma`` exactly (verified
bit-for-bit in the test suite) — the sum window is ``y[t-n:t]`` and the input
product is ``u[t-n]*u[t]``. This differs by a one-step index shift from the
canonical Atiya-Parlos form (``sum_{i=0}^{n-1} y(t-i)`` and
``u(t-n+1)*u(t)``). Both are standard NARMA-10
variants; the shift is immaterial to the task. Matching reservoirpy buys a
clean reference cross-check.
"""

import numpy as np

ORDER = 10
A1, A2, B, C = 0.3, 0.05, 1.5, 0.1


def narma10(
    u: np.ndarray,
    a1: float = A1,
    a2: float = A2,
    b: float = B,
    c: float = C,
    order: int = ORDER,
) -> np.ndarray:
    """Local NARMA-10 generator (reservoirpy-compatible indexing).

    Parameters
    ----------
    u
        1D input series of length ``L`` (the reservoir is driven by all of it).
    a1, a2, b, c, order
        NARMA coefficients; defaults are the NARMA-10 values.

    Returns
    -------
    np.ndarray
        Target series ``y`` of length ``L``. The first ``order`` entries are
        the zero initial conditions; downstream code discards them via the
        washout.
    """
    u = np.asarray(u, dtype=float).ravel()
    length = u.shape[0]
    y = np.zeros(length)
    for t in range(order, length - 1):
        y[t + 1] = (
            a1 * y[t]
            + a2 * y[t] * np.sum(y[t - order : t])
            + b * u[t - order] * u[t]
            + c
        )
    return y


def _generate_input_and_target(
    rng: np.random.Generator,
    n_timesteps: int,
    u_low: float,
    u_high: float,
    divergence_bound: float,
    max_tries: int,
) -> tuple[np.ndarray, np.ndarray, int]:
    """Draw a NARMA-10 input/target pair, regenerating divergent draws.

    The NARMA recurrence can blow up for some input draws; a divergent target
    silently poisons NRMSE. Reject any draw whose target is non-finite or
    exceeds ``divergence_bound`` and redraw. Returns ``(u, y, n_rejected)``
    where ``n_rejected`` is the number of rejected draws before success.
    """
    for n_rejected in range(max_tries):
        u = rng.uniform(u_low, u_high, size=n_timesteps)
        # Divergent draws are the expected rejection mechanism; their overflow
        # to inf/nan is screened below, so silence the overflow warning here.
        with np.errstate(over="ignore", invalid="ignore"):
            y = narma10(u)
        if np.all(np.isfinite(y)) and np.max(np.abs(y)) <= divergence_bound:
            return u, y, n_rejected
    raise RuntimeError(
        f"NARMA-10 target diverged on all {max_tries} input draws "
        f"(bound={divergence_bound}); inspect u_low/u_high or the bound."
    )


def _fit_ridge_readout(
    states: np.ndarray, targets: np.ndarray, ridge_alpha: float, readout_bias: bool
) -> tuple[np.ndarray, bool]:
    """Closed-form ridge readout. Mirrors ``memory_capacity`` (np.linalg.solve).

    Optionally augments the state with a constant bias feature (the NARMA
    target has a non-zero offset). The bias column is left unregularised.
    """
    design = states
    if readout_bias:
        design = np.hstack([states, np.ones((states.shape[0], 1))])
    n_features = design.shape[1]
    reg = ridge_alpha * np.eye(n_features)
    if readout_bias:
        reg[-1, -1] = 0.0  # do not shrink the intercept
    weights = np.linalg.solve(design.T @ design + reg, design.T @ targets)
    return weights, readout_bias


def _predict(states: np.ndarray, weights: np.ndarray, readout_bias: bool) -> np.ndarray:
    design = states
    if readout_bias:
        design = np.hstack([states, np.ones((states.shape[0], 1))])
    return design @ weights


def evaluate(
    reservoir,
    seed: int,
    T: int = 3000,
    washout: int = 200,
    n_train: int = 2000,
    n_test: int = 800,
    ridge_alpha: float = 1e-8,
    readout_bias: bool = True,
    u_low: float = 0.0,
    u_high: float = 0.5,
    divergence_bound: float = 10.0,
    max_input_tries: int = 50,
    validate: bool = False,
    **kwargs,
) -> dict:
    """NARMA-10 evaluator. Mirrors ``memory_capacity.evaluate``'s interface.

    Drives ``reservoir`` with a NARMA-10 input, trains a ridge readout on a
    train split of the post-washout states, and reports out-of-sample NRMSE on
    the held-out test split.

    Parameters
    ----------
    reservoir
        A configured ReservoirPy ``Reservoir`` node (its ``Win``/leak/spectral
        radius are fixed at build time — those are the frozen hyperparameters).
    seed
        Seed for the NARMA input stream. The runner passes the same seed to the
        connectome and its nulls to pair them on an identical input.
    T, washout, n_train, n_test
        Total input length and the post-washout train/test split sizes. Require
        ``washout + n_train + n_test <= T``.
    ridge_alpha
        Ridge regularisation for the readout.
    readout_bias
        Append a constant feature to the readout (NARMA's target is offset).
    u_low, u_high
        Input range; NARMA-10 standard is [0, 0.5].
    divergence_bound, max_input_tries
        Reject and redraw any input whose NARMA target diverges (see
        ``_generate_input_and_target``).
    validate
        If True, run a sanity gate first: a canonical density-matched
        symmetric-Gaussian reservoir at sr=0.95 must reach NRMSE below a loose
        bound (catches gross indexing/readout errors).

    Returns
    -------
    dict
        ``{"nrmse", ...}`` plus the resolved task config for the audit trail.
    """
    if not (washout + n_train + n_test <= T):
        raise ValueError(
            f"washout + n_train + n_test ({washout + n_train + n_test}) "
            f"must be <= T ({T})."
        )

    if validate:
        _run_sanity_gate(
            seed, T, washout, n_train, n_test, ridge_alpha, readout_bias,
            u_low, u_high, divergence_bound, max_input_tries,
        )

    nrmse, n_rejected = _measure(
        reservoir, seed, T, washout, n_train, n_test, ridge_alpha, readout_bias,
        u_low, u_high, divergence_bound, max_input_tries,
    )
    return {
        "nrmse": nrmse,
        "n_input": T,
        "n_washout": washout,
        "n_train": n_train,
        "n_test": n_test,
        "n_rejected_inputs": n_rejected,
        "ridge_alpha": ridge_alpha,
        "readout_bias": readout_bias,
        "u_low": u_low,
        "u_high": u_high,
    }


def _measure(
    reservoir,
    seed: int,
    T: int,
    washout: int,
    n_train: int,
    n_test: int,
    ridge_alpha: float,
    readout_bias: bool,
    u_low: float,
    u_high: float,
    divergence_bound: float,
    max_input_tries: int,
) -> tuple[float, int]:
    """Run the NARMA-10 measurement loop. Returns ``(nrmse, n_rejected)``."""
    rng = np.random.default_rng(seed)
    u, y, n_rejected = _generate_input_and_target(
        rng, T, u_low, u_high, divergence_bound, max_input_tries
    )

    if getattr(reservoir, "state", None) is not None:
        reservoir.reset()
    states = reservoir.run(u.reshape(-1, 1))  # (T, N)

    # Discard the washout transient, then split into train / test.
    states = states[washout:]
    targets = y[washout:]
    train_states, train_targets = states[:n_train], targets[:n_train]
    test_states = states[n_train : n_train + n_test]
    test_targets = targets[n_train : n_train + n_test]

    weights, _ = _fit_ridge_readout(
        train_states, train_targets, ridge_alpha, readout_bias
    )
    predictions = _predict(test_states, weights, readout_bias)

    mse = float(np.mean((predictions - test_targets) ** 2))
    target_var = float(np.var(test_targets))
    nrmse = float(np.sqrt(mse / target_var)) if target_var > 0 else float("inf")
    return nrmse, n_rejected


def _run_sanity_gate(
    seed: int,
    T: int,
    washout: int,
    n_train: int,
    n_test: int,
    ridge_alpha: float,
    readout_bias: bool,
    u_low: float,
    u_high: float,
    divergence_bound: float,
    max_input_tries: int,
) -> None:
    """Build a canonical random reservoir; assert NRMSE below a loose bound."""
    from src.nulls import random_gaussian
    from src.reservoir.weights import apply_weight_scheme
    from src.reservoir.build import build_from_adjacency

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
        input_scaling=1.0,
        seed=seed,
    )
    nrmse, _ = _measure(
        sanity_reservoir, seed + 1000, T, washout, n_train, n_test, ridge_alpha,
        readout_bias, u_low, u_high, divergence_bound, max_input_tries,
    )
    print(f"[NARMA sanity] symmetric-Gaussian random reservoir at sr=0.95: NRMSE = {nrmse:.3f}")
    assert nrmse < 0.8, (
        f"NARMA sanity check failed: NRMSE {nrmse:.3f} >= 0.8 (a working "
        "NARMA-10 ESN scores well below this; ~1.0 means the readout only "
        "predicts the mean — likely an indexing or split error)."
    )

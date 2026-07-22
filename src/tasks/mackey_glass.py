"""Mackey-Glass k-step-ahead forecasting task (driven / teacher-forced).

Drive the reservoir with the Mackey-Glass series ``x(t)``; train a single ridge
readout to predict ``x(t+h)`` ``h`` steps ahead, and score it out-of-sample.
Report NRMSE (lower is better).

This is *autonomous-system forecasting* of a mildly chaotic delay system -- the
complement to NARMA's input-driven emulation. It is **driven (teacher-forced)**:
the reservoir always sees the true ``x(t)``, never its own prediction.
Closed-loop free-running (output fed back as input) is deliberately deferred to
the Lorenz task; the only intended change from the NARMA bridge is the task.

Mackey-Glass delay differential equation (canonical mild-chaos parameters):

    dx/dt = a * x(t-tau) / (1 + x(t-tau)^n) - b * x(t)
    a = 0.2 (beta), b = 0.1 (gamma), n = 10, tau = 17.

Convention note: the local generator reproduces ``reservoirpy.datasets.
mackey_glass`` bit-for-bit (verified in the test suite) when handed the same
initial ``history`` buffer -- it uses reservoirpy's RK4 discretisation
(``_mg_rk4`` below). Keeping a local generator buys control over length,
transient discard, and normalisation, and an explicit (reproducible) history
per seed.
"""

import numpy as np

# Canonical mild-chaos parameters (reservoirpy naming: a=beta, b=gamma).
TAU, A, B, N, X0 = 17, 0.2, 0.1, 10, 1.2


def _mg_rk4(xt: float, xtau: float, a: float, b: float, n: int, h: float = 1.0) -> float:
    """One RK4 Mackey-Glass step.

    Reproduces ``reservoirpy.datasets._chaos._mg_rk4`` exactly (same operation
    order), so a series built from this matches reservoirpy bit-for-bit.
    """
    bh = -b * h
    k1 = bh * xt + a * xtau / (1 + xtau**n)
    k2 = 2 * k1 + bh * k1
    k3 = 2 * k1 + bh * k2
    k4 = k1 + bh * k3
    return xt + (k1 + k2 + k3 + k4) / 6


def mackey_glass(
    n_timesteps: int,
    history: np.ndarray,
    tau: int = TAU,
    a: float = A,
    b: float = B,
    n: int = N,
    x0: float = X0,
    h: float = 1.0,
) -> np.ndarray:
    """Local Mackey-Glass generator (reservoirpy-compatible indexing).

    Parameters
    ----------
    n_timesteps
        Number of timesteps to generate.
    history
        1D array of past values seeding the delay term; its last
        ``floor(tau / h)`` elements warm up the delayed feedback. reservoirpy
        draws this randomly from ``x0``; we pass it explicitly so the series is
        reproducible per seed and the reference cross-check is bit-exact.
    tau, a, b, n, x0, h
        Mackey-Glass parameters; defaults are the canonical mild-chaos values.

    Returns
    -------
    np.ndarray
        1D series of length ``n_timesteps``. The first value is ``x0`` (matching
        reservoirpy: the history only feeds the delayed term, not the output's
        first sample).
    """
    history_length = int(np.floor(tau / h))
    history = np.asarray(history, dtype=float).ravel()
    if history.shape[0] < history_length:
        raise ValueError(
            f"history length {history.shape[0]} < floor(tau/h) = {history_length}"
        )
    history_ = history[-history_length:]

    xt = x0
    X = np.empty(history_length + n_timesteps)
    X[:history_length] = history_
    for i in range(history_length, n_timesteps + history_length):
        X[i] = xt
        xtau = X[i - history_length] if tau > 0 else 0.0
        xt = _mg_rk4(xt, xtau, a=a, b=b, n=n, h=h)
    return X[history_length:]


def _random_history(
    rng: np.random.Generator, history_length: int, x0: float
) -> np.ndarray:
    """Random initial-history buffer, matching reservoirpy's construction.

    ``x0 * ones(L) + 0.2 * (U[0,1) - 0.5)`` -- a small perturbation around the
    initial condition. Drawn per seed so each seed visits a different stretch of
    the Mackey-Glass attractor (the analogue of NARMA's per-seed random input).
    """
    return x0 * np.ones(history_length) + 0.2 * (rng.random(history_length) - 0.5)


def _fit_ridge_readout(
    states: np.ndarray, targets: np.ndarray, ridge_alpha: float, readout_bias: bool
) -> tuple[np.ndarray, bool]:
    """Closed-form ridge readout (mirrors ``narma``/``memory_capacity``).

    Optionally augments the state with a constant bias feature; the bias column
    is left unregularised.
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
    horizon: int = 17,
    n_transient: int = 200,
    ridge_alpha: float = 1e-8,
    readout_bias: bool = True,
    tau: int = TAU,
    a: float = A,
    b: float = B,
    n: int = N,
    x0: float = X0,
    h: float = 1.0,
    validate: bool = False,
    collect_states: bool = False,
    sanity_horizon: int = 17,
    sanity_max_nrmse: float = 0.8,
    **kwargs,
) -> dict:
    """Mackey-Glass evaluator. Mirrors ``narma.evaluate``'s interface.

    Generates a Mackey-Glass series (random initial history seeded by ``seed``),
    discards an initial transient, drives ``reservoir`` with ``x(t)`` and trains
    a ridge readout to predict ``x(t+horizon)`` on a train split of the
    post-washout states, then reports out-of-sample NRMSE on the held-out test
    split.

    Parameters
    ----------
    reservoir
        A configured ReservoirPy ``Reservoir`` (its ``Win``/leak/spectral radius
        are fixed at build time -- the frozen hyperparameters).
    seed
        Seed for the Mackey-Glass initial history. The runner passes the same
        seed to the connectome and its nulls, pairing them on an identical
        trajectory.
    T, washout, n_train, n_test
        Driven-series length and the post-washout train/test split sizes.
        Require ``washout + n_train + n_test <= T``.
    horizon
        Forecast horizon ``h``: target is ``x(t + horizon)``.
    n_transient
        Initial Mackey-Glass steps discarded so the series is on its attractor
        before the reservoir sees it.
    ridge_alpha, readout_bias
        Ridge readout settings (the bias absorbs the series' DC offset).
    tau, a, b, n, x0, h
        Mackey-Glass parameters.
    validate
        If True, run a sanity gate first (a canonical random reservoir must beat
        a loose NRMSE bound at ``sanity_horizon``; catches indexing/readout
        errors).
    collect_states
        If True, also return the post-washout driven state matrix (the full
        train+test span, ``(T - washout, N)``) under the ``"states"`` key -- the
        additive, opt-in manifold-probe capture path. Off by default, so the
        committed task runs are byte-identical.

    Returns
    -------
    dict
        ``{"nrmse", ...}`` plus the resolved task config for the audit trail;
        plus ``"states"`` when ``collect_states``.
    """
    if not (washout + n_train + n_test <= T):
        raise ValueError(
            f"washout + n_train + n_test ({washout + n_train + n_test}) "
            f"must be <= T ({T})."
        )

    if validate:
        _run_sanity_gate(
            seed, T, washout, n_train, n_test, sanity_horizon, n_transient,
            ridge_alpha, readout_bias, tau, a, b, n, x0, h, sanity_max_nrmse,
        )

    nrmse, states = _measure(
        reservoir, seed, T, washout, n_train, n_test, horizon, n_transient,
        ridge_alpha, readout_bias, tau, a, b, n, x0, h,
        collect_states=collect_states,
    )
    result = {
        "nrmse": nrmse,
        "n_input": T,
        "n_washout": washout,
        "n_train": n_train,
        "n_test": n_test,
        "horizon": horizon,
        "n_transient": n_transient,
        "ridge_alpha": ridge_alpha,
        "readout_bias": readout_bias,
    }
    if collect_states:
        result["states"] = states
    return result


def build_driven_series(
    seed: int,
    T: int,
    washout: int,
    n_train: int,
    horizon: int,
    n_transient: int,
    tau: int = TAU,
    a: float = A,
    b: float = B,
    n: int = N,
    x0: float = X0,
    h: float = 1.0,
) -> tuple[np.ndarray, np.ndarray, float, float]:
    """Build the normalised driving input ``x(t)`` and target ``x(t+horizon)``.

    Draws a per-seed random Mackey-Glass trajectory, discards the transient,
    forms the driven/target pair, and z-scores both with **train-region
    statistics only** (no test leakage) so ``input_scaling`` acts in std units
    and the tanh isn't swamped by the series' ~0.9 DC offset. NRMSE is
    scale-invariant, so the shared constant on the target is immaterial -- it
    only keeps input and target in the same units (useful for the demo plot).

    Returns ``(input_norm, target_norm, mean, std)`` -- ``mean``/``std`` are the
    train-region constants, for de-normalising back to physical units.
    """
    rng = np.random.default_rng(seed)
    history_length = int(np.floor(tau / h))
    history = _random_history(rng, history_length, x0)

    # Generate transient + driven window + the horizon-step lookahead for targets.
    total = n_transient + T + horizon
    full = mackey_glass(total, history, tau=tau, a=a, b=b, n=n, x0=x0, h=h)
    if not np.all(np.isfinite(full)):
        raise RuntimeError(
            "Mackey-Glass series diverged (non-finite); inspect the parameters."
        )

    series = full[n_transient:]                       # length T + horizon
    input_series = series[:T]                          # x(t),     length T
    target_series = series[horizon : horizon + T]      # x(t+h),   length T

    ref = input_series[: washout + n_train]
    mean = float(ref.mean())
    std = float(ref.std())
    if std < 1e-12:
        std = 1.0
    return (input_series - mean) / std, (target_series - mean) / std, mean, std


def _measure(
    reservoir,
    seed: int,
    T: int,
    washout: int,
    n_train: int,
    n_test: int,
    horizon: int,
    n_transient: int,
    ridge_alpha: float,
    readout_bias: bool,
    tau: int,
    a: float,
    b: float,
    n: int,
    x0: float,
    h: float,
    collect_states: bool = False,
) -> tuple[float, np.ndarray | None]:
    """Run the Mackey-Glass measurement loop. Returns ``(nrmse, states)``.

    ``states`` is the post-washout driven state matrix (train+test span) when
    ``collect_states``, else ``None``. The metric path is untouched.
    """
    input_norm, target_norm, _, _ = build_driven_series(
        seed, T, washout, n_train, horizon, n_transient, tau, a, b, n, x0, h
    )

    if getattr(reservoir, "state", None) is not None:
        reservoir.reset()
    states = reservoir.run(input_norm.reshape(-1, 1))  # (T, N)

    # Discard the washout transient, then split into train / test.
    states = states[washout:]
    targets = target_norm[washout:]
    train_states, train_targets = states[:n_train], targets[:n_train]
    test_states = states[n_train : n_train + n_test]
    test_targets = targets[n_train : n_train + n_test]

    weights, _ = _fit_ridge_readout(
        train_states, train_targets, ridge_alpha, readout_bias
    )
    predictions = _predict(test_states, weights, readout_bias)

    captured = states if collect_states else None
    if not np.all(np.isfinite(predictions)):
        return float("inf"), captured  # supercritical reservoir blew up; no-skill+
    mse = float(np.mean((predictions - test_targets) ** 2))
    target_var = float(np.var(test_targets))
    nrmse = float(np.sqrt(mse / target_var)) if target_var > 0 else float("inf")
    return nrmse, captured


def _run_sanity_gate(
    seed: int,
    T: int,
    washout: int,
    n_train: int,
    n_test: int,
    sanity_horizon: int,
    n_transient: int,
    ridge_alpha: float,
    readout_bias: bool,
    tau: int,
    a: float,
    b: float,
    n: int,
    x0: float,
    h: float,
    sanity_max_nrmse: float,
) -> None:
    """Build a canonical random reservoir; assert NRMSE below a loose bound.

    Uses Mackey-Glass-appropriate hyperparameters (lower leak than NARMA) at a
    moderate reference horizon, where a working ESN must score well below
    no-skill. A failure means an indexing/split/readout error, not a weak
    substrate.
    """
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
        leak_rate=0.3,
        input_scaling=0.5,
        seed=seed,
    )
    nrmse, _ = _measure(
        sanity_reservoir, seed + 1000, T, washout, n_train, n_test, sanity_horizon,
        n_transient, ridge_alpha, readout_bias, tau, a, b, n, x0, h,
    )
    print(
        f"[Mackey-Glass sanity] symmetric-Gaussian random reservoir at sr=0.95, "
        f"horizon={sanity_horizon}: NRMSE = {nrmse:.3f}"
    )
    assert nrmse < sanity_max_nrmse, (
        f"Mackey-Glass sanity check failed: NRMSE {nrmse:.3f} >= "
        f"{sanity_max_nrmse} at horizon {sanity_horizon} (a working forecasting "
        "ESN scores well below this; ~1.0 means the readout only predicts the "
        "mean -- likely an indexing or split error)."
    )

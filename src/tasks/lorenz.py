"""Lorenz attractor prediction task (closed-loop / free-running).

The on-message task for the connectome-as-world-model framing: teacher-force a
readout on the true Lorenz trajectory, then cut the reservoir loose to **free-run
autonomously** -- its own 3-D prediction is fed back as its next 3-D input, with
no further teacher forcing -- and ask how well it sustains the chaotic attractor.

This is qualitatively harder than the two driven tasks (NARMA emulation,
Mackey-Glass forecasting): there the reservoir always sees the true signal; here
errors compound through the feedback loop and a mildly-unstable reservoir
diverges. That fragility is the point -- it is what the two metrics measure:

- ``vpt`` (valid-prediction time, **higher = better**): how long the free-run
  stays on the true trajectory before its normalised error crosses a threshold,
  reported in **Lyapunov time** ``t * lambda_max`` (units of e-folding time, so
  comparable across systems). A *stability* metric.
- ``climate_error`` (**lower = better**): how faithfully a long free-run
  reproduces the attractor's *climate* -- the mean over x/y/z of the
  Wasserstein-1 distance between the generated and the true per-coordinate
  marginal distributions. A *fidelity* metric: a run can be stable yet collapse
  to a fixed point or limit cycle (right stability, wrong climate).

The pre-registered prediction (PREDICTION_TASKS_INTERPRETATION.md sec 4) is that
the connectome trades fidelity for stability -- decent ``vpt`` but poor
``climate`` -- so the two metrics are reported separately and the headline test
is whether the connectome's ranking *flips* between them.

Readout target: the **next state** ``s(t+1)`` (z-scored) predicted directly and
fed straight back as the next input. The increment form ``s(t+1) = s(t) +
readout(x)`` was tried first but, at the connectome-fixed N=300, its small
corrections let the free-run drift off the attractor and blow up (climate at the
divergence cap for every hyperparameter); direct prediction self-corrects toward
the attractor each step, stays bounded, and makes the climate metric
discriminative (faithful nulls reach a climate of ~0.06).

Generator: a local fixed-step **RK4** integrator (constant dt -- the clean
one-step map the reservoir learns). ``reservoirpy.datasets.lorenz`` instead uses
adaptive ``scipy.solve_ivp`` (RK45) on a non-constant grid, so the two cannot be
bit-exact, and Lorenz chaos decorrelates *any* two integrators within a few
Lyapunov times regardless. The cross-check (test suite) is therefore
short-horizon agreement to a tolerance over the first ~100 steps, not the
bit-exact identity the driven tasks could assert.
"""

import numpy as np

# Canonical chaotic Lorenz '63 parameters (lambda_max ~ 0.9056 nats/time).
SIGMA, RHO, BETA = 10.0, 28.0, 8.0 / 3.0
H = 0.03                 # integration step (matches reservoirpy's default grid)
X0 = (1.0, 1.0, 1.0)     # initial condition (matches reservoirpy's default)
# Largest Lyapunov exponent for (sigma=10, rho=28, beta=8/3); the standard
# literature value, used to express vpt in Lyapunov time.
LAMBDA_MAX = 0.9056


def _lorenz_deriv(state: np.ndarray, sigma: float, rho: float, beta: float) -> np.ndarray:
    x, y, z = state
    return np.array([sigma * (y - x), x * (rho - z) - y, x * y - beta * z])


def lorenz_rk4(
    n_timesteps: int,
    x0=X0,
    sigma: float = SIGMA,
    rho: float = RHO,
    beta: float = BETA,
    h: float = H,
) -> np.ndarray:
    """Local fixed-step RK4 Lorenz generator.

    Returns an ``(n_timesteps, 3)`` array; row 0 is ``x0`` (so the series and any
    derived increments use a constant step ``h``). A fixed step gives the
    reservoir a clean, stationary one-step map to learn -- preferable here to
    reservoirpy's adaptive solver, which the test suite cross-checks against over
    a short (pre-chaotic-divergence) horizon.
    """
    out = np.empty((n_timesteps, 3))
    s = np.asarray(x0, dtype=float)
    for i in range(n_timesteps):
        out[i] = s
        k1 = _lorenz_deriv(s, sigma, rho, beta)
        k2 = _lorenz_deriv(s + 0.5 * h * k1, sigma, rho, beta)
        k3 = _lorenz_deriv(s + 0.5 * h * k2, sigma, rho, beta)
        k4 = _lorenz_deriv(s + h * k3, sigma, rho, beta)
        s = s + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    return out


# ---------------------------------------------------------------------------
# Ridge readout (3-D targets) -- mirrors the driven tasks' closed-form solve.
# ---------------------------------------------------------------------------
def _fit_ridge_readout(states, targets, ridge_alpha, readout_bias):
    design = np.hstack([states, np.ones((states.shape[0], 1))]) if readout_bias else states
    n_features = design.shape[1]
    reg = ridge_alpha * np.eye(n_features)
    if readout_bias:
        reg[-1, -1] = 0.0  # do not shrink the intercept
    return np.linalg.solve(design.T @ design + reg, design.T @ targets)


def _readout_step(x: np.ndarray, weights: np.ndarray, readout_bias: bool) -> np.ndarray:
    """Apply the readout to a single reservoir state ``x`` -> 3-D increment."""
    if readout_bias:
        return np.concatenate([x, [1.0]]) @ weights
    return x @ weights


def _extract_reservoir(reservoir):
    """Pull dense ``W``, ``Win``, leak and bias out of a built Reservoir.

    The free-run replays ReservoirPy's leaky-tanh update manually:
    ``x <- (1 - lr) x + lr * tanh(W x + Win u + bias)``. Verified bit-exact
    against ``Reservoir.run`` for a single channel; ``bias`` is 0 here (the
    build constructs the reservoir without one).
    """
    W = reservoir.W.toarray() if hasattr(reservoir.W, "toarray") else np.asarray(reservoir.W)
    Win = reservoir.Win.toarray() if hasattr(reservoir.Win, "toarray") else np.asarray(reservoir.Win)
    bias = np.asarray(reservoir.bias).ravel() if reservoir.bias is not None else np.zeros(1)
    bias = bias if bias.size == W.shape[0] else 0.0
    return W, Win, float(reservoir.lr), bias


def _reset(reservoir) -> None:
    """Reset to the zero state. A freshly built reservoir has no state yet (its
    first ``run`` initialises it from zero), so reset is a no-op until then."""
    if getattr(reservoir, "initialized", False):
        reservoir.reset()


def _sync_state(reservoir, driver: np.ndarray) -> np.ndarray:
    """Teacher-force ``reservoir`` over ``driver`` (true z-scored states); return
    the resulting internal state vector (the synchronised free-run start)."""
    _reset(reservoir)
    reservoir.run(driver)
    return np.asarray(reservoir.state["out"]).ravel().copy()


def _free_run(x, weights, readout_bias, W, Win, lr, bias, n_steps):
    """Autonomous closed-loop roll-out.

    From synchronised state ``x`` (having just consumed the true state at the
    sync point), predict the next state ``readout(x)`` directly, feed it back as
    the next input, and repeat. Returns the ``(n_steps, 3)`` predicted trajectory
    ``[s(g), s(g+1), ...]``.
    """
    preds = np.empty((n_steps, 3))
    for i in range(n_steps):
        s = _readout_step(x, weights, readout_bias)
        preds[i] = s
        if not np.all(np.isfinite(s)):
            preds[i:] = np.inf  # blew up: mark the rest divergent and stop
            break
        x = (1.0 - lr) * x + lr * np.tanh(W @ x + Win @ s + bias)
    return preds


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def _valid_prediction_time(preds, truth, rms_norm, epsilon, h, lambda_max) -> float:
    """First step at which the normalised error exceeds ``epsilon``, in Lyapunov
    time. Non-finite predictions count as immediately invalid."""
    err = np.linalg.norm(preds - truth, axis=1)
    err = np.where(np.isfinite(err), err, np.inf) / rms_norm
    over = np.flatnonzero(err > epsilon)
    steps = int(over[0]) if over.size else preds.shape[0]
    return steps * h * lambda_max


def _climate_error(free_run, reference) -> float:
    """Mean over x/y/z of the Wasserstein-1 distance between the free-run's and
    the reference attractor's per-coordinate marginals. ``inf`` if the free-run
    diverged (so the divergence-robust stats cap it)."""
    from scipy.stats import wasserstein_distance

    if not np.all(np.isfinite(free_run)):
        return float("inf")
    return float(np.mean([
        wasserstein_distance(free_run[:, d], reference[:, d]) for d in range(3)
    ]))


# ---------------------------------------------------------------------------
# Trajectory assembly + measurement
# ---------------------------------------------------------------------------
def build_trajectory(seed, n_transient, washout, n_train, sync_len, n_windows,
                     window_spacing, free_run_len, sigma, rho, beta, h, x0):
    """Generate one Lorenz trajectory and z-score it on the teacher-forced region.

    The per-seed initial condition is a small perturbation of ``x0`` (so each
    seed visits a different stretch of the attractor, as the driven tasks vary
    their input per seed). Returns ``(S, train_slice, holdout_start, mean, std)``
    where ``S`` is the z-scored ``(n_total, 3)`` trajectory.
    """
    rng = np.random.default_rng(seed)
    start = np.asarray(x0, dtype=float) + 0.01 * (rng.random(3) - 0.5)

    holdout_start = n_transient + washout + n_train
    n_total = holdout_start + (n_windows - 1) * window_spacing + free_run_len
    traj = lorenz_rk4(n_total, x0=start, sigma=sigma, rho=rho, beta=beta, h=h)
    if not np.all(np.isfinite(traj)):
        raise RuntimeError("Lorenz RK4 series diverged (non-finite); check params.")

    # z-score on the teacher-forced region only (no test leakage).
    fit = traj[n_transient:holdout_start]
    mean = fit.mean(axis=0)
    std = fit.std(axis=0)
    std = np.where(std < 1e-12, 1.0, std)
    return (traj - mean) / std, holdout_start, mean, std


def _measure(reservoir, seed, *, n_transient, washout, n_train, sync_len,
             n_windows, window_spacing, free_run_len, climate_len, climate_washout,
             epsilon, ridge_alpha, readout_bias, sigma, rho, beta, h, x0,
             lambda_max, collect_states=False):
    """Run the full closed-loop protocol; return ``(vpt, climate_error, states)``.

    ``vpt`` is the mean valid-prediction time (Lyapunov time) over ``n_windows``
    free-runs from held-out synchronisation points; ``climate_error`` comes from
    one long free-run. ``states`` is the post-washout **teacher-forced** driven
    state matrix the readout is fit on (``(n_train, N)``) when ``collect_states``,
    else ``None`` -- the manifold-probe capture path (the driven manifold, not the
    autonomous free-run). The metric path is untouched.
    """
    S, holdout_start, _, _ = build_trajectory(
        seed, n_transient, washout, n_train, sync_len, n_windows, window_spacing,
        free_run_len, sigma, rho, beta, h, x0,
    )

    # Teacher-force over the training region; fit the readout state(t) ->
    # next-state s(t+1) (predicted directly, fed straight back in the free-run).
    train = S[n_transient:holdout_start]            # washout + n_train states
    _reset(reservoir)
    states = reservoir.run(train)[washout:]          # drop the washout transient
    next_state = S[n_transient + washout + 1: holdout_start + 1]
    weights = _fit_ridge_readout(states, next_state, ridge_alpha, readout_bias)

    W, Win, lr, bias = _extract_reservoir(reservoir)
    rms_norm = float(np.sqrt(np.mean(np.sum(train ** 2, axis=1))))

    # VPT: free-run from each held-out synchronisation point.
    vpts = []
    for k in range(n_windows):
        g = holdout_start + k * window_spacing
        x = _sync_state(reservoir, S[g - sync_len: g])
        preds = _free_run(x, weights, readout_bias, W, Win, lr, bias, free_run_len)
        vpts.append(_valid_prediction_time(
            preds, S[g: g + free_run_len], rms_norm, epsilon, h, lambda_max))
    vpt = float(np.mean(vpts))

    # Climate: one long free-run from the held-out start; compare its marginals
    # (after discarding a settling transient) to the true post-transient climate.
    g = holdout_start
    x = _sync_state(reservoir, S[g - sync_len: g])
    long_run = _free_run(x, weights, readout_bias, W, Win, lr, bias, climate_len)
    climate = _climate_error(long_run[climate_washout:], S[n_transient:])

    captured = states if collect_states else None
    return vpt, climate, captured


def evaluate(
    reservoir,
    seed: int,
    n_transient: int = 1000,
    washout: int = 200,
    n_train: int = 10000,
    sync_len: int = 200,
    n_windows: int = 20,
    window_spacing: int = 500,
    free_run_len: int = 1000,
    climate_len: int = 5000,
    climate_washout: int = 500,
    epsilon: float = 0.4,
    ridge_alpha: float = 1e-7,
    readout_bias: bool = True,
    sigma: float = SIGMA,
    rho: float = RHO,
    beta: float = BETA,
    h: float = H,
    x0=X0,
    lambda_max: float = LAMBDA_MAX,
    validate: bool = False,
    collect_states: bool = False,
    sanity_input_scaling: float = 0.1,
    sanity_leak_rate: float = 1.0,
    sanity_min_vpt: float = 0.5,
    **kwargs,
) -> dict:
    """Closed-loop Lorenz evaluator. Returns **both** metrics from one matrix cell.

    Teacher-forces a ridge readout on the true trajectory, then free-runs the
    reservoir autonomously: ``vpt`` (mean valid-prediction time over ``n_windows``
    held-out roll-outs, in Lyapunov time) and ``climate_error`` (marginal
    Wasserstein-1 of one long free-run vs the true attractor). Mirrors the driven
    tasks' ``evaluate(reservoir, seed, **cfg) -> dict`` interface but diverges
    internally (closed loop, 3-D, two metrics).

    Parameters
    ----------
    reservoir
        A built ReservoirPy ``Reservoir`` with a 3-channel ``Win`` (the frozen
        hyperparameters and spectral radius are fixed at build time).
    seed
        Seed for the Lorenz initial condition (runner passes the same seed to the
        connectome and its nulls, pairing them on an identical trajectory).
    n_transient, washout, n_train
        Steps discarded onto the attractor; teacher-forcing washout; readout
        training length.
    sync_len, n_windows, window_spacing, free_run_len
        VPT protocol: each of ``n_windows`` free-runs is synchronised by
        teacher-forcing ``sync_len`` steps, then rolls out ``free_run_len`` steps;
        window starts are spaced ``window_spacing`` apart through the held-out
        region.
    climate_len, climate_washout
        Long free-run length and its settling transient for the climate metric.
    epsilon
        VPT error threshold on ``||pred - true|| / rms(||true||)``.
    validate
        If True, run a sanity gate first (a canonical random reservoir must reach
        a non-trivial VPT; catches readout/indexing/feedback errors).
    collect_states
        If True, also return the post-washout **teacher-forced** driven state
        matrix (``(n_train, N)``, the manifold the readout is fit on -- not the
        autonomous free-run) under the ``"states"`` key. Off by default, so the
        committed task runs are byte-identical.

    Returns
    -------
    dict
        ``{"vpt", "climate_error", ...}`` plus the resolved task config; plus
        ``"states"`` when ``collect_states``.
    """
    if validate:
        _run_sanity_gate(
            seed, n_transient, washout, n_train, sync_len, n_windows,
            window_spacing, free_run_len, climate_len, climate_washout, epsilon,
            ridge_alpha, readout_bias, sigma, rho, beta, h, x0, lambda_max,
            sanity_input_scaling, sanity_leak_rate, sanity_min_vpt,
        )

    vpt, climate_error, states = _measure(
        reservoir, seed, n_transient=n_transient, washout=washout,
        n_train=n_train, sync_len=sync_len, n_windows=n_windows,
        window_spacing=window_spacing, free_run_len=free_run_len,
        climate_len=climate_len, climate_washout=climate_washout, epsilon=epsilon,
        ridge_alpha=ridge_alpha, readout_bias=readout_bias, sigma=sigma, rho=rho,
        beta=beta, h=h, x0=x0, lambda_max=lambda_max,
        collect_states=collect_states,
    )
    result = {
        "vpt": vpt,
        "climate_error": climate_error,
        "n_transient": n_transient,
        "washout": washout,
        "n_train": n_train,
        "sync_len": sync_len,
        "n_windows": n_windows,
        "window_spacing": window_spacing,
        "free_run_len": free_run_len,
        "climate_len": climate_len,
        "epsilon": epsilon,
        "ridge_alpha": ridge_alpha,
        "readout_bias": readout_bias,
    }
    if collect_states:
        result["states"] = states
    return result


def _run_sanity_gate(seed, n_transient, washout, n_train, sync_len, n_windows,
                     window_spacing, free_run_len, climate_len, climate_washout,
                     epsilon, ridge_alpha, readout_bias, sigma, rho, beta, h, x0,
                     lambda_max, input_scaling, leak_rate, min_vpt) -> None:
    """Build a canonical random reservoir; assert it free-runs for a non-trivial
    VPT. A failure means a readout/indexing/feedback bug, not a weak substrate."""
    from src.nulls import random_gaussian  # noqa: F401  (kept for parity)
    from src.reservoir.weights import apply_weight_scheme
    from src.reservoir.build import build_from_adjacency

    n_nodes, density = 300, 0.067
    rng = np.random.default_rng(seed)
    upper = np.triu(rng.random((n_nodes, n_nodes)) < density, k=1)
    sanity_mask = (upper | upper.T).astype(float)
    weighted = apply_weight_scheme(sanity_mask, "symmetric_gaussian", seed=seed)
    sanity_reservoir = build_from_adjacency(
        weighted_adjacency=weighted, target_spectral_radius=0.95,
        leak_rate=leak_rate, input_scaling=input_scaling, seed=seed, input_dim=3,
    )
    vpt, climate_error, _ = _measure(
        sanity_reservoir, seed + 1000, n_transient=n_transient, washout=washout,
        n_train=n_train, sync_len=sync_len, n_windows=n_windows,
        window_spacing=window_spacing, free_run_len=free_run_len,
        climate_len=climate_len, climate_washout=climate_washout, epsilon=epsilon,
        ridge_alpha=ridge_alpha, readout_bias=readout_bias, sigma=sigma, rho=rho,
        beta=beta, h=h, x0=x0, lambda_max=lambda_max,
    )
    print(f"[Lorenz sanity] symmetric-Gaussian random reservoir at sr=0.95: "
          f"vpt = {vpt:.2f} Lyapunov times, climate_error = {climate_error:.3f}")
    assert vpt > min_vpt, (
        f"Lorenz sanity check failed: vpt {vpt:.2f} <= {min_vpt} Lyapunov times "
        "(a working closed-loop ESN free-runs Lorenz well past this; a near-zero "
        "VPT means the readout/feedback loop is broken, not a weak substrate)."
    )

"""Memory capacity under anatomical I/O routing (multi-aperture, single run).

Routing variant of Jaeger memory capacity for the human I/O-routing thread. The
reservoir is driven by white noise ONCE (the input is already routed to the chosen
input nodes via ``Win`` at build time); MC is then measured through several
**readout apertures** -- subsets of reservoir units (e.g. each Yeo intrinsic
network, and the pooled cortex) -- by restricting the ridge design matrix to those
state columns. ``reservoir.run`` is the expensive shared step, so every aperture
reuses the one state trajectory.

The per-aperture MC math is identical to ``src/tasks/memory_capacity.py`` (nested
design matrices, rank-1 Gram down-date per lag); it is reproduced here restricted
to a column subset rather than editing the frozen full-state evaluator (whose
byte-identity backs the four committed tasks).
"""

import numpy as np
from scipy.stats import pearsonr


def _mc_on_columns(
    states_after_warmup: np.ndarray,
    u_flat: np.ndarray,
    max_lag: int,
    ridge_alpha: float,
) -> float:
    """MC total over an already column-restricted state matrix ``(n, m)``.

    Same down-dated Gram scheme as ``memory_capacity._measure`` but on ``m`` readout
    columns: ridge is ``ridge_alpha * I_m`` (per-unit, so aperture-size consistent).
    """
    n_after_warmup, n_units = states_after_warmup.shape
    ridge_eye = ridge_alpha * np.eye(n_units)
    gram = states_after_warmup[1:].T @ states_after_warmup[1:]
    total = 0.0
    for k in range(1, max_lag + 1):
        X = states_after_warmup[k:]
        y = u_flat[: n_after_warmup - k]
        w = np.linalg.solve(gram + ridge_eye, X.T @ y)
        pred = X @ w
        if np.std(pred) < 1e-12 or np.std(y) < 1e-12:
            mc_k = 0.0
        else:
            r, _ = pearsonr(pred, y)
            mc_k = r ** 2
        total += mc_k
        if k < max_lag:  # down-date: drop row k (the first row of the current X)
            row = states_after_warmup[k]
            gram = gram - np.outer(row, row)
    return float(total)


def evaluate(
    reservoir,
    seed: int,
    T: int,
    warmup: int,
    max_lag: int,
    ridge_alpha: float,
    input_scaling: float,
    readout_apertures: dict,
    primary_aperture: str = "cortex",
    **kwargs,
) -> dict:
    """Multi-aperture routing MC.

    Parameters
    ----------
    reservoir
        Reservoir already built with ``Win`` routed to the input nodes.
    readout_apertures
        ``{name: node_indices}`` -- integer index arrays into the FULL reservoir
        (state columns). Supplied per (variant, seed) by the routing runner so the
        random-placement control can re-draw its readout sets each seed while the
        anatomical variants keep fixed Yeo/cortex indices.
    primary_aperture
        Which aperture's MC is echoed as ``"mc"`` (the runner's headline metric).

    Returns
    -------
    dict
        ``{"mc_<name>": float for each aperture, "mc": mc_<primary_aperture>}``.
    """
    rng = np.random.default_rng(seed)
    u = rng.uniform(-input_scaling, input_scaling, size=(T, 1))

    if getattr(reservoir, "state", None) is not None:
        reservoir.reset()
    states = reservoir.run(u)  # (T, N_full)

    states_after_warmup = states[warmup:]
    u_flat = u[warmup:, 0]

    out = {}
    for name, cols in readout_apertures.items():
        sub = states_after_warmup[:, np.asarray(cols)]
        out[f"mc_{name}"] = _mc_on_columns(sub, u_flat, max_lag, ridge_alpha)

    if f"mc_{primary_aperture}" not in out:
        raise ValueError(
            f"primary_aperture {primary_aperture!r} not in apertures {list(readout_apertures)}"
        )
    out["mc"] = out[f"mc_{primary_aperture}"]
    return out

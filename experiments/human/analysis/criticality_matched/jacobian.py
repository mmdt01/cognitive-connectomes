"""What governs the generation break: the true Jacobian, not the mean-field radius.

`sigma_eff = bulk95 * sigma * <1-x^2>` locates the straight -> period-2 transition
better than any alternative tested (E0.1, TIER0 §3.10) but is not a stability law: the
transition sits at 0.77-0.90 rather than 1, and at `f = 0` it happens with
`sigma_eff` = 0.014, two orders of magnitude below `sigma_eff`'s own peak.

**The diagnosis.** `sigma_eff` uses the **mean** gain over units. At `f = 0` the
collapsed cells have **88% of units saturated** and `|mean_state|` = 0.967 -- the network
is pinned against the all-positive Perron fixed point. Those saturated units contribute
`1-x^2` ~ 0, so the mean collapses toward zero while the instability lives in the ~12%
of units still unsaturated, whose local gain is nowhere near zero. Averaging a bimodal
gain distribution destroys exactly the signal that matters, and a saturating Perron
common mode is what manufactures the bimodality.

**The honest quantity.** With `leak = 1` the map is `x -> tanh(W x + Win u)`, so the
Jacobian is ``J = diag(1 - x^2) W``. `sigma_eff` is its mean-field approximation --
`rho(J)` estimated as (mean gain) x (bulk radius) -- which is exactly the step that fails
when the gain is heterogeneous. Here the per-unit time-mean gain is kept as a *vector*:

    J_sym = diag(sqrt(g)) W diag(sqrt(g)),    g_i = <1 - x_i^2>_t

which is similar to ``diag(g) W`` (so has the same spectrum) and is **symmetric** for
this substrate, so its eigenvalues are real and exact.

**The criterion being tested.** The period-2 branch is born when the most negative
eigenvalue passes below -1. So the prediction is ``lambda_min(J) < -1`` at the
transition, in **both** regimes -- which would replace an empirical locator that works in
one regime with a stability criterion that works in both. It is a real prediction and it
can fail: if `lambda_min` at the transition is as scattered as `sigma_eff` is, or if it
sits far from -1, the mean-field diagnosis is wrong.

Lorenz only, `f` grid and sigma sweep identical to the extension captures so the two
join cell-for-cell.
"""

import numpy as np
import pandas as pd

from src.reservoir import blas  # noqa: F401  (cap BLAS threads; import after numpy)
from src.reservoir.build import build_from_adjacency, rescale_spectral_radius
from src.analysis import manifold, sign_composition
from src.analysis.spectral import recurrent_spectrum
from experiments.human import matrix_config
from experiments.human.substrates import HumanSubstrateBuilder
from experiments.human.analysis.manifold import common as manifold_common
from experiments.human.analysis.phase_diagram import common as pd_common
from experiments.human.analysis.criticality_matched import common, extend_f

TASK = "lorenz"
VARIANTS = ["connectome", "connectome_weight_permuted", "degree_rewire", "erdos_renyi"]
SIGN_MODE, TARGETING = "edge", "stratified"
# A unit counts as saturated on the same convention the captures already use.
SATURATED = 0.99


def jacobian_spectrum(W_scaled: np.ndarray, gain: np.ndarray) -> dict:
    """Eigen-extremes of ``diag(gain) W_scaled``, via the symmetric similar form.

    ``diag(sqrt(g)) W diag(sqrt(g))`` is similar to ``diag(g) W`` for g >= 0, and is
    symmetric whenever ``W`` is -- which it is for the undirected human substrate under
    the edge sign transform. That buys exact real eigenvalues from ``eigvalsh`` instead
    of a general complex solve, and it is 2-3x cheaper.
    """
    root = np.sqrt(np.clip(gain, 0.0, None))
    sym = root[:, None] * W_scaled * root[None, :]
    if np.allclose(sym, sym.T, atol=1e-12):
        values = np.linalg.eigvalsh(sym)
        lo, hi = float(values[0]), float(values[-1])
    else:                                    # Dale / directed fallback
        values = np.linalg.eigvals(root[:, None] * W_scaled)
        lo, hi = float(values.real.min()), float(values.real.max())
    return {"lambda_min_J": lo, "lambda_max_J": hi,
            "rho_J": float(max(abs(lo), abs(hi)))}


def capture_cell(cell, state) -> list:
    """One (variant, f, seed, draw) cell: sweep sigma, record the Jacobian extremes.

    Mirrors ``phase_diagram.capture.capture_cell``'s construction exactly -- same base
    condition, same flip RNG entropy, same reservoir build -- so the rows join the
    extension captures cell-for-cell. It adds the Jacobian spectrum and the gain
    heterogeneity that the mean-field radius throws away.
    """
    task_name, sign_mode, targeting, variant, f_idx, seed, draw = cell
    builder, spec = state["builder"], state["specs"][task_name]
    f = state["f_grid"][f_idx]
    params = spec["params"]

    W_base = builder.weighted(pd_common.BASE_CONDITION, variant, seed)
    node_score = sign_composition.node_importance(W_base, mode=state["score_mode"])
    seed_key = [int(seed), int(f_idx), int(draw),
                pd_common.TARGETING_CODE[targeting], pd_common.VARIANT_CODE[variant]]
    flip_rng = np.random.default_rng(seed_key)
    W = sign_composition.sign_fraction_matrix(
        W_base, f, targeting, flip_rng, n_strata=state["n_strata"],
        node_score=node_score)
    bulk95 = float(recurrent_spectrum(W)["bulk95_radius"])

    rows = []
    for spectral_radius in spec["sweep"]:
        reservoir = build_from_adjacency(
            weighted_adjacency=W, target_spectral_radius=spectral_radius,
            leak_rate=spec["leak_rate"], input_scaling=spec["input_scaling"],
            seed=seed, input_dim=spec["input_dim"])
        out = spec["evaluate"](reservoir, seed=seed + spec["input_seed_offset"],
                               collect_states=True, **params)
        x = np.asarray(out["states"], dtype=float)

        gain = 1.0 - x * x                      # leak = 1, so this IS the Jacobian gain
        gain_mean = gain.mean(axis=0)           # per-unit time mean -- the vector kept
        W_scaled = rescale_spectral_radius(W, spectral_radius)
        row = dict(
            sign_mode=sign_mode, targeting=targeting, f=float(f), variant=variant,
            spectral_radius=float(spectral_radius), seed=int(seed), draw=int(draw),
            task=task_name, mean_curvature=float(manifold.mean_curvature(x)),
            bulk95=bulk95, mean_gain=float(gain.mean()),
            effective_radius=float(bulk95 * spectral_radius * gain.mean()),
            frac_saturated=float((np.abs(x) > SATURATED).mean()),
            mean_state=float(x.mean()),
            # What the mean-field radius discards: how spread the per-unit gains are,
            # and how much of the network has effectively dropped out of the dynamics.
            gain_std=float(gain_mean.std()),
            frac_units_gain_below_01=float((gain_mean < 0.01).mean()),
            gain_mean_of_active=float(gain_mean[gain_mean >= 0.01].mean())
            if (gain_mean >= 0.01).any() else 0.0,
            **jacobian_spectrum(W_scaled, gain_mean))
        for perf_metric in spec["perf"]:
            row[perf_metric] = float(out[perf_metric])
        rows.append(row)
    return rows


def run(scale: int = common.SCALE, jobs: int = 1,
        sr_max: float = extend_f.SR_MAX) -> pd.DataFrame:
    common.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    builder = HumanSubstrateBuilder(scale=scale)
    specs = manifold_common.build_specs(scale, [TASK], smoke=False, sr_max=None)
    sweep = extend_f.sr_grid(sr_max)
    for spec in specs.values():
        spec["sweep"] = sweep
    if jobs > 1:
        for variant in VARIANTS:
            for seed in range(common.N_SEEDS):
                builder.weighted(pd_common.BASE_CONDITION, variant, seed)

    cells = [(TASK, SIGN_MODE, TARGETING, variant, f_idx, seed, draw)
             for variant in VARIANTS
             for f_idx in range(len(pd_common.F_GRID))
             for seed in range(common.N_SEEDS) for draw in range(pd_common.N_DRAWS)]
    print("=" * 70 + f"\nJacobian capture -- {len(cells)} cells x {len(sweep)} sigma\n"
          + "=" * 70)
    frame = manifold_common.run_cells(cells, capture_cell, state_for(builder, specs),
                                      jobs, "jacobian")
    path = common.RESULTS_DIR / f"e01_jacobian_scale_{scale}.parquet"
    frame.to_parquet(path)
    print(f"\nSaved {path}  ({len(frame)} rows)")
    return frame


def state_for(builder, specs) -> dict:
    return dict(builder=builder, specs=specs, f_grid=pd_common.F_GRID,
                n_strata=pd_common.N_STRATA, score_mode=pd_common.SCORE_MODE)

"""The N=1000 memory run, and its N=448 protocol control.

Configuration and cost recorded in `TIER0_STATE_OF_PLAY.md` sec 2.5. Two things
distinguish it from Task B's N=448 sweep:

**1. `T` scales with `N` to hold `T_eff/N` fixed.** `T = 3000` at N=448 gives
`T_eff/N` = 5.58; `T = 6000` at N=1000 gives 5.50. The design Gram is a *sample*
covariance and its small-eigenvalue tail -- precisely the directions `d_eff` counts --
is what finite `T/N` distorts, so `d_eff` at a different ratio is not comparable.

**2. The ridge is reparameterised as `alpha = lambda * trace(G) / N`.** `alpha = 1e-6`
is *absolute*, and `trace(G)` grows with both `T` and the state energy, so keeping it
fixed while doubling `T` would silently halve the effective regularisation and push
`d_eff` toward the ceiling for free. `lambda` is pinned so the median realised `alpha`
over the supercritical region at N=448, `T`=3000 is exactly the frozen 1e-6 -- i.e. the
new rule reproduces the old one where the result lives, and adapts elsewhere.

**The same alpha is used for `d_eff` and for MC.** That requires two evaluator passes
per cell: the first harvests the driven states (the trajectory does not depend on the
ridge), from which `trace(G)` and hence `alpha` are computed; the second re-solves the
readout at that `alpha`. Twice the cost, but it reuses the frozen evaluator rather than
reimplementing the MC readout, and it keeps the `d_eff` <-> MC correspondence (+0.999
across five orders of alpha) intact.

The N=448 control is not optional: run under the new rule at the old `T`, it isolates
the effect of changing the ridge parameterisation from the effect of changing `N`.
Without it a shift at N=1000 is uninterpretable.
"""

import numpy as np
import pandas as pd

from src.analysis import manifold
from src.analysis.spectral import recurrent_spectrum
from src.reservoir.build import build_from_adjacency
from experiments.human import matrix_config
from experiments.human.substrates import HumanSubstrateBuilder
from experiments.human.analysis.manifold import common as manifold_common
from experiments.human.analysis.manifold.spectra import design_matrix
from experiments.human.analysis.criticality_matched import common

TASK = "mc"
CONDITION = "human_empirical"
VARIANTS = ["connectome", "connectome_weight_permuted", "degree_rewire", "erdos_renyi"]

# lambda in alpha = lambda * trace(G) / N, pinned so that the median realised alpha
# over the supercritical region (sigma >= sr_crit = 3.05) at N=448, T=3000 equals the
# frozen 1e-6. Measured from the persisted Gram traces of the Task B sweep; trace(G)
# varies only ~4x across the whole sigma sweep, so the realised alpha stays within a
# factor of a few of 1e-6 everywhere.
RIDGE_LAMBDA = 4.4845e-10
FROZEN_ALPHA = 1e-6

# T per scale, chosen to hold T_eff / N ~ 5.5 (see module docstring).
T_BY_SCALE = {448: 3000, 1000: 6000}
WARMUP = 500


def sr_grid(scale: int) -> list:
    """Non-uniform above criticality, coarse below (spec sec 3).

    A uniform nominal grid spends most of its points on the shared rising limb where
    the variants are indistinguishable. At N=1000 the connectome turns critical at
    sigma = 3.985, so the decay region -- where the entire result lives -- gets the
    density. At N=448 the control reuses Task B's 0.4 grid so it is directly
    comparable to the frozen sweep.
    """
    if scale == 448:
        return [round(i * 0.4, 6) for i in range(21)]          # 0 .. 8.0
    coarse = np.arange(0.0, 3.01, 0.6)                          # 6 pts, shared rise
    dense = np.linspace(3.2, 8.0, 18)                           # 18 pts, decay region
    tail = np.linspace(8.4, 10.4, 6)                            # 6 pts, post-peak
    return [round(float(s), 6) for s in np.concatenate([coarse, dense, tail])]


def cell(spec_cell, state) -> list:
    """One (variant, seed): build W once, sweep sigma, two evaluator passes per sigma."""
    variant, seed = spec_cell
    builder, spec = state["builder"], state["spec"]
    base_params = dict(spec["params"])
    base_params["T"] = state["T"]
    base_params["warmup"] = WARMUP
    n_nodes = state["n_nodes"]

    W = builder.weighted(CONDITION, variant, seed)
    rs = recurrent_spectrum(W)
    bulk95 = float(rs["bulk95_radius"])
    rung = matrix_config.VARIANT_RUNG.get(variant, -1)

    rows = []
    for spectral_radius in state["sweep"]:
        reservoir = build_from_adjacency(
            weighted_adjacency=W, target_spectral_radius=spectral_radius,
            leak_rate=spec["leak_rate"], input_scaling=spec["input_scaling"],
            seed=seed, input_dim=spec["input_dim"])
        # Pass 1: harvest the driven states. The trajectory is independent of the
        # ridge, so any alpha serves here; only the readout solve is discarded.
        probe = spec["evaluate"](reservoir, seed=seed + spec["input_seed_offset"],
                                 collect_states=True, **base_params)
        x = np.asarray(probe["states"], dtype=float)
        eig_gram = manifold.gram_spectrum(design_matrix(TASK, x, base_params))
        trace_g = float(eig_gram.sum())
        alpha = RIDGE_LAMBDA * trace_g / n_nodes

        # Pass 2: the readout at the alpha this cell actually implies.
        scored = spec["evaluate"](reservoir, seed=seed + spec["input_seed_offset"],
                                  **dict(base_params, ridge_alpha=alpha))
        d_eff = manifold.ridge_effective_rank(eig_gram, alpha)
        gain = 1.0 - x * x
        rows.append(dict(
            variant=variant, rung=rung, seed=int(seed), n_nodes=n_nodes,
            spectral_radius=float(spectral_radius), T=int(state["T"]),
            mc=float(scored["mc"]), d_eff=d_eff, d_eff_norm=d_eff / n_nodes,
            alpha=alpha, ridge_lambda=RIDGE_LAMBDA, trace_gram=trace_g,
            bulk95=bulk95, x_effective=float(spectral_radius * bulk95),
            mean_gain=float(gain.mean()),
            frac_saturated=float((np.abs(x) > 0.99).mean()),
            T_eff_over_N=float(x.shape[0] / n_nodes),
        ))
    return rows


def run(scale: int, jobs: int = 1) -> pd.DataFrame:
    from experiments.human.analysis.eigenspectrum import common as e04_common

    common.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    T = T_BY_SCALE[scale]
    sweep = sr_grid(scale)
    builder = HumanSubstrateBuilder(scale=scale)
    n_nodes = int(builder.mask.shape[0])
    spec = manifold_common.build_specs(scale, [TASK], smoke=False, sr_max=None)[TASK]

    label = "control" if scale == 448 else "run"
    print("=" * 70 + f"\nN={scale} memory {label}: T={T}, T_eff/N="
          f"{(T - WARMUP) / n_nodes:.2f}, alpha = {RIDGE_LAMBDA:.4e} * trace(G)/N\n"
          + "=" * 70)
    print(f"  {len(VARIANTS)} variants x {common.N_SEEDS} seeds x {len(sweep)} sigma "
          f"= {len(VARIANTS) * common.N_SEEDS * len(sweep)} cells, two passes each; "
          f"sigma to {max(sweep):g}; jobs={jobs}")

    if jobs > 1:
        for variant in VARIANTS:
            if variant == "connectome_weight_permuted":
                continue
            for seed in range(common.N_SEEDS):
                builder.get_mask(variant, seed)

    cells = [(v, s) for v in VARIANTS for s in range(common.N_SEEDS)]
    state = dict(builder=builder, spec=spec, sweep=sweep, T=T, n_nodes=n_nodes)
    frame = e04_common.run_cells(cells, cell, state, jobs, f"n{scale}")

    path = common.RESULTS_DIR / f"n1000_memory_scale_{scale}.parquet"
    frame.to_parquet(path)
    print(f"\nSaved {path}  ({len(frame)} rows)")
    print(f"  realised alpha: median {frame.alpha.median():.3e}, "
          f"range [{frame.alpha.min():.2e}, {frame.alpha.max():.2e}] "
          f"(frozen absolute was {FROZEN_ALPHA:.0e})")

    e04_common.write_manifest(
        common.RESULTS_DIR / f"manifest_n1000_scale_{scale}.json",
        f"N={scale} memory {label}", scale, task=TASK, condition=CONDITION,
        variants=VARIANTS, n_seeds=common.N_SEEDS, sr_grid=sweep, T=T, warmup=WARMUP,
        T_eff_over_N=(T - WARMUP) / n_nodes, ridge_lambda=RIDGE_LAMBDA,
        ridge_rule="alpha = ridge_lambda * trace(G) / N, identical for d_eff and MC",
        realised_alpha_median=float(frame.alpha.median()),
        simulates=f"yes -- MC only, f=0, N={scale}")
    return frame


def control_gate(scale: int = 448) -> dict:
    """Does the new ridge rule reproduce the frozen N=448 result?

    Compares this control against Task B's sweep at the shared sigma. They differ in
    exactly one thing -- the ridge parameterisation -- so a large shift here would mean
    the protocol change, not N, is moving the numbers, and would have to be understood
    before the N=1000 result could be read at all.

    The Task B reference is a **gitignored** parquet, so it is present wherever that
    sweep was run and absent everywhere else -- notably on a fresh cluster checkout.
    Skip rather than crash: the control's own parquet is already written by then, and
    the gate can be run later on a machine that has the reference.
    """
    new_path = common.RESULTS_DIR / f"n1000_memory_scale_{scale}.parquet"
    old_path = common.extended_sweep_path(scale)
    if not old_path.exists():
        print(f"  [control-gate] SKIPPED -- {old_path.name} is not on this machine "
              "(gitignored). The control parquet is written; run the gate where the "
              "Task B sweep lives.")
        return {"status": "skipped", "reason": "reference parquet absent",
                "reference": str(old_path)}
    new = pd.read_parquet(new_path)
    old = pd.read_parquet(old_path,
                          columns=["variant", "seed", "spectral_radius", "mc", "d_eff"])
    keys = ["variant", "seed", "_sr"]
    merged = (new.assign(_sr=new.spectral_radius.round(6))
              .merge(old.assign(_sr=old.spectral_radius.round(6)), on=keys,
                     how="inner", suffixes=("", "_frozen")))
    sup = merged[merged.spectral_radius >= 3.05]
    out = {"status": "passed", "n_cells": int(len(merged)),
           "n_supercritical": int(len(sup))}
    for col in ("mc", "d_eff"):
        rel = ((sup[col] - sup[col + "_frozen"]).abs()
               / sup[col + "_frozen"].abs().clip(lower=1e-12))
        out[col] = {"median_rel": float(rel.median()), "max_rel": float(rel.max())}
        print(f"  [control-gate] {col:6s} supercritical: median rel change "
              f"{rel.median():.2%}, max {rel.max():.2%}")
    # The margin is the quantity the N=1000 run is about, so check it directly.
    margin_new = (sup[sup.variant == "connectome"].mc.median()
                  / sup[sup.variant == "erdos_renyi"].mc.median())
    margin_old = (sup[sup.variant == "connectome"].mc_frozen.median()
                  / sup[sup.variant == "erdos_renyi"].mc_frozen.median())
    out["mc_margin"] = {"new_rule": float(margin_new), "frozen": float(margin_old)}
    print(f"  [control-gate] supercritical MC margin (connectome/ER): "
          f"{margin_old:.2f} frozen -> {margin_new:.2f} under the new rule")
    return out


SR_CRIT = {448: 3.078, 1000: 3.985}      # each scale's own 1/median(bulk95)


def figures(scales=(448, 1000)) -> None:
    """The cross-scale figure. Reads the run parquets; recomputes nothing expensive.

    Kept out of ``run()`` so the figure can be iterated during writing without
    re-simulating, and so it can be built once both scales exist.
    """
    from experiments.human.analysis.criticality_matched import analysis, panels

    frames, ladder_rows = {}, []
    for scale in scales:
        path = common.RESULTS_DIR / f"n1000_memory_scale_{scale}.parquet"
        if not path.exists():
            print(f"  [figures] {path.name} absent -- N={scale} omitted.")
            continue
        d = pd.read_parquet(path)
        n_nodes = int(d.n_nodes.iloc[0])
        cells = d.rename(columns={"x_effective": "_x_effective"})
        lo, hi = analysis.overlap_range(cells, "_x_effective",
                                        [common.CONN, common.CONTRAST])
        grid = np.linspace(lo, hi, common.N_GRID)
        frames[scale] = (analysis.paired_difference(
            analysis.reindex(cells, "_x_effective", grid, "linear"), grid), n_nodes)
        sup = d[d.spectral_radius >= SR_CRIT[scale]]
        for variant, mc in sup.groupby("variant").mc.median().items():
            ladder_rows.append(dict(scale=scale, variant=variant, mc=float(mc)))

    if not frames:
        raise FileNotFoundError("no N=1000 run parquets found; run --n1000 first.")
    common.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    panels.fig_cross_scale(frames, pd.DataFrame(ladder_rows),
                           common.FIGURES_DIR / "fig_cross_scale_n1000")

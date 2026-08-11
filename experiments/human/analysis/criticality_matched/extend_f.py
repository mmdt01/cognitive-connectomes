"""Item 2: extend the ``f > 0`` sweep so the cross-panel crossing is observable.

The reindexed (f, sigma) panels are censored at ``sigma = 6`` for every ``f > 0``,
which caps coverage at ``sigma*bulk95`` = 2.336 -- short of where the boundaries would
meet. This runs the panel grid out to ``sigma = 11.2`` (x = 3.64 at the connectome's
``bulk95``), past the x ~ 3.5 the linear extrapolation implies.

**Why the whole sigma range is re-run rather than appended.** The frozen ``f > 0``
flip patterns are not machine-portable (E0.4 §6: unstable ``np.argsort`` tie order on a
heavily-tied edge score). Appending new high-sigma cells to the frozen low-sigma ones
would splice two different flip realisations into one curve. So this captures a fresh,
internally consistent realisation set over the full range. ``f = 0`` is the identity
and reproduces the frozen values exactly, which is the gate.

**Both tasks.** The crossing needs Panel B, so this is MC *and* Lorenz -- the earlier
"~17 minutes" figure was costed on MC alone and is wrong by roughly 5x.

Reuses ``phase_diagram.capture.capture_cell`` unchanged, with only the sigma sweep
overridden, so the cell semantics are identical to the frozen capture.
"""

import numpy as np
import pandas as pd

from experiments.human.analysis.manifold import common as manifold_common
from experiments.human.analysis.phase_diagram import capture as pd_capture
from experiments.human.analysis.phase_diagram import common as pd_common
from experiments.human.substrates import HumanSubstrateBuilder
from experiments.human.analysis.criticality_matched import common

TASKS = ["mc", "lorenz"]
VARIANTS = ["connectome", "erdos_renyi"]     # the two the boundaries are built from
SIGN_MODE = "edge"
TARGETING = "stratified"
SR_STEP = 0.4                                 # the frozen grid's step
SR_MAX = 11.2                                 # x = 3.64 at connectome bulk95 = 0.3249
FROZEN_SR_MAX = 6.0


def sr_grid(sr_max: float = SR_MAX) -> list:
    return [round(i * SR_STEP, 6) for i in range(int(round(sr_max / SR_STEP)) + 1)]


def cost_estimate(sr_max: float = SR_MAX, seconds_per_eval=None) -> dict:
    """Recost, per task, before anything is queued.

    **Use measured whole-cell timings, not evaluator timings.** A first pass costed
    this from ``evaluate`` alone (MC 0.313 s, Lorenz 1.366 s) and came out 4.3x low,
    because ``capture_cell`` also rebuilds the reservoir at every sigma -- and
    ``build_from_adjacency`` runs a dense ``eigvals`` to rescale (~0.09 s at N=448) --
    then computes ``recurrent_spectrum``, the Gram spectrum, curvature and PR per
    sigma. The evaluator is under a quarter of the real per-sigma cost.

    Defaults below are the **measured** per-sigma cost of the actual code path
    (106 core-seconds per 29-sigma cell, averaged over the two tasks), not a component
    sum.
    """
    seconds_per_eval = seconds_per_eval or {"mc": 1.7, "lorenz": 5.5}
    n_sigma = len(sr_grid(sr_max))
    per_task_cells = (len(pd_common.F_GRID) * common.N_SEEDS * pd_common.N_DRAWS
                      * len(VARIANTS))
    total = {t: per_task_cells * n_sigma * seconds_per_eval[t] for t in TASKS}
    return {"n_sigma": n_sigma, "cells_per_task": per_task_cells,
            "core_seconds": total, "core_hours": sum(total.values()) / 3600.0,
            "evaluations": per_task_cells * n_sigma * len(TASKS)}


def run(scale: int = common.SCALE, jobs: int = 1, sr_max: float = SR_MAX) -> pd.DataFrame:
    common.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    est = cost_estimate(sr_max)
    print("=" * 70 + f"\nItem 2 -- f>0 extension to sigma = {sr_max}\n" + "=" * 70)
    print(f"  {est['evaluations']} evaluations, {est['core_hours']:.1f} core-hours "
          f"(MC {est['core_seconds']['mc']/3600:.1f} + Lorenz "
          f"{est['core_seconds']['lorenz']/3600:.1f}); ~"
          f"{est['core_hours']*3600/max(jobs,1)/60:.0f} min wall at jobs={jobs}")

    builder = HumanSubstrateBuilder(scale=scale)
    specs = manifold_common.build_specs(scale, TASKS, smoke=False, sr_max=None)
    sweep = sr_grid(sr_max)
    for spec in specs.values():
        spec["sweep"] = sweep                 # the only deviation from the frozen run
    if jobs > 1:
        for variant in VARIANTS:
            for seed in range(common.N_SEEDS):
                builder.get_mask(variant, seed)

    cells = [(task, SIGN_MODE, TARGETING, variant, f_idx, seed, draw)
             for task in TASKS for variant in VARIANTS
             for f_idx in range(len(pd_common.F_GRID))
             for seed in range(common.N_SEEDS) for draw in range(pd_common.N_DRAWS)]
    state = dict(builder=builder, specs=specs, f_grid=pd_common.F_GRID,
                 n_strata=pd_common.N_STRATA, score_mode=pd_common.SCORE_MODE)
    frame = manifold_common.run_cells(cells, pd_capture.capture_cell, state, jobs,
                                      "extend-f")
    path = common.RESULTS_DIR / f"item2_f_extension_scale_{scale}.parquet"
    frame.to_parquet(path)
    print(f"\nSaved {path}  ({len(frame)} rows)")

    print("\nGate:")
    gate = f0_gate(frame, scale)
    common.write_manifest(
        common.RESULTS_DIR / "manifest_item2.json", "E0.2 item 2 -- f>0 extension",
        scale, tasks=TASKS, variants=VARIANTS, sign_mode=SIGN_MODE,
        targeting=TARGETING, sr_grid=sr_grid(sr_max), f_grid=pd_common.F_GRID,
        n_seeds=common.N_SEEDS, n_draws=pd_common.N_DRAWS, gate=gate,
        simulates="yes -- MC + Lorenz, all f, N=%d" % scale)
    return frame


def f0_gate(frame: pd.DataFrame, scale: int = common.SCALE) -> dict:
    """``f = 0`` is the identity transform, so it must reproduce the frozen capture.

    This is the only part of the new grid that *can* be checked against the frozen
    file -- and it is the part that certifies the substrate, the reservoir build and
    the evaluators are unchanged. ``f > 0`` is a fresh realisation by construction.
    """
    frozen = pd.read_parquet(
        common.phase_cells_path(scale),
        columns=["sign_mode", "targeting", "f", "variant", "spectral_radius", "seed",
                 "draw", "task", "d_eff", "mean_curvature", "bulk95"])
    frozen = frozen[(frozen.sign_mode == SIGN_MODE) & (frozen.targeting == TARGETING)
                    & (frozen.f == 0.0) & (frozen.variant.isin(VARIANTS))]
    new = frame[frame.f == 0.0]
    keys = ["task", "variant", "seed", "draw", "_sr"]
    merged = (new.assign(_sr=new.spectral_radius.round(6))
              .merge(frozen.assign(_sr=frozen.spectral_radius.round(6)),
                     on=keys, how="inner", suffixes=("", "_ref")))
    out = {"n_cells": int(len(merged))}
    for col in ("bulk95", "mean_curvature", "d_eff"):
        if col + "_ref" not in merged:
            continue
        live = merged[merged._sr > 0] if col == "d_eff" else merged
        diff = (live[col] - live[col + "_ref"]).abs()
        rel = (diff / live[col + "_ref"].abs().clip(lower=1e-12)).max()
        out[col] = {"max_abs": float(diff.max()), "max_rel": float(rel)}
        print(f"  [f0-gate] {col:15s} max abs {diff.max():.3e}  max rel {rel:.3e}")
    if out.get("bulk95", {}).get("max_abs", 1) > 1e-9:
        raise RuntimeError("[f0-gate] f=0 does not reproduce the frozen substrate.")
    print(f"  [f0-gate] {len(merged)} f=0 cells reproduce the frozen capture.  [OK]")
    return out

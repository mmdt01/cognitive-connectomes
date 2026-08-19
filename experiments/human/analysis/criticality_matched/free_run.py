"""E2 and E1 -- the capture nothing in the repository has: the free-running rollout.

**Every state matrix in the repository is teacher-forced.** `readout_config.json` says so
in as many words for Lorenz: the persisted states are "the post-washout TEACHER-FORCED
driven states the readout is fit on, not the autonomous free-run". So Probes 1 to 3, the
phase diagram and the criticality-matched sweep have all measured the manifold the
reservoir occupies *while being shown the answer*, and none of them has looked at the
trajectory it produces when it is driving itself -- which is the regime the entire
prediction arm is about. `climate_error` scores that trajectory's statistics; no artifact
anywhere shows its shape.

Two captures, both cheap, both on the laptop:

**E2 -- closed-loop faithful geometry.** The generated Lorenz attractor at sigma = 2,
across the four-variant ladder and the eleven `f`, one draw per seed. Pre-stated claim,
written before any of this code existed (`report/act3b_prediction.md` §6.1): *the
connectome's free-run attractor retains the true Lorenz climate to a higher `f` than the
nulls do, and the collapse when it comes is a change of shape rather than a drift of
scale.*

**E1 -- the two curvature regimes made visible.** The reservoir's own state trajectory
either side of one substrate's transition, at fixed `f` and seed, so the two regimes are
the only thing that differs. Not at `f` = 0, where curvature is flat at 0.26 rad across
the whole sweep and there is nothing to draw.

---

**Two design decisions, both reductions of the inherited specification, both on stated
grounds.**

1. **E2 captures the 3-D generated trajectory, not a PCA of the free-run reservoir
   states.** The specification asked for "PCA on the time-centred free-run states". The
   generated trajectory is strictly better here: it is *exactly* the object
   `climate_error` scores, so the figure explains the scalar rather than introducing a
   rival to it; and the Lorenz x/y/z coordinates are a common basis for every substrate
   **by construction**, which removes the specification's own constraint 2 (rotation and
   sign make "connectome looks different from ER" a possible basis artifact) rather than
   managing it. It also cannot be misread as the subspace the readout computes in, which
   is constraint 1 and which would contradict F6.
2. **The metric path is reused, not reimplemented.** This module imports `lorenz.py`'s
   own `_fit_ridge_readout`, `_extract_reservoir`, `_sync_state`, `_free_run` and
   `_climate_error` and drives them in the evaluator's own order. `_verify_against_evaluate`
   asserts the recomputed `climate_error` equals `evaluate()`'s to floating point in the
   same process. **No frozen evaluator, hyperparameter or committed artifact is touched.**

---

**The long free-run is not reproducible across BLAS thread counts, and this module says
so rather than working around it.** Measured on one frozen cell (connectome, `f` = 0,
seed 0): VPT, `mean_curvature`, `sigma_eff` and `bulk95` come back **bit-exact** against
`e01_jacobian_scale_448.parquet`, while `climate_error` reads 0.0570 (frozen), 0.0721
(here, 1 thread) and 0.0289 (here, 4 threads). The climate rollout is `climate_len` =
3000 steps = **81.5 Lyapunov times**, so a difference at machine epsilon in the BLAS
reduction order is amplified by roughly e^81 and the trajectory decorrelates completely.
Consequences, all of them load-bearing:

* Every claim rests on **seed medians**, never on a cell. The faithful/collapsed
  separation is 20 to 40x on seed medians against ~2.5x per-cell scatter, so the claim
  survives comfortably -- but only stated that way.
* The capture runs in **one pass at a pinned thread count** and is never spliced onto the
  frozen capture. `THREADS` is pinned here for that reason and is recorded in the manifest.
* The integrity gate against the frozen parquet is **distributional**, not cell-for-cell.
  A cell-for-cell gate would fail for a reason that has nothing to do with correctness.

Launch: ``python -m experiments.human.analysis.criticality_matched --free-run
[--jobs N] [--smoke]``.
"""

import time
from pathlib import Path

import numpy as np
import pandas as pd

from src.reservoir import blas  # noqa: F401  (cap BLAS threads; import after numpy)
from src.reservoir.build import build_from_adjacency
from src.analysis import manifold, sign_composition
from src.analysis.spectral import recurrent_spectrum
from src.tasks import lorenz as lorenz_task
from experiments.human.substrates import HumanSubstrateBuilder
from experiments.human.analysis.manifold import common as manifold_common
from experiments.human.analysis.phase_diagram import common as pd_common
from experiments.human.analysis.criticality_matched import common

TASK = "lorenz"
# The operating point every VPT statement in TIER0 §2.6 is made at, and near every
# variant's own peak. Holding sigma fixed is what makes the f axis the only thing moving.
SIGMA = 2.0
F_GRID = pd_common.F_GRID
VARIANTS = ["connectome", "connectome_weight_permuted", "degree_rewire", "erdos_renyi"]
N_SEEDS = 10
# One draw, not three. At f = 0 the three draws of a seed are literal duplicates (the
# sign transform is the identity), and at f > 0 the seed is still the independent unit
# (TIER0 §2.3, "quote seeds, not replicates"), so a second draw buys within-seed variance
# this figure does not read.
DRAW = 0
# Pinned, and recorded in the manifest: the 3000-step climate rollout is 81.5 Lyapunov
# times and decorrelates under a different BLAS reduction order (module docstring).
THREADS = 1
# Stored at every Nth step. The climate marginals are computed on the FULL trajectory
# before thinning -- thinning is for the figure's sake, not the statistic's.
TRAJECTORY_STRIDE = 2

# --- E1 -----------------------------------------------------------------------------
# One substrate, one f, one seed, two sigma either side of its own transition, so the
# regime is the only thing that differs. NOT f = 0: curvature is flat at 0.26 rad across
# the whole sweep there and there would be nothing to draw.
E1_VARIANT = "connectome"
E1_F = 0.25
# **The cell is selected on THIS machine, from a scan, and is deliberately not read off
# the frozen panel.** TIER0 §6.4: the `f` > 0 flip pattern is not machine-portable --
# `np.argsort` breaks ties unstably on a heavily-tied edge score, so the same cell index
# selects a different flip realisation on a different machine. Measured here: connectome
# / f = 0.25 / seed 4 gives `bulk95` = 0.3804 on this laptop against the frozen capture's
# 0.3974 (ada), and its sigma = 2.8 cell is already collapsed (2.78 rad) where the frozen
# one is smooth (0.26 rad). Picking the cell from the frozen panel therefore selects a
# cell that does not exist here, which is precisely the splice §6.4 forbids.
#
# This costs the figure nothing. E1's claim is about the *phenomenon* -- curvature steps
# between two regimes in one grid step -- not about any particular realisation of it, and
# the scan asserts the straddle it finds rather than assuming one. The f = 0 probe in the
# module docstring reproduced the frozen panel bit-exactly for the opposite reason: at
# f = 0 the sign transform is the identity, so there is no flip pattern to differ.
E1_SIGMA_SCAN = [2.0, 2.4, 2.8, 3.2, 3.6, 4.0, 4.4]
E1_SEED_SCAN = 10
# Steps of state trajectory kept for the regime figure. 400 is ~4 orbits of the smooth
# cell and hundreds of periods of the collapsed one; the traces panel reads ~40 of them.
E1_STEPS = 400
E1_UNITS = 6                     # representative units for the time-trace panel

SMOKE_F_GRID = [0.0, 0.25, 0.5]
SMOKE_VARIANTS = ["connectome", "erdos_renyi"]
SMOKE_SEEDS = 2


def _cell_matrix(builder, variant, f, f_idx, seed, score_mode="degree"):
    """The signed base matrix for one cell, built exactly as the frozen captures build it.

    Same base condition, same importance score, same flip-RNG entropy and same
    `sign_fraction_matrix` call as `phase_diagram.capture.capture_cell` and
    `jacobian.capture_cell`, so a cell here is the same cell there. Verified by the
    reproduction gate in `run`, which rebuilds frozen cells and compares `bulk95`.
    """
    base = builder.weighted(pd_common.BASE_CONDITION, variant, seed)
    node_score = sign_composition.node_importance(base, mode=score_mode)
    flip_rng = np.random.default_rng([
        int(seed), int(f_idx), int(DRAW),
        pd_common.TARGETING_CODE["stratified"], pd_common.VARIANT_CODE[variant]])
    signed = sign_composition.sign_fraction_matrix(
        base, f, "stratified", flip_rng, n_strata=pd_common.N_STRATA,
        node_score=node_score)
    return signed, float(recurrent_spectrum(signed)["bulk95_radius"])


def _protocol(reservoir, seed, params):
    """Run the evaluator's own closed-loop protocol and keep the trajectory it throws away.

    This is `lorenz._measure` with two changes and no others: the long free-run and the
    true reference are returned rather than reduced to a scalar, and the 20 VPT windows
    are skipped (this capture reads climate, and the VPT axis is already frozen in
    `e03_frontier_scale_448.parquet`). The order of operations, the ridge solve, the
    z-scoring and the synchronisation are `lorenz.py`'s own functions.
    """
    p = params
    series, holdout_start, _, _ = lorenz_task.build_trajectory(
        seed, p["n_transient"], p["washout"], p["n_train"], p["sync_len"],
        p["n_windows"], p["window_spacing"], p["free_run_len"], p["sigma"], p["rho"],
        p["beta"], p["h"], p["x0"])
    train = series[p["n_transient"]:holdout_start]
    lorenz_task._reset(reservoir)
    driven = reservoir.run(train)[p["washout"]:]
    target = series[p["n_transient"] + p["washout"] + 1: holdout_start + 1]
    weights = lorenz_task._fit_ridge_readout(driven, target, p["ridge_alpha"],
                                             p["readout_bias"])
    W, Win, leak, bias = lorenz_task._extract_reservoir(reservoir)

    start = lorenz_task._sync_state(reservoir, series[holdout_start - p["sync_len"]:
                                                     holdout_start])
    generated = lorenz_task._free_run(start, weights, p["readout_bias"], W, Win, leak,
                                      bias, p["climate_len"])
    settled = generated[p["climate_washout"]:]
    reference = series[p["n_transient"]:]
    climate = lorenz_task._climate_error(settled, reference)
    return dict(generated=settled, reference=reference, driven=driven, climate=climate)


def _verify_against_evaluate(reservoir, seed, params) -> None:
    """Assert the reused protocol returns the evaluator's own `climate_error`.

    The point of reusing `lorenz.py`'s functions rather than reimplementing them is that
    this equality is exact in-process; if it ever stops being exact, the capture is
    measuring something the thesis does not report and must fail rather than publish.
    """
    ours = _protocol(reservoir, seed, params)["climate"]
    lorenz_task._reset(reservoir)
    theirs = reservoir  # rebuilt by the caller; evaluate() resets internally
    reference = lorenz_task.evaluate(theirs, seed=seed, **params)["climate_error"]
    assert np.isclose(ours, reference, rtol=1e-12, atol=0.0), (
        f"free_run: the reused protocol gives climate_error {ours!r} against "
        f"evaluate()'s {reference!r}. The capture is not on the evaluator's path.")


def capture_cell(cell, state) -> list:
    """One (variant, f_idx, seed) cell at the fixed operating point."""
    variant, f_idx, seed = cell
    builder, params = state["builder"], state["params"]
    spec, f = state["spec"], state["f_grid"][f_idx]
    signed, bulk95 = _cell_matrix(builder, variant, f, f_idx, seed)
    reservoir = build_from_adjacency(
        weighted_adjacency=signed, target_spectral_radius=SIGMA,
        leak_rate=spec["leak_rate"], input_scaling=spec["input_scaling"],
        seed=seed, input_dim=spec["input_dim"])
    out = _protocol(reservoir, seed + spec["input_seed_offset"], params)
    generated, reference = out["generated"], out["reference"]
    finite = bool(np.all(np.isfinite(generated)))
    thin = generated[::TRAJECTORY_STRIDE]
    return [dict(
        variant=variant, f=float(f), spectral_radius=SIGMA, seed=int(seed), draw=DRAW,
        task=TASK, bulk95=bulk95, climate_error=float(out["climate"]),
        diverged=not finite,
        # The scale/shape distinction the pre-stated claim turns on: a run that keeps the
        # attractor's spread but not its shape moves `sd_ratio` little and `climate_error`
        # a lot, and the caption has to be able to tell those apart.
        sd_ratio=float(np.mean(np.std(thin, axis=0) / np.std(reference, axis=0)))
        if finite else np.nan,
        mean_curvature_driven=float(manifold.mean_curvature(out["driven"])),
        trajectory=thin.astype(np.float32).ravel() if finite else np.zeros(0, np.float32),
        n_steps=int(thin.shape[0]) if finite else 0,
    )]


def _scan_for_e1_cell(builder, spec, params):
    """Find a seed whose curvature steps across the separator in ONE grid step, here.

    Returns ``(seed, sigma_smooth, sigma_collapsed, scan_frame)``. Cheap -- it reads
    `mean_curvature` off the driven states, which is the same quantity F12 plots, and it
    stops at the first seed that straddles, so the usual cost is a few cells rather than
    the whole scan.
    """
    f_idx = pd_common.F_GRID.index(E1_F)
    rows, chosen = [], None
    for seed in range(E1_SEED_SCAN):
        signed, _ = _cell_matrix(builder, E1_VARIANT, E1_F, f_idx, seed)
        curvature = {}
        for sigma in E1_SIGMA_SCAN:
            reservoir = build_from_adjacency(
                weighted_adjacency=signed, target_spectral_radius=sigma,
                leak_rate=spec["leak_rate"], input_scaling=spec["input_scaling"],
                seed=seed, input_dim=spec["input_dim"])
            out = spec["evaluate"](reservoir, seed=seed + spec["input_seed_offset"],
                                   collect_states=True, **params)
            value = float(manifold.mean_curvature(np.asarray(out["states"], float)))
            curvature[sigma] = value
            rows.append(dict(seed=seed, spectral_radius=sigma, mean_curvature=value))
        for lo, hi in zip(E1_SIGMA_SCAN, E1_SIGMA_SCAN[1:]):
            if curvature[lo] < 1.0 < curvature[hi]:
                chosen = (seed, lo, hi)
                break
        if chosen:
            print(f"  E1 cell: seed {chosen[0]}, sigma {chosen[1]:g} -> {chosen[2]:g}  "
                  f"(curvature {curvature[chosen[1]]:.3f} -> {curvature[chosen[2]]:.3f} rad)")
            break
    assert chosen is not None, (
        "free_run: no seed steps across CURV_COLLAPSE = 1.0 within one grid step of the "
        f"scan {E1_SIGMA_SCAN} at f = {E1_F}. Widen the scan.")
    return (*chosen, pd.DataFrame(rows))


def capture_e1(builder, spec, params) -> tuple:
    """The two curvature regimes: one substrate, one f, one seed, two sigma.

    Same cell on both rows apart from sigma, so nothing but the regime differs -- which
    is what lets the figure be captioned as a regime rather than as a substrate contrast.
    The state trajectory is kept, not a projection of it: the projection is the figure's
    choice and belongs in the builder, not in the capture.
    """
    seed, sigma_smooth, sigma_collapsed, scan = _scan_for_e1_cell(builder, spec, params)
    f_idx = pd_common.F_GRID.index(E1_F)
    signed, bulk95 = _cell_matrix(builder, E1_VARIANT, E1_F, f_idx, seed)
    rows = []
    for regime, sigma in (("smooth", sigma_smooth), ("collapsed", sigma_collapsed)):
        reservoir = build_from_adjacency(
            weighted_adjacency=signed, target_spectral_radius=sigma,
            leak_rate=spec["leak_rate"], input_scaling=spec["input_scaling"],
            seed=seed, input_dim=spec["input_dim"])
        out = spec["evaluate"](reservoir, seed=seed + spec["input_seed_offset"],
                               collect_states=True, **params)
        states = np.asarray(out["states"], dtype=float)
        # Read the same window every time, well past the washout, so the two rows are
        # the same stretch of the driven series and not two arbitrary excerpts.
        window = states[1000:1000 + E1_STEPS]
        # Per-step turning angles -- the quantity `mean_curvature` averages. Keeping the
        # distribution is the whole point: the mean is what F12 shows, and E1 exists to
        # show that the mean is a mean over a concentrated, not a spread, distribution.
        velocity = np.diff(window, axis=0)
        speed = np.linalg.norm(velocity, axis=1)
        cosine = np.clip(np.sum(velocity[:-1] * velocity[1:], axis=1)
                         / (speed[:-1] * speed[1:]), -1.0, 1.0)
        angles = np.arccos(cosine)
        # The six units with the largest swing in this window: the ones whose traces
        # actually show the period-2 alternation rather than sitting near zero.
        loudest = np.argsort(window.std(axis=0))[-E1_UNITS:][::-1]
        rows.append(dict(
            regime=regime, variant=E1_VARIANT, f=E1_F, seed=int(seed),
            spectral_radius=float(sigma), bulk95=bulk95,
            mean_curvature=float(manifold.mean_curvature(states)),
            vpt=float(out["vpt"]), climate_error=float(out["climate_error"]),
            n_steps=int(window.shape[0]), n_units=int(E1_UNITS),
            turning_angles=angles.astype(np.float32),
            unit_traces=window[:, loudest].astype(np.float32).ravel(),
            unit_index=loudest.astype(np.int32),
        ))
    return pd.DataFrame(rows), scan


def run(scale: int = 448, jobs: int = 1, smoke: bool = False) -> None:
    """Capture E2's free-run attractors and E1's two regimes, then gate both."""
    from threadpoolctl import threadpool_limits

    results_dir = Path(common.RESULTS_DIR)
    results_dir.mkdir(parents=True, exist_ok=True)
    builder = HumanSubstrateBuilder(scale=scale)
    spec = manifold_common.build_specs(scale, [TASK], False, None)[TASK]
    params = dict(spec["params"])

    f_grid = SMOKE_F_GRID if smoke else F_GRID
    variants = SMOKE_VARIANTS if smoke else VARIANTS
    n_seeds = SMOKE_SEEDS if smoke else N_SEEDS
    cells = [(v, f_grid.index(f), s)
             for v in variants for f in f_grid for s in range(n_seeds)]

    print(f"E2 free-run capture: {len(cells)} cells "
          f"({len(variants)} variants x {len(f_grid)} f x {n_seeds} seeds) at "
          f"sigma = {SIGMA:g}, {THREADS} BLAS thread(s).")
    state = dict(builder=builder, spec=spec, params=params, f_grid=f_grid)

    with threadpool_limits(limits=THREADS):
        # The gate that licenses reusing lorenz.py's internals rather than the evaluator.
        probe_matrix, _ = _cell_matrix(builder, variants[0], 0.0, 0, 0)
        probe = build_from_adjacency(
            weighted_adjacency=probe_matrix, target_spectral_radius=SIGMA,
            leak_rate=spec["leak_rate"], input_scaling=spec["input_scaling"],
            seed=0, input_dim=spec["input_dim"])
        _verify_against_evaluate(probe, 0 + spec["input_seed_offset"], params)
        print("  gate: reused protocol reproduces evaluate()'s climate_error exactly.")

        started = time.time()
        frame = manifold_common.run_cells(cells, capture_cell, state, jobs,
                                          "E2 free-run capture")
        e1, e1_scan = capture_e1(builder, spec, params)
    elapsed = time.time() - started

    suffix = "_smoke" if smoke else ""
    e2_path = results_dir / f"e2_free_run_scale_{scale}{suffix}.parquet"
    e1_path = results_dir / f"e1_curvature_regimes_scale_{scale}{suffix}.parquet"
    frame.to_parquet(e2_path, index=False)
    e1.to_parquet(e1_path, index=False)
    e1_scan.to_parquet(results_dir / f"e1_curvature_scan_scale_{scale}{suffix}.parquet",
                       index=False)
    print(f"Saved {e2_path}  ({len(frame)} rows)")
    print(f"Saved {e1_path}  ({len(e1)} rows)")

    _gate(frame, e1, scale, smoke)
    common.write_manifest(
        results_dir / f"manifest_free_run_scale_{scale}{suffix}.json",
        "E2 free-run attractors + E1 curvature regimes", scale,
        sigma=SIGMA, f_grid=list(f_grid), variants=list(variants), n_seeds=n_seeds,
        draw=DRAW, blas_threads=THREADS, trajectory_stride=TRAJECTORY_STRIDE,
        climate_len=params["climate_len"], climate_washout=params["climate_washout"],
        ridge_alpha=params["ridge_alpha"], seconds=round(elapsed, 1),
        note=("climate_error is chaotic in the BLAS reduction order over the 81.5 "
              "Lyapunov times of the climate rollout; the gate against the frozen "
              "capture is distributional, never cell-for-cell."))


def _gate(frame: pd.DataFrame, e1: pd.DataFrame, scale: int, smoke: bool) -> None:
    """Integrity gate. Distributional against the frozen capture, for the reason above."""
    print("\nIntegrity gate")
    assert frame.climate_error.notna().all(), "free_run: NaN climate_error"
    assert frame.groupby(["variant", "f"]).seed.nunique().eq(
        frame.seed.nunique()).all(), "free_run: a (variant, f) cell is missing seeds"
    print(f"  cells {len(frame)}, seeds {frame.seed.nunique()}, "
          f"diverged {int(frame.diverged.sum())}")

    frozen = Path(common.RESULTS_DIR) / f"e01_jacobian_scale_{scale}.parquet"
    if frozen.exists() and not smoke:
        reference = pd.read_parquet(frozen, columns=[
            "variant", "f", "spectral_radius", "draw", "climate_error"])
        reference = reference[(reference.spectral_radius == SIGMA)
                              & (reference.draw == DRAW)]
        joined = (frame.groupby(["variant", "f"]).climate_error.median().rename("fresh")
                  .to_frame().join(
                      reference.groupby(["variant", "f"]).climate_error.median()
                      .rename("frozen")))
        # Faithful (<0.5) vs collapsed (>2) is a 20-40x separation; the per-cell scatter
        # from BLAS-order chaos is ~2.5x. So the gate is on which SIDE of the separation
        # each cell falls, which is the only thing any claim rests on.
        agree = ((joined.fresh < 0.5) == (joined.frozen < 0.5))
        print(f"  frozen agreement on faithful-vs-collapsed: "
              f"{int(agree.sum())}/{len(joined)} (variant, f) cells")
        assert agree.mean() >= 0.75, (
            "free_run: the fresh capture disagrees with the frozen one on which side of "
            "the faithful/collapsed separation cells fall, in more than a quarter of "
            f"them:\n{joined[~agree]}")

    # E2's pre-stated claim, checked here so the result is on the record independently of
    # whether the figure is drawn: the connectome holds a faithful climate to higher f.
    faithful = frame.assign(ok=frame.climate_error < 0.5).groupby(
        ["variant", "f"]).ok.mean().unstack(0)
    if "connectome" in faithful and len(faithful.columns) > 1:
        high_f = faithful[faithful.index >= 0.30]
        nulls = [c for c in faithful.columns if c != "connectome"]
        print(f"  fraction of seeds keeping a faithful climate at f >= 0.30: "
              f"connectome {high_f['connectome'].mean():.2f}, "
              f"nulls {high_f[nulls].mean().mean():.2f}")

    print("  E1 regimes:")
    for row in e1.itertuples():
        print(f"    {row.regime:<10} sigma {row.spectral_radius:>4.1f}  "
              f"curvature {row.mean_curvature:.3f} rad  vpt {row.vpt:.2f}  "
              f"climate {row.climate_error:.3f}")
    assert e1.mean_curvature.min() < 1.0 < e1.mean_curvature.max(), (
        "free_run: E1's two cells must straddle CURV_COLLAPSE = 1.0, one smooth and one "
        f"collapsed; got {list(e1.mean_curvature.round(3))}. Pick different sigma.")
    # NOT compared cell-for-cell against the frozen panel: TIER0 §6.4 says the f > 0
    # flip pattern is not machine-portable, and this capture is on a different machine
    # from the one that froze `e01_jacobian`. The straddle assertion above is the gate,
    # and it is a statement about the phenomenon rather than about one realisation.

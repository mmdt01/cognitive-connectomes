"""Spectra extraction behind the Probe 1 to 3 summary metrics (follow-up, not a new probe).

The participation ratio does not track the null-ladder ordering (in the non-negative
empirical column at supercritical sr, MC runs 3.95 -> 13.23 while PR spans only
1.185 -> 1.398 and its order does not match), so PR -- a variance-weighted measure --
misses memory that lives in low-variance directions. This driver dumps the raw
spectra the summary metrics compress, so a better dimensionality measure can be
tested offline. It touches no frozen hyperparameter, figure, or run-matrix cell;
it reuses the SAME opt-in ``collect_states`` capture Probe 1 validated bit-for-bit
against the committed runs (there is no on-disk state cache to reuse, so states are
regenerated through that validated path).

Four additive outputs to ``experiments/human/analysis/results/scale_<N>/``:

1. ``readout_config.json`` -- exactly how each task's ridge design matrix is built
   (read from source), so the effective-rank calculation is unambiguous.
2. ``covariance_spectra.parquet`` -- full covariance spectrum ``eig_cov`` (continuity
   with Probes 1/2) and design-Gram spectrum ``eig_gram`` (the ridge sees), on a
   reduced 13-point sr grid, all other factors at full resolution.
3. ``w_spectra.parquet`` -- normalised base-matrix spectra (one row per
   condition/variant/seed): eigenvalues, near-degeneracy counts, leading-eigenvector
   IPRs, per the several-near-degenerate-pools memory hypothesis.
4. ``saturation_diagnostics.parquet`` -- scalar tanh-gain / saturation / common-mode
   diagnostics on the FULL 58-point sweep, joinable to ``manifold_metrics.parquet``.

Launched via ``python -m experiments.human.analysis.manifold --spectra [--scale N]
[--jobs N] [--smoke]``.
"""

import json

import numpy as np
import pandas as pd

from src.reservoir.build import build_from_adjacency
from src.analysis import manifold
from src.analysis.spectral import recurrent_spectrum
from experiments.human.substrates import HumanSubstrateBuilder
from experiments.human import matrix_config
from experiments.human.analysis.manifold import common

# The reduced spectral-radius grid for the full covariance/Gram spectra (Output 2).
# All 13 values are exact grid points of the committed 58-point [0, 6] sweep.
REDUCED_SR = [0.0, 0.4211, 0.8421, 1.0526, 1.2632, 1.5789, 2.0, 2.5263, 3.0526,
              3.5789, 4.1053, 5.1579, 6.0]

# How each task's ridge design matrix is built (documented in readout_config.json,
# and the single source of truth for design_matrix() below). Numeric params
# (alpha, warmup/washout, n_train) are pulled live from each task_config so the
# doc can never drift from what the capture actually computes.
_READOUT_DESIGN = {
    "mc": dict(
        bias_column=False, input_concatenated=False,
        states_centred=False, states_scaled=False,
        solver=("per lag k=1..max_lag: numpy.linalg.solve(gram + alpha*I_N, "
                "X_k.T @ y_k), X_k = states[k:], gram = X_k.T @ X_k rank-1 "
                "down-dated across lags"),
        notes=("No bias/intercept, no input concatenation, raw (un-centred, "
               "un-scaled) states; ridge identity alpha*I over all N columns. The "
               "design is per-lag and NESTED (X_k drops the first k rows of the "
               "post-warmup states); eig_gram is reported for the full post-warmup "
               "matrix (k=0), representative of all lags to within k/T_eff rows. "
               "eig_cov uses the same full post-warmup matrix, time-centred."),
    ),
    "narma10": dict(
        bias_column=True, input_concatenated=False,
        states_centred=False, states_scaled=False,
        solver=("numpy.linalg.solve(design.T @ design + reg, design.T @ y); "
                "design = [train_states, 1]; reg = alpha*I with reg[-1,-1]=0 "
                "(intercept unregularised)"),
        notes=("Readout is fit on the TRAIN split only (first n_train of the "
               "post-washout states) plus an unregularised bias column, so "
               "eig_gram is on n_train rows x (N+1) cols. eig_cov keeps Probe 1 "
               "continuity: it is the FULL post-washout span (T-washout rows, no "
               "bias), time-centred."),
    ),
    "lorenz": dict(
        bias_column=True, input_concatenated=False,
        states_centred=False, states_scaled=False,
        solver=("numpy.linalg.solve(design.T @ design + reg, design.T @ Y); "
                "design = [states, 1]; Y = z-scored next-state (3-D); reg = alpha*I "
                "with reg[-1,-1]=0 (intercept unregularised)"),
        notes=("States are the post-washout TEACHER-FORCED driven states the readout "
               "is fit on (n_train rows), not the autonomous free-run. The Lorenz "
               "TRAJECTORY (input and target) is z-scored on the teacher-forced "
               "region; the reservoir STATES themselves are not centred or scaled "
               "before the solve. eig_gram is on n_train rows x (N+1) cols; eig_cov "
               "on the same n_train states, time-centred."),
    ),
}


# ---------------------------------------------------------------------------
# Design matrix (single source of truth with readout_config.json)
# ---------------------------------------------------------------------------
def design_matrix(task_name: str, states: np.ndarray, params: dict) -> np.ndarray:
    """The ridge design matrix ``A`` exactly as the task's solver forms it.

    ``states`` is the captured post-warmup driven-state matrix (``out["states"]``).
    Mirrors ``_READOUT_DESIGN``: MC uses the raw states (no bias, per-lag nested,
    represented at k=0); NARMA/Lorenz append an unregularised bias column, NARMA on
    the train split only.
    """
    x = np.asarray(states, dtype=float)
    if task_name == "mc":
        return x
    if task_name == "narma10":
        train = x[: params["n_train"]]
        return np.hstack([train, np.ones((train.shape[0], 1))]) if params.get(
            "readout_bias", True) else train
    if task_name == "lorenz":
        return np.hstack([x, np.ones((x.shape[0], 1))]) if params.get(
            "readout_bias", True) else x
    raise ValueError(f"unknown task {task_name!r}")


def _in_reduced_grid(sr: float, tol: float = 1e-3) -> bool:
    return any(abs(sr - r) < tol for r in REDUCED_SR)


# ---------------------------------------------------------------------------
# Output 3: recurrent (W) spectra -- one row per (condition, variant, seed)
# ---------------------------------------------------------------------------
def w_spectra_cell(cell, state) -> list:
    """Normalised base-matrix spectrum for one (condition, variant, seed)."""
    condition, variant, seed = cell
    builder = state["builder"]
    rs = recurrent_spectrum(builder.weighted(condition, variant, seed))
    rung = matrix_config.VARIANT_RUNG.get(variant, -1)
    return [dict(
        condition=condition, variant=variant, rung=rung, seed=seed,
        eig_w_real=rs["eig_real"], eig_w_imag=rs["eig_imag"],
        is_symmetric=bool(rs["is_symmetric"]), perron_root=rs["perron_root"],
        base_spectral_radius=rs["base_spectral_radius"],
        bulk95_radius=rs["bulk95_radius"], spectral_gap=rs["spectral_gap"],
        n_near_degenerate_10pct=rs["n_near_degenerate_10pct"],
        n_near_degenerate_25pct=rs["n_near_degenerate_25pct"],
        top10_eigvec_ipr=rs["top10_eigvec_ipr"],
    )]


def capture_w_spectra(builder, conditions, variants, n_seeds, jobs) -> pd.DataFrame:
    cells = [(c, v, s) for c in conditions for v in variants for s in range(n_seeds)]
    return common.run_cells(cells, w_spectra_cell, {"builder": builder}, jobs, "w-spectra")


# ---------------------------------------------------------------------------
# Outputs 2 + 4: one capture pass over the full sweep
# ---------------------------------------------------------------------------
def capture_cell(cell, state) -> list:
    """Rebuild the reservoir per sr (bit-identical to the runner), capture its driven
    states, and emit a ``sat`` row (Output 4, every sr) plus a ``cov`` row (Output 2,
    reduced grid only). Rows are tagged by ``kind`` and split by the caller."""
    task_name, condition, variant, seed = cell
    builder, spec = state["builder"], state["specs"][task_name]
    bulk95 = state["bulk95"][(condition, variant, seed)]
    treat_all = state["treat_all_reduced"]
    params, alpha = spec["params"], spec["params"]["ridge_alpha"]
    rung = matrix_config.VARIANT_RUNG.get(variant, -1)
    weighted = builder.weighted(condition, variant, seed)
    rows = []
    for spectral_radius in spec["sweep"]:
        reservoir = build_from_adjacency(
            weighted_adjacency=weighted, target_spectral_radius=spectral_radius,
            leak_rate=spec["leak_rate"], input_scaling=spec["input_scaling"],
            seed=seed, input_dim=spec["input_dim"],
        )
        out = spec["evaluate"](reservoir, seed=seed + spec["input_seed_offset"],
                               collect_states=True, **params)
        x = np.asarray(out["states"], dtype=float)
        base = dict(task=task_name, condition=condition, variant=variant, rung=rung,
                    spectral_radius=spectral_radius, seed=seed)

        # Output 4: saturation / gain diagnostics (every sr).
        gain = 1.0 - x * x                       # tanh derivative (leak=1 -> x=tanh)
        mean_gain = float(gain.mean())
        rows.append(dict(
            base, kind="sat", mean_gain=mean_gain, median_gain=float(np.median(gain)),
            frac_saturated=float((np.abs(x) > 0.99).mean()),
            mean_abs_x=float(np.abs(x).mean()), mean_state=float(x.mean()),
            effective_radius=float(bulk95 * spectral_radius * mean_gain),
        ))

        # Output 2: full covariance + design-Gram spectra (reduced grid only).
        if treat_all or _in_reduced_grid(spectral_radius):
            eig_cov, total_variance = manifold.covariance_spectrum(x)
            A = design_matrix(task_name, x, params)
            eig_gram = manifold.gram_spectrum(A)
            rows.append(dict(
                base, kind="cov",
                eig_cov=eig_cov.astype(np.float32),
                eig_gram=eig_gram.astype(np.float32),
                n_design_cols=int(A.shape[1]), total_variance=float(total_variance),
                T_effective=int(A.shape[0]), alpha=float(alpha),
            ))
    return rows


def capture(builder, specs, conditions, variants, n_seeds, bulk95, treat_all, jobs):
    cells = [(t, c, v, s) for t in specs for c in conditions for v in variants
             for s in range(n_seeds)]
    state = dict(builder=builder, specs=specs, bulk95=bulk95,
                 treat_all_reduced=treat_all)
    return common.run_cells(cells, capture_cell, state, jobs, "capture")


_SAT_COLS = ["task", "condition", "variant", "rung", "spectral_radius", "seed",
             "mean_gain", "median_gain", "frac_saturated", "mean_abs_x",
             "mean_state", "effective_radius"]
_COV_COLS = ["task", "condition", "variant", "rung", "spectral_radius", "seed",
             "eig_cov", "eig_gram", "n_design_cols", "total_variance",
             "T_effective", "alpha"]


# ---------------------------------------------------------------------------
# Output 1: readout_config.json
# ---------------------------------------------------------------------------
def build_readout_config(specs: dict, n_nodes: int) -> dict:
    """Per-task readout-design record, numbers pulled live from the task params."""
    tasks = {}
    for name, spec in specs.items():
        p = spec["params"]
        design = _READOUT_DESIGN[name]
        if name == "mc":
            captured_rows = p["T"] - p["warmup"]
            design_rows = captured_rows            # k=0 representative (per-lag: -k)
        elif name == "narma10":
            captured_rows = p["T"] - p["washout"]
            design_rows = p["n_train"]
        elif name == "lorenz":
            captured_rows = p["n_train"]
            design_rows = p["n_train"]
        else:
            raise ValueError(name)
        extra_cols = 1 if design["bias_column"] else 0
        tasks[name] = dict(
            alpha=float(p["ridge_alpha"]),
            T_effective=int(design_rows),
            captured_state_rows=int(captured_rows),
            n_design_cols=int(n_nodes + extra_cols),
            n_reservoir_nodes=int(n_nodes),
            **design,
        )
    return dict(
        description=("How each task's ridge readout design matrix is built, read from "
                     "src/tasks/{memory_capacity,narma,lorenz}.py and the human "
                     "experiments/human/*/task_config.py. Determines the correct "
                     "effective-rank calculation on eig_gram: rank = "
                     "sum_i g_i / (g_i + alpha)."),
        leak_rate_note=("All three tasks use leak_rate=1.0, so the reservoir state "
                        "x == tanh(pre-activation) exactly and (1 - x^2) is the tanh "
                        "derivative used in saturation_diagnostics.parquet."),
        eig_cov_note=("eig_cov (covariance_spectra.parquet) is on the FULL captured "
                      "post-warmup states (captured_state_rows), time-centred -- "
                      "continuity with Probes 1/2. eig_gram is on the design matrix "
                      "(T_effective rows x n_design_cols), un-centred, as the ridge "
                      "solver sees it. These differ for NARMA (2800 captured vs 2000 "
                      "design)."),
        tasks=tasks,
    )


def _write_readout_config(specs, n_nodes, path) -> dict:
    config = build_readout_config(specs, n_nodes)
    path.write_text(json.dumps(config, indent=2) + "\n")
    print(f"Saved {path}")
    return config


def _write_w_spectra_note(path, n_nodes) -> None:
    note = f"""# w_spectra.parquet -- accompanying note

Normalised base-matrix (W) spectra, one row per (condition, variant, rung, seed)
= 210 rows for the human N={n_nodes} substrate. W does not depend on task, and the
spectral-radius sweep only rescales it.

## Scaling rule (base matrix -> W(sr))

The reservoir build (src/reservoir/build.py :: rescale_spectral_radius) rescales the
base weighted matrix `W_base = builder.weighted(condition, variant, seed)` to a target
nominal spectral radius:

    l1   = max(|eigvals(W_base)|)          # dense np.linalg.eigvals
    W(sr) = W_base * (sr / l1)

So the eigenvalues of W(sr) are exactly `sr` times the eigenvalues of the NORMALISED
base matrix `W_base / l1` (spectral radius 1). This file exports the spectrum of that
normalised base matrix; multiply eig_w_real / eig_w_imag by any sr to recover W(sr).

`base_spectral_radius` records the divided-out l1 (= |lambda_1| of W_base).

## Columns

- eig_w_real, eig_w_imag : length-N eigenvalues of the normalised base matrix,
  sorted by DESCENDING modulus. Human W is symmetric, so eig_w_imag ~ 0 and
  is_symmetric is True (eigh path; the general eig path is kept for directed W).
- is_symmetric           : W symmetric within 1e-9.
- perron_root            : largest real-part eigenvalue (Perron-Frobenius root for a
                           non-negative W; == 1 there, so it marks whether the top
                           mode is the real positive Perron mode).
- bulk95_radius          : pct95(|lambda|) / |lambda_1| -- identical formula to the
                           spectral tier's bulk95_ratio (here |lambda_1| == 1).
- spectral_gap           : |lambda_1| - |lambda_2| (normalised: 1 - |lambda_2|).
- n_near_degenerate_10pct / _25pct : count of |lambda_i| within 10% / 25% of
                           |lambda_1| (>= 0.9 / 0.75; includes the top mode).
- top10_eigvec_ipr       : IPR = sum_i |v_i|^4 / (sum_i |v_i|^2)^2 of the leading 10
                           eigenvectors -- high = localised on few nodes (tests the
                           near-degenerate-pool memory hypothesis).
"""
    path.write_text(note)
    print(f"Saved {path}")


# ---------------------------------------------------------------------------
# Sanity check: eig_cov reproduces the published Probe 1 PR
# ---------------------------------------------------------------------------
def _sanity_check_pr(cov_df, results_dir, n_rows: int = 8) -> None:
    """Flag (do not correct) any row where PR recomputed from eig_cov disagrees with
    the committed manifold_metrics.parquet PR beyond floating-point tolerance."""
    metrics_path = results_dir / "manifold_metrics.parquet"
    if not metrics_path.exists():
        print(f"  [sanity] {metrics_path} absent -- skipping PR cross-check.")
        return
    metrics = pd.read_parquet(metrics_path)
    metrics["_sr"] = metrics.spectral_radius.round(6)
    keys = ["task", "condition", "variant", "seed"]
    sample = cov_df.sample(min(n_rows, len(cov_df)), random_state=0)
    print(f"\n  [sanity] PR from eig_cov vs committed manifold_metrics PR "
          f"({len(sample)} rows):")
    worst = 0.0
    for _, row in sample.iterrows():
        eig = np.asarray(row["eig_cov"], dtype=float)
        pr = float(eig.sum() ** 2 / (eig ** 2).sum())
        m = metrics[(metrics.task == row.task) & (metrics.condition == row.condition)
                    & (metrics.variant == row.variant) & (metrics.seed == row.seed)
                    & (metrics._sr == round(float(row.spectral_radius), 6))]
        if m.empty:
            print(f"    {row.task}/{row.condition}/{row.variant} sr={row.spectral_radius}"
                  f" seed={row.seed}: no committed row")
            continue
        pr_ref = float(m.iloc[0]["pr"])
        rel = abs(pr - pr_ref) / max(abs(pr_ref), 1e-12)
        worst = max(worst, rel)
        flag = "" if rel < 1e-5 else "   !! DISCREPANCY"
        print(f"    {row.task:7s}/{row.condition:22s}/{row.variant:26s} "
              f"sr={row.spectral_radius:<7g} seed={row.seed}: "
              f"PR={pr:.6f} ref={pr_ref:.6f} rel={rel:.1e}{flag}")
    print(f"  [sanity] worst relative PR difference: {worst:.2e} "
          f"({'OK' if worst < 1e-5 else 'INVESTIGATE'})")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def run(smoke: bool = False, jobs: int = 1, scale: int | None = None) -> None:
    scale = matrix_config.SCALE if scale is None else scale
    tasks = common.DEFAULT_TASKS
    results_dir, _ = common.scale_dirs(scale)
    results_dir.mkdir(parents=True, exist_ok=True)

    builder = HumanSubstrateBuilder(scale=scale)
    n_nodes = int(builder.mask.shape[0])
    print("Substrate summary:")
    for key, value in builder.summary().items():
        print(f"  {key}: {value}")

    specs = common.build_specs(scale, tasks, smoke, sr_max=None)
    conditions = matrix_config.CONDITIONS
    variants = (["connectome", "degree_rewire"] if smoke else matrix_config.VARIANTS)
    n_seeds = 2 if smoke else matrix_config.N_SEEDS

    # Output 1: readout config (documentation; single source of truth for the numbers).
    config = _write_readout_config(specs, n_nodes, results_dir / "readout_config.json")

    # Output 3: W spectra (also gives bulk95 per (condition, variant, seed) for
    # effective_radius in Output 4).
    print(f"\n[Output 3] W spectra: {len(conditions)}x{len(variants)}x{n_seeds} "
          f"= {len(conditions) * len(variants) * n_seeds} rows")
    w_df = capture_w_spectra(builder, conditions, variants, n_seeds, jobs)
    bulk95 = {(r.condition, r.variant, r.seed): float(r.bulk95_radius)
              for r in w_df.itertuples()}
    _write_w_spectra_note(results_dir / "w_spectra_note.md", n_nodes)
    if not smoke:
        w_df.to_parquet(results_dir / "w_spectra.parquet")
        print(f"Saved {results_dir / 'w_spectra.parquet'}  ({len(w_df)} rows)")

    # Outputs 2 + 4: one capture pass over the full sweep.
    sweep = specs[tasks[0]]["sweep"]
    n_cells = len(tasks) * len(conditions) * len(variants) * n_seeds
    print(f"\n[Outputs 2+4] capture: tasks={list(specs)} scale={scale} "
          f"variants={len(variants)} seeds={n_seeds} sweep={len(sweep)}pts "
          f"cells={n_cells} jobs={jobs}")
    print(f"  reduced sr grid (Output 2): "
          f"{'ALL captured (smoke)' if smoke else REDUCED_SR}")
    df = capture(builder, specs, conditions, variants, n_seeds, bulk95,
                 treat_all=smoke, jobs=jobs)

    sat_df = df[df.kind == "sat"][_SAT_COLS].reset_index(drop=True)
    cov_df = df[df.kind == "cov"][_COV_COLS].reset_index(drop=True)

    # Guard: the documented readout config must match what the capture computed.
    for name in tasks:
        c = cov_df[cov_df.task == name]
        if c.empty:
            continue
        assert (c.n_design_cols == config["tasks"][name]["n_design_cols"]).all(), (
            f"{name}: n_design_cols in parquet != readout_config")
        assert (c.T_effective == config["tasks"][name]["T_effective"]).all(), (
            f"{name}: T_effective in parquet != readout_config")
        assert np.allclose(c.alpha, config["tasks"][name]["alpha"]), (
            f"{name}: alpha in parquet != readout_config")
    print("  [guard] readout_config matches captured n_design_cols / T_effective / alpha.")

    print(f"\nOutput 4 saturation ranges:")
    for task in tasks:
        s = sat_df[sat_df.task == task]
        print(f"  {task:7s}: mean_gain [{s.mean_gain.min():.3f}, {s.mean_gain.max():.3f}]  "
              f"frac_sat [{s.frac_saturated.min():.3f}, {s.frac_saturated.max():.3f}]  "
              f"eff_radius [{s.effective_radius.min():.2f}, {s.effective_radius.max():.2f}]  "
              f"mean_state [{s.mean_state.min():+.3f}, {s.mean_state.max():+.3f}]")

    if not smoke:
        cov_df.to_parquet(results_dir / "covariance_spectra.parquet")
        print(f"\nSaved {results_dir / 'covariance_spectra.parquet'}  ({len(cov_df)} rows)")
        sat_df.to_parquet(results_dir / "saturation_diagnostics.parquet")
        print(f"Saved {results_dir / 'saturation_diagnostics.parquet'}  ({len(sat_df)} rows)")

    _sanity_check_pr(cov_df, results_dir)
    print("\nSpectra extraction complete.")

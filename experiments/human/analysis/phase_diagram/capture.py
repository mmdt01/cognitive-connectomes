"""Phase-diagram capture: graded sign transform x spectral-radius sweep.

For every (task, targeting, variant, f, seed, draw) cell this builds the flipped
base matrix once (all-positive ``human_empirical`` base -> a fraction ``f`` of edges
signed, via ``src.analysis.sign_composition``), records the sr-independent
W-spectrum scalars, then sweeps the spectral radius rebuilding the reservoir exactly
as the committed runs do and capturing the driven states through the evaluators'
opt-in ``collect_states`` hook. Per (cell, sr) it writes the two order-parameter
geometries (``d_eff``, ``mean_curvature``), the contrast metric (``pr``), the
common-mode / saturation diagnostics, and the co-recorded task performance.

One tidy parquet, keyed by
``(sign_mode, targeting, f, variant, spectral_radius, seed, draw, task)``:
``results/scale_<N>/phase_cells.parquet``.

No frozen hyperparameter, evaluator, figure, or committed run-matrix cell is
touched; the only new code is the sign transform and this driver. Launch via
``python -m experiments.human.analysis.phase_diagram --capture [--scale N]
[--jobs N] [--smoke] [--targeting stratified,hub_first,...] [--tasks mc,narma10,
lorenz] [--n-draws N] [--score degree|eigenvector]``.
"""

import numpy as np
import pandas as pd

from src.reservoir import blas  # noqa: F401  (cap BLAS threads; import after numpy)
from src.reservoir.build import build_from_adjacency
from src.analysis import manifold, sign_composition
from src.analysis.spectral import recurrent_spectrum
from experiments.human.substrates import HumanSubstrateBuilder
from experiments.human import matrix_config
from experiments.human.analysis.manifold.spectra import design_matrix
from experiments.human.analysis.phase_diagram import common


# ---------------------------------------------------------------------------
# Capture
# ---------------------------------------------------------------------------
def capture_cell(cell, state) -> list:
    """One cell = (task, sign_mode, targeting, variant, f_idx, seed, draw); returns
    one row per spectral radius. Signs the base once, then rebuilds + evaluates
    across sr."""
    task_name, sign_mode, targeting, variant, f_idx, seed, draw = cell
    builder, spec = state["builder"], state["specs"][task_name]
    f = state["f_grid"][f_idx]
    params = spec["params"]
    alpha = float(params["ridge_alpha"])
    rung = matrix_config.VARIANT_RUNG.get(variant, -1)

    # All-positive symmetric base (the human_empirical substrate for this variant).
    W_base = builder.weighted(common.BASE_CONDITION, variant, seed)
    # Importance score on the FIXED base topology (held across f, sr, draw); scores
    # edges for the edge arm and nodes for the Dale arm (same per-node vector).
    node_score = sign_composition.node_importance(W_base, mode=state["score_mode"])

    # Reproducible flip pattern: a deterministic function of the cell identity. The
    # Dale arm and any non-degree score each append a salt so they get independent
    # streams while the edge / degree headline keeps its exact committed entropy (no
    # extra entry).
    seed_key = [
        int(seed), int(f_idx), int(draw),
        common.TARGETING_CODE[targeting], common.VARIANT_CODE[variant],
    ]
    if sign_mode == "dale":
        seed_key.append(common.SIGN_MODE_CODE["dale"])
    if state["score_mode"] != common.SCORE_MODE:
        seed_key.append(common.SCORE_CODE[state["score_mode"]])
    flip_rng = np.random.default_rng(seed_key)
    if sign_mode == "dale":
        W = sign_composition.sign_fraction_matrix_dale(
            W_base, f, targeting, flip_rng, n_strata=state["n_strata"],
            node_score=node_score,
        )
        neg_frac = sign_composition.realised_inhibitory_fraction(W)
    else:
        W = sign_composition.sign_fraction_matrix(
            W_base, f, targeting, flip_rng, n_strata=state["n_strata"],
            node_score=node_score,
        )
        neg_frac = sign_composition.negative_fraction(W)

    # sr-independent W-spectrum scalars of the signed base (sr only rescales).
    rs = recurrent_spectrum(W)
    bulk95 = float(rs["bulk95_radius"])
    leading_gap = float(rs["spectral_gap"])
    perron_root = float(rs["perron_root"])
    # Whether the leading (max-modulus) eigenvalue is real -- the Perron signature.
    # eig_imag is sorted by descending modulus, so eig_imag[0] is the leading one.
    # The edge flip stays symmetric (all real -> True at every f); the Dale flip
    # breaks symmetry, so this genuinely tracks the Perron mode going complex as the
    # inhibitory fraction rises.
    lead_is_real = bool(abs(float(rs["eig_imag"][0])) < 1e-9)

    rows = []
    for spectral_radius in spec["sweep"]:
        reservoir = build_from_adjacency(
            weighted_adjacency=W, target_spectral_radius=spectral_radius,
            leak_rate=spec["leak_rate"], input_scaling=spec["input_scaling"],
            seed=seed, input_dim=spec["input_dim"],
        )
        out = spec["evaluate"](reservoir, seed=seed + spec["input_seed_offset"],
                               collect_states=True, **params)
        x = np.asarray(out["states"], dtype=float)

        # Order-parameter geometries + the PR contrast.
        design = design_matrix(task_name, x, params)
        d_eff = manifold.ridge_effective_rank(manifold.gram_spectrum(design), alpha)
        curv = manifold.mean_curvature(x)
        pr = manifold.participation_ratio(x)

        # Common-mode / saturation diagnostics (leak=1 -> x == tanh, gain = 1-x^2).
        gain = 1.0 - x * x
        mean_gain = float(gain.mean())
        row = dict(
            sign_mode=sign_mode, score=state["score_mode"], targeting=targeting,
            f=float(f), variant=variant,
            rung=rung, spectral_radius=float(spectral_radius), seed=int(seed),
            draw=int(draw), task=task_name,
            d_eff=float(d_eff), mean_curvature=float(curv), pr=float(pr),
            mean_state=float(x.mean()), mean_gain=mean_gain,
            frac_saturated=float((np.abs(x) > 0.99).mean()),
            effective_radius=float(bulk95 * spectral_radius * mean_gain),
            neg_frac=neg_frac, bulk95=bulk95, leading_gap=leading_gap,
            perron_root=perron_root, lead_is_real=lead_is_real, alpha=alpha,
        )
        for perf_metric in spec["perf"]:
            row[perf_metric] = float(out[perf_metric])
        rows.append(row)
    return rows


def capture(builder, specs, grid, score_mode, n_strata, jobs) -> pd.DataFrame:
    """Capture the phase-diagram grid over (task, targeting, variant, f, seed, draw)."""
    cells = [
        (task, sign_mode, targeting, variant, f_idx, seed, draw)
        for task in specs
        for sign_mode in grid["sign_modes"]
        for targeting in grid["targetings"]
        for variant in grid["variants"]
        for f_idx in range(len(grid["f_grid"]))
        for seed in range(grid["n_seeds"])
        for draw in range(grid["n_draws"])
    ]
    state = dict(builder=builder, specs=specs, f_grid=grid["f_grid"],
                 score_mode=score_mode, n_strata=n_strata)
    return common.run_cells(cells, capture_cell, state, jobs, "phase-capture")


# ---------------------------------------------------------------------------
# f=0 correctness gate: the transform is a no-op at f=0, so its co-recorded
# performance must reproduce the committed human_empirical runs.
# ---------------------------------------------------------------------------
_STRICT_TASKS = ("mc", "narma10")   # stable metrics; Lorenz is chaotic -> reported


def validate_f0(df: pd.DataFrame, specs: dict) -> None:
    """At f=0 the flipped base equals the committed ``human_empirical`` matrix, so
    the co-recorded metric must match ``results.parquet`` at the sr points the two
    grids share (0 and 6 for the full grid). Hard-asserted for MC/NARMA, reported
    for chaotic Lorenz. Averages over draws (all identical at f=0) first."""
    f0 = df[df.f == 0.0]
    if f0.empty:
        print("  [f0-gate] no f=0 rows captured -- skipping.")
        return
    keys = ["variant", "seed"]
    for task, spec in specs.items():
        path = spec["results_dir"] / "results.parquet"
        if not path.exists():
            print(f"  [f0-gate] {task}: committed {path} absent -- skipping.")
            continue
        committed = pd.read_parquet(path).copy()
        committed = committed[committed.condition == common.BASE_CONDITION]
        committed["_sr"] = committed.spectral_radius.round(6)
        sub = f0[f0.task == task].copy()
        sub["_sr"] = sub.spectral_radius.round(6)
        # Draws are identical at f=0 (no flip); take the first draw to align 1:1.
        sub = sub[sub.draw == 0]
        shared = sorted(set(sub._sr) & set(committed._sr))
        if not shared:
            print(f"  [f0-gate] {task}: no shared sr grid points -- skipping.")
            continue
        strict = task in _STRICT_TASKS
        for perf_metric in spec["perf"]:
            merged = sub[sub._sr.isin(shared)].merge(
                committed[keys + ["_sr", perf_metric]].rename(
                    columns={perf_metric: perf_metric + "_ref"}),
                on=keys + ["_sr"], how="inner")
            if merged.empty:
                print(f"  [f0-gate] {task}/{perf_metric}: no overlapping rows.")
                continue
            a = merged[perf_metric].to_numpy(float)
            b = merged[perf_metric + "_ref"].to_numpy(float)
            fin = np.isfinite(a) & np.isfinite(b)
            rel = np.abs(a[fin] - b[fin]) / np.maximum(np.abs(b[fin]), 1e-12)
            median_rel = float(np.median(rel)) if rel.size else 0.0
            max_rel = float(rel.max()) if rel.size else 0.0
            n_gross = int((rel > 1e-2).sum())
            msg = (f"  [f0-gate] {task}/{perf_metric}: {len(merged)} rows at "
                   f"sr={shared}, median rel={median_rel:.1e}, max={max_rel:.1e}, "
                   f"gross(>1%)={n_gross}")
            if strict:
                assert median_rel < 1e-5 and n_gross == 0, (
                    msg + f"\n{task}/{perf_metric}: f=0 does NOT reproduce the "
                    "committed human_empirical run -- the transform is not a clean "
                    "no-op at f=0; investigate before trusting the sweep.")
                print(msg + "  [OK]")
            else:
                print(msg + "  [chaotic: reported, not asserted]")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def run(smoke: bool = False, jobs: int = 1, scale: int | None = None,
        targetings=None, sign_modes=None, tasks=None, n_draws: int | None = None,
        score_mode: str | None = None) -> None:
    scale = matrix_config.SCALE if scale is None else scale
    score_mode = common.SCORE_MODE if score_mode is None else score_mode
    grid = common.resolve_grid(smoke)
    if targetings is not None:
        grid["targetings"] = targetings
    else:
        grid["targetings"] = common.DEFAULT_TARGETINGS
    grid["sign_modes"] = (sign_modes if sign_modes is not None
                          else common.DEFAULT_SIGN_MODES)
    if tasks is not None:
        grid["tasks"] = tasks
    if n_draws is not None:
        grid["n_draws"] = n_draws

    results_dir, _ = common.scale_dirs(scale)
    results_dir.mkdir(parents=True, exist_ok=True)

    builder = HumanSubstrateBuilder(scale=scale)
    print("Substrate summary:")
    for key, value in builder.summary().items():
        print(f"  {key}: {value}")

    # Per-task capture spec (evaluator, frozen params, build hyperparams, perf
    # cols, committed results dir), with the sweep overridden to the phase grid.
    specs = common.build_specs(scale, grid["tasks"], smoke=False, sr_max=None)
    for name in specs:
        specs[name]["sweep"] = grid["sweep"]

    n_cells = (len(specs) * len(grid["sign_modes"]) * len(grid["targetings"])
               * len(grid["variants"]) * len(grid["f_grid"]) * grid["n_seeds"]
               * grid["n_draws"])
    print(f"\nPhase-diagram capture (sign_modes={grid['sign_modes']}, "
          f"score={score_mode}):")
    print(f"  scale={scale} tasks={list(specs)} targetings={grid['targetings']}")
    print(f"  f_grid={grid['f_grid']}")
    print(f"  sr sweep={len(grid['sweep'])} pts in [{grid['sweep'][0]}, "
          f"{grid['sweep'][-1]}]")
    print(f"  variants={grid['variants']} seeds={grid['n_seeds']} "
          f"draws={grid['n_draws']}")
    print(f"  cells={n_cells} x {len(grid['sweep'])} sr = "
          f"{n_cells * len(grid['sweep'])} evaluations  jobs={jobs}\n")

    df = capture(builder, specs, grid, score_mode, common.N_STRATA, jobs)

    print(f"\nPer-cell measurement ranges:")
    for task in grid["tasks"]:
        s = df[df.task == task]
        if s.empty:
            continue
        print(f"  {task:7s}: d_eff [{s.d_eff.min():.1f}, {s.d_eff.max():.1f}]  "
              f"curv [{s.mean_curvature.min():.2f}, {s.mean_curvature.max():.2f}]  "
              f"|mean_state| [{s.mean_state.abs().min():.3f}, "
              f"{s.mean_state.abs().max():.3f}]  "
              f"eff_radius [{s.effective_radius.min():.2f}, "
              f"{s.effective_radius.max():.2f}]")

    # Non-degree scores (the eigenvector robustness run) write a score-tagged file so
    # the degree headline parquet is never touched.
    score_tag = "" if score_mode == common.SCORE_MODE else f"_{score_mode}"
    out_path = results_dir / (f"phase_cells{score_tag}"
                              f"{'_smoke' if smoke else ''}.parquet")
    df.to_parquet(out_path)
    print(f"\nSaved {out_path}  ({len(df)} rows)")

    print("\nf=0 correctness gate (transform is a no-op -> committed human_empirical):")
    validate_f0(df, specs)
    print("\nPhase-diagram capture complete.")

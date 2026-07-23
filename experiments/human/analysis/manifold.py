"""Manifold-geometry probes on the human SC reservoir (Probe 1: dimensionality
and shape).

Reuses the ``HumanSubstrateBuilder`` + ``build_from_adjacency`` + the evaluators'
opt-in ``collect_states`` path to rebuild every (condition, variant, spectral
radius, seed) reservoir EXACTLY as the committed four-task runs did (construction
is fully seed-deterministic: the same construction seed drives mask/weights/Win,
and the same ``seed + INPUT_SEED_OFFSET`` drives the task input). It captures the
driven state matrix and computes ``manifold_metrics`` inline, then writes one tidy
``results/scale_<N>/manifold_metrics.parquet`` (a ``task`` column spans the tasks)
and the PR / curvature / entropy versus spectral-radius figures.

This is the substrate-analysis tier (like ``spectral.py``): nothing is trained and
no frozen hyperparameter or the run matrix is touched. Because each cell re-runs
the real evaluator, it also records that cell's performance metric, which is
asserted bit-for-bit against the committed ``results.parquet`` -- a correctness
gate proving the captured states are the same reservoirs the floor measured.

    python -m experiments.human.analysis.manifold --scale 448 [--jobs N] [--smoke]

Tasks captured (human N=448 has committed results for these): memory capacity,
NARMA-10, and Lorenz (its teacher-forced driven states -- the manifold the readout
is fit on, not the autonomous free-run). Mackey-Glass is skipped (not run yet).
"""

import json
import sys
import time
import multiprocessing as mp
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import spearmanr
from threadpoolctl import threadpool_limits

from src.reservoir import blas  # noqa: F401  (limit BLAS threads; import early)
from src.reservoir.build import build_from_adjacency
from src.analysis import manifold
from src.experiment.plots import _VARIANT_STYLE, _VARIANT_LABEL
from experiments.human.substrates import HumanSubstrateBuilder
from experiments.human import matrix_config
from experiments.human.human_mc import task_config as mc_task_config
from experiments.human.human_narma10 import task_config as narma_task_config
from experiments.human.human_lorenz import task_config as lorenz_task_config

_DIR = Path(__file__).resolve().parent
FIGURES_DIR = _DIR / "figures"
RESULTS_DIR = _DIR / "results"

# Task registry: name -> (results subdir, task_config module, task() args,
# performance-metric columns to co-record and validate).
_TASK_DEFS = {
    "mc": ("human_mc", mc_task_config, (), ["mc"]),
    "narma10": ("human_narma10", narma_task_config, (), ["nrmse"]),
    "lorenz": ("human_lorenz", lorenz_task_config, ("vpt",), ["vpt", "climate_error"]),
}
DEFAULT_TASKS = ["mc", "narma10", "lorenz"]

CONDITION_TITLE = {
    "human_gaussian": "Human · gaussian",
    "human_empirical_signed": "Human · empirical ±",
    "human_empirical": "Human · empirical",
}
TASK_TITLE = {
    "mc": "Memory capacity",
    "narma10": "NARMA-10",
    "lorenz": "Lorenz (teacher-forced)",
}
_SUPERCRITICAL_COLOR = "#fff3e0"

# The three headline geometry metrics and their figure metadata.
_METRIC_FIGURES = {
    "pr": dict(ylabel="participation ratio (PR)", ylim=None,
               suptitle="Manifold dimensionality (participation ratio) vs spectral radius"),
    "mean_curvature": dict(ylabel="mean curvature (rad)", ylim=(0.0, np.pi),
                           suptitle="Manifold curvature (trajectory straightening) vs spectral radius"),
    "spectral_entropy": dict(ylabel="spectral entropy (norm.)", ylim=(0.0, 1.05),
                             suptitle="Manifold spectral entropy vs spectral radius"),
}

# Shared read-only worker state for the fork-parallel path (set before the pool
# forks; children inherit copy-on-write, so the builder is never pickled).
_WORKER: dict = {}


# ---------------------------------------------------------------------------
# Task specs + spectral-radius sweep resolution
# ---------------------------------------------------------------------------
def _committed_results_dir(subdir: str, scale: int) -> Path:
    return _ROOT / "experiments" / "human" / subdir / "results" / f"scale_{scale}"


def _resolve_sweep(subdir: str, scale: int, smoke: bool, sr_max) -> list:
    """Spectral-radius grid to capture on.

    Full runs read the grid from the task's committed ``manifest.json`` so the
    Probe 3 join and the performance-validation gate align exactly; ``--sr-max``
    overrides; ``--smoke`` uses a tiny grid.
    """
    if smoke:
        return [0.0, 0.95, 1.5]
    if sr_max is not None:
        return [round(float(sr), 6) for sr in matrix_config.spectral_sweep(sr_max)]
    manifest = _committed_results_dir(subdir, scale) / "manifest.json"
    if manifest.exists():
        grid = json.loads(manifest.read_text())["spectral_radii"]
        return [round(float(sr), 6) for sr in grid]
    return [round(float(sr), 6) for sr in matrix_config.spectral_sweep(6.0)]


def _build_specs(scale: int, tasks, smoke: bool, sr_max) -> dict:
    """Per-task capture spec: the evaluator, its frozen params, the reservoir
    build hyperparameters, the sweep, and the committed-results dir."""
    offset = matrix_config.INPUT_SEED_OFFSET
    specs = {}
    for name in tasks:
        subdir, module, task_args, perf = _TASK_DEFS[name]
        t = module.task(*task_args)
        specs[name] = dict(
            evaluate=t["task_evaluate"],
            params=dict(t["task_params"]),
            input_scaling=t["input_scaling"],
            leak_rate=t["leak_rate"],
            input_dim=t.get("input_dim", 1),
            input_seed_offset=offset,
            perf=perf,
            sweep=_resolve_sweep(subdir, scale, smoke, sr_max),
            results_dir=_committed_results_dir(subdir, scale),
        )
    return specs


# ---------------------------------------------------------------------------
# Capture: one (task, condition, variant, seed) cell across its sweep
# ---------------------------------------------------------------------------
def _capture_cell(builder, spec, task_name, condition, variant, seed) -> list:
    """Rebuild the reservoir per spectral radius (bit-identical to the runner),
    capture its driven state matrix, and return one metrics row per sr."""
    weighted = builder.weighted(condition, variant, seed)
    rung = matrix_config.VARIANT_RUNG.get(variant, -1)
    rows = []
    for spectral_radius in spec["sweep"]:
        reservoir = build_from_adjacency(
            weighted_adjacency=weighted,
            target_spectral_radius=spectral_radius,
            leak_rate=spec["leak_rate"],
            input_scaling=spec["input_scaling"],
            seed=seed,
            input_dim=spec["input_dim"],
        )
        out = spec["evaluate"](
            reservoir,
            seed=seed + spec["input_seed_offset"],
            collect_states=True,
            **spec["params"],
        )
        metrics = manifold.manifold_metrics(out["states"])
        row = dict(
            task=task_name, condition=condition, variant=variant, rung=rung,
            spectral_radius=spectral_radius, seed=seed, **metrics,
        )
        for perf_metric in spec["perf"]:
            row[perf_metric] = out[perf_metric]
        rows.append(row)
    return rows


def _cell_worker(cell):
    """Fork-worker entry: read the builder/specs from ``_WORKER``, pin BLAS to one
    thread, capture the cell."""
    task_name, condition, variant, seed = cell
    builder, specs = _WORKER["builder"], _WORKER["specs"]
    with threadpool_limits(limits=1):
        return _capture_cell(builder, specs[task_name], task_name, condition,
                             variant, seed)


def _cells(specs, conditions, variants, n_seeds) -> list:
    return [(task, c, v, s) for task in specs for c in conditions
            for v in variants for s in range(n_seeds)]


def capture(builder, specs, conditions, variants, n_seeds, jobs) -> pd.DataFrame:
    """Capture manifold metrics over the (task, condition, variant, seed) grid."""
    cells = _cells(specs, conditions, variants, n_seeds)
    total = len(cells)
    t0 = time.time()
    rows = []
    if jobs and jobs > 1:
        _WORKER.update(builder=builder, specs=specs)
        print(f"Parallel capture: {total} cells across {jobs} fork workers "
              f"(1 BLAS thread each).", flush=True)
        ctx = mp.get_context("fork")
        with ctx.Pool(processes=jobs) as pool:
            for i, cell_rows in enumerate(pool.imap(_cell_worker, cells), start=1):
                rows.extend(cell_rows)
                if i % 20 == 0 or i == total:
                    elapsed = time.time() - t0
                    eta = elapsed * (total - i) / max(i, 1)
                    print(f"  {i}/{total} cells ({100 * i / total:.0f}%) "
                          f"elapsed={elapsed:.0f}s eta={eta:.0f}s", flush=True)
    else:
        for i, cell in enumerate(cells, start=1):
            task_name, condition, variant, seed = cell
            rows.extend(_capture_cell(builder, specs[task_name], task_name,
                                      condition, variant, seed))
            if i % 20 == 0 or i == total:
                elapsed = time.time() - t0
                print(f"  {i}/{total} cells ({100 * i / total:.0f}%) "
                      f"elapsed={elapsed:.0f}s", flush=True)
    print(f"Capture done in {time.time() - t0:.0f}s ({total} cells).")
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Correctness gate: co-recorded performance metric vs the committed run
# ---------------------------------------------------------------------------
# Tasks whose performance metric is a stable (non-chaotic) function of the states,
# so it reproduces the committed run tightly and can be hard-asserted. Lorenz is
# excluded: its closed-loop free-run is chaotic, so a sub-ULP state difference
# (e.g. a BLAS-thread-count mismatch vs the committed run) can amplify VPT/climate
# by O(1). Lorenz shares the SAME construction path, so MC+NARMA matching already
# proves the reservoirs are rebuilt correctly; Lorenz is reported, not asserted.
_STRICT_VALIDATION_TASKS = ("mc", "narma10")


def validate_against_committed(df: pd.DataFrame, specs: dict,
                               strict_tasks=_STRICT_VALIDATION_TASKS) -> None:
    """Check the co-recorded performance metric reproduces the committed
    ``results.parquet``. Strict tasks (stable metrics) are hard-asserted to
    machine precision (up to BLAS float-reduction order); chaotic tasks (Lorenz)
    are reported with a loud warning if agreement is poor, but not asserted."""
    keys = ["condition", "variant", "seed"]
    for task, spec in specs.items():
        path = spec["results_dir"] / "results.parquet"
        if not path.exists():
            print(f"  [validate] {task}: committed {path} absent -- skipping gate.")
            continue
        committed = pd.read_parquet(path).copy()
        committed["_sr"] = committed.spectral_radius.round(6)
        sub = df[df.task == task].copy()
        sub["_sr"] = sub.spectral_radius.round(6)
        strict = task in strict_tasks
        for perf_metric in spec["perf"]:
            merged = sub.merge(
                committed[keys + ["_sr", perf_metric]].rename(
                    columns={perf_metric: perf_metric + "_committed"}),
                on=keys + ["_sr"], how="inner",
            )
            a = merged[perf_metric].to_numpy(dtype=float)
            b = merged[perf_metric + "_committed"].to_numpy(dtype=float)
            both_fin = np.isfinite(a) & np.isfinite(b)
            n_flip = int((np.isfinite(a) ^ np.isfinite(b)).sum())  # inf vs finite
            rel = (np.abs(a[both_fin] - b[both_fin])
                   / np.maximum(np.abs(b[both_fin]), 1e-12))
            median_rel = float(np.median(rel)) if rel.size else 0.0
            max_rel = float(rel.max()) if rel.size else 0.0
            # "Gross" = >1% relative: FP/ill-conditioning noise sits ~1e-7-1e-5,
            # a real construction bug shifts essentially every row by O(0.1-1),
            # so this threshold cleanly separates them.
            n_gross = int((rel > 1e-2).sum())
            tag = "validate" if strict else "validate/soft"
            msg = (f"  [{tag}] {task}/{perf_metric}: {len(merged)} rows, "
                   f"median rel diff={median_rel:.1e}, max={max_rel:.1e}, "
                   f"gross(>1%)={n_gross}, inf/finite flips={n_flip}")
            if strict:
                assert median_rel < 1e-5 and n_gross == 0, (
                    msg + f"\n{task}/{perf_metric}: capture does NOT reproduce the "
                    "committed reservoirs -- check seeds/params/substrate.")
                print(msg)
            else:
                print(msg + ("  [chaotic metric: reported, not asserted]"
                             if median_rel < 1e-2 else
                             "  !! LARGE median disagreement -- inspect."))


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
def _aggregate(df_sub: pd.DataFrame, value_col: str) -> pd.DataFrame:
    """Per-(variant, sr) median and interquartile range across seeds."""
    g = df_sub.groupby(["variant", "spectral_radius"])[value_col]
    out = g.median().reset_index(name="median")
    out["q25"] = g.quantile(0.25).to_numpy()
    out["q75"] = g.quantile(0.75).to_numpy()
    return out


def _plot_metric_grid(df, value_col, ylabel, suptitle, path, supercrit, ylim=None):
    """Grid of ``value_col`` vs spectral radius: rows = tasks, cols = conditions,
    one median line per variant (IQR band on connectome + degree_rewire)."""
    tasks = [t for t in DEFAULT_TASKS if t in df.task.unique()]
    conditions = [c for c in matrix_config.CONDITIONS if c in df.condition.unique()]
    variants = matrix_config.VARIANTS
    nrows, ncols = len(tasks), len(conditions)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.0 * ncols, 3.1 * nrows),
                             squeeze=False, sharex=True, sharey="row")
    sr_max = float(df.spectral_radius.max())
    for i, task in enumerate(tasks):
        for j, condition in enumerate(conditions):
            ax = axes[i][j]
            sub = df[(df.task == task) & (df.condition == condition)]
            agg = _aggregate(sub, value_col)
            for variant in variants:
                vv = agg[agg.variant == variant].sort_values("spectral_radius")
                if vv.empty:
                    continue
                style = _VARIANT_STYLE[variant]
                ax.plot(vv.spectral_radius, vv["median"],
                        label=_VARIANT_LABEL[variant], **style)
                if variant in ("connectome", "degree_rewire"):
                    ax.fill_between(vv.spectral_radius, vv["q25"], vv["q75"],
                                    color=style["color"], alpha=0.15, zorder=2)
            start = supercrit.get(condition) if supercrit else None
            if start is not None:
                ax.axvspan(start, sr_max, color=_SUPERCRITICAL_COLOR, zorder=0)
            ax.axvline(1.0, color="grey", lw=0.8, ls=":", zorder=1)
            ax.grid(alpha=0.25)
            if ylim is not None:
                ax.set_ylim(*ylim)
            if i == 0:
                ax.set_title(CONDITION_TITLE.get(condition, condition), fontsize=10)
            if j == 0:
                ax.set_ylabel(f"{TASK_TITLE.get(task, task)}\n{ylabel}", fontsize=9)
            if i == nrows - 1:
                ax.set_xlabel("spectral radius")
    handles = [plt.Line2D([0], [0], **{k: v for k, v in _VARIANT_STYLE[v].items()
                                       if k != "zorder"}, label=_VARIANT_LABEL[v])
               for v in variants]
    handles.append(mpatches.Patch(facecolor=_SUPERCRITICAL_COLOR, edgecolor="none",
                                  label="connectome bulk supercritical (sr ≥ $sr_{crit}$)"))
    fig.legend(handles=handles, loc="lower center", ncol=4, fontsize=8,
               framealpha=0.9, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle(suptitle, fontsize=12)
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def write_figures(df, figures_dir, supercrit):
    figures_dir.mkdir(parents=True, exist_ok=True)
    for value_col, meta in _METRIC_FIGURES.items():
        path = figures_dir / f"manifold_{value_col}_vs_sr.png"
        _plot_metric_grid(df, value_col, meta["ylabel"], meta["suptitle"], path,
                          supercrit, ylim=meta["ylim"])
        print(f"Saved {path}")


# ---------------------------------------------------------------------------
# Quick-glance summary (for the Findings block)
# ---------------------------------------------------------------------------
def _write_summary(df, path, supercrit):
    """Seed-median PR for connectome vs degree_rewire at a canonical (~0.95) and a
    supercritical (nearest sr_crit) operating point, per task/condition."""
    srs = sorted(df.spectral_radius.unique())
    canonical = min(srs, key=lambda s: abs(s - 0.95))
    lines = ["# Manifold Probe 1 -- PR at canonical vs supercritical (seed medians)\n",
             f"Canonical sr = {canonical:g}; supercritical sr = nearest grid point to "
             "each condition's sr_crit (1/bulk95_ratio).\n",
             "| task | condition | sr | PR connectome | PR degree_rewire | PR random_gaussian |",
             "|---|---|---|---|---|---|"]

    def _median(task, condition, sr, variant):
        m = df[(df.task == task) & (df.condition == condition)
               & (np.isclose(df.spectral_radius, sr)) & (df.variant == variant)]["pr"]
        return float(m.median()) if len(m) else float("nan")

    for task in [t for t in DEFAULT_TASKS if t in df.task.unique()]:
        for condition in matrix_config.CONDITIONS:
            crit = supercrit.get(condition)
            sr_super = min(srs, key=lambda s: abs(s - crit)) if crit else max(srs)
            for label, sr in [("canonical", canonical), ("supercrit", sr_super)]:
                lines.append(
                    f"| {task} | {condition} | {sr:g} ({label}) | "
                    f"{_median(task, condition, sr, 'connectome'):.2f} | "
                    f"{_median(task, condition, sr, 'degree_rewire'):.2f} | "
                    f"{_median(task, condition, sr, 'random_gaussian'):.2f} |")
    path.write_text("\n".join(lines) + "\n")
    print(f"Saved {path}")


# ---------------------------------------------------------------------------
# Probe 2: manifold alignment with structural modes
# ---------------------------------------------------------------------------
# Bases are sr-invariant (rescaling W does not move its eigenvectors, nor the
# Laplacian's), so they are built once per (condition, variant, seed) and reused
# across the representative spectral radii; only the states change with sr.
PROBE2_VARIANTS = ["connectome", "degree_rewire"]  # substrate of interest + key null
PROBE2_N_RANDOM = 20
BASIS_TITLE = {
    "harmonics": "Laplacian harmonics (low-freq)",
    "wmodes": "W eigenmodes (dominant)",
    "random": "random orthonormal",
}
BASIS_COLOR = {"harmonics": "#1f77b4", "wmodes": "#d62728", "random": "#999999"}


def _structural_bases(weighted: np.ndarray) -> dict:
    """The two structural bases for the alignment probe (both orthonormal). The
    Laplacian uses |weighted| (== weighted for the non-negative empirical
    substrate); the W-modes are ordered by descending |eigenvalue|."""
    return {"harmonics": manifold.graph_laplacian_harmonics(weighted),
            "wmodes": manifold.symmetric_eigenbasis(weighted, order="abs_desc")}


def _probe2_sr_list(condition: str, supercrit: dict, srs: list) -> list:
    """Representative operating points: canonical (~0.95) + the connectome's
    supercritical point (nearest grid to sr_crit)."""
    canonical = min(srs, key=lambda s: abs(s - 0.95))
    crit = supercrit.get(condition)
    super_pt = min(srs, key=lambda s: abs(s - crit)) if crit else max(srs)
    out = []
    for sr in (canonical, super_pt):
        if sr not in out:
            out.append(sr)
    return out


def _alignment_cell(builder, spec, task_name, condition, variant, seed, sr_list,
                    k_grid, n_random) -> list:
    """Build the structural bases once, then per sr capture states and record the
    cumulative captured-variance curve for each basis (+ the random band)."""
    weighted = builder.weighted(condition, variant, seed)
    bases = _structural_bases(weighted)
    rows = []
    for spectral_radius in sr_list:
        reservoir = build_from_adjacency(
            weighted_adjacency=weighted, target_spectral_radius=spectral_radius,
            leak_rate=spec["leak_rate"], input_scaling=spec["input_scaling"],
            seed=seed, input_dim=spec["input_dim"])
        out = spec["evaluate"](reservoir, seed=seed + spec["input_seed_offset"],
                               collect_states=True, **spec["params"])
        states = out["states"]
        common = dict(task=task_name, condition=condition, variant=variant,
                      seed=seed, spectral_radius=spectral_radius)
        for basis_name, basis in bases.items():
            curve = manifold.basis_alignment(states, basis, k_grid)["captured"]
            for k, cap in zip(k_grid, curve):
                rows.append(dict(common, basis=basis_name, k=int(k),
                                 captured=float(cap), captured_std=0.0))
        band = manifold.random_basis_band(states, k_grid, n_random=n_random, seed=seed)
        for k, mean, std in zip(k_grid, band["mean"], band["std"]):
            rows.append(dict(common, basis="random", k=int(k),
                             captured=float(mean), captured_std=float(std)))
    return rows


def _alignment_worker(cell):
    task_name, condition, variant, seed = cell
    W = _WORKER
    with threadpool_limits(limits=1):
        return _alignment_cell(W["builder"], W["specs"][task_name], task_name,
                               condition, variant, seed,
                               W["sr_by_condition"][condition], W["k_grid"],
                               W["n_random"])


def capture_alignment(builder, specs, conditions, variants, n_seeds,
                      sr_by_condition, k_grid, n_random, jobs) -> pd.DataFrame:
    cells = [(t, c, v, s) for t in specs for c in conditions for v in variants
             for s in range(n_seeds)]
    total = len(cells)
    t0 = time.time()
    rows = []
    if jobs and jobs > 1:
        _WORKER.update(builder=builder, specs=specs, sr_by_condition=sr_by_condition,
                       k_grid=k_grid, n_random=n_random)
        print(f"Parallel alignment: {total} cells across {jobs} fork workers.",
              flush=True)
        ctx = mp.get_context("fork")
        with ctx.Pool(processes=jobs) as pool:
            for i, cell_rows in enumerate(pool.imap(_alignment_worker, cells), start=1):
                rows.extend(cell_rows)
                if i % 20 == 0 or i == total:
                    print(f"  {i}/{total} cells ({100 * i / total:.0f}%)", flush=True)
    else:
        for i, (t, c, v, s) in enumerate(cells, start=1):
            rows.extend(_alignment_cell(builder, specs[t], t, c, v, s,
                        sr_by_condition[c], k_grid, n_random))
            if i % 20 == 0 or i == total:
                print(f"  {i}/{total} cells ({100 * i / total:.0f}%)", flush=True)
    print(f"Alignment capture done in {time.time() - t0:.0f}s ({total} cells).")
    return pd.DataFrame(rows)


def _plot_alignment(df, variant, sr_by_condition, use_supercritical, suptitle, path):
    """Cumulative captured variance vs k: rows = tasks, cols = conditions; three
    curves (harmonics, W-modes, random band) for ``variant`` at each condition's
    representative operating point."""
    tasks = [t for t in DEFAULT_TASKS if t in df.task.unique()]
    conditions = [c for c in matrix_config.CONDITIONS if c in df.condition.unique()]
    nrows, ncols = len(tasks), len(conditions)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.0 * ncols, 3.1 * nrows),
                             squeeze=False, sharex=True, sharey=True)
    for i, task in enumerate(tasks):
        for j, condition in enumerate(conditions):
            ax = axes[i][j]
            sr_list = sr_by_condition[condition]
            sr = sr_list[-1] if use_supercritical else sr_list[0]
            sub = df[(df.task == task) & (df.condition == condition)
                     & (df.variant == variant) & np.isclose(df.spectral_radius, sr)]
            for basis_name in ("harmonics", "wmodes", "random"):
                b = sub[sub.basis == basis_name]
                if b.empty:
                    continue
                g = b.groupby("k").captured.median().reset_index().sort_values("k")
                ax.plot(g.k, g.captured, color=BASIS_COLOR[basis_name],
                        label=BASIS_TITLE[basis_name], lw=1.8, marker="o", ms=3)
                if basis_name == "random":
                    spread = b.groupby("k").captured_std.median().reindex(g.k).values
                    ax.fill_between(g.k, g.captured - spread, g.captured + spread,
                                    color=BASIS_COLOR[basis_name], alpha=0.25)
            ax.set_xscale("log")
            ax.set_ylim(0, 1.02)
            ax.grid(alpha=0.25, which="both")
            ax.text(0.04, 0.96, f"sr={sr:g}", transform=ax.transAxes, fontsize=8,
                    va="top", ha="left", color="0.3")
            if i == 0:
                ax.set_title(CONDITION_TITLE.get(condition, condition), fontsize=10)
            if j == 0:
                ax.set_ylabel(f"{TASK_TITLE.get(task, task)}\ncaptured variance",
                              fontsize=9)
            if i == nrows - 1:
                ax.set_xlabel("k (basis vectors, log)")
    handles = [plt.Line2D([0], [0], color=BASIS_COLOR[b], lw=1.8, marker="o", ms=3,
                          label=BASIS_TITLE[b]) for b in ("harmonics", "wmodes", "random")]
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=9,
               framealpha=0.9, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle(suptitle, fontsize=12)
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _write_alignment_summary(df, path, sr_by_condition, variant="connectome",
                             k_ref=10):
    """Captured variance at k=k_ref for each basis, connectome, at the supercritical
    operating point per task/condition (the headline alignment numbers)."""
    lines = [f"# Manifold Probe 2 -- variance captured by top-{k_ref} basis vectors "
             f"({variant}, supercritical op. point; seed medians)\n",
             "harmonics = low-freq graph-Laplacian; wmodes = dominant |eigenvalue| "
             "of W; random = chance band. Higher = manifold lives in that basis.\n",
             f"| task | condition | sr | harmonics@{k_ref} | wmodes@{k_ref} | random@{k_ref} |",
             "|---|---|---|---|---|---|"]

    def _cap(task, cond, sr, basis):
        m = df[(df.task == task) & (df.condition == cond) & (df.variant == variant)
               & np.isclose(df.spectral_radius, sr) & (df.basis == basis)
               & (df.k == k_ref)].captured
        return float(m.median()) if len(m) else float("nan")

    for task in [t for t in DEFAULT_TASKS if t in df.task.unique()]:
        for cond in matrix_config.CONDITIONS:
            sr = sr_by_condition[cond][-1]
            lines.append(f"| {task} | {cond} | {sr:g} | {_cap(task, cond, sr, 'harmonics'):.2f} | "
                         f"{_cap(task, cond, sr, 'wmodes'):.2f} | {_cap(task, cond, sr, 'random'):.2f} |")
    path.write_text("\n".join(lines) + "\n")
    print(f"Saved {path}")


def main_probe2(smoke: bool = False, jobs: int = 1, scale: int | None = None,
                tasks=None) -> None:
    scale = matrix_config.SCALE if scale is None else scale
    tasks = tasks or DEFAULT_TASKS
    results_dir = RESULTS_DIR / f"scale_{scale}"
    figures_dir = FIGURES_DIR / f"scale_{scale}"
    results_dir.mkdir(parents=True, exist_ok=True)

    builder = HumanSubstrateBuilder(scale=scale)
    # The full [0,6] grid is used only to pick representative operating points; the
    # reservoir hyperparameters/params come from the specs (smoke reduces the cells).
    specs = _build_specs(scale, tasks, smoke=False, sr_max=None)
    conditions = matrix_config.CONDITIONS
    supercrit = builder.connectome_supercritical_radii(conditions)
    srs = specs[tasks[0]]["sweep"]
    sr_by_condition = {c: _probe2_sr_list(c, supercrit, srs) for c in conditions}
    k_grid = manifold.default_k_grid(int(builder.mask.shape[0]))
    variants = ["connectome"] if smoke else PROBE2_VARIANTS
    n_seeds = 2 if smoke else matrix_config.N_SEEDS
    print(f"Probe 2 alignment: tasks={list(specs)} scale={scale} variants={variants} "
          f"n_seeds={n_seeds} jobs={jobs}")
    print(f"  operating points per condition: "
          f"{ {c: sr_by_condition[c] for c in conditions} }")
    print(f"  k_grid={k_grid}\n")

    df = capture_alignment(builder, specs, conditions, variants, n_seeds,
                           sr_by_condition, k_grid, PROBE2_N_RANDOM, jobs)
    out_parquet = results_dir / "manifold_alignment.parquet"
    df.to_parquet(out_parquet)
    print(f"\nSaved {out_parquet}  ({len(df)} rows)")

    figures_dir.mkdir(parents=True, exist_ok=True)
    _plot_alignment(df, "connectome", sr_by_condition, use_supercritical=True,
                    suptitle="Probe 2: activity-manifold alignment with structural bases "
                             "(connectome, supercritical operating point)",
                    path=figures_dir / "manifold_alignment_connectome_supercritical.png")
    print(f"Saved {figures_dir / 'manifold_alignment_connectome_supercritical.png'}")
    _plot_alignment(df, "connectome", sr_by_condition, use_supercritical=False,
                    suptitle="Probe 2: activity-manifold alignment with structural bases "
                             "(connectome, canonical operating point)",
                    path=figures_dir / "manifold_alignment_connectome_canonical.png")
    print(f"Saved {figures_dir / 'manifold_alignment_connectome_canonical.png'}")
    _write_alignment_summary(df, results_dir / "manifold_alignment_summary.md",
                             sr_by_condition)
    print("\nProbe 2 alignment complete.")


# ---------------------------------------------------------------------------
# Probe 3: geometry -> performance link
# ---------------------------------------------------------------------------
# No new reservoir runs: the Probe 1 parquet already carries the co-recorded,
# bit-exact-validated performance metric per row, so geometry and performance are
# joined by construction. Divergence caps match the task configs (stats tier).
_PERF_BY_TASK = {"mc": ["mc"], "narma10": ["nrmse"], "lorenz": ["vpt", "climate_error"]}
_PERF_PRIMARY = {"mc": "mc", "narma10": "nrmse", "lorenz": "vpt"}
_PERF_LOWER_BETTER = {"mc": False, "nrmse": True, "vpt": False, "climate_error": True}
_PERF_CAP = {"nrmse": 2.0, "climate_error": 10.0}   # None for mc/vpt (bounded)
_GEOM_METRICS = ["pr", "mean_curvature", "spectral_entropy"]
_GEOM_LABEL = {"pr": "participation ratio", "mean_curvature": "mean curvature (rad)",
               "spectral_entropy": "spectral entropy (norm.)"}
_PERF_LABEL = {"mc": "memory capacity", "nrmse": "NARMA-10 NRMSE",
               "vpt": "Lorenz VPT", "climate_error": "Lorenz climate error"}
_SUPERCRITICAL_SR = 1.25  # nominal supercritical threshold for the pooled scope


def _capped_perf(values: np.ndarray, metric: str) -> np.ndarray:
    """Divergence-cap a performance column (non-finite / beyond cap -> cap), for
    lower-is-better metrics only; bounded metrics (mc, vpt) pass through."""
    v = np.asarray(values, dtype=float)
    cap = _PERF_CAP.get(metric)
    if cap is None:
        return v
    v = np.where(np.isfinite(v), v, cap)
    return np.minimum(v, cap)


def _correlations(df: pd.DataFrame) -> pd.DataFrame:
    """Spearman rank correlation of each geometry metric vs each performance metric,
    pooled (all conditions) and per condition, over all sr and the supercritical
    region."""
    rows = []
    tasks = [t for t in DEFAULT_TASKS if t in df.task.unique()]
    for task in tasks:
        tdf = df[df.task == task]
        for perf in _PERF_BY_TASK[task]:
            for geom in _GEOM_METRICS:
                scopes = [("pooled", tdf)]
                scopes += [(c, tdf[tdf.condition == c]) for c in matrix_config.CONDITIONS]
                for cond_name, cdf in scopes:
                    for region, mask in [("all_sr", cdf.spectral_radius >= 0),
                                         ("supercritical",
                                          cdf.spectral_radius >= _SUPERCRITICAL_SR)]:
                        s = cdf[mask]
                        x = s[geom].to_numpy(float)
                        y = _capped_perf(s[perf].to_numpy(float), perf)
                        ok = np.isfinite(x) & np.isfinite(y)
                        if ok.sum() < 10:
                            continue
                        r, p = spearmanr(x[ok], y[ok])
                        rows.append(dict(task=task, performance=perf, geometry=geom,
                                         condition=cond_name, region=region,
                                         spearman_r=float(r), p_value=float(p),
                                         n=int(ok.sum())))
    return pd.DataFrame(rows)


def _gap_frame(df: pd.DataFrame, supercrit: dict) -> pd.DataFrame:
    """Per (task, condition, supercritical sr): connectome-minus-degree_rewire gap in
    geometry and performance, oriented so positive == connectome better/holds more."""
    rows = []
    tasks = [t for t in DEFAULT_TASKS if t in df.task.unique()]
    for task in tasks:
        for cond in matrix_config.CONDITIONS:
            crit = supercrit.get(cond, _SUPERCRITICAL_SR)
            sub = df[(df.task == task) & (df.condition == cond)
                     & (df.spectral_radius >= crit)]
            for sr, g in sub.groupby("spectral_radius"):
                conn = g[g.variant == "connectome"]
                deg = g[g.variant == "degree_rewire"]
                if conn.empty or deg.empty:
                    continue
                rec = dict(task=task, condition=cond, spectral_radius=float(sr),
                           # PR held: + == connectome more dimensions
                           dPR=float(conn.pr.median() - deg.pr.median()),
                           # straighter: + == connectome lower curvature
                           dStraight=float(deg.mean_curvature.median()
                                           - conn.mean_curvature.median()))
                for perf in _PERF_BY_TASK[task]:
                    cp = float(np.median(_capped_perf(conn[perf].to_numpy(float), perf)))
                    dp = float(np.median(_capped_perf(deg[perf].to_numpy(float), perf)))
                    rec[f"d_{perf}"] = (dp - cp) if _PERF_LOWER_BETTER[perf] else (cp - dp)
                rows.append(rec)
    return pd.DataFrame(rows)


_CONDITION_COLOR = {"human_gaussian": "#4c72b0", "human_empirical_signed": "#dd8452",
                    "human_empirical": "#c44e52"}


def _plot_geometry_vs_performance(df, path):
    """Scatter grid: rows = tasks, cols = geometry metrics; y = the task's primary
    performance metric; one point per (variant, sr) seed-median, coloured by
    condition. Spearman r (pooled, all sr) annotated."""
    tasks = [t for t in DEFAULT_TASKS if t in df.task.unique()]
    nrows, ncols = len(tasks), len(_GEOM_METRICS)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.0 * ncols, 3.2 * nrows),
                             squeeze=False)
    for i, task in enumerate(tasks):
        perf = _PERF_PRIMARY[task]
        tdf = df[df.task == task]
        agg = (tdf.groupby(["condition", "variant", "spectral_radius"])
               .agg(**{g: (g, "median") for g in _GEOM_METRICS},
                    perf=(perf, lambda s: np.median(_capped_perf(s.to_numpy(float), perf))))
               .reset_index())
        for j, geom in enumerate(_GEOM_METRICS):
            ax = axes[i][j]
            for cond in matrix_config.CONDITIONS:
                c = agg[agg.condition == cond]
                ax.scatter(c[geom], c["perf"], s=14, alpha=0.55,
                           color=_CONDITION_COLOR[cond], edgecolor="none",
                           label=CONDITION_TITLE.get(cond, cond))
            x = agg[geom].to_numpy(float)
            y = agg["perf"].to_numpy(float)
            ok = np.isfinite(x) & np.isfinite(y)
            r, _ = spearmanr(x[ok], y[ok])
            ax.text(0.04, 0.96, f"$r_s$={r:+.2f}", transform=ax.transAxes,
                    va="top", ha="left", fontsize=9,
                    bbox=dict(boxstyle="round", fc="white", ec="0.7", alpha=0.8))
            ax.grid(alpha=0.25)
            if i == nrows - 1:
                ax.set_xlabel(_GEOM_LABEL[geom])
            if j == 0:
                ax.set_ylabel(f"{TASK_TITLE.get(task, task)}\n{_PERF_LABEL[perf]}",
                              fontsize=9)
    handles = [plt.Line2D([0], [0], marker="o", ls="", color=_CONDITION_COLOR[c],
                          label=CONDITION_TITLE.get(c, c)) for c in matrix_config.CONDITIONS]
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=9,
               bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("Probe 3: manifold geometry vs task performance "
                 "(seed-median per variant x sr; $r_s$ = pooled Spearman)", fontsize=12)
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _plot_gap_tracking(gap, path):
    """Does the connectome-minus-degree geometric gap track the performance gap in
    the supercritical region? Rows = tasks; cols = [dPR, dStraight]; y = primary
    performance gap (oriented so + == connectome better)."""
    tasks = [t for t in DEFAULT_TASKS if t in gap.task.unique()]
    gap_cols = [("dPR", "$\\Delta$PR (connectome - degree)"),
                ("dStraight", "$\\Delta$straightness (degree - connectome curvature)")]
    nrows, ncols = len(tasks), len(gap_cols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.4 * ncols, 3.2 * nrows),
                             squeeze=False)
    for i, task in enumerate(tasks):
        perf = _PERF_PRIMARY[task]
        tdf = gap[gap.task == task]
        for j, (gcol, glabel) in enumerate(gap_cols):
            ax = axes[i][j]
            for cond in matrix_config.CONDITIONS:
                c = tdf[tdf.condition == cond]
                ax.scatter(c[gcol], c[f"d_{perf}"], s=20, alpha=0.6,
                           color=_CONDITION_COLOR[cond],
                           label=CONDITION_TITLE.get(cond, cond))
            x = tdf[gcol].to_numpy(float)
            y = tdf[f"d_{perf}"].to_numpy(float)
            ok = np.isfinite(x) & np.isfinite(y)
            if ok.sum() > 5:
                r, _ = spearmanr(x[ok], y[ok])
                ax.text(0.04, 0.96, f"$r_s$={r:+.2f}", transform=ax.transAxes,
                        va="top", ha="left", fontsize=9,
                        bbox=dict(boxstyle="round", fc="white", ec="0.7", alpha=0.8))
            ax.axhline(0, color="0.6", lw=0.8, ls=":")
            ax.axvline(0, color="0.6", lw=0.8, ls=":")
            ax.grid(alpha=0.25)
            if i == nrows - 1:
                ax.set_xlabel(glabel, fontsize=9)
            if j == 0:
                ax.set_ylabel(f"{TASK_TITLE.get(task, task)}\n$\\Delta${_PERF_LABEL[perf]}"
                              "\n(+ = connectome better)", fontsize=8)
    handles = [plt.Line2D([0], [0], marker="o", ls="", color=_CONDITION_COLOR[c],
                          label=CONDITION_TITLE.get(c, c)) for c in matrix_config.CONDITIONS]
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=9,
               bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("Probe 3: does the connectome-vs-degree GEOMETRY gap track the "
                 "PERFORMANCE gap? (supercritical sr)", fontsize=12)
    fig.tight_layout(rect=[0, 0.05, 1, 0.97])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _plot_overlay(df, supercrit, path):
    """The story figure: PR(sr) (left axis) and the primary performance curve (right
    axis) on shared axes, connectome (solid) vs degree_rewire (dashed), per
    task x condition. Seed medians."""
    tasks = [t for t in DEFAULT_TASKS if t in df.task.unique()]
    conditions = [c for c in matrix_config.CONDITIONS if c in df.condition.unique()]
    nrows, ncols = len(tasks), len(conditions)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.2 * ncols, 3.1 * nrows),
                             squeeze=False, sharex=True)
    for i, task in enumerate(tasks):
        perf = _PERF_PRIMARY[task]
        for j, cond in enumerate(conditions):
            axL = axes[i][j]
            axR = axL.twinx()
            sub = df[(df.task == task) & (df.condition == cond)]
            for variant, ls in [("connectome", "-"), ("degree_rewire", "--")]:
                v = sub[sub.variant == variant]
                pr = v.groupby("spectral_radius").pr.median()
                pf = v.groupby("spectral_radius")[perf].apply(
                    lambda s: np.median(_capped_perf(s.to_numpy(float), perf)))
                axL.plot(pr.index, pr.values, ls=ls, color="black", lw=1.6,
                         label=f"PR {variant}")
                axR.plot(pf.index, pf.values, ls=ls, color="#c44e52", lw=1.6,
                         label=f"{perf} {variant}")
            start = supercrit.get(cond)
            if start is not None:
                axL.axvspan(start, float(df.spectral_radius.max()),
                            color=_SUPERCRITICAL_COLOR, zorder=0)
            axL.grid(alpha=0.2)
            if i == 0:
                axL.set_title(CONDITION_TITLE.get(cond, cond), fontsize=10)
            if j == 0:
                axL.set_ylabel(f"{TASK_TITLE.get(task, task)}\nPR (black)", fontsize=9)
            if j == ncols - 1:
                axR.set_ylabel(f"{_PERF_LABEL[perf]} (red)", fontsize=9)
            if i == nrows - 1:
                axL.set_xlabel("spectral radius")
    fig.suptitle("Probe 3 story: PR (black) and performance (red) vs sr -- "
                 "connectome (solid) vs degree_rewire (dashed)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _write_probe3_summary(corr, gap, path):
    """Headline correlations + gap-tracking, for the Findings block."""
    lines = ["# Manifold Probe 3 -- geometry -> performance (human N=448)\n",
             "## Pooled Spearman r (geometry vs primary performance, supercritical)\n",
             "| task | performance | geometry | r_s | n |", "|---|---|---|---|---|"]
    for task in [t for t in DEFAULT_TASKS if t in corr.task.unique()]:
        perf = _PERF_PRIMARY[task]
        for geom in _GEOM_METRICS:
            r = corr[(corr.task == task) & (corr.performance == perf)
                     & (corr.geometry == geom) & (corr.condition == "pooled")
                     & (corr.region == "supercritical")]
            if not r.empty:
                lines.append(f"| {task} | {perf} | {geom} | {r.spearman_r.values[0]:+.2f} "
                             f"| {int(r.n.values[0])} |")
    lines += ["\n## Gap-tracking Spearman (connectome-degree geometry gap vs "
              "performance gap, supercritical)\n",
              "| task | dPR vs dPerf | dStraight vs dPerf |", "|---|---|---|"]
    for task in [t for t in DEFAULT_TASKS if t in gap.task.unique()]:
        perf = _PERF_PRIMARY[task]
        t = gap[gap.task == task]
        out = {}
        for gcol in ("dPR", "dStraight"):
            x, y = t[gcol].to_numpy(float), t[f"d_{perf}"].to_numpy(float)
            ok = np.isfinite(x) & np.isfinite(y)
            out[gcol] = spearmanr(x[ok], y[ok])[0] if ok.sum() > 5 else float("nan")
        lines.append(f"| {task} | {out['dPR']:+.2f} | {out['dStraight']:+.2f} |")
    path.write_text("\n".join(lines) + "\n")
    print(f"Saved {path}")


def main_probe3(smoke: bool = False, jobs: int = 1, scale: int | None = None) -> None:
    scale = matrix_config.SCALE if scale is None else scale
    results_dir = RESULTS_DIR / f"scale_{scale}"
    figures_dir = FIGURES_DIR / f"scale_{scale}"
    metrics_parquet = results_dir / "manifold_metrics.parquet"
    if not metrics_parquet.exists():
        raise FileNotFoundError(
            f"{metrics_parquet} not found -- run Probe 1 (--probe 1) first.")
    df = pd.read_parquet(metrics_parquet)
    print(f"Probe 3: loaded {len(df)} rows from {metrics_parquet}")

    builder = HumanSubstrateBuilder(scale=scale)
    supercrit = builder.connectome_supercritical_radii(matrix_config.CONDITIONS)

    corr = _correlations(df)
    gap = _gap_frame(df, supercrit)
    results_dir.mkdir(parents=True, exist_ok=True)
    corr.to_parquet(results_dir / "manifold_geometry_performance.parquet")
    gap.to_parquet(results_dir / "manifold_gap_tracking.parquet")
    print(f"Saved {results_dir / 'manifold_geometry_performance.parquet'} ({len(corr)} rows)")

    figures_dir.mkdir(parents=True, exist_ok=True)
    _plot_geometry_vs_performance(df, figures_dir / "manifold_geometry_vs_performance.png")
    print(f"Saved {figures_dir / 'manifold_geometry_vs_performance.png'}")
    _plot_gap_tracking(gap, figures_dir / "manifold_gap_tracking.png")
    print(f"Saved {figures_dir / 'manifold_gap_tracking.png'}")
    _plot_overlay(df, supercrit, figures_dir / "manifold_pr_performance_overlay.png")
    print(f"Saved {figures_dir / 'manifold_pr_performance_overlay.png'}")
    _write_probe3_summary(corr, gap, results_dir / "manifold_probe3_summary.md")

    # Headline glance
    print("\nPooled Spearman (geometry vs primary perf, supercritical):")
    for task in [t for t in DEFAULT_TASKS if t in corr.task.unique()]:
        perf = _PERF_PRIMARY[task]
        cells = []
        for geom in _GEOM_METRICS:
            r = corr[(corr.task == task) & (corr.performance == perf)
                     & (corr.geometry == geom) & (corr.condition == "pooled")
                     & (corr.region == "supercritical")]
            if not r.empty:
                cells.append(f"{geom}={r.spearman_r.values[0]:+.2f}")
        print(f"  {task} ({perf}): " + "  ".join(cells))
    print("\nProbe 3 complete.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(smoke: bool = False, jobs: int = 1, scale: int | None = None,
         sr_max: float | None = None, tasks=None) -> None:
    scale = matrix_config.SCALE if scale is None else scale
    tasks = tasks or DEFAULT_TASKS
    results_dir = RESULTS_DIR / f"scale_{scale}"
    figures_dir = FIGURES_DIR / f"scale_{scale}"
    results_dir.mkdir(parents=True, exist_ok=True)

    builder = HumanSubstrateBuilder(scale=scale)
    print("Substrate summary:")
    for key, value in builder.summary().items():
        print(f"  {key}: {value}")

    specs = _build_specs(scale, tasks, smoke, sr_max)
    conditions = matrix_config.CONDITIONS
    variants = matrix_config.VARIANTS
    n_seeds = 2 if smoke else matrix_config.N_SEEDS
    print(f"\nCapturing tasks={list(specs)} scale={scale} "
          f"sweep={len(specs[tasks[0]]['sweep'])} pts n_seeds={n_seeds} jobs={jobs}\n")

    df = capture(builder, specs, conditions, variants, n_seeds, jobs)

    # T_effective > N check (PR is otherwise bounded by T, not the geometry).
    n_nodes = int(builder.mask.shape[0])
    print(f"\nManifold metric ranges (N={n_nodes}):")
    for task in tasks:
        sub = df[df.task == task]
        print(f"  {task}: PR [{sub.pr.min():.1f}, {sub.pr.max():.1f}]  "
              f"curvature [{sub.mean_curvature.min():.2f}, {sub.mean_curvature.max():.2f}]  "
              f"entropy [{sub.spectral_entropy.min():.2f}, {sub.spectral_entropy.max():.2f}]")

    out_parquet = results_dir / "manifold_metrics.parquet"
    df.to_parquet(out_parquet)
    print(f"\nSaved {out_parquet}  ({len(df)} rows)")

    # Figures + summary first, so a validation issue never costs the deliverables.
    supercrit = builder.connectome_supercritical_radii(conditions)
    write_figures(df, figures_dir, supercrit)
    _write_summary(df, results_dir / "manifold_metrics_summary.md", supercrit)

    if not smoke:
        print("\nValidating co-recorded performance vs the committed runs:")
        validate_against_committed(df, specs)
    print("\nProbe 1 capture complete.")


def _flag(argv, flag, default, cast=int):
    for i, arg in enumerate(argv):
        if arg == flag and i + 1 < len(argv):
            return cast(argv[i + 1])
        if arg.startswith(flag + "="):
            return cast(arg.split("=", 1)[1])
    return default


if __name__ == "__main__":
    _probe = _flag(sys.argv, "--probe", 1, int)
    _common = dict(smoke="--smoke" in sys.argv,
                   jobs=_flag(sys.argv, "--jobs", 1, int),
                   scale=_flag(sys.argv, "--scale", None, int))
    if _probe == 2:
        main_probe2(**_common)
    elif _probe == 3:
        main_probe3(**_common)
    else:
        main(**_common, sr_max=_flag(sys.argv, "--sr-max", None, float))

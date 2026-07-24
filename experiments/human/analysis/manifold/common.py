"""Shared scaffolding for the human manifold-geometry probe drivers.

Task specs, spectral-radius sweep resolution, scale-tagged output dirs, the
fork-parallel cell-capture harness (shared by Probe 1 metrics and Probe 2
alignment), plotting palettes/titles, and CLI helpers.
"""

import json
import multiprocessing as mp
import time
from pathlib import Path

import numpy as np
import pandas as pd

from src.reservoir import blas  # noqa: F401  (limit BLAS threads; import after numpy)
from experiments.human import matrix_config
from experiments.human.human_mc import task_config as mc_task_config
from experiments.human.human_narma10 import task_config as narma_task_config
from experiments.human.human_lorenz import task_config as lorenz_task_config

_ANALYSIS_DIR = Path(__file__).resolve().parents[1]   # experiments/human/analysis
_ROOT = Path(__file__).resolve().parents[4]           # repo root
FIGURES_DIR = _ANALYSIS_DIR / "figures"
RESULTS_DIR = _ANALYSIS_DIR / "results"

DEFAULT_TASKS = ["mc", "narma10", "lorenz"]
# name -> (committed-results subdir, task_config module, task() args, perf columns).
TASK_DEFS = {
    "mc": ("human_mc", mc_task_config, (), ["mc"]),
    "narma10": ("human_narma10", narma_task_config, (), ["nrmse"]),
    "lorenz": ("human_lorenz", lorenz_task_config, ("vpt",), ["vpt", "climate_error"]),
}

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
CONDITION_COLOR = {"human_gaussian": "#4c72b0", "human_empirical_signed": "#dd8452",
                   "human_empirical": "#c44e52"}
SUPERCRITICAL_COLOR = "#fff3e0"
SUPERCRITICAL_SR = 1.25  # nominal supercritical threshold (fallback / pooled scope)


# ---------------------------------------------------------------------------
# Output dirs + df filters
# ---------------------------------------------------------------------------
def scale_dirs(scale: int) -> tuple[Path, Path]:
    """Scale-tagged (results_dir, figures_dir)."""
    return RESULTS_DIR / f"scale_{scale}", FIGURES_DIR / f"scale_{scale}"


def present_tasks(df: pd.DataFrame) -> list:
    return [t for t in DEFAULT_TASKS if t in df.task.unique()]


def present_conditions(df: pd.DataFrame) -> list:
    return [c for c in matrix_config.CONDITIONS if c in df.condition.unique()]


# ---------------------------------------------------------------------------
# Task specs + spectral-radius sweep resolution
# ---------------------------------------------------------------------------
def committed_results_dir(subdir: str, scale: int) -> Path:
    return _ROOT / "experiments" / "human" / subdir / "results" / f"scale_{scale}"


def resolve_sweep(subdir: str, scale: int, smoke: bool, sr_max) -> list:
    """Spectral-radius grid to capture on.

    Full runs read the grid from the task's committed ``manifest.json`` so the
    Probe 3 join and the performance-validation gate align exactly; ``--sr-max``
    overrides; ``--smoke`` uses a tiny grid.
    """
    if smoke:
        return [0.0, 0.95, 1.5]
    if sr_max is not None:
        return [round(float(sr), 6) for sr in matrix_config.spectral_sweep(sr_max)]
    manifest = committed_results_dir(subdir, scale) / "manifest.json"
    if manifest.exists():
        grid = json.loads(manifest.read_text())["spectral_radii"]
        return [round(float(sr), 6) for sr in grid]
    return [round(float(sr), 6) for sr in matrix_config.spectral_sweep(6.0)]


def build_specs(scale: int, tasks, smoke: bool, sr_max) -> dict:
    """Per-task capture spec: the evaluator, its frozen params, the reservoir
    build hyperparameters, the sweep, and the committed-results dir."""
    offset = matrix_config.INPUT_SEED_OFFSET
    specs = {}
    for name in tasks:
        subdir, module, task_args, perf = TASK_DEFS[name]
        t = module.task(*task_args)
        specs[name] = dict(
            evaluate=t["task_evaluate"],
            params=dict(t["task_params"]),
            input_scaling=t["input_scaling"],
            leak_rate=t["leak_rate"],
            input_dim=t.get("input_dim", 1),
            input_seed_offset=offset,
            perf=perf,
            sweep=resolve_sweep(subdir, scale, smoke, sr_max),
            results_dir=committed_results_dir(subdir, scale),
        )
    return specs


# ---------------------------------------------------------------------------
# Fork-parallel cell-capture harness (shared by Probe 1 and Probe 2)
# ---------------------------------------------------------------------------
# Read-only worker state for the fork path (set in the parent before the pool
# forks; children inherit it copy-on-write, so the builder is never pickled --
# only the small cell tuples and returned rows cross the process boundary).
_WORKER: dict = {}


def _progress(i: int, total: int, t0: float, eta: bool = True) -> None:
    if i % 20 == 0 or i == total:
        elapsed = time.time() - t0
        msg = f"  {i}/{total} cells ({100 * i / total:.0f}%) elapsed={elapsed:.0f}s"
        if eta:
            msg += f" eta={elapsed * (total - i) / max(i, 1):.0f}s"
        print(msg, flush=True)


def _fork_worker(cell):
    """Fork-worker entry: pin BLAS to one thread and run the cell function on the
    inherited worker state."""
    from threadpoolctl import threadpool_limits
    with threadpool_limits(limits=1):
        return _WORKER["cell_fn"](cell, _WORKER["state"])


def run_cells(cells, cell_fn, state, jobs, label) -> pd.DataFrame:
    """Run ``cell_fn(cell, state) -> rows`` over ``cells``, sequential or across
    ``jobs`` fork workers (1 BLAS thread each). Returns the concatenated rows as a
    DataFrame, in input order."""
    total = len(cells)
    t0 = time.time()
    rows = []
    if jobs and jobs > 1:
        _WORKER.clear()
        _WORKER.update(cell_fn=cell_fn, state=state)
        print(f"Parallel {label}: {total} cells across {jobs} fork workers "
              f"(1 BLAS thread each).", flush=True)
        ctx = mp.get_context("fork")
        with ctx.Pool(processes=jobs) as pool:
            for i, cell_rows in enumerate(pool.imap(_fork_worker, cells), start=1):
                rows.extend(cell_rows)
                _progress(i, total, t0)
    else:
        for i, cell in enumerate(cells, start=1):
            rows.extend(cell_fn(cell, state))
            _progress(i, total, t0, eta=False)
    print(f"{label} done in {time.time() - t0:.0f}s ({total} cells).")
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def flag(argv, name, default, cast=int):
    """Parse ``--name V`` / ``--name=V`` from argv (cast applied); default if absent."""
    for i, arg in enumerate(argv):
        if arg == name and i + 1 < len(argv):
            return cast(argv[i + 1])
        if arg.startswith(name + "="):
            return cast(arg.split("=", 1)[1])
    return default

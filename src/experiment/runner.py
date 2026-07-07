"""Generic experiment runner: connectome x null-ladder x spectral-radius matrix.

Task-agnostic. Loops conditions x variants x spectral radii x seeds; for each
cell it weights the substrate (via the connectome's ``SubstrateBuilder``),
builds a reservoir at the target spectral radius, and scores it with the task's
``evaluate()`` (injected through ``cfg.task_evaluate``). Writes
``results.parquet``, ``null_diagnostics.parquet`` and ``manifest.json``.

With ``jobs > 1`` the (condition, variant, seed) cells are evaluated in parallel
across forked worker processes (each pinned to one BLAS thread, so ``jobs``
workers fill ``jobs`` cores). Results are BYTE-IDENTICAL to the sequential path:
every cell is fully seeded (mask/weights/Win/task-input all derive from the
construction seed), and rows are collected in the same nested order. Parallel
mode does not support ``checkpoint_path`` (checkpointing stays on the jobs=1
path, e.g. the long closed-loop Lorenz run).
"""

import json
import os
import time
import multiprocessing as mp
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from threadpoolctl import threadpool_limits

from src.reservoir.build import build_from_adjacency

# Shared read-only worker state for the parallel path. Set in the parent before
# the pool forks; children inherit it copy-on-write, so the (possibly large)
# builder is never pickled per task -- only the small (condition, variant, seed)
# tuples and the returned rows cross the process boundary.
_WORKER: dict = {}


def _evaluate_cell(builder, cfg, condition, variant, seed, spectral_radii):
    """Evaluate one (condition, variant, seed) cell across all spectral radii.

    Weights the substrate once, then sweeps the radii (the rescale happens in
    ``build_from_adjacency``). Returns the list of per-sr result rows. Shared by
    the sequential and parallel paths so the two produce identical rows.
    """
    weighted = builder.weighted(condition, variant, seed)
    # Optional routing hooks (the I/O-routing thread). A builder MAY route the
    # input to a subset of units (``input_nodes``) and/or supply per-cell task
    # kwargs (``cell_task_kwargs`` -- e.g. this cell's readout apertures). Both are
    # (variant, seed)-dependent so they are resolved once per cell, outside the sr
    # loop. Every other builder defines neither -> ``input_nodes=None`` (dense Win,
    # byte-identical) and no extra task kwargs, so all committed tasks are unchanged.
    input_nodes = (builder.input_nodes(variant, seed)
                   if hasattr(builder, "input_nodes") else None)
    cell_kwargs = (builder.cell_task_kwargs(condition, variant, seed)
                   if hasattr(builder, "cell_task_kwargs") else {})
    rows = []
    for spectral_radius in spectral_radii:
        reservoir = build_from_adjacency(
            weighted_adjacency=weighted,
            target_spectral_radius=spectral_radius,
            leak_rate=cfg.leak_rate,
            input_scaling=cfg.input_scaling,
            seed=seed,
            input_dim=cfg.input_dim,
            input_nodes=input_nodes,
        )
        metrics = cfg.task_evaluate(
            reservoir,
            seed=seed + cfg.input_seed_offset,
            **cfg.task_params,
            **cell_kwargs,
        )
        row = dict(
            condition=condition,
            variant=variant,
            rung=cfg.variant_rung.get(variant, -1),
            spectral_radius=spectral_radius,
            seed=seed,
        )
        row[cfg.metric] = metrics[cfg.metric]
        for field in cfg.extra_metric_fields:
            row[field] = metrics[field]
        rows.append(row)
    return rows


def _run_cell_worker(task):
    """Parallel-worker entry: read the forked builder/cfg from ``_WORKER``, pin
    BLAS to one thread, and return ``(rows, this-cell's diagnostics)``."""
    condition, variant, seed = task
    builder, cfg = _WORKER["builder"], _WORKER["cfg"]
    # Clear so we return ONLY the null-validation records this cell generates.
    # (Across workers the same (variant, seed) mask is rebuilt by every condition
    # of that topology -> duplicates, deduped once collected in the parent.)
    builder.diagnostics.clear()
    with threadpool_limits(limits=1):
        rows = _evaluate_cell(builder, cfg, condition, variant, seed,
                              _WORKER["spectral_radii"])
    return rows, list(builder.diagnostics)


def _run_parallel(builder, cfg, conditions, variants, spectral_radii, n_seeds,
                  jobs, t0):
    """Fork ``jobs`` workers over the (condition, variant, seed) grid. Returns
    ``(rows_in_nested_order, deduped_diagnostics)``."""
    tasks = [(c, v, s) for c in conditions for v in variants for s in range(n_seeds)]
    total = len(tasks)
    _WORKER.update(builder=builder, cfg=cfg, spectral_radii=spectral_radii)
    print(f"Parallel grid: {total} cells x {len(spectral_radii)} sr across "
          f"{jobs} fork workers (1 BLAS thread each).", flush=True)

    rows, diag_records = [], []
    ctx = mp.get_context("fork")
    # imap preserves input order -> rows land in the same nested order as the
    # sequential loop (condition, variant, seed, then sr within each cell).
    with ctx.Pool(processes=jobs) as pool:
        for i, (cell_rows, cell_diags) in enumerate(
                pool.imap(_run_cell_worker, tasks), start=1):
            rows.extend(cell_rows)
            diag_records.extend(cell_diags)
            if i % 10 == 0 or i == total:
                elapsed = time.time() - t0
                eta = elapsed * (total - i) / max(i, 1)
                print(f"  {i}/{total} cells ({100 * i / total:.0f}%) "
                      f"elapsed={elapsed:.0f}s eta={eta:.0f}s", flush=True)

    # Dedup diagnostics: keep one record per (topology, variant, seed, property).
    seen, deduped = set(), []
    for d in diag_records:
        key = (d.get("topology"), d.get("variant"), d.get("seed"), d.get("property"))
        if key not in seen:
            seen.add(key)
            deduped.append(d)
    return rows, deduped


def _run_sequential(builder, cfg, conditions, variants, spectral_radii, n_seeds,
                    checkpoint_path, t0):
    """Sequential grid with opt-in resumable checkpointing. Returns
    ``(rows, builder.diagnostics)``."""
    # Optional resumable checkpointing (opt-in; None -> unchanged behaviour).
    # After each (condition, variant, seed) finishes its spectral-radius sweep,
    # the accumulated rows are flushed atomically to ``checkpoint_path``; on a
    # restart those cells are skipped. Intended for the long closed-loop Lorenz
    # run, so a hard interruption costs at most one cell's sweep, not the whole run.
    rows, done = [], set()
    if checkpoint_path is not None and Path(checkpoint_path).exists():
        prev = pd.read_parquet(checkpoint_path)
        rows = prev.to_dict("records")
        done = set(zip(prev.condition, prev.variant, prev.seed))
        print(f"Resuming from checkpoint {checkpoint_path}: {len(done)} "
              f"(condition,variant,seed) cells already complete ({len(rows)} rows).")

    def _flush_checkpoint():
        if checkpoint_path is None:
            return
        Path(checkpoint_path).parent.mkdir(parents=True, exist_ok=True)
        tmp = f"{checkpoint_path}.tmp"
        pd.DataFrame(rows).to_parquet(tmp)
        os.replace(tmp, checkpoint_path)  # atomic swap: never a half-written file

    total = len(conditions) * len(variants) * len(spectral_radii) * n_seeds
    n_done = len(rows)
    n_this_session = 0

    for condition in conditions:
        for variant in variants:
            for seed in range(n_seeds):
                if (condition, variant, seed) in done:
                    continue
                rows.extend(_evaluate_cell(builder, cfg, condition, variant, seed,
                                           spectral_radii))
                n_done += len(spectral_radii)
                n_this_session += len(spectral_radii)
                if n_done % 100 < len(spectral_radii) or n_done == total:
                    elapsed = time.time() - t0
                    eta = elapsed * (total - n_done) / max(n_this_session, 1)
                    print(f"  {n_done}/{total} ({100 * n_done / total:.0f}%) "
                          f"elapsed={elapsed:.0f}s eta={eta:.0f}s", flush=True)
                _flush_checkpoint()  # cell complete -> safe resume point

    return rows, list(builder.diagnostics)


def run_matrix(builder, cfg, conditions=None, variants=None,
               spectral_radii=None, n_seeds=None, checkpoint_path=None,
               jobs=1) -> pd.DataFrame:
    conditions = conditions or cfg.conditions
    variants = variants or cfg.variants
    spectral_radii = spectral_radii or cfg.spectral_radii
    n_seeds = n_seeds if n_seeds is not None else cfg.n_seeds

    print("Substrate summary:")
    for key, value in builder.summary().items():
        print(f"  {key}: {value}")
    print(f"\nInhibitory neurons: {builder.sign_coverage['n_inhibitory']} "
          f"({builder.sign_coverage['inhibitory_labels']})\n")

    t0 = time.time()
    if jobs and jobs > 1:
        if checkpoint_path is not None:
            raise ValueError("checkpoint_path is not supported with jobs > 1; "
                             "use jobs=1 to enable checkpointing.")
        rows, diag_records = _run_parallel(
            builder, cfg, conditions, variants, spectral_radii, n_seeds, jobs, t0)
    else:
        rows, diag_records = _run_sequential(
            builder, cfg, conditions, variants, spectral_radii, n_seeds,
            checkpoint_path, t0)

    elapsed = time.time() - t0
    print(f"\nMatrix done in {elapsed:.0f}s ({elapsed/60:.1f} min)")

    results = pd.DataFrame(rows)
    diagnostics = pd.DataFrame(diag_records)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "n_evaluations": len(results),
        "elapsed_seconds": round(elapsed, 1),
        "jobs": jobs,
        "conditions": conditions,
        "variants": variants,
        "spectral_radii": spectral_radii,
        "n_seeds": n_seeds,
        "substrate_summary": builder.summary(),
        "config": cfg.manifest_dict(),
    }

    cfg.results_dir.mkdir(parents=True, exist_ok=True)
    results.to_parquet(cfg.results_parquet)
    if not diagnostics.empty:
        diagnostics.to_parquet(cfg.null_diagnostics_parquet)
    with open(cfg.manifest_json, "w") as fh:
        json.dump(manifest, fh, indent=2)

    print(f"Saved {cfg.results_parquet}")
    print(f"Saved {cfg.null_diagnostics_parquet}")
    print(f"Saved {cfg.manifest_json}")

    _matched_sr_glance(results, cfg, conditions, variants)
    return results


def _matched_sr_glance(results, cfg, conditions, variants) -> None:
    """Sanity glance at MATCHED spectral radius (canonical vs supercritical) --
    the meaningful comparison is connectome vs null at the same sr."""
    metric = cfg.metric
    mean_by = (results.groupby(["condition", "variant", "spectral_radius"])[metric]
               .mean().reset_index())
    srs = sorted(results.spectral_radius.unique())
    canonical_sr = min(srs, key=lambda s: abs(s - 0.95))
    supercritical_sr = min(srs, key=lambda s: abs(s - 1.5))
    print(f"\nMean {metric} at matched sr "
          f"(canonical≈{canonical_sr}, supercritical≈{supercritical_sr}):")
    for condition in conditions:
        print(f"  [{condition}]")
        for variant in variants:
            row_c = mean_by[(mean_by.condition == condition)
                            & (mean_by.variant == variant)
                            & (mean_by.spectral_radius == canonical_sr)]
            row_s = mean_by[(mean_by.condition == condition)
                            & (mean_by.variant == variant)
                            & (mean_by.spectral_radius == supercritical_sr)]
            if not row_c.empty and not row_s.empty:
                print(f"    {variant:18s}: canonical={row_c[metric].values[0]:.3f}  "
                      f"supercritical={row_s[metric].values[0]:.3f}")

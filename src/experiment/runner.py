"""Generic experiment runner: connectome x null-ladder x spectral-radius matrix.

Task-agnostic. Loops conditions x variants x spectral radii x seeds; for each
cell it weights the substrate (via the connectome's ``SubstrateBuilder``),
builds a reservoir at the target spectral radius, and scores it with the task's
``evaluate()`` (injected through ``cfg.task_evaluate``). Writes
``results.parquet``, ``null_diagnostics.parquet`` and ``manifest.json``.
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.reservoir.build import build_from_adjacency


def run_matrix(builder, cfg, conditions=None, variants=None,
               spectral_radii=None, n_seeds=None, checkpoint_path=None) -> pd.DataFrame:
    conditions = conditions or cfg.conditions
    variants = variants or cfg.variants
    spectral_radii = spectral_radii or cfg.spectral_radii
    n_seeds = n_seeds if n_seeds is not None else cfg.n_seeds

    print("Substrate summary:")
    for key, value in builder.summary().items():
        print(f"  {key}: {value}")
    print(f"\nInhibitory neurons: {builder.sign_coverage['n_inhibitory']} "
          f"({builder.sign_coverage['inhibitory_labels']})\n")

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
    t0 = time.time()

    for condition in conditions:
        for variant in variants:
            for seed in range(n_seeds):
                if (condition, variant, seed) in done:
                    continue
                # Weight the substrate once per (condition, variant, seed);
                # reuse across the spectral-radius sweep (rescale happens in
                # build_from_adjacency).
                weighted = builder.weighted(condition, variant, seed)
                for spectral_radius in spectral_radii:
                    reservoir = build_from_adjacency(
                        weighted_adjacency=weighted,
                        target_spectral_radius=spectral_radius,
                        leak_rate=cfg.leak_rate,
                        input_scaling=cfg.input_scaling,
                        seed=seed,
                        input_dim=cfg.input_dim,
                    )
                    metrics = cfg.task_evaluate(
                        reservoir,
                        seed=seed + cfg.input_seed_offset,
                        **cfg.task_params,
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
                    n_done += 1
                    n_this_session += 1
                    if n_done % 100 == 0 or n_done == total:
                        elapsed = time.time() - t0
                        eta = elapsed * (total - n_done) / max(n_this_session, 1)
                        print(f"  {n_done}/{total} ({100*n_done/total:.0f}%) "
                              f"elapsed={elapsed:.0f}s eta={eta:.0f}s", flush=True)
                _flush_checkpoint()  # cell complete -> safe resume point

    elapsed = time.time() - t0
    print(f"\nMatrix done in {elapsed:.0f}s ({elapsed/60:.1f} min)")

    results = pd.DataFrame(rows)
    diagnostics = pd.DataFrame(builder.diagnostics)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "n_evaluations": len(results),
        "elapsed_seconds": round(elapsed, 1),
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

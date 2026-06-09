"""Run the C. elegans NARMA-10 bridge matrix.

3 conditions (v2a, v2b, v2d) x 6 variants (connectome + rungs 0-4) x the
spectral-radius sweep x seeds. Each cell builds a reservoir and scores it on
NARMA-10; results are written to ``results/results.parquet``.

Usage:
    python notebooks/celegans_narma10/run_experiment.py            # full run
    python notebooks/celegans_narma10/run_experiment.py --smoke    # tiny check
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.reservoir import blas  # noqa: F401  (limit BLAS threads; import early)

import json
import time
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from src.reservoir.build import build_from_adjacency
from src.tasks.narma import evaluate as evaluate_narma

import config
from substrates import SubstrateBuilder


def run(conditions=None, variants=None, spectral_radii=None, n_seeds=None) -> pd.DataFrame:
    conditions = conditions or config.CONDITIONS
    variants = variants or config.VARIANTS
    spectral_radii = spectral_radii or config.SPECTRAL_RADII
    n_seeds = n_seeds if n_seeds is not None else config.N_SEEDS

    builder = SubstrateBuilder()
    print("Substrate summary:")
    for key, value in builder.summary().items():
        print(f"  {key}: {value}")
    print(f"\nInhibitory (v2d) neurons: {builder.sign_coverage['n_inhibitory']} "
          f"({builder.sign_coverage['inhibitory_labels']})\n")

    rows = []
    total = len(conditions) * len(variants) * len(spectral_radii) * n_seeds
    n_done = 0
    t0 = time.time()

    for condition in conditions:
        for variant in variants:
            for seed in range(n_seeds):
                # Weight the substrate once per (condition, variant, seed);
                # reuse across the spectral-radius sweep (rescale happens in
                # build_from_adjacency).
                weighted = builder.weighted(condition, variant, seed)
                for spectral_radius in spectral_radii:
                    reservoir = build_from_adjacency(
                        weighted_adjacency=weighted,
                        target_spectral_radius=spectral_radius,
                        leak_rate=config.LEAK_RATE,
                        input_scaling=config.INPUT_SCALING,
                        seed=seed,
                    )
                    metrics = evaluate_narma(
                        reservoir,
                        seed=seed + config.INPUT_SEED_OFFSET,
                        **config.NARMA_PARAMS,
                    )
                    rows.append(dict(
                        condition=condition,
                        variant=variant,
                        rung=config.VARIANT_RUNG.get(variant, -1),
                        spectral_radius=spectral_radius,
                        seed=seed,
                        nrmse=metrics["nrmse"],
                        n_rejected_inputs=metrics["n_rejected_inputs"],
                    ))
                    n_done += 1
                    if n_done % 100 == 0 or n_done == total:
                        elapsed = time.time() - t0
                        eta = elapsed * (total - n_done) / max(n_done, 1)
                        print(f"  {n_done}/{total} ({100*n_done/total:.0f}%) "
                              f"elapsed={elapsed:.0f}s eta={eta:.0f}s", flush=True)

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
        "config": config.as_dict(),
    }

    config.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    results.to_parquet(config.RESULTS_PARQUET)
    if not diagnostics.empty:
        diagnostics.to_parquet(config.NULL_DIAGNOSTICS_PARQUET)
    with open(config.MANIFEST_JSON, "w") as fh:
        json.dump(manifest, fh, indent=2)

    print(f"Saved {config.RESULTS_PARQUET}")
    print(f"Saved {config.NULL_DIAGNOSTICS_PARQUET}")
    print(f"Saved {config.MANIFEST_JSON}")

    # Quick sanity glance at MATCHED spectral radius (canonical vs
    # supercritical) -- the meaningful comparison is connectome vs null at the
    # same sr, not each variant at its own optimum.
    mean_by = (results.groupby(["condition", "variant", "spectral_radius"])["nrmse"]
               .mean().reset_index())
    srs = sorted(results.spectral_radius.unique())
    canonical_sr = min(srs, key=lambda s: abs(s - 0.95))
    supercritical_sr = min(srs, key=lambda s: abs(s - 1.5))
    print(f"\nMean NRMSE at matched sr "
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
                print(f"    {variant:18s}: canonical={row_c.nrmse.values[0]:.3f}  "
                      f"supercritical={row_s.nrmse.values[0]:.3f}")
    return results


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        run(spectral_radii=[0.0, 0.95, 1.5], n_seeds=2)
    else:
        run()

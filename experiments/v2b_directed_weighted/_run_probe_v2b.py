"""v2b supercritical probe — mirrors v2c's design with v2b's directed + empirical-weight pipeline.

Two conditions: connectome, degree_rewire (directed).
Three supercritical spectral radii: {1.25, 1.50, 1.75}.
Two weight transforms: sqrt, raw.
50 seeds.

2 conditions x 3 sr x 2 transforms x 50 seeds = 600 evaluations.

Same seed convention as v2a/v2c probes: construction seed used for mask
generation, weight sampling, and reservoir input projection; the MC
input stream uses ``seed + 1000``.

Saves probe_v2b_supercritical.parquet alongside this script with columns:
condition, spectral_radius, seed, mc, weight_transform.
"""

from src.reservoir import blas  # noqa: F401

import time
from pathlib import Path

import numpy as np
import pandas as pd

from src.connectomes.celegans_cook2019 import load as load_connectome
from src.nulls import degree_rewire
from src.reservoir.weights import apply_weight_scheme
from src.reservoir.build import build_from_adjacency
from src.tasks.memory_capacity import evaluate as evaluate_mc

MC_PARAMS = dict(T=3000, warmup=500, max_lag=50, ridge_alpha=1e-6)
INPUT_SCALING = 1.0
LEAK_RATE = 1.0
MC_INPUT_SEED_OFFSET = 1000

PROBE_SPECTRAL_RADII = [1.25, 1.50, 1.75]
N_SEEDS = 50
TRANSFORMS = ["sqrt", "raw"]
CONDITIONS = ["connectome", "degree_rewire"]

OUT_DIR = Path(__file__).resolve().parent
PROBE_PARQUET = OUT_DIR / "probe_v2b_supercritical.parquet"


def main():
    connectome = load_connectome("directed_weighted_chemical")
    raw_adjacency = connectome.adjacency
    binary_directed_mask = (raw_adjacency != 0).astype(float)

    # Pre-compute the weighted adjacency and empirical pool for each transform.
    transformed = {}
    for tag in TRANSFORMS:
        if tag == "sqrt":
            w = np.where(raw_adjacency > 0, np.sqrt(raw_adjacency), 0.0)
        elif tag == "raw":
            w = raw_adjacency.astype(float).copy()
        else:
            raise ValueError(tag)
        transformed[tag] = {
            "weighted_adjacency": w,
            "empirical_pool": w[w != 0].copy(),
        }

    def make_mask(condition, seed):
        if condition == "connectome":
            return binary_directed_mask.copy()
        if condition == "degree_rewire":
            return degree_rewire.generate(binary_directed_mask, seed=seed, directed=True)
        raise ValueError(condition)

    rows = []
    t0 = time.time()
    total = len(TRANSFORMS) * len(CONDITIONS) * len(PROBE_SPECTRAL_RADII) * N_SEEDS
    n_done = 0
    for transform_tag in TRANSFORMS:
        connectome_weighted = transformed[transform_tag]["weighted_adjacency"]
        empirical_pool = transformed[transform_tag]["empirical_pool"]
        for condition in CONDITIONS:
            for spectral_radius in PROBE_SPECTRAL_RADII:
                for seed in range(N_SEEDS):
                    if condition == "connectome":
                        condition_weighted = connectome_weighted
                    else:
                        mask = make_mask(condition, seed)
                        condition_weighted = apply_weight_scheme(
                            mask,
                            "asymmetric_empirical",
                            seed=seed,
                            empirical_weights=empirical_pool,
                        )
                    reservoir = build_from_adjacency(
                        weighted_adjacency=condition_weighted,
                        target_spectral_radius=spectral_radius,
                        leak_rate=LEAK_RATE,
                        input_scaling=INPUT_SCALING,
                        seed=seed,
                    )
                    metrics = evaluate_mc(
                        reservoir,
                        seed=seed + MC_INPUT_SEED_OFFSET,
                        input_scaling=INPUT_SCALING,
                        **MC_PARAMS,
                    )
                    rows.append(dict(
                        condition=condition,
                        spectral_radius=spectral_radius,
                        seed=seed,
                        mc=metrics["mc"],
                        weight_transform=transform_tag,
                    ))
                    n_done += 1
                    if n_done % 50 == 0:
                        elapsed = time.time() - t0
                        pct = 100.0 * n_done / total
                        eta = elapsed * (total - n_done) / max(n_done, 1)
                        print(
                            f"  {n_done}/{total} ({pct:.0f}%) "
                            f"elapsed={elapsed:.1f}s eta={eta:.1f}s",
                            flush=True,
                        )

    elapsed = time.time() - t0
    print(f"Probe done in {elapsed:.1f} s ({elapsed/60:.2f} min)")

    df = pd.DataFrame(rows)
    df.to_parquet(PROBE_PARQUET)
    print(f"Saved {PROBE_PARQUET}")


if __name__ == "__main__":
    main()

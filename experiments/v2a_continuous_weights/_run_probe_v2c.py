"""v2c probe runner — rung-3 (clustering) + rung-4 (modularity) nulls.

Four conditions: connectome, degree_rewire, clustering_rewire, modularity_rewire.
Three supercritical spectral radii: {1.25, 1.50, 1.75}.
50 seeds. Saves probe_v2c.parquet alongside this script.

The Louvain partition for modularity_rewire is pre-computed once on the
connectome (louvain_seed=0) and reused across all 50 rewire seeds — this
keeps the null's *definition* fixed across seeds.
"""

from src.reservoir import blas  # noqa: F401

import time
import warnings
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

from src.connectomes.celegans_cook2019 import load as load_connectome
from src.nulls import (
    degree_rewire,
    clustering_rewire,
    modularity_rewire,
)
from src.nulls.validation import validate_null
from src.reservoir.weights import apply_weight_scheme
from src.reservoir.build import build_from_adjacency
from src.tasks.memory_capacity import evaluate as evaluate_mc

MC_PARAMS = dict(T=3000, warmup=500, max_lag=50, ridge_alpha=1e-6)
INPUT_SCALING = 1.0
LEAK_RATE = 1.0
MC_INPUT_SEED_OFFSET = 1000

PROBE_SPECTRAL_RADII = [1.25, 1.50, 1.75]
N_SEEDS = 50
LOUVAIN_SEED = 0

CONDITIONS = ["connectome", "degree_rewire", "clustering_rewire", "modularity_rewire"]

OUT_DIR = Path(__file__).resolve().parent
PROBE_PARQUET = OUT_DIR / "probe_v2c.parquet"


def main():
    connectome = load_connectome("binary_undirected_chemical")
    adjacency = connectome.adjacency

    graph = nx.from_numpy_array(adjacency)
    louvain_partition = nx.community.louvain_communities(graph, seed=LOUVAIN_SEED)
    print(
        f"Louvain partition (seed={LOUVAIN_SEED}): "
        f"{len(louvain_partition)} communities, "
        f"sizes={sorted([len(c) for c in louvain_partition], reverse=True)}"
    )

    diagnostics_rows = []

    def make_mask(condition: str, seed: int) -> np.ndarray:
        if condition == "connectome":
            return adjacency.copy()
        if condition == "degree_rewire":
            return degree_rewire.generate(adjacency, seed=seed)
        if condition == "clustering_rewire":
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                mask, diag = clustering_rewire.generate(
                    adjacency, seed=seed, tolerance=0.05, return_diagnostics=True
                )
            diag = {"condition": condition, "seed": seed, **diag}
            diagnostics_rows.append(diag)
            cluster_check = validate_null(
                adjacency, mask, "clustering", tolerance=0.05
            )
            assert cluster_check["preserved"], (
                f"clustering_rewire seed={seed}: clustering not preserved within 5% "
                f"(expected={cluster_check['expected']:.4f}, "
                f"actual={cluster_check['actual']:.4f})"
            )
            return mask
        if condition == "modularity_rewire":
            mask, diag = modularity_rewire.generate(
                adjacency,
                seed=seed,
                community_partition=louvain_partition,
                return_diagnostics=True,
            )
            diag = {"condition": condition, "seed": seed, **diag}
            diagnostics_rows.append(diag)
            mod_check = validate_null(
                adjacency,
                mask,
                "modularity",
                tolerance=0.01,
                community_partition=louvain_partition,
            )
            assert mod_check["preserved"], (
                f"modularity_rewire seed={seed}: Q not preserved within 0.01 "
                f"(expected={mod_check['expected']:.4f}, "
                f"actual={mod_check['actual']:.4f})"
            )
            return mask
        raise ValueError(condition)

    rows = []
    t0 = time.time()
    total = len(CONDITIONS) * len(PROBE_SPECTRAL_RADII) * N_SEEDS
    n_done = 0
    for condition in CONDITIONS:
        for spectral_radius in PROBE_SPECTRAL_RADII:
            for seed in range(N_SEEDS):
                mask = make_mask(condition, seed)
                weighted = apply_weight_scheme(
                    mask, "symmetric_gaussian", seed=seed
                )
                reservoir = build_from_adjacency(
                    weighted_adjacency=weighted,
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
                rows.append(
                    dict(
                        condition=condition,
                        spectral_radius=spectral_radius,
                        seed=seed,
                        mc=metrics["mc"],
                    )
                )
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

    if diagnostics_rows:
        diag_df = pd.DataFrame(diagnostics_rows)
        print("\nNull-generation diagnostics (mean over 50 seeds):")
        for condition in ["clustering_rewire", "modularity_rewire"]:
            sub = diag_df[diag_df["condition"] == condition]
            if not sub.empty:
                print(
                    f"  {condition}: acceptance_rate "
                    f"mean={sub['acceptance_rate'].mean():.4f} "
                    f"min={sub['acceptance_rate'].min():.4f} "
                    f"max={sub['acceptance_rate'].max():.4f}"
                )


if __name__ == "__main__":
    main()

"""Stage 7 probe runner — kept as inline-equivalent code, executed once outside notebook.

Re-runs connectome vs degree_rewire at sr in {1.25, 1.50, 1.75} with n_seeds=50,
saves probe_supercritical.parquet alongside this script.
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

OUT_DIR = Path(__file__).resolve().parent
PROBE_PARQUET = OUT_DIR / "probe_supercritical.parquet"


def main():
    connectome = load_connectome("binary_undirected_chemical")

    def make_mask(condition, seed):
        if condition == "connectome":
            return connectome.adjacency.copy()
        if condition == "degree_rewire":
            return degree_rewire.generate(connectome.adjacency, seed=seed)
        raise ValueError(condition)

    rows = []
    t0 = time.time()
    total = 2 * len(PROBE_SPECTRAL_RADII) * N_SEEDS
    n_done = 0
    for condition in ["connectome", "degree_rewire"]:
        for spectral_radius in PROBE_SPECTRAL_RADII:
            for seed in range(N_SEEDS):
                mask = make_mask(condition, seed)
                weighted = apply_weight_scheme(mask, "symmetric_gaussian", seed=seed)
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
                rows.append(dict(
                    condition=condition,
                    spectral_radius=spectral_radius,
                    seed=seed,
                    mc=metrics["mc"],
                ))
                n_done += 1
                if n_done % 25 == 0:
                    elapsed = time.time() - t0
                    print(f"  {n_done}/{total} ({elapsed:.1f}s)", flush=True)
    elapsed = time.time() - t0
    print(f"Probe done in {elapsed:.1f} s ({elapsed/60:.2f} min)")

    df = pd.DataFrame(rows)
    df.to_parquet(PROBE_PARQUET)
    print(f"Saved {PROBE_PARQUET}")

    # Permutation test
    perm_rng = np.random.default_rng(20240517)
    print("\nPermutation test (10,000 permutations per sr, two-sided):")
    print(f"{'sr':>6s}  {'conn mean':>10s}  {'conn std':>9s}  {'rew mean':>9s}  {'rew std':>8s}  {'Delta':>8s}  {'SE':>7s}  {'p-value':>8s}")
    for sr in PROBE_SPECTRAL_RADII:
        sub_c = df[(df["condition"] == "connectome") & (df["spectral_radius"] == sr)]["mc"].values
        sub_r = df[(df["condition"] == "degree_rewire") & (df["spectral_radius"] == sr)]["mc"].values
        observed_delta = float(sub_c.mean() - sub_r.mean())
        pooled = np.concatenate([sub_c, sub_r])
        n_c = len(sub_c)
        n_perm = 10000
        perm_deltas = np.zeros(n_perm)
        for i in range(n_perm):
            permuted = perm_rng.permutation(pooled)
            perm_deltas[i] = permuted[:n_c].mean() - permuted[n_c:].mean()
        p = float((np.abs(perm_deltas) >= abs(observed_delta) - 1e-12).mean())
        pooled_se = float(np.sqrt(sub_c.var(ddof=1) / n_c + sub_r.var(ddof=1) / len(sub_r)))
        print(f"{sr:6.2f}  {sub_c.mean():10.4f}  {sub_c.std(ddof=1):9.4f}  {sub_r.mean():9.4f}  {sub_r.std(ddof=1):8.4f}  {observed_delta:+8.4f}  {pooled_se:7.4f}  {p:8.4f}")


if __name__ == "__main__":
    main()

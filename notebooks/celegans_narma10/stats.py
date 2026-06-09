"""Statistics for the NARMA-10 bridge: connectome vs each null.

For every (condition, spectral_radius), compare the connectome's seed-wise
NRMSE against each null variant with a two-sided permutation test, Holm-correct
across the five nulls, and report Cohen's d on the *performance* direction.

NRMSE is lower-is-better, so Cohen's d is defined as

    d = (mean_null_nrmse - mean_connectome_nrmse) / pooled_sd

i.e. d > 0 means the connectome BEATS the null (lower NRMSE). This matches the
sign convention of the memory-capacity d-values (connectome better => positive),
so the two tasks read the same way despite NRMSE and MC pointing oppositely.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd

import config


def cohens_d(connectome: np.ndarray, null: np.ndarray) -> float:
    """Cohen's d on the performance direction (positive => connectome better)."""
    n1, n2 = len(connectome), len(null)
    if n1 < 2 or n2 < 2:
        return float("nan")
    pooled_var = ((n1 - 1) * np.var(connectome, ddof=1)
                  + (n2 - 1) * np.var(null, ddof=1)) / (n1 + n2 - 2)
    pooled_sd = np.sqrt(pooled_var)
    if pooled_sd < 1e-12:
        return 0.0
    return float((np.mean(null) - np.mean(connectome)) / pooled_sd)


def permutation_pvalue(connectome: np.ndarray, null: np.ndarray,
                       n_permutations: int, rng: np.random.Generator) -> float:
    """Two-sided permutation test on the difference in means (unpaired)."""
    observed = abs(np.mean(connectome) - np.mean(null))
    pooled = np.concatenate([connectome, null])
    n1 = len(connectome)
    count = 0
    for _ in range(n_permutations):
        rng.shuffle(pooled)
        diff = abs(np.mean(pooled[:n1]) - np.mean(pooled[n1:]))
        if diff >= observed - 1e-12:
            count += 1
    # +1 smoothing so p is never exactly zero.
    return (count + 1) / (n_permutations + 1)


def holm(pvalues: list[float]) -> list[float]:
    """Holm-Bonferroni step-down correction. Returns adjusted p-values."""
    m = len(pvalues)
    order = np.argsort(pvalues)
    adjusted = [0.0] * m
    running_max = 0.0
    for rank, idx in enumerate(order):
        val = (m - rank) * pvalues[idx]
        running_max = max(running_max, val)
        adjusted[idx] = min(running_max, 1.0)
    return adjusted


def compute_stats(results: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(config.PERMUTATION_SEED)
    rows = []
    for condition in sorted(results.condition.unique()):
        cond_df = results[results.condition == condition]
        for sr in sorted(cond_df.spectral_radius.unique()):
            sr_df = cond_df[cond_df.spectral_radius == sr]
            connectome = sr_df[sr_df.variant == "connectome"].sort_values("seed").nrmse.values
            family = []
            for variant in config.NULL_VARIANTS:
                null = sr_df[sr_df.variant == variant].sort_values("seed").nrmse.values
                if len(connectome) == 0 or len(null) == 0:
                    continue
                d = cohens_d(connectome, null)
                p = permutation_pvalue(connectome, null, config.N_PERMUTATIONS, rng)
                family.append(dict(
                    condition=condition, spectral_radius=sr, null_variant=variant,
                    rung=config.VARIANT_RUNG[variant],
                    mean_connectome_nrmse=float(np.mean(connectome)),
                    mean_null_nrmse=float(np.mean(null)),
                    cohens_d=d, p_raw=p,
                ))
            if family:
                p_holm = holm([row["p_raw"] for row in family])
                for row, adj in zip(family, p_holm):
                    row["p_holm"] = adj
                    row["significant"] = bool(adj < config.ALPHA)
                rows.extend(family)
    return pd.DataFrame(rows)


def print_summary(stats: pd.DataFrame) -> None:
    """Print the headline: connectome vs degree_rewire in the supercritical region."""
    print("\n=== Connectome vs degree_rewire (rung 2) in the supercritical region ===")
    print("(Cohen's d > 0 => connectome lower NRMSE => better)")
    sub = stats[(stats.null_variant == "degree_rewire")
                & (stats.spectral_radius.isin(config.SUPERCRITICAL_RADII))]
    for condition in config.CONDITIONS:
        cond = sub[sub.condition == condition].sort_values("spectral_radius")
        if cond.empty:
            continue
        cells = [f"sr={r.spectral_radius}: d={r.cohens_d:+.2f} "
                 f"(p_holm={r.p_holm:.3f}{'*' if r.significant else ''})"
                 for r in cond.itertuples()]
        print(f"  {condition}: " + " | ".join(cells))

    print("\n=== Significant connectome-vs-null cells (Holm p < "
          f"{config.ALPHA}), any rung ===")
    sig = stats[stats.significant].sort_values(["condition", "spectral_radius", "rung"])
    if sig.empty:
        print("  (none)")
    else:
        for r in sig.itertuples():
            verdict = "connectome better" if r.cohens_d > 0 else "null better"
            print(f"  {r.condition} sr={r.spectral_radius} vs {r.null_variant}: "
                  f"d={r.cohens_d:+.2f} p_holm={r.p_holm:.3f} ({verdict})")


def main() -> pd.DataFrame:
    results = pd.read_parquet(config.RESULTS_PARQUET)
    stats = compute_stats(results)
    config.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stats.to_parquet(config.STATS_PARQUET)
    print(f"Saved {config.STATS_PARQUET}  ({len(stats)} comparisons)")
    print_summary(stats)
    return stats


if __name__ == "__main__":
    main()

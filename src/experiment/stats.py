"""Generic statistics: connectome vs each null per (condition, spectral_radius).

Task-agnostic. For every (condition, sr), compares the connectome's seed-wise
metric against each null with a two-sided permutation test, Holm-corrects across
the nulls, and reports Cohen's d on the *performance* direction so that
**d > 0 always means the connectome beats the null**, whether the metric is
lower- or higher-is-better (set via ``cfg.metric_lower_is_better``).
"""

import numpy as np
import pandas as pd


def cohens_d(connectome: np.ndarray, null: np.ndarray, lower_is_better: bool) -> float:
    n1, n2 = len(connectome), len(null)
    if n1 < 2 or n2 < 2:
        return float("nan")
    pooled_var = ((n1 - 1) * np.var(connectome, ddof=1)
                  + (n2 - 1) * np.var(null, ddof=1)) / (n1 + n2 - 2)
    pooled_sd = np.sqrt(pooled_var)
    if pooled_sd < 1e-12:
        return 0.0
    diff = ((np.mean(null) - np.mean(connectome)) if lower_is_better
            else (np.mean(connectome) - np.mean(null)))
    return float(diff / pooled_sd)


def permutation_pvalue(connectome: np.ndarray, null: np.ndarray,
                       n_permutations: int, rng: np.random.Generator) -> float:
    """Two-sided permutation test on the difference in means (unpaired)."""
    observed = abs(np.mean(connectome) - np.mean(null))
    pooled = np.concatenate([connectome, null])
    n1 = len(connectome)
    count = 0
    for _ in range(n_permutations):
        rng.shuffle(pooled)
        if abs(np.mean(pooled[:n1]) - np.mean(pooled[n1:])) >= observed - 1e-12:
            count += 1
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


def compute_stats(results: pd.DataFrame, cfg) -> pd.DataFrame:
    rng = np.random.default_rng(cfg.permutation_seed)
    metric = cfg.metric
    rows = []
    for condition in sorted(results.condition.unique()):
        cond_df = results[results.condition == condition]
        for sr in sorted(cond_df.spectral_radius.unique()):
            sr_df = cond_df[cond_df.spectral_radius == sr]
            connectome = (sr_df[sr_df.variant == "connectome"]
                          .sort_values("seed")[metric].values)
            family = []
            for variant in cfg.null_variants:
                null = (sr_df[sr_df.variant == variant]
                        .sort_values("seed")[metric].values)
                if len(connectome) == 0 or len(null) == 0:
                    continue
                d = cohens_d(connectome, null, cfg.metric_lower_is_better)
                p = permutation_pvalue(connectome, null, cfg.n_permutations, rng)
                family.append(dict(
                    condition=condition, spectral_radius=sr, null_variant=variant,
                    rung=cfg.variant_rung[variant],
                    mean_connectome=float(np.mean(connectome)),
                    mean_null=float(np.mean(null)),
                    cohens_d=d, p_raw=p,
                ))
            if family:
                p_holm = holm([row["p_raw"] for row in family])
                for row, adj in zip(family, p_holm):
                    row["p_holm"] = adj
                    row["significant"] = bool(adj < cfg.alpha)
                rows.extend(family)
    return pd.DataFrame(rows)


def print_summary(stats: pd.DataFrame, cfg) -> None:
    """Headline: connectome vs degree_rewire in the supercritical region."""
    print("\n=== Connectome vs degree_rewire (rung 2) in the supercritical region ===")
    print("(Cohen's d > 0 => connectome beats the null)")
    sub = stats[(stats.null_variant == "degree_rewire")
                & (stats.spectral_radius.isin(cfg.supercritical_radii))]
    for condition in cfg.conditions:
        cond = sub[sub.condition == condition].sort_values("spectral_radius")
        if cond.empty:
            continue
        cells = [f"sr={r.spectral_radius}: d={r.cohens_d:+.2f} "
                 f"(p_holm={r.p_holm:.3f}{'*' if r.significant else ''})"
                 for r in cond.itertuples()]
        print(f"  {condition}: " + " | ".join(cells))

    print(f"\n=== Significant connectome-vs-null cells (Holm p < {cfg.alpha}) ===")
    sig = stats[stats.significant].sort_values(["condition", "spectral_radius", "rung"])
    if sig.empty:
        print("  (none)")
    else:
        for r in sig.itertuples():
            verdict = "connectome better" if r.cohens_d > 0 else "null better"
            print(f"  {r.condition} sr={r.spectral_radius} vs {r.null_variant}: "
                  f"d={r.cohens_d:+.2f} p_holm={r.p_holm:.3f} ({verdict})")


def run(cfg) -> pd.DataFrame:
    results = pd.read_parquet(cfg.results_parquet)
    stats = compute_stats(results, cfg)
    cfg.results_dir.mkdir(parents=True, exist_ok=True)
    stats.to_parquet(cfg.stats_parquet)
    print(f"Saved {cfg.stats_parquet}  ({len(stats)} comparisons)")
    print_summary(stats, cfg)
    return stats

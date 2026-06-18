"""Generic statistics: connectome vs each null per (condition, spectral_radius).

Task-agnostic and **divergence-robust**. Supercritical reservoirs can blow up
(huge or non-finite metric values); a single such seed would poison a mean-based
test. So for each (condition, sr) this module:

- **caps** blow-ups (values beyond ``cfg.metric_divergence_cap``, or non-finite)
  to the cap, and reports the **divergence rate** (fraction of seeds blown up)
  per variant -- an honest "how often did it fail" alongside the central tendency;
- compares the connectome against each null with a **rank-based permutation test**
  (insensitive to outlier magnitude) and Holm-corrects across the nulls;
- reports both a rank effect size (**Cliff's delta**) and a capped parametric one
  (**Cohen's d**), plus mean and median, all on the *performance* direction so
  **a positive effect always means the connectome beats the null** (set via
  ``cfg.metric_lower_is_better``).
"""

import numpy as np
import pandas as pd


def _robustify(values: np.ndarray, cap, lower_is_better: bool):
    """Return ``(capped, diverged)``: blow-ups clipped to the cap, and the mask of
    which seeds blew up (non-finite, or beyond the cap on the bad side)."""
    values = np.asarray(values, dtype=float)
    diverged = ~np.isfinite(values)
    if cap is not None:
        diverged = diverged | (values > cap if lower_is_better else values < cap)
    capped = values.copy()
    if diverged.any():
        if cap is not None:
            fill = float(cap)
        else:
            finite = values[np.isfinite(values)]
            fill = (float(finite.max()) if lower_is_better else float(finite.min())) \
                if finite.size else 0.0
        capped[diverged] = fill
    return capped, diverged


def cohens_d(connectome: np.ndarray, null: np.ndarray, lower_is_better: bool) -> float:
    """Parametric effect size on the performance direction (computed on capped values)."""
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


def _winloss(a: np.ndarray, b: np.ndarray) -> int:
    """``#(a_i < b_j) - #(a_i > b_j)`` over all pairs (rank dominance count)."""
    cmp = a[:, None] - b[None, :]
    return int((cmp < 0).sum() - (cmp > 0).sum())


def cliffs_delta(connectome: np.ndarray, null: np.ndarray, lower_is_better: bool) -> float:
    """Rank effect size in [-1, 1] on the performance direction (>0 => connectome
    better). Magnitude-insensitive: a blown-up null seed simply loses every
    pairwise comparison, so divergence counts as 'connectome better' via ranks."""
    total = connectome.size * null.size
    if total == 0:
        return float("nan")
    winloss = _winloss(connectome, null)  # #(conn < null) - #(conn > null)
    oriented = winloss if lower_is_better else -winloss
    return float(oriented / total)


def rank_permutation_pvalue(connectome: np.ndarray, null: np.ndarray,
                            n_permutations: int, rng: np.random.Generator) -> float:
    """Two-sided permutation test on the rank-dominance statistic (a permutation
    Mann-Whitney). Robust to blow-ups: ties at the cap contribute neither win nor
    loss, and outlier magnitude is irrelevant."""
    observed = abs(_winloss(connectome, null))
    pooled = np.concatenate([connectome, null])
    n1 = connectome.size
    count = 0
    for _ in range(n_permutations):
        rng.shuffle(pooled)
        if abs(_winloss(pooled[:n1], pooled[n1:])) >= observed - 1e-9:
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
    cap = cfg.metric_divergence_cap
    lower = cfg.metric_lower_is_better
    rows = []
    for condition in sorted(results.condition.unique()):
        cond_df = results[results.condition == condition]
        for sr in sorted(cond_df.spectral_radius.unique()):
            sr_df = cond_df[cond_df.spectral_radius == sr]
            conn_raw = (sr_df[sr_df.variant == "connectome"]
                        .sort_values("seed")[metric].values)
            if conn_raw.size == 0:
                continue
            connectome, conn_div = _robustify(conn_raw, cap, lower)
            family = []
            for variant in cfg.null_variants:
                null_raw = (sr_df[sr_df.variant == variant]
                            .sort_values("seed")[metric].values)
                if null_raw.size == 0:
                    continue
                null, null_div = _robustify(null_raw, cap, lower)
                family.append(dict(
                    condition=condition, spectral_radius=sr, null_variant=variant,
                    rung=cfg.variant_rung[variant],
                    mean_connectome=float(np.mean(connectome)),
                    mean_null=float(np.mean(null)),
                    median_connectome=float(np.median(connectome)),
                    median_null=float(np.median(null)),
                    frac_diverged_connectome=float(conn_div.mean()),
                    frac_diverged_null=float(null_div.mean()),
                    cohens_d=cohens_d(connectome, null, lower),
                    cliffs_delta=cliffs_delta(connectome, null, lower),
                    p_raw=rank_permutation_pvalue(connectome, null,
                                                  cfg.n_permutations, rng),
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
    print("(Cohen's d > 0 => connectome beats the null; null_div = null blow-up rate)")
    sub = stats[(stats.null_variant == "degree_rewire")
                & (stats.spectral_radius.isin(cfg.supercritical_radii))]
    for condition in cfg.conditions:
        cond = sub[sub.condition == condition].sort_values("spectral_radius")
        if cond.empty:
            continue
        cells = []
        for r in cond.itertuples():
            div = f", null_div={r.frac_diverged_null:.0%}" if r.frac_diverged_null > 0 else ""
            cells.append(f"sr={r.spectral_radius}: d={r.cohens_d:+.2f} "
                         f"(δ={r.cliffs_delta:+.2f}, p={r.p_holm:.3f}"
                         f"{'*' if r.significant else ''}{div})")
        print(f"  {condition}: " + " | ".join(cells))

    print(f"\n=== Significant connectome-vs-null cells (Holm p < {cfg.alpha}) ===")
    sig = stats[stats.significant].sort_values(["condition", "spectral_radius", "rung"])
    if sig.empty:
        print("  (none)")
    else:
        for r in sig.itertuples():
            verdict = "connectome better" if r.cliffs_delta > 0 else "null better"
            print(f"  {r.condition} sr={r.spectral_radius} vs {r.null_variant}: "
                  f"d={r.cohens_d:+.2f} δ={r.cliffs_delta:+.2f} p_holm={r.p_holm:.3f} "
                  f"({verdict})")

    print("\n=== Divergence rates in the supercritical region ===")
    sc = stats[stats.spectral_radius.isin(cfg.supercritical_radii)]
    for condition in cfg.conditions:
        cond = sc[sc.condition == condition]
        if cond.empty:
            continue
        conn = cond.frac_diverged_connectome.mean()
        worst = (cond.groupby("null_variant").frac_diverged_null.mean()
                 .sort_values(ascending=False))
        nulls = "; ".join(f"{v}={r:.0%}" for v, r in worst.items() if r > 0)
        print(f"  {condition}: connectome={conn:.0%}  |  nulls: {nulls or 'none'}")


def run(cfg) -> pd.DataFrame:
    results = pd.read_parquet(cfg.results_parquet)
    stats = compute_stats(results, cfg)
    cfg.results_dir.mkdir(parents=True, exist_ok=True)
    stats.to_parquet(cfg.stats_parquet)
    print(f"Saved {cfg.stats_parquet}  ({len(stats)} comparisons)")
    print_summary(stats, cfg)
    return stats

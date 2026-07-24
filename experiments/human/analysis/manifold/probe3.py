"""Probe 3 -- geometry -> performance link.

No new reservoir runs: Probe 1's parquet already carries the co-recorded,
bit-exact-validated performance metric per row, so geometry and performance are
joined by construction. Computes Spearman rank correlations of {PR, curvature,
entropy} vs each task metric (pooled + per condition, all-sr + supercritical) and
the connectome-minus-degree geometry-gap vs performance-gap tracking. Writes the
geometry-performance + gap-tracking parquets, three figures (geometry-vs-performance
scatter, gap-tracking scatter, PR/performance overlay), and a summary.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

from experiments.human.substrates import HumanSubstrateBuilder
from experiments.human import matrix_config
from experiments.human.analysis.manifold import common

_PERF_BY_TASK = {"mc": ["mc"], "narma10": ["nrmse"], "lorenz": ["vpt", "climate_error"]}
_PERF_PRIMARY = {"mc": "mc", "narma10": "nrmse", "lorenz": "vpt"}
_PERF_LOWER_BETTER = {"mc": False, "nrmse": True, "vpt": False, "climate_error": True}
_PERF_CAP = {"nrmse": 2.0, "climate_error": 10.0}   # None for mc/vpt (bounded)
_GEOM_METRICS = ["pr", "mean_curvature", "spectral_entropy"]
_GEOM_LABEL = {"pr": "participation ratio", "mean_curvature": "mean curvature (rad)",
               "spectral_entropy": "spectral entropy (norm.)"}
_PERF_LABEL = {"mc": "memory capacity", "nrmse": "NARMA-10 NRMSE",
               "vpt": "Lorenz VPT", "climate_error": "Lorenz climate error"}


# ---------------------------------------------------------------------------
# Analyses
# ---------------------------------------------------------------------------
def _capped_perf(values: np.ndarray, metric: str) -> np.ndarray:
    """Divergence-cap a performance column (non-finite / beyond cap -> cap), for
    lower-is-better metrics only (matches the task configs); bounded metrics
    (mc, vpt) pass through."""
    v = np.asarray(values, dtype=float)
    cap = _PERF_CAP.get(metric)
    if cap is None:
        return v
    v = np.where(np.isfinite(v), v, cap)
    return np.minimum(v, cap)


def _correlations(df: pd.DataFrame) -> pd.DataFrame:
    """Spearman rank correlation of each geometry metric vs each performance metric,
    pooled (all conditions) and per condition, over all sr and the supercritical
    region."""
    rows = []
    for task in common.present_tasks(df):
        tdf = df[df.task == task]
        for perf in _PERF_BY_TASK[task]:
            for geom in _GEOM_METRICS:
                scopes = [("pooled", tdf)]
                scopes += [(c, tdf[tdf.condition == c]) for c in matrix_config.CONDITIONS]
                for cond_name, cdf in scopes:
                    for region, mask in [("all_sr", cdf.spectral_radius >= 0),
                                         ("supercritical",
                                          cdf.spectral_radius >= common.SUPERCRITICAL_SR)]:
                        s = cdf[mask]
                        x = s[geom].to_numpy(float)
                        y = _capped_perf(s[perf].to_numpy(float), perf)
                        ok = np.isfinite(x) & np.isfinite(y)
                        if ok.sum() < 10:
                            continue
                        r, p = spearmanr(x[ok], y[ok])
                        rows.append(dict(task=task, performance=perf, geometry=geom,
                                         condition=cond_name, region=region,
                                         spearman_r=float(r), p_value=float(p),
                                         n=int(ok.sum())))
    return pd.DataFrame(rows)


def _gap_frame(df: pd.DataFrame, supercrit: dict) -> pd.DataFrame:
    """Per (task, condition, supercritical sr): connectome-minus-degree_rewire gap in
    geometry and performance, oriented so positive == connectome better/holds more."""
    rows = []
    for task in common.present_tasks(df):
        for cond in matrix_config.CONDITIONS:
            crit = supercrit.get(cond, common.SUPERCRITICAL_SR)
            sub = df[(df.task == task) & (df.condition == cond)
                     & (df.spectral_radius >= crit)]
            for sr, g in sub.groupby("spectral_radius"):
                conn = g[g.variant == "connectome"]
                deg = g[g.variant == "degree_rewire"]
                if conn.empty or deg.empty:
                    continue
                rec = dict(task=task, condition=cond, spectral_radius=float(sr),
                           # PR held: + == connectome more dimensions
                           dPR=float(conn.pr.median() - deg.pr.median()),
                           # straighter: + == connectome lower curvature
                           dStraight=float(deg.mean_curvature.median()
                                           - conn.mean_curvature.median()))
                for perf in _PERF_BY_TASK[task]:
                    cp = float(np.median(_capped_perf(conn[perf].to_numpy(float), perf)))
                    dp = float(np.median(_capped_perf(deg[perf].to_numpy(float), perf)))
                    rec[f"d_{perf}"] = (dp - cp) if _PERF_LOWER_BETTER[perf] else (cp - dp)
                rows.append(rec)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
def _annotate_spearman(ax, x, y):
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() > 5:
        r, _ = spearmanr(x[ok], y[ok])
        ax.text(0.04, 0.96, f"$r_s$={r:+.2f}", transform=ax.transAxes, va="top",
                ha="left", fontsize=9,
                bbox=dict(boxstyle="round", fc="white", ec="0.7", alpha=0.8))


def _plot_geometry_vs_performance(df, path):
    """Scatter grid: rows = tasks, cols = geometry metrics; y = the task's primary
    performance metric; one point per (variant, sr) seed-median, coloured by
    condition. Spearman r (pooled, all sr) annotated."""
    tasks = common.present_tasks(df)
    nrows, ncols = len(tasks), len(_GEOM_METRICS)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.0 * ncols, 3.2 * nrows),
                             squeeze=False)
    for i, task in enumerate(tasks):
        perf = _PERF_PRIMARY[task]
        tdf = df[df.task == task]
        agg = (tdf.groupby(["condition", "variant", "spectral_radius"])
               .agg(**{g: (g, "median") for g in _GEOM_METRICS},
                    perf=(perf, lambda s: np.median(_capped_perf(s.to_numpy(float), perf))))
               .reset_index())
        for j, geom in enumerate(_GEOM_METRICS):
            ax = axes[i][j]
            for cond in matrix_config.CONDITIONS:
                c = agg[agg.condition == cond]
                ax.scatter(c[geom], c["perf"], s=14, alpha=0.55,
                           color=common.CONDITION_COLOR[cond], edgecolor="none",
                           label=common.CONDITION_TITLE.get(cond, cond))
            _annotate_spearman(ax, agg[geom].to_numpy(float), agg["perf"].to_numpy(float))
            ax.grid(alpha=0.25)
            if i == nrows - 1:
                ax.set_xlabel(_GEOM_LABEL[geom])
            if j == 0:
                ax.set_ylabel(f"{common.TASK_TITLE.get(task, task)}\n{_PERF_LABEL[perf]}",
                              fontsize=9)
    _condition_legend(fig)
    fig.suptitle("Probe 3: manifold geometry vs task performance "
                 "(seed-median per variant x sr; $r_s$ = pooled Spearman)", fontsize=12)
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _plot_gap_tracking(gap, path):
    """Does the connectome-minus-degree geometric gap track the performance gap in
    the supercritical region? Rows = tasks; cols = [dPR, dStraight]; y = primary
    performance gap (oriented so + == connectome better)."""
    tasks = common.present_tasks(gap)
    gap_cols = [("dPR", "$\\Delta$PR (connectome - degree)"),
                ("dStraight", "$\\Delta$straightness (degree - connectome curvature)")]
    nrows, ncols = len(tasks), len(gap_cols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.4 * ncols, 3.2 * nrows),
                             squeeze=False)
    for i, task in enumerate(tasks):
        perf = _PERF_PRIMARY[task]
        tdf = gap[gap.task == task]
        for j, (gcol, glabel) in enumerate(gap_cols):
            ax = axes[i][j]
            for cond in matrix_config.CONDITIONS:
                c = tdf[tdf.condition == cond]
                ax.scatter(c[gcol], c[f"d_{perf}"], s=20, alpha=0.6,
                           color=common.CONDITION_COLOR[cond],
                           label=common.CONDITION_TITLE.get(cond, cond))
            _annotate_spearman(ax, tdf[gcol].to_numpy(float),
                               tdf[f"d_{perf}"].to_numpy(float))
            ax.axhline(0, color="0.6", lw=0.8, ls=":")
            ax.axvline(0, color="0.6", lw=0.8, ls=":")
            ax.grid(alpha=0.25)
            if i == nrows - 1:
                ax.set_xlabel(glabel, fontsize=9)
            if j == 0:
                ax.set_ylabel(f"{common.TASK_TITLE.get(task, task)}\n$\\Delta${_PERF_LABEL[perf]}"
                              "\n(+ = connectome better)", fontsize=8)
    _condition_legend(fig)
    fig.suptitle("Probe 3: does the connectome-vs-degree GEOMETRY gap track the "
                 "PERFORMANCE gap? (supercritical sr)", fontsize=12)
    fig.tight_layout(rect=[0, 0.05, 1, 0.97])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _plot_overlay(df, supercrit, path):
    """The story figure: PR(sr) (left axis) and the primary performance curve (right
    axis) on shared axes, connectome (solid) vs degree_rewire (dashed), per
    task x condition. Seed medians."""
    tasks = common.present_tasks(df)
    conditions = common.present_conditions(df)
    nrows, ncols = len(tasks), len(conditions)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.2 * ncols, 3.1 * nrows),
                             squeeze=False, sharex=True)
    for i, task in enumerate(tasks):
        perf = _PERF_PRIMARY[task]
        for j, cond in enumerate(conditions):
            axL = axes[i][j]
            axR = axL.twinx()
            sub = df[(df.task == task) & (df.condition == cond)]
            for variant, ls in [("connectome", "-"), ("degree_rewire", "--")]:
                v = sub[sub.variant == variant]
                pr = v.groupby("spectral_radius").pr.median()
                pf = v.groupby("spectral_radius")[perf].apply(
                    lambda s: np.median(_capped_perf(s.to_numpy(float), perf)))
                axL.plot(pr.index, pr.values, ls=ls, color="black", lw=1.6)
                axR.plot(pf.index, pf.values, ls=ls, color="#c44e52", lw=1.6)
            start = supercrit.get(cond)
            if start is not None:
                axL.axvspan(start, float(df.spectral_radius.max()),
                            color=common.SUPERCRITICAL_COLOR, zorder=0)
            axL.grid(alpha=0.2)
            if i == 0:
                axL.set_title(common.CONDITION_TITLE.get(cond, cond), fontsize=10)
            if j == 0:
                axL.set_ylabel(f"{common.TASK_TITLE.get(task, task)}\nPR (black)", fontsize=9)
            if j == ncols - 1:
                axR.set_ylabel(f"{_PERF_LABEL[perf]} (red)", fontsize=9)
            if i == nrows - 1:
                axL.set_xlabel("spectral radius")
    fig.suptitle("Probe 3 story: PR (black) and performance (red) vs sr -- "
                 "connectome (solid) vs degree_rewire (dashed)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _condition_legend(fig):
    handles = [plt.Line2D([0], [0], marker="o", ls="", color=common.CONDITION_COLOR[c],
                          label=common.CONDITION_TITLE.get(c, c))
               for c in matrix_config.CONDITIONS]
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=9,
               bbox_to_anchor=(0.5, -0.02))


def _write_summary(corr, gap, path):
    """Headline correlations + gap-tracking, for the Findings block."""
    lines = ["# Manifold Probe 3 -- geometry -> performance (human N=448)\n",
             "## Pooled Spearman r (geometry vs primary performance, supercritical)\n",
             "| task | performance | geometry | r_s | n |", "|---|---|---|---|---|"]
    for task in common.present_tasks(corr):
        perf = _PERF_PRIMARY[task]
        for geom in _GEOM_METRICS:
            r = corr[(corr.task == task) & (corr.performance == perf)
                     & (corr.geometry == geom) & (corr.condition == "pooled")
                     & (corr.region == "supercritical")]
            if not r.empty:
                lines.append(f"| {task} | {perf} | {geom} | {r.spearman_r.values[0]:+.2f} "
                             f"| {int(r.n.values[0])} |")
    lines += ["\n## Gap-tracking Spearman (connectome-degree geometry gap vs "
              "performance gap, supercritical)\n",
              "| task | dPR vs dPerf | dStraight vs dPerf |", "|---|---|---|"]
    for task in common.present_tasks(gap):
        perf = _PERF_PRIMARY[task]
        t = gap[gap.task == task]
        out = {}
        for gcol in ("dPR", "dStraight"):
            x, y = t[gcol].to_numpy(float), t[f"d_{perf}"].to_numpy(float)
            ok = np.isfinite(x) & np.isfinite(y)
            out[gcol] = spearmanr(x[ok], y[ok])[0] if ok.sum() > 5 else float("nan")
        lines.append(f"| {task} | {out['dPR']:+.2f} | {out['dStraight']:+.2f} |")
    path.write_text("\n".join(lines) + "\n")
    print(f"Saved {path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def run(smoke: bool = False, jobs: int = 1, scale: int | None = None) -> None:
    scale = matrix_config.SCALE if scale is None else scale
    results_dir, figures_dir = common.scale_dirs(scale)
    metrics_parquet = results_dir / "manifold_metrics.parquet"
    if not metrics_parquet.exists():
        raise FileNotFoundError(
            f"{metrics_parquet} not found -- run Probe 1 (--probe 1) first.")
    df = pd.read_parquet(metrics_parquet)
    print(f"Probe 3: loaded {len(df)} rows from {metrics_parquet}")

    builder = HumanSubstrateBuilder(scale=scale)
    supercrit = builder.connectome_supercritical_radii(matrix_config.CONDITIONS)

    corr = _correlations(df)
    gap = _gap_frame(df, supercrit)
    results_dir.mkdir(parents=True, exist_ok=True)
    corr.to_parquet(results_dir / "manifold_geometry_performance.parquet")
    gap.to_parquet(results_dir / "manifold_gap_tracking.parquet")
    print(f"Saved {results_dir / 'manifold_geometry_performance.parquet'} ({len(corr)} rows)")

    figures_dir.mkdir(parents=True, exist_ok=True)
    _plot_geometry_vs_performance(df, figures_dir / "manifold_geometry_vs_performance.png")
    print(f"Saved {figures_dir / 'manifold_geometry_vs_performance.png'}")
    _plot_gap_tracking(gap, figures_dir / "manifold_gap_tracking.png")
    print(f"Saved {figures_dir / 'manifold_gap_tracking.png'}")
    _plot_overlay(df, supercrit, figures_dir / "manifold_pr_performance_overlay.png")
    print(f"Saved {figures_dir / 'manifold_pr_performance_overlay.png'}")
    _write_summary(corr, gap, results_dir / "manifold_probe3_summary.md")

    print("\nPooled Spearman (geometry vs primary perf, supercritical):")
    for task in common.present_tasks(corr):
        perf = _PERF_PRIMARY[task]
        cells = []
        for geom in _GEOM_METRICS:
            r = corr[(corr.task == task) & (corr.performance == perf)
                     & (corr.geometry == geom) & (corr.condition == "pooled")
                     & (corr.region == "supercritical")]
            if not r.empty:
                cells.append(f"{geom}={r.spearman_r.values[0]:+.2f}")
        print(f"  {task} ({perf}): " + "  ".join(cells))
    print("\nProbe 3 complete.")

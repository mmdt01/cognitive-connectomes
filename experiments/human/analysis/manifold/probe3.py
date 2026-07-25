"""Probe 3 -- geometry -> performance link.

No new reservoir runs: Probe 1's parquet already carries the co-recorded,
bit-exact-validated performance metric per row, so geometry and performance are
joined by construction. Computes Spearman rank correlations of {PR, curvature,
entropy} vs each task metric (pooled + per condition, all-sr + supercritical) and
the connectome-minus-degree geometry-gap vs performance-gap tracking. Writes the
geometry-performance + gap-tracking parquets, three figures (geometry-vs-performance
scatter, gap-tracking scatter, PR/performance overlay), and a summary.

REBUILD (headline): ``run_deff`` re-runs the dimensionality link around the ridge
EFFECTIVE RANK (d_eff, from the design-Gram spectrum in covariance_spectra.parquet)
instead of the variance-weighted participation ratio. PR misses the low-variance
directions the ridge readout uses; d_eff counts them and orders the null ladder for
memory capacity where PR does not. PR is kept and reported alongside as the contrast
that motivated the change. Depends on the ``--spectra`` extraction having been run.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

from src.analysis import manifold
from src.experiment.plots import _VARIANT_STYLE, _VARIANT_LABEL
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
# REBUILD: ridge effective rank (d_eff) -- the headline dimensionality measure
# ---------------------------------------------------------------------------
# Empirical column supercritical threshold for the ladder analyses. The reduced
# covariance-spectra grid has 5 points at/above this (3.0526 .. 6.0).
_DEFF_SUPERCRITICAL_SR = 3.05
_DEFF_JOIN_KEYS = ["task", "condition", "variant", "rung", "seed", "_sr"]
_DEFF_PERF_COLS = ["pr", "mean_curvature", "mc", "nrmse", "vpt", "climate_error"]


def _pr_sanity_check(cov: pd.DataFrame, metrics: pd.DataFrame, n_rows: int = 12) -> float:
    """Step 1 gate: PR recomputed from eig_cov must reproduce the published
    manifold_metrics PR (confirms the spectra and metric code agree). Flags (asserts)
    any mismatch beyond floating-point tolerance rather than silently correcting."""
    sample = cov.sample(min(n_rows, len(cov)), random_state=0)
    worst = 0.0
    for _, row in sample.iterrows():
        eig = np.asarray(row["eig_cov"], dtype=float)
        pr = manifold._pr_from_eigenvalues(eig)
        m = metrics[(metrics.task == row.task) & (metrics.condition == row.condition)
                    & (metrics.variant == row.variant) & (metrics.seed == row.seed)
                    & (metrics._sr == round(float(row.spectral_radius), 6))]
        if m.empty:
            continue
        worst = max(worst, abs(pr - m.iloc[0]["pr"]) / max(abs(m.iloc[0]["pr"]), 1e-12))
    assert worst < 1e-5, (
        f"[Step 1] PR from eig_cov disagrees with published manifold_metrics PR "
        f"(worst rel diff {worst:.2e} >= 1e-5) -- spectra and metric code are out of "
        "sync; investigate before trusting d_eff.")
    print(f"[Step 1] PR(eig_cov) vs published PR: worst rel diff = {worst:.2e}  (OK, < 1e-5)")
    return worst


def load_deff_table(results_dir) -> pd.DataFrame:
    """Step 2: d_eff for every covariance-spectra row (each task's own alpha + Gram),
    joined to the performance metrics on the reduced 13-point sr grid."""
    cov = pd.read_parquet(results_dir / "covariance_spectra.parquet").copy()
    metrics = pd.read_parquet(results_dir / "manifold_metrics.parquet").copy()
    metrics["_sr"] = metrics.spectral_radius.round(6)
    _pr_sanity_check(cov, metrics)

    cov["d_eff"] = [manifold.ridge_effective_rank(g, a)
                    for g, a in zip(cov["eig_gram"], cov["alpha"])]
    cov["_sr"] = cov.spectral_radius.round(6)
    joined = cov[_DEFF_JOIN_KEYS + ["spectral_radius", "d_eff", "alpha"]].merge(
        metrics[_DEFF_JOIN_KEYS + _DEFF_PERF_COLS], on=_DEFF_JOIN_KEYS, how="inner")
    assert len(joined) == len(cov), (
        f"[Step 2] join dropped rows ({len(joined)} != {len(cov)}); key/grid mismatch.")
    return joined.drop(columns="_sr")


def _spearman_capped(sub, xcol, ycol):
    x = sub[xcol].to_numpy(float)
    y = _capped_perf(sub[ycol].to_numpy(float), ycol)
    ok = np.isfinite(x) & np.isfinite(y)
    return (float(spearmanr(x[ok], y[ok])[0]), int(ok.sum())) if ok.sum() > 3 else (np.nan, 0)


def deff_correlations(deff: pd.DataFrame) -> pd.DataFrame:
    """Step 3: the compact correlation table -- d_eff and PR side by side."""
    emp = deff[(deff.condition == "human_empirical")
               & (deff.spectral_radius >= _DEFF_SUPERCRITICAL_SR)]
    gau = deff[(deff.condition == "human_gaussian")
               & (deff.spectral_radius >= _DEFF_SUPERCRITICAL_SR)]
    rows = []

    def add(analysis, task, y, scope, sub, want_curv=False):
        d_rs, n = _spearman_capped(sub, "d_eff", y)
        p_rs, _ = _spearman_capped(sub, "pr", y)
        c_rs, _ = _spearman_capped(sub, "mean_curvature", y) if want_curv else (np.nan, 0)
        rows.append(dict(analysis=analysis, task=task, y=y, scope=scope,
                         d_eff_rs=d_rs, pr_rs=p_rs, curvature_rs=c_rs, n=n))

    # (a) ladder ordering: median per variant across the 7 rungs.
    for task, perf in [("mc", "mc"), ("narma10", "nrmse")]:
        g = emp[emp.task == task].groupby("variant", as_index=False).median(numeric_only=True)
        add("(a) ladder ordering", task, perf,
            "empirical, sr>=3.05, median/variant (7 rungs)", g)
    # (b) within-regime: pooled across variant x sr x seed.
    for task, perf in [("mc", "mc"), ("narma10", "nrmse")]:
        add("(b) within-regime", task, perf,
            "empirical, sr>=3.05, pooled var/sr/seed", emp[emp.task == task])
    # (c) task-axis separation: d_eff must NOT read Lorenz VPT; curvature does the
    # generative axis -- reported both within-empirical (frozen) and pooled (real).
    add("(c) task-axis (within-empirical)", "lorenz", "vpt",
        "empirical, sr>=3.05, pooled", emp[emp.task == "lorenz"], want_curv=True)
    add("(c) task-axis (pooled conditions)", "lorenz", "vpt",
        "all conditions, sr>=3.05, pooled",
        deff[(deff.task == "lorenz") & (deff.spectral_radius >= _DEFF_SUPERCRITICAL_SR)],
        want_curv=True)
    # (d) sign-gating control: no ladder ordering under balanced sign (gaussian).
    for task, perf in [("mc", "mc"), ("narma10", "nrmse")]:
        g = gau[gau.task == task].groupby("variant", as_index=False).median(numeric_only=True)
        add("(d) sign-gating control (gaussian)", task, perf,
            "gaussian, sr>=3.05, median/variant (7 rungs)", g)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# d_eff figures
# ---------------------------------------------------------------------------
def _plot_deff_vs_mc(deff, path):
    """Money figure: d_eff vs MC (left) and PR vs MC (right), empirical column,
    supercritical, coloured by variant (small points = each sr x seed; large markers
    = per-variant median). Perfect ladder ordering under d_eff vs none under PR."""
    emp = deff[(deff.task == "mc") & (deff.condition == "human_empirical")
               & (deff.spectral_radius >= _DEFF_SUPERCRITICAL_SR)]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4))
    for ax, xcol, xlabel in [(axes[0], "d_eff", "ridge effective rank $d_{eff}$"),
                             (axes[1], "pr", "participation ratio (PR)")]:
        for variant in matrix_config.VARIANTS:
            v = emp[emp.variant == variant]
            if v.empty:
                continue
            style = _VARIANT_STYLE[variant]
            ax.scatter(v[xcol], v["mc"], s=10, alpha=0.35, color=style["color"],
                       edgecolor="none", zorder=2)
            ax.scatter(v[xcol].median(), v["mc"].median(), s=90, color=style["color"],
                       edgecolor="black", lw=0.8, zorder=3, label=_VARIANT_LABEL[variant])
        g = emp.groupby("variant", as_index=False).median(numeric_only=True)
        r, _ = _spearman_capped(g, xcol, "mc")
        ax.text(0.04, 0.96, f"ladder $r_s$={r:+.2f}", transform=ax.transAxes, va="top",
                fontsize=10, bbox=dict(boxstyle="round", fc="white", ec="0.7", alpha=0.85))
        ax.set_xlabel(xlabel)
        ax.set_ylabel("memory capacity")
        ax.grid(alpha=0.25)
    axes[1].legend(fontsize=7, framealpha=0.9, loc="lower right", ncol=1)
    fig.suptitle("Probe 3 rebuilt: ridge effective rank orders the memory ladder; "
                 "PR does not (human empirical, sr ≥ 3.05)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _plot_deff_vs_sr(deff, path):
    """d_eff vs spectral radius, one median line per variant, empirical column -- the
    connectome holds the most usable directions across the supercritical sweep."""
    emp = deff[(deff.task == "mc") & (deff.condition == "human_empirical")]
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    for variant in matrix_config.VARIANTS:
        v = (emp[emp.variant == variant].groupby("spectral_radius", as_index=False)
             .d_eff.median().sort_values("spectral_radius"))
        if v.empty:
            continue
        ax.plot(v.spectral_radius, v.d_eff, label=_VARIANT_LABEL[variant],
                **_VARIANT_STYLE[variant])
    ax.axvspan(_DEFF_SUPERCRITICAL_SR, float(emp.spectral_radius.max()),
               color=common.SUPERCRITICAL_COLOR, zorder=0)
    ax.axvline(1.0, color="grey", lw=0.8, ls=":", zorder=1)
    ax.set_xlabel("spectral radius")
    ax.set_ylabel("ridge effective rank $d_{eff}$ (MC readout)")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=7, framealpha=0.9, loc="upper right")
    fig.suptitle("Usable readout directions vs spectral radius (human empirical, MC)",
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _plot_two_axis(deff, path):
    """Two-axis account: memory reads out d_eff (left, empirical, coloured by variant);
    the generative Lorenz task reads out trajectory straightness (right, all conditions
    where curvature varies, coloured by condition)."""
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4))
    emp = deff[(deff.task == "mc") & (deff.condition == "human_empirical")
               & (deff.spectral_radius >= _DEFF_SUPERCRITICAL_SR)]
    for variant in matrix_config.VARIANTS:
        v = emp[emp.variant == variant]
        if not v.empty:
            axes[0].scatter(v["d_eff"], v["mc"], s=12, alpha=0.5,
                            color=_VARIANT_STYLE[variant]["color"], edgecolor="none")
    r, _ = _spearman_capped(emp.groupby("variant", as_index=False).median(numeric_only=True),
                            "d_eff", "mc")
    axes[0].text(0.04, 0.96, f"ladder $r_s$={r:+.2f}", transform=axes[0].transAxes,
                 va="top", fontsize=10, bbox=dict(boxstyle="round", fc="white", ec="0.7"))
    axes[0].set_xlabel("ridge effective rank $d_{eff}$")
    axes[0].set_ylabel("memory capacity")
    axes[0].set_title("Memory axis: $d_{eff}$ → MC (empirical)", fontsize=10)

    lor = deff[(deff.task == "lorenz") & (deff.spectral_radius >= _DEFF_SUPERCRITICAL_SR)]
    for cond in matrix_config.CONDITIONS:
        c = lor[lor.condition == cond]
        if not c.empty:
            axes[1].scatter(c["mean_curvature"], c["vpt"], s=12, alpha=0.5,
                            color=common.CONDITION_COLOR[cond],
                            label=common.CONDITION_TITLE.get(cond, cond))
    rc, _ = _spearman_capped(lor, "mean_curvature", "vpt")
    axes[1].text(0.04, 0.96, f"$r_s$={rc:+.2f}", transform=axes[1].transAxes, va="top",
                 fontsize=10, bbox=dict(boxstyle="round", fc="white", ec="0.7"))
    axes[1].set_xlabel("mean curvature (rad)")
    axes[1].set_ylabel("Lorenz VPT")
    axes[1].set_title("Generative axis: curvature → VPT (all conditions)", fontsize=10)
    axes[1].legend(fontsize=7, framealpha=0.9, loc="upper right")
    for ax in axes:
        ax.grid(alpha=0.25)
    fig.suptitle("Two-axis account: memory reads effective rank, generation reads "
                 "straightness", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _write_deff_summary(corr, path):
    lines = ["# Probe 3 rebuilt -- ridge effective rank d_eff (human N=448)\n",
             "d_eff = sum_i g_i / (g_i + alpha) over the design-Gram spectrum (trace of "
             "the ridge hat matrix; ESL). PR reported alongside as the contrast.\n",
             "| analysis | task | y | scope | d_eff r_s | PR r_s | curvature r_s | n |",
             "|---|---|---|---|---|---|---|---|"]

    def fmt(x):
        return "--" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:+.2f}"

    for r in corr.itertuples():
        lines.append(f"| {r.analysis} | {r.task} | {r.y} | {r.scope} | "
                     f"{fmt(r.d_eff_rs)} | {fmt(r.pr_rs)} | {fmt(r.curvature_rs)} | {r.n} |")
    path.write_text("\n".join(lines) + "\n")
    print(f"Saved {path}")


def run_deff(scale: int | None = None) -> None:
    """The d_eff rebuild (Steps 2 to 4). Reads covariance_spectra.parquet (from the
    ``--spectra`` extraction) + manifold_metrics.parquet; writes probe3_deff.parquet,
    three figures, and the correlation summary. No reservoir runs."""
    scale = matrix_config.SCALE if scale is None else scale
    results_dir, figures_dir = common.scale_dirs(scale)
    cov_path = results_dir / "covariance_spectra.parquet"
    if not cov_path.exists():
        print(f"  [d_eff] {cov_path} absent -- run `--spectra` first; skipping rebuild.")
        return
    print("\n=== Probe 3 rebuild: ridge effective rank (d_eff) ===")
    deff = load_deff_table(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    deff.to_parquet(results_dir / "probe3_deff.parquet")
    print(f"[Step 2] Saved {results_dir / 'probe3_deff.parquet'}  ({len(deff)} rows)")

    corr = deff_correlations(deff)
    _write_deff_summary(corr, results_dir / "probe3_deff_summary.md")
    figures_dir.mkdir(parents=True, exist_ok=True)
    _plot_deff_vs_mc(deff, figures_dir / "probe3_deff_vs_mc.png")
    _plot_deff_vs_sr(deff, figures_dir / "probe3_deff_vs_sr.png")
    _plot_two_axis(deff, figures_dir / "probe3_deff_two_axis.png")
    for name in ("probe3_deff_vs_mc", "probe3_deff_vs_sr", "probe3_deff_two_axis"):
        print(f"Saved {figures_dir / (name + '.png')}")

    print("\n[Step 3] correlation table (d_eff vs PR side by side):")
    with pd.option_context("display.width", 160, "display.max_columns", None):
        print(corr[["analysis", "task", "y", "d_eff_rs", "pr_rs", "curvature_rs", "n"]]
              .to_string(index=False))
    print("\nProbe 3 (d_eff rebuild) complete.")


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
    print("\nProbe 3 (PR-based) complete.")

    # Headline rebuild around ridge effective rank (supersedes the PR link above;
    # needs the --spectra extraction, so skips gracefully if it is absent).
    run_deff(scale)

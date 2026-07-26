"""Phase-diagram analysis: the two mirrored panels and their boundaries.

Reads ``phase_cells.parquet`` (from ``capture``) and computes, for the
``stratified`` primary (and any placement targetings present):

- seed x draw medians per (targeting, f, sr, variant, task);
- the two order parameters, both oriented so **higher = connectome advantage** and
  each resolved to its own task -- Panel A memory reads the **MC** task
  (``dD = d_eff(connectome) - d_eff(erdos_renyi)``, plus ``dMC``, and ``dNARMA``
  from the NARMA task); Panel B generative reads the **Lorenz** task
  (``dStraight = curvature(ER) - curvature(conn)``, plus ``dVPT``, ``dClimate``);
- the connectome-vs-ER Cliff's delta per cell (rank stats from
  ``src/experiment/stats.py``);
- observed boundaries (the 25%-of-global-max contour, and the Cliff's-delta
  contour) -- for Panel A the *collapse* contour (advantage destroyed by sign) and
  for the emergent Panel B its mirror, the *onset* contour (advantage created by
  sign) -- and predicted boundaries (each panel's own driven-state ``|mean_state|``
  collapse and ``effective_radius`` crossing 1, plus the task-independent
  ``bulk95``), and the correlation of each order parameter with each candidate
  spectral predictor across all cells;
- the cross-panel comparison (do the two boundaries coincide) and the placement
  ``f*`` per targeting.

Writes ``phase_grid.parquet``, ``phase_boundaries.parquet``,
``phase_predictor_corr.parquet`` and ``phase_summary.md``. No reservoir runs.
"""

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from src.experiment import stats as expstats
from experiments.human import matrix_config
from experiments.human.analysis.phase_diagram import common

CONN, CTR = "connectome", common.CONTRAST_VARIANT      # erdos_renyi

# Each order parameter, the task it is read from, the raw metric, the sign of
# "connectome first" and whether the raw metric is lower-is-better.
#   name         task        metric          conn_first  lower_is_better
_ORDER_PARAMS = [
    ("dD",        "mc",       "d_eff",         True,  False),
    ("dMC",       "mc",       "mc",            True,  False),
    ("dNARMA",    "narma10",  "nrmse",         False, True),
    ("dStraight", "lorenz",   "mean_curvature", False, True),
    ("dVPT",      "lorenz",   "vpt",           True,  False),
    ("dClimate",  "lorenz",   "climate_error", False, True),
]
# The panel each order parameter belongs to and the task supplying its predictors.
_PANEL_A_OPS = ["dD", "dMC", "dNARMA"]
_PANEL_B_OPS = ["dStraight", "dVPT", "dClimate"]
_PANEL_A_TASK, _PANEL_B_TASK = "mc", "lorenz"

# Cliff's-delta geometry per panel: (order param, task, metric, lower_is_better).
_CLIFF_A = ("cliffs_dD", "mc", "d_eff", False)
_CLIFF_B = ("cliffs_dStraight", "lorenz", "mean_curvature", True)

_MEASURE_COLS = ["d_eff", "mean_curvature", "pr", "mean_state", "mean_gain",
                 "frac_saturated", "effective_radius", "neg_frac", "bulk95",
                 "leading_gap", "perron_root"]
_PERF_COLS = ["mc", "nrmse", "vpt", "climate_error"]

_REP_F = [0.0, 0.25, 0.5]
_REP_SR = [2.0, 4.0, 6.0]
_CLIFF_SIG = 0.33
_LEVEL_FRAC = 0.25


# ---------------------------------------------------------------------------
# Cell medians + order parameters (task-resolved)
# ---------------------------------------------------------------------------
def cell_medians(df: pd.DataFrame) -> pd.DataFrame:
    """seed x draw median of every measurement per (targeting, f, sr, variant, task)."""
    df = df.copy()
    df["abs_mean_state"] = df["mean_state"].abs()
    value_cols = ([c for c in _MEASURE_COLS if c in df.columns]
                  + [c for c in _PERF_COLS if c in df.columns] + ["abs_mean_state"])
    return (df.groupby(["targeting", "f", "spectral_radius", "variant", "task"],
                       as_index=False)[value_cols].median())


def order_parameters(med: pd.DataFrame) -> pd.DataFrame:
    """Order parameters + panel-specific spectral predictors per (targeting, f, sr).

    Each order parameter is read from its own task; Panel A predictors come from the
    MC driven states, Panel B predictors from the Lorenz driven states, and the
    task-independent ``bulk95`` / ``perron_root`` (properties of the flipped W) from
    whichever task is present."""
    tasks_present = set(med.task.unique())
    rows = []
    for (tg, f, sr), g in med.groupby(["targeting", "f", "spectral_radius"]):
        rec = dict(targeting=tg, f=float(f), spectral_radius=float(sr))

        def val(task, variant, col):
            r = g[(g.task == task) & (g.variant == variant)]
            return float(r[col].iloc[0]) if not r.empty and col in r else np.nan

        for name, task, metric, conn_first, _ in _ORDER_PARAMS:
            if task not in tasks_present:
                continue
            a, b = val(task, CONN, metric), val(task, CTR, metric)
            rec[name] = (a - b) if conn_first else (b - a)
        # Raw per-variant MC d_eff (reference).
        for v in (CONN, CTR, "degree_rewire"):
            rec[f"d_eff_{v}"] = val(_PANEL_A_TASK, v, "d_eff")
        # Panel-specific connectome-side driven-state predictors.
        for prefix, task in [("A", _PANEL_A_TASK), ("B", _PANEL_B_TASK)]:
            rec[f"{prefix}_abs_mean_state"] = val(task, CONN, "abs_mean_state")
            rec[f"{prefix}_effective_radius"] = val(task, CONN, "effective_radius")
            rec[f"{prefix}_mean_gain"] = val(task, CONN, "mean_gain")
        # Task-independent flipped-W spectral scalars (same across tasks).
        any_task = _PANEL_A_TASK if _PANEL_A_TASK in tasks_present else sorted(tasks_present)[0]
        rec["bulk95"] = val(any_task, CONN, "bulk95")
        rec["perron_root"] = val(any_task, CONN, "perron_root")
        rec["leading_gap"] = val(any_task, CONN, "leading_gap")
        rows.append(rec)
    return pd.DataFrame(rows).sort_values(["targeting", "f", "spectral_radius"])


def cliffs_grid(df: pd.DataFrame, task: str, value_col: str,
                lower_is_better: bool) -> pd.DataFrame:
    """Connectome-vs-ER Cliff's delta per (targeting, f, sr) for one task, over the
    seed x draw replicates (>0 == connectome better on the performance direction)."""
    cols = ["targeting", "f", "spectral_radius", "cliffs"]
    sub = df[df.task == task] if value_col in df.columns else df.iloc[0:0]
    rows = []
    for (tg, f, sr), g in sub.groupby(["targeting", "f", "spectral_radius"]):
        a = g[g.variant == CONN][value_col].to_numpy(float)
        b = g[g.variant == CTR][value_col].to_numpy(float)
        a, b = a[np.isfinite(a)], b[np.isfinite(b)]
        d = (expstats.cliffs_delta(a, b, lower_is_better)
             if a.size and b.size else np.nan)
        rows.append(dict(targeting=tg, f=float(f), spectral_radius=float(sr),
                         cliffs=float(d) if np.isfinite(d) else np.nan))
    return pd.DataFrame(rows, columns=cols)


# ---------------------------------------------------------------------------
# Boundary extraction
# ---------------------------------------------------------------------------
def _pivot(op: pd.DataFrame, value_col: str) -> pd.DataFrame:
    return op.pivot_table(index="f", columns="spectral_radius", values=value_col)


def _cross(fvals: np.ndarray, col: np.ndarray, level: float) -> float:
    """First f (interpolated) where a high-at-low-f column drops below ``level``.
    f[0] if already below at the smallest f; NaN if it never drops below."""
    ok = np.isfinite(col)
    if ok.sum() < 2:
        return np.nan
    f, c = fvals[ok], col[ok]
    if c[0] < level:
        return float(f[0])
    for k in range(1, len(c)):
        if c[k] < level:
            t = (level - c[k - 1]) / (c[k] - c[k - 1])
            return float(f[k - 1] + t * (f[k] - f[k - 1]))
    return np.nan


def _cross_up(fvals: np.ndarray, col: np.ndarray, level: float) -> float:
    """First f (interpolated) where a low-at-low-f column rises above ``level``.
    f[0] if already above at the smallest f; NaN if it never rises above. The
    mirror of ``_cross`` for an emergent (rather than collapsing) quantity."""
    ok = np.isfinite(col)
    if ok.sum() < 2:
        return np.nan
    f, c = fvals[ok], col[ok]
    if c[0] > level:
        return float(f[0])
    for k in range(1, len(c)):
        if c[k] > level:
            t = (level - c[k - 1]) / (c[k] - c[k - 1])
            return float(f[k - 1] + t * (f[k] - f[k - 1]))
    return np.nan


def observed_boundary(op: pd.DataFrame, value_col: str,
                      level_frac: float = _LEVEL_FRAC) -> dict:
    """f*(sr) where the order parameter falls to ``level_frac`` of its global max."""
    if value_col not in op.columns:
        return {}
    piv = _pivot(op, value_col)
    if piv.empty or not np.isfinite(piv.to_numpy()).any():
        return {}
    level = level_frac * float(np.nanmax(piv.to_numpy()))
    fvals = piv.index.to_numpy(float)
    return {float(sr): _cross(fvals, piv[sr].to_numpy(float), level)
            for sr in piv.columns}


def significance_boundary(cliff: pd.DataFrame, threshold: float = _CLIFF_SIG) -> dict:
    piv = _pivot(cliff, "cliffs")
    if piv.empty:
        return {}
    fvals = piv.index.to_numpy(float)
    return {float(sr): _cross(fvals, piv[sr].to_numpy(float), threshold)
            for sr in piv.columns}


def onset_boundary(op: pd.DataFrame, value_col: str,
                   level_frac: float = _LEVEL_FRAC) -> dict:
    """f*(sr) where an EMERGENT order parameter first rises to ``level_frac`` of its
    global max. The mirror of ``observed_boundary`` for Panel B, whose connectome
    advantage is *created* by sign (it is ~0 at f=0 and grows) rather than destroyed
    by it, so the collapse contour would spuriously pin the boundary at f=0."""
    if value_col not in op.columns:
        return {}
    piv = _pivot(op, value_col)
    if piv.empty or not np.isfinite(piv.to_numpy()).any():
        return {}
    level = level_frac * float(np.nanmax(piv.to_numpy()))
    fvals = piv.index.to_numpy(float)
    return {float(sr): _cross_up(fvals, piv[sr].to_numpy(float), level)
            for sr in piv.columns}


def significance_onset(cliff: pd.DataFrame, threshold: float = _CLIFF_SIG) -> dict:
    """f* where the connectome-vs-ER Cliff's delta first rises above ``threshold``
    (the emergent-advantage mirror of ``significance_boundary``)."""
    piv = _pivot(cliff, "cliffs")
    if piv.empty:
        return {}
    fvals = piv.index.to_numpy(float)
    return {float(sr): _cross_up(fvals, piv[sr].to_numpy(float), threshold)
            for sr in piv.columns}


def predictor_boundary_collapse(op: pd.DataFrame, value_col: str,
                                level_frac: float = _LEVEL_FRAC) -> dict:
    """f*(sr) where a predictor falls to ``level_frac`` of its own f=0 value at that
    sr (the ``|mean_state|`` common-mode collapse)."""
    if value_col not in op.columns:
        return {}
    piv = _pivot(op, value_col)
    if piv.empty:
        return {}
    fvals = piv.index.to_numpy(float)
    out = {}
    for sr in piv.columns:
        col = piv[sr].to_numpy(float)
        out[float(sr)] = (_cross(fvals, col, level_frac * col[0])
                          if col.size and np.isfinite(col[0]) and col[0] > 0
                          else np.nan)
    return out


def predictor_boundary_threshold(op: pd.DataFrame, value_col: str,
                                 level: float = 1.0) -> dict:
    """f*(sr) where a predictor crosses an absolute ``level`` in f (e.g.
    ``effective_radius`` crossing 1). Either crossing direction; NaN if none."""
    if value_col not in op.columns:
        return {}
    piv = _pivot(op, value_col)
    if piv.empty:
        return {}
    fvals = piv.index.to_numpy(float)
    out = {}
    for sr in piv.columns:
        col = piv[sr].to_numpy(float)
        ok = np.isfinite(col)
        f, c = fvals[ok], col[ok]
        cross = np.nan
        for k in range(1, len(c)):
            if (c[k - 1] - level) * (c[k] - level) <= 0 and c[k] != c[k - 1]:
                t = (level - c[k - 1]) / (c[k] - c[k - 1])
                cross = float(f[k - 1] + t * (f[k] - f[k - 1]))
                break
        out[float(sr)] = cross
    return out


def _boundary_agreement(obs: dict, pred: dict) -> tuple[float, int]:
    diffs = [abs(obs[sr] - pred[sr]) for sr in obs
             if sr in pred and np.isfinite(obs[sr]) and np.isfinite(pred.get(sr, np.nan))]
    return (float(np.mean(diffs)), len(diffs)) if diffs else (np.nan, 0)


# ---------------------------------------------------------------------------
# Predictor correlations
# ---------------------------------------------------------------------------
def predictor_correlations(op: pd.DataFrame) -> pd.DataFrame:
    """Spearman of each order parameter vs each candidate predictor across cells.
    Panel A order params test the MC-side predictors (A_*) + bulk95/perron_root;
    Panel B order params test the Lorenz-side predictors (B_*) + bulk95/perron_root."""
    shared = ["bulk95", "perron_root"]
    spec = {op_name: (["A_abs_mean_state", "A_effective_radius", "A_mean_gain"] + shared)
            for op_name in _PANEL_A_OPS}
    spec.update({op_name: (["B_abs_mean_state", "B_effective_radius", "B_mean_gain"] + shared)
                 for op_name in _PANEL_B_OPS})
    rows = []
    for op_name, preds in spec.items():
        if op_name not in op.columns or op[op_name].isna().all():
            continue
        panel = "A_memory" if op_name in _PANEL_A_OPS else "B_generative"
        for region, mask in [("all_sr", op.spectral_radius >= 0),
                             ("supercritical", op.spectral_radius >= 1.0)]:
            sub = op[mask]
            y = sub[op_name].to_numpy(float)
            for pred in preds:
                if pred not in sub.columns:
                    continue
                x = sub[pred].to_numpy(float)
                good = np.isfinite(x) & np.isfinite(y)
                if good.sum() < 6:
                    continue
                r, p = spearmanr(x[good], y[good])
                rows.append(dict(panel=panel, order_parameter=op_name, predictor=pred,
                                 region=region, spearman_r=float(r),
                                 p_value=float(p), n=int(good.sum())))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def _rep(op: pd.DataFrame, col: str, f: float, sr: float) -> float:
    if col not in op.columns:
        return np.nan
    m = op[(np.isclose(op.f, f)) & (np.isclose(op.spectral_radius, sr))]
    return float(m[col].iloc[0]) if not m.empty else np.nan


def _boundaries_frame(op, cliff_dD, cliff_dS, targeting):
    # Panel A memory collapses with f (advantage destroyed by sign); Panel B
    # generative is emergent (advantage created by sign), so its boundary is the
    # ONSET contour, not the collapse contour -- see onset_boundary.
    obs_A = observed_boundary(op, "dD")
    sig_A = significance_boundary(cliff_dD)
    obs_B = onset_boundary(op, "dStraight")
    sig_B = significance_onset(cliff_dS)
    predA_ms = predictor_boundary_collapse(op, "A_abs_mean_state")
    predB_ms = predictor_boundary_collapse(op, "B_abs_mean_state")
    predB_er = predictor_boundary_threshold(op, "B_effective_radius", 1.0)
    rows = []
    for sr in sorted(set(op.spectral_radius)):
        rows.append(dict(
            targeting=targeting, spectral_radius=float(sr),
            fA_obs_mag=obs_A.get(sr, np.nan), fA_obs_sig=sig_A.get(sr, np.nan),
            fB_obs_mag=obs_B.get(sr, np.nan), fB_obs_sig=sig_B.get(sr, np.nan),
            fA_pred_meanstate=predA_ms.get(sr, np.nan),
            fB_pred_meanstate=predB_ms.get(sr, np.nan),
            fB_pred_effradius=predB_er.get(sr, np.nan)))
    agreement = dict(A_vs_meanstate=_boundary_agreement(obs_A, predA_ms),
                     B_vs_effradius=_boundary_agreement(obs_B, predB_er),
                     B_vs_meanstate=_boundary_agreement(obs_B, predB_ms),
                     A_vs_B=_boundary_agreement(obs_A, obs_B))
    return pd.DataFrame(rows), agreement


def run(smoke: bool = False, scale: int | None = None) -> None:
    scale = matrix_config.SCALE if scale is None else scale
    results_dir, _ = common.scale_dirs(scale)
    cells_path = results_dir / ("phase_cells_smoke.parquet" if smoke
                                else "phase_cells.parquet")
    if not cells_path.exists():
        raise FileNotFoundError(f"{cells_path} not found -- run --capture first.")
    df = pd.read_parquet(cells_path)
    print(f"Phase analysis: loaded {len(df)} rows from {cells_path}")
    print(f"  targetings={sorted(df.targeting.unique())}  "
          f"tasks={sorted(df.task.unique())}")

    med = cell_medians(df)
    op = order_parameters(med)
    cliff_dD = cliffs_grid(df, _CLIFF_A[1], _CLIFF_A[2], _CLIFF_A[3])
    cliff_dS = cliffs_grid(df, _CLIFF_B[1], _CLIFF_B[2], _CLIFF_B[3])
    op = op.merge(cliff_dD.rename(columns={"cliffs": "cliffs_dD"}),
                  on=["targeting", "f", "spectral_radius"], how="left")
    op = op.merge(cliff_dS.rename(columns={"cliffs": "cliffs_dStraight"}),
                  on=["targeting", "f", "spectral_radius"], how="left")

    results_dir.mkdir(parents=True, exist_ok=True)
    op.to_parquet(results_dir / "phase_grid.parquet")
    print(f"Saved {results_dir / 'phase_grid.parquet'}  ({len(op)} cells)")

    corr = predictor_correlations(op)
    if not corr.empty:
        corr.to_parquet(results_dir / "phase_predictor_corr.parquet")

    bframes, agreements = [], {}
    for tg, op_tg in op.groupby("targeting"):
        bf, ag = _boundaries_frame(op_tg,
                                   cliff_dD[cliff_dD.targeting == tg],
                                   cliff_dS[cliff_dS.targeting == tg], tg)
        bframes.append(bf)
        agreements[tg] = ag
    boundaries = pd.concat(bframes, ignore_index=True)
    boundaries.to_parquet(results_dir / "phase_boundaries.parquet")
    print(f"Saved {results_dir / 'phase_boundaries.parquet'}  ({len(boundaries)} rows)")

    _write_summary(op, corr, agreements, results_dir / "phase_summary.md", smoke)
    print("\nPhase-diagram analysis complete.")


def _snap(targets, present) -> list:
    """Nearest present grid values to each target (exact when the target exists),
    de-duplicated in order -- so representative cells are exact on the full grid and
    still resolve on a coarse smoke grid."""
    present = sorted(set(present))
    out = []
    for t in targets:
        if present:
            nearest = min(present, key=lambda p: abs(p - t))
            if nearest not in out:
                out.append(nearest)
    return out


def _write_summary(op, corr, agreements, path, smoke) -> None:
    prim = op[op.targeting == "stratified"] if "stratified" in set(op.targeting) else op
    rep_f = _snap(_REP_F, prim.f.unique())
    rep_sr = _snap(_REP_SR, prim.spectral_radius.unique())
    lines = [f"# Phase diagram -- sign fraction x spectral radius (human N=448"
             f"{', SMOKE' if smoke else ''})\n",
             "Order parameters oriented so **higher = connectome advantage**; "
             "primary = `edge` / `stratified`. Panel A reads the MC task, Panel B "
             "the Lorenz task.\n"]

    for label, cols in [("Panel A -- memory", _PANEL_A_OPS),
                        ("Panel B -- generative", _PANEL_B_OPS)]:
        present = [c for c in cols if c in prim.columns and prim[c].notna().any()]
        if not present:
            continue
        lines.append(f"## {label}\n")
        for c in present:
            lines.append(f"### {c} (f x sr)\n")
            lines.append("| f \\ sr | " + " | ".join(f"{s:g}" for s in rep_sr) + " |")
            lines.append("|---|" + "---|" * len(rep_sr))
            for f in rep_f:
                cells = " | ".join(f"{_rep(prim, c, f, s):+.2f}" for s in rep_sr)
                lines.append(f"| {f:g} | {cells} |")
            lines.append("")

    if not corr.empty:
        lines.append("## Order parameter vs spectral predictor (Spearman, "
                     "stratified, supercritical)\n")
        lines.append("| panel | order param | predictor | r_s | n |")
        lines.append("|---|---|---|---|---|")
        sup = corr[corr.region == "supercritical"].copy()
        sup["absr"] = sup.spearman_r.abs()
        for r in sup.sort_values(["order_parameter", "absr"], ascending=[True, False]).itertuples():
            lines.append(f"| {r.panel} | {r.order_parameter} | {r.predictor} | "
                         f"{r.spearman_r:+.2f} | {r.n} |")
        lines.append("")

    lines.append("## Boundary agreement (mean |f*_observed - f*_predicted|)\n")
    lines.append("| targeting | comparison | mean abs df* | n sr |")
    lines.append("|---|---|---|---|")
    for tg, ag in agreements.items():
        for name, (mad, n) in ag.items():
            mad_s = f"{mad:.3f}" if np.isfinite(mad) else "--"
            lines.append(f"| {tg} | {name} | {mad_s} | {n} |")
    lines.append("")

    path.write_text("\n".join(lines) + "\n")
    print(f"Saved {path}")

"""E0.2 analysis: reindex the memory panel onto effective criticality.

The pipeline, in the order the pre-registration fixes it:

1. **Source agreement gate.** ``phase_cells.parquet`` (primary) and
   ``probe3_deff.parquet`` (cross-check) must give the same ``d_eff`` on the sr grid
   points they share. They are computed by the same code path with the same ridge
   alpha, so they must agree to floating point. A material disagreement stops the run
   -- that would be a pipeline finding to resolve before any number goes near a paper.
2. **f=0 identity check.** At ``f = 0`` the sign transform is the identity, so every
   draw and both sign modes must give bit-identical ``d_eff``. Asserted, not assumed.
3. **Per-seed reindex.** Each ``(variant, seed)`` carries its own x-axis, because
   ``bulk95`` is resampled per seed for the nulls (and is extreme-value noisy -- E0.4
   §5). Interpolate that seed's ``d_eff`` onto the common grid, *then* aggregate
   across seeds. Never the reverse.
4. **Overlap only.** The common grid is clipped to the range every compared
   (variant, seed) genuinely covers. Nothing is extrapolated; anything outside is
   masked and reported.
5. **Interpolation sensitivity.** Linear and cubic are both run; if the verdict
   depends on which, that is reported rather than resolved by picking one.

``dD`` is formed **within a seed** before aggregating: the seed convention pairs the
connectome and its null on the same ``Win`` and the same input series, so the
per-seed difference is a paired comparison, not a difference of independent means.
"""

import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

from experiments.human.analysis.criticality_matched import common

_LOAD_COLS = ["sign_mode", "targeting", "f", "variant", "spectral_radius", "seed",
              "draw", "task", "d_eff", "alpha", "bulk95", "mean_gain",
              "effective_radius"]


# ---------------------------------------------------------------------------
# Load + gates
# ---------------------------------------------------------------------------
def load_cells(scale: int = common.SCALE) -> pd.DataFrame:
    """The f=0 MC cut of the frozen phase capture, with the effective axis added."""
    path = common.phase_cells_path(scale)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found -- E0.2 needs the phase capture.")
    df = pd.read_parquet(path, columns=_LOAD_COLS)
    df = df[(df.task == common.TASK) & (df.f == common.F_CUT)
            & (df.targeting == common.TARGETING)]
    _identity_gate(df)
    df = df[(df.sign_mode == common.SIGN_MODE) & (df.draw == common.DRAW)]
    df = df[df.variant.isin(common.VARIANTS)].copy()
    # The primary axis. bulk95 is taken from the frozen file's own column (E0.4 §6:
    # recomputed f>0 flip patterns are not machine-portable; f=0 is exact either way,
    # but using the file's own value keeps the pairing exact by construction).
    df["_x_effective"] = df.spectral_radius * df.bulk95
    print(f"Loaded {len(df)} cells from {path.name} "
          f"(f={common.F_CUT}, task={common.TASK}, {df.seed.nunique()} seeds, "
          f"{df.spectral_radius.nunique()} sr points, variants {sorted(df.variant.unique())})")
    return df


def load_panel_cells(scale: int = common.SCALE) -> tuple[pd.DataFrame, dict]:
    """The cells the panel is built from, preferring Task B's extended sweep.

    Task B ran the same capture path on a **superset** grid (same 0.4 step, out to
    sigma = 8 instead of 6) and gated the shared cells to bit-identity against the
    frozen capture, so when it is present it is strictly more information about the
    same experiment. The frozen phase capture is the fallback, and the source is
    recorded either way -- the matched-axis result depends on how far the sweep
    reached, so which source produced it is not a detail.
    """
    path = common.extended_sweep_path(scale)
    if path.exists():
        df = pd.read_parquet(
            path, columns=["variant", "spectral_radius", "seed", "d_eff", "mc",
                           "alpha", "bulk95", "mean_gain", "effective_radius"])
        df = df[df.variant.isin(common.VARIANTS)].copy()
        df["_x_effective"] = df.spectral_radius * df.bulk95
        meta = dict(source="taskB_extended", path=str(path),
                    sr_max=float(df.spectral_radius.max()),
                    n_sr=int(df.spectral_radius.nunique()),
                    variants=sorted(df.variant.unique()))
        print(f"Loaded {len(df)} cells from {path.name} "
              f"(sigma to {meta['sr_max']:g}, {meta['n_sr']} points, "
              f"variants {meta['variants']})")
        return df, meta
    df = load_cells(scale)
    return df, dict(source="frozen_phase_cells", path=str(common.phase_cells_path(scale)),
                    sr_max=float(df.spectral_radius.max()),
                    n_sr=int(df.spectral_radius.nunique()),
                    variants=sorted(df.variant.unique()))


def _identity_gate(df: pd.DataFrame) -> None:
    """At f=0 the transform is the identity: draws and sign modes must coincide."""
    grouped = df.groupby(["variant", "spectral_radius", "seed"]).d_eff
    spread = float((grouped.max() - grouped.min()).max())
    n_bad = int((grouped.nunique() > 1).sum())
    print(f"  [identity-gate] f=0 across draw x sign_mode: {n_bad} of "
          f"{grouped.ngroups} cells differ (worst spread {spread:.3e})")
    if n_bad or spread > 0.0:
        raise RuntimeError(
            "[identity-gate] f=0 is not behaving as the identity transform: d_eff "
            f"varies across draw/sign_mode in {n_bad} cells. STOP -- the f=0 cut is "
            "the whole basis of this analysis.")


def source_agreement_gate(cells: pd.DataFrame, scale: int = common.SCALE) -> dict:
    """``phase_cells`` vs ``probe3_deff`` on their shared sr grid points."""
    path = common.probe3_path(scale)
    if not path.exists():
        print(f"  [source-gate] {path} absent -- cross-check skipped.")
        return {"status": "skipped", "reference": str(path)}

    probe3 = pd.read_parquet(path)
    probe3 = probe3[(probe3.task == common.TASK)
                    & (probe3.condition == "human_empirical")].copy()
    left = cells.assign(_sr=cells.spectral_radius.round(6))
    right = probe3.assign(_sr=probe3.spectral_radius.round(6))[
        ["variant", "seed", "_sr", "d_eff", "alpha"]]
    merged = left.merge(right, on=["variant", "seed", "_sr"], how="inner",
                        suffixes=("", "_ref"))
    shared = sorted(merged._sr.unique())
    if merged.empty:
        raise RuntimeError("[source-gate] the two d_eff sources share no grid cells.")

    alphas = sorted(set(merged.alpha.unique()) | set(merged.alpha_ref.unique()))
    if len(alphas) != 1:
        raise RuntimeError(
            f"[source-gate] the two sources used different ridge alphas {alphas}; "
            "d_eff is alpha-dependent, so they are not comparable. STOP.")

    # sigma = 0 zeroes the recurrent matrix, leaving a rank-1 design Gram with ~N
    # eigenvalues at the numerical noise floor. Whether each clears alpha = 1e-6 is
    # decided by rounding, so d_eff there (~1.0015) carries a ~1e-3 wobble that
    # reflects float arithmetic, not the pipeline. Reported, not gated -- and it
    # contributes nothing to the panel, where dD is 0 at sigma = 0 by construction.
    live = merged[merged._sr > 0.0]
    zero = merged[merged._sr == 0.0]
    abs_diff = (live.d_eff - live.d_eff_ref).abs()
    rel_diff = abs_diff / live.d_eff_ref.abs().clip(lower=1e-12)
    worst_abs, worst_rel = float(abs_diff.max()), float(rel_diff.max())
    zero_abs = (float((zero.d_eff - zero.d_eff_ref).abs().max())
                if not zero.empty else 0.0)
    print(f"  [source-gate] {len(merged)} shared cells at sr={shared}; "
          f"alpha={alphas[0]:g}")
    print(f"  [source-gate] sigma>0: max abs {worst_abs:.2e}, max rel {worst_rel:.2e}  "
          f"{'OK' if worst_rel <= common.SOURCE_AGREEMENT_TOL else 'FAIL'}")
    print(f"  [source-gate] sigma=0 (degenerate rank-1 Gram): max abs {zero_abs:.2e} "
          "on d_eff ~ 1.0 -- reported, not gated")
    if worst_rel > common.SOURCE_AGREEMENT_TOL:
        raise RuntimeError(
            f"[source-gate] the two d_eff sources disagree at sigma > 0 "
            f"(max rel diff {worst_rel:.2e} > {common.SOURCE_AGREEMENT_TOL:.0e}). "
            "STOP and report -- this is a pipeline finding that must be resolved "
            "before either number is used.")
    print("  [source-gate] the two d_eff sources agree.  [OK]")
    return {"status": "passed", "reference": str(path), "n_cells": int(len(merged)),
            "shared_sr": [float(s) for s in shared], "alpha": float(alphas[0]),
            "max_abs_diff": worst_abs, "max_rel_diff": worst_rel,
            "sigma0_max_abs_diff": zero_abs}


# ---------------------------------------------------------------------------
# Per-seed reindexing
# ---------------------------------------------------------------------------
def _interp(x, y, grid, method):
    """Interpolate one seed's curve onto ``grid``; NaN strictly outside its support."""
    order = np.argsort(x)
    x, y = np.asarray(x, float)[order], np.asarray(y, float)[order]
    keep = np.concatenate([[True], np.diff(x) > 0])      # drop duplicate abscissae
    x, y = x[keep], y[keep]
    if x.size < 2:
        return np.full(grid.shape, np.nan)
    if method == "linear":
        out = np.interp(grid, x, y)
    elif method == "cubic":
        out = CubicSpline(x, y, extrapolate=False)(grid)
    else:
        raise ValueError(f"unknown interpolation method {method!r}")
    return np.where((grid >= x[0]) & (grid <= x[-1]), out, np.nan)


def overlap_range(cells: pd.DataFrame, x_col: str, variants) -> tuple[float, float]:
    """The x-range every compared (variant, seed) genuinely covers.

    The lower bound is the largest per-curve minimum and the upper bound the smallest
    per-curve maximum, so the common grid never leaves any curve's support.
    """
    lo, hi = -np.inf, np.inf
    for (_, _), group in cells[cells.variant.isin(variants)].groupby(["variant", "seed"]):
        x = group[x_col].to_numpy(float)
        lo, hi = max(lo, float(np.nanmin(x))), min(hi, float(np.nanmax(x)))
    return lo, hi


def reindex(cells: pd.DataFrame, x_col: str, grid: np.ndarray,
            method: str) -> dict:
    """``variant -> (n_seeds, n_grid)`` array of ``d_eff`` interpolated per seed."""
    out = {}
    for variant, vgroup in cells.groupby("variant"):
        seeds = sorted(vgroup.seed.unique())
        curves = np.full((len(seeds), grid.size), np.nan)
        for i, seed in enumerate(seeds):
            sub = vgroup[vgroup.seed == seed]
            curves[i] = _interp(sub[x_col].to_numpy(float),
                                sub.d_eff.to_numpy(float), grid, method)
        out[variant] = curves
    return out


def paired_difference(curves: dict, grid: np.ndarray) -> pd.DataFrame:
    """Per-seed ``dD = d_eff(connectome) - d_eff(ER)``, aggregated across seeds.

    The difference is formed *within* a seed: the seed convention pairs connectome and
    null on the same ``Win`` and input series, so this is a paired contrast.
    """
    conn, ctr = curves[common.CONN], curves[common.CONTRAST]
    dd = conn - ctr
    n = np.isfinite(dd).sum(axis=0)
    with np.errstate(invalid="ignore"):
        frame = pd.DataFrame({
            "x": grid,
            "dD_median": np.nanmedian(dd, axis=0),
            "dD_mean": np.nanmean(dd, axis=0),
            "dD_q25": np.nanquantile(dd, 0.25, axis=0),
            "dD_q75": np.nanquantile(dd, 0.75, axis=0),
            "n_seeds": n,
            "frac_positive": np.nansum(dd > 0, axis=0) / np.maximum(n, 1),
        })
    for variant, arr in curves.items():
        frame[f"d_eff_{variant}"] = np.nanmedian(arr, axis=0)
        frame[f"n_{variant}"] = np.isfinite(arr).sum(axis=0)
    frame.loc[frame.n_seeds == 0, ["dD_median", "dD_mean", "dD_q25", "dD_q75"]] = np.nan
    return frame


def build_axis(cells: pd.DataFrame, axis: str, method: str,
               n_grid: int = common.N_GRID) -> tuple[pd.DataFrame, dict]:
    """Reindex + difference on one axis. Returns (frame, coverage info)."""
    spec = common.AXES[axis]
    x_col = spec["column"]
    lo, hi = overlap_range(cells, x_col, [common.CONN, common.CONTRAST])
    grid = np.linspace(lo, hi, n_grid)
    curves = reindex(cells, x_col, grid, method)
    frame = paired_difference(curves, grid)
    frame["axis"], frame["interp"] = axis, method
    full_lo = float(cells[x_col].min())
    full_hi = float(cells[x_col].max())
    info = dict(axis=axis, interp=method, overlap_lo=lo, overlap_hi=hi,
                full_lo=full_lo, full_hi=full_hi,
                fraction_of_full_range=(hi - lo) / (full_hi - full_lo)
                if full_hi > full_lo else np.nan,
                complete_seed_coverage=bool((frame.n_seeds == common.N_SEEDS).all()))
    return frame, info


# ---------------------------------------------------------------------------
# Reading the panel
# ---------------------------------------------------------------------------
def _zero_crossing(x: np.ndarray, y: np.ndarray) -> float:
    """First x where y crosses from <=0 to >0 (linear interpolation); NaN if none."""
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    for k in range(1, y.size):
        if y[k - 1] <= 0.0 < y[k]:
            t = (0.0 - y[k - 1]) / (y[k] - y[k - 1])
            return float(x[k - 1] + t * (x[k] - x[k - 1]))
    return np.nan


def summarise_axis(frame: pd.DataFrame, info: dict) -> dict:
    """Peak, onset and edge behaviour of dD on one axis."""
    x = frame.x.to_numpy(float)
    y = frame.dD_median.to_numpy(float)
    ok = np.isfinite(y)
    if not ok.any():
        return dict(info, peak_dD=np.nan)
    idx = int(np.nanargmax(y))
    at_edge = bool(idx >= (ok.sum() - max(2, len(y) // 20)))
    return dict(
        info,
        peak_dD=float(y[idx]), peak_x=float(x[idx]),
        peak_at_upper_edge=at_edge,
        dD_at_upper_edge=float(y[ok][-1]),
        min_dD=float(np.nanmin(y)), min_x=float(x[int(np.nanargmin(y))]),
        zero_crossing_x=_zero_crossing(x, y),
        frac_grid_positive=float(np.nansum(y > 0) / ok.sum()),
    )


def interpolation_sensitivity(cells: pd.DataFrame, axis: str) -> pd.DataFrame:
    """Same axis under every interpolation method, for the sensitivity statement."""
    rows = []
    for method in common.INTERP_METHODS:
        frame, info = build_axis(cells, axis, method)
        rows.append(summarise_axis(frame, info))
    return pd.DataFrame(rows)


def sigma_eff_trajectories(cells: pd.DataFrame) -> pd.DataFrame:
    """Per-variant seed-median trajectory of (sr, sigma_eff, d_eff).

    ``sigma_eff`` is non-monotone in ``sr``, so this is a *parametric* curve traced by
    ``sr``, not a matching axis. Reported with the fold (the turning point) located.
    """
    grouped = (cells.groupby(["variant", "spectral_radius"], as_index=False)
               .agg(sigma_eff=("effective_radius", "median"),
                    d_eff=("d_eff", "median"),
                    mean_gain=("mean_gain", "median"),
                    bulk95=("bulk95", "median")))
    rows = []
    for variant, group in grouped.groupby("variant"):
        group = group.sort_values("spectral_radius").copy()
        peak = int(np.argmax(group.sigma_eff.to_numpy(float)))
        group["is_sigma_eff_peak"] = np.arange(len(group)) == peak
        group["branch"] = np.where(np.arange(len(group)) <= peak, "rising", "folded")
        rows.append(group)
    return pd.concat(rows, ignore_index=True)

"""E0.2 extension: the full (f, sigma) phase panels reindexed on effective criticality.

E0.2 corrected the ``f = 0`` cut. The phase diagram's **headline** result, though, is
cross-panel: the memory boundary and the generative boundary run opposite in sigma and
cross near (sigma ~ 4, f ~ 0.12). That crossing is currently stated in **nominal**
coordinates, and E0.2 showed nominal sigma does not match effective criticality --
so if the memory boundary moves under reindexing, the crossing moves with it and the
dissociation claim has to be restated before it goes into a draft.

This module reindexes both panels onto ``sigma * bulk95`` and relocates the crossing.

Three things make it different from the ``f = 0`` cut:

1. **``bulk95`` is a function of ``f``.** Sign flips reshape the spectrum, so the
   x-axis is built from a per-``(variant, f, seed, draw)`` ``bulk95`` -- always taken
   from the cell file's **own** column, because the ``f > 0`` flip pattern is not
   machine-portable (E0.4 §6) and only a file's own values pair correctly with its own
   ``d_eff``.
2. **The replicate unit is (seed, draw)**, not seed alone: at ``f > 0`` the draws are
   genuinely different flip patterns, unlike at ``f = 0`` where the transform is the
   identity.
3. **Coverage shrinks with ``f`` in a way that must be shown.** The connectome has the
   smallest ``bulk95`` at every ``f``, so it bounds the overlap at
   ``max(sigma) * bulk95_connectome(f)``. It is drawn on the figures rather than hidden.

**Two cell sources.** ``extension`` (default) is item 2's re-run of the same grid out
to ``sigma = 11.2``, which lifts the old ``sigma = 6`` censoring of every ``f > 0``
row; ``frozen`` is the original ``phase_cells.parquet`` capture, kept runnable because
it is what the published nominal-axis control was read from. The two are *different
flip realisations* -- ``f = 0`` is the identity and agrees cell-for-cell, ``f > 0``
agrees only distributionally (``extend_f.reproduction_gate``) -- so outputs are tagged
by source and neither overwrites the other.

Boundary extraction reuses the phase-diagram package's own operators unchanged
(``observed_boundary`` for the collapsing memory panel, ``onset_boundary`` for the
emergent generative one), so "the boundary" means exactly what it meant before -- only
the axis it is expressed on has changed.
"""

import numpy as np
import pandas as pd

from experiments.human.analysis.phase_diagram import analysis as pd_analysis
from experiments.human.analysis.criticality_matched import analysis, common

SIGN_MODE = "edge"                # the placement-neutral, exactly-normal primary
TARGETING = "stratified"
CONN, CTR = "connectome", "erdos_renyi"

# (name, task, metric, conn_first) -- orientation so that higher = connectome better.
PANELS = {
    "dD": dict(task="mc", metric="d_eff", conn_first=True,
               label=r"$\Delta d_{eff}$ (connectome $-$ ER)", kind="collapse"),
    "dStraight": dict(task="lorenz", metric="mean_curvature", conn_first=False,
                      label=r"$\Delta$straightness (ER $-$ connectome curvature)",
                      kind="onset"),
}
# Grid points per source, chosen to hold the *resolution* fixed rather than the point
# count: the extension covers roughly twice the x-range (coverage to 4.58 against
# 2.336), so 121 points there give dx = 0.038 against the frozen panel's 0.039. A bare
# constant would have halved the extension's resolution or doubled the frozen panel's,
# and the frozen panel is what the published control numbers were read from.
N_GRID_BY_SOURCE = {"frozen": 61, "extension": 121}
N_GRID = N_GRID_BY_SOURCE["frozen"]
_LOAD_COLS = ["sign_mode", "targeting", "f", "variant", "spectral_radius", "seed",
              "draw", "task", "d_eff", "mean_curvature", "bulk95"]

DEFAULT_SOURCE = "extension"
# The extension carries an extra ``score`` column and no ``narma10`` rows (hence no
# ``nrmse``); every column this module reads is present in both, with matching dtypes,
# and the two sigma grids agree exactly on their 16 shared points.
_SOURCE_PATH = {"extension": common.f_extension_path,
                "frozen": common.phase_cells_path}
# The sigma the frozen capture stopped at -- the old coverage edge, still used as the
# comparison range for the reproduction gate and the level-definition sensitivity.
FROZEN_SR_MAX = 6.0


def source_path(scale: int = common.SCALE, source: str = DEFAULT_SOURCE):
    if source not in _SOURCE_PATH:
        raise ValueError(f"unknown source {source!r} (expected one of "
                         f"{sorted(_SOURCE_PATH)})")
    return _SOURCE_PATH[source](scale)


def source_tag(source: str, axis: str) -> str:
    """Artifact suffix. ``frozen``/``effective`` keeps the original (untagged) names so
    the published artifacts stay exactly where TIER0 §2.3 points."""
    return ("" if source == "frozen" else f"_{source}") + \
           ("" if axis == "effective" else f"_{axis}")


def load_cells(scale: int = common.SCALE, axis: str = "effective",
               source: str = DEFAULT_SOURCE) -> pd.DataFrame:
    """``axis='effective'`` reindexes on ``sigma * bulk95``; ``axis='nominal'`` keeps
    ``sigma``.

    The nominal path exists as the **control**. On the frozen source it reproduces the
    published crossing at (sigma ~ 4, f ~ 0.12) cell-for-cell. On the extension it can
    only be a *distributional* control -- the flip realisation is new -- so it is read
    against ``extend_f.crossing_bootstrap``'s replicate-resampling interval rather than
    against a single published number.
    """
    path = source_path(scale, source)
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found -- run `--extend-f` first (or pass --source frozen).")
    df = pd.read_parquet(path, columns=_LOAD_COLS)
    df = df[(df.sign_mode == SIGN_MODE) & (df.targeting == TARGETING)
            & (df.variant.isin([CONN, CTR]))].copy()
    if axis == "effective":
        df["_x"] = df.spectral_radius * df.bulk95
    elif axis == "nominal":
        df["_x"] = df.spectral_radius
    else:
        raise ValueError(f"unknown axis {axis!r}")
    print(f"Loaded {len(df)} cells from {path.name} [source={source}] "
          f"({df.f.nunique()} f x {df.spectral_radius.nunique()} sigma to "
          f"{df.spectral_radius.max():g} x {df.seed.nunique()} seeds x "
          f"{df.draw.nunique()} draws, tasks {sorted(df.task.unique())})")
    return df


def coverage(df: pd.DataFrame) -> pd.DataFrame:
    """Per ``f``: the largest x every compared (variant, seed, draw) reaches.

    This is simultaneously the overlap boundary and -- for ``f > 0``, where the sweep
    still stops at sigma = 6 -- the censoring boundary.
    """
    rows = []
    for f, group in df.groupby("f"):
        hi = group.groupby(["variant", "seed", "draw"])._x.max().min()
        lo = group.groupby(["variant", "seed", "draw"])._x.min().max()
        rows.append(dict(f=float(f), x_lo=float(lo), x_hi=float(hi),
                         sigma_max=float(group.spectral_radius.max())))
    return pd.DataFrame(rows).sort_values("f").reset_index(drop=True)


def replicate_stacks(df: pd.DataFrame, panel: str, grid: np.ndarray,
                     method: str = "linear") -> tuple[dict, list]:
    """``f -> (n_replicates, n_grid)`` paired differences, plus the replicate labels.

    Per ``f``, per (seed, draw) replicate: interpolate both variants' metric onto the
    common grid **within each curve's own support**, then difference within the
    replicate (paired -- same Win, same input series). NaN wherever a replicate has no
    support, so nothing is extrapolated.

    The un-aggregated stacks are the unit ``crossing_bootstrap`` resamples, which is
    why this is separated from the median that ``reindex_panel`` takes over it.
    """
    spec = PANELS[panel]
    sub = df[df.task == spec["task"]]
    stacks, labels = {}, []
    for f, fgroup in sub.groupby("f"):
        replicates, keys = [], []
        for (seed, draw), rep in fgroup.groupby(["seed", "draw"]):
            curves = {}
            for variant in (CONN, CTR):
                v = rep[rep.variant == variant]
                if v.empty:
                    break
                curves[variant] = analysis._interp(
                    v._x.to_numpy(float), v[spec["metric"]].to_numpy(float),
                    grid, method)
            if len(curves) != 2:
                continue
            diff = (curves[CONN] - curves[CTR] if spec["conn_first"]
                    else curves[CTR] - curves[CONN])
            replicates.append(diff)
            keys.append((int(seed), int(draw)))
        if not replicates:
            continue
        stacks[float(f)] = np.vstack(replicates)
        labels = keys if not labels else labels
    return stacks, labels


def panel_from_stacks(stacks: dict, grid: np.ndarray, panel: str) -> pd.DataFrame:
    """Median-over-replicates order parameter on the (f, x) grid."""
    rows = []
    for f, stack in stacks.items():
        with np.errstate(invalid="ignore"):
            median = np.nanmedian(stack, axis=0)
        n = np.isfinite(stack).sum(axis=0)
        median = np.where(n > 0, median, np.nan)
        for x, value, count in zip(grid, median, n):
            rows.append(dict(f=float(f), spectral_radius=float(x),
                             n_replicates=int(count), **{panel: float(value)}))
    return pd.DataFrame(rows)


def reindex_panel(df: pd.DataFrame, panel: str, grid: np.ndarray,
                  method: str = "linear") -> pd.DataFrame:
    """Median-over-replicates order parameter on the (f, x) grid."""
    stacks, _ = replicate_stacks(df, panel, grid, method)
    return panel_from_stacks(stacks, grid, panel)


def boundaries(op: pd.DataFrame, panel: str,
               level_frac: float = pd_analysis._LEVEL_FRAC) -> dict:
    """f*(x) using the phase-diagram package's own boundary operators, unchanged.

    Panel A's advantage is destroyed by sign (a collapse contour); Panel B's is
    created by it (an onset contour). Mirroring the operator to the phenomenon is the
    project's existing convention -- reused, not reinvented.

    ``level_frac`` is exposed only so the level can be pinned to a *sub-range* of the
    panel (``level_frac_on_subrange``): both operators set their contour at
    ``level_frac x the panel's own global max``, so extending the sweep can move the
    boundary everywhere without any cell changing. That has to be measured, not
    assumed away.
    """
    if PANELS[panel]["kind"] == "collapse":
        return pd_analysis.observed_boundary(op, panel, level_frac)
    return pd_analysis.onset_boundary(op, panel, level_frac)


def level_frac_full_coverage(op: pd.DataFrame, panel: str) -> float:
    """The ``level_frac`` whose contour level is 25% of the largest **fully covered**
    cell, expressed against the panel's own global max so the operator is unchanged.

    Both boundary operators set their level from the panel's global max, and a max is
    maximally sensitive to its least-supported cell. Past the all-replicates coverage
    edge the panel is still populated, but only by the replicates whose own ``bulk95``
    reached that far -- a ``bulk95``-selected subsample. On the extension the raw
    global max of ``dStraight`` is +2.849 from a cell backed by **1 replicate of 30**,
    against +0.032 over cells all 30 reach: a 89x difference in the level, which
    decides the boundary everywhere. Cells backed by one replicate and cells backed by
    thirty are not like for like, so the level is taken over the latter.

    This is a level-setting rule only -- the boundary is still extracted over the whole
    panel, and the ragged cells are still painted on the figure.
    """
    full = op[panel].to_numpy(float)
    if not np.isfinite(full).any():
        return pd_analysis._LEVEL_FRAC
    full_max = float(np.nanmax(full))
    covered = op[op.n_replicates >= int(op.n_replicates.max())][panel].to_numpy(float)
    if not np.isfinite(covered).any() or full_max == 0.0:
        return pd_analysis._LEVEL_FRAC
    return pd_analysis._LEVEL_FRAC * float(np.nanmax(covered)) / full_max


def level_frac_on_subrange(op: pd.DataFrame, panel: str, x_max: float) -> float:
    """The ``level_frac`` that reproduces the contour level a panel truncated at
    ``x_max`` would have used. ``level = 0.25 * max(sub)`` expressed as a fraction of
    ``max(full)``, so the unchanged operator can be called on the full panel."""
    full = op[panel].to_numpy(float)
    sub = op.loc[op.spectral_radius <= x_max, panel].to_numpy(float)
    if not np.isfinite(full).any() or not np.isfinite(sub).any():
        return pd_analysis._LEVEL_FRAC
    full_max, sub_max = float(np.nanmax(full)), float(np.nanmax(sub))
    if full_max == 0.0:
        return pd_analysis._LEVEL_FRAC
    return pd_analysis._LEVEL_FRAC * sub_max / full_max


def crossing(bound_a: dict, bound_b: dict) -> dict:
    """Where the memory and generative boundaries cross, on the reindexed axis."""
    xs = sorted(set(bound_a) & set(bound_b))
    pairs = [(x, bound_a[x], bound_b[x]) for x in xs
             if np.isfinite(bound_a[x]) and np.isfinite(bound_b[x])]
    if len(pairs) < 2:
        return {"crosses": False, "reason": "fewer than two x with both boundaries"}
    for (x0, a0, b0), (x1, a1, b1) in zip(pairs, pairs[1:]):
        d0, d1 = a0 - b0, a1 - b1
        if d0 == 0.0:
            return {"crosses": True, "x": float(x0), "f": float(a0)}
        if d0 * d1 < 0.0:
            t = d0 / (d0 - d1)
            return {"crosses": True, "x": float(x0 + t * (x1 - x0)),
                    "f": float(a0 + t * (a1 - a0))}
    return {"crosses": False, "reason": "boundaries do not intersect over the overlap",
            "gap_sign": float(np.sign(pairs[0][1] - pairs[0][2])),
            "x_range": [float(pairs[0][0]), float(pairs[-1][0])]}


def _boundary_support(op: pd.DataFrame, bound: dict, panel: str) -> pd.DataFrame:
    """How many replicates back each boundary point.

    Above the all-replicates coverage edge the panel is still populated, but only by
    the replicates whose own ``bulk95`` reached that far -- a selected subsample. The
    boundary is not filtered on this (it is reported, not policed), so the count that
    produced each ``f*`` travels with it.
    """
    piv = op.pivot_table(index="f", columns="spectral_radius", values="n_replicates")
    fvals = piv.index.to_numpy(float)
    rows = []
    for x in sorted(bound):
        f_star = bound[x]
        counts = (piv[x].to_numpy(float) if x in piv.columns
                  else np.full(fvals.shape, np.nan))
        finite = np.isfinite(counts)
        n_at = (float(np.interp(f_star, fvals, counts))
                if np.isfinite(f_star) and finite.all() else np.nan)
        rows.append(dict(panel=panel, x=float(x), f_star=float(f_star),
                         n_replicates_at_f_star=n_at,
                         n_replicates_max=float(counts[finite].max())
                         if finite.any() else np.nan))
    return pd.DataFrame(rows)


def run(scale: int = common.SCALE, axis: str = "effective",
        source: str = DEFAULT_SOURCE) -> dict:
    common.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    print("=" * 70 + f"\nE0.2 -- (f, sigma) panels, axis = {axis}, source = {source}\n"
          + "=" * 70)
    df = load_cells(scale, axis, source)
    cover = coverage(df)
    x_hi = float(cover.x_hi.max())
    n_grid = N_GRID_BY_SOURCE.get(source, N_GRID)
    grid = np.linspace(0.0, x_hi, n_grid)
    print(f"\nCoverage: x_hi ranges {cover.x_hi.min():.3f} (f={cover.loc[cover.x_hi.idxmin(), 'f']:g}) "
          f"to {cover.x_hi.max():.3f} (f={cover.loc[cover.x_hi.idxmax(), 'f']:g}); "
          f"grid to {x_hi:.3f} ({n_grid} pts, dx={grid[1] - grid[0]:.4f}), "
          f"masked beyond each f's own coverage")

    # The x the frozen capture's sigma = 6 reached on this axis -- the sub-range the
    # contour level is re-pinned to for the sensitivity read.
    x_frozen = (FROZEN_SR_MAX if axis == "nominal"
                else float(coverage(df[df.spectral_radius <= FROZEN_SR_MAX]).x_hi.max()))

    ops, bounds, bounds_sub, bounds_raw, support = {}, {}, {}, {}, []
    for panel in PANELS:
        op = reindex_panel(df, panel, grid)
        if op.empty:
            print(f"  [{panel}] no data -- skipped")
            continue
        ops[panel] = op
        # Primary: the contour level is set by the largest fully covered cell.
        cov_frac = level_frac_full_coverage(op, panel)
        bounds[panel] = boundaries(op, panel, cov_frac)
        # Sensitivities: level pinned to the frozen sweep's x-range, and the operator's
        # literal default (level from the panel's raw global max, ragged cells included).
        bounds_sub[panel] = boundaries(op, panel,
                                       level_frac_on_subrange(op, panel, x_frozen))
        bounds_raw[panel] = boundaries(op, panel)
        support.append(_boundary_support(op, bounds[panel], panel))
        finite = {k: v for k, v in bounds[panel].items() if np.isfinite(v)}
        raw_max = float(np.nanmax(op[panel].to_numpy(float)))
        print(f"  [{panel}] boundary defined at {len(finite)}/{len(bounds[panel])} "
              f"x points; f* range "
              f"[{min(finite.values()):.3f}, {max(finite.values()):.3f}]; "
              f"level {cov_frac * raw_max:.4f} (full-coverage cells) vs "
              f"{pd_analysis._LEVEL_FRAC * raw_max:.4f} (raw max)"
              if finite else f"  [{panel}] boundary undefined everywhere")

    _cross = lambda b: (crossing(b["dD"], b["dStraight"]) if len(b) == 2
                        else {"crosses": False, "reason": "one panel missing"})
    cross, cross_sub, cross_raw = _cross(bounds), _cross(bounds_sub), _cross(bounds_raw)
    print(f"\nCross-panel [primary, level from full-coverage cells]: {cross}")
    print(f"  [sensitivity] level pinned to x <= {x_frozen:.3f}: {cross_sub}")
    print(f"  [sensitivity] level from the raw global max:        {cross_raw}")

    combined = pd.concat(
        [op.assign(panel=name) for name, op in ops.items()], ignore_index=True)
    tag = source_tag(source, axis)
    combined.to_parquet(common.RESULTS_DIR / f"e02_heatmap_panels{tag}.parquet")
    cover.to_csv(common.RESULTS_DIR / f"e02_heatmap_coverage{tag}.csv", index=False)
    rows = []
    for panel, bound in bounds.items():
        for x, f_star in bound.items():
            rows.append(dict(panel=panel, x=float(x), f_star=float(f_star),
                             f_star_level_on_subrange=float(bounds_sub[panel][x]),
                             f_star_level_raw_max=float(bounds_raw[panel][x])))
    pd.DataFrame(rows).to_csv(
        common.RESULTS_DIR / f"e02_heatmap_boundaries{tag}.csv", index=False)
    if support:
        pd.concat(support, ignore_index=True).to_csv(
            common.RESULTS_DIR / f"e02_heatmap_boundary_support{tag}.csv", index=False)
    print(f"Saved panels, coverage and boundaries to {common.RESULTS_DIR}")
    return {"ops": ops, "bounds": bounds, "bounds_level_on_subrange": bounds_sub,
            "bounds_level_raw_max": bounds_raw, "coverage": cover, "crossing": cross,
            "crossing_level_on_subrange": cross_sub, "crossing_level_raw_max": cross_raw,
            "x_frozen_edge": x_frozen, "grid": grid, "axis": axis, "source": source,
            "scale": scale}


def run_both(scale: int = common.SCALE, source: str = DEFAULT_SOURCE) -> dict:
    """Both axes plus the figure. The nominal axis is the control (on the frozen source
    it reproduces the published crossing), so the figure is only meaningful with both."""
    from experiments.human.analysis.criticality_matched import panels
    results = {axis: run(scale, axis, source) for axis in ("nominal", "effective")}
    common.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    stem = "fig_heatmaps_matched" + ("" if source == "frozen" else f"_{source}")
    panels.fig_heatmaps(results, common.FIGURES_DIR / stem)
    return results

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
   x-axis is built from a per-``(variant, f, seed, draw)`` ``bulk95`` -- taken from
   ``phase_cells.parquet``'s own column, because the ``f > 0`` flip pattern is not
   machine-portable (E0.4 §6) and only the frozen file's own values pair correctly
   with its own ``d_eff``.
2. **The replicate unit is (seed, draw)**, not seed alone: at ``f > 0`` the draws are
   genuinely different flip patterns, unlike at ``f = 0`` where the transform is the
   identity.
3. **Coverage shrinks with ``f`` in a way that must be shown.** The connectome has the
   smallest ``bulk95`` at every ``f``, so it bounds the overlap at
   ``max(sigma) * bulk95_connectome(f)``. Because the sigma = 8 extension was ``f = 0``
   only, every ``f > 0`` row is still censored at sigma = 6 -- and that censoring
   boundary *is* the coverage boundary. It is drawn on the figures rather than hidden.

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
N_GRID = 61
_LOAD_COLS = ["sign_mode", "targeting", "f", "variant", "spectral_radius", "seed",
              "draw", "task", "d_eff", "mean_curvature", "bulk95"]


def load_cells(scale: int = common.SCALE, axis: str = "effective") -> pd.DataFrame:
    """``axis='effective'`` reindexes on ``sigma * bulk95``; ``axis='nominal'`` keeps
    ``sigma``.

    The nominal path exists as the **control**: run through the identical pipeline it
    must reproduce the published crossing at (sigma ~ 4, f ~ 0.12). If it does not,
    the pipeline is wrong and nothing it says about the corrected axis can be trusted.
    """
    path = common.phase_cells_path(scale)
    df = pd.read_parquet(path, columns=_LOAD_COLS)
    df = df[(df.sign_mode == SIGN_MODE) & (df.targeting == TARGETING)
            & (df.variant.isin([CONN, CTR]))].copy()
    if axis == "effective":
        df["_x"] = df.spectral_radius * df.bulk95
    elif axis == "nominal":
        df["_x"] = df.spectral_radius
    else:
        raise ValueError(f"unknown axis {axis!r}")
    print(f"Loaded {len(df)} cells from {path.name} "
          f"({df.f.nunique()} f x {df.spectral_radius.nunique()} sigma x "
          f"{df.seed.nunique()} seeds x {df.draw.nunique()} draws, "
          f"tasks {sorted(df.task.unique())})")
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


def reindex_panel(df: pd.DataFrame, panel: str, grid: np.ndarray,
                  method: str = "linear") -> pd.DataFrame:
    """Median-over-replicates order parameter on the (f, x) grid.

    Per ``f``, per (seed, draw) replicate: interpolate both variants' metric onto the
    common grid **within each curve's own support**, difference within the replicate
    (paired -- same Win, same input series), then aggregate. NaN wherever a replicate
    has no support, so nothing is extrapolated.
    """
    spec = PANELS[panel]
    sub = df[df.task == spec["task"]]
    rows = []
    for f, fgroup in sub.groupby("f"):
        replicates = []
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
        if not replicates:
            continue
        stack = np.vstack(replicates)
        with np.errstate(invalid="ignore"):
            median = np.nanmedian(stack, axis=0)
        n = np.isfinite(stack).sum(axis=0)
        median = np.where(n > 0, median, np.nan)
        for x, value, count in zip(grid, median, n):
            rows.append(dict(f=float(f), spectral_radius=float(x), n_replicates=int(count),
                             **{panel: float(value)}))
    return pd.DataFrame(rows)


def boundaries(op: pd.DataFrame, panel: str) -> dict:
    """f*(x) using the phase-diagram package's own boundary operators, unchanged.

    Panel A's advantage is destroyed by sign (a collapse contour); Panel B's is
    created by it (an onset contour). Mirroring the operator to the phenomenon is the
    project's existing convention -- reused, not reinvented.
    """
    if PANELS[panel]["kind"] == "collapse":
        return pd_analysis.observed_boundary(op, panel)
    return pd_analysis.onset_boundary(op, panel)


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


def run(scale: int = common.SCALE, axis: str = "effective") -> dict:
    common.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    print("=" * 70 + f"\nE0.2 -- (f, sigma) panels, axis = {axis}\n" + "=" * 70)
    df = load_cells(scale, axis)
    cover = coverage(df)
    x_hi = float(cover.x_hi.max())
    grid = np.linspace(0.0, x_hi, N_GRID)
    print(f"\nCoverage: x_hi ranges {cover.x_hi.min():.3f} (f={cover.loc[cover.x_hi.idxmin(), 'f']:g}) "
          f"to {cover.x_hi.max():.3f} (f={cover.loc[cover.x_hi.idxmax(), 'f']:g}); "
          f"grid to {x_hi:.3f}, masked beyond each f's own coverage")

    ops, bounds = {}, {}
    for panel in PANELS:
        op = reindex_panel(df, panel, grid)
        if op.empty:
            print(f"  [{panel}] no data -- skipped")
            continue
        ops[panel] = op
        bounds[panel] = boundaries(op, panel)
        finite = {k: v for k, v in bounds[panel].items() if np.isfinite(v)}
        print(f"  [{panel}] boundary defined at {len(finite)}/{len(bounds[panel])} "
              f"x points; f* range "
              f"[{min(finite.values()):.3f}, {max(finite.values()):.3f}]"
              if finite else f"  [{panel}] boundary undefined everywhere")

    cross = (crossing(bounds["dD"], bounds["dStraight"])
             if len(bounds) == 2 else {"crosses": False, "reason": "one panel missing"})
    print(f"\nCross-panel: {cross}")

    combined = pd.concat(
        [op.assign(panel=name) for name, op in ops.items()], ignore_index=True)
    tag = "" if axis == "effective" else f"_{axis}"
    combined.to_parquet(common.RESULTS_DIR / f"e02_heatmap_panels{tag}.parquet")
    cover.to_csv(common.RESULTS_DIR / f"e02_heatmap_coverage{tag}.csv", index=False)
    rows = []
    for panel, bound in bounds.items():
        for x, f_star in bound.items():
            rows.append(dict(panel=panel, x=float(x), f_star=float(f_star)))
    pd.DataFrame(rows).to_csv(
        common.RESULTS_DIR / f"e02_heatmap_boundaries{tag}.csv", index=False)
    print(f"Saved panels, coverage and boundaries to {common.RESULTS_DIR}")
    return {"ops": ops, "bounds": bounds, "coverage": cover, "crossing": cross,
            "grid": grid, "axis": axis}


def run_both(scale: int = common.SCALE) -> dict:
    """Both axes plus the figure. The nominal axis is the control (it must reproduce
    the published crossing), so the figure is only meaningful with both."""
    from experiments.human.analysis.criticality_matched import panels
    results = {axis: run(scale, axis) for axis in ("nominal", "effective")}
    common.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    panels.fig_heatmaps(results, common.FIGURES_DIR / "fig_heatmaps_matched")
    return results

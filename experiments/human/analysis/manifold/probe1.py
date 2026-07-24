"""Probe 1 -- manifold dimensionality and shape.

Rebuilds every (condition, variant, spectral radius, seed) reservoir EXACTLY as the
committed four-task runs did (construction is fully seed-deterministic: the same
construction seed drives mask/weights/Win, the same ``seed + INPUT_SEED_OFFSET``
drives the task input), captures the driven state matrix via the evaluators' opt-in
``collect_states`` path, and computes ``manifold_metrics`` (participation ratio,
curvature, spectral entropy) inline. Writes one tidy
``results/scale_<N>/manifold_metrics.parquet`` (a ``task`` column spans the tasks)
and the PR / curvature / entropy versus spectral-radius figures.

Because each cell re-runs the real evaluator it also co-records that cell's
performance metric, asserted against the committed ``results.parquet`` -- a
correctness gate proving the captured states are the same reservoirs the floor
measured (Probe 3 then reads that co-recorded performance).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from src.reservoir.build import build_from_adjacency
from src.analysis import manifold
from src.experiment.plots import _VARIANT_STYLE, _VARIANT_LABEL
from experiments.human.substrates import HumanSubstrateBuilder
from experiments.human import matrix_config
from experiments.human.analysis.manifold import common

# The three headline geometry metrics and their figure metadata.
_METRIC_FIGURES = {
    "pr": dict(ylabel="participation ratio (PR)", ylim=None,
               suptitle="Manifold dimensionality (participation ratio) vs spectral radius"),
    "mean_curvature": dict(ylabel="mean curvature (rad)", ylim=(0.0, np.pi),
                           suptitle="Manifold curvature (trajectory straightening) vs spectral radius"),
    "spectral_entropy": dict(ylabel="spectral entropy (norm.)", ylim=(0.0, 1.05),
                             suptitle="Manifold spectral entropy vs spectral radius"),
}

# Tasks whose performance metric is a stable (non-chaotic) function of the states,
# so it reproduces the committed run tightly and can be hard-asserted. Lorenz is
# excluded: its closed-loop free-run is chaotic, so a sub-ULP state difference
# (e.g. a BLAS-thread-count mismatch vs the committed run) can amplify VPT/climate
# by O(1). Lorenz shares the SAME construction path, so MC+NARMA matching already
# proves the reservoirs are rebuilt correctly; Lorenz is reported, not asserted.
_STRICT_VALIDATION_TASKS = ("mc", "narma10")


# ---------------------------------------------------------------------------
# Capture
# ---------------------------------------------------------------------------
def capture_cell(cell, state) -> list:
    """Rebuild the reservoir per spectral radius (bit-identical to the runner),
    capture its driven state matrix, and return one metrics row per sr."""
    task_name, condition, variant, seed = cell
    builder, spec = state["builder"], state["specs"][task_name]
    weighted = builder.weighted(condition, variant, seed)
    rung = matrix_config.VARIANT_RUNG.get(variant, -1)
    rows = []
    for spectral_radius in spec["sweep"]:
        reservoir = build_from_adjacency(
            weighted_adjacency=weighted,
            target_spectral_radius=spectral_radius,
            leak_rate=spec["leak_rate"],
            input_scaling=spec["input_scaling"],
            seed=seed,
            input_dim=spec["input_dim"],
        )
        out = spec["evaluate"](
            reservoir,
            seed=seed + spec["input_seed_offset"],
            collect_states=True,
            **spec["params"],
        )
        row = dict(task=task_name, condition=condition, variant=variant, rung=rung,
                   spectral_radius=spectral_radius, seed=seed,
                   **manifold.manifold_metrics(out["states"]))
        for perf_metric in spec["perf"]:
            row[perf_metric] = out[perf_metric]
        rows.append(row)
    return rows


def capture(builder, specs, conditions, variants, n_seeds, jobs) -> pd.DataFrame:
    """Capture manifold metrics over the (task, condition, variant, seed) grid."""
    cells = [(task, c, v, s) for task in specs for c in conditions
             for v in variants for s in range(n_seeds)]
    return common.run_cells(cells, capture_cell, {"builder": builder, "specs": specs},
                            jobs, "capture")


# ---------------------------------------------------------------------------
# Correctness gate: co-recorded performance metric vs the committed run
# ---------------------------------------------------------------------------
def validate_against_committed(df: pd.DataFrame, specs: dict,
                               strict_tasks=_STRICT_VALIDATION_TASKS) -> None:
    """Check the co-recorded performance metric reproduces the committed
    ``results.parquet``. Strict tasks (stable metrics) are hard-asserted on bulk
    agreement (BLAS float-reduction order gives ~1e-7 noise; a real construction
    bug shifts ~every row by O(0.1-1)); chaotic tasks (Lorenz) are reported."""
    keys = ["condition", "variant", "seed"]
    for task, spec in specs.items():
        path = spec["results_dir"] / "results.parquet"
        if not path.exists():
            print(f"  [validate] {task}: committed {path} absent -- skipping gate.")
            continue
        committed = pd.read_parquet(path).copy()
        committed["_sr"] = committed.spectral_radius.round(6)
        sub = df[df.task == task].copy()
        sub["_sr"] = sub.spectral_radius.round(6)
        strict = task in strict_tasks
        for perf_metric in spec["perf"]:
            merged = sub.merge(
                committed[keys + ["_sr", perf_metric]].rename(
                    columns={perf_metric: perf_metric + "_committed"}),
                on=keys + ["_sr"], how="inner",
            )
            a = merged[perf_metric].to_numpy(dtype=float)
            b = merged[perf_metric + "_committed"].to_numpy(dtype=float)
            both_fin = np.isfinite(a) & np.isfinite(b)
            n_flip = int((np.isfinite(a) ^ np.isfinite(b)).sum())  # inf vs finite
            rel = (np.abs(a[both_fin] - b[both_fin])
                   / np.maximum(np.abs(b[both_fin]), 1e-12))
            median_rel = float(np.median(rel)) if rel.size else 0.0
            max_rel = float(rel.max()) if rel.size else 0.0
            n_gross = int((rel > 1e-2).sum())  # >1% == a real bug, not FP noise
            tag = "validate" if strict else "validate/soft"
            msg = (f"  [{tag}] {task}/{perf_metric}: {len(merged)} rows, "
                   f"median rel diff={median_rel:.1e}, max={max_rel:.1e}, "
                   f"gross(>1%)={n_gross}, inf/finite flips={n_flip}")
            if strict:
                assert median_rel < 1e-5 and n_gross == 0, (
                    msg + f"\n{task}/{perf_metric}: capture does NOT reproduce the "
                    "committed reservoirs -- check seeds/params/substrate.")
                print(msg)
            else:
                print(msg + ("  [chaotic metric: reported, not asserted]"
                             if median_rel < 1e-2 else
                             "  !! LARGE median disagreement -- inspect."))


# ---------------------------------------------------------------------------
# Figures + summary
# ---------------------------------------------------------------------------
def _aggregate(df_sub: pd.DataFrame, value_col: str) -> pd.DataFrame:
    """Per-(variant, sr) median and interquartile range across seeds."""
    g = df_sub.groupby(["variant", "spectral_radius"])[value_col]
    out = g.median().reset_index(name="median")
    out["q25"] = g.quantile(0.25).to_numpy()
    out["q75"] = g.quantile(0.75).to_numpy()
    return out


def _plot_metric_grid(df, value_col, ylabel, suptitle, path, supercrit, ylim=None):
    """Grid of ``value_col`` vs spectral radius: rows = tasks, cols = conditions,
    one median line per variant (IQR band on connectome + degree_rewire)."""
    tasks = common.present_tasks(df)
    conditions = common.present_conditions(df)
    variants = matrix_config.VARIANTS
    nrows, ncols = len(tasks), len(conditions)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.0 * ncols, 3.1 * nrows),
                             squeeze=False, sharex=True, sharey="row")
    sr_max = float(df.spectral_radius.max())
    for i, task in enumerate(tasks):
        for j, condition in enumerate(conditions):
            ax = axes[i][j]
            agg = _aggregate(df[(df.task == task) & (df.condition == condition)], value_col)
            for variant in variants:
                vv = agg[agg.variant == variant].sort_values("spectral_radius")
                if vv.empty:
                    continue
                style = _VARIANT_STYLE[variant]
                ax.plot(vv.spectral_radius, vv["median"],
                        label=_VARIANT_LABEL[variant], **style)
                if variant in ("connectome", "degree_rewire"):
                    ax.fill_between(vv.spectral_radius, vv["q25"], vv["q75"],
                                    color=style["color"], alpha=0.15, zorder=2)
            start = supercrit.get(condition) if supercrit else None
            if start is not None:
                ax.axvspan(start, sr_max, color=common.SUPERCRITICAL_COLOR, zorder=0)
            ax.axvline(1.0, color="grey", lw=0.8, ls=":", zorder=1)
            ax.grid(alpha=0.25)
            if ylim is not None:
                ax.set_ylim(*ylim)
            if i == 0:
                ax.set_title(common.CONDITION_TITLE.get(condition, condition), fontsize=10)
            if j == 0:
                ax.set_ylabel(f"{common.TASK_TITLE.get(task, task)}\n{ylabel}", fontsize=9)
            if i == nrows - 1:
                ax.set_xlabel("spectral radius")
    handles = [plt.Line2D([0], [0], **{k: v for k, v in _VARIANT_STYLE[v].items()
                                       if k != "zorder"}, label=_VARIANT_LABEL[v])
               for v in variants]
    handles.append(mpatches.Patch(facecolor=common.SUPERCRITICAL_COLOR, edgecolor="none",
                                  label="connectome bulk supercritical (sr ≥ $sr_{crit}$)"))
    fig.legend(handles=handles, loc="lower center", ncol=4, fontsize=8,
               framealpha=0.9, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle(suptitle, fontsize=12)
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def write_figures(df, figures_dir, supercrit):
    figures_dir.mkdir(parents=True, exist_ok=True)
    for value_col, meta in _METRIC_FIGURES.items():
        path = figures_dir / f"manifold_{value_col}_vs_sr.png"
        _plot_metric_grid(df, value_col, meta["ylabel"], meta["suptitle"], path,
                          supercrit, ylim=meta["ylim"])
        print(f"Saved {path}")


def _write_summary(df, path, supercrit):
    """Seed-median PR for connectome vs degree_rewire at a canonical (~0.95) and a
    supercritical (nearest sr_crit) operating point, per task/condition."""
    srs = sorted(df.spectral_radius.unique())
    canonical = min(srs, key=lambda s: abs(s - 0.95))
    lines = ["# Manifold Probe 1 -- PR at canonical vs supercritical (seed medians)\n",
             f"Canonical sr = {canonical:g}; supercritical sr = nearest grid point to "
             "each condition's sr_crit (1/bulk95_ratio).\n",
             "| task | condition | sr | PR connectome | PR degree_rewire | PR random_gaussian |",
             "|---|---|---|---|---|---|"]

    def _median(task, condition, sr, variant):
        m = df[(df.task == task) & (df.condition == condition)
               & (np.isclose(df.spectral_radius, sr)) & (df.variant == variant)]["pr"]
        return float(m.median()) if len(m) else float("nan")

    for task in common.present_tasks(df):
        for condition in matrix_config.CONDITIONS:
            crit = supercrit.get(condition)
            sr_super = min(srs, key=lambda s: abs(s - crit)) if crit else max(srs)
            for label, sr in [("canonical", canonical), ("supercrit", sr_super)]:
                lines.append(
                    f"| {task} | {condition} | {sr:g} ({label}) | "
                    f"{_median(task, condition, sr, 'connectome'):.2f} | "
                    f"{_median(task, condition, sr, 'degree_rewire'):.2f} | "
                    f"{_median(task, condition, sr, 'random_gaussian'):.2f} |")
    path.write_text("\n".join(lines) + "\n")
    print(f"Saved {path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def run(smoke: bool = False, jobs: int = 1, scale: int | None = None,
        sr_max: float | None = None, tasks=None) -> None:
    scale = matrix_config.SCALE if scale is None else scale
    tasks = tasks or common.DEFAULT_TASKS
    results_dir, figures_dir = common.scale_dirs(scale)
    results_dir.mkdir(parents=True, exist_ok=True)

    builder = HumanSubstrateBuilder(scale=scale)
    print("Substrate summary:")
    for key, value in builder.summary().items():
        print(f"  {key}: {value}")

    specs = common.build_specs(scale, tasks, smoke, sr_max)
    conditions = matrix_config.CONDITIONS
    variants = matrix_config.VARIANTS
    n_seeds = 2 if smoke else matrix_config.N_SEEDS
    print(f"\nCapturing tasks={list(specs)} scale={scale} "
          f"sweep={len(specs[tasks[0]]['sweep'])} pts n_seeds={n_seeds} jobs={jobs}\n")

    df = capture(builder, specs, conditions, variants, n_seeds, jobs)

    # T_effective > N check (PR is otherwise bounded by T, not the geometry).
    n_nodes = int(builder.mask.shape[0])
    print(f"\nManifold metric ranges (N={n_nodes}):")
    for task in tasks:
        sub = df[df.task == task]
        print(f"  {task}: PR [{sub.pr.min():.1f}, {sub.pr.max():.1f}]  "
              f"curvature [{sub.mean_curvature.min():.2f}, {sub.mean_curvature.max():.2f}]  "
              f"entropy [{sub.spectral_entropy.min():.2f}, {sub.spectral_entropy.max():.2f}]")

    out_parquet = results_dir / "manifold_metrics.parquet"
    df.to_parquet(out_parquet)
    print(f"\nSaved {out_parquet}  ({len(df)} rows)")

    # Figures + summary first, so a validation issue never costs the deliverables.
    supercrit = builder.connectome_supercritical_radii(conditions)
    write_figures(df, figures_dir, supercrit)
    _write_summary(df, results_dir / "manifold_metrics_summary.md", supercrit)

    if not smoke:
        print("\nValidating co-recorded performance vs the committed runs:")
        validate_against_committed(df, specs)
    print("\nProbe 1 capture complete.")

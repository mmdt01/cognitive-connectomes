"""Probe 2 -- manifold alignment with structural modes.

For the connectome (and the ``degree_rewire`` null), at each condition's canonical
and supercritical operating point, captures the driven states and records the
cumulative state variance captured by the top-k low-frequency graph-Laplacian
**harmonics** vs dominant **W-eigenmodes** vs a **random**-orthonormal band. The
bases are sr-invariant (rescaling ``W`` moves neither its eigenvectors nor the
Laplacian's), so they are built once per (condition, variant, seed) and reused
across the operating points; only the states change with sr. Writes
``manifold_alignment.parquet`` + cumulative-variance figures (canonical +
supercritical) + a summary.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.reservoir.build import build_from_adjacency
from src.analysis import manifold
from experiments.human.substrates import HumanSubstrateBuilder
from experiments.human import matrix_config
from experiments.human.analysis.manifold import common

PROBE2_VARIANTS = ["connectome", "degree_rewire"]  # substrate of interest + key null
PROBE2_N_RANDOM = 20
BASIS_TITLE = {
    "harmonics": "Laplacian harmonics (low-freq)",
    "wmodes": "W eigenmodes (dominant)",
    "random": "random orthonormal",
}
BASIS_COLOR = {"harmonics": "#1f77b4", "wmodes": "#d62728", "random": "#999999"}


# ---------------------------------------------------------------------------
# Capture
# ---------------------------------------------------------------------------
def _structural_bases(weighted: np.ndarray) -> dict:
    """The two structural bases for the alignment probe (both orthonormal). The
    Laplacian uses |weighted| (== weighted for the non-negative empirical
    substrate); the W-modes are ordered by descending |eigenvalue|."""
    return {"harmonics": manifold.graph_laplacian_harmonics(weighted),
            "wmodes": manifold.symmetric_eigenbasis(weighted, order="abs_desc")}


def _sr_list(condition: str, supercrit: dict, srs: list) -> list:
    """Representative operating points: canonical (~0.95) + the connectome's
    supercritical point (nearest grid to sr_crit)."""
    canonical = min(srs, key=lambda s: abs(s - 0.95))
    crit = supercrit.get(condition)
    super_pt = min(srs, key=lambda s: abs(s - crit)) if crit else max(srs)
    out = []
    for sr in (canonical, super_pt):
        if sr not in out:
            out.append(sr)
    return out


def alignment_cell(cell, state) -> list:
    """Build the structural bases once, then per sr capture states and record the
    cumulative captured-variance curve for each basis (+ the random band)."""
    task_name, condition, variant, seed = cell
    builder, spec = state["builder"], state["specs"][task_name]
    k_grid, n_random = state["k_grid"], state["n_random"]
    sr_list = state["sr_by_condition"][condition]
    weighted = builder.weighted(condition, variant, seed)
    bases = _structural_bases(weighted)
    rows = []
    for spectral_radius in sr_list:
        reservoir = build_from_adjacency(
            weighted_adjacency=weighted, target_spectral_radius=spectral_radius,
            leak_rate=spec["leak_rate"], input_scaling=spec["input_scaling"],
            seed=seed, input_dim=spec["input_dim"])
        out = spec["evaluate"](reservoir, seed=seed + spec["input_seed_offset"],
                               collect_states=True, **spec["params"])
        states = out["states"]
        base = dict(task=task_name, condition=condition, variant=variant,
                    seed=seed, spectral_radius=spectral_radius)
        for basis_name, basis in bases.items():
            curve = manifold.basis_alignment(states, basis, k_grid)["captured"]
            for k, cap in zip(k_grid, curve):
                rows.append(dict(base, basis=basis_name, k=int(k),
                                 captured=float(cap), captured_std=0.0))
        band = manifold.random_basis_band(states, k_grid, n_random=n_random, seed=seed)
        for k, mean, std in zip(k_grid, band["mean"], band["std"]):
            rows.append(dict(base, basis="random", k=int(k),
                             captured=float(mean), captured_std=float(std)))
    return rows


def capture_alignment(builder, specs, conditions, variants, n_seeds,
                      sr_by_condition, k_grid, n_random, jobs) -> pd.DataFrame:
    cells = [(t, c, v, s) for t in specs for c in conditions for v in variants
             for s in range(n_seeds)]
    state = dict(builder=builder, specs=specs, sr_by_condition=sr_by_condition,
                 k_grid=k_grid, n_random=n_random)
    return common.run_cells(cells, alignment_cell, state, jobs, "alignment")


# ---------------------------------------------------------------------------
# Figure + summary
# ---------------------------------------------------------------------------
def _plot_alignment(df, variant, sr_by_condition, use_supercritical, suptitle, path):
    """Cumulative captured variance vs k: rows = tasks, cols = conditions; three
    curves (harmonics, W-modes, random band) for ``variant`` at each condition's
    representative operating point."""
    tasks = common.present_tasks(df)
    conditions = common.present_conditions(df)
    nrows, ncols = len(tasks), len(conditions)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.0 * ncols, 3.1 * nrows),
                             squeeze=False, sharex=True, sharey=True)
    for i, task in enumerate(tasks):
        for j, condition in enumerate(conditions):
            ax = axes[i][j]
            sr_list = sr_by_condition[condition]
            sr = sr_list[-1] if use_supercritical else sr_list[0]
            sub = df[(df.task == task) & (df.condition == condition)
                     & (df.variant == variant) & np.isclose(df.spectral_radius, sr)]
            for basis_name in ("harmonics", "wmodes", "random"):
                b = sub[sub.basis == basis_name]
                if b.empty:
                    continue
                g = b.groupby("k").captured.median().reset_index().sort_values("k")
                ax.plot(g.k, g.captured, color=BASIS_COLOR[basis_name],
                        label=BASIS_TITLE[basis_name], lw=1.8, marker="o", ms=3)
                if basis_name == "random":
                    spread = b.groupby("k").captured_std.median().reindex(g.k).values
                    ax.fill_between(g.k, g.captured - spread, g.captured + spread,
                                    color=BASIS_COLOR[basis_name], alpha=0.25)
            ax.set_xscale("log")
            ax.set_ylim(0, 1.02)
            ax.grid(alpha=0.25, which="both")
            ax.text(0.04, 0.96, f"sr={sr:g}", transform=ax.transAxes, fontsize=8,
                    va="top", ha="left", color="0.3")
            if i == 0:
                ax.set_title(common.CONDITION_TITLE.get(condition, condition), fontsize=10)
            if j == 0:
                ax.set_ylabel(f"{common.TASK_TITLE.get(task, task)}\ncaptured variance",
                              fontsize=9)
            if i == nrows - 1:
                ax.set_xlabel("k (basis vectors, log)")
    handles = [plt.Line2D([0], [0], color=BASIS_COLOR[b], lw=1.8, marker="o", ms=3,
                          label=BASIS_TITLE[b]) for b in ("harmonics", "wmodes", "random")]
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=9,
               framealpha=0.9, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle(suptitle, fontsize=12)
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _write_summary(df, path, sr_by_condition, variant="connectome", k_ref=10):
    """Captured variance at k=k_ref for each basis, connectome, at the supercritical
    operating point per task/condition (the headline alignment numbers)."""
    lines = [f"# Manifold Probe 2 -- variance captured by top-{k_ref} basis vectors "
             f"({variant}, supercritical op. point; seed medians)\n",
             "harmonics = low-freq graph-Laplacian; wmodes = dominant |eigenvalue| "
             "of W; random = chance band. Higher = manifold lives in that basis.\n",
             f"| task | condition | sr | harmonics@{k_ref} | wmodes@{k_ref} | random@{k_ref} |",
             "|---|---|---|---|---|---|"]

    def _cap(task, cond, sr, basis):
        m = df[(df.task == task) & (df.condition == cond) & (df.variant == variant)
               & np.isclose(df.spectral_radius, sr) & (df.basis == basis)
               & (df.k == k_ref)].captured
        return float(m.median()) if len(m) else float("nan")

    for task in common.present_tasks(df):
        for cond in matrix_config.CONDITIONS:
            sr = sr_by_condition[cond][-1]
            lines.append(f"| {task} | {cond} | {sr:g} | {_cap(task, cond, sr, 'harmonics'):.2f} | "
                         f"{_cap(task, cond, sr, 'wmodes'):.2f} | {_cap(task, cond, sr, 'random'):.2f} |")
    path.write_text("\n".join(lines) + "\n")
    print(f"Saved {path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def run(smoke: bool = False, jobs: int = 1, scale: int | None = None,
        tasks=None) -> None:
    scale = matrix_config.SCALE if scale is None else scale
    tasks = tasks or common.DEFAULT_TASKS
    results_dir, figures_dir = common.scale_dirs(scale)
    results_dir.mkdir(parents=True, exist_ok=True)

    builder = HumanSubstrateBuilder(scale=scale)
    # The full [0,6] grid is used only to pick representative operating points; the
    # reservoir hyperparameters/params come from the specs (smoke reduces the cells).
    specs = common.build_specs(scale, tasks, smoke=False, sr_max=None)
    conditions = matrix_config.CONDITIONS
    supercrit = builder.connectome_supercritical_radii(conditions)
    srs = specs[tasks[0]]["sweep"]
    sr_by_condition = {c: _sr_list(c, supercrit, srs) for c in conditions}
    k_grid = manifold.default_k_grid(int(builder.mask.shape[0]))
    variants = ["connectome"] if smoke else PROBE2_VARIANTS
    n_seeds = 2 if smoke else matrix_config.N_SEEDS
    print(f"Probe 2 alignment: tasks={list(specs)} scale={scale} variants={variants} "
          f"n_seeds={n_seeds} jobs={jobs}")
    print(f"  operating points per condition: "
          f"{ {c: sr_by_condition[c] for c in conditions} }")
    print(f"  k_grid={k_grid}\n")

    df = capture_alignment(builder, specs, conditions, variants, n_seeds,
                           sr_by_condition, k_grid, PROBE2_N_RANDOM, jobs)
    out_parquet = results_dir / "manifold_alignment.parquet"
    df.to_parquet(out_parquet)
    print(f"\nSaved {out_parquet}  ({len(df)} rows)")

    figures_dir.mkdir(parents=True, exist_ok=True)
    _plot_alignment(df, "connectome", sr_by_condition, use_supercritical=True,
                    suptitle="Probe 2: activity-manifold alignment with structural bases "
                             "(connectome, supercritical operating point)",
                    path=figures_dir / "manifold_alignment_connectome_supercritical.png")
    print(f"Saved {figures_dir / 'manifold_alignment_connectome_supercritical.png'}")
    _plot_alignment(df, "connectome", sr_by_condition, use_supercritical=False,
                    suptitle="Probe 2: activity-manifold alignment with structural bases "
                             "(connectome, canonical operating point)",
                    path=figures_dir / "manifold_alignment_connectome_canonical.png")
    print(f"Saved {figures_dir / 'manifold_alignment_connectome_canonical.png'}")
    _write_summary(df, results_dir / "manifold_alignment_summary.md", sr_by_condition)
    print("\nProbe 2 alignment complete.")

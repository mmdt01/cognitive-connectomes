"""CLI for E0.2 -- the effective-criticality-matched memory panel.

    python -m experiments.human.analysis.criticality_matched [MODE ...] [--scale N]

Modes (default ``--panel``); all are reanalysis except ``--task-b`` / ``--extend-f``,
which are the only steps that simulate anything:

    --panel      the f=0 matched memory panel, three figures and the verdict
    --task-a     d_eff(alpha): is the ridge effective rank saturated?
    --task-b     extend the f=0 MC sweep to sigma=8 [--jobs N] [--sr-max X] [--mc-alpha]
    --extend-f   extend the f>0 (f, sigma) grid, MC + Lorenz [--jobs N] [--sr-max X]
    --heatmaps   the (f, sigma) panels on both axes + the cross-panel figure
    --closeout   the item 4/5 close-out reanalyses
    --n1000      the N=1000 memory run (--scale 1000), or its N=448 protocol
                 control (--scale 448), per N1000_RUN_SPEC.md [--jobs N]

Nothing here overwrites a frozen artifact; every output carries a manifest recording
the config and the git commit that produced it.
"""

import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from experiments.human.analysis.criticality_matched import (
    analysis, common, panels, verdict)

# Representative matched points for the "same x, different nominal sigma" table.
# The top one tracks the actual overlap, so it stays correct when Task B extends it.
_MATCHED_X_BASE = [0.78, 1.00, 1.36]


def _handoff(cells: pd.DataFrame, eff_summary: dict) -> dict:
    """The N=1000 configuration this analysis implies, in both coordinate systems.

    ``bulk95`` is aggregated with the **median**, per
    ``eigenspectrum.common.SR_CRIT_CONVENTION`` -- the mean does not commute with the
    reciprocal, so a mean-based ``sr_crit`` here would disagree with E0.4's table.
    """
    bulk = cells.groupby("variant").bulk95.median()
    conn448 = float(bulk[common.CONN])
    sigma_max = float(cells.spectral_radius.max())
    xs = _MATCHED_X_BASE + [round(eff_summary["overlap_hi"], 3)]
    matched = [(x, x / conn448, x / float(bulk[common.CONTRAST])) for x in xs]

    if eff_summary.get("peak_at_upper_edge"):
        text_448 = (
            f"The sweep reaches σ = {sigma_max:g}, giving σ·bulk95 up to "
            f"{eff_summary['overlap_hi']:.3f}, and the peak is *still* on that edge. "
            f"Reaching σ·bulk95 = {eff_summary['overlap_hi'] + 0.5:.1f} would need "
            f"σ = {(eff_summary['overlap_hi'] + 0.5) / conn448:.2f}.")
    else:
        text_448 = (
            f"**Task B resolved this.** Extending the sweep to σ = {sigma_max:g} moved "
            f"the overlap to σ·bulk95 ≤ {eff_summary['overlap_hi']:.3f}, and the "
            f"matched peak is now **interior** to it (at "
            f"{eff_summary['peak_x']:.3f}), so the figure below is a measurement "
            "rather than a lower bound.")

    lines = []
    summary_path = common.eigenspectrum_summary(1000)
    if summary_path.exists():
        e04 = pd.read_csv(summary_path)
        emp = e04[e04.condition == "human_empirical"].set_index("variant")
        conn1000 = float(emp.loc[common.CONN, "bulk95_median"])
        er1000 = float(emp.loc[common.CONTRAST, "bulk95_median"])
        target_hi = 2.0
        sr_needed = target_hi / conn1000
        lines += [
            "From E0.4, at N=1000: connectome `bulk95` = "
            f"{conn1000:.4f} (`sr_crit` = {1 / conn1000:.3f}), ER `bulk95` = "
            f"{er1000:.4f} (`sr_crit` = {1 / er1000:.3f}).\n",
            "**Sweep `σ ∈ [0, 8]`, MC only, `f = 0`, variants "
            "{connectome, weight-permuted, degree, ER}.** In the two coordinate "
            "systems:\n",
            "| | nominal σ | σ·bulk95 (connectome) | σ·bulk95 (ER) |",
            "|---|---|---|---|",
            f"| lower bound | 0 | 0 | 0 |",
            f"| connectome critical | {1 / conn1000:.2f} | 1.00 | "
            f"{(1 / conn1000) * er1000:.2f} |",
            f"| ER critical | {1 / er1000:.2f} | {(1 / er1000) * conn1000:.2f} | 1.00 |",
            f"| upper bound | 8.00 | {8 * conn1000:.3f} | {8 * er1000:.3f} |",
            "",
            f"The binding constraint is the connectome (smallest `bulk95`, shortest "
            f"reach): σ = {sr_needed:.2f} is needed for σ·bulk95 = {target_hi:.1f}, so "
            "**σ_max = 8** gives a usable overlap of "
            f"[0, {8 * conn1000:.3f}] — comparable headroom to N=448 and enough to "
            "get past the point where the N=448 analysis was censored.",
            "",
            "**The wedge lives supercritically in matched coordinates**, so the grid "
            "must be dense above σ·bulk95 ≈ 1. Concentrate points in "
            f"σ ∈ [{1 / conn1000:.1f}, 8] for the connectome; a uniform nominal grid "
            "wastes most of its points below criticality.",
            "",
            "Carry forward from the roadmap's §2b pre-flight, unchanged and still "
            "required: raise `T` to preserve `T_eff/N`, reparameterise the ridge "
            "`alpha` with `T_eff`, re-run N=448 under the new `T`/`alpha` first as the "
            "control, and report `d_eff / N` with the ceiling drawn (§4.3 above shows "
            "why).",
        ]
    else:
        lines.append("E0.4's N=1000 `bulk95_summary.csv` is absent — run "
                     "`python -m experiments.human.analysis.eigenspectrum --tables "
                     "--scale 1000` to generate the handoff numbers.")

    return {"matched_sr": matched, "extend_448": text_448, "n1000": "\n".join(lines),
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "git_commit": common.code_version()["git_commit"] or "unknown"}


def run(scale: int = common.SCALE) -> None:
    common.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    common.FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 70 + "\nE0.2 -- effective-criticality-matched memory panel\n" + "=" * 70)
    cells, source_meta = analysis.load_panel_cells(scale)
    print("\nGates:")
    gate = analysis.source_agreement_gate(cells, scale)

    frames, summaries = {}, {}
    for axis in ("nominal", "effective"):
        frame, info = analysis.build_axis(cells, axis, common.PRIMARY_INTERP)
        frames[axis] = frame
        summaries[axis] = analysis.summarise_axis(frame, info)

    sensitivity = {axis: analysis.interpolation_sensitivity(cells, axis)
                   for axis in ("nominal", "effective")}
    traj = analysis.sigma_eff_trajectories(cells)

    n_nodes = scale
    ceilings = {}
    for variant in common.VARIANTS:
        col = f"d_eff_{variant}"
        if col in frames["effective"]:
            peak = float(frames["effective"][col].max())
            ceilings[variant] = (peak, peak / n_nodes)

    combined = pd.concat(frames.values(), ignore_index=True)
    combined.to_parquet(common.RESULTS_DIR / "e02_panel.parquet")
    print(f"\nSaved {common.RESULTS_DIR / 'e02_panel.parquet'}  ({len(combined)} rows)")
    traj.to_parquet(common.RESULTS_DIR / "e02_sigma_eff_trajectories.parquet")
    pd.DataFrame(summaries.values()).to_csv(
        common.RESULTS_DIR / "e02_axis_summary.csv", index=False)
    pd.concat(sensitivity.values(), ignore_index=True).to_csv(
        common.RESULTS_DIR / "e02_interpolation_sensitivity.csv", index=False)
    print(f"Saved {common.RESULTS_DIR / 'e02_axis_summary.csv'} and "
          f"{common.RESULTS_DIR / 'e02_interpolation_sensitivity.csv'}")

    panels.fig_panel_a(frames, summaries, common.FIGURES_DIR / "fig_panelA_matched")
    panels.fig_absolute(frames, n_nodes, common.FIGURES_DIR / "fig_absolute_deff")
    panels.fig_sigma_eff(traj, common.FIGURES_DIR / "fig_sigma_eff")

    handoff = _handoff(cells, summaries["effective"])
    handoff["source"] = source_meta
    profiles = verdict.variant_profiles(frames["effective"])
    verdict.write(verdict.build_outcome(summaries, sensitivity, ceilings, traj,
                                        gate, handoff, profiles))

    common.write_manifest(
        common.RESULTS_DIR / "manifest_e02.json", "E0.2 criticality-matched panel",
        scale, f_cut=common.F_CUT, task=common.TASK, variants=common.VARIANTS,
        contrast=common.CONTRAST, axes=list(common.AXES), primary_axis=common.PRIMARY_AXIS,
        interpolation=common.INTERP_METHODS, primary_interpolation=common.PRIMARY_INTERP,
        n_grid=common.N_GRID, n_seeds=common.N_SEEDS, gates={"source_agreement": gate},
        cell_source=source_meta,
        overlap=[summaries["effective"]["overlap_lo"],
                 summaries["effective"]["overlap_hi"]],
        source=source_meta["path"])

    nom, eff = summaries["nominal"], summaries["effective"]
    print("\n" + "=" * 70)
    print(f"  peak dD  nominal {nom['peak_dD']:+.1f} (sigma={nom['peak_x']:.2f})"
          f"  ->  effective {eff['peak_dD']:+.1f} (x={eff['peak_x']:.2f})"
          f"   [{eff['peak_dD'] / nom['peak_dD']:.0%} retained]")
    print(f"  min  dD  nominal {nom['min_dD']:+.1f}  ->  effective {eff['min_dD']:+.1f}")
    print(f"  effective peak at upper edge of overlap: {eff['peak_at_upper_edge']}")
    print("=" * 70)
    print("\nE0.2 complete.")


if __name__ == "__main__":
    scale = common.flag(sys.argv, "--scale", common.SCALE, int)
    modes = ([m for m in ("--panel", "--task-a", "--task-b", "--extend-f",
                          "--heatmaps", "--closeout", "--n1000") if m in sys.argv]
             or ["--panel"])
    if "--task-b" in modes:
        # The only simulating step: extend the MC sweep so the matched-axis peak
        # stops being censored. Run before --panel so the panel picks it up.
        from experiments.human.analysis.criticality_matched import extend_sweep
        extend_sweep.run(
            scale=scale, jobs=common.flag(sys.argv, "--jobs", 1, int),
            sr_max=common.flag(sys.argv, "--sr-max", extend_sweep.SR_MAX, float),
            mc_alphas=(extend_sweep.MC_ALPHA_GRID if "--mc-alpha" in sys.argv else ()))
    if "--panel" in modes:
        run(scale=scale)
    if "--task-a" in modes:
        from experiments.human.analysis.criticality_matched import alpha_sweep
        alpha_sweep.run(scale=scale)
    if "--extend-f" in modes:
        from experiments.human.analysis.criticality_matched import extend_f
        extend_f.run(scale=scale, jobs=common.flag(sys.argv, "--jobs", 1, int),
                     sr_max=common.flag(sys.argv, "--sr-max", extend_f.SR_MAX, float))
    if "--heatmaps" in modes:
        from experiments.human.analysis.criticality_matched import heatmaps
        heatmaps.run_both(scale=scale)
    if "--closeout" in modes:
        from experiments.human.analysis.criticality_matched import closeout
        closeout.run(scale=scale)
    if "--n1000" in modes:
        from experiments.human.analysis.criticality_matched import n1000
        n1000.run(scale=scale, jobs=common.flag(sys.argv, "--jobs", 1, int))
        if scale == 448:
            print("\nControl gate:")
            n1000.control_gate(scale)

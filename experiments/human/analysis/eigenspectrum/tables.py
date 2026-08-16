"""E0.4 step 1: per-seed eigenspectra and the ``bulk95`` / ``sr_crit`` table.

Eigendecomposes the recurrent matrix ``W`` for every rung of the null ladder x every
weight condition x every seed, at a given parcellation scale. **No reservoir
simulation** -- this is eigendecomposition only, and it reuses
``manifold.spectra.capture_w_spectra`` (hence
``src.analysis.spectral.recurrent_spectrum``) rather than re-deriving any spectral
quantity.

Reported per (condition, variant, seed), all on the **normalised** base
``W / |lambda_1|`` except where noted:

===================== =====================================================
``lambda_max_raw``     ``|lambda_1|`` of the **un-normalised** W (the scale the
                       reservoir build divides out). Multiply the normalised
                       eigenvalues by this to recover the unnormalised spectrum.
``perron_root``        largest real part; ``== 1`` exactly when the leading mode is
                       the real positive Perron root (the non-negative signature).
``bulk95``             ``pct95(|lambda|) / |lambda_1|`` -- see common.BULK95_DEFINITION.
``outlier_bulk_gap``   ``1 - bulk95``: how far the Perron outlier sits above the
                       bulk edge, in normalised units.
``lambda2_ratio``      ``|lambda_2| / |lambda_1|`` (``= 1 - spectral_gap``).
``sr_crit``            ``1 / median(bulk95)`` -- the nominal sr at which the bulk
                       turns critical. See common.SR_CRIT_CONVENTION for why the
                       median, not the mean, is the aggregator.
``max_abs_imag``       ``max |Im lambda|``; ~0 for the symmetric human substrate.
===================== =====================================================

Two gates run before anything is written:

1. **Reproduction gate (N=448).** Every scalar must match the frozen
   ``analysis/results/scale_448/w_spectra.parquet`` cell for cell, to floating-point
   precision (``< 1e-12``; the residual is BLAS-thread-count noise, not a difference
   in what was computed). That file is read-only here.
2. **Headline gate.** The documented N=448 values must come back (connectome
   ``bulk95`` ~0.325 / ``sr_crit`` ~3.08, nulls 0.48-0.55). A failure raises rather
   than writing a table, because a change here invalidates everything downstream.
"""

import numpy as np
import pandas as pd

from experiments.human.substrates import HumanSubstrateBuilder
from experiments.human.analysis.manifold import spectra as manifold_spectra
from experiments.human.analysis.eigenspectrum import common

# Documented N=448 reference values (PROJECT_KNOWLEDGE_BASE.md sec 6-7 and the E0.4
# task spec), in the human_empirical column. `tol` is a hard gate; a value outside it
# means the substrate or the spectral code has changed and the run must stop.
_HEADLINE_448 = {
    "connectome": dict(bulk95=0.325, tol=0.005, sr_crit=3.08, sr_tol=0.05),
    # The two numbers are two AGGREGATORS of the same cells, not a disagreement:
    # 0.5120 is the per-seed MEAN and 0.5203 is the MEDIAN. The roadmap's 0.520 is the
    # median and is the correct figure (TIER0 sec 2.1, corrected 15 Aug 2026); the
    # earlier reading of it as "documentation drift" was backwards and is withdrawn.
    # This gate compares against `means` below, so the threshold stays on 0.512 -- it
    # is gating the mean against the mean. Fix the aggregator (see `summarise`, which
    # is already on the median) rather than this number.
    "connectome_weight_permuted": dict(bulk95=0.512, tol=0.010, quoted=0.520),
}
_NULL_BAND = (0.48, 0.56)      # documented "nulls ~0.48-0.55", with rounding headroom
_NULL_VARIANTS = ["random_gaussian", "erdos_renyi", "degree_rewire",
                  "clustering_rewire", "modularity_rewire"]

_SUMMARY_METRICS = ["bulk95", "sr_crit", "outlier_bulk_gap", "lambda2_ratio",
                    "lambda_max_raw", "perron_root"]


# ---------------------------------------------------------------------------
# Capture + derive
# ---------------------------------------------------------------------------
def capture(scale: int, jobs: int) -> pd.DataFrame:
    """Per-seed spectra for every (condition, variant, seed) at ``scale``."""
    builder = HumanSubstrateBuilder(scale=scale)
    print("Substrate summary:")
    for key, value in builder.summary().items():
        print(f"  {key}: {value}")

    # Warm the mask cache in the parent so fork children inherit it copy-on-write
    # instead of re-running each rewire (the expensive part at N=1000).
    if jobs > 1:
        print(f"\nPre-warming null masks ({len(common.VARIANTS) - 2} rungs x "
              f"{common.N_SEEDS} seeds) before forking...", flush=True)
        for variant in common.VARIANTS:
            if variant in ("connectome", "connectome_weight_permuted"):
                continue                        # no mask ladder involved
            for seed in range(common.N_SEEDS):
                builder.get_mask(variant, seed)

    n_cells = len(common.CONDITIONS) * len(common.VARIANTS) * common.N_SEEDS
    print(f"\nEigendecomposing {n_cells} cells "
          f"({len(common.CONDITIONS)} conditions x {len(common.VARIANTS)} variants x "
          f"{common.N_SEEDS} seeds), jobs={jobs}")
    return manifold_spectra.capture_w_spectra(
        builder, common.CONDITIONS, common.VARIANTS, common.N_SEEDS, jobs)


def derive(df: pd.DataFrame) -> pd.DataFrame:
    """Add the E0.4 scalars to a ``capture_w_spectra`` frame (no re-derivation of
    bulk95 -- only algebra on what ``recurrent_spectrum`` already returned)."""
    out = df.copy()
    out["bulk95"] = out["bulk95_radius"].astype(float)
    out["lambda_max_raw"] = out["base_spectral_radius"].astype(float)
    out["outlier_bulk_gap"] = 1.0 - out["bulk95"]
    out["lambda2_ratio"] = 1.0 - out["spectral_gap"].astype(float)
    out["sr_crit"] = 1.0 / out["bulk95"]
    out["max_abs_imag"] = [float(np.abs(np.asarray(v, dtype=float)).max())
                           for v in out["eig_w_imag"]]
    return out


# ---------------------------------------------------------------------------
# Gate 1: reproduction against the frozen committed spectra
# ---------------------------------------------------------------------------
_REPRO_COLS = ["bulk95_radius", "perron_root", "spectral_gap",
               "base_spectral_radius"]


def reproduction_gate(df: pd.DataFrame, scale: int) -> dict:
    """Cell-for-cell comparison against the committed ``w_spectra.parquet``.

    Same code path and same seeds, so the values must agree to floating-point
    precision (the ``1e-12`` threshold admits only BLAS-thread-count round-off, which
    is ~1e-15 here). Returns a report; raises on any larger difference."""
    path = common.committed_w_spectra(scale)
    if not path.exists():
        print(f"  [repro-gate] no committed reference at {path} -- skipped "
              f"(expected for scale != 448).")
        return {"status": "skipped", "reference": str(path)}

    ref = pd.read_parquet(path)
    keys = ["condition", "variant", "seed"]
    merged = df[keys + _REPRO_COLS].merge(
        ref[keys + _REPRO_COLS], on=keys, how="inner", suffixes=("", "_ref"))
    assert len(merged) == len(ref) == len(df), (
        f"[repro-gate] row-count mismatch: new={len(df)} ref={len(ref)} "
        f"joined={len(merged)} -- the (condition, variant, seed) grids differ.")

    worst = {}
    for col in _REPRO_COLS:
        diff = float(np.abs(merged[col].to_numpy(float)
                            - merged[col + "_ref"].to_numpy(float)).max())
        worst[col] = diff
        print(f"  [repro-gate] {col:24s} max |new - committed| = {diff:.3e}")
    bad = {k: v for k, v in worst.items() if v > 1e-12}
    if bad:
        raise RuntimeError(
            f"[repro-gate] scale {scale} does NOT reproduce the committed "
            f"w_spectra.parquet: {bad}. STOP -- the substrate or the spectral code "
            "has changed, which invalidates every downstream bulk95 / sr_crit number.")
    print(f"  [repro-gate] {len(merged)} cells reproduce {path.name} to "
          f"floating-point precision (worst {max(worst.values()):.1e}).  [OK]")
    return {"status": "passed", "reference": str(path), "n_cells": len(merged),
            "max_abs_diff": worst}


# ---------------------------------------------------------------------------
# Gate 2: the documented headline values
# ---------------------------------------------------------------------------
def headline_gate(df: pd.DataFrame, scale: int) -> dict:
    """Check the documented N=448 values come back. Raises on a hard failure."""
    if scale != 448:
        print(f"  [headline-gate] no documented reference values at N={scale} "
              "-- reporting only.")
        return {"status": "skipped"}

    emp = df[df.condition == common.BASE_CONDITION]
    means = emp.groupby("variant")[["bulk95"]].mean()
    means["sr_crit"] = 1.0 / emp.groupby("variant").bulk95.median()
    report, failures, notes = {}, [], []

    for variant, spec in _HEADLINE_448.items():
        got = float(means.loc[variant, "bulk95"])
        report[variant] = got
        ok = abs(got - spec["bulk95"]) <= spec["tol"]
        print(f"  [headline-gate] {variant:28s} bulk95 = {got:.4f} "
              f"(expected {spec['bulk95']:.4f} +/- {spec['tol']:.3f})  "
              f"{'OK' if ok else 'FAIL'}")
        if not ok:
            failures.append(f"{variant} bulk95 {got:.4f} != {spec['bulk95']:.4f}")
        if "sr_crit" in spec:
            got_sr = float(means.loc[variant, "sr_crit"])
            report[variant + "_sr_crit"] = got_sr
            ok_sr = abs(got_sr - spec["sr_crit"]) <= spec["sr_tol"]
            print(f"  [headline-gate] {variant:28s} sr_crit = {got_sr:.4f} "
                  f"(expected {spec['sr_crit']:.2f} +/- {spec['sr_tol']:.2f})  "
                  f"{'OK' if ok_sr else 'FAIL'}")
            if not ok_sr:
                failures.append(f"{variant} sr_crit {got_sr:.4f} != {spec['sr_crit']}")
        if "quoted" in spec and abs(got - spec["quoted"]) > spec["tol"]:
            median = float(emp[emp.variant == variant].bulk95.median())
            notes.append(
                f"{variant}: this gate's bulk95 = {got:.4f} is the per-seed MEAN; the "
                f"median is {median:.4f}, and ACTION_PLAN_JOURNAL_ROADMAP.md's "
                f"{spec['quoted']:.3f} is the median and is correct. The two are "
                f"aggregators of the same cells, not a discrepancy. Report the median "
                f"(CONVENTIONS, sr_crit = 1/median(bulk95)); this gate and the "
                f"mean +/- sd table in bulk95_summary.md are still on the mean and "
                f"should move to the median when E0.4 is next re-run.")

    lo, hi = _NULL_BAND
    for variant in _NULL_VARIANTS:
        got = float(means.loc[variant, "bulk95"])
        report[variant] = got
        ok = lo <= got <= hi
        print(f"  [headline-gate] {variant:28s} bulk95 = {got:.4f} "
              f"(expected in [{lo}, {hi}])  {'OK' if ok else 'FAIL'}")
        if not ok:
            failures.append(f"{variant} bulk95 {got:.4f} outside [{lo}, {hi}]")

    for note in notes:
        print(f"  [headline-gate] NOTE: {note}")
    if failures:
        raise RuntimeError(
            "[headline-gate] the documented N=448 values do NOT reproduce: "
            + "; ".join(failures)
            + ". STOP and report this before running anything downstream -- it is a "
              "more important finding than any reanalysis built on top of it.")
    print("  [headline-gate] all documented N=448 values reproduce.  [OK]")
    return {"status": "passed", "values": report, "notes": notes}


# ---------------------------------------------------------------------------
# Summary table
# ---------------------------------------------------------------------------
def summarise(df: pd.DataFrame) -> pd.DataFrame:
    """Mean / sd / min / max / median across seeds per (condition, variant).

    ``sr_crit`` is then recomputed from the median ``bulk95`` per
    ``common.SR_CRIT_CONVENTION`` -- NOT carried over from the per-seed mean of
    ``1/bulk95``, which Jensen biases upward.
    """
    grouped = df.groupby(["condition", "variant"])[_SUMMARY_METRICS]
    out = grouped.agg(["mean", "std", "min", "max", "median"])
    out.columns = [f"{metric}_{stat}" for metric, stat in out.columns]
    out = out.reset_index()
    # The reported sr_crit: invert the central bulk95, so the table is self-consistent.
    out["sr_crit"] = 1.0 / out["bulk95_median"]
    out = out.rename(columns={"sr_crit_mean": "sr_crit_perseed_mean",
                              "sr_crit_median": "sr_crit_perseed_median",
                              "sr_crit_std": "sr_crit_perseed_std"})
    out["n_seeds"] = df.groupby(["condition", "variant"]).size().to_numpy()
    # Fixed condition/variant order rather than alphabetical.
    out["_c"] = out.condition.map({c: i for i, c in enumerate(common.CONDITIONS)})
    out["_v"] = out.variant.map({v: i for i, v in enumerate(common.VARIANTS)})
    return out.sort_values(["_c", "_v"]).drop(columns=["_c", "_v"]).reset_index(drop=True)


def _markdown(summary: pd.DataFrame, scale: int, n_nodes: int, gates: dict) -> str:
    lines = [
        f"# E0.4 -- spectral characterisation of the null ladder (human N={n_nodes})\n",
        f"Scale `{scale}`, {common.N_SEEDS} seeds per cell, eigendecomposition only "
        "(no reservoir simulation).\n",
        f"`{common.BULK95_DEFINITION}`\n",
        f"`{common.SR_CRIT_CONVENTION}`\n",
        "Values are **mean ± sd across seeds**, except `sr_crit`, which is "
        "`1 / median(bulk95)` (a single number, not a mean of per-seed values). "
        "`lambda_max_raw` is the "
        "un-normalised `|λ₁|` the reservoir build divides out; every other column is "
        "on the normalised base `W / |λ₁|`. The connectome has sd = 0 by "
        "construction in the empirical column -- it is one fixed graph, only the "
        "nulls are resampled.\n",
    ]
    for condition in common.CONDITIONS:
        sub = summary[summary.condition == condition]
        if sub.empty:
            continue
        lines += [
            f"\n## `{condition}`\n",
            "| variant | bulk95 | sr_crit = 1/median(bulk95) | outlier-to-bulk gap | "
            "\\|λ₂\\|/\\|λ₁\\| | λ_max (raw) |",
            "|---|---|---|---|---|---|",
        ]
        for row in sub.itertuples():
            lines.append(
                f"| {common.VARIANT_TITLE.get(row.variant, row.variant)} "
                f"| {row.bulk95_mean:.4f} ± {row.bulk95_std:.4f} "
                f"| {row.sr_crit:.3f} "
                f"| {row.outlier_bulk_gap_mean:.4f} ± {row.outlier_bulk_gap_std:.4f} "
                f"| {row.lambda2_ratio_mean:.4f} ± {row.lambda2_ratio_std:.4f} "
                f"| {row.lambda_max_raw_mean:.4f} ± {row.lambda_max_raw_std:.4f} |")

    lines.append("\n## Gates\n")
    repro, head = gates.get("reproduction", {}), gates.get("headline", {})
    lines.append(f"- Reproduction vs committed `w_spectra.parquet`: "
                 f"**{repro.get('status', 'n/a')}**"
                 + (f" ({repro['n_cells']} cells, max abs diff "
                    f"{max(repro['max_abs_diff'].values()):.1e})"
                    if repro.get("status") == "passed" else ""))
    lines.append(f"- Documented N=448 headline values: "
                 f"**{head.get('status', 'n/a')}**")
    for note in head.get("notes", []):
        lines.append(f"- NOTE: {note}")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def run(scale: int, jobs: int = 1) -> pd.DataFrame:
    results_dir, _ = common.scale_dirs(scale)
    results_dir.mkdir(parents=True, exist_ok=True)

    raw = capture(scale, jobs)
    df = derive(raw)
    n_nodes = int(np.asarray(df.eig_w_real.iloc[0]).size)

    print("\nGates:")
    gates = {"reproduction": reproduction_gate(df, scale),
             "headline": headline_gate(df, scale)}

    summary = summarise(df)
    df.to_parquet(results_dir / "spectra_per_seed.parquet")
    print(f"\nSaved {results_dir / 'spectra_per_seed.parquet'}  ({len(df)} rows)")
    summary.to_csv(results_dir / "bulk95_summary.csv", index=False)
    print(f"Saved {results_dir / 'bulk95_summary.csv'}")
    (results_dir / "bulk95_summary.md").write_text(
        _markdown(summary, scale, n_nodes, gates))
    print(f"Saved {results_dir / 'bulk95_summary.md'}")

    common.write_manifest(
        results_dir / "manifest_tables.json", "E0.4 tables", scale,
        n_nodes=n_nodes, conditions=common.CONDITIONS, variants=common.VARIANTS,
        n_seeds=common.N_SEEDS, gates=gates,
        max_abs_imag=float(df.max_abs_imag.max()),
        source="experiments.human.analysis.manifold.spectra.capture_w_spectra "
               "-> src.analysis.spectral.recurrent_spectrum",
    )

    emp = summary[summary.condition == common.BASE_CONDITION]
    print(f"\n{common.BASE_CONDITION} (N={n_nodes}):")
    for row in emp.itertuples():
        print(f"  {common.VARIANT_TITLE.get(row.variant, row.variant):24s} "
              f"bulk95={row.bulk95_mean:.4f}±{row.bulk95_std:.4f}  "
              f"sr_crit={row.sr_crit:.3f}")
    print(f"\nmax |Im λ| over all cells = {df.max_abs_imag.max():.2e} "
          f"({'symmetric -> real spectrum' if df.max_abs_imag.max() < 1e-9 else 'COMPLEX'})")
    return df

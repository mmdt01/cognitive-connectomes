"""E0.4 step 2: ``bulk95`` as a function of the sign fraction ``f``.

``bulk95`` is not one constant per variant -- signing edges reshapes the spectrum, so
any reindexing of the *full* (f, sr) phase diagram onto an effective-criticality axis
needs ``bulk95`` per **(variant, f)** cell, not per variant. This module computes it
across the whole ``f`` grid, for both sign modes, at any scale.

Eigendecomposition only: the same graded sign transform the phase-diagram capture
applies (``src.analysis.sign_composition``), with the **identical** flip-RNG entropy
convention, then ``recurrent_spectrum``. No reservoir is built and no task is run.

The N=448 values are gated against the ``bulk95`` column already frozen in
``phase_cells.parquet``, in two tiers:

- **f = 0 (hard).** The transform is the identity there, so the value must match to
  floating-point precision. This tests the substrate and the spectral code, and it is
  the cut E0.2's memory gate uses. A failure raises.
- **f > 0 (distributional).** The flip *pattern* is not portable across machines:
  ``_select_flips`` builds its strata with ``np.argsort(escore)``, ``kind="quicksort"``
  is not stable, and ``escore`` (the endpoint-degree product) is massively tied --
  5323 edges but only 695 distinct scores at N=448, largest tie group 42. A different
  tie order moves ~40 edges between strata, and because ``rng.choice`` is then drawn
  per stratum the whole downstream selection diverges. The frozen capture ran on the
  cluster; this runs on a different CPU. So per-cell equality is *reported*, and what
  is *asserted* is that the seed x draw distribution agrees -- which is what the
  phase-diagram conclusions actually rest on.

**Consequence for downstream work:** use the ``bulk95`` frozen in
``phase_cells.parquet`` when reindexing that file's own cells; the values computed
here are a fresh, self-consistent realisation set, correct in distribution but not
cell-for-cell identical to the frozen capture at ``f > 0``. Making the flip pattern
portable needs ``kind="stable"`` in ``_select_flips`` -- a one-line change that would
invalidate the frozen capture, so it is flagged, not applied here.

Note the two sign modes differ in spectral character: ``edge`` preserves symmetry (real
spectrum, ``eigh``), while ``dale`` negates whole outgoing columns and therefore breaks
it (complex spectrum, general ``eig``) -- so ``lead_is_real`` genuinely tracks the
Perron mode going complex as the inhibitory fraction rises.

**Normality diagnostic.** Because of that, every cell also records whether ``W`` is
symmetric and how far it is from *normal*:

    non_normality = || W^T W - W W^T ||_F  /  || W ||_F^2

which is 0 exactly when ``W`` is normal (in particular whenever it is symmetric) and is
scale-invariant, so it is comparable across ``f``, variants and parcellations. This
exists to answer a specific confound question: if non-normality co-varies with ``f``,
then the sign axis is not a pure sign axis -- it is partly a normality axis, and any
claim attributed to sign composition has to be read against that. ``asymmetry``
(``||W - W^T||_F / ||W||_F``) is recorded alongside as the cruder, more legible
companion.
"""

import numpy as np
import pandas as pd

from src.analysis import sign_composition
from src.analysis.spectral import recurrent_spectrum
from experiments.human.substrates import HumanSubstrateBuilder
from experiments.human.analysis.phase_diagram import common as pd_common
from experiments.human.analysis.eigenspectrum import common


def normality_measures(W: np.ndarray) -> dict:
    """Scale-invariant distance of ``W`` from normal, and from symmetric.

    ``non_normality = ||W^T W - W W^T||_F / ||W||_F^2`` is zero exactly when ``W`` is
    normal (its eigenvectors are orthogonal and the spectrum alone governs the
    dynamics). ``asymmetry = ||W - W^T||_F / ||W||_F`` is the blunter companion. Both
    are dimensionless, so they compare across ``f``, variant and N.
    """
    W = np.asarray(W, dtype=float)
    frob_sq = float((W * W).sum())
    if frob_sq <= 0.0:
        return {"non_normality": 0.0, "asymmetry": 0.0}
    commutator = W.T @ W - W @ W.T
    return {
        "non_normality": float(np.linalg.norm(commutator, "fro") / frob_sq),
        "asymmetry": float(np.linalg.norm(W - W.T, "fro") / np.sqrt(frob_sq)),
    }


def cell(spec, state) -> list:
    """One (sign_mode, variant, f_idx, seed, draw) -> one row of spectral scalars."""
    sign_mode, variant, f_idx, seed, draw = spec
    builder = state["builder"]
    f = common.F_GRID[f_idx]
    targeting = common.F_TARGETING

    W_base = builder.weighted(common.BASE_CONDITION, variant, seed)
    node_score = sign_composition.node_importance(W_base, mode=common.F_SCORE_MODE)

    # Identical entropy convention to phase_diagram.capture.capture_cell: the degree
    # score adds no salt (it is the committed headline), dale adds its own.
    seed_key = [int(seed), int(f_idx), int(draw),
                pd_common.TARGETING_CODE[targeting],
                pd_common.VARIANT_CODE[variant]]
    if sign_mode == "dale":
        seed_key.append(pd_common.SIGN_MODE_CODE["dale"])
    flip_rng = np.random.default_rng(seed_key)

    if sign_mode == "dale":
        W = sign_composition.sign_fraction_matrix_dale(
            W_base, f, targeting, flip_rng, n_strata=common.N_STRATA,
            node_score=node_score)
        realised = sign_composition.realised_inhibitory_fraction(W)
    else:
        W = sign_composition.sign_fraction_matrix(
            W_base, f, targeting, flip_rng, n_strata=common.N_STRATA,
            node_score=node_score)
        realised = sign_composition.negative_fraction(W)

    rs = recurrent_spectrum(W)
    bulk95 = float(rs["bulk95_radius"])
    normality = normality_measures(W)
    return [dict(
        sign_mode=sign_mode, targeting=targeting, score=common.F_SCORE_MODE,
        f=float(f), variant=variant, seed=int(seed), draw=int(draw),
        bulk95=bulk95, sr_crit=1.0 / bulk95, outlier_bulk_gap=1.0 - bulk95,
        lambda2_ratio=1.0 - float(rs["spectral_gap"]),
        perron_root=float(rs["perron_root"]),
        lambda_max_raw=float(rs["base_spectral_radius"]),
        is_symmetric=bool(rs["is_symmetric"]),
        lead_is_real=bool(abs(float(rs["eig_imag"][0])) < 1e-9),
        realised_f=float(realised),
        **normality,
    )]


def capture(scale: int, jobs: int, sign_modes) -> pd.DataFrame:
    builder = HumanSubstrateBuilder(scale=scale)
    if jobs > 1:
        for variant in common.F_VARIANTS:
            if variant == "connectome_weight_permuted":
                continue
            for seed in range(common.N_SEEDS):
                builder.get_mask(variant, seed)
    cells = [
        (sign_mode, variant, f_idx, seed, draw)
        for sign_mode in sign_modes
        for variant in common.F_VARIANTS
        for f_idx in range(len(common.F_GRID))
        for seed in range(common.N_SEEDS)
        for draw in range(common.N_DRAWS)
    ]
    print(f"bulk95(f): {len(cells)} cells "
          f"(sign_modes={list(sign_modes)} x {len(common.F_VARIANTS)} variants x "
          f"{len(common.F_GRID)} f x {common.N_SEEDS} seeds x {common.N_DRAWS} draws), "
          f"targeting={common.F_TARGETING}, score={common.F_SCORE_MODE}, jobs={jobs}")
    return common.run_cells(cells, cell, {"builder": builder}, jobs, "bulk95-f")


# ---------------------------------------------------------------------------
# Gate: reproduce the frozen phase-diagram bulk95 column
# ---------------------------------------------------------------------------
_GATE_KEYS = ["sign_mode", "targeting", "f", "variant", "seed", "draw"]


_EXACT_TOL = 1e-12          # floating-point noise only
_DIST_SIGMA = 4.0           # |mean difference| allowed, in combined standard errors


def phase_cells_gate(df: pd.DataFrame, scale: int) -> dict:
    """Two-tier comparison against ``phase_cells.parquet``'s frozen ``bulk95``.

    ``bulk95`` is a property of the signed W alone, so it is constant across the task
    and sr axes of the phase capture -- one value per key. Only the variants the phase
    diagram actually ran are comparable (it omitted the weight-permuted control).

    Tier 1 (f = 0) is asserted exactly; tier 2 (f > 0) is asserted only in
    distribution, for the tie-ordering reason in the module docstring."""
    path = common.committed_phase_cells(scale)
    if not path.exists():
        print(f"  [phase-gate] no committed phase_cells at {path} -- skipped.")
        return {"status": "skipped", "reference": str(path)}

    ref = pd.read_parquet(path, columns=_GATE_KEYS + ["bulk95"])
    ref = ref[ref.targeting == common.F_TARGETING]
    ref = ref.groupby(_GATE_KEYS, as_index=False).bulk95.first()
    ref["f"] = ref.f.round(6)

    mine = df.copy()
    mine["f"] = mine.f.round(6)
    merged = mine.merge(ref, on=_GATE_KEYS, how="inner", suffixes=("", "_ref"))
    if merged.empty:
        raise RuntimeError(
            f"[phase-gate] no overlapping cells with {path.name}; the grid or the key "
            "convention has drifted.")
    merged["abs_diff"] = (merged.bulk95 - merged.bulk95_ref).abs()
    covered = sorted(merged.variant.unique())
    print(f"  [phase-gate] {len(merged)} shared cells (variants {covered}).")

    # --- Tier 1: f = 0 must be exact (the transform is the identity there) -----
    zero = merged[merged.f == 0.0]
    zero_worst = float(zero.abs_diff.max()) if not zero.empty else float("nan")
    print(f"  [phase-gate] f=0 ({len(zero)} cells): max |new - frozen| = "
          f"{zero_worst:.3e}  {'OK' if zero_worst <= _EXACT_TOL else 'FAIL'}")
    if not np.isfinite(zero_worst) or zero_worst > _EXACT_TOL:
        raise RuntimeError(
            f"[phase-gate] the f=0 identity cells do NOT reproduce "
            f"{path.name} (max diff {zero_worst:.3e}). STOP -- the substrate or the "
            "spectral code has changed, which invalidates every bulk95 downstream.")

    # --- Tier 2: f > 0 per-cell (reported) then distributional (asserted) ------
    pos = merged[merged.f > 0.0]
    pos_worst = float(pos.abs_diff.max()) if not pos.empty else 0.0
    n_exact = int((pos.abs_diff <= _EXACT_TOL).sum())
    print(f"  [phase-gate] f>0 ({len(pos)} cells): max |new - frozen| = "
          f"{pos_worst:.3e}, cell-for-cell identical: {n_exact}/{len(pos)}")

    dist_rows, dist_fail = [], []
    if not pos.empty and pos_worst > _EXACT_TOL:
        print("  [phase-gate] per-cell reproduction FAILED -> testing agreement in "
              "DISTRIBUTION over seed x draw (see module docstring: unstable argsort "
              "tie order makes the flip pattern machine-dependent).")
        for (sign_mode, variant, f), group in pos.groupby(["sign_mode", "variant", "f"]):
            a, b = group.bulk95.to_numpy(float), group.bulk95_ref.to_numpy(float)
            n = a.size
            sem = float(np.sqrt(a.var(ddof=1) / n + b.var(ddof=1) / n))
            delta = float(a.mean() - b.mean())
            z = abs(delta) / sem if sem > 0 else (0.0 if delta == 0 else np.inf)
            ok = z <= _DIST_SIGMA
            dist_rows.append(dict(sign_mode=sign_mode, variant=variant, f=float(f),
                                  mean_new=float(a.mean()), mean_ref=float(b.mean()),
                                  delta=delta, sem=sem, z=float(z), n=n, ok=bool(ok)))
            if not ok:
                dist_fail.append(dist_rows[-1])
        worst = max(dist_rows, key=lambda r: r["z"]) if dist_rows else None
        print(f"  [phase-gate] {len(dist_rows) - len(dist_fail)}/{len(dist_rows)} "
              f"(sign_mode, variant, f) groups agree in mean within "
              f"{_DIST_SIGMA:g} SE")
        if worst is not None:
            print(f"  [phase-gate] worst group: {worst['sign_mode']}/"
                  f"{worst['variant']} f={worst['f']:g}  mean {worst['mean_new']:.4f} "
                  f"vs {worst['mean_ref']:.4f}  (delta {worst['delta']:+.4f} = "
                  f"{worst['z']:.2f} SE, n={worst['n']})")
        if dist_fail:
            raise RuntimeError(
                f"[phase-gate] bulk95(f) disagrees with the frozen capture in "
                f"DISTRIBUTION, not just per cell ({len(dist_fail)} of "
                f"{len(dist_rows)} groups beyond {_DIST_SIGMA:g} SE). STOP -- this is "
                "not a tie-ordering artefact; the transform itself differs, which "
                "would invalidate the phase diagram.")
        print("  [phase-gate] distributions agree: a flip-pattern (tie-order) "
              "difference, not a transform difference.  [OK, with caveat]")

    status = ("passed" if pos_worst <= _EXACT_TOL
              else "passed_in_distribution")
    return {"status": status, "reference": str(path), "n_cells": len(merged),
            "variants_covered": covered,
            "f0_max_abs_diff": zero_worst, "fpos_max_abs_diff": pos_worst,
            "fpos_cells_identical": n_exact, "fpos_cells": int(len(pos)),
            "distribution_groups": len(dist_rows),
            "distribution_failures": len(dist_fail),
            "distribution_worst_z": (max(r["z"] for r in dist_rows)
                                     if dist_rows else None),
            "caveat": (None if pos_worst <= _EXACT_TOL else
                       "f>0 flip pattern is not machine-portable (unstable np.argsort "
                       "tie order over a heavily-tied edge score); distributions "
                       "agree. Use phase_cells.parquet's own bulk95 column when "
                       "reindexing that file's cells.")}


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
def summarise(df: pd.DataFrame) -> pd.DataFrame:
    out = (df.groupby(["sign_mode", "variant", "f"], as_index=False)
           .agg(bulk95_mean=("bulk95", "mean"), bulk95_std=("bulk95", "std"),
                sr_crit_mean=("sr_crit", "mean"), sr_crit_std=("sr_crit", "std"),
                perron_root_mean=("perron_root", "mean"),
                lead_is_real_frac=("lead_is_real", "mean"),
                realised_f_mean=("realised_f", "mean"),
                symmetric_frac=("is_symmetric", "mean"),
                non_normality_mean=("non_normality", "mean"),
                non_normality_std=("non_normality", "std"),
                asymmetry_mean=("asymmetry", "mean"),
                n=("bulk95", "size")))
    out["_v"] = out.variant.map({v: i for i, v in enumerate(common.F_VARIANTS)})
    return (out.sort_values(["sign_mode", "_v", "f"]).drop(columns="_v")
            .reset_index(drop=True))


def _markdown(summary: pd.DataFrame, scale: int, gate: dict) -> str:
    lines = [
        f"# E0.4 -- `bulk95` as a function of sign fraction `f` (human N={scale})\n",
        f"Targeting `{common.F_TARGETING}` (placement-neutral), score "
        f"`{common.F_SCORE_MODE}`, {common.N_SEEDS} seeds x {common.N_DRAWS} draws "
        "per cell. Eigendecomposition only.\n",
        "`bulk95` is a property of the signed matrix, so it is independent of both "
        "the spectral radius and the task -- but **not** of `f`. Any "
        "effective-criticality reindex of the full (f, sr) panel must use the value "
        "for that variant's own `f` cell.\n",
        f"Phase-diagram reproduction gate: **{gate.get('status', 'n/a')}**"
        + (f" ({gate['n_cells']} shared cells; f=0 exact to "
           f"{gate['f0_max_abs_diff']:.1e}; f>0 identical in "
           f"{gate['fpos_cells_identical']}/{gate['fpos_cells']} cells, "
           f"{gate['distribution_groups'] - gate['distribution_failures']}/"
           f"{gate['distribution_groups']} groups agreeing in mean, worst "
           f"{gate['distribution_worst_z']:.2f} SE)"
           if gate.get("status") == "passed_in_distribution" else "")
        + "\n",
    ]
    if gate.get("caveat"):
        lines.append(f"> **Caveat.** {gate['caveat']}\n")
    for sign_mode in sorted(summary.sign_mode.unique()):
        sub = summary[summary.sign_mode == sign_mode]
        variants = [v for v in common.F_VARIANTS if v in set(sub.variant)]
        f_values = sorted(sub.f.unique())
        lines += [f"\n## `{sign_mode}` sign mode -- mean `bulk95`\n",
                  "| variant | " + " | ".join(f"f={f:g}" for f in f_values) + " |",
                  "|---|" + "---|" * len(f_values)]
        for variant in variants:
            row = sub[sub.variant == variant].set_index("f").bulk95_mean
            cells = " | ".join(f"{row.get(f, float('nan')):.4f}" for f in f_values)
            lines.append(f"| {common.VARIANT_TITLE.get(variant, variant)} | {cells} |")
        lines += [f"\n### `{sign_mode}` -- implied `sr_crit = 1/bulk95`\n",
                  "| variant | " + " | ".join(f"f={f:g}" for f in f_values) + " |",
                  "|---|" + "---|" * len(f_values)]
        for variant in variants:
            row = sub[sub.variant == variant].set_index("f").sr_crit_mean
            cells = " | ".join(f"{row.get(f, float('nan')):.3f}" for f in f_values)
            lines.append(f"| {common.VARIANT_TITLE.get(variant, variant)} | {cells} |")

        lines += [
            f"\n### `{sign_mode}` -- non-normality "
            "`||WᵀW − WWᵀ||_F / ||W||_F²` (0 = normal)\n",
            "| variant | " + " | ".join(f"f={f:g}" for f in f_values) + " |",
            "|---|" + "---|" * len(f_values)]
        for variant in variants:
            row = sub[sub.variant == variant].set_index("f").non_normality_mean
            cells = " | ".join(f"{row.get(f, float('nan')):.3e}" for f in f_values)
            lines.append(f"| {common.VARIANT_TITLE.get(variant, variant)} | {cells} |")
        sym = sub.symmetric_frac
        lines.append(f"\nFraction of cells with symmetric `W`: "
                     f"{float(sym.min()):.2f}–{float(sym.max()):.2f}.\n")
    return "\n".join(lines) + "\n"


def run(scale: int, jobs: int = 1, sign_modes=None) -> pd.DataFrame:
    sign_modes = common.F_SIGN_MODES if sign_modes is None else sign_modes
    results_dir, _ = common.scale_dirs(scale)
    results_dir.mkdir(parents=True, exist_ok=True)

    df = capture(scale, jobs, sign_modes)

    # Persist before gating: a gate failure is a finding to inspect, not a reason to
    # throw away the eigendecompositions that produced it.
    df.to_parquet(results_dir / "bulk95_vs_f.parquet")
    print(f"\nSaved {results_dir / 'bulk95_vs_f.parquet'}  ({len(df)} rows)")

    print("\nGate:")
    gate = phase_cells_gate(df, scale)

    summary = summarise(df)
    summary.to_csv(results_dir / "bulk95_vs_f_summary.csv", index=False)
    print(f"Saved {results_dir / 'bulk95_vs_f_summary.csv'}")
    (results_dir / "bulk95_vs_f_summary.md").write_text(
        _markdown(summary, scale, gate))
    print(f"Saved {results_dir / 'bulk95_vs_f_summary.md'}")

    common.write_manifest(
        results_dir / "manifest_bulk95_f.json", "E0.4 bulk95-vs-f", scale,
        f_grid=common.F_GRID, variants=common.F_VARIANTS, sign_modes=list(sign_modes),
        targeting=common.F_TARGETING, score_mode=common.F_SCORE_MODE,
        n_seeds=common.N_SEEDS, n_draws=common.N_DRAWS, n_strata=common.N_STRATA,
        base_condition=common.BASE_CONDITION, gate=gate,
        source="src.analysis.sign_composition + src.analysis.spectral.recurrent_spectrum",
    )

    print("\nmean bulk95 at f = 0 / 0.25 / 0.5:")
    for sign_mode in sorted(summary.sign_mode.unique()):
        for variant in common.F_VARIANTS:
            row = summary[(summary.sign_mode == sign_mode)
                          & (summary.variant == variant)].set_index("f").bulk95_mean
            if row.empty:
                continue
            print(f"  {sign_mode:5s} {common.VARIANT_TITLE.get(variant, variant):18s} "
                  f"{row.get(0.0, float('nan')):.4f}  {row.get(0.25, float('nan')):.4f}  "
                  f"{row.get(0.5, float('nan')):.4f}")
    return df

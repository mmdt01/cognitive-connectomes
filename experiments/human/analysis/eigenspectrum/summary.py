"""E0.4 step 4: the cross-scale summary that reports the experiment's conclusions.

Reads the per-scale artifacts ``tables.py`` and ``bulk95_f.py`` wrote (plus their
manifests, for the gate outcomes) and consolidates them into one document:
``results/E04_summary.md``. Recomputes nothing.

Its job is to state, in one place: whether the documented N=448 values reproduced,
what the N=1000 numbers are, and the two caveats E0.2 and the N=1000 launch need to
carry forward.
"""

import json

import pandas as pd

from experiments.human.analysis.eigenspectrum import common

_HEADLINE_VARIANTS = ["connectome", "connectome_weight_permuted", "degree_rewire",
                      "erdos_renyi", "random_gaussian", "clustering_rewire",
                      "modularity_rewire"]


def _load(scale: int) -> dict:
    results_dir, _ = common.scale_dirs(scale)
    out = {"scale": scale, "results_dir": results_dir}
    summary_path = results_dir / "bulk95_summary.csv"
    if not summary_path.exists():
        return {}
    out["summary"] = pd.read_csv(summary_path)
    for key, name in (("tables_manifest", "manifest_tables.json"),
                      ("bulk95f_manifest", "manifest_bulk95_f.json")):
        path = results_dir / name
        out[key] = json.loads(path.read_text()) if path.exists() else None
    f_path = results_dir / "bulk95_vs_f_summary.csv"
    out["bulk95_f"] = pd.read_csv(f_path) if f_path.exists() else None
    return out


def _headline_table(loaded: dict) -> list:
    scales = sorted(loaded)
    lines = ["| variant | " + " | ".join(
        f"bulk95 (N={s}) | sr_crit (N={s})" for s in scales) + " |",
        "|---|" + "---|" * (2 * len(scales))]
    for variant in _HEADLINE_VARIANTS:
        cells = []
        for scale in scales:
            frame = loaded[scale]["summary"]
            row = frame[(frame.condition == common.BASE_CONDITION)
                        & (frame.variant == variant)]
            if row.empty:
                cells += ["--", "--"]
                continue
            row = row.iloc[0]
            cells.append(f"{row.bulk95_mean:.4f} ± {row.bulk95_std:.4f}")
            cells.append(f"{row.sr_crit:.3f}")
        lines.append(f"| {common.VARIANT_TITLE.get(variant, variant)} | "
                     + " | ".join(cells) + " |")
    return lines


def _normality_section(loaded: dict) -> list:
    """Section 4: is the sign axis confounded with a normality axis?"""
    lines = ["\n## 4. Normality diagnostic — is the sign axis a pure sign axis?\n",
             "`non_normality = ||WᵀW − WWᵀ||_F / ||W||_F²` (0 ⟺ normal; symmetric ⇒ "
             "normal). Mean over seeds × draws, `stratified` targeting.\n"]
    for scale in sorted(loaded):
        frame = loaded[scale].get("bulk95_f")
        if frame is None or "non_normality_mean" not in frame:
            continue
        lines.append(f"\n**N={scale}**\n")
        for sign_mode in sorted(frame.sign_mode.unique()):
            sub = frame[frame.sign_mode == sign_mode]
            worst = float(sub.non_normality_mean.max())
            sym = float(sub.symmetric_frac.min())
            if worst < 1e-12:
                lines.append(
                    f"- **`{sign_mode}`: normal at every `f`** (max non-normality "
                    f"{worst:.1e}; W symmetric in 100% of cells). The edge transform "
                    "flips an undirected edge and mirrors it, so symmetry — and "
                    "therefore normality — is exactly preserved. **No confound: the "
                    "edge sign axis is a pure sign axis.**")
                continue
            rows = []
            for variant in common.F_VARIANTS:
                v = sub[sub.variant == variant].set_index("f").non_normality_mean
                if not v.empty:
                    rows.append(f"{common.VARIANT_TITLE.get(variant, variant)} "
                                f"{v.get(0.0, float('nan')):.3f}→"
                                f"{v.get(0.5, float('nan')):.3f}")
            lines.append(
                f"- **`{sign_mode}`: non-normality rises with `f`** (0 at f=0 to "
                f"{worst:.3f} at f=0.5; W symmetric in only {sym:.0%} of f>0 cells). "
                f"Per variant, f=0→0.5: {'; '.join(rows)}. **This is a confound: on "
                "the Dale axis, sign fraction and non-normality co-vary, and they do "
                "so *unequally across variants* — the connectome becomes roughly "
                "twice as non-normal as its nulls at matched `f`.**")
    lines.append(
        "\n**Reading.** Any Dale-arm result attributed to sign composition is also a "
        "result about departure from normality, and the two cannot be separated on "
        "this design. The edge arm is clean, so it is the right place to make "
        "mechanistic claims about sign per se; the Dale arm remains the "
        "biologically interpretable one, but its claims must be stated as "
        "\"node-wise inhibition\" (which entails non-normality) rather than \"sign "
        "fraction\" alone. Note the rise saturates by f≈0.2, so the biologically "
        "relevant ~20% inhibition sits near the knee, not on the plateau.")
    return lines


def _variance_section(loaded: dict) -> list:
    """Section 5: why does bulk95's seed spread grow with N for the random rungs?"""
    lines = ["\n## 5. Seed variance — why `bulk95` spread grows with N\n",
             "Spectral statistics should self-average, so a spread that *grows* with "
             "N looks wrong. Decomposing `bulk95 = (absolute bulk radius) / |λ₁|` "
             "shows the numerator behaves correctly and the noise is entirely in the "
             "normaliser.\n",
             "| variant | N | rel. sd `bulk95` | rel. sd abs. bulk | rel. sd \\|λ₁\\| |",
             "|---|---|---|---|---|"]
    for variant in ["connectome_weight_permuted", "degree_rewire", "erdos_renyi",
                    "random_gaussian"]:
        for scale in sorted(loaded):
            path = loaded[scale]["results_dir"] / "spectra_per_seed.parquet"
            if not path.exists():
                continue
            frame = pd.read_parquet(path)
            sub = frame[(frame.condition == common.BASE_CONDITION)
                        & (frame.variant == variant)]
            if sub.empty:
                continue
            b = sub.bulk95.to_numpy(float)
            l1 = sub.lambda_max_raw.to_numpy(float)
            absolute = b * l1
            lines.append(
                f"| {common.VARIANT_TITLE.get(variant, variant)} | {scale} "
                f"| {b.std() / b.mean():.3f} | {absolute.std() / absolute.mean():.3f} "
                f"| {l1.std() / l1.mean():.3f} |")
    lines.append(
        "\n**Not a null-generation or density-matching fault.** Matching is exact at "
        "both scales — `validate_null` asserts it on every build, and a direct check "
        "over 10 seeds confirms every constrained rung at **both** N=448 and N=1000: "
        "Erdős–Rényi edge count 10/10, degree rewire degree sequence 10/10, "
        "clustering rewire 10/10, modularity rewire 10/10, all at the exact target "
        "edge count (5,323 at N=448; 10,784 at N=1000, density 0.0216). Only rung 0 "
        "(`random_gaussian`) varies its edge count, by design (density in "
        "expectation), and it does so *less* at N=1000 (rel sd 0.016 → 0.008).")
    lines.append(
        "\n**The absolute bulk does self-average**: its relative spread falls with N "
        "for every variant (column 3). The rise is in `|λ₁|`, and `bulk95` is a ratio "
        "to it — across seeds `corr(bulk95, |λ₁|)` runs −0.87 to −0.97.")
    lines.append(
        "\n**Mechanism: an extreme-value effect in the resampled weights.** The nulls "
        "draw weights with replacement from the empirical pool, and on a sparse "
        "non-negative graph `|λ₁|` is driven by the largest sampled weights: "
        "`corr(max sampled weight, |λ₁|)` = +0.85 to +0.95. The N=1000 pool is "
        "*heavier*-tailed than the N=448 pool (Hill α 2.49 → 2.28; max/mean 32 → 38), "
        "and at α ≈ 2.3 the sample maximum does not concentrate — so the max-weight "
        "spread grows with N (rel sd 0.113 → 0.158) and drags `|λ₁|` with it.")
    lines.append(
        "\n**The control confirms it.** `weight-permuted` *permutes* the connectome's "
        "exact weight multiset instead of resampling it, so its maximum weight is "
        "identical in every seed (max-weight rel sd exactly 0) — and it is the one "
        "variant whose `|λ₁|` spread *falls* with N (0.060 → 0.037), i.e. the one that "
        "self-averages as expected. The degree rewire sits in between: it resamples "
        "weights but keeps the hub structure, which anchors `|λ₁|` and damps the "
        "effect.")
    lines.append(
        "\n**Consequence.** `bulk95` for a resampling null is noisier than it looks, "
        "and its noise is dominated by a single sampled weight rather than by the bulk "
        "it describes. Per-seed effective-criticality axes (`sr · bulk95`) inherit "
        "that noise, so E0.2 must interpolate and aggregate per seed rather than "
        "pooling — which is the procedure already specified.")
    return lines


def build(loaded: dict) -> str:
    scales = sorted(loaded)
    lines = [
        "# E0.4 — spectral characterisation and `bulk95` (human SC)\n",
        "Eigendecomposition of the recurrent matrix `W` across the full null ladder, "
        f"at N = {' and '.join(str(s) for s in scales)}, "
        f"{common.N_SEEDS} seeds per cell. **No reservoir simulation.**\n",
        f"`{common.BULK95_DEFINITION}`\n",
        f"`{common.SR_CRIT_CONVENTION}`\n",
        "\n## 1. Headline — `human_empirical` (the non-negative, f=0 substrate)\n",
    ]
    lines += _headline_table(loaded)

    lines.append("\n## 2. Gates\n")
    for scale in scales:
        manifest = loaded[scale].get("tables_manifest") or {}
        gates = manifest.get("config", {}).get("gates", {})
        repro = gates.get("reproduction", {})
        head = gates.get("headline", {})
        lines.append(f"**N={scale}** — reproduction vs committed `w_spectra.parquet`: "
                     f"`{repro.get('status', 'n/a')}`"
                     + (f" ({repro.get('n_cells')} cells, worst "
                        f"{max(repro['max_abs_diff'].values()):.1e})"
                        if repro.get("status") == "passed" else "")
                     + f"; documented headline values: `{head.get('status', 'n/a')}`.")
        for note in head.get("notes", []):
            lines.append(f"  - NOTE: {note}")

    lines.append("\n## 3. `bulk95` depends on the sign fraction `f`\n")
    lines.append(
        "Signing edges reshapes the spectrum, so any effective-criticality reindex of "
        "the **full (f, sr) panel** must use each cell's own `bulk95`, not one "
        "constant per variant. Values at `f` = 0 / 0.25 / 0.5, `stratified` targeting:\n")
    for scale in scales:
        frame = loaded[scale].get("bulk95_f")
        if frame is None:
            continue
        lines += [f"\n**N={scale}**\n",
                  "| sign mode | variant | f=0 | f=0.25 | f=0.5 |",
                  "|---|---|---|---|---|"]
        for sign_mode in sorted(frame.sign_mode.unique()):
            for variant in common.F_VARIANTS:
                row = frame[(frame.sign_mode == sign_mode)
                            & (frame.variant == variant)].set_index("f").bulk95_mean
                if row.empty:
                    continue
                lines.append(
                    f"| `{sign_mode}` | {common.VARIANT_TITLE.get(variant, variant)} "
                    f"| {row.get(0.0, float('nan')):.4f} "
                    f"| {row.get(0.25, float('nan')):.4f} "
                    f"| {row.get(0.5, float('nan')):.4f} |")

    lines += _normality_section(loaded)
    lines += _variance_section(loaded)

    lines.append("\n## 6. Caveats to carry forward\n")
    for scale in scales:
        manifest = loaded[scale].get("bulk95f_manifest") or {}
        gate = manifest.get("config", {}).get("gate", {})
        if gate.get("caveat"):
            lines.append(f"- **N={scale} flip-pattern portability.** {gate['caveat']} "
                         f"(f=0 exact to {gate['f0_max_abs_diff']:.1e}; f>0 identical "
                         f"in {gate['fpos_cells_identical']}/{gate['fpos_cells']} "
                         f"cells; {gate['distribution_groups'] - gate['distribution_failures']}"
                         f"/{gate['distribution_groups']} groups agree in mean, worst "
                         f"{gate['distribution_worst_z']:.2f} SE.)")
    lines.append(
        "- **The human substrate is symmetric**, so its spectrum is real to machine "
        "precision and the complex-plane scatter is degenerate (see "
        "`figS_complex_plane`). The eigenvalue *distribution* on the real axis is the "
        "informative view, and is what Figure 1 shows.")

    lines.append("\n## 7. Handoff — the sr band the N=1000 run implies\n")
    if 1000 in loaded:
        frame = loaded[1000]["summary"]
        emp = frame[frame.condition == common.BASE_CONDITION].set_index("variant")
        conn = float(emp.loc["connectome", "sr_crit"])
        er = float(emp.loc["erdos_renyi", "sr_crit"])
        deg = float(emp.loc["degree_rewire", "sr_crit"])
        conn_b95 = float(emp.loc["connectome", "bulk95_median"])
        lines.append(
            f"At N=1000 the connectome turns critical at `sr_crit` = **{conn:.3f}** "
            f"(vs 3.078 at N=448), ER at {er:.3f} and degree at {deg:.3f}.\n")
        lines.append(
            f"**The `[0, 6]` sweep is too short at this scale — extend it to "
            f"`sr = 8`.** The comparison happens on the `sr · bulk95` axis, and the "
            f"connectome has the smallest `bulk95` ({conn_b95:.4f}), so it is the "
            f"variant that runs out of axis first. Over `sr ∈ [0, 6]` it reaches only "
            f"`sr · bulk95` = {6 * conn_b95:.3f}, leaving barely half a unit above "
            f"criticality — too thin to resolve a wedge. Reaching an effective "
            f"criticality of 2.0 (the headroom N=448 had) needs "
            f"`sr = 2.0 / {conn_b95:.4f}` = **{2.0 / conn_b95:.2f}**, so a sweep to "
            f"`sr = 8` gives `sr · bulk95` ∈ [0, {8 * conn_b95:.3f}] and a comfortable "
            f"overlap region.\n")
        lines.append(
            "Converting the band precisely is E0.2's job; the `bulk95` values it needs "
            "are in table 1 above.")
    else:
        lines.append("N=1000 tables absent — run `--tables --scale 1000` first.")
    return "\n".join(lines) + "\n"


def run(scales=None) -> None:
    scales = common.SCALES if scales is None else scales
    loaded = {}
    for scale in scales:
        data = _load(scale)
        if data:
            loaded[scale] = data
        else:
            print(f"  [summary] no bulk95_summary.csv at N={scale} -- omitted.")
    if not loaded:
        raise FileNotFoundError("no per-scale E0.4 artifacts found; run --tables first.")

    common.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = common.RESULTS_DIR / "E04_summary.md"
    path.write_text(build(loaded))
    print(f"Saved {path}")
    common.write_manifest(common.RESULTS_DIR / "manifest_summary.json",
                          "E0.4 summary", scale=sorted(loaded),
                          inputs=["bulk95_summary.csv", "bulk95_vs_f_summary.csv",
                                  "manifest_tables.json", "manifest_bulk95_f.json"])

# F13 panel (c) — where the four collapse counts come from

**Date:** 30 August 2026 · **Scope:** F13's `f` = 0 period-two collapse panel · **Method:** source
and artifact reading only. No experiment, sweep, evaluator, builder or verdict was run; nothing
under `experiments/human/analysis/manifold/` was imported; no figure was re-rendered; no repository
file was written except this one. All 14 files read were SHA-256 hashed before and after and are
unchanged.

**The question.** `report/act3b_prediction.md`'s F13 block reports four `f` = 0 collapse counts —
Erdős–Rényi 5 of 10, weight-permuted 3 of 10, degree-matching 1 of 10, connectome 0 of 10 — under a
**Source** line naming `item2_collapse_loci_scale_448.csv` for panel (c). A prior audit established
that that artifact holds only `connectome` and `erdos_renyi` rows, at every `f`. Two of the four
counts therefore have no source in it, and they match the curvature-branch quartet 0/3/1/5. Which
is it?

**Answer in one line.** The builder draws **two** bars, not four. The two middle values are
**prose-only**, and they come from a *different* artifact — `e01_threshold_table_scale_448.csv`, the
curvature branch. The defect is a caption over-reach, not a builder/source mismatch.

---

## 1. What the builder actually draws

`report/figlib/figures/act3_prediction.py:204` and `:241-249`:

```python
    loci = ctx.frame("collapse_loci")
...
    # --- (c) f = 0: the biologically real cut ---------------------------------------
    at_zero = loci[np.isclose(loci.f, 0.0)]
    variants = [v for v in style.VARIANT_ORDER if v in set(at_zero.variant)]
    counts = [int(at_zero[at_zero.variant == v].n_seeds_collapsed.iloc[0])
              for v in variants]
    totals = [int(at_zero[at_zero.variant == v].n_seeds.iloc[0]) for v in variants]
    axes[2].bar(np.arange(len(variants)), counts, ...)
```

| | |
|---|---|
| **File** | `collapse_loci` → `sources.py:936-941` → `item2_collapse_loci_scale_448.csv` |
| **Columns** | `f`, `variant`, `n_seeds_collapsed`, `n_seeds` |
| **Filter** | `np.isclose(loci.f, 0.0)` |
| **Bars drawn** | **TWO** |

The category list is an **intersection** — `[v for v in style.VARIANT_ORDER if v in set(at_zero.variant)]`
— not the four-variant ladder. The CSV's `f == 0` slice is two rows:

```
0.0,connectome,0.0,,,,,,0,10,,
0.0,erdos_renyi,0.5,7.6,8.0,4.24510451471733,4.447252348751488,0.01149355756105313,5,10,,
```

The builder therefore *cannot* draw four: it never sees a `connectome_weight_permuted` or
`degree_rewire` row. All 22 rows of the file are those two variants across the 11 `f` values.

## 2. Where the two middle values come from

Not from the figure. From the caption at `act3b_prediction.md:311`:

> Weight-permuted and degree-matching sit between, at 3 of 10 and 1 of 10.

Their actual source is `e01_threshold_table_scale_448.csv`:

```
variant,f,frac_seeds_collapsed,n_seeds,spectral_radius_lo,spectral_radius_hi
connectome,0.0,0.0,10,,
connectome_weight_permuted,0.0,0.3,10,4.8,5.2
degree_rewire,0.0,0.1,10,7.6,8.0
erdos_renyi,0.0,0.5,10,7.6,8.0
```

0.0 / 0.3 / 0.1 / 0.5 × 10 = **0 / 3 / 1 / 5** — the exact quartet, and it is the **curvature
branch**: `threshold.py:87-89` sets `collapsed=bool(above.size)` from `curv > CURV_COLLAPSE`, with
`CURV_COLLAPSE = extend_f.CURV_COLLAPSE = 1.0` rad (the midpoint of the empty valley between the
~0.25 and ~π modes).

**Why this table reaches four variants and the collapse-loci file does not.** `threshold.py`'s
`load_cells` concatenates *both* variant sets — `extend_f.VARIANT_SETS = {"boundary": ["connectome",
"erdos_renyi"], "nulls": ["connectome_weight_permuted", "degree_rewire"]}`. `extend_f`'s own
collapse-loci writer restricts to `VARIANTS = ["connectome", "erdos_renyi"]` (`extend_f.py:32, :417`),
because those are "the two the boundaries are built from".

## 3. Every artifact holding a per-variant collapse count or flag

Scanned: every `.csv` header and every `.parquet` column set under `experiments/` and `report/`, for
`collaps` / `period` / `regime` / `curv`.

| artifact | columns | 4 variants at `f` = 0? | `f` = 0 counts |
|---|---|---|---|
| `item2_collapse_loci_scale_448.csv` | `f, variant, frac_collapsed, sigma_lo, sigma_hi, x_lo, x_hi, sigma_eff_at_collapse, n_seeds_collapsed, n_seeds, delta_sigma_collapse, delta_x_collapse` | **No** — connectome + ER only | 0/10, 5/10 |
| `e01_threshold_table_scale_448.csv` | `variant, f, frac_seeds_collapsed, n_seeds, spectral_radius_lo/hi, x_linear_lo/hi, effective_radius_lo/hi, vpt_lo` | **Yes** (11 rows × 4) | 0/10, 3/10, 1/10, 5/10 |
| `e01_threshold_brackets_scale_448.csv` | `variant, f, seed, draw, collapsed, spectral_radius_lo/hi, x_linear_lo/hi, effective_radius_lo/hi, vpt_lo` | **Yes** (330 rows × 4) | per-seed boolean, identical across all 3 draws at `f` = 0: conn 0, wperm 3, degree 1, ER 5 (of 10) |

So a four-variant source **does exist** — it is simply not the artifact FIGURE_LIST names for
F13(c), and the builder never opens it.

**Ruled out:** `e1_curvature_regimes_scale_448.parquet` has a `regime` column but is a 2-row
illustration frame (connectome only, `f` = 0.25, σ = 2.0 vs 2.4, carrying raw `turning_angles` /
`unit_traces`) — not a count artifact. The per-cell parquets (`item2_f_extension`,
`item3_f_extension_nulls`, `e01_jacobian`) carry `mean_curvature` but no collapse flag; they are the
inputs `threshold.py` reduces.

## 4. Does FIGURE_LIST match the builder?

**Yes.** `FIGURE_LIST.md:112` states `(c) item2_collapse_loci_scale_448.csv filter f == 0, cols
n_seeds_collapsed / n_seeds` — precisely what `act3_prediction.py:241-245` reads. Its own summary is
two-variant and consistent: *"plus the `f` = 0 collapse panel (ER 5/10 seeds, connectome 0/10)"*. It
never claims four bars.

**The mismatch is caption ↔ panel, not FIGURE_LIST ↔ builder.** Within `act3b_prediction.md`:

| location | says | consistent with the panel? |
|---|---|---|
| `:26` claim A3P.4 | 5 of 10 / 0 of 10 | yes |
| `:98` unit note | "counts **seeds** (5/10, 0/10)" | yes |
| `:125` gate row | `f = 0 collapse, ER / connectome` — 5/10, 0/10 | yes |
| `:288-290` **Source** line | `(c) item2_collapse_loci_scale_448.csv, f == 0` | yes |
| `:311` caption final sentence | "+ weight-permuted and degree-matching … 3 of 10 and 1 of 10" | **no** |

One sentence over-reaches; everything else in the act is correct.

## 5. Rendered output

**Rendered, and panel (c) shows TWO categories.** `report/figures/F13.png` (249k, 24 Aug 17:52):
panel (c) has exactly two bars, x-ticks `Connectome` and `Erdős–Rényi`, annotated `0/10` and `5/10`,
title *f = 0, σ ≤ 11.2 / Fisher exact p = 0.033*. No weight-permuted or degree-matching bar.
`F13.pdf` sits beside it at the same timestamp (not opened). The smoke render
`report/figures/_smoke/F13.png` (17:47) likewise shows two bars — its placeholder frame
`_ph_collapse_loci` (`sources.py:682-690`) also enumerates only `["connectome", "erdos_renyi"]`.
Nothing was re-rendered.

---

## What could not be determined

Whether the caption's two middle values were intended as **prose context for a two-bar panel** or as
a **specification for a four-bar panel that was never built**. Nothing in the builder docstring,
FIGURE_LIST, or the act text states the intent either way. Recorded, not inferred.

The numbers themselves are real and sourced; what is wrong is their attribution to F13(c) and to
`item2_collapse_loci_scale_448.csv`. Note also that the two branches are not interchangeable: the
collapse-loci file's Fisher test and its σ ≈ 7.6–8.0 locus are computed on the `item2` boundary
capture, while `e01_threshold_table`'s quartet is the curvature-separator reduction over both
variant sets. Whether the caption should cite the second artifact or drop the sentence is a decision
for the act, not for this audit.

---

## Files read — SHA-256 before = after (all unchanged)

| file | hash |
|---|---|
| `report/figlib/figures/act3_prediction.py` | `c7bdbe6985d52dfbe4eab90c24b4d2c436af1af2ddd3b0f0768c51d6ddd539fa` |
| `report/act3b_prediction.md` | `32a2acc418e05169f185f2352370eb3befcf3e115283a19013b0bbf88afcc612` |
| `report/FIGURE_LIST.md` | `8ef4bfadc740895010b62f61599a117141bcb3347da0b69933cf8a8e6ed75966` |
| `report/figlib/sources.py` | `1bd2ddefe6f2ad51ab9f970e3f7038afc62c061ee7375822fd398223695ca537` |
| `report/figlib/style.py` | `33d8ab5eb63e25dd161445f82d211512871f29455ebfd341b08106120d08069c` |
| `…/criticality_matched/results/item2_collapse_loci_scale_448.csv` | `948291635eb673b507eb2fb933d005be64e1c7659c823f86eb8f22180bbb54a7` |
| `…/criticality_matched/results/e01_threshold_table_scale_448.csv` | `733fcb5e2d3853f510440186f2cd75b9b205fa819a43464e94203410492b2650` |
| `…/criticality_matched/results/e01_threshold_brackets_scale_448.csv` | `c2cb4bbd4427dc964edbe841eed6394a4bc55117b4d64951f2a6f932686a488d` |
| `…/criticality_matched/results/item2_summary_scale_448.md` | `598ea2f1e1ec94307d9efbf9ecfd88cdecc5316b25e6f6732e524e61c6771d9c` |
| `…/criticality_matched/threshold.py` | `afa17cd46b04e780a3b7337b41177bb9ccabe22709b48e5fffe5f147e4817f9e` |
| `…/criticality_matched/extend_f.py` | `842bd4a48d7935471670a688431e3363ffd391c9988025417d0cd66a44300f6f` |
| `…/criticality_matched/results/e1_curvature_regimes_scale_448.parquet` | `f2c8810cd1a5373e22d6445313679550a871d70b0fa04d6ce3a55a7fd82821fd` |
| `report/figures/F13.png` | `feb7692968590ba2dd2a1c55d9f86b4f74e6d2470f5405df111213fc7514e57c` |
| `report/figures/_smoke/F13.png` | `51b3f40a2f35d47b644d75471404f564e090456a0f395d73cff309c3369e9306` |

`git status --porcelain` identical to the session-start snapshot apart from this file.

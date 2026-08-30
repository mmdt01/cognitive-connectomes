# Zero-VPT cells and curvature-branch seeds — read-only audit

**Date:** 2026-08-30
**Scope:** `f == 0` (all-positive substrate), Lorenz task, N = 448, 29-point nominal-sigma
sweep (0 → 11.2, step 0.4), 10 seeds per grid point.
**Mode:** read-only. No file in the repository was created, edited, overwritten or deleted;
no experiment, sweep, evaluator, builder or verdict command was run; nothing under
`experiments/human/analysis/manifold/` was imported or called. All reads were direct
`pandas.read_parquet` / `read_csv`. This document is written to the session scratchpad,
outside the repository.

Throughout, `criticality_matched/` = `experiments/human/analysis/criticality_matched/`.

---

## 0. File integrity

SHA-256 taken before any analysis and again after all analysis. **All identical.**

| file | sha256 |
|---|---|
| `criticality_matched/results/e01_jacobian_scale_448.parquet` | `ed356d46d3ccce2cc1803193b18e5dfd99561e3c951c2649532022ceb779da90` |
| `criticality_matched/results/e03_frontier_scale_448.parquet` | `d933158a34c34cbcd47226585ccae6a0559deea3c21f805a6c1b006632e4645e` |
| `criticality_matched/results/item2_collapse_loci_scale_448.csv` | `948291635eb673b507eb2fb933d005be64e1c7659c823f86eb8f22180bbb54a7` |
| `report/proposals/f_decay_dissociation_values.csv` | `f32b46768a15f617490184278f69fd31a8b2a442d0891361bdabdfd8dff3ab92` |
| `criticality_matched/frontier.py` (read for the floor definition) | `fc08392ea09597e086ffb5b089311b7247c37d6e4cc209312f0820770897147c` |
| `report/proposals/f_decay_dissociation.py` (read for the zero test) | `46218b79164cbe69c40fe9cf265633bf6cfd7676c40c79deba1b5da8b1727eaf` |

**ASSERT: all files unchanged.** `git status --porcelain` also matches the session-start
snapshot exactly (one modified tex file and five untracked paths, none of them touched here).

---

## 1. Reproduction gate — PASSED (20 / 20)

From `e01_jacobian_scale_448.parquet` at `f == 0`, seed medians per
(`variant`, `spectral_radius`), rounded to two decimal places:

| variant | quantity | σ=2 | σ=4 | σ=6 | σ=8 | σ=11.2 |
|---|---|---|---|---|---|---|
| connectome | curvature | 0.26 | 0.26 | 0.26 | 0.26 | 0.26 |
| connectome | VPT | 4.43 | 2.81 | 0.81 | 1.18 | 0.44 |
| Erdős–Rényi | curvature | 0.26 | 0.26 | 0.26 | 0.27 | 1.70 |
| Erdős–Rényi | VPT | 3.73 | 2.45 | 1.18 | 0.49 | 0.23 |

All twenty values reproduce exactly at the precision printed in TIER0 §3.11.

The gate is insensitive to how the draws are collapsed. The parquet carries three draws per
seed; at `f == 0` no edges are flipped and the three draws are bit-identical (max distinct
values per (variant, σ, seed) = 1). Median-over-raw-rows and median-of-per-seed-medians give
the same twenty numbers.

**Unit of analysis used everywhere below:** one row per (`variant`, `spectral_radius`, `seed`)
at `f == 0` after collapsing the identical draws → **1160 seed-cells** = 4 variants × 29 σ × 10 seeds.

---

## 2. QUESTION A — the zero-VPT cells

### A1. The 84 / 53 / 24 / 7 / 0 breakdown — confirmed

**Column:** `vpt`.
**Test:** exact equality, `vpt == 0.0`. No tolerance. This is the same test the proposal
figure uses (`report/proposals/f_decay_dissociation.py`, the `zeros = sub[sub[VPT_COL] == 0.0]`
line in `build`, and the `values["vpt"] == 0.0` line in `main`).

| variant | zeros |
|---|---|
| connectome | **53** |
| connectome_weight_permuted | **24** |
| erdos_renyi | **7** |
| degree_rewire | **0** |
| **total** | **84 / 1160** |

Confirmed exactly.

The count is not an artefact of the choice of test. The zeros are exact floating-point zeros,
and the smallest strictly-positive VPT anywhere in the f = 0 grid is 0.0013584, so:

| threshold | cells |
|---|---|
| `vpt == 0` | 84 |
| `vpt ≤ 1e-12` | 84 |
| `vpt ≤ 1e-9` | 84 |
| `vpt ≤ 1e-6` | 84 |
| `vpt ≤ 1e-3` | 84 |
| `vpt ≤ 1e-2` | 98 |

The count is stable across six orders of magnitude of tolerance before it moves.

**Cross-check.** `report/proposals/f_decay_dissociation_values.csv` holds the same 1160 rows
with the same 84 zeros in the same 53 / 24 / 7 / 0 split, and agrees with the parquet to
9e-16 on both `vpt` and curvature. The CSV is a faithful copy of the parquet at f = 0.

### A2. Where the zeros occur along the sweep

| variant | n | σ values (count per σ) |
|---|---|---|
| connectome | 53 | 3.6:1, 4.0:1, 4.4:1, 4.8:1, 5.6:3, 6.0:5, 6.4:3, 6.8:3, 7.2:3, 7.6:3, 8.0:3, 8.4:3, 8.8:3, 9.2:3, 9.6:3, 10.0:4, 10.4:4, 10.8:3, 11.2:3 |
| connectome_weight_permuted | 24 | 4.8:1, 7.2:1, 7.6:1, 8.0:2, 8.4:2, 8.8:2, 9.2:2, 9.6:2, 10.0:2, 10.4:3, 10.8:3, 11.2:3 |
| erdos_renyi | 7 | 5.6:1, 6.0:1, 6.4:1, 6.8:2, 7.2:1, 8.4:1 |
| degree_rewire | 0 | — |

**Concentrated at the high-σ end, for all three variants that have any.** No zero of any
variant occurs below σ = 3.6, so the entire lower third of the sweep is zero-free.

- The connectome's zeros occupy 19 of the 29 σ points and run continuously from σ = 5.6 to
  the top of the sweep (with four isolated earlier points at 3.6, 4.0, 4.4, 4.8).
- The weight-permuted zeros occupy 12 σ points and run continuously from σ = 7.2 to the top
  (with one isolated earlier point at 4.8).
- Erdős–Rényi is the exception to the "continues to the top" pattern: its 7 zeros form a
  **band** at σ ∈ [5.6, 8.4] and there are none at σ > 8.4.

### A3. Per-cell zero / non-zero split, with the median of the surviving seeds

> **NEW VALUE** — every `connectome_weight_permuted` and `degree_rewire` number in this
> section is new. TIER0 §3.11 publishes only connectome and Erdős–Rényi.

| variant | σ | n zero | n non-zero | median of non-zero | min–max non-zero |
|---|---|---|---|---|---|
| connectome | 3.6 | 1 | 9 | 2.8065 | 0.3274–6.4089 |
| connectome | 4.0 | 1 | 9 | 3.0741 | 0.4537–6.1264 |
| connectome | 4.4 | 1 | 9 | 2.9654 | 0.3233–5.7406 |
| connectome | 4.8 | 1 | 9 | 3.2778 | 0.7145–5.7134 |
| connectome | 5.6 | 3 | 7 | 2.3921 | 0.0557–5.2081 |
| connectome | 6.0 | 5 | 5 | 2.4166 | 1.6138–4.4365 |
| connectome | 6.4 | 3 | 7 | 1.5431 | 0.0041–2.2903 |
| connectome | 6.8 | 3 | 7 | 1.5676 | 0.3301–2.4152 |
| connectome | 7.2 | 3 | 7 | 1.5662 | 0.0014–1.9968 |
| connectome | 7.6 | 3 | 7 | 1.3693 | 0.0041–1.9575 |
| connectome | 8.0 | 3 | 7 | 1.3856 | 0.4564–1.8379 |
| connectome | 8.4 | 3 | 7 | 1.1315 | 0.3831–2.0227 |
| connectome | 8.8 | 3 | 7 | 1.2810 | 0.1888–2.1218 |
| connectome | 9.2 | 3 | 7 | 1.2755 | 0.0041–2.0743 |
| connectome | 9.6 | 3 | 7 | 0.9794 | 0.1902–1.9738 |
| connectome | 10.0 | 4 | 6 | 1.2185 | 0.3247–1.6491 |
| connectome | 10.4 | 4 | 6 | 1.0032 | 0.3192–1.6070 |
| connectome | 10.8 | 3 | 7 | 0.6547 | 0.1888–1.5065 |
| connectome | 11.2 | 3 | 7 | 0.6221 | 0.3165–1.3693 |
| weight-permuted | 4.8 | 1 | 9 | 1.9697 | 0.2309–4.8345 |
| weight-permuted | 7.2 | 1 | 9 | 0.6955 | 0.2201–4.1852 |
| weight-permuted | 7.6 | 1 | 9 | 0.6955 | 0.2201–4.1934 |
| weight-permuted | 8.0 | 2 | 8 | 1.1913 | 0.1182–3.9054 |
| weight-permuted | 8.4 | 2 | 8 | 1.2409 | 0.1155–3.6283 |
| weight-permuted | 8.8 | 2 | 8 | 1.0446 | 0.1127–2.7453 |
| weight-permuted | 9.2 | 2 | 8 | 0.9753 | 0.1114–3.1936 |
| weight-permuted | 9.6 | 2 | 8 | 0.6310 | 0.1100–1.8855 |
| weight-permuted | 10.0 | 2 | 8 | 0.6174 | 0.0014–2.1096 |
| weight-permuted | 10.4 | 3 | 7 | 0.8735 | 0.0014–1.6532 |
| weight-permuted | 10.8 | 3 | 7 | 0.8327 | 0.0014–1.4942 |
| weight-permuted | 11.2 | 3 | 7 | 0.7974 | 0.0014–1.6953 |
| erdos_renyi | 5.6 | 1 | 9 | 1.6437 | 0.3844–2.2903 |
| erdos_renyi | 6.0 | 1 | 9 | 1.3747 | 0.3192–2.3297 |
| erdos_renyi | 6.4 | 1 | 9 | 0.9359 | 0.2323–1.8732 |
| erdos_renyi | 6.8 | 2 | 8 | 0.9298 | 0.2350–1.4915 |
| erdos_renyi | 7.2 | 1 | 9 | 0.4945 | 0.0095–1.4263 |
| erdos_renyi | 8.4 | 1 | 9 | 0.4795 | 0.0869–1.1641 |

**A zero is a minority of seeds failing, never the whole cell.** The worst cell in the entire
grid is 5 of 10 (connectome at σ = 6.0); every other cell with a zero is 1–4 of 10. The
surviving seeds are not marginal survivors either — their medians run 0.6–3.3 Lyapunov times,
the same order as the published seed-medians at those σ.

**A structural fact that changes what "53" means.** The 53 connectome zeros come from only
**five distinct seeds**, and three of those account for 49 of the 53 because they stay zero
across most of the upper sweep:

| variant | seed | n zero cells | σ values |
|---|---|---|---|
| connectome | 6 | 19 | 3.6, 4.0, 4.4, 4.8, then every σ from 5.6 to 11.2 |
| connectome | 0 | 15 | every σ from 5.6 to 11.2 |
| connectome | 7 | 15 | every σ from 5.6 to 11.2 |
| connectome | 8 | 3 | 6.0, 10.0, 10.4 |
| connectome | 4 | 1 | 6.0 |
| weight-permuted | 9 | 11 | 7.2 → 11.2 (contiguous) |
| weight-permuted | 8 | 10 | 4.8, then 8.0 → 11.2 |
| weight-permuted | 7 | 3 | 10.4, 10.8, 11.2 |
| erdos_renyi | 4 | 5 | 5.6, 6.0, 6.4, 6.8, 7.2 |
| erdos_renyi | 0 | 2 | 6.8, 8.4 |

Counted in *seeds* rather than *cells*, the breakdown is **5 / 3 / 2 / 0**
(connectome / weight-permuted / Erdős–Rényi / degree-matching). The 53-vs-7 gap in cells is
therefore in large part a statement that the connectome's affected seeds remain zero over a
wider stretch of σ, not that a larger fraction of its seeds fail.

### A4. Comparison against `e03_frontier_scale_448.parquet` — the two files DISAGREE

`e03_frontier_scale_448.parquet` stores no per-seed values. It stores `frac_at_floor` per
(variant, f, σ, metric). Taking `metric == "vpt"`, `f == 0`, and `frac_at_floor × n_seeds`:

| variant | e01 (exact `vpt == 0`) | e03 (`frac_at_floor × n_seeds`) |
|---|---|---|
| connectome | 53 | **59** |
| connectome_weight_permuted | 24 | **28** |
| erdos_renyi | 7 | **16** |
| degree_rewire | 0 | **0** |
| **total** | **84** | **103** |

Both are reported. **They are not reconciled here.** Two facts can be stated without
reconciling them:

1. The underlying VPT values are the same data. e01-derived seed medians and e03's stored
   `median` column agree to 4e-16 at every one of the 116 (variant, σ) cells at f = 0.
2. The difference lies in the test, not in the data. e03's floor test is recorded in its own
   builder as `s <= floor + tol` with `tol = BOUND_TOL * max(abs(ceiling), 1.0)` and
   `BOUND_TOL = 1e-3` (`criticality_matched/frontier.py`, `frontier()`). For VPT the ceiling is
   `600 * 0.03 * 0.9056`, so the floor test is `vpt ≤ 0.0163008`, not `vpt == 0`. Applying that
   threshold to e01 reproduces 59 / 28 / 16 / 0 = 103 exactly.

The largest divergence is Erdős–Rényi (7 → 16). The nine extra cells are all at σ ≥ 7.6 —
precisely the region where e01 records no ER exact zeros at all.

Per-cell e03 floor counts at f = 0, `metric == vpt`, where non-zero:

| variant | σ | n at floor | stored median |
|---|---|---|---|
| connectome | 3.2 | 1 | 3.3403 |
| connectome | 3.6 | 1 | 2.6543 |
| connectome | 4.0 | 1 | 2.8071 |
| connectome | 4.4 | 1 | 2.7997 |
| connectome | 4.8 | 1 | 2.8635 |
| connectome | 5.2 | 1 | 2.4057 |
| connectome | 5.6 | 3 | 1.0290 |
| connectome | 6.0 | 5 | 0.8069 |
| connectome | 6.4 | 4 | 1.0494 |
| connectome | 6.8 | 3 | 1.1349 |
| connectome | 7.2 | 4 | 1.3136 |
| connectome | 7.6 | 4 | 1.3414 |
| connectome | 8.0 | 3 | 1.1845 |
| connectome | 8.4 | 3 | 0.7166 |
| connectome | 8.8 | 3 | 0.4211 |
| connectome | 9.2 | 4 | 0.3654 |
| connectome | 9.6 | 3 | 0.3423 |
| connectome | 10.0 | 4 | 0.3457 |
| connectome | 10.4 | 4 | 0.3430 |
| connectome | 10.8 | 3 | 0.3410 |
| connectome | 11.2 | 3 | 0.4428 |
| weight-permuted | 4.8 | 1 | 1.4141 |
| weight-permuted | 7.2 | 1 | 0.5923 |
| weight-permuted | 7.6 | 1 | 0.5916 |
| weight-permuted | 8.0 | 2 | 0.7709 |
| weight-permuted | 8.4 | 2 | 0.8429 |
| weight-permuted | 8.8 | 2 | 0.7206 |
| weight-permuted | 9.2 | 2 | 0.6072 |
| weight-permuted | 9.6 | 2 | 0.3219 |
| weight-permuted | 10.0 | 3 | 0.3206 |
| weight-permuted | 10.4 | 4 | 0.2744 |
| weight-permuted | 10.8 | 4 | 0.2724 |
| weight-permuted | 11.2 | 4 | 0.3416 |
| erdos_renyi | 5.6 | 1 | 1.3829 |
| erdos_renyi | 6.0 | 1 | 1.1750 |
| erdos_renyi | 6.4 | 1 | 0.8415 |
| erdos_renyi | 6.8 | 2 | 0.7023 |
| erdos_renyi | 7.2 | 2 | 0.4782 |
| erdos_renyi | 7.6 | 1 | 0.4490 |
| erdos_renyi | 8.0 | 1 | 0.4856 |
| erdos_renyi | 8.4 | 1 | 0.4136 |
| erdos_renyi | 8.8 | 1 | 0.4170 |
| erdos_renyi | 9.2 | 1 | 0.4503 |
| erdos_renyi | 10.0 | 1 | 0.2235 |
| erdos_renyi | 10.4 | 1 | 0.2262 |
| erdos_renyi | 10.8 | 1 | 0.2112 |
| erdos_renyi | 11.2 | 1 | 0.2289 |

Note that e03 places connectome floor-cells at σ = 3.2 and σ = 5.2, where e01 records no
exact zero at all.

### A5. Connectome zeros at low σ

**No connectome zero occurs at σ ≤ 2.0.** The connectome's lowest σ with any zero is **σ = 3.6**
(a single seed, seed 6).

| variant | lowest σ with a zero |
|---|---|
| connectome | 3.6 |
| connectome_weight_permuted | 4.8 |
| erdos_renyi | 5.6 |
| degree_rewire | none |

### A6. Degree-matching — confirmed

**Confirmed: `degree_rewire` has no exact zeros anywhere at `f == 0`**, across all 290 of its
seed-cells. Its minimum VPT at f = 0 is 0.0679, and that minimum sits at σ = 0.0 — the
un-driven end of the sweep, not the high-gain end. `e03_frontier_scale_448.parquet`
independently records `frac_at_floor = 0` for every `degree_rewire` (f = 0, vpt) cell, so
the two files agree on this variant under both tests.

**Scope caveat.** This is an `f == 0` statement only. Across all f, `degree_rewire` has 3658
zero-VPT rows out of 9570 — so "no zeros anywhere" holds for the all-positive substrate, not
for the sign-flip sweep.

### A7. Is a zero VPT the same event as a period-two collapse?

**Not determinable from these files.**

Neither file carries a per-run period-two flag. `e01_jacobian_scale_448.parquet` has no
collapse column — its 22 columns are run keys plus Jacobian, gain and curvature diagnostics,
`vpt` and `climate_error`. `item2_collapse_loci_scale_448.csv` records only aggregate counts
and σ-brackets. There is no key on which the two could be joined at the level of an individual
run, so the identity of the two events cannot be tested here.

One observation from within e01, stated as an observation and **not** as a mechanism: at cell
level the exact-zero VPT cells and the high-curvature (> 2 rad) cells are largely
non-coincident.

| | `vpt == 0` false | `vpt == 0` true |
|---|---|---|
| curvature ≤ 2.0 | 1003 | 70 |
| curvature > 2.0 | 73 | 14 |

Of the 84 zero cells, 70 sit on the low-curvature branch and 14 on the high-curvature branch;
all 53 connectome zeros sit on the low-curvature branch, since the connectome never reaches
the upper branch at all (§3.2). Per variant:

| variant | branch F / zero F | branch F / zero T | branch T / zero F | branch T / zero T |
|---|---|---|---|---|
| connectome | 237 | 53 | 0 | 0 |
| connectome_weight_permuted | 241 | 12 | 25 | 12 |
| degree_rewire | 281 | 0 | 9 | 0 |
| erdos_renyi | 244 | 5 | 39 | 2 |

This rules the two out of being the same cell-level event *under a curvature-branch reading*.
Curvature branch is not the collapse flag, so it does not answer the question as posed.

---

## 3. QUESTION B — are the branch seeds the collapse seeds?

### B1. The branch rule, and the distribution that justifies it

**Rule:** a seed is on the upper branch if its **maximum `mean_curvature` across the 29 σ
points at f = 0 exceeds 2.0 rad** — reaching it at *any* σ, not at a specified one.

Per-seed maximum curvature, all 40 seeds, sorted:

```
0.2583 0.2587 0.2592 0.2601 0.2601 0.2603 0.2605 0.2607 0.2611 0.2611
0.2613 0.2624 0.2626 0.2631 0.2642 0.2645 0.2653 0.2654 0.2661 0.2663
0.2665 0.2665 0.2666 0.2674 0.2675 0.2676 0.2683 0.2698 0.2704 0.2748
0.2803  |  3.0219 3.0943 3.1050 3.1115 3.1371 3.1383 3.1384 3.1398 3.1399
```

**The distribution is cleanly separated, with no seeds in between.** 31 seeds top out in
[0.258, 0.280]; 9 seeds top out in [3.022, 3.140], against π = 3.1416. The largest gap in the
sorted list is **2.7416**, between 0.2803 and 3.0219 — an order of magnitude wider than the
full spread of either group.

The threshold is therefore not a tuned choice. Any cutoff in the open interval (0.281, 3.021)
produces the same partition:

| cutoff | connectome | weight-permuted | degree_rewire | erdos_renyi |
|---|---|---|---|---|
| > 1.0 | 0 | 3 | 1 | 5 |
| > 1.5 | 0 | 3 | 1 | 5 |
| > 2.0 | 0 | 3 | 1 | 5 |
| > 2.5 | 0 | 3 | 1 | 5 |
| > 3.0 | 0 | 3 | 1 | 5 |
| > 3.10 | 0 | 2 | 0 | 5 |

Only at 3.10 does the partition begin to move, dropping weight-permuted seed 8 (max 3.022) and
degree_rewire seed 4 (max 3.094).

**At cell level** the bimodality is nearly as clean, but not perfectly so. Of 1160 cells, 1072
lie below 0.5 rad and 86 lie above 3.0 rad, leaving **two cells in between**:

| variant | σ | seed | curvature | vpt |
|---|---|---|---|---|
| connectome_weight_permuted | 3.6 | 0 | 2.9859 | 0.2988 |
| erdos_renyi | 10.0 | 5 | 1.9413 | 0.4849 |

The proposal figure's draft caption says three such cells. Under the window used here
(0.30 < c < 3.00) there are two. This is a difference in where the "in between" window is
drawn, not a disagreement about the data. Nothing was amended.

### B2. Branch seeds and their onset σ

> **NEW VALUE** — the `connectome_weight_permuted` and `degree_rewire` rows are new.
> TIER0 §3.11 publishes only connectome and Erdős–Rényi.

| variant | branch seeds | lowest σ on branch, per seed | cells on branch, of 29 |
|---|---|---|---|
| connectome | **none** | — | — |
| connectome_weight_permuted | 0, 8, 9 | seed 0: 3.6 · seed 8: 11.2 · seed 9: 5.2 | 20 · 1 · 16 |
| degree_rewire | 4 | seed 4: 8.0 | 9 |
| erdos_renyi | 0, 4, 5, 6, 8 | seed 0: 6.8 · seed 4: 7.6 · seed 5: 10.4 · seed 6: 8.8 · seed 8: 8.0 | 12 · 10 · 3 · 7 · 9 |

This confirms the panel-(a) counts: 5 Erdős–Rényi, 3 weight-permuted, 1 degree-matching,
0 connectome.

Two qualifications on membership. Weight-permuted seed 8 is on the branch for a single cell,
at the very last σ of the sweep; Erdős–Rényi seed 5 for three cells. Onset σ is not clustered
— it spans 3.6 to 11.2 across the nine branch seeds.

### B3. Collapse seed identities — NOT AVAILABLE; question stopped here

**`item2_collapse_loci_scale_448.csv` stores only counts, not seed identities.**

Its twelve columns are `f, variant, frac_collapsed, sigma_lo, sigma_hi, x_lo, x_hi,
sigma_eff_at_collapse, n_seeds_collapsed, n_seeds, delta_sigma_collapse, delta_x_collapse`.
There is no seed column and no per-seed row anywhere in the file, which holds 22 data rows in
total. As instructed, this question stops here; no identities were inferred from any other
source.

Two further facts about the file bear directly on the premise of Question B:

1. **The file contains only two variants — `connectome` and `erdos_renyi`.** There are no
   `connectome_weight_permuted` or `degree_rewire` rows at any f. The premise that the file's
   f = 0 collapse counts are "the same four numbers in the same order" cannot be checked as
   stated: only two of the four numbers exist in this file.
2. At `f == 0` the file records `n_seeds_collapsed = 0` of 10 for connectome and
   `n_seeds_collapsed = 5` of 10 for erdos_renyi. Those two do match the corresponding branch
   counts from §3.2 (connectome 0, ER 5). The 3 for weight-permuted and the 1 for
   degree-matching are **not in this file**, and were not looked for elsewhere.

For completeness, the full f = 0 content of the file:

```
f,variant,frac_collapsed,sigma_lo,sigma_hi,x_lo,x_hi,sigma_eff_at_collapse,n_seeds_collapsed,n_seeds,...
0.0,connectome,0.0,,,,,,0,10,,
0.0,erdos_renyi,0.5,7.6,8.0,4.24510451471733,4.447252348751488,0.01149355756105313,5,10,,
```

### B4. Branch × collapse contingency table — UNANSWERABLE

Seed identities exist in `e01_jacobian_scale_448.parquet` but not in
`item2_collapse_loci_scale_448.csv`. The contingency table cannot be built. Not answered.

### B5. Common seed numbering — CANNOT BE ESTABLISHED

The question does not arise in the form posed, because `item2_collapse_loci_scale_448.csv`
carries no seed identifiers at all. There is nothing to compare a numbering against, and hence
no basis on which to establish or refute that "seed 3" denotes the same network in both files.
Consistent with the instruction, **B4 is treated as unanswerable rather than answered on an
assumption.**

---

## 4. Summary of what was and was not established

**Established:**

- The reproduction gate passes 20 / 20.
- The 84 / 53 / 24 / 7 / 0 zero breakdown is correct, under exact equality on `vpt`, and is
  stable to a tolerance of 1e-3.
- Zeros are confined to the upper sweep (none below σ = 3.6) and the connectome's lowest zero
  is at σ = 3.6, with none at σ ≤ 2.0.
- No zero cell is a whole-cell failure; the worst is 5 of 10, and surviving seeds at those
  cells predict at 0.6–3.3 Lyapunov times.
- In *seeds* rather than *cells* the zero breakdown is 5 / 3 / 2 / 0.
- `degree_rewire` has no zeros at f = 0 by either file's test.
- The nine upper-branch seeds are cleanly separated from the other 31 by a gap of 2.74 rad,
  and are 0 / 3 / 1 / 5 by variant.

**Not established, and why:**

- Whether a zero VPT is the same event as a period-two collapse. Neither file carries a
  per-run collapse flag (A7).
- Whether the branch seeds are the collapse seeds.
  `item2_collapse_loci_scale_448.csv` stores counts only, and covers only two of the four
  variants (B3–B5).

**One discrepancy surfaced and left unreconciled:** e01 and e03 give different zero counts
(84 vs 103) because they apply different tests to the same values (A4).

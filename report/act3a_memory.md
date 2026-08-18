# Act III (memory arm) — geometry sets memory capacity

**Session 3 of the §4b sweep.** Read `report/CONVENTIONS.md` first. Canonical results
live in `TIER0_STATE_OF_PLAY.md`; canonical claims in `ACTION_PLAN_JOURNAL_ROADMAP.md` §1.

**This act carries the most withdrawn material of any, and three phrases must never come
back.** Stated here because this is the chapter where each would return:

| withdrawn | what replaced it |
|---|---|
| "the connectome is **subcritically worse than ER**" | **parity below criticality, advantage above — and name the axis.** The deficit is −217.4 at matched *spectral radius* and −24.0 at matched *bulk radius*. Neither axis is neutral: `σ·W/\|λ₁\|` has spectral radius exactly σ, so nominal matching pins the Perron root and `σ·bulk95` matching pins the bulk, and the mechanism under test *is* the Perron mode. "89% an artifact of nominal-σ matching" is also ruled out (`TIER0` §1.1) |
| "**hub inhibition collapses memory**" | **hub-targeted inhibition closes the advantage fastest; nothing collapses, the null moves.** Inhibiting the connectome's hubs *raises* its own memory more than any other placement (11.43 → 14.88 at `f` = 0.1 against periphery-first's 12.94). The advantage narrows because ER gains +8.5 against the connectome's +3.4. The `f*` ordering (hub 0.087 < stratified 0.124 < periphery 0.164) is real; the word "collapse" is not. And it is not a separate result: hub-first is the most efficient way to destroy the Perron common mode, so it is the placement-resolved face of §3.7's rescue account (`TIER0` §3.8) |
| the crossing, quoted bare | **always with its axis.** (`σ·bulk95` = 2.938, `f` = 0.153) is the **first crossing inside full replicate coverage**; five more sit past the coverage edge (minimum `x_hi` = 3.58) where the boundary rests on a `bulk95`-selected subsample and must not be read. On the nominal axis there is **no** crossing once the sweep passes σ = 6. So a bare coordinate states as a property of the system what is a joint property of the system *and* the matching choice — and the matched-bulk axis is the one that hands the connectome a 1.7× larger Perron root, which is the very quantity under test |

The third is F16's and Session 4 renders it. It is restated here because this chapter is
where contribution 3 is argued and where a reader meets the boundary language first.

---

## 1. Claims register

Every claim this chapter makes, each with a figure and a source. The chapter is written to
this register, not the other way round.

| # | claim (one sentence, as it will appear) | figure | TIER0 § | artifact |
|---|---|---|---|---|
| A3M.1 | **The memory result is a crossing, not a peak**: matched on effective criticality the connectome peaks **lowest** (`d_eff` 432.4, 96.5% of the `d_eff = N` ceiling) yet at the top of the four-variant overlap still holds **47%** of its own peak against the nulls' 28 / 22 / 11%. | F7 | §1.2 | `taskB_extended_sweep_scale_448.parquet` |
| A3M.2 | **Peak capacity is unresolvable at N = 448 and must not be claimed either way**: every variant peaks within 3.5% of the ceiling, so the resolvable quantity is the decay rate. A ceiling can clip curves but cannot manufacture a crossing. | F7b, F7c | §1.2 | same |
| A3M.3 | **At its own peak the connectome is at parity, not "always worst"**: the paired per-seed deficit is **2 to 6%**, with a 95% CI excluding zero at 5 of 5 α against Erdős–Rényi and the weight-permuted control but at **1 of 5** against degree-matching. | F10 | §3.4 | `closeout_peak_parity.csv` |
| A3M.4 | **The supercritical margin is not an N = 448 accident**: connectome/ER supercritical MC is **4.40 → 4.42** across a 2.2× change in N with the threshold at the connectome's `sr_crit` for every variant, and **3.56 → 3.85** with each variant's own. The claim survives both filters; "scale-invariant" full stop is true of one filter only. | F9 | §2.4 | `n1000_memory_scale_{448,1000}.parquet` |
| A3M.5 | **The advantage is a rescue from Perron domination, not a capacity gain**: the connectome is the **least** common-mode dominated substrate despite carrying much the largest Perron root (`\|x̄\|` 0.759 against 0.949 to 0.989 at σ = 6, `f` = 0), because a large spectral gap lets the leading mode be driven hard without the bulk following. | F11a | §3.7, §3.12 | `item2_f_extension` + `item3_f_extension_nulls` |
| A3M.6 | **`bulk95` is a partial controller whose power depends on whether a Perron mode exists**: matching on `σ·bulk95` absorbs only **26%** of the connectome−ER MC gap at `f` = 0 (6.42 → 4.75) and leaves ~0.5 by `f` ≥ 0.2, a 9.5× collapse in what it fails to explain. | F11b | §3.7, §1.4 | `e03_mechanism_matched_scale_448.csv` |
| A3M.7 | **The ridge α constraint does not bind**, so α is chosen on other grounds: `d_eff`↔MC correspondence is **+0.999 at every α** from 1e-8 to 1e-3 and the supercritical ladder orders at **+1.00** at every α — provided α is raised in *both* places. | prose (F10's α axis carries it) | §3.3 | `taskB_mc_alpha_correspondence.csv` |
| A3M.8 | **Aceituno, Yan & Liu are reconciled rather than contradicted**: their spread-beats-compact ordering reproduces exactly on our substrates at α = 1e-8 (peak MC ER > degree > weight-permuted > connectome). Spread wins at the peak, a large gap wins across the range. | prose + F7 | §1.2, roadmap contr. 3 | `taskB_mc_alpha_peaks.csv` |

**Claims deliberately NOT made here** (and why):

- **"The connectome is a better reservoir."** It is not, at the peak, and A3M.3 is the
  data saying so. `CONVENTIONS` forbids the phrase outright.
- **"The connectome is subcritically worse than ER."** Withdrawn; see the table above.
  The chapter states both axes and rests on surviving both.
- **"Hub inhibition collapses memory."** Withdrawn; nothing collapses. The placement
  result appears only as a consequence of A3M.5, per `TIER0` §3.8.
- **Any peak-capacity claim in either direction.** A3M.2 is the claim: at N = 448 the
  peak is not resolvable. The one thing that *is* said about the peak is A3M.3's parity,
  which is a statement with a CI attached.
- **"The supercritical memory margin is scale-invariant"**, full stop. True on one
  filter (4.40 → 4.42, +0.5%) and false on the other (3.56 → 3.85, +8%). F9 draws both.
- **That `bulk95` is *the* ladder controller.** The N = 1000 falsification test came back
  **inconclusive**, and inconclusive because the *predictor's* own degree/ER ordering at
  N = 1000 is not significant (+0.0142 [−0.0191, +0.0475], p = 0.16), not because the
  outcome was noisy. A3M.6 is the narrower thing the controlled comparison does support.
- **The correlation half of the §3.7 mechanism test.** `|mean_state|` and `σ·bulk95` are
  collinear by construction, the within-`f` Spearmans against `dMC` are near-identical
  (0.959 against 0.956 at `f` = 0.15), and `TIER0` §3.7 says the pooled supercritical
  contrast (+0.796 against −0.004) **must not be quoted**. F11 plots the matched-axis
  residual only.
- **Any statement about `f` > 0 memory without its σ.** The memory advantage is
  supercritical and maximal at `f` = 0; the generative advantage is near-critical and
  absent at `f` = 0. Written without the σ the two read as a contradiction
  (`TIER0` §2.6).
- **A curvature or trajectory-geometry account of memory.** That axis is Act III's
  *prediction* arm and does not move at `f` = 0 anyway (Act II item 15).
- **That negative weights trade memory away.** In absolute terms **no substrate
  degrades**: supercritical MC rises with `f` for all four, the connectome by +2.75 and
  ER by +10.69. The wedge closes because the nulls gain about four times as much from a
  much lower start (`TIER0` §1.1b, §2.6). This is the same "the null moved" failure the
  chapter is built to avoid, and the chapter says so in its own voice.

---

## 2. Reproduction gate

Run before any figure work. A failed reproduction is the finding and stops the act.

**Verdict: PASSED.** Every quantity the act rests on returns from the frozen artifacts at
the precision `TIER0` publishes it to. Two of them required their aggregation to be
recovered first, and in one case that recovery **found a defect in the session-0 F7
builder** (§2.2, audit item 1). Recomputed with `report/CONVENTIONS.md`'s conventions
from `e02_panel.parquet`, `e02_axis_summary.csv`,
`taskB_extended_sweep_scale_448.parquet`, `n1000_memory_scale_{448,1000}.parquet` and
`closeout_peak_parity.csv`.

### 2.1 The matched-axis peak `dD` and its location (`TIER0` §2.2)

| quantity | `TIER0` | recomputed (panel) | recomputed (summary) | agrees to |
|---|---|---|---|---|
| nominal peak `dD` | +343.3 at σ = 4.47 | +343.2762 at 4.4667 | +343.2762 at 4.4667 | all published digits |
| nominal most-negative `dD` | −217.4 | −217.4405 | −217.4405 | all published digits |
| **matched peak `dD`** | **+196.5 at `σ·bulk95` = 1.949** | **+196.5335 at 1.9494** | +196.5335 at 1.9494 | all published digits |
| matched most-negative `dD` | −24.0 | −24.0495 | −24.0495 | all published digits |
| retained at the true peak | 57% | 0.5725 | — | 1 s.f. as published |
| deficit removed on the matched axis | 89% | 0.8894 | — | 1 s.f. as published |
| matched peak is interior; `dD` at the overlap top | +155.5 | +155.4717 | +155.4717 | all published digits |

The overlap top is 2.5992 and the peak sits at 1.9494, so the matched peak is a
**measurement, not a bound** — which is what Task B was run to establish.

### 2.2 The crossing table (`TIER0` §1.2) — and the aggregation it depends on

| variant | peak `d_eff` | recomputed | at `σ·bulk95` | recomputed | at overlap top | recomputed | retained | recomputed |
|---|---|---|---|---|---|---|---|---|
| Connectome | **432.4** | **432.354** | 1.04 | 1.0397 | **204.9** | **204.930** | **47%** | 47.40% |
| Weight-permuted | 445.7 | 445.731 | 0.93 | 0.9314 | 126.8 | 126.787 | 28% | 28.44% |
| Degree-matching | 444.7 | 444.722 | 0.91 | 0.9097 | 96.4 | 96.399 | 22% | 21.68% |
| Erdős–Rényi | 446.6 | 446.624 | 0.97 | 0.9747 | 49.5 | 49.458 | 11% | 11.07% |

**All sixteen numbers return to every published digit — but only under one aggregation,
and `TIER0` does not state which.** `bulk95` is a single constant for the connectome
(one fixed graph) and a **per-seed** extreme-value statistic for the three resampling
nulls, spreading 0.41 to 0.61 across ten degree-rewire seeds. On the matched axis
`x = σ · bulk95` each seed therefore sits on its own grid, and E0.2 aggregates **per seed
then across seeds** throughout — interpolate each seed's curve onto the common grid
(clipped to the interval every (variant, seed) covers, which is what puts the top of the
overlap at 2.5992), then take the median. `E02_verdict` §4.4 states the rule and the
reason; `TIER0` §1.2 publishes the result without naming it.

The alternative — median `d_eff` at fixed nominal σ, with `σ · median(bulk95)` as the x
coordinate — is a different statistic, and it is what the session-0 F7 builder computed.
Measured side by side:

| variant | peak (per-seed) | peak (median-of-curves) | at x (per-seed) | at x (median-of-curves) | retained |
|---|---|---|---|---|---|
| Connectome | 432.4 | 432.4 | 1.040 | 1.040 | 47% / 47% |
| Weight-permuted | 445.7 | 445.4 | 0.931 | 1.041 | 28% / 29% |
| Degree-matching | 444.7 | 446.0 | 0.910 | 0.854 | 22% / 21% |
| Erdős–Rényi | 446.6 | 446.1 | 0.975 | 1.107 | 11% / 12% |

**The connectome row is identical under both**, because its `bulk95` is a constant — so
the row a reader checks first is the one row that cannot reveal the problem. That is the
third time this shape has appeared (Act I item 13, Act II item 1). Fixed; see §3's F7
block and audit item 1.

### 2.3 The N = 448 → N = 1000 margin (`TIER0` §2.4)

Threshold = **the connectome's** `sr_crit` (3.078 / 3.985), applied to every variant.
130 cells per variant at N = 448, 210 at N = 1000.

| supercritical MC | `TIER0` N=448 | recomputed | `TIER0` N=1000 | recomputed |
|---|---|---|---|---|
| connectome | 12.32 | 12.3232 | 13.93 | 13.9294 |
| weight-permuted | 7.34 | 7.3449 | 8.98 | 8.9837 |
| degree | 4.61 | 4.6138 | 5.09 | 5.0942 |
| Erdős–Rényi | 2.80 | 2.8031 | 3.15 | 3.1543 |
| **margin conn/ER** | **4.40** | **4.3963** | **4.42** | **4.4160** |

Threshold = **each variant's own** `sr_crit`:

| supercritical MC | `TIER0` N=448 | recomputed | `TIER0` N=1000 | recomputed |
|---|---|---|---|---|
| weight-permuted | 8.81 | 8.8093 | 9.66 | 9.6628 |
| degree | 5.43 | 5.4320 | 5.73 | 5.7277 |
| Erdős–Rényi | 3.46 | 3.4626 | 3.62 | 3.6183 |
| **margin conn/ER** | **3.56** | **3.5590** | **3.85** | **3.8497** |

Both margins agree to the two decimals published (4.3963 → 4.40, 4.4160 → 4.42). The
change on the primary filter is **+0.45%**.

Secondary quantities, same section: the matched `dD` peak stays **interior** at both
scales — +199.3 at `x` = 1.949 with the overlap reaching 2.599 (N = 448) and **+612.8 at
`x` = 1.979** with the overlap reaching 2.610 (N = 1000), declining to +459.6 at the
edge; normalised, `dD/N` **0.445 → 0.613**. All as published. The falsification contrast
also returns exactly: ER − degree = **−1.804 [−2.125, −1.484]** at N = 448 and **−1.902
[−2.187, −1.617]** at N = 1000, Wilcoxon p = 0.002 at both.

### 2.4 Peak `d_eff / N` at both scales — **two different aggregations, published side by side**

| variant | `TIER0` §1.2, N=448 | recomputed | `TIER0` §2.4, N=1000 | recomputed |
|---|---|---|---|---|
| connectome | 0.965 | 0.9651 | **0.971** | 0.9710 |
| weight-permuted | 0.995 | 0.9949 | 0.994 | 0.9939 |
| degree | 0.993 | 0.9927 | 0.984 | 0.9840 |
| Erdős–Rényi | 0.997 | 0.9969 | 0.999 | 0.9992 |

Both columns reproduce exactly — **under different rules, and they are not
interchangeable.** §1.2's N = 448 column is the per-seed-then-median matched-axis curve
of §2.2, its peaks divided by N, on Task B at the frozen α = 1e-6. §2.4's N = 1000 column
is the **maximum over all cells** of `d_eff_norm` on the N = 1000 parquet at the
reparameterised α — the most permissive of the three aggregations tried; medianing over
seeds at each σ and then taking the maximum gives 0.956 / 0.980 / 0.979 / 0.999 on that
same file. The conclusion — the ceiling is not escaped at either scale — holds under
every rule, so nothing in this act rests on the choice. What does not survive is reading
the two columns as a series: see audit item 3.

The two N = 448 columns available also differ, for a real reason: `taskB` runs at the
frozen absolute α = 1e-6 (peak `d_eff/N` = 0.9651 for the connectome) and the N = 1000
control at the reparameterised α (0.9757 under the same rule), because the new rule's
realised α at N = 448 is below 1e-6 over much of the sweep. §1.2 quotes the Task B
number; F7 draws Task B.

### 2.5 Paired per-seed peak differences with CIs across the α grid (`TIER0` §3.4)

Frozen `closeout_peak_parity.csv`, connectome − Erdős–Rényi:

| α | `TIER0` diff | recomputed | `TIER0` CI | recomputed CI | `TIER0` % | recomputed | `TIER0` p | recomputed |
|---|---|---|---|---|---|---|---|---|
| 1e-8 | −0.561 | −0.5611 | [−0.617, −0.506] | [−0.6165, −0.5058] | −3.6 | −3.61 | 0.002 | 0.0020 |
| 1e-6 | −0.359 | −0.3592 | [−0.560, −0.159] | [−0.5598, −0.1586] | −2.4 | −2.41 | 0.006 | 0.0059 |
| 1e-5 | −0.487 | −0.4869 | [−0.742, −0.232] | [−0.7420, −0.2318] | −3.3 | −3.33 | 0.006 | 0.0059 |
| 7e-5 | −0.665 | −0.6646 | [−0.945, −0.385] | [−0.9447, −0.3845] | −4.7 | −4.70 | 0.006 | 0.0059 |
| 1e-3 | −0.756 | −0.7555 | [−1.277, −0.234] | [−1.2774, −0.2336] | −5.9 | −5.91 | 0.020 | 0.0195 |

CI excludes zero: **5/5** against Erdős–Rényi, **5/5** against the weight-permuted
control, **1/5** against degree-matching. Effect **2.4 to 5.9%** — "2 to 6%" as
published.

**Recomputed independently rather than read off the CSV.** All 15 rows were rebuilt from
`taskB`'s own per-seed α columns (per-seed peak over σ, paired within seed on the same
`Win` and input series, 95% t-CI, Wilcoxon), and every one agrees with the frozen file to
better than 5e-3 on the mean difference and on both CI ends.

**Precisions logged.** Peak `dD` and its location, the crossing table, both margins,
peak `d_eff/N` and all 15 parity rows: agreement at **every digit `TIER0` publishes**.
The two margins round rather than match exactly (4.3963 → 4.40, 4.4160 → 4.42), which is
the published precision. Nothing in the act required a number to be softened.

### 2.6 Code audit

**Functions audited:** the MC evaluator (`src/tasks/memory_capacity.evaluate` /
`_measure`), the ridge reparameterisation
(`criticality_matched/n1000.py:cell`, `RIDGE_LAMBDA`, `T_BY_SCALE`, `sr_grid`,
`control_gate`), the design matrix and Gram (`manifold/spectra.design_matrix`,
`src/analysis/manifold.gram_spectrum`), and `d_eff`
(`src/analysis/manifold.ridge_effective_rank`) at both scales.

**Findings:**

1. **α is identical in `d_eff` and MC at every cell, and it is the same float — not two
   copies of one number.** `n1000.cell` computes
   `alpha = RIDGE_LAMBDA * trace(G) / n_nodes` from the pass-1 Gram and then passes *that
   variable* both to `manifold.ridge_effective_rank(eig_gram, alpha)` and to
   `spec["evaluate"](..., ridge_alpha=alpha)`. There is no second derivation to drift.
   Checked over all **2,040 cells** at both scales:
   `max |alpha − ridge_lambda·trace_gram/n_nodes| / alpha = 0.0` exactly, with a single
   `ridge_lambda` = 4.4845e-10 at both scales. This is `CONVENTIONS`' requirement met by
   construction, the same way Act II found it met for `probe3`.
2. **The pin holds where it was set.** The supercritical median realised α at N = 448,
   T = 3000 is **1.0000e-06** — exactly the frozen absolute value λ was pinned to
   reproduce. At N = 1000 it is 2.139e-06, and `T_eff/N` is 5.5804 against 5.5000, both
   as `TIER0` §2.4/§2.5 describe.
3. **The two evaluator passes see one and the same trajectory, so `d_eff` and MC are not
   merely at the same α but on the same states.** The MC evaluator resets the reservoir
   and redraws its input from `default_rng(seed)`, so pass 2 reproduces pass 1's states.
   Verified rather than assumed: on four rebuilt cells the pass-1 and pass-2 state
   matrices are **bit-identical** (`np.array_equal`). This matters because
   `alpha` is derived from pass 1's Gram and applied to pass 2's solve; had the reset not
   fired, the ridge would have been chosen on a different trajectory from the one scored.
4. **Four N = 448 cells rebuilt from scratch reproduce the frozen parquet.** Fresh
   substrate build → reservoir → two passes, against `n1000_memory_scale_448.parquet`:

   | cell | α (rel. error) | `d_eff` | frozen | MC | frozen |
   |---|---|---|---|---|---|
   | connectome s0 σ=4.0 | 1.8e-15 | 416.3571 | 416.3571 | 13.5545 | 13.5545 |
   | connectome s3 σ=6.0 | 9.5e-16 | 406.7806 | 406.7805 | 13.4261 | 13.4261 |
   | erdos_renyi s0 σ=4.0 | 2.4e-15 | 123.3159 | 123.3160 | 6.3355 | 6.3355 |
   | degree_rewire s1 σ=5.2 | 2.0e-16 | 79.8875 | 79.8876 | 4.8317 | 4.8317 |

5. **The N = 448 control under the new T/α reproduces the old result, so the N = 1000
   numbers may be read as N.** Re-run of `control_gate` logic on all 840 shared cells
   (Task B's grid is reused exactly at N = 448, so the merge is complete):
   supercritical median relative change **0.32% on MC and 0.70% on `d_eff`**, maxima 1.44%
   and 2.45% — `TIER0` §2.4 and `N1000_verdict` §4.0 to the digit. The supercritical
   margin moves **4.3513 → 4.3963**, published as 4.35 → 4.40. The same numbers hold at
   σ ≥ 3.078 as at σ ≥ 3.05, because the σ grid steps 0.4 and both thresholds select
   σ ≥ 3.2.
6. **`d_eff` at the five α is recoverable from the stored Gram spectrum, so the α axis is
   not a separate computation.** Recomputing `ridge_effective_rank` from `taskB`'s stored
   `eig_gram` at each α reproduces the stored `d_eff_alpha_*` columns to
   **≤ 1.9e-07** (the `float32` storage of the spectrum), and `mc` equals
   `mc_alpha_1e-06` **bit-for-bit** — confirming the base columns are the frozen 1e-6
   pair rather than an independent solve.
7. **`TIER0` §3.3's "+0.999 at every α" is a seed-median statistic (n = 52), not a
   cell-level one — and the document does not say so.** Reproduced exactly:
   +0.99915 / +0.99915 / +0.99898 / +0.99906 / +0.99898, matching
   `taskB_mc_alpha_correspondence.csv` to ten decimals, with n = 52 = 4 variants × 13
   supercritical σ. Pooled over the 520 individual cells the same statistic is +0.9973 to
   +0.9984, i.e. **+0.998**, which is what a later reader recomputing it will get. Both
   support the claim; only one is the published digit. Act II hit the identical
   two-aggregation trap on contribution 6. See audit item 4.
8. **The MC design is per-lag and nested; the reported `d_eff` is at `k` = 0.** The
   solver forms `X_k = states[k:]` for `k` = 1..50 while `gram_spectrum` is taken on the
   full post-warmup matrix. Act II quantified the offset on real cells at **0.31 to 0.82
   `d_eff` units** against a rigorous Weyl bound of 50, and nothing in this act's
   arithmetic changes it. Carried forward rather than re-measured (`CONVENTIONS` working
   rule 7: the audit budget does not scale).
9. **`ridge_effective_rank` ridges the unregularised bias direction — and MC has no bias
   column**, so every `d_eff` in this act is untouched by Act II's item 9. `design_matrix`
   returns the raw states for `mc` and appends a bias only for NARMA/MG/Lorenz.

---

## 3. Figures

One block per figure ID from `FIGURE_LIST.md`. **Caption written before the figure.**

### F7 — the crossing: peaks lowest, retains most

- **Claim carried:** A3M.1, A3M.2 — **the lead figure of chapter 6 and a workshop
  figure.**
- **Source:** source `taskb` = `criticality_matched/results/taskB_extended_sweep_scale_448.parquet`,
  no row filter (f = 0, MC, 4 variants, σ 0 to 8 step 0.4, 10 seeds).
  `x = spectral_radius * bulk95` from the file's own column, **per seed**; each seed's
  curve is interpolated onto a common grid over the interval every (variant, seed)
  covers, and the median is taken across seeds.
- **Panels:** (a) `d_eff` against `σ·bulk95`, four variants, peaks marked, `d_eff = N`
  ceiling drawn, top-of-overlap rule at 2.599; (b) peak `d_eff / N` per variant against
  the ceiling; (c) percentage of own peak retained at the top of the overlap.
- **The figure shows the crossing, not the peak, and (b) and (c) are how.** Read off (a)
  alone the panel says the connectome is the worst substrate on this axis, which is both
  the wrong reading and — at N = 448 — an unresolvable one. (b) makes the peak
  unreadability visible (every variant within 3.5% of the hard ceiling, connectome 0.965
  against 0.993 to 0.997) and (c) makes the decay difference visible (47% against 28 / 22
  / 11%, a four-fold spread). The crossing *is* the pair.
- **(b) is a dot plot and (c) a bar chart, and the difference is not decorative.** (b)'s
  axis cannot start at zero — its whole content is the last 5% below the ceiling — and
  bars on a cropped baseline would read as a large effect, which is exactly the claim
  A3M.2 forbids. Dots carry no area, so the crop is honest. (c) is zero-based and is
  therefore drawn as bars.
- **The aggregation is asserted against `TIER0` §1.2, not trusted.** The builder checks
  that the connectome peaks lowest, that it retains most, and that all four peaks and
  overlap-top values match the published table to 0.1. A figure that stops reproducing
  the table it is captioned with fails the build.
- **Stripped of in-panel furniture on the author's review.** (a)'s "top of overlap"
  text, (b)'s per-dot value labels and both small-panel titles are gone; the rules,
  markers and percentages that *are* the data stay. Each removed item is a sentence the
  caption was already carrying or now carries, and three annotated panels at this width
  were spending ink restating the caption. The one thing the caption had to gain is a
  clause naming (a)'s unlabelled dashed rule.
- **The legend is figure-level, below all three panels.** In (a) there is nowhere inside
  the axes that a four-entry box fits: the curves rise through the lower left, run along
  the ceiling across the top, and the nulls' tails occupy the lower right. Measured, not
  judged — the lower-left placement the figure was first built with had the rising limb
  crossing the first two entries. F5's treatment, for F5's reason.
- **The ceiling label sits on the left, which is a deviation from the shared helper's
  default and is why `draw_ceiling` gained a `side` argument.** The top-of-overlap rule
  occupies the right-hand edge, and a right-aligned ceiling label has that rule drawn
  through it. Default is unchanged, so F3 and F6 take the identical path.
- **Caption (final wording):**

  > **Figure F7. Matched on effective criticality the connectome peaks lowest and
  > retains most: the memory result is a crossing, not a capacity difference.** Human
  > N = 448 self-built consensus, all-positive weights (`f` = 0), memory-capacity task,
  > 10 seeds, ridge α = 1e-6. **(a)** Ridge effective rank `d_eff` against
  > `σ·bulk95` — the axis that holds the **bulk** radius fixed and lets the Perron root
  > vary (F3). `bulk95` is a per-seed quantity for the three resampling nulls, so each
  > seed is reindexed onto the common grid before the median is taken; the grid is
  > clipped to the range every (variant, seed) covers, which is what puts the top of the
  > overlap — the **dashed rule** — at `σ·bulk95` = 2.599. All four substrates rise
  > together, all four reach the
  > `d_eff = N = 448` ceiling, and they separate only on the way down. **(b)** At the
  > peak they are **not** separable: every variant lands within 3.5% of the ceiling
  > (connectome 0.965, nulls 0.993 to 0.997), so peak capacity is unresolvable at this
  > size and no claim is made about it in either direction. **(c)** The decay is
  > resolvable and is the result: at the top of the overlap the connectome still holds
  > **47%** of its own peak against **28 / 22 / 11%** — a four-fold spread. A ceiling can
  > clip curves but
  > cannot manufacture a crossing, so the decay result is robust to finite size in a way
  > the peak result is not. The same retention ordering holds on the **nominal** axis,
  > where the Perron root rather than the bulk is matched, so it is not an artifact of
  > the axis that hands the connectome the larger gap. At its own optimum the
  > connectome's memory is at parity with the nulls, 2 to 6% below and not reliably so
  > against every null (F10); the advantage here is robustness, not capacity.

### F9 — the supercritical margin across a 2.2× change in N

- **Claim carried:** A3M.4
- **Source:** source `n1000` = `n1000_memory_scale_448.parquet` and
  `n1000_memory_scale_1000.parquet` concatenated on an `n_nodes` column. Supercritical is
  `spectral_radius >= sr_crit`, under both of `TIER0` §2.4's threshold rules.
- **Panels:** (a) MC against nominal σ for the connectome and Erdős–Rényi at both scales,
  with the connectome's `sr_crit` at each scale drawn (3.078, 3.985); (b) supercritical
  median MC per variant at both scales, threshold = the connectome's `sr_crit` applied to
  every variant, margin annotated; (c) the same under each variant's own `sr_crit`.
- **Both filters are drawn, and that is the figure's main design decision.** `TIER0` §2.4
  publishes two tables and says to report both, because the answer depends on which is
  used: 4.40 → 4.42 (flat, +0.5%) on the connectome's threshold and 3.56 → 3.85 (growing,
  +8%) on each variant's own. One panel would present a filter choice as a property of
  the data — the same failure the two-axis discipline of §1.1 exists to prevent, one axis
  over. Neither is a null result and the claim survives both, which is the point worth
  making visible.
- **The primary reading is the conservative one, and the caption says why.** The
  connectome's threshold samples every null further above its own critical point, where
  it has decayed more; it is reported as primary only because it is the one comparison in
  which every variant is evaluated over an identical σ range.
- **(a) exists to show where the two thresholds cut**, which is what makes the filter
  choice concrete rather than a note. The `sr_crit` rules are unlabelled — they sit 0.9 σ
  apart, so a label on each, rotated or not, lands on the other's rule or on the
  Erdős–Rényi curve — and the caption names them.
- **Tidied on the author's review: (a)'s title gone and its legend lifted out of the
  axes; (b) and (c) cut to the filter they apply, with the margin annotations moved to
  the caption.** Two gains beyond the ink. (a)'s legend was inside the axes only because
  3 units of empty `y` had been bought for it, which cost the curves a fifth of the
  panel; below the panel, the y limit is the data's again. And (b)/(c) no longer carry a
  number the caption also carries, which is the usual way the two drift apart.
- **(a)'s legend is anchored to (a), not to the figure — unlike F7's and F10's.** It
  names two of the four substrates and a dash encoding that (b) and (c) do not use
  (they encode scale by fill instead), so a figure-wide legend at the bottom would read
  as applying to all three panels and would be wrong about two of them.
- **The panel letters are placed in points, one offset per panel.** (a) and (b) each
  clear a long rotated y label plus tick labels, (c) has neither, and (a) is half again
  as wide as the others — so a shared axes-fraction offset puts the three letters at
  three different distances from what they have to clear, and the 'a' landed on its own
  y label. Equal panel heights keep them in line vertically. This is the case
  `style.panel_label`'s `offset_points` argument exists for (Act I, F1).
- **The margins are now asserted rather than drawn.** 4.40 / 4.42 and 3.56 / 3.85 appear
  only in the caption, so the builder checks all four against `TIER0` §2.4 to 0.005. A
  caption number with nothing on the figure checking it is a number that can go stale
  silently — this is the same reasoning as F7's crossing-table assertion.
- **Caption (final wording):**

  > **Figure F9. The supercritical memory margin survives a 2.2× change in N, under both
  > definitions of "supercritical".** Memory-capacity task, `f` = 0, four substrates ×
  > 10 seeds, `T` scaled 3000 → 6000 to hold `T_eff/N` at 5.50 to 5.58 and the ridge
  > reparameterised as α = λ·trace(G)/N with λ pinned so the N = 448 supercritical median
  > α is exactly the frozen 1e-6. **(a)** Median MC against nominal σ for the connectome
  > and Erdős–Rényi at both scales; the dotted rules are the connectome's `sr_crit`,
  > 3.078 at N = 448 and 3.985 at N = 1000. Absolute MC rises about 13% for both
  > substrates with N. **(b)** Supercritical median MC with the threshold set at **the
  > connectome's** `sr_crit` for every variant: the connectome/ER margin is **4.40 at
  > N = 448 and 4.42 at N = 1000**, a change of +0.5%. **(c)** With **each variant's own**
  > `sr_crit` the same margin is **3.56 → 3.85**, i.e. it grows about 8%. Both readings
  > are defensible and they say different things, so both are drawn: the claim
  > "the supercritical memory margin is not an N = 448 accident" survives either, while
  > "scale-invariant" full stop is true of (b) alone. (b) is the primary reading because
  > it evaluates every variant over an identical σ range — which is also the filter that
  > flatters the connectome, since it samples each null further above its own critical
  > point. The N = 1000 run does **not** escape the `d_eff` ceiling (peak `d_eff/N`
  > 0.971 for the connectome against the nulls' 0.984 to 0.999), so F7's
  > robustness-not-capacity framing stands at both scales. What this run did not settle
  > is whether `bulk95` is the ladder controller: the pre-registered falsification test
  > returned **inconclusive**, because the `bulk95` reversal it rests on is itself not
  > significant at N = 1000 (paired degree − ER = +0.014 [−0.019, +0.048], p = 0.16).

### F10 — peak parity, with the CIs that forbid "always worst"

- **Claim carried:** A3M.3
- **Source:** source `peak_parity` = `criticality_matched/results/closeout_peak_parity.csv`,
  15 rows = 5 α × 3 contrasts, every contrast connectome minus a null. Paired per seed on
  the same `Win` and the same input series.
- **Panels:** (a) the paired peak MC difference with its 95% t-CI, one row per α, one
  colour per null; (b) the same as a percentage of the null's own peak, with the 2 to 6%
  band shaded.
- **The figure exists to stop a sentence being written.** Point estimates alone say the
  connectome's peak MC is below every null at every α, which reads as "always worst".
  The intervals say the effect is 2 to 6% and that against degree-matching it excludes
  zero at **one** α of five. `TIER0` §3.4's defensible wording is *parity*, and the
  figure has to carry the uncertainty for that wording to be readable off it rather than
  taken on trust.
- **Reliability is drawn on the marker, not written in a corner**: filled = CI excludes
  zero, open = CI includes it. The four open blue markers *are* the "1 of 5 against
  degree-matching" clause. A text block saying so had to sit somewhere, and every
  placement measured landed on an interval — these panels are intervals nearly edge to
  edge. The legend is figure-level for the same reason.
- **(b) is not a redundant panel.** "2 to 6%" is the form the claim is written in, and a
  reader should not have to divide by a peak that is not on the page. The percentage is
  the same statistic under a linear rescaling, so the interval carries across unchanged.
- **The α axis is doing work of its own** and the caption says so: `TIER0` §3.3 shows the
  `d_eff`↔MC correspondence is +0.999 at every α, so α can be chosen on other grounds —
  which is what makes a five-α panel a robustness check rather than a fishing grid.
- **Caption (final wording):**

  > **Figure F10. At its own optimum the connectome's memory is at parity with the
  > nulls, not below them all.** Paired per-seed differences in **peak** memory capacity
  > (each substrate at its own best σ), 10 seeds, same input weights and same input
  > series within a seed; bars are 95% t-intervals and filled markers are intervals that
  > exclude zero. **(a)** In MC units and **(b)** as a percentage of the null's own peak.
  > The deficit is **2 to 6%** and is statistically reliable against Erdős–Rényi and
  > against the weight-permuted placement control (5 of 5 α each, Wilcoxon p ≤ 0.02), but
  > against **degree-matching** the interval excludes zero at only **1 of 5** α and the
  > point estimate changes sign at α = 1e-6. The defensible statement is therefore
  > *parity at the peak*: "the connectome is always the worst substrate" overstates a
  > 2 to 6% effect that is not reliable against every null. The five α span five orders
  > of magnitude and are shown because the `d_eff`↔MC correspondence is +0.999 at every
  > one of them (`TIER0` §3.3) — provided α is raised in both places — so the readout
  > regularisation is not what produces the result, in either direction. This is also
  > where Aceituno, Yan & Liu's spread-beats-compact ordering is reproduced rather than
  > contradicted: at α = 1e-8, nearest the pseudoinverse limit they optimise, peak MC
  > orders ER > degree > weight-permuted > connectome. Spread wins at the peak; a large
  > spectral gap wins across the range (F7).

### F11 — the advantage is a rescue from Perron domination

- **Claim carried:** A3M.5, A3M.6
- **Source:** (a) source `f_extension` = `item2_f_extension_scale_448.parquet` +
  `item3_f_extension_nulls_scale_448.parquet` concatenated, filtered to `task == "mc"`
  and `spectral_radius == 6.0`, column `mean_state` by `f`, **absolute-valued per cell
  and then medianed over seeds**. (b) source `mechanism_matched` =
  `e03_mechanism_matched_scale_448.csv`, columns `median_abs_gap_matched_sigma` and
  `median_abs_gap_matched_x` against `f`.
- **Panels:** (a) common-mode amplitude `|x̄|` against `f` at σ = 6, four variants;
  (b) the median absolute connectome−ER MC gap against `f` under each matching axis.
- **`|.|` comes before the median and the builder asserts it.** `mean_state` is signed
  with a sign set by the input realisation. Median-first reports **0.638** for the
  connectome and **0.575** for the weight-permuted null at σ = 6, `f` = 0 — the null
  *below* the connectome, arguing against this figure's own caption and against
  `TIER0` §3.7. The session-0 builder did exactly that. Act II caught the identical
  defect in F4b (`act2_manifold.md` item 1); the assertion is why it cannot come back.
- **Only the controlled half of §3.7 is plotted.** The correlation half is confounded —
  `|mean_state|` and `σ·bulk95` are collinear by construction, and `TIER0` §3.7 says its
  pooled supercritical contrast must not be quoted. (b) is the matched-axis residual,
  which is the only part that adjudicates.
- **Tidied on the author's review: (a)'s y label cut to "common-mode amplitude",
  (b)'s title and its arrow-and-text annotation removed, (b)'s y label renamed.** The
  definition of `|x̄|` and the 26% both live in the caption now, and (b) no longer
  restates a number the caption carries.
- **(b)'s y label keeps the absolute-value bars, which the requested wording dropped.**
  The plotted column is `median(|connectome − ER|)` over the swept range
  (`frontier.py:700` takes `nanmedian(abs(·))`), not the median of the signed
  difference — the two are not equal, since the sign turns over below criticality. So
  the label reads `ΔMC: |Connectome − Erdős–Rényi|`; without the bars the axis would
  assert a signed quantity the data is not. **"Median" moved to the caption as
  requested**; the bars stayed because they say *what* is plotted rather than how it was
  aggregated.
- **The 26% is now asserted rather than drawn**, against `TIER0` §3.7 to 0.5 points —
  F9's reasoning, and for the same reason: it is a caption number with nothing else
  checking it.
- **This is not F4b, and the caption says which is which.** F4b carries the same
  `|mean_state|` quantity against **σ at `f` = 0**, from Probe 1's independent capture;
  F11a is against **`f` at σ = 6**, from the `f`-extension. The two captures agree to
  three decimals at their shared point, which is a cross-validation rather than a
  duplication.
- **Caption (final wording):**

  > **Figure F11. The connectome does not make memory better — non-negativity makes it
  > worse for everyone, and the connectome's spectral gap makes it least worse.**
  > Memory-capacity task, N = 448, 10 seeds. **(a)** The common-mode amplitude `|x̄|` —
  > the grand mean of the state matrix over time and units, absolute-valued per cell
  > before the seed median — against the fraction `f` of negative weights, at the
  > supercritical operating point σ = 6. With non-negative weights (`f` = 0)
  > Perron-Frobenius pins the leading eigenvector to an all-positive, hub-loaded
  > direction; the network synchronises into it, tanh saturates, and the fluctuation
  > subspace the ridge readout uses is crushed. The nulls sit at **0.949 to 0.989**,
  > essentially every unit pinned near +1, while the connectome sits at **0.759** —
  > the **least** dominated substrate *despite* carrying much the largest Perron root
  > (F1, F2). That is what the gap buys: the leading mode can be driven hard without the
  > bulk following. Balancing the signs removes the common mode entirely (two orders of
  > magnitude by `f` = 0.5) for every substrate, which is why the advantage goes with it
  > — the handicap is removed, not the resistance. **(b)** How much of the
  > connectome−Erdős–Rényi memory gap the matched-bulk axis accounts for: the **median
  > over the swept range** of the absolute MC difference between the two substrates,
  > under each matching axis. Matching on
  > `σ·bulk95` rather than on nominal σ absorbs only **26%** of the gap at `f` = 0
  > (6.42 → 4.75) but leaves a residual of about **0.5** by `f` ≥ 0.2, a
  > 9.5-fold collapse in what it fails to explain. So `bulk95` is a **partial**
  > controller whose explanatory power depends on whether a Perron mode exists at all —
  > which is sharper than the N = 1000 falsification test managed (F9). Since a
  > structural connectome is non-negative by construction, evolution cannot choose `f`,
  > and resistance to Perron domination is the only property available to select on.

---

## 4. Section outline

Structure only, at the level of section headings and the argument each carries. Prose is
written by hand, not generated (see the roadmap §4b note on drafting).

**Chapter 6, first half — Act III's memory arm.** The chapter Act II hands to. Act I
established that the substrates differ in exactly one spectral quantity; Act II
established what each half of the spectrum does to the state matrix and handed over
`d_eff` as the measure. This half asks what the gap buys on a task, and its answer is a
correction to the obvious one: not more memory, but memory that survives further.

1. **What is being asked, and the two ways of asking it.** One paragraph plus methods.
   The memory-capacity task; the two matching axes and what each holds fixed, carried
   forward from chapter 3 rather than re-derived. State up front that **neither axis is
   neutral toward the Perron-mode hypothesis** and that every claim in the chapter is
   reported on both. No results.
2. **The crossing.** *Carries A3M.1, A3M.2.* Figure F7. The chapter's opening result and
   the one the rest is scaffolding for.
   1. The four curves on the matched axis: they rise together, they all reach the
      ceiling, they separate on the way down.
   2. **The peak is unresolvable at N = 448, stated before anything is claimed about
      it.** Every variant within 3.5% of `d_eff = N`. This is a limitation converted
      into a design constraint: it is *why* the chapter reads the decay region.
   3. The retention: 47% against 28 / 22 / 11%. A ceiling can clip curves; it cannot
      manufacture a crossing.
   4. The same ordering on the nominal axis, where the Perron root is matched — so the
      result is not bought by the axis that hands the connectome the larger gap.
3. **Parity at the peak, said with an interval.** *Carries A3M.3.* Figure F10.
   Deliberately placed immediately after §2, not in a limitations section.
   1. The paired statistic and why it is paired (same `Win`, same input series).
   2. 2 to 6%, reliable against two nulls of three. The wording this licenses and the
      wording it forbids.
   3. The α axis as a robustness check that the +0.999 correspondence earns.
   4. **Aceituno, Yan & Liu reconciled here rather than in a related-work paragraph**,
      because this is the panel that reproduces their ordering. Spread wins at the peak,
      a large gap wins across the range — the two results answer different questions
      about different parts of the σ axis.
4. **Does it survive N?** *Carries A3M.4.* Figure F9. Short, and it has to be here
   rather than in an appendix, because §2's claim is a claim about a finite-size regime.
   1. The protocol: `T` scaled to hold `T_eff/N`, the ridge reparameterised, and the
      N = 448 control that isolates the parameterisation from N.
   2. The margin under both thresholds, and why both are reported.
   3. **The ceiling is not escaped, as predicted in advance** — so §2's framing stands
      rather than being rescued.
   4. **The falsification test that came back inconclusive, and why it was a flawed
      test.** Reported in the text, not buried: the predictor's own degree/ER ordering is
      not established at N = 1000, so the test could not discriminate. This is the
      chapter's one pre-registered test that did not resolve, and saying so is what
      licenses the rest.
5. **What the gap actually buys.** *Carries A3M.5, A3M.6.* Figure F11. The mechanism
   section, and the chapter's argumentative peak.
   1. Perron-Frobenius on a non-negative operator: the hub-loaded all-positive leading
      eigenvector, synchronisation, saturation, and the crushed fluctuation subspace.
      This is Act II's common-mode result, now used rather than established.
   2. The inversion that is the finding: the largest Perron root gives the **least**
      dominated substrate.
   3. Balanced signs remove the common mode for everyone, so **nobody degrades with `f`**
      — the advantage narrows because the nulls gain about four times what the connectome
      gains from a much lower start. Name this as the same "the null moved" failure
      twice more in this programme, because the chapter has just used the same discipline
      on its own delta in §2.
   4. `bulk95` as a **partial** controller: 26% absorbed at `f` = 0, ~0.5 residual by
      `f` ≥ 0.2. State that the correlation version of this test is confounded and is not
      reported.
   5. **Hub-targeted inhibition, as a consequence and not a separate result.** One
      paragraph: hub-first is the most efficient way to destroy the common mode, so it
      closes the advantage fastest; nothing collapses, and the connectome's own memory
      *rises* most under it. The `f*` ordering is real and is reported without the
      mechanistic story that was falsified.
6. **The one-line version, and what it costs to say.** Closing paragraph of the half.
   The connectome does not make memory better; non-negativity makes it worse for
   everyone, and the connectome's gap makes it least worse. Since a structural connectome
   is non-negative by construction, resistance to Perron domination is the only property
   available to select on — evolution cannot choose `f`. Forward-reference to the
   prediction arm, where the *same* axis is read with the opposite sign.

---

## 5. Audit log and open issues

Anything that did not reproduce, any number that moved, any claim that had to be weakened,
and anything a later session needs to know.

1. **The session-0 F7 builder was on the wrong aggregation, and it moved published
   numbers.** It computed the median `d_eff` at each nominal σ and used
   `σ · median(bulk95)` as the x coordinate. `bulk95` is per seed for the three
   resampling nulls, so that collapses ten different x values into one. Against
   `TIER0` §1.2 it moved the peak **locations** by up to 0.15 on x (degree 0.910 → 0.854,
   ER 0.975 → 1.107), the peak `d_eff` by up to 1.3 and the retained fractions by a point
   (ER 11% → 12%). **The connectome row is identical under both**, because its `bulk95`
   is a constant — so the one row a reader checks first is the one row that cannot reveal
   the defect. That is now the third instance of this shape (Act I item 13, Act II
   item 1). Fixed: `_matched_axis_curves` in `act3_memory.py` is the rule in one place,
   the builder asserts all eight published values, and `FIGURE_LIST`'s F7 source cell and
   a new F7 flag both record it. `sources.py`'s `taskb` filter note carries it too, so
   `--verify` prints it.
2. **`TIER0` §1.2 does not name its aggregation, and only one aggregation returns its
   table.** The rule is E0.2's per-seed-then-across-seeds reindex, stated in
   `E02_verdict` §4.4 but not in `TIER0`. Recovered here and confirmed to reproduce all
   sixteen published values exactly. **Worth a line in `TIER0` §1.2 naming it** — the
   same recommendation Act II made for §3.12's pooled median, and for the same reason: a
   later session recomputing the table has no way to know which statistic to build.
3. **`TIER0`'s two peak-`d_eff/N` columns are on different files, different α and
   different aggregations, and must not be read as a series.** §1.2's N = 448 figures are
   the per-seed-then-median matched-axis peaks from Task B at the frozen α = 1e-6
   (connectome 0.965); §2.4's N = 1000 figures are the **maximum over all cells** of
   `d_eff_norm` on the N = 1000 parquet at the reparameterised α (connectome 0.971, nulls
   0.984 to 0.999). Each reproduces exactly under its own rule.

   The natural cross-scale reading — "0.965 → 0.971, so the ceiling loosens with N" —
   **has the wrong sign**, and both confounds push the same way. Put on one file and one
   rule, the connectome's peak `d_eff/N` *falls* with N: max-over-cells gives
   **0.9967 → 0.9710** and median-over-seeds-then-max gives **0.9757 → 0.9563**. The
   claim `TIER0` actually makes — the ceiling is not escaped at either scale — is
   untouched, and holds under every rule tried. Nothing in this act quotes the
   comparison; F9's caption quotes §2.4's numbers with the scale attached and says only
   that the ceiling is not escaped.
4. **`TIER0` §3.3's "+0.999 at every α" is an n = 52 seed-median statistic and the
   document does not say so.** Reproduced to ten decimals from
   `taskB_mc_alpha_correspondence.csv` (n = 52 = 4 variants × 13 supercritical σ). The
   cell-level version over all 520 supercritical cells is **+0.9973 to +0.9984**, i.e.
   +0.998 — which is what a later reader recomputing "the correspondence" will get.
   Nothing rests on the third decimal, but this is Act II's contribution-6 trap in a
   different section, and the fix is the same: name the unit beside the number.
5. **`TIER0` §2.5 attributes the N = 448 control's realised α to the N = 1000 run — a
   mislabelled diagnostic, not a wrong result. FOR THE AUTHOR'S DECISION.** §2.5's
   "Hyperparameters" paragraph is explicitly about the N = 1000 configuration and states
   *"Realised α: median 8.6e-07, range [2.6e-07, 1.1e-06]"*. Measured from the frozen
   parquets, those are the **N = 448 control's** figures (median 8.605e-07, range
   [2.61e-07, 1.12e-06], matching to every quoted digit). The N = 1000 run's realised α
   is **median 1.918e-06, range [5.84e-07, 2.46e-06]**. Nothing downstream uses these —
   the α *rule* is exact at every cell (§2.6 finding 1) and the pin is confirmed (finding
   2) — so no number in this act or in F9 moves. **Not corrected here**, because `TIER0`
   is rank 1 and this act file is rank 4; sessions 0 and 2 each amended `TIER0` on the
   author's explicit decision, and this is logged for the same.
6. **The generated `E02_verdict.md` restated the withdrawn framing of §1.1, and the file
   is tracked.** `criticality_matched/verdict.py` wrote that the subcritical deficit
   *"is almost entirely a normalisation artifact"* and that any statement of it should be
   *"restated as an artifact of nominal-σ matching"* — the exact wording `TIER0` §1.1
   opens by ruling out ("that is not defensible and must not be written that way"). It
   also wrote "because its bulk is more compressed", "the connectome's compact bulk" and
   "the mechanism the compact bulk produces", all three of which `CONVENTIONS` replaces
   with "a larger spectral gap". **Fixed in `verdict.py`**: the passage now reports the
   deficit on both axes, says what each holds fixed, names the wording that is ruled out,
   and summarises as *parity below criticality, advantage above*. Strings only — no
   behaviour, no signature, no artifact regenerated.

   **The tracked `results/E02_verdict.md` still carries the old text**, because
   regenerating it is a run and this session did not need one. Whoever next runs
   `criticality_matched --verdict` will pick up the corrected wording; until then the
   committed `.md` and its generator disagree, and that is deliberate and recorded here.
   This is Act II item 5's category — a withdrawn claim written into generated
   markdown — found this time inside the act that owns the module.
7. **Two shared-module additions, both additive, and a full re-render proves it.**
   `style.AXIS_COLOUR` (one colour per matching axis, for the figures that contrast the
   two rather than plotting on one) and a `side` argument on `style.draw_ceiling` (F7's
   top-of-overlap rule occupies the right-hand edge, where the ceiling label defaults
   to). Both default to the previous behaviour. `python -m report.figlib --all` then
   moved **only F7, F9, F10 and F11** — verified with `git status`, not assumed.

   **`act1_structure.f3_two_axes` still carries the same two hexes as a local
   `axis_style` dict**, so the constant is now defined twice with equal values. Not
   unified, because that is a cross-act edit and `CONVENTIONS` reserves it to Act I's
   session. A later session touching F3 should point it at `style.AXIS_COLOUR`.
8. **F11's builder had Act II item 1's defect too — the same median-then-abs — and it is
   the second act in a row to find it.** At σ = 6, `f` = 0 it would have drawn the
   connectome at 0.638 and the weight-permuted null at 0.575, i.e. the null below the
   connectome, contradicting `TIER0` §3.7 and F11's own caption. Fixed and asserted.
   Worth stating as a general lesson rather than a third bug report: **`mean_state` is
   signed with an arbitrary sign, and any figure or table that aggregates it must
   absolute-value per cell first.** `TIER0` §3.12 carries the gotcha; two of the three
   builders that used the column got it wrong anyway.
9. **The five α columns in `taskB` are `d_eff`/MC *pairs*, and the base columns are the
   1e-6 member of that grid rather than a separate solve.** `mc` equals `mc_alpha_1e-06`
   bit-for-bit and `d_eff` is the 1e-6 effective rank of the stored `eig_gram`
   (recomputed to ≤ 1.9e-07, the `float32` storage). So the α robustness check in F10 and
   the frozen headline numbers are on one and the same evaluator pass, not two.
10. **What this act did not do, deliberately.** No run: every figure is built from frozen
    artifacts, and the only simulation performed was four N = 448 cells rebuilt as an
    audit check against the frozen parquet (§2.6 finding 4). Mackey-Glass was not
    inspected. The `f` > 0 material is used only where `TIER0` §2.6 and §3.7 already
    publish it, and always with its σ attached. F16 — the crossing with its axis — is
    Session 4's, and this act's numbers are the memory-arm half it will need.
12. **Substrate naming brought into line with F1 to F6, on the author's review.** Act
    III's builders were still on `VARIANT_LABEL` / `VARIANT_TICK` — the rung-numbered
    scheme ("rung 2 · degree", "rung 1 · ER") — while every figure in chapters 3 to 5
    uses `VARIANT_TITLE` and `VARIANT_TITLE_TICK`, the real null-model names. Three
    substrates were therefore named one way in chapter 5 and another in chapter 6.
    Changed in all four figures: legends and curve labels take `VARIANT_TITLE`, and the
    two remaining in-figure abbreviations went with them — F9's margin annotation
    ("connectome / ER" → "connectome / Erdős–Rényi") and F11b's y label.

    **Two layout consequences, both handled rather than absorbed.** The real names are
    wider than the one-unit category spacing in F7's (b), (c) and F9's (b), (c), so those
    tick labels are **rotated 30°** rather than wrapped onto two lines or shrunk below
    the contract's sizes; and F9's panel-(a) legend would have been nearly twice the
    panel's width as four "Connectome, N = 448"-style entries, so it is now a
    **two-column crossed legend** — substrate by colour in one column, scale by dash in
    the other. F11b's y label is wrapped mid-phrase so its longest line matches panel
    (a)'s, which is what keeps it clear of the panel letter.

    **`VARIANT_TICK` and `VARIANT_LABEL` are untouched in `style.py`** — this is a
    per-figure choice, as it was for F1 (Act I item on `VARIANT_TITLE_TICK`) and F4b
    (Act II item 12), not an amendment to the contract.
11. **For Session 4.** The memory arm is validated: F7's crossing, F9's two margins,
    F10's parity intervals and F11's mechanism all reproduce and all assert against
    `TIER0` in their builders. `_matched_axis_curves` in `act3_memory.py` is the
    per-seed-then-median rule for the matched axis; if the prediction arm reindexes
    anything on `σ·bulk95` it needs the same rule, and for the same reason. The
    generative-boundary key `dStraight` is still the withdrawn word in
    `report/figlib/style.py` and `phase_diagram/analysis.py` — Act II item 4 flagged it
    as sessions 3 and 4's, and it belongs to the prediction arm, so it is **not** touched
    here. **And `act3_prediction.py` is still on the rung-numbered substrate names** —
    `VARIANT_LABEL` at lines 77 and 96 and `variant_kwargs`' default at 67 and 134 — so
    F12, F13, F14 and F16 will name the substrates differently from every other figure in
    the thesis until session 4 makes the same change item 12 records here.

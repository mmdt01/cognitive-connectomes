# Tier 0 — canonical state of play

**Status:** consolidated 8 August 2026; N=1000 result added 11 August 2026; `f > 0`
extension added 12 August 2026 (§2.3, which supersedes the earlier "the crossing does not
survive" verdict). **This document supersedes** the individual
summaries it draws on: `eigenspectrum/results/E04_summary.md`,
`criticality_matched/results/E02_verdict.md` §4, `taskA_alpha_summary.md`,
`taskB_summary.md`, `item2_summary_scale_448.md` and `closeout_*`. Those remain as the
detailed record and the
artifact trail; where they disagree with this document, **this document is correct**.

Every number below is traceable to a named artifact. Four steps required simulation --
Task B (`f = 0`, MC only, N=448), the N=448 protocol control, the N=1000 run (§2.4) and
the `f > 0` extension (§2.3), all on ada. Everything else is reanalysis of frozen
parquets.

---

## 0. One-paragraph summary

The connectome's memory advantage over random nulls **survives** correction for
effective criticality, but it is not the advantage previously claimed. It is not a
capacity advantage — the connectome has the **lowest** peak memory of any variant, on
both `d_eff` and MC, at every ridge α tested. It is a **robustness** advantage: all
variants peak at essentially the same height and the connectome retains far more of it
as effective criticality rises. The previously reported subcritical *deficit* is
axis-dependent: present at matched spectral radius, absent at matched bulk radius —
neither axis is neutral, and the result stands on surviving both. Separately, the
cross-panel memory/generation **crossing survives** reindexing once the `f > 0`
censoring is lifted — it sits at (x = 2.938, f = 0.153), and the same extension shows
the generative advantage is present at the biologically real `f = 0` too, where the
σ = 6 sweep had hidden it (§2.3). Read in **absolute** terms (§2.6) the account
sharpens again: negative weights *improve* supercritical memory for every substrate, so
the advantage's collapse with `f` is the nulls catching up, not the connectome degrading
— the connectome's edge is resistance to **Perron domination**, and balanced signs remove
the domination rather than the resistance (§3.7).

---

## 1. What was withdrawn or reframed

### 1.1 RESTATED — the subcritical deficit is axis-dependent, and *neither axis is neutral*

An earlier draft of this section called the subcritical deficit "89% an artifact of
nominal-σ matching". **That is not defensible and must not be written that way.**

The operator actually simulated is `σ·W/|λ₁|`. Its spectral radius is **exactly σ for
every variant** — the normalisation guarantees it. Its bulk radius is `σ·bulk95`. So the
two axes are not "wrong" and "right"; they hold **different spectral features fixed**:

| axis | what it holds fixed | what it lets vary |
|---|---|---|
| nominal σ | **spectral radius** (textbook ESN criticality) | bulk radius |
| `σ·bulk95` | **bulk radius** | Perron root — deliberately unmatched |

At the matched point x = 1.949 the connectome sits at σ = 6.0 against ER's σ = 3.54: a
**1.7× larger Perron root**. And the memory mechanism under test *is* the hub-localised
Perron mode. **So the `σ·bulk95` axis is not neutral toward the hypothesis it is
testing** — it hands the connectome more of the very thing proposed as the cause.
Nominal σ is not neutral either, in the opposite direction.

> **Correct wording:** the subcritical deficit is **present at matched spectral radius**
> (−217.4) and **absent at matched bulk radius** (−24.0). The two axes hold different
> spectral features fixed, and the connectome's spectral gap is what separates them.
>
> **Present both axes side by side, state what each holds fixed, and let the result
> stand on surviving both — which it does.** That is a stronger position than claiming
> one axis is correct.

The supercritical advantage survives on both axes (+343.3 nominal, +196.5 matched), and
the ladder ordering survives on both. The *subcritical* claim survives on neither
reading as originally stated, and should simply be dropped: **parity below criticality,
advantage above** is true on the matched axis and defensible as a summary because the
nominal-axis deficit is fully explained by the unmatched bulk.

Fixed in `PROJECT_KNOWLEDGE_BASE.md`, `PHASE_DIAGRAM_EXPERIMENT.md` §9.5 and the
roadmap's Act I.

### 1.1b REFRAMED — the memory panel's `f`-collapse is the nulls catching up

The phase diagram reports the memory advantage as "a low-`f`, supercritical wedge,
extinguished by `f` ≈ 0.15–0.20". In absolute terms **no substrate degrades**: MC at
σ = 6 *rises* with `f` for all four variants, the connectome by +2.75 and ER by +10.69,
so the wedge closes because the nulls gain four times as much from a much lower start
(§2.6). Balanced signs destroy the Perron common mode, which is the thing the nulls were
losing to (§3.7).

> **Correct wording:** sign composition does not trade the connectome's memory away — it
> *removes the handicap the nulls were under*. The connectome's edge is resistance to
> Perron domination, and balanced signs remove the domination rather than the resistance.

This is the same failure mode as §1.2, one axis over: a delta read without its levels.

### 1.2 REFRAMED — memory is robustness, not capacity

At matched effective criticality every variant peaks within a few percent of the
`d_eff = N` ceiling, so **peak capacity is unresolvable at N=448**. The result is a
decay-rate difference. **Lead with the crossing:**

| variant | peak `d_eff` | at `σ·bulk95` | at top of overlap (2.599) | retained |
|---|---|---|---|---|
| Connectome | **432.4** (lowest) | 1.04 | **204.9** | **47%** |
| Weight-permuted | 445.7 | 0.93 | 126.8 | 28% |
| Degree-matching | 444.7 | 0.91 | 96.4 | 22% |
| Erdős–Rényi | 446.6 (highest) | 0.97 | 49.5 | 11% |

A ceiling can clip curves but **cannot manufacture a crossing**, so the decay result is
robust to finite size in a way the peak result is not. This is the single most
important structural fact in Tier 0.

The retention ordering is the same on the nominal axis, where the Perron root *is*
matched — so it is not an artifact of the matched-bulk axis handing the connectome a
larger gap (§1.1). It survives both axes, which is the standard the claim should be
held to.

### 1.3 CONVENTION — `sr_crit = 1 / median_over_seeds(bulk95)`

`1/x` is convex, so `mean(1/bulk95) > 1/mean(bulk95)` (Jensen) and **the per-seed mean
is biased upward** — by up to 0.087 at N=1000. The median commutes with monotone
transforms, so the two computation orders agree to ≤0.0014 and `sr_crit` can be
reproduced by inverting the reported central `bulk95`. Implemented in
`eigenspectrum.common.SR_CRIT_CONVENTION`; both scales re-run.

### 1.4 ANSWERED — the N=1000 question

It was never the ceiling question: peak MC is ~15 against N = 448, so MC was never
ceiling-limited, and `d_eff` saturation is confined to the peak, which is not where the
result lives. The question was whether the supercritical margin scales with N.

> **Answered: it holds. Margin 4.40 (N=448) → 4.42 (N=1000), a +0.5% change.** Absolute
> MC rose ~13% at both scales; the *ratio* is what survived unchanged. The supercritical
> memory margin is **not an N=448 accident**. Full result in §2.4.

> **The successor question is sharper: is `bulk95` actually the ladder controller?** The
> N=1000 falsification test came back inconclusive — not because the outcome was noisy
> but because the *predictor* was (§2.4). That is now the open mechanistic question.

---

## 2. The corrected results

### 2.1 E0.4 — spectra (`eigenspectrum/`)

Reproduction gate passed at N=448: 210 cells match the frozen `w_spectra.parquet` to
1.2e-14; documented values return (connectome `bulk95` 0.3249, `sr_crit` 3.078; nulls
0.489–0.551). Weight-permuted is **0.512**, not the 0.520 quoted in the roadmap.

| variant | `bulk95` N=448 | `sr_crit` | `bulk95` N=1000 | `sr_crit` |
|---|---|---|---|---|
| connectome | 0.3249 | **3.078** | 0.2509 | **3.985** |
| weight-permuted | 0.5120 | 1.922 | 0.4254 | 2.395 |
| degree | 0.5238 | 1.873 | 0.4449 | 2.301 |
| Erdős–Rényi | 0.5509 | 1.807 | 0.4307 | 2.438 |

**The null ordering by `bulk95` reverses between scales** (at N=448 ER > degree; at
N=1000 ER < degree), so that ordering must not be assumed to carry.

### 2.2 E0.2 — the `f = 0` memory panel (`criticality_matched/`)

Pre-registered prediction (locked before any analysis): *the wedge shrinks
substantially or vanishes*. **Partially confirmed; the "vanishes" branch is rejected.**

| quantity | nominal σ | `σ·bulk95` | change |
|---|---|---|---|
| peak `dD` | +343.3 at σ=4.47 | **+196.5 at 1.949** | 57% retained |
| most negative `dD` | −217.4 | **−24.0** | 89% of deficit removed |

After Task B extended the sweep to σ = 8, the matched peak is **interior** to the
overlap [0, 2.599] and turns over, declining to +155.5. So 57% is the value at the true
peak, not a bound. Interpolation-insensitive (linear/cubic within 0.8%).

### 2.3 The (f, σ) panels reindexed — the crossing survives, once the censoring is lifted

**Superseded 12 August 2026 by the `f > 0` extension** (roadmap §4a item 1, run on ada,
12 min at 128 workers). The earlier verdict — "the dissociation is not refuted, the
crossing is" — was read off a panel censored at σ = 6 for every `f > 0`. With the same
grid swept to **σ = 11.2**, the censoring is gone and the verdict changes.

**Reproduction gate — exact, not distributional.** The extension was run on the machine
that produced the frozen capture and reproduced **every shared cell bit-for-bit**:
max |Δ| = 0 on `d_eff`, `mean_curvature`, `bulk95` and `neg_frac` across all 21,120
shared cells, 19,200 of them at `f > 0`. So §6.4's non-portability is strictly
*cross-machine*, and the extension is a **strict superset** of the frozen capture —
every difference below comes from the added σ range alone, not from a new realisation.

**On `σ·bulk95` the boundaries cross at (x = 2.938, f = 0.153)**, in a region every
replicate covers. Coverage now runs to x = 3.58–4.36 (was 1.95–2.34). The memory
boundary rises 0 → 0.19 and the generative boundary falls 0.35 → 0.05; the gap passes
through zero at 2.94, having been −0.162 and narrowing at the old coverage limit. The
old linear extrapolation put it near x ≈ 3.5 — right in direction, 19% too far out,
which is why it was recorded as arithmetic rather than a claim.

**The contour level had to be pinned to fully covered cells.** Both boundary operators
set their contour at 25% of the panel's *global max*, and past the all-replicates
coverage edge the panel is still populated — but only by the replicates whose own
`bulk95` reached that far. On the extended panel the raw global max of `dStraight`
(+2.849) comes from a cell backed by **one replicate of 30**, against +0.032 over fully
covered cells: an 89× difference in the level, which decides the boundary everywhere.
The level is therefore taken over cells all 30 replicates reach. Three conventions —
full-coverage cells, `n ≥ 15`, and the level pinned to the old x ≤ 2.336 range — give
**the identical crossing**; only the raw-global-max convention (level set by the n = 1
cell) gives none.

**The nominal axis moves the other way, and that is the same fact.** Over the extended
sweep the published nominal crossing **does not survive** — not through coverage (every
nominal cell has all 30 replicates) but because the generative panel's true maximum sits
at f ≈ 0–0.05, σ ≈ 7–11, which σ = 6 never saw; including it raises the level and drops
the generative boundary below the memory boundary throughout. Pinning the level back to
σ ≤ 6 returns **(σ = 4.392, f = 0.1309)** against the published (4.39, 0.130), so the
pipeline reproduces it exactly: what moved is the panel, not the method. Under
replicate resampling on the shared σ ≤ 6 grid the crossing sits at σ = 4.53
[3.85, 5.31], f = 0.136 [0.113, 0.158] — and **fails to appear in 29% of resamples**,
so it was never a sharp feature even where it was first read.

> **Neither axis is neutral here either (§1.1, generation side).** At σ = 11.2 the
> connectome reaches x = 3.58 while ER reaches ~6.2, so the region where ER collapses
> and the connectome does not falls *outside* the matched-x overlap altogether. The
> effective axis cannot see the generative advantage at its largest; the nominal axis
> can, and pays by leaving the bulk unmatched. Report both.

**Open flag CLOSED — the Panel B negative region is explained.** Curvature is a step
function of σ (straight ~0.25 rad → saturated period-2 ~2.9 rad in one grid step), so
the panel is decided by *where each variant takes the step*. Bracketed at the sweep's
own 0.4 resolution, `Δx_collapse` (connectome − ER) is negative at 9 of 10 `f`: on the
matched-bulk axis the connectome steps at a **smaller** x than ER, so between the two
step locations it is the more curved of the pair and Panel B goes strongly negative. In
nominal σ the ordering is level or reversed (`Δσ_collapse` ≥ 0). The negative region is
the generation-side face of the axis asymmetry, not a defect. Its depth is bounded by
the mode gap (~2.6 rad) and its location by the 0.4 σ grid (±0.16 in x for the
connectome). The one exception is f = 0.15, where the connectome's nominal margin (3.2
in σ, against 0–0.8 elsewhere) is large enough to survive the change of axis.

**New: the generative advantage exists at f = 0 — it was censored, not absent.** Over
σ ≤ 11.2, ER collapses to period-2 in **5 of 10 seeds** (σ ≈ 7.6–8.0) while the
connectome collapses in **0 of 10** (Fisher exact p = 0.033); at f = 0.05 it is 7 seeds
against 5. **Quote seeds, not replicates.** The independent unit is the seed: the three
draws of a seed share its mask, `Win` and input series, and at f = 0 the sign transform
is the identity, so the draws are literal duplicates. Every Panel B cell therefore rests
on ~10 independent units, not 30 — which Panel A survives easily (effects of d ≈ +10)
and Panel B does not. This is a real but modest asymmetry, and it must not be written as
"50% of replicates". The phase diagram's
reading that `ΔS` is ~0 at f = 0 and *emerges* as an onset in `f` is an artifact of
stopping at σ = 6: **the onset is in σ**, and at f = 0 it lies beyond the old sweep.
This is the biologically real cut (macro dMRI weights are non-negative), so it matters
more than the f > 0 counterfactual does.

Artifacts: `criticality_matched/results/item2_summary_scale_448.md`,
`item2_reproduction_gate_scale_448.csv`, `item2_collapse_loci_scale_448.csv`,
`e02_heatmap_*_extension*`, `figures/fig_heatmaps_matched_extension.png`.

### 2.4 N=1000 — the margin holds; the controller test is inconclusive

Run on ada, 128 workers, with the N=448 control from the same machine. Protocol: `T`
scaled 3000 → 6000 to hold `T_eff/N` (5.58 → 5.50), ridge reparameterised as
`α = λ·trace(G)/N` with λ pinned so the N=448 supercritical median α equals the frozen
1e-6. **Control passed**: the reparameterisation moved the N=448 margin 4.35 → 4.40
(median per-cell change 0.32%), so any shift at N=1000 is attributable to N.

| supercritical MC (σ ≥ `sr_crit`) | N=448 | N=1000 |
|---|---|---|
| connectome | 12.32 | 13.93 |
| weight-permuted | 7.34 | 8.98 |
| degree | 4.61 | 5.09 |
| Erdős–Rényi | 2.80 | 3.15 |
| **margin conn/ER** | **4.40** | **4.42** |

**Secondary predictions, both confirmed in advance.** The ceiling is *not* escaped (peak
`d_eff/N`: connectome 0.971, nulls 0.984–0.999), so §1.2's robustness-not-capacity
framing stands. The matched `dD` peak stays **interior** at `σ·bulk95` = 1.979 with
post-peak coverage to 2.610 — vindicating σ_max = 10.4 over 8. Peak `dD` +199 → +613;
normalised, `dD/N` 0.445 → 0.613.

**The falsification test did not swap, and the test was flawed.** `bulk95` reverses
degree/ER between scales, so it predicts ER should retain more memory than degree at
N=1000. Degree stays above ER at both scales, decisively and unchanged (ER − degree
−1.80 → −1.90, p = 0.002 both), dropping the ladder Spearman against `bulk95` from
+1.00 to +0.80. **But the reversal the test rests on is not significant** — paired
degree − ER = +0.0142 [−0.0191, +0.0475], p = 0.16, whereas the same contrast at N=448
*is* significant. The pre-registration asserted the test was "on the sign, not the size"
without checking the sign was established; it is not. Correct classification is
**inconclusive**. The connectome-vs-nulls separation (~40% in `bulk95`) is untouched.

### 2.5 N=1000 — configuration as executed, and what it cost

Folded in from `N1000_RUN_SPEC.md`, now retired. This is the record of what was
actually run, not a plan.

**Grid.** MC only, `f = 0`, variants {connectome, weight-permuted, degree, ER} × 10
seeds. N=448 control: σ ∈ [0, 8] on the frozen 0.4 step (21 points), `T` = 3000.
N=1000: **30 non-uniform σ points to 10.4** — 6 coarse over [0, 3.0], **18 dense over
[3.2, 8.0]** where the result lives, 6 over [8.4, 10.4] for post-peak coverage — with
`T` = 6000.

**Why σ_max = 10.4 and not 8.** The comparison happens on `σ·bulk95` and the connectome
has the smallest `bulk95` (0.2509), so it bounds the overlap: σ_max = 8 reaches only
2.007, which would have put the peak on the boundary and made the turnover invisible —
recreating exactly the censoring Task B was run to remove. σ_max = 10.4 reaches 2.610,
matching the N=448 coverage. Vindicated: the peak landed at 1.979, interior.

**Hyperparameters.** `T` = 6000 / warmup 500 holds `T_eff/N` at 5.50 against 5.58 at
N=448 — the design Gram is a *sample* covariance and its small-eigenvalue tail, which is
exactly what `d_eff` counts, is what finite `T/N` distorts. Ridge
`α = λ·trace(G)/N` with **λ = 4.4845e-10**, identical in `d_eff` and MC, which needs two
evaluator passes per cell (α depends on `trace(G)`, which depends on the states).
Realised α: median 8.6e-07, range [2.6e-07, 1.1e-06].

**Threading — the operational trap.** `OMP_NUM_THREADS`, `MKL_NUM_THREADS` and
`OPENBLAS_NUM_THREADS` must all be set to 1 **in the environment before Python starts**.
The Gram eigendecomposition uses multithreaded BLAS by default, and 128 workers each
spawning 128 threads will thrash; the in-process `threadpool_limits` cap only constrains
libraries already loaded. Parallelism belongs at the cell level.

**Cost, measured.** N=448 control: **32 s wall on ada at 128 workers** (2.4 core-s per
evaluation), against 400 s at 12 workers on the laptop (2.9 core-s per evaluation) — so
ada's per-core rate is close to the laptop's, not 1.5–2× slower as assumed. Memory is a
non-issue: the state matrix is 44 MB (5500 × 1000 float64), ~68 MB per worker with the
Gram and eigendecomposition workspace, ~8.7 GB marginal across 128 fork workers.

> **Estimating lesson, recorded because it recurred three times this session.** Cost
> from a **measured cell of the actual code path**, never from component timings. The
> spec's original figures were wrong by ~60× (mis-scaled from a whole-matrix wall-clock
> as though it were per-cell), the `f>0` extension was under-costed 4.3× (evaluator time
> only, ignoring the per-σ reservoir rebuild and its dense `eigvals`), and the N=1000
> estimate omitted the two-pass design that holding α matched requires.

**What this run did not settle:** the `f > 0` censoring and therefore the
memory/generation boundary crossing (§2.3, separate cheaper run); whether `bulk95` is
the ladder controller (§2.4, partially answered in §3.7); and the Dale non-normality
confound (§3.5).

### 2.6 E0.3 — the absolute (MC, VPT) frontier

Roadmap §4a item 3, run 12 August 2026. Everything else in the phase-diagram programme
reads *differences*; this reads **within-substrate absolute levels** across
(variant, f, σ), four variants, nominal σ. Two substrates had to be captured first —
`degree_rewire` reached only σ = 6 and **`connectome_weight_permuted` had never been run
under the `f` sweep at all** — 12 min on ada, gates in §2.3's terms (degree bit-exact
against the frozen capture; both against Task B at `f = 0`).

Metrics are **MC and VPT only**. `d_eff` is excluded because it is ceiling-limited at
N=448 and reads flat across `f` for reasons that have nothing to do with `f`;
`climate_error` is excluded per §6.2. MC is bounded by `max_lag` = 50 (observed ≤ 16.0)
and VPT by `free_run_len` (16.3 Lyapunov times, observed ≤ 7.95), so neither risks a
ceiling — but **VPT's floor is live**: 42% of Lorenz cells are exactly 0.

> **Headline: negative weights *improve* supercritical memory for every substrate, and
> nobody degrades.** MC at σ = 6, seed-median:
>
> | variant | f = 0 | f = 0.25 | f = 0.5 | change |
> |---|---|---|---|---|
> | connectome | 11.43 | 14.35 | 14.18 | **+2.75** |
> | weight-permuted | 5.02 | 13.64 | 13.60 | **+8.58** |
> | degree | 4.11 | 13.43 | 13.19 | **+9.08** |
> | Erdős–Rényi | 2.42 | 13.30 | 13.11 | **+10.69** |
>
> The connectome's advantage falls from **+9.01 to +1.07** *solely because the nulls gain
> about four times what it gains, from a much lower start*. So the memory panel's
> "advantage extinguished by `f` ≈ 0.15–0.20" is **the nulls catching up** — the same
> failure mode §1.2 caught for `d_eff` at `f = 0`, now shown across the whole `f` axis
> and on a metric that is *not* ceiling-limited. Peak MC over σ is flat in `f` and
> equal across variants (~15.4), so the peak was never where this lived.

**Generation is real — the instrument was wrong.** Read as VPT rather than curvature, at
σ = 2 (near every variant's own peak), paired within seed:

| f | vs weight-permuted | vs degree | vs ER |
|---|---|---|---|
| 0.00 | +0.28 | −0.01 | +0.44 (none significant) |
| 0.20 | +1.46 | +0.28 | +1.82 |
| 0.25 | +1.71 | +1.62 | +2.20 |
| 0.50 | +1.35 | +1.34 | +1.42 |

At `f = 0` the connectome is level with every null. From `f` ≈ 0.20–0.25 it is **the only
substrate still predicting** (1.3–2.8 Lyapunov times against 0.1–0.9), clearing the
weight-permuted placement control — so this is a **weight-placement** effect, not
topology. Compare the 0.032 rad curvature residual the matched-axis Panel B was
contouring (§2.3): the generative arm was weak because the *order parameter* was wrong.

**The dissociation survives, restated in absolute terms.** Memory is **supercritical and
maximal at `f = 0`** (MC +4.75 to +8.97 at σ = 6, decaying with `f`); generation is
**near-critical and absent at `f = 0`** (VPT +1.0 to +2.2 at σ = 2, emerging from
`f` ≈ 0.20). Same claim the delta panels made, now with absolute levels, paired CIs and
the full four-variant ladder.

Artifacts: `criticality_matched/results/e03_frontier_verdict_scale_448.md`,
`e03_frontier_scale_448.parquet`, `e03_frontier_paired_scale_448.csv`,
`e03_frontier_live_window_scale_448.csv`, `figures/fig_frontier_absolute.png`.

---

## 3. Mechanism findings

### 3.1 The compact bulk is a large Perron root, not a small bulk

The **absolute** bulk radius is near-identical across variants (spread **4.4%**) while
`bulk95` spreads **47.3%**. The entire between-variant difference is in `|λ₁|`:

| variant | `bulk95` | `abs(λ₁)` | absolute bulk |
|---|---|---|---|
| connectome | 0.3249 | **0.1889** | 0.0614 |
| weight-permuted | 0.5203 | 0.1152 | 0.0599 |
| degree | 0.5338 | 0.1115 | 0.0595 |
| Erdős–Rényi | 0.5535 | 0.1061 | 0.0587 |

**The headline structural statistic is the gap ratio** `|λ₁| / absolute bulk`:

| variant | gap ratio |
|---|---|
| **connectome** | **3.078** |
| weight-permuted | 1.922 |
| degree | 1.873 |
| Erdős–Rényi | 1.807 |

Note the identity: `|λ₁|/abs_bulk = 1/bulk95 = sr_crit` — the gap ratio, the inverse
bulk and the critical scale are **the same number**, so adopting it costs nothing and
names the quantity after what it measures.

> **Restate Act I:** connectome weight placement does not compress the bulk. It raises
> the Perron root (1.78× ER's) over a bulk that is essentially everyone's.
> **"anomalously compact bulk" → "anomalously large spectral gap"**, gap ratio 3.08 vs
> 1.81–1.92. Same fact, stated in the direction the data supports.

### 3.2 `d_eff(α)` — the ordering is not a ridge artifact

At α = 1e-6, peak `d_eff/N` is ≥0.993 for every null and 0.961 for the connectome, so
the peak is ceiling-limited. But the ladder ordering lives elsewhere entirely:

| σ region | ordering (+1 = connectome highest) | spread |
|---|---|---|
| subcritical (σ < 1.5) | **−1.00** (inverted) | 83 |
| near peak (1.5 ≤ σ < 3.08) | **−0.11** (absent) | 83 |
| supercritical (σ ≥ 3.08) | **+0.93** | 352 |

The supercritical ordering is **flat across α from 1e-10 to 1e2**. Only the near-peak
region moves with α, and only because raising α un-saturates the peak.

**The σ ≥ 3.05 threshold is structural, not tuned:** it is the connectome's own
critical point (1/0.3249 = 3.078), and the ordering already flips sign at σ = 2.53,
0.52 *below* it. The threshold therefore discards σ where the effect already holds — it
is conservative. Report the ordering as a **curve in σ** (artifact:
`taskA_ordering_by_sigma.csv`), not as a single thresholded number.

### 3.3 MC(α) — the α constraint does not bind

Running the *same frozen evaluator* at five α from 1e-8 to 1e-3:

- **`d_eff`↔MC correspondence is +0.999 at every α.** Raising α does not break the
  link, provided it is raised in both places. **α can be chosen on other grounds.**
- **Supercritical MC ladder ordering is +1.00 at every α** (12.28 vs 2.82 at α = 1e-6).
- **The connectome's optimal σ moves with α** (2.4 → 3.6) while every null stays at
  1.2–1.6.

### 3.4 Peak parity — say "parity", not "always worst"

Paired per-seed differences (same `Win`, same input series), 95% t-CI + Wilcoxon:

| α | connectome − ER | 95% CI | % of ER | Wilcoxon p |
|---|---|---|---|---|
| 1e-8 | −0.561 | [−0.617, −0.506] | −3.6% | 0.002 |
| 1e-6 | −0.359 | [−0.560, −0.159] | −2.4% | 0.006 |
| 1e-5 | −0.487 | [−0.742, −0.232] | −3.3% | 0.006 |
| 7e-5 | −0.665 | [−0.945, −0.385] | −4.7% | 0.006 |
| 1e-3 | −0.756 | [−1.277, −0.234] | −5.9% | 0.020 |

The deficit **is** statistically reliable against ER and weight-permuted (5/5 α with
CI excluding zero) but **not** against degree-matching (1/5). The effect is 2–6%.

> **Defensible wording:** *the connectome's peak memory is at or slightly below the
> nulls' (2–6%, reliable against ER); its advantage is supercritical.* Do not write
> "always worst" — it overstates a 2–6% effect that is not reliable against every null.

### 3.5 Dale minus edge — non-normality helps *near* criticality, not above it

Edge mode is exactly normal at every `f`; Dale is not (connectome ~2× as non-normal as
its nulls at matched `f`). Differencing `dD` at matched `f`:

- **Supercritical (σ ≥ 3.05):** ≈0 for `f` ≥ 0.25; **−25.8 at f = 0.15**, −10.7 at
  f = 0.20. Non-normality does **not** buy supercritical memory; around f ≈ 0.15–0.20 it
  costs.
- **Near criticality (σ = 2.0):** strongly **positive** and growing with `f` (+18 at
  f = 0.20 up to +62 at f = 0.40).

> The hypothesis that hub-targeted inhibition → non-normality → transient amplification
> → memory is **supported near criticality and contradicted supercritically**. Since the
> hub-gating capstone is a supercritical result, non-normality is not its explanation.

### 3.6 Anisotropy — hypothesis rejected

The proposed explanation for the connectome's moving optimum (more anisotropic → α
strips directions faster) is **not supported**. Over σ ∈ [2.0, 4.2], the connectome has
the *shallowest* covariance decay:

| variant | PR | decay exponent | top-mode fraction |
|---|---|---|---|
| connectome | 1.253 | **−3.03** (shallowest) | 0.891 |
| degree | 1.205 | −3.87 | 0.908 |
| Erdős–Rényi | 1.294 | **−4.16** (steepest) | 0.873 |

PR is flat across variants (1.21–1.29) and every variant is dominated by one mode
(0.87–0.91). The connectome is **less** anisotropic by decay exponent, not more.

**Refit at the correct end of the spectrum (item 3).** The decay exponent above was
fitted over the *top* decile, while the surviving hypothesis was about the *bottom* — so
it was refitted on the **design-Gram** spectrum (the object the ridge floor actually acts
on) using the exact sensitivity of `d_eff` to the floor,
`−d(d_eff)/d(log α) = Σᵢ gᵢα/(gᵢ+α)²`, which counts directions sitting *at* the floor.
Supercritical (σ ≥ 3.05) medians:

| variant | floor sensitivity | modes within a decade of α | fraction below α | `d_eff` |
|---|---|---|---|---|
| connectome | **8.85** (lowest) | 36 | **6.6%** | 412.9 |
| weight-permuted | 18.09 | 84 | 48.8% | 223.1 |
| degree | 17.75 | 82 | 65.8% | 138.2 |
| Erdős–Rényi | 10.26 | 48 | **79.4%** | 74.8 |

**The "more directions at the floor" reading is also rejected**: supercritically the
connectome has the *fewest* modes at the floor and by far the most well clear of it
(6.6% below α against ER's 79.4%). ER's low sensitivity is degenerate — it has almost
nothing left to strip.

**But the σ-resolved version does explain the moving optimum.** Floor sensitivity is
strongly σ-dependent, and each substrate's *minimum* sits at a different σ: the
connectome's at σ ≈ 3.6 (5.8), every null's at σ ≈ 1.6–2.0 (1.8–3.9). Raising α
penalises high-floor-mass regions, so the optimum migrates toward each substrate's own
floor-mass minimum — and the measured optima do exactly that (connectome 2.4 → 3.6 as α
rises four orders, toward its minimum at 3.6; nulls 1.2 → 1.6, toward theirs at 1.6–2.0).

> **The loose end is closed, but not by anisotropy.** The connectome's α-sensitive
> optimum is explained by *where along σ its Gram spectrum sits relative to the ridge
> floor*, not by how anisotropic its covariance is. Stated as consistent-with rather
> than proven: the migration direction and endpoint match for all four variants, but the
> tracking has not been fitted quantitatively.

---

### 3.7 The memory advantage is a rescue from Perron domination, not a capacity gain

Two spectral quantities do separate jobs. `bulk95` sets **where** a substrate crosses
into supercriticality: the simulated operator is `σ·W/|λ₁|`, so the leading mode always
has gain exactly σ while the bulk has gain `σ·bulk95`. The **Perron common mode** sets
**how catastrophic** crossing is: non-negativity gives a hub-loaded all-positive leading
eigenvector, the network synchronises into it, tanh saturates, and the fluctuation
subspace the ridge readout uses is crushed.

**The common-mode amplitude confirms it, and inverts the naive expectation.**
`|mean_state|` (the Probe-2 common-mode proxy, recorded per cell), seed-median:

| σ | f | connectome | weight-permuted | degree | ER |
|---|---|---|---|---|---|
| 2 | 0.00 | **0.114** | 0.532 | 0.586 | 0.593 |
| 2 | 0.50 | 0.004 | 0.001 | 0.001 | 0.001 |
| 6 | 0.00 | **0.759** | 0.949 | 0.959 | 0.989 |
| 6 | 0.50 | 0.016 | 0.015 | 0.018 | 0.024 |

The connectome is the **least** common-mode dominated substrate *despite carrying by far
the largest Perron root* — at σ = 6 the nulls sit at 0.95–0.99, essentially every unit
pinned near +1 and the network fully synchronised. That is what the spectral gap buys:
the leading mode can be driven hard without the bulk following. Balanced signs remove the
common mode entirely (two orders of magnitude), which is why the advantage goes with it.

**A partial answer to §6.7 (is `bulk95` the ladder controller?).** Matching on
x = `σ·bulk95` — a controlled comparison, not a correlation — absorbs only **26%** of the
connectome−ER MC gap at `f = 0` (median |gap| 6.42 → 4.75) and leaves a residual of
**~0.5** by `f` ≥ 0.2, a 9.5× collapse in what `bulk95` fails to explain. Re-indexed on
x, the `f = 0` curves stay separated and the `f = 0.5` curves superimpose
(`fig_mechanism_axes`). So `bulk95` is a **partial** controller whose explanatory power
depends on whether a Perron mode exists — sharper than the inconclusive N=1000 test
(§2.4) managed.

> **NOT IDENTIFYING, reported as such.** The correlation half of this test does not
> work. `|mean_state|` and `σ·bulk95` are collinear by construction — both monotone in σ
> at fixed `f`, both monotone in `f` at fixed σ — and the within-`f` Spearmans against
> `dMC` are near-identical (at `f` = 0.15: 0.959 vs 0.956). The pooled supercritical
> contrast looks decisive (+0.796 vs −0.004) and **must not be quoted**: it is
> confounding. Only the matched-axis residual above adjudicates.

> **Wording for the draft:** the connectome does not make memory better. Non-negativity
> makes it worse for everyone, and the connectome's spectral gap makes it least worse.
> Since a structural connectome is non-negative by construction (§ biological
> interpretation in `PROJECT_KNOWLEDGE_BASE.md`), resistance to Perron domination is the
> only property available to select on — evolution cannot choose `f`.

Artifacts: `e03_mechanism_corr_scale_448.csv`, `e03_mechanism_matched_scale_448.csv`,
`figures/fig_mechanism_axes.png`.

---

## 4. Robustness of the E0.2 verdict

| axis | overlap | peak `dD` | at x | min `dD` |
|---|---|---|---|---|
| `σ·bulk95` (per-seed) | [0, 2.599] | +196.5 | 1.949 | −24.0 |
| `σ·bulk95` (variant median) | [0, 2.599] | **+197.6** | 2.144 | −31.5 |
| `σ·absolute bulk` | [0, 0.430] | +349.5 | 0.279 | −245.8 |

**The verdict is robust to `bulk95`'s extreme-value noise.** Replacing every cell's own
`bulk95` with its variant median — removing all per-seed noise — moves the peak by 0.6%.

**The `|λ₁|`-free axis is not a third axis at all — it is the nominal one.** Because
the absolute bulk is near-constant across variants (§3.1), `σ · absolute bulk` ≈
constant × σ, so it returns the uncorrected numbers (+349.5 / −245.8 against nominal's
+343.3 / −217.4). Read through §1.1 this is not a failure but a confirmation: matching
on absolute bulk radius and matching on spectral radius are the *same* matching, because
the variants differ only in `|λ₁|`. There are two axes here, not three.

---

## 5. The Aceituno argument — put this in the text

Aceituno, Yan & Liu (arXiv:1707.02469) find that *spread* eigenvalue modulus maximises
memory under OLS/pseudoinverse. **That is reproduced here**: at α = 1e-8, peak MC orders
ER > degree > weight-permuted > connectome — the exact reverse of the null ladder — and
it is not overturned at any α.

So our substrate **loses at the thing the field optimises for**, and the paper must say
so rather than let a reviewer find it. The answer is biological:

> A brain does not get to tune its gain to an optimum and hold it there. Neuromodulation,
> arousal and plasticity move the effective operating point continuously, and the
> operating point is not a free parameter that evolution can pin. Under those conditions
> the operative desideratum is not peak capacity at a tuned σ but **retained capacity
> across a range of σ** — which is exactly what the compact-bulk/large-gap substrate
> buys and what a spread-bulk substrate does not. Aceituno et al. optimise the peak; the
> connectome's edge is that it still has usable memory where a spread-bulk substrate has
> none (12.28 vs 2.82 supercritically).

Both statements are true and they are about different questions. **Spread wins at the
peak; compact wins across the range.**

---

## 6. Known limits — state these, do not work around them

1. ~~**`f > 0` is censored at σ = 6.**~~ **RESOLVED 12 Aug 2026** by the σ = 11.2
   extension (§2.3): coverage now reaches x = 3.58–4.36 and the crossing is observable
   at (2.938, 0.153). Residual limit: the boundary past the all-replicates coverage
   edge is built from a `bulk95`-selected subsample, so the *contour level* is taken
   over fully covered cells only, and the boundary itself is noisy there. Cost, for the
   record: 14.5 core-hours measured, 12 min wall at 128 workers — the ~17-minute
   estimate was right for the wall clock and wrong about why (it costed MC alone).
2. **`σ·bulk95` matches the linear operator, not the dynamics.** Realised gain at each
   variant's `σ_eff` fold differs materially (0.542 connectome vs 0.690 ER). This is
   part of the mechanism and must not be matched away, but "matched effective
   criticality" must be read narrowly.
3. **`σ_eff` never reaches 1 on MC driven states** (peaks 0.57–0.63). The "`σ_eff`
   crossing 1" criterion belongs to the *Lorenz* states and must not cross panels.
4. **The `f > 0` flip pattern is not machine-portable** (unstable `np.argsort` tie order
   on a heavily-tied edge score). Distributions agree (60/60 groups within 4 SE); per-cell
   values do not. Use each file's own `bulk95` when reindexing its cells.
   Fix for future runs: `kind="stable"` in `_select_flips` — deliberately not applied,
   since it would invalidate the frozen capture. **Refined 12 Aug 2026:** the caveat is
   strictly *cross-machine*. Re-running the grid on ada, the machine that produced the
   frozen capture, reproduced all 19,200 shared `f > 0` cells **exactly** (§2.3), so
   flip patterns are reproducible on their originating machine and a re-run there can be
   spliced onto the frozen capture. Across machines the caveat stands.
5. **On the Dale axis, sign fraction and non-normality co-vary**, unequally across
   variants. Dale-arm claims are about node-wise inhibition, not sign fraction alone.
6. **Peak `d_eff` is ceiling-limited at N=448 and will be at any N.** Confirmed at
   N=1000 (peak `d_eff/N` 0.971–0.999). No parcellation makes the peak comparison
   informative; read the decay region.
7. **Whether `bulk95` is the ladder controller is open — now partially answered.** The
   N=1000 test that was meant to settle it is underpowered *on the predictor side*: the
   degree/ER `bulk95` ordering at N=1000 is itself within noise (p = 0.16). A properly
   powered test needs more seeds, or a variant pair whose `bulk95` separation is large and
   stable across scales. **§3.7 answers the part that can be answered without more
   seeds:** `bulk95` absorbs only 26% of the connectome−ER MC gap at `f = 0` and nearly
   all of it by `f` ≥ 0.2, so it is a partial controller whose explanatory power depends
   on whether a Perron common mode exists.

8. **Paired tests at n = 10 seeds cannot survive broad multiplicity correction.** The
   smallest p a two-sided Wilcoxon can return on 10 pairs is `2/2^10` = 0.00195, so **no
   Holm correction over more than ~25 tests can reach 0.05 at any effect size**. Reporting
   "nothing is significant" over a 66-cell table would be a fact about seed count, not
   about substrates. Correct treatment: declare the family narrowly (one metric × null
   `f`-sweep) and rest the claim on the CIs and effect sizes, which is what §2.6 does.

9. **"Usable range" is threshold-dependent and must not be quoted from the flattering
   end.** Measured as "VPT is not identically zero", the connectome's usable σ window
   looks ~2× the nulls'. Under any threshold meaning *usefully predicting* (≥ 1 Lyapunov
   time, or ≥ 50% of that substrate's own peak) it is 1.25–1.5× at high `f` and
   **reverses** at low `f`, where degree-matching holds a Lyapunov time twice as far. The
   nulls drop to exactly 0 while the connectome decays gradually just above it, which is
   what the weak threshold is detecting. All three criteria are in
   `e03_frontier_live_window_scale_448.csv`.

10. **The `f > 0` boundary above the all-replicates coverage edge rests on a
    `bulk95`-selected subsample.** The contour level is therefore taken over fully covered
    cells only (§2.3); the boundary line itself is still noisy there and the region is
    drawn but should not be read quantitatively.

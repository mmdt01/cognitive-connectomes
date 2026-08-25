# Tier 0 — canonical state of play

**Status:** consolidated 8 August 2026; N=1000 result added 11 August 2026. **12–13
August 2026: the three §4a gating reanalyses landed and each changed something** — the
`f > 0` extension (§2.3, superseding "the crossing does not survive"), the absolute
frontier (§2.6, superseding the memory panel's mechanism) and the generation threshold
analysis (§3.10–§3.11, withdrawing the `σ_eff → 1` criterion). **This document
supersedes** the individual summaries it draws on:
`eigenspectrum/results/E04_summary.md`, `criticality_matched/results/E02_verdict.md` §4,
`taskA_alpha_summary.md`, `taskB_summary.md`, `item2_summary_scale_448.md`,
`e03_frontier_verdict_scale_448.md`, `e01_threshold_verdict_scale_448.md` and
`closeout_*`. Those remain as the detailed record and the artifact trail; where they
disagree with this document, **this document is correct**.

Every number below is traceable to a named artifact. **Six steps required simulation**,
all on ada: Task B (`f = 0`, MC only, N=448), the N=448 protocol control, the N=1000 run
(§2.4), the `f > 0` extension (§2.3), the two-null extension that completed the ladder
(§2.6) and the Jacobian capture (§3.11). Everything else is reanalysis of frozen
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
censoring is lifted — it sits at (x = 2.938, f = 0.153), and the same extension shows a
generative *collapse-resistance* asymmetry at the biologically real `f = 0` too, far
supercritically (σ ≈ 7.6–8.0) where the σ = 6 sweep had hidden it — though not near
criticality, where `f = 0` shows no advantage at all (§2.3, §2.6; always attach the σ).
Read in **absolute** terms (§2.6) the account
sharpens again: negative weights *improve* supercritical memory for every substrate, so
the advantage's collapse with `f` is the nulls catching up, not the connectome degrading
— the connectome's edge is resistance to **Perron domination**, and balanced signs remove
the domination rather than the resistance (§3.7).

**On the generation side the story is different in kind.** Generation is a **switch**,
not a dial: the trajectory is either on the straight attractor or in a saturated
period-2 state, with nothing stable between, and a single binary bit explains as much of
prediction quality as the full continuous geometry does (§3.10). `σ_eff` locates that
switch better than any alternative but does **not** cross 1 at it, so the criterion is
withdrawn and only the locator survives. And the gating account is **scope-limited to
`f > 0`**: at the biologically real `f = 0`, prediction decays ~10× with the geometry
completely flat (§3.11). What sets generation at `f = 0` is open.

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
is biased upward**, by up to **0.0431** within the four-rung ladder (Erdős–Rényi,
N=1000). The median commutes with monotone transforms, so the two computation
orders agree to ≤0.0014 and `sr_crit` can be reproduced by inverting the reported
central `bulk95`. Implemented in
`eigenspectrum.common.SR_CRIT_CONVENTION`; both scales re-run.

> **Amended 25 August 2026 (a): the Jensen figure is the ladder's, and 0.087 is named
> as `random_gaussian`'s.** This section read *"by up to 0.087 at N=1000"*. That value
> is right and reproduces exactly, as `mean(1/bulk95) − 1/mean(bulk95)` = **0.0868**
> for **`random_gaussian` at N=1000** on `human_empirical`, which is the rung
> `common.SR_CRIT_CONVENTION`'s own source comment names ("for random_gaussian, whose
> bulk95 is the most dispersed"). But `random_gaussian` is **not a rung of the
> four-variant ladder**, so the figure overstated the bias for every substrate this
> document otherwise reports. Within the ladder the true Jensen gap tops out at
> **0.0431** (Erdős–Rényi, N=1000), which is what the paragraph above now carries.
>
> **Two further qualifications from the same recomputation, since the gloss was loose
> in a second way.** Against the *median* rather than the mean the ladder maximum is
> **0.0727** (Erdős–Rényi, N=1000), and the sign is **negative** for all three N=1000
> nulls: the per-seed mean of `1/bulk95` sits *below* `1/median(bulk95)` there. So
> "biased upward" is a statement about **mean-vs-mean, not mean-vs-median**.
>
> **The convention does not change**: the median is still the right aggregator, it is
> the one in use, and nothing downstream moves; only the number justifying it. It is
> on the record because a justification that names a rung outside the ladder cannot be
> checked by a reader who has only the ladder. Source: `report/act1_structure.md` §5
> item 4. `report/CONVENTIONS.md` carried the same figure and was corrected in the
> same pass.

### 1.4 ANSWERED — the N=1000 question

It was never the ceiling question: peak MC is ~15 against N = 448, so MC was never
ceiling-limited, and `d_eff` saturation is confined to the peak, which is not where the
result lives. The question was whether the supercritical margin scales with N.

> **Answered: it holds. Margin 4.40 (N=448) → 4.42 (N=1000), a +0.5% change.** Absolute
> MC rose ~13% at both scales; the *ratio* is what survived unchanged. The supercritical
> memory margin is **not an N=448 accident**. Full result in §2.4.

> **The successor question is sharper: is `bulk95` actually the ladder controller?** The
> N=1000 falsification test came back inconclusive — not because the outcome was noisy
> but because the *predictor* was (§2.4). **Partially answered since, in §3.7:** a
> controlled matched-axis comparison shows `bulk95` absorbs only 26% of the gap at
> `f = 0` and nearly all of it by `f` >= 0.2, so it is a partial controller whose power
> depends on whether a Perron mode exists.

---

## 2. The corrected results

### 2.1 E0.4 — spectra (`eigenspectrum/`)

Reproduction gate passed at N=448: 210 cells match the frozen `w_spectra.parquet` to
1.2e-14; documented values return (connectome `bulk95` 0.3249, `sr_crit` 3.078; nulls
0.481–0.553).

**Every number below is a median over seeds**, per §1.3 and `CONVENTIONS`, so `sr_crit`
is exactly `1 / bulk95` row by row.

| variant | `bulk95` N=448 | `sr_crit` | `bulk95` N=1000 | `sr_crit` |
|---|---|---|---|---|
| connectome | 0.3249 | **3.078** | 0.2509 | **3.985** |
| weight-permuted | 0.5203 | 1.922 | 0.4176 | 2.395 |
| degree | 0.5338 | 1.873 | 0.4346 | 2.301 |
| Erdős–Rényi | 0.5535 | 1.807 | 0.4102 | 2.438 |

> **Corrected 15 August 2026 (session 0).** The `bulk95` columns previously held the
> per-seed **mean** while the `sr_crit` columns beside them held `1/median` — the two
> columns were on different conventions, at both scales, which is exactly the Jensen bias
> §1.3 exists to prevent. Only the `bulk95` columns moved; every `sr_crit` was already
> correct, so nothing downstream changes. The roadmap's **0.520** for weight-permuted was
> right and an earlier note here calling it 0.512 has been withdrawn. Anyone holding
> 0.5120 / 0.5238 / 0.5509 (N=448) or 0.4254 / 0.4449 / 0.4307 (N=1000) is holding the
> means. §3.1's table was already on medians and is unchanged.

**The null ordering by `bulk95` reverses between scales** (at N=448 ER > degree; at
N=1000 ER < degree), so that ordering must not be assumed to carry. The reversal holds
under either convention; the ordering of the *other* two nulls does not, which is a
further reason to quote medians only.

**The connectome/ER `bulk95` ratio rises with scale: 0.587 (N=448) → 0.612 (N=1000).**
On the withdrawn mean convention it read 0.590 → 0.583, i.e. falling. The direction of
this ratio depends on the convention, so quote it only as a median and only with both
values.

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

**There are six crossings on the matched axis, and the published one is the first — the
only one inside full replicate coverage.** Recomputed from the frozen boundary files in
session 0 (15 August 2026), the memory and generative boundaries swap order at
**x = 2.943, 3.525, 3.598, 3.670, 3.743 and 4.361**. The all-replicates coverage edge is
`x_hi` = 3.58 at its minimum over `f`, so **only the first lies inside it**; the other five
sit in the region §6.10 says is drawn but must not be read quantitatively, where the
boundary rests on a `bulk95`-selected subsample and oscillates.

> **Quote the crossing as the first one inside full replicate coverage, not as "the"
> crossing.** The bare phrasing implies a unique feature, and a reader who recomputes the
> boundaries will find six. The published (2.938, 0.153) remains the value of record; the
> 2.943 above is a coarse linear interpolation on the union of the two boundaries' grids,
> not a competing estimate, and the 0.005 gap is that interpolation, not a disagreement.
> On the nominal axis there is **no** crossing under any of the three level conventions.

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
`e02_heatmap_*_extension*`, `figures/figB_two_axis_methods.png` (the same panels,
retitled as the two-axis methods figure).

### 2.4 N=1000 — the margin holds; the controller test is inconclusive

Run on ada, 128 workers, with the N=448 control from the same machine. Protocol: `T`
scaled 3000 → 6000 to hold `T_eff/N` (5.58 → 5.50), ridge reparameterised as
`α = λ·trace(G)/N` with λ pinned so the N=448 supercritical median α equals the frozen
1e-6. **Control passed**: the reparameterisation moved the N=448 margin 4.35 → 4.40
(median per-cell change 0.32%), so any shift at N=1000 is attributable to N.

| supercritical MC (σ ≥ **the connectome's** `sr_crit`) | N=448 | N=1000 |
|---|---|---|
| connectome | 12.32 | 13.93 |
| weight-permuted | 7.34 | 8.98 |
| degree | 4.61 | 5.09 |
| Erdős–Rényi | 2.80 | 3.15 |
| **margin conn/ER** | **4.40** | **4.42** |

**The threshold is the connectome's `sr_crit` (3.078 at N=448, 3.985 at N=1000) applied to
every variant, and the result depends on that choice. Report both.** Added 15 August 2026
(session 0): the two-axis discipline of §1.1 exists precisely because a result that turns
on a matching choice must be shown under both, and this is the same situation one axis
over.

| supercritical MC, threshold = **each variant's own** `sr_crit` | N=448 | N=1000 |
|---|---|---|
| connectome | 12.32 | 13.93 |
| weight-permuted | 8.81 | 9.66 |
| degree | 5.43 | 5.73 |
| Erdős–Rényi | 3.46 | 3.62 |
| **margin conn/ER** | **3.56** | **3.85** |

> **The two filters say different things and both are defensible.** On the connectome's
> threshold the margin is **invariant** (4.40 → 4.42, +0.5%). On each variant's own
> threshold it **grows ~8%** with N (3.56 → 3.85). Neither is a null result: the margin
> holds or improves either way, and the claim "the supercritical memory margin is not an
> N=448 accident" survives both. What must not be written is "scale-invariant" full stop,
> since that is true of one filter only.
>
> **Why the connectome's threshold is the primary reading**, on the same grounds §3.2 uses:
> it is the *conservative* choice. It samples every null further above its own critical
> point, where the null has decayed more — so it is the filter that flatters the
> connectome, and it is reported as primary only because it is the one comparison in which
> every variant is evaluated over an identical σ range. Using each variant's own threshold
> compares each in its own regime and is the more natural reading of the word
> "supercritical"; it gives the smaller margin and the growing one.

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

> **Estimating lesson, recorded because it has now recurred four times.** Cost from a
> **measured cell of the actual code path**, never from component timings. The spec's
> original figures were wrong by ~60× (mis-scaled from a whole-matrix wall-clock as
> though it were per-cell), the `f>0` extension was under-costed 4.3× (evaluator time
> only, ignoring the per-σ reservoir rebuild and its dense `eigvals`), the N=1000 estimate
> omitted the two-pass design that holding α matched requires, and the Jacobian capture
> (§3.11) ran ~4× over an unmeasured guess — **no cell was timed for that code path at
> all**, and it pays a second dense `eigvals` per σ on top of the build's.
>
> **A fourth cause worth naming separately: ada is shared.** That run met a load average
> of **264 on 128 cores** from another user. Per-core rates measured on a quiet machine
> are an upper bound, not a plan.

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
maximal at `f = 0`** (MC +4.75 to +8.97 at σ = 6, decaying with `f`); the generative
*advantage over the nulls* is **near-critical and absent at `f = 0`** (VPT +1.0 to +2.2
at σ = 2, emerging from `f` ≈ 0.20). Same claim the delta panels made, now with absolute
levels, paired CIs and the full four-variant ladder.

> **This does not contradict §2.3's "the generative advantage exists at `f = 0`" — the
> two statements are about different σ, and both are needed.** At `f = 0` there is no VPT
> advantage *near criticality* (σ ≈ 2: +0.28, −0.01, +0.44, none significant), which is
> what this section reports. Far supercritically (σ ≈ 7.6–8.0) there *is* a
> collapse-resistance asymmetry — ER falls into period-2 in 5 of 10 seeds while the
> connectome does so in 0 of 10 — which is what §2.3 reports. **Always attach the σ.**
> Written without it, the two read as a contradiction and one of them will be quoted
> wrongly.

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

**The 4.4% is an N=448 number. The gap ratio is what is scale-robust, not the spread.**
Added 15 August 2026 (session 0), because the figure list needed the scale attached and
the roadmap's contribution 1 was carrying "4.4% spread" and "scale-robust" in one
sentence.

| | N=448 | N=1000 |
|---|---|---|
| absolute-bulk spread across variants | **4.4%** | **6.4%** |
| `bulk95` spread | 47.3% | 48.5% |
| gap ratio, connectome vs nulls | **3.078** vs 1.81–1.92 | **3.985** vs 2.30–2.44 |

> **What survives the change of scale is the separation, not the near-identity.** The
> connectome's gap ratio stands ~1.7x clear of every null at both scales; the nulls'
> absolute bulks are near-identical at N=448 and merely close at N=1000. Write "the
> absolute bulk is essentially everyone's" of N=448, and "the gap ratio separates the
> connectome from every null at both scales" of the scale claim. Do not let one sentence
> carry both.

**Aggregation note.** The absolute-bulk column above is `median(bulk95) x
median(|λ₁|)` — the convention §3.1's table already used, which it reproduces exactly at
N=448. Taking the median of the per-seed products instead gives the identical 4.4% at
N=448 but **6.9%** at N=1000. Quote the aggregation with the number at N=1000, where the
two differ.

> **Restate Act I:** connectome weight placement does not compress the bulk. It raises
> the Perron root (1.78× ER's) over a bulk that is essentially everyone's.
> **"anomalously compact bulk" → "anomalously large spectral gap"**, gap ratio 3.08 vs
> 1.81–1.92. Same fact, stated in the direction the data supports.

### 3.2 `d_eff(α)` — the ordering is not a ridge artifact

At α = 1e-6, peak `d_eff/N` is ≥0.993 for every null and 0.961 for the connectome, so
the peak is ceiling-limited. But the ladder ordering lives elsewhere entirely:

> **Cross-note, 25 August 2026: a second pair of peak `d_eff/N` values exists and
> neither is wrong.** `report/FIGURE_LIST.md`'s F3 flag and `report/act1_structure.md`'s
> F3 block quote **0.997** for Erdős–Rényi against the connectome's **0.965**, read off
> the **E0.2 panel** (`e02_panel.parquet`, per-substrate medians over seeds on the
> nominal axis). The pair above is this section's own: the **taskA α sweep** at
> α = 1e-6, per-variant peak over σ. Different source, different filter, same argument,
> and until now neither document named the other. **The thesis quotes this section's
> pair**; 0.965 / 0.997 appears only inside F3's own caption, where its filter is
> stated. Nothing is edited on either side.

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

**Verified 24 August 2026.** All sixteen cells of the table above were recomputed from the
frozen `covariance_spectra.parquet` and every one reproduces at the precision published
here; the derived `closeout_floor_mass.csv` also reproduces cell for cell over all 910
rows. No run was involved. Record: `report/checks/floor_sensitivity_check.md` §1.

**The "more directions at the floor" reading is also rejected**: supercritically the
connectome has the *fewest* modes at the floor and by far the most well clear of it
(6.6% below α against ER's 79.4%). ER's low sensitivity is degenerate — it has almost
nothing left to strip. **That is a statement about the stock and not about the cost**:
read as a rate, ER is the *most* floor-sensitive substrate on the ladder. See note (c).

**But the σ-resolved version does explain the moving optimum.** Floor sensitivity is
strongly σ-dependent, and each substrate's *interior minimum* sits at a different σ: the
connectome's at σ ≈ 3.6 (5.8), every null's at σ ≈ 1.6–2.0 (interior minima 1.8 to 2.4;
the previously published 1.8–3.9 is a different quantity, see note (ii)). Raising α
penalises high-floor-mass regions, so the optimum migrates toward each substrate's own
interior floor-mass minimum — and the measured optima do exactly that (connectome
2.4 → 3.6 as α rises five orders, toward its interior minimum at 3.6; nulls 1.2 → 1.6,
toward theirs at 1.6–2.0).

> **The loose end is closed, but not by anisotropy.** The connectome's α-sensitive
> optimum is explained by *where along σ its Gram spectrum sits relative to the ridge
> floor*, not by how anisotropic its covariance is. Stated as consistent-with rather
> than proven: the migration direction and endpoint match for all four variants, but the
> tracking has not been fitted quantitatively.

> **Amended 24 August 2026 (a): the aggregation is now on the record.** All four
> statistics in the refit table are computed on the **zero-stripped** design-Gram
> spectrum, `g = g[g > 0]`, as `criticality_matched/closeout.py:floor_mass` implements it.
> This section did not say so, and the omission is load-bearing: without the strip the
> **fraction below α** reproduces for **no** variant. The error grows down the ladder
> because the count of exactly-zero eigenvalues does (seed median 1.0 connectome, 11.5
> weight-permuted, 44.5 degree, 91.5 ER), so on the full 448-direction denominator the
> four read 7.03 / 50.00 / 69.53 / 83.59% against the published 6.6 / 48.8 / 65.8 / 79.4%.
> **The other three statistics are unaffected**: a zero eigenvalue contributes exactly 0 to
> `d_eff`, exactly 0 to the sensitivity, and is never within a decade of α, so only the
> fraction has a denominator to move. This is the same class of gap as §3.12's pooled
> median and §1.2's per-seed reindex, a published number that only one unstated
> aggregation returns, and it is recorded for the same reason: a later recomputation has
> no way to guess it. Source: `report/checks/floor_sensitivity_check.md` §1.3.

> **Amended 24 August 2026 (b): "minimum" means the INTERIOR minimum, and the null band
> was a different quantity.** Two corrections to the σ-resolved paragraph above; the
> σ-locations and the connectome's 5.8 are unchanged and reproduce exactly.
>
> **(i) Interior, not global.** Floor sensitivity vanishes at **both** ends of the
> spectrum, because each term `gᵢα/(gᵢ+α)²` peaks at 1/4 when `gᵢ = α` and falls away in
> either direction. A substrate whose spectrum stands far above the floor and one whose
> spectrum has already fallen far below it therefore both read low, the curve is
> two-humped, and it goes to zero as σ goes to zero, where a dead reservoir has almost no
> spectrum above the floor to lose. On the median curve the connectome's **global**
> minimum over non-zero σ is consequently at **σ = 0.4211** (2.687), *below* its interior
> dip at **σ = 3.5789** (5.785). Read as a global minimum the connectome's half of this
> claim does **not** reproduce; read as the interior dip between the two humps, which is
> what the argument needs and what the data supports, it reproduces exactly and in 8 of 10
> seeds, with every null's interior dip at 1.5789 or 2.0000 in 10 of 10 seeds. Anything
> quoting this section says **interior**.
>
> **(ii) The band 1.8–3.9 is withdrawn as the span of the null minima.** The three null
> interior minima are **2.383** (weight-permuted), **1.837** (degree) and **1.815** (ER),
> spanning **1.8 to 2.4**, which is what the paragraph above now carries. The published
> **1.8–3.9** is a different quantity: the span of the *sensitivity across the minimum
> region*, over the six values the three nulls take at σ = 1.5789 and σ = 2.0000 (lowest
> 1.815, ER at 2.0000; highest 3.925, degree at 2.0000). Both are true statements about
> different things, and **the second must not be used in a caption or read as the span of
> the minima**. Source: `report/checks/floor_sensitivity_check.md` §3.2 and §3.4.

> **Amended 24 August 2026 (c): ER's degeneracy has a second half, and the first half is
> misread without it.** The sentence above is confirmed, not withdrawn: ER's low floor
> sensitivity *is* degenerate, and 73.2% of its spectrum sits at or more than a decade
> below the floor before α is raised at all (20.4% of its directions exactly zero, a
> further 52.8% more than a decade under, against the connectome's 5.1% combined). But
> **"10.26 is low" is a statement about a level, and what governs how much a substrate
> loses when α rises is a rate.** Per unit of surviving dimensionality the ordering
> inverts:
>
> | variant | `d_eff` | floor sensitivity | sensitivity / `d_eff` | `d_eff` lost per decade of α |
> |---|---|---|---|---|
> | connectome | 412.9 | 8.85 | **2.1%** | 23.3 (**5.6%**) |
> | weight-permuted | 223.1 | 18.09 | 8.1% | 52.1 (23.3%) |
> | degree | 138.2 | 17.75 | 12.8% | 37.6 (27.2%) |
> | Erdős–Rényi | 74.8 | 10.26 | **13.7%** | 21.8 (**29.1%**) |
>
> The *absolute* loss per decade is nearly the same for the two ends of the ladder, 23.3
> against 21.8; the connectome simply has 413 directions to lose it from and ER has 75.
> **So "ER has almost nothing left to strip" must never be written as "raising α costs ER
> little".** It costs ER 29.1% of everything it has, the most of any substrate here, and
> the conflated reading is the one that flatters the connectome, which is the direction
> this programme has already been caught in three times. Source:
> `report/checks/floor_sensitivity_check.md` §5.3.

> **Amended 24 August 2026 (d): "four orders" was the step count, not the order count.**
> The paragraph above read *"as α rises four orders"* and now reads **five**. The α grid
> is 1e-8, 1e-6, 1e-5, 7e-5, 1e-3, so it spans `log10(1e-3 / 1e-8)` = **5** orders of
> magnitude in **4** steps, and the published figure was counting the steps. §3.4's own
> α table lists the same five values, and `report/act3a_memory.md`'s F10 caption already
> said "the five α span **five** orders", so the repository stated both counts for one
> grid. **No result moves**: the optima 2.4 → 3.6 and 1.2 → 1.6 are unchanged, and
> nothing is computed from the count. Corrected in `report/act2_manifold.md` (A2.7 and
> §4.5) and `report/checks/floor_sensitivity_check.md` §3.3 in the same pass.

> **Amended 25 August 2026 (e): the four-bin position table is now on the record.**
> The refit table above is a table of *statistics*; what chapter 5's §4 actually opens
> on is a table of **positions**: where each substrate's design-Gram spectrum sits
> relative to the ridge floor, bin by bin. Until now that table existed only in
> `report/checks/floor_sensitivity_check.md` §5.1, so the headline of a chapter section
> was not in the document canonical for results. Every value below is taken from that
> file; no run was involved and nothing was recomputed here.
>
> **Per-bin medians over the 50 supercritical cells, as a percentage of all 448
> directions.** Same filter as the refit table: `task == "mc"`,
> `condition == "human_empirical"`, `spectral_radius >= 3.05`, α = 1e-6, on the
> **zero-stripped** spectrum of amendment (a).
>
> | variant | exactly zero | more than a decade below α | within a decade of α | more than a decade above α |
> |---|---|---|---|---|
> | connectome | 0.2% | 4.9% | 8.0% | **89.0%** |
> | weight-permuted | 2.6% | 36.0% | 18.6% | 38.1% |
> | degree | 9.9% | 49.3% | 18.3% | 22.0% |
> | Erdős–Rényi | **20.4%** | **52.8%** | 10.6% | **11.4%** |
>
> **The connectome holds 89.0% of its directions more than a decade clear of the floor
> against Erdős–Rényi's 11.4%**, and that is what `d_eff` 412.9 against 74.8 counts.
> Read the other way, **73.2% of Erdős–Rényi's spectrum is at or more than a decade
> below the floor before α is raised at all** (20.4% exactly zero, a further 52.8% more
> than a decade under) against the connectome's **5.1%** combined, which is the level
> half of amendment (c) and the reason its rate half is needed.
>
> **Two qualifiers travel with the table and the section cannot be written without
> them.** (i) **The four bins partition each *individual* cell exactly, but four
> medians taken separately are not constrained to sum to 100, and they do not**: the
> connectome's four come to **102.1%**. Anything drawing these bins therefore groups
> rather than stacks, since a stacked bar asserts a partition the medians do not form.
> (ii) **The zero-strip of amendment (a) applies here too**, which is why "exactly
> zero" is its own bin rather than folded into "below the floor": the strip is what
> the fraction-below-α statistic is computed on, and showing the zeros separately is
> what makes the exclusion visible instead of merely stated.
>
> Source: `report/checks/floor_sensitivity_check.md` §5.1. This is the **headline of
> chapter 5's §4** (`report/CROSS_ACT_SPINE.md`'s chain step 3, drawn as F18a), and it
> is promoted for that reason: a caption-first rule cannot be applied to a number that
> is not in a rank-1 document. The σ-resolved sensitivity curve and the five per-α
> migration rows stay in the check file; they are figure data, not published results.

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

### 3.8 RESTATED — hub-gating is the Perron account, not a separate result

The placement capstone was read off `f*`, the contour where `dD` falls to 25% of its max
— a **delta on a ceiling-limited metric**. Read in absolute MC (no ceiling issue) at
σ = 6 on the Dale axis:

| f | connectome (hub / strat / periph) | ER (hub / strat / periph) |
|---|---|---|
| 0.00 | 11.43 / 11.43 / 11.43 | 2.42 / 2.42 / 2.42 |
| 0.10 | **14.88** / 13.94 / 12.94 | **10.95** / 7.23 / 6.50 |
| 0.20 | 15.58 / 15.57 / 14.20 | 14.98 / 13.53 / 10.89 |

> **Inhibiting the connectome's hubs *improves* the connectome's memory** — more than any
> other placement (11.43 → 14.88 at `f` = 0.1, against periphery-first's 12.94). The
> *advantage* closes fastest under hub-first because **ER gains +8.5 while the connectome
> gains +3.4**. The `f*` ordering (hub 0.087 < stratified 0.124 < periphery 0.164) is
> real and reproduces under both hub definitions; the word "collapse" is not. **Nothing
> collapses.**

Two further reasons the original reading was exposed: ER's own `d_eff` swings **more**
across targetings than the connectome's (range 172 vs 75 at `f` = 0.1), so the null was
never a fixed reference; and at σ = 6 every variant is against the `d_eff = N = 448`
ceiling for `f` ≥ 0.2.

**The mechanism survives and is now a consequence rather than a separate finding.**
Hub-targeted inhibition is the most efficient way to destroy the Perron common mode
(§3.7); destroying it helps *every* substrate, and helps most whichever was most dominated
by it — which is ER. So hub-gating is the placement-resolved face of the same rescue
account, not an independent controller.

> **This is the third claim in this project to turn out to be "the null moved"** (§1.2,
> §1.1b, §3.8). Any `f*`, boundary or delta should be read beside its levels before it is
> written down.

### 3.9 REFRAMED — one mechanism, two readouts (replaces "two different controllers")

The programme has described the dissociation as *two* spectral controllers: memory
governed by the hub-localised common mode, generation by `σ_eff` crossing 1 (a criterion
since withdrawn, §3.10). That framing is weaker than the data requires. Both are the **same** quantity — where the
leading effective gain sits relative to **±1** — and the two tasks simply prefer
opposite signs of it.

Each unit is `x → tanh(gain·x + input)`, so a one-dimensional map argument applies:
gain **> +1** gives a stable non-zero **fixed point**; gain **< −1** destabilises it and
a stable **period-2 orbit** appears. There is no third stable option, which is why
curvature is not graded but a two-spike distribution — 98% of 38,280 Lorenz cells sit at
~0.25 rad (smooth) or at **π** (2.99–3.20 rad, successive steps antiparallel) and 0.56%
lie anywhere between (§3.10).

**Perron–Frobenius pins a non-negative matrix to the fixed-point branch.** Its dominant
eigenvalue is guaranteed real, positive, and carried by an all-positive eigenvector.
Negative eigenvalues must exist (zero diagonal forces trace = 0) but are subdominant,
bounded by roughly `bulk95·λ₁` — 0.325 λ₁ for the connectome against 0.55 λ₁ for ER.
Grading `f` destroys the guarantee: the spectrum becomes symmetric about zero, the most
negative eigenvalue grows toward λ₁, and the period-2 branch becomes reachable at far
lower σ.

> **The same fact carries opposite consequences for the two tasks.** A dominant positive
> mode is a **liability for memory** — the network synchronises into it, every unit does
> the same thing and readout dimensions are wasted (`|mean_state|` 0.95–0.99 for the
> nulls at σ = 6, §3.7) — and **protective for generation**, because a fixed point is
> smooth and smooth is what closed-loop prediction needs. One structural cause, two
> readouts with opposite preference. That is why the two advantages *had* to occupy
> opposite regions of (`f`, σ): they are the same axis read from both ends.

**Status: consistent with everything measured, not yet a derivation.** What is measured
is the bimodality, the binary-bit R² (0.364 against continuous curvature's 0.371), the
`|mean_state|` ordering, the collapse loci and the two advantage regions. What is
inference is that a single leading-eigenvalue account generates both.

> **And it does not yet explain the `f = 0` collapse.** At `f = 0` ER collapses in 5 of
> 10 seeds at σ ≈ 7.6–8.0 with `σ_eff` = 0.014 — two orders of magnitude below its own
> peak. The linear account predicts that a non-negative matrix eventually reaches the
> period-2 branch (subdominant negative eigenvalues do exist) but not *where*, and
> something saturation-dependent is doing the work. **E0.1 (§3.10) tested this and
> confirmed the failure**: `σ_eff` is the best available locator of the transition in the
> `f > 0` regime but is not a stability law anywhere, and at `f = 0` it does not apply at
> all. What governs the `f = 0` break is open.

### 3.10 E0.1 — generation is a switch, and `σ_eff → 1` is withdrawn

Roadmap §4a item 2, run 12 August 2026 as a **threshold-location** analysis. The
mediation form it was originally specified in is not answerable: curvature is a
two-state step, so a correlation against it is a correlation between two clusters.

> **Why threshold, not dose (measured 12 Aug, 38,280 Lorenz cells).** Curvature is not a
> graded quantity on this substrate. **98% of cells sit in one of two spikes and 0.56%
> lie anywhere between them** (215 cells in [0.6, 2.2] rad). Consequently a single binary
> "has it collapsed" bit explains **R² = 0.364** of VPT variance against continuous
> curvature's **0.371** — the entire 0.25→3.14 rad range is worth 0.7 percentage points
> beyond the bit. Within the straight cluster the residual correlation is **+0.145**
> (*opposite* to the expected sign, n = 15,866); within the collapsed cluster, excluding
> the 67% of cells at the VPT = 0 floor, it is −0.151. Binning on `σ_eff` does not
> isolate a graded path either: each band's correlation tracks its *cluster mixing
> proportion*, peaking at −0.810 where the band is ~60/40 and weakening toward both ends.

> **The pre-registration, as it stood before fitting.** Held here because a falsified
> prediction is only evidence if the prediction is on the record: *`σ_eff` = 1 locates
> the transition, with a variant-dependent offset — measured so far as `σ_eff` ≈
> 0.98–1.02 at collapse for ER against 0.78–0.88 for the connectome. If the offset is not
> variant-dependent, or if `σ_eff` locates the transition no better than nominal σ does,
> say so.*
>
> **Outcome:** the offset *was* variant-dependent as predicted and `σ_eff` *did* beat the
> alternatives — but the pre-registered **value** of 1 was wrong, and the criterion is
> withdrawn below.

**Generation is gated, not graded.** A single binary "has it collapsed" bit explains
**R² = 0.364** of VPT variance; continuous curvature manages **0.371**. The entire
0.25 → 3.14 rad range is worth 0.7 percentage points beyond the bit. So the Act III
claim is *capacity is gated by which dynamical regime the manifold is in*, **not**
*capacity is graded by how curved it is*. **Scope limit (§3.11): this holds for
`f > 0` only.** At `f = 0` — the biological cut — prediction decays ~10× with curvature
flat at 0.26 across the whole sweep, so geometry gates nothing there.

**Which quantity locates the transition?** Each candidate scored by the spread of its own
value at the transition across 4 variants × 11 `f` — a predictor should take the *same*
value wherever the transition happens. Read at the last straight σ, before the transition
changes the gain.

| criterion | median at transition | IQR | **CV** |
|---|---|---|---|
| nominal σ | 1.800 | 1.200 | 0.667 |
| `σ·bulk95` (linear negative-mode gain) | 1.002 | 0.747 | 0.746 |
| **`σ_eff`** | 0.777 | 0.162 | **0.209** |

`σ_eff` is ~3× more invariant than either alternative, and the **variant-dependent offset
predicted in advance is present**, ordered by spectral gap: connectome transitions at the
*lowest* `σ_eff` (0.71–0.82), then weight-permuted (0.79–0.91), degree (0.82–0.91), ER
highest (0.87–0.95).

> **But `σ_eff → 1` is falsified as a criterion, on two independent grounds.**
> **(i)** Only **1 of 38** transition brackets contains 1; the transition sits in the band
> **0.77–0.90** for every variant. **(ii)** `σ_eff` *folds* — it rises, turns over and
> falls as the tanh gain collapses faster than σ grows — so it has a maximum over the
> sweep, and that maximum is **below 1 for every variant at `f` ≤ 0.20** (and for the
> nulls until `f` ≥ 0.30) while transitions happen throughout. A criterion whose claimed
> value is unreachable in a regime where the event still occurs is not a stability law.
> **Keep `σ_eff` as the empirical locator; drop the unit crossing.**
>
> The *linear* criterion `σ·bulk95` brackets 1 far more often (13/38, median bracket
> [1.018, 1.221]), consistent with linear instability being necessary but saturation
> delaying the actual transition.

**OPEN — what governs the `f = 0` break.** At the biologically real cut the locator does
not apply at all: ER transitions with `σ_eff` = 0.014, two orders of magnitude below its
own peak of 0.607, and on the *descending* branch (0.014 before the step, 0.011 after).
**And the connectome never breaks at `f` = 0 at all** — 0 of 10 seeds inside σ ≤ 11.2.
Whatever drives the `f = 0` collapse, it is not an effective radius crossing anything.
This is now an explicit open question rather than an assumed answer.

Artifacts: `criticality_matched/results/e01_threshold_verdict_scale_448.md`,
`e01_threshold_table_scale_448.csv`, `e01_threshold_invariance_scale_448.csv`,
`e01_threshold_straddle_scale_448.csv`, `e01_sigma_eff_fold_scale_448.csv`,
`figures/figE_threshold_location.png`.

### 3.11 The exact Jacobian — a better ruler, no law, and a scope limit on §3.10

§3.10 left the `f = 0` break unexplained. `σ_eff` is a **mean-field** quantity — it uses
the gain averaged over units — and at `f = 0` the collapsed cells have 88% of units
saturated with `|mean_state|` = 0.967, so the mean is dominated by units contributing
~0 while the dynamics live in the unsaturated remainder. The obvious hypothesis was that
the averaging was the problem. It was tested by computing the **exact** local quantity:
with `leak = 1` the map is `x → tanh(Wx + Win u)`, so the Jacobian is `J = diag(1−x²)W`,
kept as a per-unit gain vector and diagonalised exactly via the symmetric similar form
`diag(√g)·W·diag(√g)`. Full grid, Lorenz, 4 variants × 11 `f` × 29 σ × 10 seeds × 3
draws (38,280 cells, ada).

**1. The exact Jacobian is a better locator than `σ_eff`, and still not a stability law.**

| quantity | median at transition | its critical value | IQR | CV | fraction of critical |
|---|---|---|---|---|---|
| **`λ_min(J)`** | −0.849 | −1 | 0.129 | **0.152** | 0.85 |
| `σ_eff` | +0.668 | +1 | 0.203 | 0.304 | 0.67 |

> **Why `σ_eff`'s CV is 0.304 here and 0.209 in §3.10.** Different aggregation units, not
> a disagreement. §3.10 scores per **(variant, `f`) cell** after dropping cells where
> fewer than half the seeds transition (n = 37); this table scores per **seed-level
> transition** with no such filter (n = 378), which is noisier and the only unit on which
> the two quantities can be compared like for like. The comparison *within* this table is
> the valid one; do not read 0.209 against 0.152.

Keeping the gain heterogeneity **halves** the scatter, so the mean-field step does cost
something. But `λ_min(J)` does not reach −1 either: generation breaks while the fixed
point is still **linearly stable**. So the transition is not a local linear bifurcation
in either regime, and the mean-field approximation was not the missing piece.

> **What is missing is almost certainly the closed loop.** In generation the input *is*
> the network's own prediction fed back, so the operative map is
> `x → tanh((W + Win·W_out)x)` and the true Jacobian carries a rank-3 readout term that
> none of this computes. Testing it needs `W_out`, which the evaluator does not expose.

**2. The two regimes break by different mechanisms — confirmed on the grid.** At `f > 0`,
`λ_min(J)` at the transition is tight at −0.849 [−0.898, −0.769] over 378 seed-level
transitions. At `f = 0` it is −0.165, scattered over [−0.367, −0.044], on 9 transitions
out of 40 possible. Same measurement, different phenomenon — no longer a single-seed
hint.

**3. SCOPE LIMIT on §3.10: at `f = 0` capacity is lost with the geometry intact.**
Seed medians at `f = 0`:

| σ | 2 | 4 | 6 | 8 | 11.2 |
|---|---|---|---|---|---|
| connectome curvature | 0.26 | 0.26 | 0.26 | 0.26 | **0.26** |
| connectome VPT | 4.43 | 2.81 | 0.81 | 1.18 | **0.44** |
| ER curvature | 0.26 | 0.26 | 0.26 | 0.27 | 1.70 |
| ER VPT | 3.73 | 2.45 | 1.18 | 0.49 | 0.23 |

The connectome's trajectory geometry is **flat across the entire sweep** while its
prediction falls ~10×.

> **"Capacity is gated by which dynamical regime the manifold is in" (§3.10) is a
> statement about the `f > 0` counterfactual, not about the biological substrate.** At
> `f = 0` — where the real connectome lives, since dMRI weights are non-negative by
> construction — generation degrades smoothly with **no geometric event at all**, and
> curvature is blind to it. This is consistent with §3.9 rather than a contradiction: the
> switch *is* a sign-composition phenomenon, and a non-negative matrix has no dominant
> negative eigenvalue to flip. Take the negative weights away and the switch, and the
> explanation resting on it, both disappear.

**OPEN — what sets generation at `f = 0`.** Not geometry (above). **And not memory
either:** at σ = 6, `f = 0` the connectome has ~4.7× ER's MC (11.43 vs 2.42) and slightly
*lower* VPT (0.81 vs 1.18), so the obvious fallback does not work. Logged as a named open
question rather than a third guess.

Artifacts: `e01_jacobian_scale_448.parquet`, `criticality_matched/jacobian.py`.

### 3.12 Act II — the manifold probes (promoted from the knowledge base, 15 Aug 2026)

Probes 2 and 3 were written up in `PROJECT_KNOWLEDGE_BASE.md` and the probe summaries but
never in this document, so Act II's figures had no canonical source and the caption-first
rule could not be applied to them. Promoted here in session 0. **Every number below was
recomputed from the frozen parquets at the time of promotion**; nothing is carried over on
trust.

**1. The Perron mode is a common mode: it lives in the mean, not in the fluctuations.**
`|mean_state|` at σ = 6 is in §3.7's table (connectome 0.759 against the nulls'
0.949–0.989). The complementary half is that once the mean over time is removed, the
leading mode is *gone*: on the all-positive substrate the top `W`-eigenmode captures
**0.0001** of the time-centred state variance, **below the random-orthonormal baseline of
0.0023**. So the decomposition is clean — the Perron mode carries the common mode and the
bulk carries everything the readout can use.

**2. Sign composition selects which structural basis the fluctuations occupy.** Captured
variance at k = 10, connectome, at each condition's own supercritical operating point:

| task | all-positive: harm / wmodes | signed: harm / wmodes | gaussian: harm / wmodes |
|---|---|---|---|
| MC | **0.056** / 0.009 | 0.017 / **0.060** | 0.020 / **0.040** |
| NARMA-10 | **0.040** / 0.002 | 0.005 / **0.527** | 0.006 / **0.886** |
| Lorenz | **0.168** / 0.004 | 0.019 / **0.081** | 0.012 / **0.522** |

The *ordering* swaps in all three tasks: harmonics ahead when weights are non-negative,
`W`-eigenmodes ahead once signs are balanced.

> **State the swap, not the capture.** On the all-positive substrate neither basis
> captures much at k = 10 (0.04–0.17), so "the manifold lives in low-frequency graph
> harmonics" **overstates it**. What is measured is which basis wins. The low absolute
> capture is itself consistent: supercritical `d_eff` on that substrate is ~413 of 448
> (§3.2), so the fluctuations occupy hundreds of directions and no 10-vector basis should
> capture them. Where `d_eff` is *low* the capture is high — gaussian NARMA reaches 0.886
> — and the two probes agree on that without being fitted to each other.

**Scope limit.** Probe 2 captured `connectome` and `degree_rewire` only, at four spectral
radii. No Probe 2 statement may imply the four-variant ladder.

**Priority.** Sign-gating of the manifold transition is largely pre-empted by Krauss 2019
and is presented as **confirmatory**, per the roadmap's "what must NOT be claimed".

**3. Variance-weighted dimensionality misses readout-relevant structure (contribution 6).**
MC on the all-positive substrate, σ ≥ 3.05, α = 1e-6:

| statistic | `d_eff` | PR |
|---|---|---|
| ladder ordering against measured MC (7 rungs, median per variant) | **+1.000** | **+0.107** |
| within-regime, pooled (n = 350 cells) | **+0.998** | +0.308 |
| range across the seven rungs | **75 to 413** (of N = 448) | 1.19 to 1.38 |

That third row is the argument. Across the same seven substrates `d_eff` moves 5.5-fold
while PR moves by 16%, because memory lives in roughly 400 low-variance directions that a
variance-weighted measure discounts. **Both correlations are against *measured MC*, not
against rung index** — correlating against the index gives −0.18 and −0.54 and is a
different quantity. (The PR sign was published as +0.54 and **corrected to −0.54 in
session 2**, recomputed from `probe3_deff.parquet`: `spearman(rung, d_eff)` = −0.1802 and
`spearman(rung, pr)` = −0.5406. The magnitude was right, the sign was not, and PR is
negatively rank-correlated with the index under every index definition tried — the
`rung` column −0.541, position in ladder order −0.607. Nothing rests on it, since this is
the number that must not be quoted, but it is stated twice in canonical documents.)

> **Gotcha: `mean_state` is signed and its sign is arbitrary.** It depends on the input
> realisation, so seeds straddle zero. Take `|mean_state|` *before* aggregating; a signed
> median silently shrinks the connectome's σ = 6 value from 0.759 to 0.638.

**Cross-capture check.** Probe 1's `saturation_diagnostics.parquet` and the `f > 0`
extension are independent captures of the same reservoirs; at σ = 6, f = 0 on MC they
agree to three decimals on `|mean_state|` for all four variants.

Artifacts: `results/scale_448/manifold_alignment.parquet`,
`saturation_diagnostics.parquet`, `probe3_deff.parquet`, and the `*_summary.md` files
beside them.

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
3. **There is no "`σ_eff` crossing 1" criterion — it is withdrawn (§3.10).** `σ_eff`
   never reaches 1 on MC driven states (peaks 0.57–0.63), and E0.1 shows it does not
   reach 1 on the *Lorenz* states either over much of the grid: it folds, and its maximum
   is below 1 for every variant at `f` ≤ 0.20 while generation transitions happen
   throughout. Where it *is* reachable the transition still sits at 0.77–0.90, not 1.
   `σ_eff` survives as the best **empirical locator** of the generation threshold
   (~3× more invariant than the alternatives), not as a stability law, and it is
   Lorenz-only — it must not cross panels.
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

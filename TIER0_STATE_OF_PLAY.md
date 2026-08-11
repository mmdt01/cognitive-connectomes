# Tier 0 — canonical state of play

**Status:** consolidated 8 August 2026. **This document supersedes** the individual
summaries it draws on: `eigenspectrum/results/E04_summary.md`,
`criticality_matched/results/E02_verdict.md` §4, `taskA_alpha_summary.md`,
`taskB_summary.md` and `closeout_*`. Those remain as the detailed record and the
artifact trail; where they disagree with this document, **this document is correct**.

Every number below is traceable to a named artifact. Nothing here required a new
simulation except Task B (`f = 0`, MC only, N=448).

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
cross-panel memory/generation **crossing does not survive** reindexing within the range
the data covers.

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

### 1.4 RESTATED — what the N=1000 run is for

**It is not the ceiling question.** Peak MC is ~15 against N = 448, so MC was never
ceiling-limited; the finite-size problem was always a `d_eff` problem, and Task A
showed `d_eff` saturation is confined to the peak, which is not where the result lives.

> **The N=1000 question is: does the supercritical margin (12.28 vs 2.82 in MC at
> α = 1e-6) scale with N, or is it an N=448 accident?**

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

### 2.3 The (f, σ) panels reindexed — the crossing does not survive

**Control passes:** the same pipeline on the nominal axis reproduces the published
crossing at **(σ = 4.39, f = 0.130)** against the documented (σ ≈ 4, f ≈ 0.12).

On `σ·bulk95`, over the covered range the memory boundary (`f*` 0 → 0.119) stays
**below** the generative boundary (`f*` ≈ 0.285, flat) and they never meet. The gap
narrows at −0.139 per unit x but is still 0.165 at the coverage limit x = 2.336.

> **The dissociation is not refuted — the crossing is.** The boundaries diverge and
> remain separated by 0.17–0.34 in `f`; the crossing lies beyond the swept range. A
> linear extrapolation would place it near x ≈ 3.5, which is 1.5× the covered range and
> is **arithmetic, not a claim**.

Coverage stops at 2.336 because the σ = 8 extension was `f = 0` only; every `f > 0` row
is still censored at σ = 6, and that censoring edge *is* the coverage edge.

**Open flag:** Panel B on the corrected axis develops a strong negative region around
x ≈ 1.0, f ≈ 0.35–0.45. Mechanically expected (at matched x the connectome sits at much
higher nominal σ), but it should be examined before the generative panel is drafted.

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

1. **`f > 0` is censored at σ = 6.** The σ = 8 extension was `f = 0` only, so the
   reindexed heatmap coverage stops at x = 2.336 and the boundary crossing is not
   observable. Fixable with one ~17-minute run.
2. **`σ·bulk95` matches the linear operator, not the dynamics.** Realised gain at each
   variant's `σ_eff` fold differs materially (0.542 connectome vs 0.690 ER). This is
   part of the mechanism and must not be matched away, but "matched effective
   criticality" must be read narrowly.
3. **`σ_eff` never reaches 1 on MC driven states** (peaks 0.57–0.63). The "`σ_eff`
   crossing 1" criterion belongs to the *Lorenz* states and must not cross panels.
4. **The `f > 0` flip pattern is not machine-portable** (unstable `np.argsort` tie order
   on a heavily-tied edge score). Distributions agree (60/60 groups within 4 SE); per-cell
   values do not. Use `phase_cells.parquet`'s own `bulk95` when reindexing its cells.
   Fix for future runs: `kind="stable"` in `_select_flips` — deliberately not applied,
   since it would invalidate the frozen capture.
5. **On the Dale axis, sign fraction and non-normality co-vary**, unequally across
   variants. Dale-arm claims are about node-wise inhibition, not sign fraction alone.
6. **Peak `d_eff` is ceiling-limited at N=448 and will be at any N.** No parcellation
   makes the peak comparison informative; read the decay region.

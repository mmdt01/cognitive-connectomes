# N=1000 — verdict

> **Sections 1–3 are a PRE-REGISTRATION.** Written and fixed **before the run**, from
> N=448 results and the E0.4 N=1000 spectra only. Section 4 (outcome) is appended
> afterwards. If the outcome contradicts a prediction, **the prediction stands as
> written** — it is not to be revised, softened, or re-scoped after the fact.
>
> Written: 8 August 2026, before any N=1000 MC cell was run.
> Configuration and prior state: `TIER0_STATE_OF_PLAY.md` (sec 2.5 records the
> configuration as executed; it was `N1000_RUN_SPEC.md` at the time of writing,
> since folded in and retired).

---

## 1. What this run is for

**Does the connectome's supercritical memory margin scale with N, or is it an N=448
accident?**

It is **not** the ceiling question. Peak MC is ~15 against N=448, so MC was never
ceiling-limited; the finite-size problem was always a `d_eff` problem, and `d_eff`
saturation is confined to the *peak*, which is not where the result lives.

Reference values at N=448 (α = 1e-6):

| quantity | connectome | ER |
|---|---|---|
| supercritical MC (σ ≥ `sr_crit`) | **12.28** | **2.82** |
| `d_eff` at top of matched overlap | **204.9** | **49.5** |
| peak `d_eff` | 432.4 (lowest) | 446.6 (highest) |
| retained fraction, peak → overlap top | **47%** | **11%** |

---

## 2. Primary prediction

**The supercritical margin will hold or grow at N=1000.**

Reasoning stated in advance: the margin is a decay-rate difference driven by the
spectral gap, and the gap ratio `|λ₁|/abs_bulk` **increases** with N (3.078 → 3.985 for
the connectome, while the nulls move 1.81–1.92 → 1.80–2.44). If the gap is the
controller, a larger gap should buy more retention, not less.

**Quantitative commitments:**

| outcome | criterion (MC ratio connectome : ER, σ ≥ `sr_crit`) |
|---|---|
| **scales** | ratio ≥ 4.35 (i.e. ≥ the N=448 value of 12.28/2.82) |
| **holds** | ratio in [3.0, 4.35) |
| **does not scale** | **ratio < 3.0** — a ≥30% erosion of the N=448 margin |
| **fails** | ratio < 1.5, or the connectome not highest supercritically |

**"Does not scale" is ratio < 3.0.** That is the number to hold me to. A margin that
erodes by more than 30% between N=448 and N=1000 cannot be described as scaling, and the
finite-size caveat in `PROJECT_KNOWLEDGE_BASE.md` would then have to become a limitation
of the result rather than a caveat on it.

---

## 3. Falsification test — the `bulk95` ordering reversal

**This is the sharpest test available and it is not a confirmation.**

The null ordering by `bulk95` **reverses between scales**:

| | N=448 | N=1000 |
|---|---|---|
| degree | 0.5238 | **0.4449** |
| Erdős–Rényi | **0.5509** | 0.4307 |
| ordering | ER > degree | **degree > ER** |

The Act I → Act III chain claims `bulk95` (equivalently the spectral gap, equivalently
`sr_crit`) is what orders the memory ladder. That claim makes a **forced prediction**:

> **If `bulk95` orders the MC ladder, then at N=1000 degree and ER must swap in the
> supercritical MC ordering** — ER, having the *smaller* `bulk95` (larger gap) at
> N=1000, must now retain *more* memory than degree, reversing their N=448 order.

Outcomes, committed in advance:

- **Swap observed** → `bulk95` is the controller. Strong support for Act I → Act III,
  and it is a genuine prediction rather than a fit.
- **N=448 ordering preserved (degree > ER supercritically)** → **`bulk95` is not the
  controller**, and the Act I → Act III chain breaks. This would be the most important
  negative result in the programme and must be reported as such, not explained away.
- **Neither cleanly** (difference within noise) → the test is underpowered at 10 seeds;
  report the paired per-seed difference with a CI and call it inconclusive. Do **not**
  read a null as support.

The relevant comparison is **paired per-seed** (same `Win`, same input series),
supercritical region, with a CI — the same discipline as the peak-parity analysis. The
`bulk95` difference at N=1000 is small (0.4449 vs 0.4307, 3.2%), so a large MC swap is
not expected; the test is on the **sign** of the difference, not its size.

---

## 3b. Secondary predictions

**Matched `dD` peak stays interior.** At σ_max = 10.4 the connectome reaches
`σ·bulk95` = 2.609, matching the N=448 coverage (2.599) where the peak at 1.949 is
interior with room to spare. **Predicted: the peak remains interior**, at
`σ·bulk95` ≈ 1.7–2.3. If it sits at the upper edge, σ_max was still too low and the
number is a bound again — say so rather than reporting it as a measurement.

**The ceiling will not be escaped — stated in advance.** For the peak to count as
escaped, peak `d_eff/N` would have to fall below ~0.95 for *every* variant, leaving
visible separation at the peak. **It will not.** Expected: nulls ≥ 0.99, connectome
≈ 0.96, i.e. the same picture as N=448. Peak `d_eff` is ceiling-limited at any N; this
is predicted, not a disappointment, and it is why the analysis reads the decay region.
**If the peak does separate at N=1000, the N=448 conclusion in
`TIER0_STATE_OF_PLAY.md` §1.2 was wrong and must be revised.**

**Subcritical parity holds.** On the matched-bulk axis the connectome should again be at
parity or marginally better below criticality (N=448: min `dD` = −24.0 against −217.4
nominal). Predicted: |min `dD`| / N smaller at N=1000 than the 0.054 seen at N=448.

---

## 4. Outcome

*Run 11 August 2026 on ada (128 workers). N=448 control and N=1000 run from the same
machine. Artifacts: `n1000_memory_scale_{448,1000}.parquet`.*

### 4.0 Control

The ridge reparameterisation is neutral at N=448: supercritical MC margin 4.35 (frozen,
absolute α) → **4.40** (new rule), median per-cell change 0.32% MC / 0.70% `d_eff`. ada
reproduced the laptop's realised α to three significant figures. **Baseline for §2 is
therefore 4.40.**

### 4.1 PRIMARY — the margin holds

| | N=448 | N=1000 |
|---|---|---|
| connectome | 12.32 | 13.93 |
| weight-permuted | 7.34 | 8.98 |
| degree | 4.61 | 5.09 |
| Erdős–Rényi | 2.80 | 3.15 |
| **margin conn/ER** | **4.40** | **4.42** |

Against §2's criteria the ratio of 4.42 clears the ≥4.35 bar, so it lands in the
**"scales"** band as written. But the change is **+0.5%**, so the substantive
description is that it **holds** — flat, not growing. Absolute MC rose ~13% for both
connectome and ER, and the ratio is what survived unchanged.

**The supercritical margin is not an N=448 accident.** That was the question this run
existed to answer, and it is answered.

### 4.2 FALSIFICATION — no swap, but the test was underpowered on the predictor side

Predicted: if `bulk95` orders the MC ladder, degree and ER must swap at N=1000, because
`bulk95` reverses between scales.

**They did not swap.** Degree stays above ER at both scales, decisively and by an
essentially unchanged margin:

| | ER − degree (paired, per seed) | p |
|---|---|---|
| N=448 | −1.804 [−2.125, −1.484] | 0.002 |
| N=1000 | −1.902 [−2.187, −1.617] | 0.002 |

`bulk95` at N=1000 puts ER (0.4307) *below* degree (0.4449), so it predicts ER should
retain more memory. It retains decisively less. The ladder Spearman against `bulk95`
therefore drops from **+1.00 at N=448 to +0.80 at N=1000** — one transposition, on
exactly the pair where the predictor made a discriminating claim.

**But this does not cleanly falsify, and the reason is a flaw in my own test design.**
The `bulk95` reversal the test rests on **is not statistically significant**: paired
across seeds, degree − ER = **+0.0142 [−0.0191, +0.0475], p = 0.16**. At N=448 the same
contrast *is* significant (−0.0271, CI excludes zero). So at N=1000 the predictor has no
established ordering between degree and ER, and a test cannot be discriminating on a
distinction the predictor cannot make.

I pre-registered that the difference was small (3.2%) and asserted the test was "on the
sign, not the size" — but never checked whether the sign itself was established. It
isn't. **The honest classification is §3's third branch: inconclusive**, and it is
inconclusive for a reason I should have caught before running.

What survives: `bulk95`'s *point-estimate* ordering fails to predict the MC ordering at
N=1000, which is weak evidence against `bulk95`-as-sole-controller and warrants a
properly powered test. The connectome-vs-nulls separation — where `bulk95` differs by
~40%, far outside noise — is untouched and remains perfectly ordered.

### 4.3 SECONDARY — both predictions confirmed

**Ceiling not escaped, as stated in advance.** Peak `d_eff/N` at N=1000: connectome
**0.971**, weight-permuted 0.994, degree 0.984, ER 0.999 (predicted ≈0.96 and ≥0.99).
Peak `d_eff` remains ceiling-limited, so the decay region is still the place to read the
result — no revision to `TIER0_STATE_OF_PLAY.md` §1.2 is required.

**Matched peak stays interior.** At σ_max = 10.4 the overlap reaches `σ·bulk95` = 2.610
and the peak sits at **1.979** (predicted 1.7–2.3), interior with post-peak coverage,
declining to +459.6 at the edge. σ_max = 10.4 was the right call; σ_max = 8 would have
placed it at the boundary again.

`dD` peak grows +199.3 → **+612.8**, but that is mostly `d_eff` scaling with N. In
normalised terms the advantage does grow: peak `dD/N` **0.445 → 0.613**.

### 4.4 What this settles, and what it does not

**Settles:** the supercritical memory margin is scale-stable (4.40 → 4.42), the matched
peak is a measurement at both scales, and the ceiling caveat is confirmed rather than
escaped.

**Does not settle:** whether `bulk95` is the ladder controller. The N=1000 test was
underpowered because the predictor's own degree/ER ordering is within noise there. A
properly powered version needs either more seeds (to establish the `bulk95` ordering) or
a variant pair whose `bulk95` separation is large and stable across scales.

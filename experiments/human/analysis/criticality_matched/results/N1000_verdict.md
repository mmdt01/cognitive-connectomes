# N=1000 — verdict

> **Sections 1–3 are a PRE-REGISTRATION.** Written and fixed **before the run**, from
> N=448 results and the E0.4 N=1000 spectra only. Section 4 (outcome) is appended
> afterwards. If the outcome contradicts a prediction, **the prediction stands as
> written** — it is not to be revised, softened, or re-scoped after the fact.
>
> Written: 8 August 2026, before any N=1000 MC cell was run.
> Configuration: `N1000_RUN_SPEC.md`. Prior state: `TIER0_STATE_OF_PLAY.md`.

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

*To be appended after the run. Not yet run at the time of writing.*

# Fact sheet 06: chapter 5 section 1, "What Act I handed over, and the question it leaves"

**Section:** `report/act2_manifold.md` §4 (restructured 24 August 2026 into seven
sections), **section 1**. One paragraph, **no results**.
**Claims carried:** none.
**Figures:** none.

The question the section poses: a reservoir's readout sees a `T x N` state matrix, so
which part of the spectrum ends up where in that matrix?

Source key: **T0** = `TIER0_STATE_OF_PLAY.md`. **A2** = `report/act2_manifold.md`.
**SPINE** = `report/CROSS_ACT_SPINE.md` (structure only).

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| `sr_crit` **3.078** against **1.807 to 1.922** | the criticality scale Act I handed over | T0 §2.1, §3.1 | `eigenspectrum/results/scale_448/spectra_per_seed.parquet` | `1 / median_over_seeds(bulk95)` | 448 | not applicable | the same number as the gap ratio and as `1/bulk95`. Restated here, not re-derived |
| **2500 x 448** | the state matrix the readout actually sees, on the memory-capacity task | A2 §2.5, §2.6 finding 4. **Not in T0** | `covariance_spectra.parquet`; `readout_config.json` | post-warmup rows, **no bias column** | 448 | not applicable | `T` = 3000 with warmup 500 gives `T_eff` = 2500. MC has no bias column, so `eig_gram` has 448 entries; NARMA-10 and Lorenz carry one and have 449 |
| **N = 448** | the parcellation every figure in this chapter sits at | T0 §3.6, §3.12; A2 throughout | `results/scale_448/` | not applicable | 448 | not applicable | chapter 5 is entirely at N = 448; the N = 1000 replicate is Act I's S1 and Act III's F9 |
| **f = 0** | the sign condition | SPINE, "The primary variable and the intervention"; A2 §4 item 3.4 | not applicable | not applicable | 448 | not applicable | **entirely at `f` = 0.** No sign manipulation appears anywhere in this chapter; `f` enters once, in chapter 6 §6.3, as an intervention |
| the Perron mode | the object to be decomposed | SPINE, Act I "Hands on"; T0 §3.7 | not applicable | not applicable | 448 | not applicable | handed over as an **object**, not as an explanation. Act I gives no mechanism for why placement produces the gap |
| **spectral radius (sigma) is the primary variable** | the axis every headline claim is made along | SPINE, "The primary variable and the intervention" | not applicable | not applicable | 448 | nominal | it is the operating point, the thing neuromodulation, arousal and plasticity move in a real brain. **"The two axes" is reserved for the matching pair** (nominal sigma against `sigma*bulk95`) and must not be used for sigma against `f` |

## Forbidden phrasings for this section

- **"the two axes"** meaning sigma against `f`. In this project the phrase is an
  established term for the **matching** pair and stays reserved for it. Sigma is a primary
  variable and `f` is an intervention, which is a different relationship and gets
  different words.
- **Any result.** This section states what was handed over and poses a question.
- **"the gap keeps the Gram spectrum clear of the floor"** stated as something Act I
  showed. Section 4 measures it, and the link runs through section 3's common-mode
  account.
- **"compact bulk", "compressed bulk."**
- **Introducing `f`**, other than the one clause noting that this chapter is entirely at
  `f` = 0 and that `f` enters in chapter 6 §6.3.
- **"the biological cut"** for `f` = 0.

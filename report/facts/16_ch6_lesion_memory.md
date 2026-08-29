# Fact sheet 16: chapter 6 section 4, "Removing the common mode: memory"

**Section:** `report/CROSS_ACT_SPINE.md`, Act III, **§6.4** of the seven-section breakdown
added 28 August 2026. **This is where `f` enters the thesis**, once, as a lesion.
**Claims carried:** A3M.5, A3M.6 (`report/act3a_memory.md` §1); RM §1 contribution 3's
`f` half; T0 §1.1b, §3.7 and §3.8.
**Figures:** **F11, panel (a) across the whole `f` axis and panel (b)**, the other half of
the panel split of open flag 3. Hub-targeted inhibition has **no figure** and is prose.

**Extraction only.** Every number was read from the document named in its source cell.

Source key: **T0** = `TIER0_STATE_OF_PLAY.md` (rank 1). **RM** =
`ACTION_PLAN_JOURNAL_ROADMAP.md` §1. **FL** = `report/FIGURE_LIST.md`. **A3M** =
`report/act3a_memory.md`. **A3P** = `report/act3b_prediction.md`. **SPINE** =
`report/CROSS_ACT_SPINE.md` (structure only). A row whose source is not T0 is **not
TIER0-backed** and says so.

## Movement 1: the intervention, and why, stated once

**The argument for the lesion is that comparison alone cannot test the common-mode
account**, because every substrate at `f` = 0 has a Perron mode. Grading `f` is the only
manipulation in the thesis that removes the proposed cause and checks whether the effect
goes with it.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| Perron-Frobenius pins a non-negative matrix to an all-positive, hub-loaded leading eigenvector | why every substrate at `f` = 0 carries a common mode | T0 §3.9, §3.7 | not applicable | not applicable | 448 | not applicable | the dominant eigenvalue is **guaranteed real and positive**. This is why the account cannot be tested by comparing substrates: they all have one |
| grading `f` makes the spectrum **symmetric about zero** and grows the most negative eigenvalue **toward `lambda_1`** | what the lesion does to the operator | T0 §3.9; SPINE | not applicable | not applicable | 448 | not applicable | the period-2 branch becomes reachable at far lower sigma, which is **§6.5's** consequence and is named here only as the same manipulation |
| `\|mean_state\|` **0.016 / 0.015 / 0.018 / 0.024** at sigma = 6, `f` = 0.5 | the lesion measured: the common mode is gone | T0 §3.7 | `item2_f_extension_scale_448.parquet` + `item3_f_extension_nulls_scale_448.parquet` | absolute value per cell, then seed median | 448 | nominal | **two orders of magnitude** below the `f` = 0 values (0.759 / 0.949 / 0.959 / 0.989). At sigma = 2 the same column reads **0.004 / 0.001 / 0.001 / 0.001** against 0.114 / 0.532 / 0.586 / 0.593 |
| `f` in **11 values, 0 to 0.50 in steps of 0.05** | the grid the lesion is graded on | **Not in T0.** A3P §2.0 | `e01_jacobian_scale_448.parquet`; `item2_f_extension_scale_448.parquet` | per cell | 448 | nominal | 4 variants x 11 `f` x 29 sigma x 10 seeds x 3 draws. At `f` = 0 the three draws are literal duplicates; **above `f` = 0 they are not**, but the independent unit is still the seed |
| **`f` = 0 is what the instrument produces**; `f` > 0 is the missing half of the biology | the plausibility framing, stated once | SPINE, "The primary variable and the intervention" | not applicable | not applicable | 448 | not applicable | macro dMRI is non-negative because of the **measurement**, not because cortex is: tractography cannot represent sign, while real cortical circuits have inhibition. **Never "the biological cut"** |
| on the Dale axis, sign fraction and **non-normality co-vary**, unequally across variants | the scope limit on the placement arm of this section | T0 §6.5 | not applicable | not applicable | 448 | nominal | **Dale-arm claims are about node-wise inhibition, not sign fraction alone.** This is what keeps movement 4 a consequence rather than a second manipulation |

## Movement 2: nobody degrades, and the advantage closes because the nulls gain more

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| connectome MC **11.43 / 14.35 / 14.18**, change **+2.75** | MC at sigma = 6 at `f` = 0, 0.25, 0.5 | T0 §2.6 | `e03_frontier_scale_448.parquet` | seed median | 448 | nominal | **at sigma = 6**, supercritical. MC is bounded by `max_lag` = 50 (observed <= 16.0), so unlike `d_eff` it is **not ceiling-limited** |
| weight-permuted **5.02 / 13.64 / 13.60**, **+8.58** | the same for the placement control | T0 §2.6 | as above | as above | 448 | nominal | as above |
| degree-matching **4.11 / 13.43 / 13.19**, **+9.08** | the same | T0 §2.6 | as above | as above | 448 | nominal | as above |
| Erdős–Rényi **2.42 / 13.30 / 13.11**, **+10.69** | the same | T0 §2.6 | as above | as above | 448 | nominal | as above |
| advantage **+9.01 to +1.07** | the connectome minus Erdős–Rényi MC gap across `f` | T0 §2.6 | as above | difference of the seed medians above | 448 | nominal | **it falls solely because the nulls gain about four times what the connectome gains, from a much lower start.** The delta is never written without the four level pairs above it |
| peak MC over sigma is **flat in `f` and equal across variants (~15.4)** | that the peak was never where this lived | T0 §2.6 | as above | per-variant peak over sigma | 448 | nominal | the same shape as §6.2's peak parity, one axis over |
| `d_eff` is **excluded** from this comparison | why the lesion is read on MC | T0 §2.6 | not applicable | not applicable | 448 | nominal | `d_eff` is **ceiling-limited at N = 448 and reads flat across `f` for reasons that have nothing to do with `f`**; `climate_error` is excluded on its own grounds |
| **the wedge closes because the nulls catch up** | the restatement that replaces "extinguished by `f` ~ 0.15 to 0.20" | T0 §1.1b | as above | as above | 448 | nominal | **sign composition does not trade the connectome's memory away; it removes the handicap the nulls were under.** This is the **third** claim in the project to turn out to be "the null moved" |
| **+8.95** at `f` = 0 falling to **+0.50** at `f` = 0.50 | the same advantage on the phase-diagram grid | **Not in T0.** A3P §5 item 7's bridge paragraph | phase-diagram grid | supercritical advantage across `f` | 448 | nominal | **this is not T0 §2.6's +9.01 to +1.07** and the two must not be swapped (`GAPS.md` B16). Different populations and filters; the bridge paragraph is §6.6's |

## Movement 3: how much of the gap `bulk95` explains, as a controlled comparison

**A controlled comparison, not a correlation.** The correlation half of the same test does
not work and T0 §3.7 says its headline number must not be quoted.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| **26%**, median `\|gap\|` **6.42 to 4.75** | what matching on `sigma*bulk95` absorbs of the connectome-minus-ER MC gap at `f` = 0 | T0 §3.7 | `e03_mechanism_matched_scale_448.csv` | **median of the absolute difference over the swept range**, under each matching axis | 448 | sigma*bulk95 against nominal | the percentage travels with **both levels**: a ratio of two small numbers read alone is not a result |
| residual **~0.5** by `f` >= 0.2, a **9.5x** collapse | what `bulk95` fails to explain once the Perron mode is gone | T0 §3.7 | as above | as above | 448 | sigma*bulk95 | re-indexed on `x`, the **`f` = 0 curves stay separated** and the **`f` = 0.5 curves superimpose** |
| `bulk95` is a **partial** controller | the conclusion of the controlled comparison | T0 §3.7, §6.7, §1.4 | as above | as above | 448 | sigma*bulk95 | its explanatory power **depends on whether a Perron mode exists**. Sharper than the N = 1000 falsification test managed, which returned **inconclusive** |
| **+0.796 against -0.004** | the pooled supercritical correlation contrast | T0 §3.7 | `e03_mechanism_corr_scale_448.csv` | pooled supercritical | 448 | both | **MUST NOT BE QUOTED: it is confounding.** `\|mean_state\|` and `sigma*bulk95` are collinear by construction and the within-`f` Spearmans are near-identical (**0.959 against 0.956** at `f` = 0.15) |

## Movement 4: hub-targeted inhibition, as a consequence of where the mode is destroyed

**Not a separate result.** Hub-first is the most efficient way to destroy the Perron common
mode, so this is the placement-resolved face of the same rescue account. **Compress to one
paragraph if the section runs long.** No figure.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| connectome **11.43 / 11.43 / 11.43** against Erdős–Rényi **2.42 / 2.42 / 2.42** at `f` = 0 | absolute MC by inhibition placement (hub / stratified / periphery) | T0 §3.8 | Dale-axis capture | seed median at sigma = 6 | 448 | nominal | at `f` = 0 the three placements are the same reservoir, which is why the row is constant |
| connectome **14.88 / 13.94 / 12.94** against Erdős–Rényi **10.95 / 7.23 / 6.50** at `f` = 0.10 | the same at `f` = 0.10 | T0 §3.8 | as above | as above | 448 | nominal | **inhibiting the connectome's hubs raises the connectome's own memory, more than any other placement** (14.88 against periphery-first's 12.94) |
| connectome **15.58 / 15.57 / 14.20** against Erdős–Rényi **14.98 / 13.53 / 10.89** at `f` = 0.20 | the same at `f` = 0.20 | T0 §3.8 | as above | as above | 448 | nominal | at sigma = 6 **every variant is against the `d_eff` = N = 448 ceiling for `f` >= 0.2**, which is why the reading is on absolute MC |
| Erdős–Rényi **+8.5** against the connectome's **+3.4** | why the advantage closes fastest under hub-first | T0 §3.8 | as above | as above | 448 | nominal | **nothing collapses; the null moves.** The gains travel with the levels 2.42 to 10.95 and 11.43 to 14.88 |
| `f*` ordering **hub 0.087 < stratified 0.124 < periphery 0.164** | the placement ordering itself | T0 §3.8 | as above | contour where `dD` falls to 25% of its max | 448 | nominal | **real, and it reproduces under both hub definitions.** It is a **delta on a ceiling-limited metric**, which is why it is reported beside the absolute levels and never alone |
| Erdős–Rényi's `d_eff` range **172 against 75** at `f` = 0.1 | that the null was never a fixed reference | T0 §3.8 | as above | range across targetings | 448 | nominal | ER's own `d_eff` swings **more** across targetings than the connectome's |
| supercritical Dale minus edge **~0 for `f` >= 0.25**, **-25.8 at `f` = 0.15**, **-10.7 at `f` = 0.20** | the falsified mechanism, non-normality | T0 §3.5 | Dale and edge captures at matched `f` | differenced `dD` at matched `f`, sigma >= 3.05 | 448 | nominal | **non-normality does not buy supercritical memory; around `f` ~ 0.15 to 0.20 it costs.** Near criticality (sigma = 2) it is strongly positive and growing (**+18** at `f` = 0.20 up to **+62** at `f` = 0.40), and the hub-gating capstone is a **supercritical** result |
| Dale is about **2x as non-normal** as its nulls at matched `f`; edge mode is **exactly normal** at every `f` | the measurement behind the falsification | T0 §3.5 | as above | per cell | 448 | nominal | **report hub-gating without a mechanistic story attached** (RM §1, "what must NOT be claimed"): the empirical result is solid, its proposed mechanism was falsified |

## Forbidden phrasings for this section

- **"hub inhibition collapses memory."** **Nothing collapses; the null moves.** Write
  "hub-targeted inhibition closes the advantage fastest".
- **"negative weights trade the connectome's memory away", or any degradation reading.**
  In absolute terms **no substrate degrades**: supercritical MC rises with `f` for all
  four, the connectome by +2.75 and Erdős–Rényi by +10.69.
- **Any delta without its levels.** +9.01 to +1.07 travels with 11.43 / 2.42 and
  14.18 / 13.11; +8.5 against +3.4 travels with 2.42 to 10.95 and 11.43 to 14.88; the 26%
  travels with 6.42 to 4.75.
- **The pooled supercritical correlation contrast** (+0.796 against -0.004). Only the
  matched-axis residual adjudicates.
- **"`bulk95` is the ladder controller."** It is a **partial** controller whose power
  depends on whether a Perron mode exists.
- **A mechanistic story for hub-gating.** Non-normality was the proposed mechanism and it
  is falsified supercritically, which is where the result lives.
- **Treating hub-targeted inhibition as an independent controller or a separate result.**
  It is a consequence of where the common mode is destroyed.
- **"the biological cut"** for `f` = 0, and any framing in which `f` > 0 is a departure
  from biology rather than its missing half.
- **Any memory statement without its sigma.** Everything in this section is at
  **sigma = 6**, supercritical.
- **Reading `d_eff` across `f`.** It is ceiling-limited at N = 448 and reads flat across
  `f` for reasons that have nothing to do with `f`.
- **A curvature or trajectory-geometry account of memory**, and any graded straightness
  account anywhere.
- **Swapping T0 §2.6's +9.01 to +1.07 for the bridge paragraph's +8.95 to +0.50.**
  Different populations; see `GAPS.md` B16.

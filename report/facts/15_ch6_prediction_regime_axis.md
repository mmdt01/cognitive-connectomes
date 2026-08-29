# Fact sheet 15: chapter 6 section 3, "Prediction along the regime axis, at `f` = 0"

**Section:** `report/CROSS_ACT_SPINE.md`, Act III, **§6.3** of the seven-section breakdown
added 28 August 2026. Entirely at **`f` = 0**.
**Claims carried:** A3P.4 and A3P.9 (`report/act3b_prediction.md` §1); RM §1
contribution 4's `f` = 0 half and its scope limit.
**Figures:** **F13 panel (c)** for the collapse asymmetry, and **F13 panels (a, b) at
their `f` = 0 column** for the near-critical null result. **The decay result has no
figure**: `report/CROSS_ACT_SPINE.md` open flag 2, and it is stated inline.

**Extraction only.** Every number was read from the document named in its source cell.
**No Mackey-Glass data was inspected** (CONV working rule 6).

Source key: **T0** = `TIER0_STATE_OF_PLAY.md` (rank 1). **RM** =
`ACTION_PLAN_JOURNAL_ROADMAP.md` §1. **FL** = `report/FIGURE_LIST.md`. **A3P** =
`report/act3b_prediction.md`. **SPINE** = `report/CROSS_ACT_SPINE.md` (structure only).
A row whose source is not T0 is **not TIER0-backed** and says so.

## Movement 1: what the closed loop asks that the driven tasks do not

**Three sentences. The full protocol is the methods chapter's**; what §6.3 needs is the
distinction between a teacher-forced diagnostic and a free-running outcome, and the fact
that the two quantities it puts side by side come from different regimes.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| curvature and `sigma_eff` are **teacher-forced**; VPT and `climate_error` are **free-run** | which regime each quantity is measured in | **Not in T0.** A3P §2.6 finding 4 | `e01_jacobian_scale_448.parquet` | per cell | 448 | nominal | the section **must say this**, or a reader assumes curvature is measured on the thing being predicted. It is not a defect: the switch is a property of the operator and is visible under drive |
| `x -> tanh((W + Win*W_out)x)` | the operative map in the closed loop | T0 §3.11 | not applicable | not applicable | 448 | not applicable | it carries a **rank-3 readout term** that nothing in the repository computes; testing it needs a `W_out` the evaluator does not expose |
| VPT ceiling **16.3 Lyapunov times**, observed maximum **7.95** | that the horizon is not binding | T0 §2.6 | `e03_frontier_scale_448.parquet` | per cell | 448 | nominal | A3P §2.6 finding 3 gives the same as **16.301** = 600 x 0.03 x 0.9056 and **7.952**, i.e. **48.8% of ceiling**, with **zero of 38,280 cells** reaching it, so lengthening the horizon would buy nothing |
| **42%** of Lorenz cells are exactly **0** | that the VPT **floor** is live | T0 §2.6 | as above | share of cells | 448 | nominal | A3P §2.6 finding 3 gives **41.3%**, rising from **7.2%** at `f` = 0 to about **65%** at `f` >= 0.30 (`GAPS.md` B15). A zero means **all 20 windows failed at the first predicted step**, a strong statement, not a marginal one |
| threshold `\|\|pred - true\|\|_2 / rms_norm > epsilon`, `rms_norm` = **1.7321**, epsilon = **0.4** | what "valid prediction" means | **Not in T0.** A3P §2.6 finding 3 | as above | per rollout window, mean over 20 windows | 448 | nominal | 0.693 in z-scored units; `rms_norm` is sqrt(3), the z-scored three-dimensional series. **Protocol detail: the methods chapter carries it**, §6.3 does not |
| `climate_error` is **not reproducible per cell** | the limit that governs how the rollout may be read | **Not in T0.** A3P §2.6 finding 5 | `e2_free_run_scale_448.parquet` | seed medians only | 448 | nominal | the climate rollout is **3000 steps = 81.5 Lyapunov times**, so a machine-epsilon difference in BLAS reduction order decorrelates the trajectory. **Never quote a per-cell climate value, anywhere in the thesis** |
| **38,280** cells = 4 x 11 x 29 x 10 x 3; the independent unit is the **seed** | what a cell is and what it is not | T0 §2.3 for the rule; **A3P §2.0** for the arithmetic and the check | `e01_jacobian_scale_448.parquet` | one Lorenz evaluation per cell | 448 | nominal | at `f` = 0 the sign transform is the **identity**, so the three draws of a seed are **literal duplicates**: 100% of (variant, sigma, seed) groups return the same curvature and VPT. Every `f` = 0 statement rests on **~10 units per substrate, not 30** |

## Movement 2: prediction decays with the operating point while the geometry does not move

**This is `report/CROSS_ACT_SPINE.md` open flag 2: the result has no figure and is stated
inline.** The numbers exist in T0 §3.11's own table.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| connectome curvature **0.26 / 0.26 / 0.26 / 0.26 / 0.26** at sigma = 2, 4, 6, 8, 11.2 | the geometry, flat across the entire sweep | T0 §3.11 | `e01_jacobian_scale_448.parquet` | seed medians at `f` = 0 | 448 | nominal | **flat across the entire sweep.** The whole table is quoted, not the endpoints, because the claim is the flatness |
| connectome VPT **4.43 / 2.81 / 0.81 / 1.18 / 0.44** at the same sigma | prediction over the same sweep | T0 §3.11 | as above | as above | 448 | nominal | falls **~10x** while curvature does not move. Note the non-monotone step at sigma = 8 (1.18 above sigma = 6's 0.81), which the "~10x" summary smooths over |
| Erdős–Rényi curvature **0.26 / 0.26 / 0.26 / 0.27 / 1.70** and VPT **3.73 / 2.45 / 1.18 / 0.49 / 0.23** | the null's version of the same table | T0 §3.11 | as above | as above | 448 | nominal | Erdős–Rényi's curvature **does** move by sigma = 11.2 (1.70), which is the collapse of movement 3 showing up in the geometry column. The connectome's does not |
| **0.258 to 0.261** over sigma 2 to 11.2, VPT **4.43 to 0.44** = **10.0x** | the same result at the precision the gate reproduced it to | **Not in T0.** A3P §2.1 gate row | as above | seed medians at `f` = 0 | 448 | nominal | the gate's own restatement of T0 §3.11, quoted where three digits are wanted. T0's table is the published form |
| **no figure exists for this table** | the status of the result | SPINE open flag 2 | not applicable | not applicable | 448 | nominal | either stated inline or a figure proposed through the amendment procedure. **It is stated inline**: `FIGURE_LIST` has no slot for it and CONV working rule 3 forbids one that is not listed |

## Movement 3: collapse resistance far supercritically, and the near-critical null result

**The two are stated in the same breath and the radius is named every time.** T0 §2.6 says
in terms that written without the sigma they read as a contradiction and one of them will
be quoted wrongly.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| Erdős–Rényi **5 of 10 seeds**, connectome **0 of 10**, Fisher exact **p = 0.033** | collapse to period-2 at `f` = 0 | T0 §2.3, §2.6 | `item2_collapse_loci_scale_448.csv` | **seeds, not replicates** | 448 | nominal | **far supercritically, sigma ~ 7.6 to 8.0.** Never write "50% of replicates"; the independent unit is the seed |
| **sigma ~ 7.6 to 8.0** | where the asymmetry lives | T0 §2.3, §2.6 | as above | as above | 448 | nominal | **the onset is in sigma, not in `f`.** The phase diagram's reading that it emerges as an onset in `f` was an artifact of stopping the sweep at sigma = 6 |
| **+0.28 / -0.01 / +0.44**, none significant | the paired VPT margin at `f` = 0, **sigma = 2** | T0 §2.6 | `e03_frontier_paired_scale_448.csv` | paired within seed, at sigma = 2 | 448 | nominal | **near criticality there is no advantage at all at `f` = 0.** This row and the two above it are the pair T0 §2.6 says must always carry its sigma |
| **7 seeds against 5** at `f` = 0.05 | the same collapse count one grid step into `f` | T0 §2.3 | `item2_collapse_loci_scale_448.csv` | seeds | 448 | nominal | quoted only to show the `f` = 0 result is not a knife edge; **`f` > 0 is §6.4 and §6.5's**, so this is the furthest §6.3 goes |
| weight-permuted **3 of 10** and degree-matching **1 of 10** | the two middle rungs of the same collapse count | **Not in T0.** A3P's F13 caption only | as above | seeds | 448 | nominal | they sit between the connectome and Erdős–Rényi; the ordering **within the nulls** carries no claim |
| **n = 10 seeds**, Fisher p = 0.033 | the sample the biological half of the prediction claim rests on | T0 §2.3; SPINE open flag 5 | as above | seeds | 448 | nominal | **the weight it carries relative to its sample is stated in the text**, not left to inference. T0 §6.8: a two-sided Wilcoxon on 10 pairs cannot go below p = 0.00195, so declare the family narrowly and rest on effect sizes |
| at sigma = 11.2 the connectome reaches `x` = **3.58** while Erdős–Rényi reaches **~6.2** | why the matched axis cannot see this result | T0 §2.3 | `item2_f_extension_scale_448.parquet` | per seed | 448 | both | **the region where ER collapses and the connectome does not falls outside the matched-`x` overlap altogether.** The effective axis cannot see the generative advantage at its largest; the nominal axis can, and pays by leaving the bulk unmatched. **Report both** |

## Movement 4: what sets generation at `f` = 0, as a named open problem

**Three candidates, each ruled out on the data, and no fourth offered.** T0 §3.11 logs it
as a named open question rather than a third guess; A3P §5 item 6 assembles the bounding
evidence and adds no candidate.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| curvature **0.26 flat** while VPT falls **~10x** | candidate 1, **geometry**, ruled out | T0 §3.11 | `e01_jacobian_scale_448.parquet` | seed medians at `f` = 0 | 448 | nominal | **curvature is blind to the loss.** "Capacity is gated by which dynamical regime the manifold is in" is a statement about the **`f` > 0 counterfactual**, not about the biological substrate |
| Erdős–Rényi transitions at `sigma_eff` = **0.014**, against its own peak of **0.607**, on the **descending** branch (0.014 before the step, 0.011 after) | candidate 2, **the locator**, ruled out | T0 §3.10, §3.11 | `e01_threshold_table_scale_448.csv` | per transition | 448 | nominal | two orders of magnitude below its own peak. **And the connectome never breaks at `f` = 0 at all**: 0 of 10 seeds inside sigma <= 11.2. Whatever drives the `f` = 0 collapse, it is not an effective radius crossing anything |
| at sigma = 6 the connectome has **~4.7x** Erdős–Rényi's MC (**11.43** against **2.42**) and slightly **lower** VPT (**0.81** against **1.18**) | candidate 3, **memory doing the work**, ruled out | T0 §3.11 | `e03_frontier_scale_448.parquet`; `e01_jacobian_scale_448.parquet` | seed medians at `f` = 0, sigma = 6 | 448 | nominal | **the ordering is inverted.** A3P §5 item 6 quotes the same four numbers as 11.425 / 2.420 and 0.807 / 1.175. The ratio travels with both levels |
| `lambda_min(J)` = **-0.165**, scattered over **[-0.367, -0.044]**, on **9 transitions of 40 possible** | the exact-Jacobian measurement at `f` = 0 | T0 §3.11 | `e01_jacobian_scale_448.parquet` | **seed-level**, n as stated | 448 | nominal | at `f` > 0 the same quantity is tight at **-0.849 [-0.898, -0.769]** over **378** seed-level transitions. **Same measurement, different phenomenon.** A3P recomputes at the **draw** level (-0.881 [-0.922, -0.793], n = 1,069 for `f` > 0; n = 27 at `f` = 0), so **quote one unit or the other** |
| `lambda_min(J)` **never reaches -1** in either regime | that the break is not a local linear bifurcation | T0 §3.11 | as above | as above | 448 | nominal | **generation breaks while the fixed point is still linearly stable**, so the mean-field step was not the missing piece either. Keeping the gain heterogeneity **halves** the scatter (CV 0.152 against `sigma_eff`'s 0.304 on the same unit) |
| **no fourth candidate is offered** | the status of the section's close | T0 §3.11; A3P §1 A3P.9 and §5 item 6 | not applicable | not applicable | 448 | not applicable | **F17 is the nearest this thesis gets**: it measures the closed-loop trajectory directly, but it does not compute the closed-loop Jacobian and does not close the question. F17 itself belongs to §6.5 |

## Forbidden phrasings for this section

- **Any generative statement without its sigma.** The `f` = 0 advantage is **far
  supercritical** (sigma ~ 7.6 to 8.0); at sigma = 2 there is **no** advantage at `f` = 0.
  Written without the sigma the two read as a contradiction, and T0 §2.6 says so in terms.
- **"50% of replicates."** The unit is the **seed**: 5 of 10 against 0 of 10, on ~10
  independent units per substrate, not 30.
- **"the generative advantage emerges with `f`"** at `f` = 0. That reading was an artifact
  of stopping the sweep at sigma = 6. **The onset is in sigma.**
- **"generation tracks trajectory straightness"**, and any graded curvature or
  straightness account. At `f` = 0 the geometry does not move at all.
- **"capacity is gated by which dynamical regime the manifold is in"** stated of `f` = 0.
  It is scope-limited to **`f` > 0**, and this section is where the limit is measured.
- **"`sigma_eff` crosses 1 at the transition."** Falsified. `sigma_eff` survives as the
  best empirical **locator**, never a criterion or a law, and at `f` = 0 **it does not
  apply at all**.
- **"curvature is flat, so geometry does not matter."** At `f` = 0 capacity is lost **with
  the geometry intact**, and what sets generation there is a named open question.
- **Offering a fourth explanation**, or letting the `f` > 0 mechanism read as general.
  Three candidates are ruled out on the data and the question is left open.
- **Any per-cell `climate_error` value**, at any point in the thesis.
- **Quoting the two `lambda_min(J)` aggregation units against each other** (seed level
  against draw level), or `sigma_eff`'s **0.209** against the Jacobian's **0.152**.
- **Introducing `f` > 0 results.** The furthest this section goes into `f` is the `f` = 0.05
  collapse count, quoted to show the result is not a knife edge.

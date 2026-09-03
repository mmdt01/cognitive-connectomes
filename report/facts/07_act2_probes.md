# Fact sheet 07: chapter 5 section 2, "The probes, and what each can and cannot support"

**Section:** `report/act2_manifold.md` §4, **section 2**. Methods.
**Claims carried:** none. It fixes definitions, operating points and scope.
**Figures:** none.

Two things are stated **up front rather than in a limitations section**: Probe 2's scope,
and the `mean_state` sign convention. `d_eff` is **defined** here and **justified** in
section 5; running the two together is what makes the measure look assumed.

Source key: **T0** = `TIER0_STATE_OF_PLAY.md`. **A2** = `report/act2_manifold.md`.
**FL** = `report/FIGURE_LIST.md`. **CHK** = `report/checks/floor_sensitivity_check.md`.
**CONV** = `report/CONVENTIONS.md`.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| **two** substrates (`connectome`, `degree_rewire`), each recorded at **two** spectral radii per condition, **four distinct** across the capture | Probe 2's entire coverage | T0 §3.12 scope limit, as amended 2 September 2026; FL F4/F5 flag; A2 §1, §5 item 23 | `results/scale_448/manifold_alignment.parquet` | not applicable; the radius axis is **nested inside `condition`**, not crossed with it | 448 | nominal | **stated up front.** No Probe 2 statement may imply the four-variant ladder, and neither F4a nor F5 may be read as a ladder result. **The four radii are not the per-cell depth**: one shared canonical point at 0.9474 plus each condition's own supercritical point (3.0526 / 2.5263 / 1.2632), so no (condition, variant) cell holds more than **two**. This qualifier travels onto **every row sourced from Probe 2** |
| **3.0526** / **2.5263** / **1.2632** | the supercritical operating point of each condition (`human_empirical` / `human_empirical_signed` / `human_gaussian`) | A2 §2.3, F5 block. **Not in T0** | `manifold_alignment.parquet` | read from the data, one per condition | 448 | nominal | each condition is at **its own** operating point; the three are not one sigma |
| `\|mean_state\|`, absolute value taken **before** any aggregation | the common-mode proxy and its sign convention | T0 §3.12 gotcha; A2 §2.4, §4 item 2 | `saturation_diagnostics.parquet`; `item2_f_extension_scale_448.parquet` | **abs then median**, never median then abs | 448 | nominal | `mean_state` is **signed and its sign is arbitrary**, set by the input realisation, so seeds straddle zero. A signed median shrinks the connectome's sigma = 6 value from **0.759** to **0.638**; A2 §5 item 1 records that it also puts the weight-permuted null at **0.575**, below the connectome, inverting the ladder |
| `d_eff = sum_i g_i/(g_i + alpha)` | the ridge effective rank, defined | A2 F6 block, §2.6; T0 §3.6 for the derivative form | `covariance_spectra.parquet`, column `eig_gram` | exact sum over directions | 448 | not applicable | it is **exactly a sum of one weight per direction**, which is what licenses the area-as-count reading in section 5. Defined here, **justified in section 5** |
| ridge `alpha` = **1e-6** for MC | the readout floor, and the floor `d_eff` is measured against | T0 §3.3, §3.6; CHK provenance table; A2 §2.6 finding 1 | `human_mc/task_config.py:26`; `readout_config.json`; the `alpha` column of `covariance_spectra.parquet`; `probe3_deff.parquet` | one value, not a sweep, within MC | 448 | not applicable | **the same float, not two copies of one number**: `capture_cell` takes `alpha` from the same `params` dict it passes to the evaluator. CONV requires `alpha` be identical in `d_eff` and MC or the **+0.999** correspondence that licenses reading one through the other is void |
| NARMA-10 **1e-8**, Lorenz **1e-7** | the other two tasks' ridge alphas in the same file | CHK provenance and Task 2; A2 §2.6 finding 1. **Not in T0** | `covariance_spectra.parquet`, `alpha` column | one per task | 448 | not applicable | `closeout.py:floor_mass` takes `alpha` as a **default argument** and does not read the file's column. For MC the two are equal, so nothing in T0 §3.6 is affected; **any extension to another task must read the column** |
| **8,190 rows** = 3 tasks x 3 conditions x 7 variants x 13 spectral radii x 10 seeds | the covariance/Gram capture, a complete factorial with no holes | CHK Task 2. **Not in T0** | `results/scale_448/covariance_spectra.parquet` (27 MB) | one row per cell; zero duplicate keys | 448 | nominal | `eig_gram` is present, non-null, NaN-free and non-negative in **8,190 of 8,190** rows. Lengths are **448** for MC and **449** for NARMA-10 and Lorenz, which is the bias column those two designs carry |
| **13** spectral radii: 0, 0.4211, 0.8421, 1.0526, 1.2632, 1.5789, 2.0, 2.5263, 3.0526, 3.5789, 4.1053, 5.1579, 6.0 | the probe grid | CHK Task 2. **Not in T0** | as above | not applicable | 448 | nominal | **a different grid from Task B's** 21 points (0 to 8, step 0.4). Panels drawn from both grids say so |
| **520 cells** for MC on the ladder (4 variants x 13 radii x 10 seeds); **200** of them supercritical | what a four-variant radius-resolved figure can draw without a run | CHK Task 2 and Task 4. **Not in T0** | as above | not applicable | 448 | nominal | **no run needed, and none happened.** The coverage stops at sigma = 6 and has 13 points rather than 21, which bounds what a figure can draw but does not block it |
| **350 rows** = 7 variants x 5 sigma x 10 seeds | the Probe 3 filter | T0 §3.12(3); A2 §2.2; FL F6 row | `probe3_deff.parquet` at `task == "mc"`, `condition == "human_empirical"`, `spectral_radius >= 3.05`, `alpha == 1e-6` | not applicable | 448 | nominal | `alpha == 1e-6` is **the only alpha this file carries** at `spectral_radius >= 3.05` |
| **0.31 to 0.82** `d_eff` units | the per-lag Gram offset, MC design nested and `eig_gram` reported at `k` = 0 | A2 §2.5, §2.6 finding 3, §5 item 8. **Not in T0** | measured on four real cells at sigma = 3.0526 | worst measured shift from `k` = 0 to `k` = 50 | 448 | nominal | Weyl bounds it at `0 <= d_eff(0) - d_eff(k) <= k`, i.e. up to **50** units; measured it is **1.6% of that bound and 0.24% of the 75-to-413 ladder range**. The reported `d_eff` is a valid stand-in for every lag and the approximation cannot move the ordering |
| bounded by **1.0** `d_eff` unit, in practice **~1e-12** | `ridge_effective_rank` ridging the unregularised bias direction | A2 §2.6 finding 5, §5 item 9. **Not in T0** | `manifold.ridge_effective_rank` | not applicable | 448 | not applicable | **MC has no bias column, so nothing in this chapter is affected.** It matters only for `d_eff` quoted on NARMA-10 or Lorenz |
| **3.3e-16** | agreement of the time-centring implementation with `np.cov(rowvar=False)` | A2 §2.5, §2.6 finding 2. **Not in T0** | `manifold.covariance_eigenvalues` | exact comparison | 448 | not applicable | time-centring removes **each unit's mean over time**, not the mean over units. `gram_spectrum` correctly does **not** centre: the ridge solver inverts the un-centred `A^T A` |
| **pooled median over 3 tasks x 10 seeds (n = 30)** | the aggregation behind the 0.0001 quoted in section 3 | A2 §2.1, §5 item 6. **Not in T0**, which does not state the aggregation | `manifold_alignment.parquet` | pooled median, not the median of per-task medians | 448 | nominal | it is the **only** aggregation returning both published digits; the median of per-task medians gives 0.000098 (0.0001) but 0.002455 (0.0025), which is wrong. The **median is load-bearing**: one Lorenz seed at 0.0558 pulls the mean to 0.00217 against a random mean of 0.00232 |

## Forbidden phrasings for this section

- **Any ladder reading of Probe 2.** "the four substrates' basis alignment", "across the
  ladder the harmonics lead", or any sentence in which F4a or F5 stands for more than
  `connectome` and `degree_rewire` at two spectral radii per condition, four distinct
  across the capture.
- **"the manifold lives in low-frequency graph harmonics."** Withdrawn as an overstatement
  before the numbers that would tempt it even appear.
- **Justifying `d_eff` here.** The definition is a methods fact; the reason to prefer it is
  a result and belongs to section 5. Running them together is what makes the measure look
  assumed.
- **Median-then-absolute-value on `mean_state`**, or any aggregation statement that leaves
  the order unspecified.
- **"alpha was chosen at 1e-6 for `d_eff`."** It is the readout's own alpha, the same
  float, and that is the point.
- **"the Gram spectrum is a property of `W`."** It is a property of the reservoir **driven
  by this task at this operating point**. Nothing in this chapter derives it from `W`'s
  spectrum.
- **"compact bulk", "compressed bulk."**
- Any **graded curvature or trajectory-straightness** account, and any mention of
  curvature as a measured variable of this chapter. The temporal axis is flat here and is
  handed over as a boundary in section 7.

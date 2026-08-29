# Fact sheet 17: chapter 6 section 5, "Removing the common mode: generation"

**Section:** `report/CROSS_ACT_SPINE.md`, Act III, **§6.5** of the seven-section breakdown
added 28 August 2026. The same intervention as §6.4, the opposite consequence.
**Claims carried:** A3P.1, A3P.2, A3P.3, A3P.5, A3P.7, A3P.8
(`report/act3b_prediction.md` §1); RM §1 contribution 4's `f` > 0 half.
**Figures:** **F12**, **F13 panels (a, b)**, **F14**, **F17**.

**Extraction only.** Every number was read from the document named in its source cell.
**No Mackey-Glass data was inspected.**

Source key: **T0** = `TIER0_STATE_OF_PLAY.md` (rank 1). **RM** =
`ACTION_PLAN_JOURNAL_ROADMAP.md` §1. **FL** = `report/FIGURE_LIST.md`. **A3P** =
`report/act3b_prediction.md`. **SPINE** = `report/CROSS_ACT_SPINE.md` (structure only).
A row whose source is not T0 is **not TIER0-backed** and says so. **The whole of movement
4 (E2, the free-running rollout) is act-file-only**: T0 has no section for it.

## Movement 1: the switch appears once negative weights make the period-2 branch reachable

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| gain **> +1** gives a stable fixed point, **< -1** a stable period-2 orbit, **nothing stable between** | the one-dimensional map argument | T0 §3.9 | not applicable | not applicable | 448 | not applicable | each unit is `x -> tanh(gain*x + input)`. **There is no third stable option**, which is why curvature is not graded. Stated in full in §6.6; used here |
| **98%** of 38,280 cells in two spikes, **0.56%** between (**215** cells in [0.6, 2.2] rad) | curvature is a two-state step, not a dial | T0 §3.9, §3.10 | `e01_jacobian_scale_448.parquet` | share of cells, no row filter | 448 | nominal | the spikes are at **~0.25 rad** (smooth) and **pi (2.99 to 3.20 rad**, successive steps antiparallel). **Lorenz only** |
| **216** cells (**0.5643%**), two spikes **99.44%** | the same counts as recomputed by the reproduction gate | **Not in T0.** A3P §2.1 and §5 item 1 | as above | as above | 448 | nominal | a **one-cell** near-miss against T0's 215, stable under all four open/closed conventions; T0's 98% **understates** the two-spike share. Logged, not reconciled |
| binary bit **R2 = 0.364** against continuous curvature's **0.371** | that a single collapsed-or-not bit is worth nearly the whole geometry | T0 §3.10 | as above | over all cells | 448 | nominal | **the entire 0.25 to 3.14 rad range is worth 0.7 percentage points beyond the bit.** A3P recomputes the continuous value as **0.37049**, which rounds to **0.370** |
| within the smooth cluster **+0.145** (n = **15,866**); within the collapsed cluster, excluding the **67%** at the VPT floor, **-0.151** | the residual relation inside each regime | T0 §3.10 | as above | **Spearman** rank correlation | 448 | nominal | **+0.145 is the opposite sign to a graded account.** The pooled -0.78 was cluster mixing. The separator is **curvature = 1.0**, which sits inside the empty band, and the correlation is a **rank** correlation: as a Pearson it is **+0.006** (A3P §2.6 finding 1, **not in T0**) |
| binning on `sigma_eff` peaks at **-0.810** where the band is about **60/40** | that no binning isolates a graded path | T0 §3.10 | as above | per band | 448 | nominal | each band's correlation tracks its **cluster mixing proportion** and weakens toward both ends |
| **scope: `f` > 0 only** | the limit that travels with every sentence of this movement | T0 §3.10, §3.11 | as above | as above | 448 | nominal | at `f` = 0 curvature is flat at 0.26 while prediction falls ~10x, so **geometry gates nothing there**. §6.3 measured that; this section must not let the `f` > 0 mechanism read as general |

## Movement 2: prediction improves before it breaks, clearing the placement control

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| **+0.28 / -0.01 / +0.44**, none significant, at `f` = 0.00 | paired VPT margin against weight-permuted, degree-matching and Erdős–Rényi | T0 §2.6 | `e03_frontier_paired_scale_448.csv` | paired within seed, **sigma = 2** | 448 | nominal | **near-critical**, near every variant's own peak. At `f` = 0 the connectome is **level with every null** |
| **+1.46 / +0.28 / +1.82** at `f` = 0.20 | the same | T0 §2.6 | as above | as above | 448 | nominal | **two of three, not three of three**: degree-matching is +0.28 here (A3P §5 item 2) |
| **+1.71 / +1.62 / +2.20** at `f` = 0.25 | the same | T0 §2.6 | as above | as above | 448 | nominal | the first `f` at which the margin clears **all three** nulls |
| **+1.35 / +1.34 / +1.42** at `f` = 0.50 | the same | T0 §2.6 | as above | as above | 448 | nominal | quoted so the margin is not read as monotone in `f` |
| **+1.0 to +2.2 Lyapunov times**, the connectome the only substrate still predicting (**1.3 to 2.8** against **0.1 to 0.9**) | the headline of the generative advantage | T0 §2.6 | `e03_frontier_scale_448.parquet` | seed medians at sigma = 2 | 448 | nominal | **from `f` ~ 0.20 to 0.25.** RM §1 contribution 4 compresses this to "from `f` ~ 0.20" **with "over all three nulls" attached, and those two cannot both be true** (A3P §5 item 2; `GAPS.md` B17). Write **from `f` = 0.25**, or state the `f` = 0.20 exception |
| clearing the **weight-permuted** control | that this is a **weight-placement** effect, not a topological one | T0 §2.6 | `e03_frontier_paired_scale_448.csv` | paired within seed | 448 | nominal | the control freezes the weight draw, so clearing it is what licenses the word **placement** |
| **0.032 rad** | the curvature residual the matched-axis panel was contouring | T0 §2.6 | `e02_heatmap_*_extension*` | level over fully covered cells | 448 | sigma*bulk95 | **the generative arm was weak because the order parameter was wrong**, not because the effect was absent. Read as VPT it is real |
| usable range **~2x** under one threshold, **1.25 to 1.5x** at high `f` under another, and **reversed** at low `f` | that "usable range" is threshold-dependent | T0 §6.9 | `e03_frontier_live_window_scale_448.csv` | three stated criteria | 448 | nominal | **must not be quoted from the flattering end.** Under "VPT is not identically zero" the window looks ~2x the nulls'; under "usefully predicting" (>= 1 Lyapunov time, or >= 50% of that substrate's own peak) it is 1.25 to 1.5x at high `f` and **reverses at low `f`**, where degree-matching holds a Lyapunov time twice as far |

## Movement 3: what locates the transition, and what does not

**One paragraph and its figure.** F14 draws the §3.10 comparison; the exact Jacobian is a
different aggregation unit and is not drawn against it.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| `sigma_eff` median at transition **0.777**, IQR **0.162**, **CV 0.209** | the best locator of the three candidates | T0 §3.10 | `e01_threshold_invariance_scale_448.csv` | per **(variant, `f`)** cell, cells where fewer than half the seeds transition dropped (**n = 37**) | 448 | nominal | **CV is `IQR / median`**, not `sd / mean` (A3P §2.6 finding 2, **not in T0**). Under `sd/mean` the three read **0.256 / 0.540 / 0.589** and the ordering of the two **alternatives** reverses; the claim survives either definition but the statistic must be named |
| nominal sigma median **1.800**, IQR **1.200**, CV **0.667** | the first alternative | T0 §3.10 | as above | as above | 448 | nominal | `sigma_eff` is about **3x more invariant** |
| `sigma*bulk95` median **1.002**, IQR **0.747**, CV **0.746** | the second alternative, the linear negative-mode gain | T0 §3.10 | as above | as above | 448 | sigma*bulk95 | it brackets 1 far more often (**13 of 38**, median bracket **[1.018, 1.221]**), consistent with linear instability being **necessary but saturation delaying the transition** |
| **1 of 38** brackets contains 1; the transition sits at **0.77 to 0.90** | the first ground on which the unit crossing is falsified | T0 §3.10 | `e01_threshold_straddle_scale_448.csv` | per bracket | 448 | nominal | **draw no line at 1**; draw the 0.77 to 0.90 band |
| `sigma_eff` **folds**, and its maximum is **below 1 for every variant at `f` <= 0.20** (nulls until `f` >= 0.30) | the second, independent ground | T0 §3.10, §6.3 | `e01_sigma_eff_fold_scale_448.csv` | per (variant, `f`) | 448 | nominal | **a criterion whose claimed value is unreachable in a regime where the event still occurs is not a stability law.** On MC driven states it peaks at 0.57 to 0.63 |
| connectome **0.71 to 0.82**, weight-permuted **0.79 to 0.91**, degree **0.82 to 0.91**, Erdős–Rényi **0.87 to 0.95** | the variant-dependent offset, **pre-registered before fitting** | T0 §3.10 | `e01_threshold_table_scale_448.csv` | per-variant bracket over `f` | 448 | nominal | **ordered by spectral gap**, and the connectome is lowest **on the median**, not at every `f`. The prediction as it stood is on the record: the offset was predicted and confirmed, **the value of 1 was wrong** |
| `lambda_min(J)` **-0.849**, IQR **0.129**, **CV 0.152**, fraction of critical **0.85**; `sigma_eff` **+0.668**, IQR **0.203**, **CV 0.304**, **0.67** | the exact Jacobian as a better ruler | T0 §3.11 | `e01_jacobian_scale_448.parquet` | **seed-level transitions, n = 378**, no filter | 448 | nominal | **do not read 0.209 against 0.152**: different aggregation units. The comparison **within** this pair is the valid one. Keeping the gain heterogeneity halves the scatter, and `lambda_min(J)` still does not reach -1 |
| `sigma_eff = bulk95 * sigma * mean_gain` | what the locator is | T0 §3.10, §6.3; RM §2 | as above | averaged over units and time on **driven** states | 448 | nominal | **Lorenz-only. It must not cross panels.** Write **locator**, never **criterion** or **law** |

## Movement 4: the free-running rollout, both halves of its pre-registration

**Everything in this movement is act-file-only**: E2 is a new capture with no `TIER0`
section. **The pre-registered claim is reported in both halves and the refuted half at
length**, because the refutation is the more informative one.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| the registered claim: the connectome's free-run attractor **retains the true Lorenz climate to a higher `f`**, and **the collapse is a change of shape rather than a drift of scale** | the pre-registration, written by session 2 before the code existed | **Not in T0.** A3P §6.1; FL F17 row | not applicable | not applicable | 448 | nominal | quoted as written. The first clause is confirmed and the second refuted, and **both are reported** |
| **0.43** against the nulls' **0.14** at `f` >= 0.30 | first clause, **confirmed**: fraction of cells holding a faithful climate | **Not in T0.** A3P §6.1; FL F17 row | `e01_jacobian_scale_448.parquet` (**the frozen capture**, 30 cells per variant and `f`) | fraction of cells, sigma = 2 | 448 | nominal | **the scalar claim is quoted from the frozen capture**, which carries 30 cells per (variant, `f`) against the fresh capture's 10 |
| connectome **0.43**, weight-permuted **0.64**, degree-matching **0.66**, Erdős–Rényi **0.70** | the same ordering read as the fixed-point rate over `f` >= 0.20 | **Not in T0.** A3P §6.1 | `e2_free_run_scale_448.parquet` (fresh capture, **440 rows** = 4 x 11 x 10 at sigma = 2) | rate over cells | 448 | nominal | lower is better here, so the ordering is the same one; the two readings are on **different captures** and are not interchangeable |
| **229** of 440 below 0.05, **158** between 0.90 and 1.10, **11** anywhere between | second clause, **refuted**: `sd_ratio`, free-run spread over true spread, is **bimodal** | **Not in T0.** A3P §1 A3P.8 and §6.1 | as above | per cell | 448 | nominal | **the collapse is a loss of scale, not a distortion of shape.** "Wrong shape, right scale" describes **34 cells out of 440** |
| **206 of the 229** point-collapsed cells have climate error **> 2** | that the two order parameters agree | **Not in T0.** A3P §6.1 | as above | per cell | 448 | nominal | stated as a **count**, never as per-cell climate values, which are chaotic over the rollout's 81.5 Lyapunov times |
| **87%** of the 229 rest more than **3** z-scored units from the origin, median **11.5**, furthest **38.5** | where a collapsed free-run actually stops | **Not in T0.** A3P §3's F17 block and caption | as above | over the 229 collapsed cells | 448 | nominal | against a true attractor spanning about **+/-2.5** per coordinate, which is why those cells' climate errors run to 8 and beyond |
| **39 of 44** cells agree | the integrity gate against the frozen capture | **Not in T0.** A3P §6.1 | as above | **distributional**, which side of the faithful/collapsed separation each cell falls on | 448 | nominal | **never cell-for-cell**: the fresh capture is run in one pass at a pinned thread count and is **never spliced onto the frozen capture** |
| the fixed-point branch of the one-dimensional map, **observed in the closed loop** | why the refutation strengthens the chapter | **Not in T0** for the observation; T0 §3.9 for the map | as above | not applicable | 448 | not applicable | **two independent order parameters, one under teacher forcing and one under autonomous rollout, both two-valued.** This is the closed-loop half of §6.6's map argument |

## Forbidden phrasings for this section

- **"generation tracks trajectory straightness"**, and any graded straightness account.
  Within the smooth cluster the residual correlation is **+0.145**, the **opposite** sign;
  the pooled -0.78 was cluster mixing.
- **"`sigma_eff` crosses 1 at the generative transition."** Falsified on two independent
  grounds. Write **locator**, never **criterion** or **law**, and **draw no line at 1**.
- **Quoting `sigma_eff`'s CV 0.209 against the exact Jacobian's 0.152.** Different
  aggregation units; T0 §3.11 forbids it in terms.
- **Quoting 0.209 without naming the statistic.** It is **IQR / median**.
- **"the connectome predicts better from `f` ~ 0.20 over all three nulls."** At `f` = 0.20
  degree-matching is **+0.28**; the three-null statement starts at **`f` = 0.25**.
- **"the connectome's usable range is twice the nulls'."** Threshold-dependent, and it
  **reverses at low `f`** under any threshold meaning *usefully predicting*.
- **Any per-cell `climate_error` value.** Seed medians and rates only.
- **Letting the `f` > 0 mechanism read as general.** Everything in movements 1 to 3 is
  scope-limited to `f` > 0, and §6.3 measured what happens at `f` = 0.
- **Reporting only the confirmed half of E2's pre-registration.** The refuted half is
  reported at length, and it is the half that carries the map argument into the closed
  loop.
- **Reading E2's fresh capture and the frozen capture as one population.** 10 cells per
  (variant, `f`) against 30, and the integrity gate between them is distributional.
- **"the biological cut"** for `f` = 0.
- **Any generative statement without its sigma.** Movements 2 and 4 are at **sigma = 2**.

# Fact sheet 18: chapter 6 section 6, "One axis, two readouts"

**Section:** `report/CROSS_ACT_SPINE.md`, Act III, **§6.6** of the seven-section breakdown
added 28 August 2026. The unifying section, placed at the **end** of the chapter so the
claim is the conclusion of a causal test rather than a frame the reader must accept up
front.
**Claims carried:** A3P.6 (`report/act3b_prediction.md` §1); **RM §1 contribution 2**;
T0 §3.9.
**Figures:** **F16**. The bridge paragraph has **no figure**: NARMA-10 has no slot on
`report/FIGURE_LIST.md` and is not given one.

**Extraction only.** Every number was read from the document named in its source cell.

Source key: **T0** = `TIER0_STATE_OF_PLAY.md` (rank 1). **RM** =
`ACTION_PLAN_JOURNAL_ROADMAP.md` §1. **FL** = `report/FIGURE_LIST.md`. **A3P** =
`report/act3b_prediction.md`. **SPINE** = `report/CROSS_ACT_SPINE.md` (structure only).
A row whose source is not T0 is **not TIER0-backed** and says so.

## Movement 1: the map argument, now earned rather than asserted

**Earned because §6.4 and §6.5 showed both consequences following from one manipulation.**
The section states the argument; it does not introduce it as a premise.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| `x -> tanh(gain*x + input)`: gain **> +1** a stable fixed point, **< -1** a stable period-2 orbit, **nothing stable between** | the one-dimensional map that both readouts share | T0 §3.9 | not applicable | not applicable | 448 | not applicable | **there is no third stable option**, which is why curvature is a two-spike distribution rather than a graded quantity |
| negative eigenvalues bounded by roughly `bulk95*lambda_1`: **0.325 lambda_1** (connectome) against **0.55 lambda_1** (Erdős–Rényi) | why Perron-Frobenius pins a non-negative matrix to the fixed-point branch | T0 §3.9 | not applicable | not applicable | 448 | not applicable | zero diagonal forces trace = 0, so negative eigenvalues **must exist** but are subdominant. Grading `f` destroys the guarantee and the period-2 branch becomes reachable at far lower sigma |
| `\|mean_state\|` **0.95 to 0.99** for the nulls at sigma = 6 | the same fact read as a **liability for memory** | T0 §3.7, §3.9 | `item2_f_extension_scale_448.parquet` + `item3_f_extension_nulls_scale_448.parquet` | absolute value per cell, then seed median | 448 | nominal | the network synchronises into the mode, every unit does the same thing and readout dimensions are wasted. **At `f` = 0, sigma = 6** |
| a fixed point is smooth, and smooth is what closed-loop prediction needs | the same fact read as **protective for generation** | T0 §3.9 | not applicable | not applicable | 448 | not applicable | **one structural cause, two readouts with opposite preference.** That is why the two advantages *had* to occupy opposite regions of (`f`, sigma) |
| what is **measured**: the bimodality; the binary-bit **R2 = 0.364** against **0.371**; the `\|mean_state\|` ordering; the collapse loci; the two advantage regions | the evidence the argument rests on | T0 §3.9 | `e01_jacobian_scale_448.parquet`; `item2_collapse_loci_scale_448.csv`; the `f`-extension | as published in each | 448 | both | listed explicitly because the next row is the limit |
| what is **inference**: that a single leading-eigenvalue account generates both | the status of the argument | T0 §3.9 | not applicable | not applicable | 448 | not applicable | **consistent with everything measured, not yet a derivation.** The section says so in its own voice |
| and it does **not** explain the `f` = 0 collapse | the boundary of the argument, handed to §6.7 | T0 §3.9, §3.11 | as above | as above | 448 | nominal | at `f` = 0 Erdős–Rényi collapses at `sigma_eff` = **0.014**, two orders of magnitude below its own peak, and **something saturation-dependent is doing the work** |

## Movement 2: the crossing quantified, with its axis and its coverage

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| **(`sigma*bulk95` = 2.938, `f` = 0.153)** | where the memory and generative boundaries cross | T0 §2.3 | `e02_heatmap_boundaries_extension.csv` | contour level at **25% of the panel's global max over fully covered cells** (`f_star`) | 448 | sigma*bulk95 | **the first crossing inside full replicate coverage**, and the value of record. **Never quoted bare**, always with its axis and its coverage |
| **no crossing at all** on nominal sigma once the sweep passes sigma = 6 | the same object on the other axis | T0 §2.3 | `..._extension_nominal.csv` | `f_star` | 448 | nominal | the generative panel's true maximum sits at `f` ~ 0 to 0.05, sigma ~ 7 to 11, **which sigma = 6 never saw**; including it drops the generative boundary below the memory boundary throughout |
| **six** crossings: **2.943, 3.525, 3.598, 3.670, 3.743, 4.361** | what a reader who recomputes the boundaries will find | T0 §2.3 | as above | coarse linear interpolation on the union of the two boundaries' grids | 448 | sigma*bulk95 | the published **2.938** and this **2.943** are **the same object**: the 0.005 gap is the interpolation, not a competing estimate. A3P §5 item 4 solves the root and returns **(2.938, 0.1527)** |
| all-replicates coverage edge **`x_hi` = 3.58** at its minimum over `f`, running to **4.36** | the coverage mask | T0 §2.3, §6.10 | `e02_heatmap_coverage_extension.csv` | per `f`, minimum over `f` quoted | 448 | sigma*bulk95 | coverage now runs to **3.58 to 4.36** where it was **1.95 to 2.34**. Beyond it the boundary rests on a **`bulk95`-selected subsample** and is drawn but **must not be read quantitatively** |
| "only the first lies inside" does **not** hold on T0's own arithmetic | a disagreement carried, not resolved | **A3P §5 item 3.** T0 §2.3 states the opposite | as above | as above | 448 | sigma*bulk95 | **3.525 < 3.58**, so two lie inside the stated minimum edge; under the honest **per-`f`** edge **five of six** do. Neither reading gives one. What is defensible, and what F16 says, is that the published crossing is **first by a clear margin** (the next is 0.56 further out) and inside coverage under **both** conventions, and that crossings 2 to 5 span x = 0.22 and are **one oscillation**, not five features (`GAPS.md` B18) |
| memory boundary rises **0 to 0.19**, generative boundary falls **0.35 to 0.05**, the gap passing through zero at **2.94** | the two boundaries that produce the crossing | T0 §2.3 | as above | as above | 448 | sigma*bulk95 | the gap was **-0.162 and narrowing** at the old coverage limit; the old linear extrapolation put the crossing near **x ~ 3.5**, right in direction and **19% too far out** |
| raw global max **+2.849** from a cell backed by **1 replicate of 30**, against **+0.032** over fully covered cells: an **89x** difference | why the contour level is pinned to fully covered cells | T0 §2.3 | as above | level convention | 448 | sigma*bulk95 | the level **decides the boundary everywhere**. Three conventions (full-coverage cells, `n >= 15`, and the level pinned to the old `x <= 2.336` range) give the **identical** crossing; only the raw-global-max convention gives none |
| pinning the level back to sigma <= 6 returns **(sigma = 4.392, `f` = 0.1309)** against the published **(4.39, 0.130)** | that the pipeline reproduces the old nominal crossing exactly | T0 §2.3 | `..._extension_nominal.csv` plus a sub-panel re-run | as above | 448 | nominal | **what moved is the panel, not the method.** It comes from re-running the boundary operator on the sigma <= 6 **sub-panel**, so F16 marks it as a **quoted** number with a leader, never as a curve read off the extended file |
| under replicate resampling on the shared sigma <= 6 grid: sigma = **4.53 [3.85, 5.31]**, `f` = **0.136 [0.113, 0.158]**, failing to appear in **29%** of resamples | how sharp the old nominal crossing ever was | T0 §2.3 | as above | replicate resampling | 448 | nominal | **it was never a sharp feature even where it was first read** |
| `f_star_level_on_subrange` **does** give a nominal crossing, at **sigma = 4.382** | a correction to FL's F16 flag, in the safe direction | **Not in T0.** A3P §5 item 5. FL's F16 flag says all three conventions give none | `..._extension_nominal.csv` | the third level convention | 448 | nominal | a **0.01** agreement with the published 4.392, so it **strengthens** "what moved is the panel, not the method". The headline claim, **no nominal crossing on the `f_star` convention**, is untouched |
| the generative boundary is defined at **84 of 121** effective-axis points and **46 of 121** nominal | the boundaries have gaps | FL, F16 flag | as above | `f_star` is NaN where no contour exists | 448 | both | **break the line at the gaps; never interpolate across them** |
| `dx_collapse` (connectome minus ER) is **negative at 9 of 10 `f`**; depth bounded by the mode gap (**~2.6 rad**), location by the **0.4** sigma grid (**+/-0.16** in x) | why the matched-axis generative panel goes strongly negative | T0 §2.3 | `item2_collapse_loci_scale_448.csv` | bracketed at the sweep's own 0.4 resolution | 448 | sigma*bulk95 | **the generation-side face of the axis asymmetry, not a defect.** In nominal sigma the ordering is level or reversed. The one exception is `f` = 0.15, where the connectome's nominal margin (**3.2** in sigma, against **0 to 0.8** elsewhere) survives the change of axis |
| **neither axis is neutral** | the standing qualifier on the whole movement | T0 §1.1, §2.3 | not applicable | not applicable | 448 | both | nominal matching pins the **Perron root** and matched-bulk matching pins the **bulk**, and the mechanism under test is the Perron mode. **Report both, and rest the claim on surviving both** |

## Movement 3: the bridge from memory capacity through NARMA-10 to Lorenz

**One paragraph, and it is what makes the dissociation an axis rather than two tasks.**
**Every row of this movement is act-file-only**: T0 has no NARMA-10 section, and there is
**no figure**.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| the advantage peaks at sigma = **6.0** (MC), **4.0** (NARMA-10) and **2.0** (Lorenz VPT) at `f` = 0.25 | the trade-off varying continuously **along sigma** | **Not in T0.** A3P §5 item 7 | phase-diagram grid | connectome minus Erdős–Rényi, as a function of sigma | 448 | nominal | 6.0 is **the top of the grid**, so the MC location is a boundary value. The point is that it varies **along the spectral-radius axis contribution 2 is about** |
| median locations over the whole `f` axis: **6.0, 5.2, 2.0** | the same, aggregated over `f` | **Not in T0.** A3P §5 item 7 | as above | median over `f` of the per-`f` argmax | 448 | nominal | quoted with the per-`f` = 0.25 triple above, not instead of it |
| NARMA-10's supercritical advantage **+0.12 to +0.23** in NRMSE over `f` <= 0.15, decaying | that NARMA-10 does **not** interpolate on the `f` axis | **Not in T0.** A3P §5 item 7 | as above | supercritical, per `f` | 448 | nominal | it groups with **memory**, and the reason is mechanical: **NARMA-10 is teacher-forced**, so the reservoir is re-anchored every step and the regime switch has no closed-loop consequence |
| MC **+8.95** at `f` = 0 falling to **+0.50** at `f` = 0.50; Lorenz **~0** at `f` = 0, emerging from `f` = 0.20 (**+0.05 to +1.54**) | the two ends of the same `f` axis | **Not in T0.** A3P §5 item 7 | as above | as above | 448 | nominal | **the MC pair is not T0 §2.6's +9.01 to +1.07** (`GAPS.md` B16). **The discontinuity in this programme is at the closed loop**, not on the memory-to-prediction spectrum |
| Erdős–Rényi NRMSE **127.0, 22.8, 17.4** on three of ten seeds at `f` = 0.45, sigma = 6, against the connectome's **0.51 to 1.02** | the robustness note the bridge must carry | **Not in T0.** A3P §5 item 7 | as above | per seed | 448 | nominal | the seed median absorbs it, but the effect is a **robustness statement, not a capacity one**, the same shape as the Lorenz collapse-resistance result |
| MC **1e-6**, NARMA-10 **1e-8**, Lorenz **1e-7** | each task's own ridge alpha | **Not in T0.** A3P §5 item 7 | task configs | per task | 448 | not applicable | every bridge number is a **task-native performance metric at that task's own alpha**, so **no cross-task `d_eff` comparison at mixed alpha is made** |
| **three tasks, not four** | the scope of the bridge | **Not in T0.** A3P §5 item 7 | not applicable | not applicable | 448 | not applicable | Mackey-Glass is **not** in the bridge. A3P calls it "never run on the human substrate", while SPINE open flag 4 and RM §5 say the driven MG data **is** collected (`GAPS.md` B19). Either way it is a **schedule decision, not a gap in the argument**, and must be described that way |
| **2,800** captured rows against **2,000** in the design, plus an unregularised bias column | why no PR-versus-`d_eff` statement transfers to NARMA-10 | **Not in T0.** A3P §1 and §5 item 7 | NARMA-10 capture | row sets | 448 | not applicable | this is exactly why F6 is **MC-only**. The caveat cannot be dropped, so **the statement is not made** |

## Forbidden phrasings for this section

- **The crossing, quoted bare.** Always **(`sigma*bulk95` = 2.938, `f` = 0.153)**, always
  named as the **first crossing inside full replicate coverage**, always with the statement
  that the nominal axis has **none** past sigma = 6.
- **"only the first crossing lies inside coverage", stated as arithmetic.** It does not
  hold on either coverage convention. Write that the published crossing is **first by a
  clear margin and inside coverage under both conventions**, and that the rest are **one
  oscillation of a boundary resting on a selected subsample**.
- **Anything read off the uncovered region**, including the number and position of the
  further crossings.
- **Presenting the nominal crossing as read off the extended panel.** It is a quoted
  number from a sigma <= 6 sub-panel re-run.
- **"two controllers", "two mechanisms", or "the memory controller and the generative
  controller."** The claim is **one axis read out with opposite sign**.
- **Stating the map argument as a derivation.** It is consistent with everything measured
  and is **not yet a derivation**, and it does not explain the `f` = 0 collapse.
- **"generation tracks trajectory straightness"** and any graded curvature account.
- **"`sigma_eff` crosses 1."** It is a **locator**, Lorenz-only, and must not cross panels.
- **Letting the bridge read as "NARMA-10 sits between memory and prediction on every
  axis."** On sigma it interpolates; **on `f` it groups with memory**, because it is
  teacher-forced.
- **Transferring the PR-versus-`d_eff` claim to NARMA-10.**
- **Quoting the bridge's MC advantage (+8.95 to +0.50) as T0 §2.6's (+9.01 to +1.07)**, or
  the reverse.
- **"the connectome is a better reservoir."**

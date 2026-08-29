# Fact sheet 14: chapter 6 section 2, "Memory along the regime axis, at `f` = 0"

**Section:** `report/CROSS_ACT_SPINE.md`, Act III, **§6.2** of the seven-section breakdown
added 28 August 2026. Entirely at **`f` = 0**; `f` is not mentioned before §6.4.
**Claims carried:** A3M.1, A3M.2, A3M.3, A3M.4, A3M.5, A3M.7, A3M.8 (`report/act3a_memory.md` §1);
RM §1 contribution 3.
**Figures:** **F7** (the lead figure, and a workshop figure), **F10**, **F9**, and **F11
panel (a) at its `f` = 0 column only**, the panel split of open flag 3.

**Extraction only.** Every number was read from the document named in its source cell.

Source key: **T0** = `TIER0_STATE_OF_PLAY.md` (rank 1). **RM** =
`ACTION_PLAN_JOURNAL_ROADMAP.md` §1. **FL** = `report/FIGURE_LIST.md`. **A3M** =
`report/act3a_memory.md`. **SPINE** = `report/CROSS_ACT_SPINE.md` (structure only).
**CONV** = `report/CONVENTIONS.md`. A row whose source is not T0 is **not TIER0-backed**
and says so.

## Movement 1: the crossing: peaks lowest, retains most, and why the peak is unresolvable

**The section leads on the crossing, not on the peak.** F7's three panels are the pair
that makes it readable: (a) the curves, (b) the peak's unreadability, (c) the decay.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| **432.4** (lowest) at `sigma*bulk95` = **1.04** | the connectome's peak `d_eff` | T0 §1.2 | `taskB_extended_sweep_scale_448.parquet` | **per seed onto the common grid, then median across seeds** | 448 | sigma*bulk95 | **the lowest peak of the four**, and it is quoted only beside the retention figure. `bulk95` is per seed for the three nulls, so median-at-fixed-nominal-sigma is a different statistic and moves published values |
| **445.7** at 0.93, **444.7** at 0.91, **446.6** (highest) at 0.97 | weight-permuted, degree-matching and Erdős–Rényi peak `d_eff` | T0 §1.2 | as above | as above | 448 | sigma*bulk95 | the ladder ordering **within the nulls** is not a claim at any scale |
| **204.9** against **126.8 / 96.4 / 49.5** | `d_eff` at the top of the four-variant overlap | T0 §1.2 | as above | as above | 448 | sigma*bulk95 | the top of the overlap is **`x` = 2.599**, which is where every (variant, seed) curve still has coverage |
| **47%** against **28 / 22 / 11%** | fraction of its own peak retained at the top of the overlap | T0 §1.2; SPINE chain step 6 | as above | as above | 448 | sigma*bulk95 | a **four-fold spread**, and the result of the section. **The same retention ordering holds on the nominal axis**, where the Perron root rather than the bulk is matched, so it is not an artifact of the axis that hands the connectome the larger gap |
| **2.599** | the top of the four-variant overlap on the matched axis | T0 §1.2, §2.2 | as above | the interval every (variant, seed) covers, after clipping | 448 | sigma*bulk95 | quoted whenever a retention number is quoted; a retention figure without its `x` is not a quantity |
| peak `d_eff / N` **0.965** against **0.993 to 0.997** | how close each peak sits to the hard ceiling | **Not published as a column in T0 §1.2.** A3M §2.4 and F7's caption; the connectome's value is 432.4 / 448 | as above | as above | 448 | sigma*bulk95 | **T0 §3.2 has a different pair for the same argument** (connectome **0.961**, every null **>= 0.993**, taskA alpha sweep) and **body prose quotes T0's pair** (`GAPS.md` B2). Do not read the two as a series |
| **within 3.5% of the ceiling** | the statement that the peak is unresolvable at N = 448 | **Not in T0.** A3M claim A3M.2 and F7's caption. T0 §1.2 says "within a few percent" | as above | as above | 448 | sigma*bulk95 | the resolvable quantity is the **decay rate**. **A ceiling can clip curves but cannot manufacture a crossing** (T0 §1.2), which is why the decay result is robust to finite size in a way the peak result is not |
| peak `d_eff` is ceiling-limited **at any N** | the scope of the peak's unreadability | T0 §6.6 | `n1000_memory_scale_1000.parquet` | peak `d_eff/N` 0.971 to 0.999 at N = 1000 | 448 and 1000 | both | **no parcellation makes the peak comparison informative; read the decay region.** This is why §6.2 is a decay-region section |
| ordering **-1.00** subcritical, **-0.11** near peak, **+0.93** supercritical, spread **83 / 83 / 352** | where along sigma the ladder ordering lives | T0 §3.2 | `taskA_ordering_by_sigma.csv` | per-sigma ordering statistic, alpha = 1e-6 | 448 | nominal | report the ordering as a **curve in sigma**, not as a single thresholded number. The sigma >= 3.05 threshold is the connectome's own critical point and is **conservative**: the ordering already flips sign at **sigma = 2.53**, 0.52 below it |

## Movement 2: parity at the peak, with its interval, and the Aceituno reconciliation

**The reconciliation is placed here, on the panel that reproduces Aceituno, Yan & Liu's
ordering**, not deferred to the discussion. F10's alpha axis is what carries it.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| **-0.561** [-0.617, -0.506], **-3.6%**, p = 0.002 | paired peak MC difference, connectome minus Erdős–Rényi, at alpha = 1e-8 | T0 §3.4 | `closeout_peak_parity.csv` | paired per seed (same `Win`, same input series), 95% t-CI plus Wilcoxon | 448 | nominal, each substrate at **its own peak sigma** | never quoted as a point estimate alone; the interval is what forbids "always worst" |
| **-0.359** [-0.560, -0.159], -2.4%, p = 0.006 | the same at alpha = 1e-6 | T0 §3.4 | as above | as above | 448 | as above | as above |
| **-0.487** [-0.742, -0.232], -3.3%, p = 0.006 | the same at alpha = 1e-5 | T0 §3.4 | as above | as above | 448 | as above | as above |
| **-0.665** [-0.945, -0.385], -4.7%, p = 0.006 | the same at alpha = 7e-5 | T0 §3.4 | as above | as above | 448 | as above | as above |
| **-0.756** [-1.277, -0.234], -5.9%, p = 0.020 | the same at alpha = 1e-3 | T0 §3.4 | as above | as above | 448 | as above | as above |
| **5 of 5** alpha against Erdős–Rényi and the weight-permuted control, **1 of 5** against degree-matching | reliability of the peak deficit | T0 §3.4 | as above | CI excluding zero | 448 | nominal | **this is the parity claim.** The effect is **2 to 6%** and is not reliable against every null |
| at alpha = **1e-8**, peak MC orders **ER > degree > weight-permuted > connectome** | Aceituno, Yan & Liu's spread-beats-compact ordering, reproduced on our substrates | T0 §5 | `taskB_mc_alpha_peaks.csv` | per-variant peak MC over sigma | 448 | nominal | **reproduced, not contradicted**, and **not overturned at any alpha**. Nearest the pseudoinverse limit they optimise. **Spread wins at the peak; a large gap wins across the range** |
| **12.28** against **2.82** | supercritical MC, connectome against Erdős–Rényi, at alpha = 1e-6 | T0 §3.3, and T0 §5's Aceituno paragraph | `taskB_extended_sweep_scale_448.parquet` | supercritical median | 448 | nominal | **T0 §2.4's table gives 12.32 against 2.80 for the same pair** under its own filter (`GAPS.md` B14). CONV pairs "4.40 to 4.42" with "12.28 against 2.82", i.e. a ratio from one filter beside levels from the other |
| **+0.999 at every alpha** from 1e-8 to 1e-3 | the `d_eff` to MC correspondence | T0 §3.3 | `taskB_mc_alpha_correspondence.csv` | **seed-median statistic, n = 52** = 4 variants x 13 supercritical sigma | 448 | nominal | **provided alpha is raised in both places.** The cell-level version over the 520 supercritical cells is **+0.9973 to +0.9984**, i.e. **+0.998** (A3M §2.6 finding 7, **not stated in T0**). Name the unit beside the number |
| supercritical MC ladder ordering **+1.00 at every alpha** | that the alpha constraint does not bind | T0 §3.3 | as above | as above | 448 | nominal | which is what makes a five-alpha panel a robustness check rather than a fishing grid |
| the connectome's optimal sigma moves **2.4 to 3.6**; every null stays at **1.2 to 1.6** | the alpha-dependence of the optimum | T0 §3.3, §3.6 | as above | per-variant argmax over sigma at each alpha | 448 | nominal | the five alpha span **five orders of magnitude in four steps**. Chapter 5 explains the migration by each substrate's **interior** floor-mass minimum; §6.2 uses it, it does not re-derive it |

## Movement 3: the N = 1000 margin, compressed: protocol, both thresholds, ceiling, falsification

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| **12.32 / 7.34 / 4.61 / 2.80** and **13.93 / 8.98 / 5.09 / 3.15** | supercritical MC per variant at N = 448 and N = 1000 | T0 §2.4 | `n1000_memory_scale_{448,1000}.parquet` | seed medians over cells with `sigma >= ` **the connectome's** `sr_crit` | 448 and 1000 | nominal | the threshold is **3.078** at N = 448 and **3.985** at N = 1000, **applied to every variant**. The levels are quoted with the margin |
| margin **4.40 to 4.42**, a **+0.5%** change | connectome / Erdős–Rényi supercritical MC margin, connectome's threshold | T0 §2.4 | as above | ratio of the two seed medians above | 448 and 1000 | nominal | the **primary** reading, and it is the **conservative** one: it samples every null further above its own critical point, so it is the filter that flatters the connectome |
| **12.32 / 8.81 / 5.43 / 3.46** and **13.93 / 9.66 / 5.73 / 3.62**, margin **3.56 to 3.85** | the same under **each variant's own** `sr_crit` | T0 §2.4 | as above | seed medians over each variant's own supercritical range | 448 and 1000 | nominal | the margin **grows about 8%** here. **Report both.** "Scale-invariant" full stop is true of one filter only |
| `T` **3000 to 6000**, `T_eff/N` **5.58 to 5.50**, `alpha = lambda*trace(G)/N` with **lambda = 4.4845e-10** | the protocol that makes the two scales comparable | T0 §2.4, §2.5 | `n1000_memory_scale_{448,1000}.parquet` | alpha identical in `d_eff` and MC, two evaluator passes per cell | 448 and 1000 | not applicable | the design Gram is a **sample** covariance and its small-eigenvalue tail is what `d_eff` counts, which is what finite `T/N` distorts |
| control moved the N = 448 margin **4.35 to 4.40**, median per-cell change **0.32%** | that the reparameterisation is not what moved the result | T0 §2.4 | `n1000_memory_scale_448.parquet` | median over shared cells | 448 | nominal | **the control passed**, so any shift at N = 1000 is attributable to N |
| peak `d_eff/N` **0.971** (connectome) against **0.984 to 0.999** (nulls) | the ceiling, not escaped | T0 §2.4 | `n1000_memory_scale_1000.parquet` | **maximum over all cells** of `d_eff_norm` at the reparameterised alpha | 1000 | nominal | **a secondary prediction confirmed in advance.** Under a different rule on the same file (median over seeds at each sigma, then maximum) the four read 0.956 / 0.980 / 0.979 / 0.999; the conclusion holds under every rule (A3M §2.4) |
| peak `dD` **+199 to +613**; `dD/N` **0.445 to 0.613**; matched peak interior at `x` = **1.979** with coverage to **2.610** | the matched-axis peak at both scales | T0 §2.4 | `n1000_memory_scale_{448,1000}.parquet` | median over seeds of the per-seed difference | 448 and 1000 | sigma*bulk95 | the peak stays **interior**, which vindicates sigma_max = 10.4 over 8; the normalised advantage **grows** |
| ER - degree **-1.80 to -1.90**, p = **0.002** at both scales | the outcome side of the falsification test | T0 §2.4 | as above | paired | 448 and 1000 | nominal | degree stays above ER at both scales, **decisively and unchanged**, dropping the ladder Spearman against `bulk95` from **+1.00 to +0.80** |
| degree - ER = **+0.0142** [-0.0191, +0.0475], p = **0.16** | the predictor side, and why the test was flawed | T0 §2.4 | `spectra_per_seed.parquet` at `scale_1000` | paired over seeds | 1000 | not applicable | **the reversal the test rests on is not significant.** The pre-registration asserted the test was "on the sign, not the size" without checking the sign was established. **Correct classification: inconclusive**, because the *predictor* was noisy, not the outcome |
| **26%** absorbed, residual **~0.5** by `f` >= 0.2 | what the matched axis explains of the gap | T0 §3.7, §1.4 | `e03_mechanism_matched_scale_448.csv` | median absolute gap over the swept range | 448 | sigma*bulk95 | named here only as **the part of the controller question that can be answered**; the result itself is §6.4's, since it needs the `f` axis |

## Movement 4: what the gap buys at `f` = 0: the mechanism

**Chapter 5's common-mode and floor results are used, not re-established.** This movement
takes **F11 panel (a) at its `f` = 0 column only**; the panel's `f` axis is §6.4's.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| `\|mean_state\|` **0.114 / 0.532 / 0.586 / 0.593** at sigma = 2 | common-mode amplitude near criticality at `f` = 0 | T0 §3.7 | `item2_f_extension_scale_448.parquet` + `item3_f_extension_nulls_scale_448.parquet` | **absolute value per cell, then seed median** | 448 | nominal | at **`f` = 0**. Absolute value **before** the median, or the connectome reads 0.638 and a null falls below it |
| `\|mean_state\|` **0.759 / 0.949 / 0.959 / 0.989** at sigma = 6 | the same supercritically | T0 §3.7, §3.12 | as above | as above | 448 | nominal | the connectome is the **least** common-mode dominated substrate **despite carrying by far the largest Perron root**; the nulls sit with essentially every unit pinned near +1 |
| **0.114 to 0.759** against Erdős–Rényi's **0.593 to 0.989** | how the common mode grows with the operating point | SPINE, Act III; the endpoints are T0 §3.7's | as above | as above | 448 | nominal | this is the "what the gap buys" sentence: the leading mode can be **driven hard without the bulk following** |
| `bulk95` sets **where** a substrate crosses into supercriticality; the Perron common mode sets **how catastrophic** crossing is | the two spectral quantities, doing separate jobs | T0 §3.7 | not applicable | not applicable | 448 | both | the simulated operator is `sigma*W/\|lambda_1\|`, so the leading mode always has gain exactly sigma and the bulk has gain `sigma*bulk95` |
| **89.0%** against **11.4%**, `d_eff` **412.9** against **74.8** | chapter 5's floor account, used as the link to `d_eff` | T0 §3.6, amendment (e) | `covariance_spectra.parquet` | per-bin medians / medians over the 50 supercritical cells | 448 | nominal | **used, not re-established.** Erdős–Rényi's low absolute floor sensitivity is **degenerate**: per unit of surviving dimensionality it is the **most** floor-sensitive substrate, losing **29.1%** of `d_eff` per decade of alpha against the connectome's **5.6%** |
| negative eigenvalues bounded by roughly `bulk95*lambda_1`: **0.325 lambda_1** against **0.55 lambda_1** | why a non-negative matrix is pinned to the fixed-point branch | T0 §3.9 | not applicable | not applicable | 448 | not applicable | zero diagonal forces trace = 0, so negative eigenvalues **must exist** but are subdominant. This is the map argument's premise and it is stated in full in §6.6 |
| **+0.796 against -0.004** | the pooled supercritical correlation contrast | T0 §3.7 | `e03_mechanism_corr_scale_448.csv` | pooled supercritical | 448 | both | **MUST NOT BE QUOTED.** `\|mean_state\|` and `sigma*bulk95` are collinear by construction and the within-`f` Spearmans are near-identical (0.959 against 0.956 at `f` = 0.15). Only the matched-axis residual adjudicates |

## Movement 5: the one-line version, and what it costs to say

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| "the connectome does not make memory better; non-negativity makes it worse for everyone; the connectome's gap makes it least worse" | the defensible one-liner | T0 §3.7; RM §1 contribution 3 | not applicable | not applicable | 448 | not applicable | it is a **rescue from Perron domination, not a capacity gain**. The costs are the two rows below and they are stated in the same paragraph |
| peak deficit **2 to 6%**, reliable against two nulls of three | the first cost of the one-liner | T0 §3.4 | `closeout_peak_parity.csv` | paired per seed | 448 | nominal | say **parity**, never "always worst" and never "deficit" |
| Aceituno's ordering **reproduces exactly at alpha = 1e-8** | the second cost | T0 §5 | `taskB_mc_alpha_peaks.csv` | per-variant peak MC | 448 | nominal | **our substrate loses at the thing the field optimises for**, and the section says so rather than letting a reviewer find it. The answer is biological: the operating point is not a free parameter evolution can pin |
| **evolution cannot choose `f`** | why resistance to Perron domination is the only property available to select on | T0 §3.7 | not applicable | not applicable | 448 | not applicable | a structural connectome is non-negative **by construction**. This is the sentence that hands §6.4 its motivation without introducing `f` here |

## Forbidden phrasings for this section

- **"always worst."** The peak deficit is **2 to 6%** and is not reliable against
  degree-matching (1 of 5 alpha). Write **parity at the peak**.
- **Any peak-capacity claim in either direction.** At N = 448 the peak is not resolvable,
  and it is ceiling-limited at any N. The one thing said about the peak is parity, and it
  comes with a CI.
- **"the connectome is a better reservoir."** It is not, at the peak, and this section is
  where the data says so.
- **"the connectome is subcritically worse than ER."** Write **parity below criticality,
  advantage above**, with the axis named.
- **"the supercritical memory margin is scale-invariant"**, full stop. True on the
  connectome's-threshold filter (4.40 to 4.42) and false on each variant's own
  (3.56 to 3.85). Both are drawn.
- **"`bulk95` is the ladder controller."** The N = 1000 falsification test came back
  **inconclusive**, and inconclusive because the *predictor's* own ordering is not
  significant (p = 0.16), not because the outcome was noisy.
- **The pooled supercritical correlation contrast** (+0.796 against -0.004). T0 §3.7 says
  it must not be quoted; it is confounding.
- **Any statement about memory without its sigma.** The memory advantage is
  **supercritical**; the generative advantage over the nulls is near-critical and absent at
  `f` = 0. Without the sigma the two read as a contradiction.
- **Introducing `f`.** The one permitted mention is that this section is entirely at
  `f` = 0 and that the manipulation arrives in §6.4. **Nobody-degrades, the null-catch-up
  and hub-targeted inhibition are §6.4's** and must not be previewed with numbers here.
- **"hub inhibition collapses memory."** Nothing collapses; the null moves. The result is
  §6.4's in any case.
- **A curvature or trajectory-geometry account of memory.** That axis is the prediction
  arm's, and it does not move at `f` = 0 anyway.
- **"compact bulk", "compressed bulk."**
- **Reading T0 §3.2's peak `d_eff/N` pair against F7's.** Different source, different
  filter; body prose quotes T0's.

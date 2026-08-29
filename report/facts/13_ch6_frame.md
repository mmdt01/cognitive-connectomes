# Fact sheet 13: chapter 6 section 1, "What is being asked, and along which axis"

**Section:** `report/CROSS_ACT_SPINE.md`, Act III, **§6.1** of the seven-section breakdown
added 28 August 2026. **No results.**
**Claims carried:** none. Everything below is restated from chapter 3 or chapter 5, or is
an address rather than a result.
**Figures:** none. F3 is chapter 3's and its argument is carried forward, not re-drawn.

**Extraction only.** Every number was read from the document named in its source cell.
Nothing was recomputed, nothing was run, and no parquet was opened.

Source key: **T0** = `TIER0_STATE_OF_PLAY.md` (rank 1, canonical for numbers).
**RM** = `ACTION_PLAN_JOURNAL_ROADMAP.md` §1. **SPINE** = `report/CROSS_ACT_SPINE.md`
(structure only, explicitly not canonical for numbers). **FL** =
`report/FIGURE_LIST.md`. **CONV** = `report/CONVENTIONS.md`. **A2** =
`report/act2_manifold.md`. **A3M** = `report/act3a_memory.md`. **A3P** =
`report/act3b_prediction.md`. A row whose source is not T0 is **not TIER0-backed** and
says so.

**Three qualifier classes bind every sheet in this chapter and are not repeated row by
row where the row's own qualifier already carries them:** the **axis** (nominal or
`sigma*bulk95`, and what it holds fixed), the **spectral radius** (memory's advantage is
supercritical, the generative advantage over the nulls is near-critical, the `f` = 0
collapse asymmetry is far supercritical), and **levels beside every margin or ratio**.

## Movement 1: what chapter 5 handed over

**Restated, not re-established.** The mechanism paragraph of §6.2 uses these; it does not
re-derive them.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| `\|mean_state\|` **0.759** against **0.949 to 0.989** | common-mode amplitude, the substrate least dominated by its own Perron mode | T0 §3.7, §3.12; SPINE chain step 2 | `item2_f_extension_scale_448.parquet` + `item3_f_extension_nulls_scale_448.parquet`; `saturation_diagnostics.parquet` | **absolute value per cell, then seed median** | 448 | nominal | at **sigma = 6, `f` = 0**. A signed median shrinks the connectome's value to 0.638 and puts a null below it |
| **89.0%** against **11.4%** | directions more than a decade clear of the ridge floor | T0 §3.6 amendment (e) of 25 August 2026, sourced to `report/checks/floor_sensitivity_check.md` §5.1 | `results/scale_448/covariance_spectra.parquet` | per-bin median over the **50 supercritical cells**, zero-stripped, as a percentage of all 448 directions | 448 | nominal | supercritical (`spectral_radius >= 3.05`), MC, alpha = 1e-6. The four per-bin medians **do not sum to 100** (connectome 102.1%). Quoted **as a pair** |
| `d_eff` **412.9** against **74.8** | usable dimensionality supercritically | T0 §3.6; SPINE chain step 4 | `covariance_spectra.parquet` | median over 50 supercritical cells | 448 | nominal | **radius-dependent**: a property of a substrate **at an operating point**, which is what lets chapter 6 read the same axis twice |
| **+0.998** | `d_eff` against measured MC, pooled within-regime | T0 §3.12(3); SPINE chain step 5 | `probe3_deff.parquet` | pooled over **n = 350 cells** | 448 | nominal | the seven-rung, median-per-variant statistic is **+1.000** against PR's **+0.107**; the pooled pair is **+0.998** against **+0.308**. **Quote one aggregation unit or the other, never one number from each** |
| `sr_crit` **3.078** against **1.807 to 1.922** | the criticality scale each substrate brings with it | T0 §2.1, §3.1 | `eigenspectrum/results/scale_448/spectra_per_seed.parquet` | `1 / median_over_seeds(bulk95)` | 448 | not applicable | the same number as the gap ratio and as `1/bulk95`. It is what makes the second matching axis available at all |
| curvature **0.261 rad** (connectome) and **0.263 rad** (Erdős–Rényi) | the temporal axis of the manifold, flat at `f` = 0 | **Not in T0.** A2 §1 and §5 item 15 only | this act's Probe 1 capture, 36,540 cells | seed median over the whole sigma = 0 to 6 sweep | 448 | nominal | handed over as a **boundary, not a result**; maximum 0.26 for both. §6.3 is where it becomes an open problem, not a reversal |

## Movement 2: the two demands the chapter puts to the substrate

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| **MC** primary, NARMA-10 and Mackey-Glass corroborating | the memory demand and the task that carries it | FL, claim-to-primary-task mapping | not applicable | not applicable | 448 | not applicable | declared **before any data was inspected**, so "there is always a task where it holds" cannot be said. Mackey-Glass corroborates **MC**, not Lorenz, because the implemented task is teacher-forced |
| **Lorenz** primary, **no corroborating task** | the prediction demand and the task that carries it | FL, claim-to-primary-task mapping | not applicable | not applicable | 448 | not applicable | closed-loop generation, the regime switch and the resistance margin rest on Lorenz alone |
| **MC + Lorenz jointly**, no out-of-sample test | the demand the unifying section makes | FL, claim-to-primary-task mapping; RM §1 contribution 2 | not applicable | not applicable | 448 | not applicable | stated in §6.7 rather than left to the discussion. It rests on F16 plus the joint reading of F7 and F13 |

## Movement 3: the operating-point axis, and the two matching axes carried forward

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| `sigma*W/\|lambda_1\|` | the operator actually simulated | T0 §1.1 | definition; realised in `e02_panel.parquet` | not applicable | 448 | both | its spectral radius is **exactly sigma for every variant**, guaranteed by the normalisation; its bulk radius is `sigma*bulk95` |
| nominal sigma | matching axis 1 | T0 §1.1 | as above | not applicable | 448 | nominal | holds the **spectral radius** (the Perron root) fixed and lets the bulk vary. **Not neutral**, in the opposite direction to the matched axis |
| `sigma*bulk95` | matching axis 2 | T0 §1.1 | as above | **per seed, from the cell file's own `bulk95` column** | 448 | sigma*bulk95 | holds the **bulk radius** fixed and leaves the Perron root **deliberately unmatched**. Since the mechanism under test *is* the Perron mode, this axis hands the connectome more of the proposed cause |
| **1.7x larger Perron root** at the matched point | what the matched axis gives away | T0 §1.1 | `e02_panel.parquet` | at `x` = **1.949** the connectome sits at **sigma = 6.0** against Erdős–Rényi's **sigma = 3.54** | 448 | sigma*bulk95 | the levels travel with the ratio. This is the sentence that makes "neither axis is neutral" concrete |
| **+343.3** at sigma = **4.47** and **-217.4**, against **+196.5** at `x` = **1.949** and **-24.0** | peak and most-negative `dD` on the two axes | T0 §2.2 | `e02_panel.parquet`, `e02_axis_summary.csv` | median over seeds of the **per-seed difference** | 448 | both, one pair each | **carried forward from chapter 3, not re-derived.** Never quote one axis's pair without the other's, and never write "89% an artifact of nominal-sigma matching" |
| `bulk95` is a **function of `f`** and is **per seed** for the three resampling nulls | why the matched axis is a per-seed reindex | CONV, numerical conventions; FL F7 flag | `item2_f_extension_*` / `item3_f_extension_*` | interpolate each seed's curve onto the common grid, **then** take the median | 448 | sigma*bulk95 | it spreads **0.41 to 0.61** across ten degree-rewire seeds; the connectome's is one constant, so **the connectome row cannot reveal an aggregation defect** |
| **spectral radius (sigma) is the primary variable** | the axis every headline claim is made along | SPINE, "The primary variable and the intervention" | not applicable | not applicable | 448 | both | it is the operating point, the thing neuromodulation, arousal and plasticity move in a real brain. **"The two axes" is reserved for the matching pair** and must not be used for sigma against `f` |
| **`f` is an intervention, not a peer**, introduced in §6.4 | the scope statement this section closes on | SPINE, "The primary variable and the intervention" | not applicable | not applicable | 448 | not applicable | **`f` = 0 is what the instrument produces**, since tractography cannot represent sign; it is not "the biological cut". `f` > 0 is the missing half of the biology |

## Movement 4: the orientation table: the address of every result in the chapter

**This table is an assembly of addresses, not a result.** Every cell is sourced below; no
document carries the table itself (recorded in `GAPS.md` section A). Its purpose is that
two of these addresses read as a contradiction if the radius is dropped, which T0 §2.6
warns about in those words.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| memory advantage: **MC / `d_eff`**, `f` = **0**, **supercritical**, both axes | address of §6.2's headline | T0 §1.2, §2.4 | `taskB_extended_sweep_scale_448.parquet`; `n1000_memory_scale_{448,1000}.parquet` | per seed then across seeds (`d_eff`); seed medians over the supercritical range (MC) | 448 and 1000 | both | supercritical means `sigma >= 3.078` (the connectome's `sr_crit`) or each variant's own; the retention figure is read **at the top of the overlap, `x` = 2.599** |
| peak parity: **MC**, `f` = **0**, **each substrate at its own peak sigma**, nominal | address of §6.2's parity result | T0 §3.4 | `closeout_peak_parity.csv` | paired per seed, 95% t-CI plus Wilcoxon | 448 | nominal | the peak is **not** a supercritical statement; it is each substrate's own optimum, and the effect is **2 to 6%** |
| generative advantage over the nulls: **Lorenz VPT**, `f` from **0.20 to 0.25**, **sigma = 2**, nominal | address of §6.5's headline | T0 §2.6 | `e03_frontier_scale_448.parquet`, `e03_frontier_paired_scale_448.csv` | paired within seed | 448 | nominal | **near-critical**, at sigma = 2, near every variant's own peak. **At `f` = 0 this address shows no advantage at all** (+0.28, -0.01, +0.44, none significant) |
| `f` = 0 collapse asymmetry: **Lorenz**, `f` = **0**, **sigma ~ 7.6 to 8.0**, nominal | address of §6.3's resistance result | T0 §2.3 | `item2_collapse_loci_scale_448.csv` | **seeds**, not replicates: 10 independent units per substrate | 448 | nominal | **far supercritical.** Read against the row above without the sigma the two are a contradiction, which is exactly what T0 §2.6 says will happen |
| the crossing: **(`sigma*bulk95` = 2.938, `f` = 0.153)** | address of §6.6's unifying result | T0 §2.3 | `e02_heatmap_boundaries_extension.csv` | contour level taken over **fully covered cells** (`f_star`) | 448 | sigma*bulk95 | the **first crossing inside full replicate coverage**; **absent on the nominal axis** once the sweep passes sigma = 6. Never quoted bare |
| the `f` = 0 decay: **Lorenz**, `f` = **0**, **sigma 2 to 11.2**, nominal | address of §6.3's open problem | T0 §3.11 | `e01_jacobian_scale_448.parquet` | seed medians | 448 | nominal | curvature **0.26 flat** while VPT falls **4.43 to 0.44**. **This result has no figure** (open flag 2) |
| the lesion: **MC**, `f` **0 to 0.5**, **sigma = 6**, nominal | address of §6.4 | T0 §2.6, §3.7 | `e03_frontier_scale_448.parquet`; `e03_mechanism_matched_scale_448.csv` | seed medians at sigma = 6 | 448 | nominal, with the matched axis as the controlled comparison | every level is quoted with its delta: **11.43 to 14.18** against Erdős–Rényi's **2.42 to 13.11** |

## Forbidden phrasings for this section

- **Any result.** This section states what was handed over, what is being asked, and where
  each answer lives. The first number that is an outcome belongs to §6.2.
- **"the two axes"** meaning sigma against `f`. The phrase is reserved for the matching
  pair, nominal sigma against `sigma*bulk95`. Sigma is a primary variable and `f` is an
  intervention, and they get different words.
- **"the biological cut"** for `f` = 0 against `f` > 0. `f` = 0 is what the instrument
  produces; `f` > 0 is the missing half of the biology.
- **Introducing `f` as a second axis of the chapter**, or before §6.4, other than the one
  sentence flagging that §6.2 and §6.3 are entirely at `f` = 0 and that a manipulation
  arrives in §6.4.
- **Re-deriving the two-axis argument.** It is chapter 3's, contribution 5's, and F3's.
  Carrying it forward is the instruction; restating its derivation is not.
- **"89% an artifact of nominal-sigma matching."** Ruled out in T0 §1.1's own words. Write
  the deficit as **present at matched spectral radius (-217.4) and absent at matched bulk
  radius (-24.0)**, with what each axis holds fixed.
- **"the connectome is subcritically worse than ER."** Write **parity below criticality,
  advantage above**, and name the axis.
- **Any margin without its levels.** 4.40 to 4.42 travels with 12.28 against 2.82; the
  1.7x Perron root travels with sigma = 6.0 against 3.54.
- **"compact bulk", "compressed bulk."** The absolute bulk is everyone's; write "large
  spectral gap".
- **"the connectome is a better reservoir."** It is not, at the peak.

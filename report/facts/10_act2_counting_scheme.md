# Fact sheet 10: chapter 5 section 5, "Which counting scheme sees it"

**Section:** `report/act2_manifold.md` §4, **section 5**.
**Claims carried:** A2.4, A2.5. **Contribution 6.** **Chain step 4**: clear of the floor to
usable dimensionality.
**Figure:** F6 (a, b, c).

**The range comes first, because the range is the mechanism.** PR's failure is a
**consequence of section 4**, not a separate finding: the ridge floor sits ten orders of
magnitude below the leading variance, so hundreds of directions clear it while carrying
almost none of the variance.

Source key: **T0** = `TIER0_STATE_OF_PLAY.md`. **A2** = `report/act2_manifold.md`.
**FL** = `report/FIGURE_LIST.md`. **CHK** = `report/checks/floor_sensitivity_check.md`.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| **5.5-fold** | how far `d_eff` moves across the seven substrates | T0 §3.12(3) | `results/scale_448/probe3_deff.parquet` | per-variant medians over 50 supercritical cells each | 448 | nominal | **the range is the argument.** A2 §2.2 recomputes 5.52-fold |
| **75 to 413** of N = 448 | the `d_eff` range across the seven rungs | T0 §3.12(3) | as above | as above | 448 | nominal | A2 §2.2 recomputes 74.769 to 412.940. Quoted with "of N = 448" |
| **16%** | how far PR moves across the same seven substrates | T0 §3.12(3) | as above | as above | 448 | nominal | A2 §2.2 recomputes 16.2%. **Quoted against the 5.5-fold as the same sentence's other half** |
| **1.19 to 1.38** | the PR range across the seven rungs | T0 §3.12(3) | as above | as above | 448 | nominal | A2 §2.2 recomputes 1.1895 to 1.3821 |
| **+1.000** (`d_eff`) against **+0.107** (PR) | Spearman against **measured MC**, over **seven per-variant medians** | T0 §3.12(3) | as above | 7-point correlation over per-variant medians | 448 | nominal | **AGGREGATION UNIT 1.** Both are against **measured MC**, never against rung index. **One number from this row and one from the next may never appear in the same sentence** |
| **+0.998** (`d_eff`) against **+0.308** (PR) | Spearman against measured MC, **pooled within-regime over 350 cells** | T0 §3.12(3) | as above, filter `task == "mc"`, `condition == "human_empirical"`, `spectral_radius >= 3.05`, `alpha == 1e-6` | 350-point correlation over cells | 448 | nominal | **AGGREGATION UNIT 2**, separate from the row above. A2 §2.2 recomputes +0.998172 and +0.308132. **These are four numbers, not two, and each pair has its own unit**: quoting +0.107 against +0.998 mixes the PR value from one with the `d_eff` value from the other |
| **-0.18** and **-0.54** | the same pair against **rung index**, a **different quantity** | T0 §3.12(3), as corrected in session 2 | as above | 7 rungs, `rung` column | 448 | nominal | **the number that must NOT be quoted**, named and set aside. A2 §2.2 recomputes -0.180 and -0.541; under position in ladder order PR gives -0.607. The sign was published as **+0.54** and corrected; the magnitude was always right |
| **438 of 448** | directions whose ridge weight `g_i/(g_i + alpha)` exceeds 0.5 | **Not in T0.** A2 A2.4 and F6 caption; FL F6 claim cell is silent on it | `results/scale_448/covariance_spectra.parquet` | **one connectome cell** at sigma = 3.0526, the seed whose `d_eff` is nearest the median of the ten | 448 | nominal | **one cell, not a median.** Its `d_eff` is **431** and its PR **1.28**; the per-substrate medians in F6b and F6c are over all 50 supercritical cells, where the connectome sits at **413** and **1.38** |
| **two directions carry 95% of PR = 1.28** | how fast the variance weight collapses | **Not in T0.** A2 A2.4 and F6 caption | as above | the same single cell | 448 | nominal | same-cell qualifier as above. "the variance weight has collapsed by the fifth direction" |
| `d_eff` = **431** on the single cell against **413** as the connectome's median | the difference F6's own panels carry | **Not in T0.** A2 F6 block and caption | as above | one cell against median over 50 | 448 | nominal | stated in the caption **and** in panel (a)'s title ("one connectome cell"), so the caveat sits in the figure rather than resting on a caption sentence a journal edit may cut |
| `d_eff = sum_i g_i/(g_i+alpha)`; `sum_i p_i/sum_j p_j^2 = 1/sum_j p_j^2 = PR` | both measures are **exactly** sums of one weight per direction | **Not in T0.** A2 A2.4, F6 block and caption | as above | exact identities | 448 | not applicable | this is what licenses **area-as-count** in F6a. PR's identity is written out because it is the less obvious of the two |
| **one and the same 2500 x 448** post-warmup state matrix | PR and `d_eff` are computed on the same data | **Not in T0.** A2 §2.6 finding 4, F6 caption | as above | PR on the **time-centred covariance**, `d_eff` on the **un-centred Gram** the solver inverts | 448 | not applicable | **the difference is one of weighting, not of data slice**, which is exactly what contribution 6 claims. This is true of MC; it is **not** true of NARMA-10 (2800 rows captured, 2000 enter the design) and F6 does not use it |
| per-rung medians: connectome **412.94 / 1.3821 / 13.622**; weight-permuted **223.13 / 1.2233 / 9.178**; random_gaussian **81.32 / 1.2778 / 4.795**; erdos_renyi **74.77 / 1.2859 / 4.577**; degree_rewire **138.18 / 1.1895 / 6.797**; clustering_rewire **260.32 / 1.2241 / 9.832**; modularity_rewire **167.43 / 1.1909 / 7.452** | `d_eff` / PR / MC per rung | **Not in T0** as a table. A2 §2.2 only | as above | median over 50 supercritical cells per variant | 448 | nominal | the seven-rung ladder is **Probe 3's**, and only F6 draws it. MC itself moves **2.98-fold** (4.58 to 13.62) over the same substrates |
| **+0.999** | the `d_eff` to MC correspondence, at every alpha from 1e-8 to 1e-3 | T0 §3.3 | `taskA` alpha sweep | across the alpha grid | 448 | nominal | **it is what licenses reading the floor account as a memory account**, and it is void if the two alphas ever drift. Raising alpha does not break the link provided it is raised in both places |
| supercritical ordering **flat across alpha from 1e-10 to 1e2** | robustness of the ladder ordering to the ridge | T0 §3.2 | `taskA_ordering_by_sigma.csv` | ordering statistic per sigma region | 448 | nominal | only the **near-peak** region moves with alpha, and only because raising alpha un-saturates the peak. Report the ordering as a **curve in sigma**, not as a single thresholded number |
| **-1.00** subcritical (sigma < 1.5), **-0.11** near peak (1.5 <= sigma < 3.08), **+0.93** supercritical (sigma >= 3.08); spreads **83 / 83 / 352** | the ordering by sigma region | T0 §3.2 | as above | +1 = connectome highest | 448 | nominal | quoted as three regions, never as one number |
| the **sigma >= 3.05** threshold is **structural, not tuned** | why the supercritical cut is where it is | T0 §3.2 | as above | not applicable | 448 | nominal | it is the connectome's own critical point (`1/0.3249` = 3.078), and the ordering **already flips sign at sigma = 2.53**, 0.52 below it, so the threshold **discards sigma where the effect already holds**: it is conservative |
| peak `d_eff/N` **>= 0.993** for every null, **0.961** for the connectome at alpha = 1e-6 | the peak is ceiling-limited | T0 §3.2 | as above | per-variant peak over sigma | 448 | nominal | **peak capacity is unresolvable at N = 448** and will be at any N (T0 §6 item 6); the ladder ordering lives elsewhere entirely. Read the decay region |

## Forbidden phrasings for this section

- **Any sentence containing one number from the seven-rung unit and one from the 350-cell
  unit.** "+0.998 against +0.107" is the specific error T0 §3.12 and roadmap contribution
  6 both warn against. Use **+1.000 against +0.107** (seven per-variant medians) or
  **+0.998 against +0.308** (350 cells), never a number from each.
- **The rung-index correlation quoted as the result.** It is a different quantity; name it
  and set it aside.
- **"+0.54"** for the PR rung-index value. The sign was corrected to **-0.54**.
- **"PR is wrong."** PR measures what it says it measures. The claim is that the quantity
  it measures is not the one a ridge readout can use, which is about fit-for-purpose, not
  correctness.
- **"`d_eff` is a better measure in general."** The demonstration is empirical, on one
  task, one substrate family and one readout. Dambre 2012 is the parent bound and is cited
  as such; Clark 2025 is a **terminology collision to be distinguished**, not a result to
  be claimed against.
- **PR's failure presented as a separate finding.** It is a consequence of section 4.
- **A mechanism for why the low-variance directions carry memory.** F6a shows they clear
  the ridge floor and that MC tracks how many do. Nothing here explains what the
  information in them is.
- **431 and 413 used interchangeably.** 431 is one cell; 413 is the median over fifty.
- **"peak `d_eff` shows the connectome uses more directions."** The peak is
  ceiling-limited; the ordering lives in the decay region.
- **"the manifold lives in low-frequency graph harmonics."**
- **"compact bulk", "compressed bulk."**

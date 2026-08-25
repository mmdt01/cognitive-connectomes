# Fact sheet 08: chapter 5 section 3, "The Perron mode carries the mean"

**Section:** `report/act2_manifold.md` §4, **section 3**.
**Claims carried:** A2.1, A2.2. **Chain step 2** in `report/CROSS_ACT_SPINE.md`: spectral
gap to weak common-mode domination.
**Figure:** F4 (a and b).

The inversion is the finding: the substrate with much the largest Perron root is the
**least** dominated by it.

Source key: **T0** = `TIER0_STATE_OF_PLAY.md`. **A2** = `report/act2_manifold.md`.
**FL** = `report/FIGURE_LIST.md`.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| **0.0001** | share of the **time-centred** state variance held by the top `W` eigenmode | T0 §3.12(1) | `results/scale_448/manifold_alignment.parquet` | **pooled median over 3 tasks x 10 seeds (n = 30)**; recomputed 0.000143 | 448 | nominal | the aggregation is **not stated in T0** and had to be recovered (A2 §2.1, §5 item 6); it is the only one returning both published digits. `k` = 1, connectome, `human_empirical`, sigma = 3.0526. **Probe 2 scope: two substrates, four spectral radii** |
| **0.0023** | the random-orthonormal baseline for the same quantity | T0 §3.12(1) | as above | as above; recomputed 0.002316 | 448 | nominal | quoted **with** the 0.0001, never alone. For scale, `1/N` = **0.002232**, so the random band is at chance as expected |
| **0.0006** (0.000642) | the same quantity on **MC alone**, the task every other Act II number is measured on | A2 §2.1, §5 item 6; A2 F4 caption. **Not in T0** | as above | median over 10 seeds, MC only | 448 | nominal | **4.5x the quoted digit** and still **3.9x below its own baseline** (0.002521). F4a draws MC and quotes 0.0006 for what it draws, then quotes the pooled 0.0001 as the value of record. The claim is **direction, not magnitude** |
| **29 of 30** (task, seed) cells below their own random baseline | robustness of the direction to the aggregation choice | A2 §2.1, §5 item 6. **Not in T0** | as above | count over 3 tasks x 10 seeds | 448 | nominal | this is what makes the claim robust where the magnitude is not. On **means** the statement is nearly degenerate: one Lorenz seed at 0.0558 pulls the mean to 0.00217 against a random mean of 0.00232 |
| **10 of 10 seeds at every `k` <= 5** | how consistently the dominant modes fall below chance | A2 A2.1, F4 caption; A2 §4 item 3.2. **Not in T0** | as above | per seed, MC | 448 | nominal | stated with the `k` range; it is not a statement about all `k`. **Probe 2 scope applies** |
| chance by **`k` ~ 20** | where the `W`-eigenmode curve reaches the random baseline | A2 A2.1, F4 caption; A2 §4 item 3.2. **Not in T0** | as above | medians over seeds, MC | 448 | nominal | "reach chance only around `k` = 20 and track it thereafter"; approximate and written as such |
| **7.6x above chance at `k` = 1** | the low-frequency graph harmonics on the same states | A2 F4 block and caption. **Not in T0** | as above | medians over seeds, MC | 448 | nominal | this is the **control that makes the shortfall mean something**: without it, "the dominant modes are at or below chance" could mean no structural basis aligns with the fluctuations. It is a property of the leading dynamical modes, not of structural bases in general |
| chance band **0.00136 to 0.00321** at `k` = 1 | the across-seed range of the per-seed 20-basis mean | A2 F4 block. **Not in T0** | as above | across-seed range of the per-seed chance **mean** | 448 | nominal | it is **not** the across-basis s.d. A single random direction has s.d. **0.0029** about a mean of **0.0025**, which is simply what one direction out of 448 does, is not the quantity being compared, and cannot be drawn on a log axis because the lower edge is negative |
| `\|mean_state\|` **0.759** / **0.949** / **0.959** / **0.989** at sigma = 6 | common-mode amplitude, connectome / weight-permuted / degree / Erdős–Rényi | T0 §3.7 (and §3.12(1)) | `saturation_diagnostics.parquet`; also `item2_f_extension_scale_448.parquet` for F11 | **absolute value per seed, then seed median** | 448 | nominal | at **sigma = 6, `f` = 0**; every sigma-bearing claim names its sigma. The connectome is the **least** common-mode dominated substrate **despite carrying by far the largest Perron root**; that is the inversion, and it is what the spectral gap buys |
| `\|mean_state\|` **0.114** / **0.532** / **0.586** / **0.593** at sigma = 2 | the same quantity near criticality | T0 §3.7 | as above | as above | 448 | nominal | quoted with its sigma. It is the low end of the rise F4b draws |
| **0.638** | the connectome's sigma = 6 value under **median then absolute value** | T0 §3.12 gotcha; A2 §2.4, §5 item 1 | as above | **the wrong order**, quoted only as the gotcha | 448 | nominal | this is an **aggregation qualifier on the 0.759, not an alternative value**. T0 states the shrink; A2 §5 item 1 records that it is **worse than T0 says**: the weight-permuted null reads **0.575**, below the connectome, so the panel would argue against its own caption |
| **0.575** | the weight-permuted value under the same wrong order | A2 §2.4, §5 item 1; FL F11 flag. **Not in T0** | as above | median then abs | 448 | nominal | the null lands **below** the connectome, inverting the ladder. Both F4b's and F11's builders now assert the connectome is lowest, so it fails the build rather than the reader |
| **0.676** at sigma = 2.42 | the maximum discrepancy between the two aggregation orders across the sweep | A2 §5 item 1. **Not in T0** | as above | worst over the 58-point sweep | 448 | nominal | weight-permuted; recorded as the size of the trap, not as a result |
| agreement to **three decimals** | Probe 1's `saturation_diagnostics.parquet` against the `f > 0` extension at sigma = 6, `f` = 0 on MC | T0 §3.12 cross-capture check | both files | per variant, all four | 448 | nominal | two **independent captures of the same reservoirs**, so this is a cross-validation and not a duplication. F4b is against **sigma at `f` = 0**; F11 is the same numbers against **`f` at sigma = 6** and belongs to chapter 6 |
| `sr_crit` **1.81 to 1.92** against the connectome's **3.08** | why the nulls' `\|mean_state\|` rises first | T0 §2.1, §3.1 | `spectra_per_seed.parquet` | `1/median(bulk95)` | 448 | nominal | the nulls **become supercritical first**; the shaded region in F4b starts at the connectome's `sr_crit` |
| **f = 0** throughout | the sign condition | A2 §4 item 3.4 | not applicable | not applicable | 448 | nominal | **no sign manipulation appears in this section, or anywhere in this chapter** |

## Forbidden phrasings for this section

- **"the connectome's Perron mode is small"** or any reading in which weak domination
  means a weak leading eigenvalue. The connectome carries **much the largest** Perron
  root; that is what makes the inversion a finding.
- **Any ladder reading of Probe 2.** F4a is `connectome` at one operating point out of the
  four Probe 2 captured, on a two-substrate file.
- **"the manifold lives in low-frequency graph harmonics."** The harmonics curve is in
  F4a as a **control**, not as a claim about where the manifold lives.
- **Quoting 0.0001 as an MC number.** It is a pooled median over three tasks; MC alone is
  0.0006.
- **"the leading mode carries none of the variance."** It carries the **time-average**;
  what falls below chance is its share of the **time-centred** variance.
- **A signed median of `mean_state`**, or 0.638 quoted as a value rather than as the
  gotcha.
- **`\|mean_state\|` quoted without its sigma.** Every sigma-bearing claim names its sigma.
- **"hub inhibition collapses memory."** Nothing in this section touches hub targeting,
  and the phrase is withdrawn: hub-targeted inhibition closes the advantage fastest;
  nothing collapses, the null moves.
- **"compact bulk", "compressed bulk."**
- Any **graded curvature or trajectory-straightness** account.

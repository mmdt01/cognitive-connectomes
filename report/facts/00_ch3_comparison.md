# Fact sheet 00: chapter 3, "The comparison problem"

**Section:** `report/act1_structure.md` §4, chapter 3 outline item 1. Act I owns one
section in chapter 3; `report/CROSS_ACT_SPINE.md` names it and points here for detail.
**Claims carried:** A1.6 (contribution 5), A1.7.
**Figure:** F3, single panel, three sub-panels (a) nominal, (b) `sigma*bulk95`, (c) the deltas.
**Extraction only.** Every number below was read from the document named in its source
cell. Nothing was recomputed and nothing was run.

Source key: **T0** = `TIER0_STATE_OF_PLAY.md` (rank 1, canonical for numbers).
**FL** = `report/FIGURE_LIST.md`. **A1** = `report/act1_structure.md`. **CONV** =
`report/CONVENTIONS.md`. A row whose source is not T0 is **not TIER0-backed** and says so.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| `sigma*W/\|lambda_1\|` | the operator actually simulated | T0 §1.1 | definition; realised in `criticality_matched/results/e02_panel.parquet` | not applicable | 448 | both | its spectral radius is **exactly sigma for every variant**, guaranteed by the normalisation, so the nominal axis is not noisy in sigma; its bulk radius is `sigma*bulk95` |
| nominal sigma | matching axis 1 | T0 §1.1 | as above | not applicable | 448 | nominal | holds the **spectral radius** (the Perron root) fixed, lets the bulk radius vary; textbook ESN criticality; **not neutral**, in the opposite direction to the matched axis |
| `sigma*bulk95` | matching axis 2 | T0 §1.1 | as above | per seed, from the cell file's own `bulk95` column | 448 | sigma*bulk95 | holds the **bulk radius** fixed, leaves the **Perron root deliberately unmatched**; since the memory mechanism under test *is* the hub-localised Perron mode, this axis hands the connectome more of the proposed cause |
| **+343.3** | peak `dD` (connectome minus Erdős–Rényi, `d_eff`) | T0 §2.2 | `e02_panel.parquet`, `e02_axis_summary.csv` | median over seeds of the **per-seed difference** | 448 | nominal | quoted with its axis and with what that axis holds fixed; never against the matched figure without both statements |
| **4.47** | the nominal sigma at which peak `dD` occurs | T0 §2.2 | as above | as above | 448 | nominal | this is nominal sigma, not `x` |
| **-217.4** | most negative `dD` | T0 §2.2 | as above | as above | 448 | nominal | this is the **subcritical deficit present at matched spectral radius**; the deficit claim as originally stated survives on neither axis and is dropped |
| **+196.5** | peak `dD` | T0 §2.2 | as above | median over seeds of the per-seed difference | 448 | sigma*bulk95 | interior to the overlap [0, 2.599] and turning over, so it is the value at the true peak, not a bound |
| **1.949** | the `x` at which peak `dD` occurs | T0 §2.2 | as above | as above | 448 | sigma*bulk95 | `x = sigma*bulk95`, per seed |
| **-24.0** | most negative `dD` | T0 §2.2 | as above | as above | 448 | sigma*bulk95 | the deficit is **absent at matched bulk radius** |
| **57% retained** | ratio of the matched peak to the nominal peak | T0 §2.2 | as above | as above | 448 | both (a ratio between them) | after Task B extended the sweep to sigma = 8 the matched peak is **interior** and declines to +155.5, so 57% is the value at the true peak, **not a bound** |
| **+155.5** | the matched `dD` at the post-peak decline | T0 §2.2 | `taskB_extended_sweep_scale_448.parquet` (Task B extension) | as above | 448 | sigma*bulk95 | quoted only as what shows the peak is interior |
| **[0, 2.599]** | the four-variant overlap on the matched axis | T0 §2.2, §4 | `e02_panel.parquet` | per seed then across seeds | 448 | sigma*bulk95 | the overlap is what bounds the comparison; the peak sits inside it |
| **within 0.8%** | interpolation sensitivity of the matched peak | T0 §2.2 | `e02_panel.parquet`, `interp` column | linear against cubic | 448 | sigma*bulk95 | quoted as robustness of the peak, not of the axis |
| **89% of the deficit removed** | change in the most negative `dD` between axes | T0 §2.2 | `e02_axis_summary.csv` | as above | 448 | both | **must NOT be written as "89% an artifact of nominal-sigma matching"**; T0 §1.1 says that phrasing is not defensible. Write: present at matched spectral radius, absent at matched bulk radius |
| **1.7x larger Perron root** | connectome against Erdős–Rényi at the matched point | T0 §1.1 | `e02_panel.parquet` | at the matched point x = 1.949 | 448 | sigma*bulk95 | this is why the matched axis is not neutral; it is the reason both axes are reported |
| **sigma = 6.0** against **sigma = 3.54** | the nominal sigma each substrate sits at when x = 1.949 | T0 §1.1 | as above | as above | 448 | sigma*bulk95 | always quoted as the pair; one alone does not carry the point |
| **+197.6 at 2.144**, min **-31.5** | peak and most negative `dD` under the variant-median `bulk95` | T0 §4 | `e02_panel.parquet` | every cell's own `bulk95` replaced by its **variant median** | 448 | sigma*bulk95 | robustness check against `bulk95`'s extreme-value noise; the peak moves **0.6%** |
| **0.6%** | movement of the peak under the variant-median substitution | T0 §4 | as above | as above | 448 | sigma*bulk95 | the verdict is robust to per-seed `bulk95` noise |
| **+349.5 at 0.279**, min **-245.8** | peak and most negative `dD` on `sigma*absolute bulk` | T0 §4 | `e02_panel.parquet` | as above | 448 | not a third axis | **it is the nominal axis**: the absolute bulk is near-constant across variants, so `sigma*absolute bulk` is a constant times sigma and returns the nominal numbers (+343.3 / -217.4). **There are two axes here, not three** |
| **9.4** (nominal), **8.3** (matched) | maximum parting between the difference of medians and the median of differences | FL, F3 flag; A1 §3, F3 block. **Not in T0** | `e02_panel.parquet` | (a) and (b) are per-substrate medians; (c) is the median of per-seed differences | 448 | both | (a) and (b) are **not expected to subtract to** (c); the caption states the discrepancy rather than hiding it |
| **+338.1** | the difference-of-medians value at the nominal peak, against the published +343.3 | FL, F3 flag; A1 §3, F3 block. **Not in T0** | `e02_panel.parquet` | difference of separately medianed curves | 448 | nominal | the paired per-seed statistic (+343.3) is the published one and the correct one for a paired comparison; do not redraw (c) as the difference of medians |
| **>= 0.993** (every null), **0.961** (connectome) | peak `d_eff/N`, **the pair the thesis quotes** | T0 §3.2 | `taskA` alpha sweep | per-variant peak over sigma, alpha = 1e-6 | 448 | nominal | the `d_eff = N = 448` ceiling is **load-bearing, not decoration**: Erdős–Rényi runs along it, so the advantage in (c) is largely how far below ceiling the connectome sits and where. **Body prose quotes this pair** |
| **0.997 of N** (Erdős–Rényi), **0.965** (connectome) | the same quantity on the E0.2 panel, **F3's own source** | FL's F3 flag and A1's F3 block, both cross-noted to T0 §3.2 on 25 August 2026. **Not in T0** | `e02_panel.parquet` | per-substrate medians over seeds, nominal axis | 448 | nominal | **neither pair is wrong; they are different sources and filters.** Resolved 25 August 2026 by cross-note rather than change: this pair appears **only inside F3's caption, where its filter is stated**, and must not be carried into body prose as the published value. T0 §3.2 now names it and its filter, and both figure-side documents name T0's |
| `sr_crit = 1 / median_over_seeds(bulk95)` | the criticality scale convention | T0 §1.3; CONV | `eigenspectrum.common.SR_CRIT_CONVENTION` | median over seeds, **not** mean | 448 and 1000 | not applicable | median, so that `sr_crit` can be reproduced by inverting the reported central `bulk95` |
| **0.0431** | upper bound on the Jensen bias of the per-seed mean of `1/bulk95`, **within the four-rung ladder** | **T0 §1.3 as amended 25 August 2026 (a)**; CONV, corrected the same day | `spectra_per_seed.parquet` | mean against mean, Erdős–Rényi at N=1000 | 1000 | not applicable | **this replaces the 0.087 both documents used to carry.** "Biased upward" is a statement about **mean-against-mean, not mean-against-median**: against the median the ladder maximum is **0.0727** (Erdős–Rényi, N=1000) and the sign is **negative** for all three N=1000 nulls. The convention itself does not change |
| **0.0868** | the same gap for **`random_gaussian` at N=1000**, a rung **outside** the ladder | **T0 §1.3 amendment (a)**; A1 §5 item 4 | as above | mean against mean | 1000 | not applicable | this is the value CONV and T0 §1.3 previously quoted as **0.087** in the ladder's context. It is right, and it is the rung `common.SR_CRIT_CONVENTION`'s own source comment names. Quoted **only** as `random_gaussian`'s, so the larger number stays traceable |
| **<= 0.0014** | agreement between the two computation orders under the median | T0 §1.3 | `spectra_per_seed.parquet` | median commutes with monotone transforms | 448 and 1000 | not applicable | this is what licenses reading `sr_crit` off the published `bulk95` |
| `alpha = lambda*trace(G)/N` | the ridge reparameterisation | T0 §2.5; CONV | `n1000_memory_scale_1000.parquet` | two evaluator passes per cell | 1000 | not applicable | **`alpha` must be identical in `d_eff` and MC**, or the +0.999 correspondence that licenses reading one through the other is void |
| **lambda = 4.4845e-10** | the pinned reparameterisation constant | T0 §2.5 | as above | pinned so the N=448 supercritical median alpha equals the frozen 1e-6 | 1000 | not applicable | quoted with what it was pinned to |
| median **8.6e-07**, range **[2.6e-07, 1.1e-06]** | the realised alpha at N=1000 | T0 §2.5 | as above | median and range over cells | 1000 | not applicable | realised, not nominal; alpha depends on `trace(G)` which depends on the states |
| **4.35 -> 4.40** | the N=448 supercritical margin under the reparameterisation control | T0 §2.4, §2.5 | `n1000_memory_scale_448.parquet` | median per-cell change **0.32%** | 448 | not applicable | the control **passed**, so any shift at N=1000 is attributable to N |
| **T = 3000 -> 6000**, `T_eff/N` **5.58 -> 5.50** | the protocol scaling between the two runs | T0 §2.5 | as above | warmup 500 at both scales | 448 and 1000 | not applicable | the design Gram is a sample covariance and its small-eigenvalue tail is what finite `T/N` distorts, which is exactly what `d_eff` counts |
| `\|lambda_1\|` relative s.d. **0** / **0.0628** / **0.0885** / **0.0867** | non-concentration of the normaliser across seeds (connectome / weight-permuted / degree / Erdős–Rényi) | FL, F3 flag; A1 A1.7 and §5. **Not in T0** | `spectra_per_seed.parquet` | relative s.d. across 10 seeds | 448 | not applicable | the connectome's 0 is trivial (one fixed graph, nothing resampled). **Do not write "the permuted-multiset control has relative s.d. exactly 0" without saying of what** |
| `\|lambda_1\|` relative s.d. **0** / **0.0385** / **0.0908** / **0.1285** | the same at the larger parcellation | FL, F3 flag; A1 §5. **Not in T0** | `scale_1000/spectra_per_seed.parquet` | as above | 1000 | not applicable | as above |
| **6.3%** | the residual relative s.d. in `\|lambda_1\|` once the weight multiset is frozen by permutation | A1 A1.7 (0.0628 at N=448 in A1 §5 and FL's F3 flag). **Not in T0** | `spectra_per_seed.parquet` | relative s.d. across 10 seeds | 448 | not applicable | this residual **is the placement contribution alone**; that is the whole point of the permutation control |
| largest sampled weight, relative s.d. **0** (permuted), **0.119** | non-concentration of the weight draw itself | FL, F3 flag (**0.119**); A1 §5 item 7 (**0.118992**). **Not in T0** | `spectra_per_seed.parquet` | relative s.d. across 10 seeds; identical for degree and Erdős–Rényi, which draw the same pool under the same seed | 448 | not applicable | the 0 is exact **for the largest sampled weight**, because permutation gives an identical multiset every seed; it is **not** 0 for `\|lambda_1\|` |
| largest sampled weight, relative s.d. **0.167** | the same at the larger parcellation | FL, F3 flag (**0.167**); A1 §5 item 7 (**0.167018**). **Not in T0** | `scale_1000/spectra_per_seed.parquet` | as above | 1000 | not applicable | as above |
| **2 distinct values across 10 seeds** (N=448), **3** (N=1000) | how few maxima the resampling nulls actually realise | FL, F3 flag; A1 §5 item 7. **Not in T0** | `spectra_per_seed.parquet`, both scales | count of distinct maxima over 10 seeds | 448 and 1000 | not applicable | this is the non-concentration the claim rests on, shown directly rather than through a tail index |
| **+0.854 to +0.949** | correlation of the largest sampled weight with `\|lambda_1\|` | FL, F3 flag (band); A1 §5 item 7 (**+0.854** degree and **+0.939** Erdős–Rényi at N=448; **+0.949** and **+0.906** at N=1000). **Not in T0** | `spectra_per_seed.parquet`, both scales | across seeds, per variant | 448 and 1000 | not applicable | A1.7 states the band as **+0.85 to +0.95**; the four values are inside it |
| Hill index **2.49** (N=448) **-> 2.28** (N=1000) | tail index of the **empirical weight pool** | FL, F3 flag, citing E0.4 §5. **Not in T0** | E0.4 §5 | tail index over the weight pool | 448 and 1000 | not applicable | **attributed to the empirical weight pool, NOT to `\|lambda_1\|`.** Do not write "`\|lambda_1\|` is an extreme-value statistic with Hill alpha ~2.3". Defensible wording: the normaliser is a **single non-concentrating order statistic**, so what nominal matching equalises rests on one sampled weight and the bulk radius each seed realises inherits the spread |
| the rule adopted | report both axes, state what each holds fixed, rest no claim on one alone | T0 §1.1; CONV | not applicable | not applicable | all | both | A1.6 is **symmetric**: neither axis is neutral, and the claim rests on **surviving both**. It does not say one axis is correct |

## Forbidden phrasings for this section

- **"89% an artifact of nominal-sigma matching"**, or any wording making one axis the
  correction of the other. T0 §1.1 states in terms that this is not defensible. The
  deficit is present at matched spectral radius and absent at matched bulk radius.
- **"the correct axis"**, "the right axis", "the corrected numbers". The two axes hold
  different spectral features fixed; A1.6 is symmetric and is deliberately so.
- **"`sigma*bulk95` is the neutral comparison."** It is not: it hands the connectome a
  1.7x larger Perron root, which is the mechanism under test.
- **"the connectome is subcritically worse than Erdős–Rényi."** Write "parity below
  criticality, advantage above", and name the axis.
- **"there are three matching axes."** `sigma*absolute bulk` is the nominal axis; T0 §4
  says so explicitly. Two axes, not three.
- **"`\|lambda_1\|` is an extreme-value statistic with Hill alpha ~2.3."** The Hill index
  belongs to the empirical weight pool, not to `\|lambda_1\|`.
- **"the permuted-multiset control has relative s.d. exactly 0"** without naming the
  quantity. It is exactly 0 for the largest sampled weight and 0.0628 for `\|lambda_1\|`.
- **"the nominal axis is noisy in sigma."** The normalisation makes the spectral radius
  exactly sigma for every variant.
- **"compact bulk", "compressed bulk"**, which would arrive here through the F1 unit
  discussion. Write "large spectral gap".
- **"the connectome is a better reservoir."** No task appears in this section, and
  contributions 1 and 5 are task-free.

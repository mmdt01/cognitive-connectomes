# Fact sheet 09: chapter 5 section 4, "The Gram spectrum against the ridge floor"

**Section:** `report/act2_manifold.md` §4, **section 4**. New on 24 August 2026; the
restructure exists for it.
**Claims carried:** A2.6, A2.7. **Chain step 3** in `report/CROSS_ACT_SPINE.md`: the
measured link from weak common-mode domination to usable dimensionality, and the one step
of the chain that had no figure until 24 August.
**Figure:** F18 (a, b, c). It prints **between F4 and F6**.

**Provenance warning that governs the whole sheet.** T0 §3.6 files this result under a
**rejected** anisotropy hypothesis. The rejection stands; what is used is the **refit at
the correct end of the spectrum**. The verification record is
`report/checks/floor_sensitivity_check.md`, which is a check file and is **not canonical
for results**.

> **Updated 25 August 2026.** The section's headline, the four-variant by four-bin
> position table, **was not in T0 and now is**: it was promoted as **T0 §3.6 amendment
> (e)**, sourced to CHK §5.1, carrying the two qualifiers the section cannot be written
> without (the bins partition each individual cell exactly while the per-bin medians are
> not constrained to sum to 100, connectome 102.1%; and the zero-strip of amendment
> (a)). What **stays check-file-only, deliberately, is figure data**: the 13-point
> sigma-resolved sensitivity curve behind F18b and the five per-alpha migration rows
> behind F18c. Rows below still marked **Not in T0** are the ones no rank-1 document
> carries.

Source key: **T0** = `TIER0_STATE_OF_PLAY.md`. **CHK** =
`report/checks/floor_sensitivity_check.md`. **FL** = `report/FIGURE_LIST.md`.
**A2** = `report/act2_manifold.md`. **SPINE** = `report/CROSS_ACT_SPINE.md` (structure
only, explicitly not canonical for numbers).

## 4.1 The position table (the headline, stated before any rate)

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| **89.0%** | the connectome's directions more than a decade **clear** of the floor | **T0 §3.6 amendment (e)** of 25 August 2026, sourced to CHK §5.1; also FL F18 row, SPINE step 3, A2 A2.6 | `results/scale_448/covariance_spectra.parquet` | **per-bin median over the 50 supercritical cells**, as a percentage of all 448 directions | 448 | nominal | supercritical (`spectral_radius >= 3.05`), MC, `human_empirical`, alpha = 1e-6. The four per-bin medians **do not sum to 100**; the connectome's come to **102.1%** |
| **11.4%** | the same bin for Erdős–Rényi | **T0 §3.6 amendment (e)**; also FL F18 row, SPINE step 3, A2 A2.6 | as above | as above | 448 | nominal | quoted **as the pair** with 89.0%; alone it invites the degenerate reading |
| **0.2% / 4.9% / 8.0% / 89.0%** (connectome) | the four position bins: exactly zero, more than a decade below alpha, within a decade of alpha, more than a decade above alpha | **T0 §3.6 amendment (e)**, sourced to CHK §5.1 | as above | per-bin medians over 50 cells | 448 | nominal | the four bins **partition each individual cell exactly**; four medians taken separately are not constrained to sum to 100 |
| **2.6% / 36.0% / 18.6% / 38.1%** (weight-permuted) | the same four bins | **T0 §3.6 amendment (e)**, sourced to CHK §5.1 | as above | as above | 448 | nominal | as above |
| **9.9% / 49.3% / 18.3% / 22.0%** (degree) | the same four bins | **T0 §3.6 amendment (e)**, sourced to CHK §5.1 | as above | as above | 448 | nominal | as above |
| **20.4% / 52.8% / 10.6% / 11.4%** (Erdős–Rényi) | the same four bins | **T0 §3.6 amendment (e)** for all four; 20.4% and 52.8% were already in **amendment (c)** | as above | as above | 448 | nominal | as above |
| **73.2%** | Erdős–Rényi's spectrum at or more than a decade **below** the floor before alpha is raised at all | T0 §3.6 amendment (c) | as above | 20.4 + 52.8 | 448 | nominal | **"before alpha is raised at all"** is part of the number. It is a statement about a **level**, not a rate; §4.3 below is where the rate goes |
| **5.1%** | the connectome's combined at-or-below-floor fraction | T0 §3.6 amendment (c) | as above | 0.2 + 4.9 | 448 | nominal | the connectome's profile is the **reverse** of Erdős–Rényi's |
| **102.1%** | the sum of the connectome's four per-bin medians | **T0 §3.6 amendment (e)**, which carries it as a required qualifier; also CHK §5.1, A2 F18 block and §4 item 4.1 | as above | four medians taken separately | 448 | nominal | **stated with the aggregation.** It is why F18a is **grouped, not stacked**: a stacked bar would assert a partition the medians do not form. CHK records that an earlier draft called these "the median cell", which is a different statistic |
| **398.5** | the connectome's directions more than a decade clear, as a count | **Not in T0.** A2 F18 block and §5 item 18 only | as above | per-bin median over 50 cells | 448 | nominal | quoted only to say it is **close to but not identical with** `d_eff` = 413, which is why `d_eff` rides in F18a's legend rather than being annotated against the top bar |

## 4.2 The zero-strip convention

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| `g = g[g > 0]` | the zero-strip: exact zeros dropped **before all four statistics** | **T0 §3.6 amendment (a)** of 24 August 2026 | `criticality_matched/closeout.py:floor_mass`; `report/figlib/sources.py:_floor_statistics` | applied to the design-Gram spectrum before every statistic | 448 | nominal | cite it to **T0 §3.6 amendment (a)**. Before that amendment the convention was undocumented and load-bearing; FL's F18 flag is now the figure-side pointer to it rather than an outstanding request |
| **6.6% / 48.8% / 65.8% / 79.4%** | the published fraction below alpha, connectome / weight-permuted / degree / Erdős–Rényi | T0 §3.6 refit table | `covariance_spectra.parquet` | median over 50 supercritical cells, on the **zero-stripped** spectrum | 448 | nominal | these are on the **zero-stripped denominator** and reproduce only under it |
| **7.03 / 50.00 / 69.53 / 83.59%** | the same fractions on the **full 448-direction** denominator | **T0 §3.6 amendment (a)** | as above | median over 50 cells, no strip | 448 | nominal | the **counterfactual**, quoted to show the strip is load-bearing: **without it the fraction below alpha reproduces for no variant.** It also matters for substance: Erdős–Rényi's headline 79.4% **understates** how much of its spectrum is unusable |
| median **1.0 / 11.5 / 44.5 / 91.5** | the count of exactly-zero Gram eigenvalues per cell | T0 §3.6 amendment (a); CHK §1.3 | as above | seed median | 448 | nominal | the error from missing the strip **grows down the ladder because this count does** |
| the other three statistics are **unaffected** | why only the fraction moves | T0 §3.6 amendment (a); CHK §1.3 | as above | not applicable | 448 | nominal | a zero eigenvalue contributes **exactly 0** to `d_eff`, **exactly 0** to the sensitivity, and is **never within a decade of alpha**; only the fraction has a denominator to move |

## 4.3 Floor sensitivity as a rate, with the both-ends warning first

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| `-d(d_eff)/d(log alpha) = sum_i g_i*alpha/(g_i+alpha)^2` | floor sensitivity, defined | T0 §3.6; CHK §1.0 | as above | derivative with respect to the **natural** log of alpha, so units are `d_eff` per e-fold | 448 | nominal | each term **peaks at 1/4 when `g_i = alpha` and falls away in either direction**, so the quantity **vanishes at both ends of the spectrum**. State the warning **before** the numbers |
| **8.85** / **18.09** / **17.75** / **10.26** | floor sensitivity, connectome / weight-permuted / degree / Erdős–Rényi | T0 §3.6 | `covariance_spectra.parquet` | median over the 50 supercritical cells | 448 | nominal | supercritical (`sigma >= 3.05`), MC, alpha = 1e-6. **A low value never interprets itself**: it means either "clear of the floor" or "already below it", and only the position table tells the two apart |
| **36** / **84** / **82** / **48** | modes within a decade of alpha | T0 §3.6 | as above | median over 50 cells | 448 | nominal | CHK §1.2 records that the weight-permuted and Erdős–Rényi values are **83.5** and **47.5**, half-integers rounded half-up, because the median of 50 integer counts lands on a half. A figure drawing them plots the halves and says which it is doing |
| **412.9** / **223.1** / **138.2** / **74.8** | `d_eff`, supercritical | T0 §3.6 (and §3.12(3) for the range) | as above | median over 50 cells | 448 | nominal | this is what the position table **counts**. CHK §1.2 cross-validates against `probe3_deff.parquet` (412.94 / 223.13 / 138.18 / 74.77), two code paths onto the same cells |
| **2.1% / 8.1% / 12.8% / 13.7%** | floor sensitivity as a share of `d_eff` | **T0 §3.6 amendment (c)** | as above | ratio of the two medians | 448 | nominal | the **rate**, and the qualifier on every level in §4.3: "10.26 is low" is a statement about a **level**, and what governs how much a substrate loses when alpha rises is a **rate**. CHK §5.3 gives 2.14 / 8.11 / 12.85 / 13.72% |
| **23.3 (5.6%)** / **52.1 (23.3%)** / **37.6 (27.2%)** / **21.8 (29.1%)** | `d_eff` lost per decade of alpha, absolute and as a share | **T0 §3.6 amendment (c)** | as above | as above | 448 | nominal | **the absolute loss per decade is nearly the same at the two ends of the ladder** (23.3 against 21.8); the connectome has 413 directions to lose it from and Erdős–Rényi has 75. Per unit of surviving dimensionality Erdős–Rényi is the **most** floor-sensitive substrate on the ladder |
| **6.4 times** | how much more floor-sensitive Erdős–Rényi is than the connectome per unit of surviving dimensionality | **Not in T0.** CHK §5.3 only | as above | ratio of the two shares | 448 | nominal | the same fact as 13.72% against 2.14%, stated as a ratio |
| **about 75** against **about 413** directions left to lose | the stock each substrate has | **Not in T0.** CHK §5.2 only | as above | from `d_eff` | 448 | nominal | "almost nothing left to strip", quantified. **83% of Erdős–Rényi's reservoir contributes nothing a ridge readout can use; 92% of the connectome's is usable** (CHK §5.2) |

## 4.4 The radius-resolved interior minima

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| **3.5789**, value **5.785** | the connectome's **interior** floor-sensitivity minimum | **T0 §3.6 amendment (b)(i)** (and the main §3.6 paragraph as "sigma approx 3.6, value 5.8") | `covariance_spectra.parquet` | median over 10 seeds at each of 13 radii; argmin taken over `sigma >= 1.2632` | 448 | nominal | **"interior" is not droppable.** The curve is two-humped and falls to zero at sigma = 0 |
| **8 of 10 seeds** | how consistently the connectome's dip sits at 3.5789 | **T0 §3.6 amendment (b)(i)**; CHK §3.2 (2 of 10 at 4.1053) | as above | per-seed argmin | 448 | nominal | the separation is a **seed-level fact, not an artifact of medianing** |
| **1.5789 or 2.0000** in **10 of 10 seeds** | every null's interior dip | **T0 §3.6 amendment (b)(i)**; CHK §3.2 | as above | per-seed argmin | 448 | nominal | CHK §3.2 gives the per-seed split: weight-permuted 7 of 10 at 2.0000, degree 7 of 10 at 1.5789, Erdős–Rényi 5 of 10 at each |
| **2.383** / **1.837** / **1.815** | the three null interior minima, weight-permuted / degree / Erdős–Rényi | **T0 §3.6 amendment (b)(ii)** | as above | median curve | 448 | nominal | spanning **1.8 to 2.4** |
| **1.8 to 2.4** | the span of the three null interior minima | **T0 §3.6 amendment (b)(ii)** | as above | as above | 448 | nominal | this replaces the published 1.8 to 3.9, which is **withdrawn as the span of the null minima** |
| **1.8 to 3.9** | a **different quantity**: the span of the sensitivity **across the minimum region**, over the six values the three nulls take at sigma = 1.5789 and sigma = 2.0000 | **T0 §3.6 amendment (b)(ii)**; CHK §3.2 | as above | six values, lowest 1.815 (Erdős–Rényi at 2.0000), highest 3.925 (degree at 2.0000) | 448 | nominal | **must not be used in a caption or read as the span of the minima.** Both are true statements about different things |
| **0.4211**, value **2.687** | the connectome's **global** minimum over non-zero sigma | **T0 §3.6 amendment (b)(i)**; CHK §3.2 | as above | median curve | 448 | nominal | it sits **below** the interior dip at 5.785, with `d_eff` = 20.8 (CHK §3.2). **This is the reason the word "interior" is not droppable**: read as a global minimum the connectome's half of the claim does **not** reproduce |
| the curve falls to **0.00** at sigma = 0 for every variant | why the minima that matter are interior | **Not in T0** as a table. CHK §3.1 (the 13-point per-variant curve); FL F18 flag; A2 F18 block | as above | median over 10 seeds | 448 | nominal | a dead reservoir has almost no spectrum above the floor to lose. F18b **draws the whole curve including sigma = 0 and shades the low-sigma limb** rather than cropping |

## 4.5 The migration

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| **2.4 to 3.6** | the connectome's measured ridge-optimal sigma as alpha rises | T0 §3.6 (and §3.3) | `criticality_matched/results/taskB_extended_sweep_scale_448.parquet` | argmax over sigma of the seed-median `mc_alpha_*` column | 448 | nominal | it migrates **toward** its own interior dip. **Consistent-with, not fitted**: nothing regresses the optimum on the sensitivity curve and no residual is bounded |
| **1.2 to 1.6** | every null's measured ridge-optimal sigma over the same alpha grid | T0 §3.6 (and §3.3) | as above | as above | 448 | nominal | the nulls **move once, at the first step, and then stop** (CHK §3.3) |
| **1e-8: 2.4 / 1.2 / 1.2 / 1.2** | ridge-optimal sigma at the first alpha | **Not in T0.** CHK §3.3 only | as above | as above | 448 | nominal | the five per-alpha rows are in the **check file only**; T0 §3.6 publishes the endpoints alone |
| **1e-6: 2.8 / 1.6 / 1.6 / 1.6** | the same at the second alpha | **Not in T0.** CHK §3.3 only | as above | as above | 448 | nominal | as above |
| **1e-5: 3.2 / 1.6 / 1.6 / 1.6** | the same at the third alpha | **Not in T0.** CHK §3.3 only | as above | as above | 448 | nominal | as above |
| **7e-5: 3.2 / 1.6 / 1.6 / 1.6** | the same at the fourth alpha | **Not in T0.** CHK §3.3 only | as above | as above | 448 | nominal | as above |
| **1e-3: 3.6 / 1.6 / 1.6 / 1.6** | the same at the fifth alpha | **Not in T0.** CHK §3.3 only | as above | as above | 448 | nominal | as above. CHK §3.3 reproduces the frozen `taskB_mc_alpha_peaks.csv` exactly (max deviation 0.0 on the peak sigma, 1.8e-15 on the peak MC over all 20 rows) |
| **five orders of magnitude** in **four steps** | the alpha grid 1e-8, 1e-6, 1e-5, 7e-5, 1e-3 | **T0 §3.6 amendment (d)** of 24 August 2026 | as above | not applicable | 448 | not applicable | **"four orders" was the step count, not the order count**, and is corrected to **five**. Nothing is computed from the count, so no result moves |
| **two different sigma grids** | the qualifier on the whole migration panel | T0 §3.6 (grid difference implicit); CHK §3.4 qualification 1; FL F18 flag; A2 §4 item 4.5 | probe grid (13 points, 0 to 6) against Task B grid (21 points, 0 to 8, step 0.4) | not applicable | 448 | nominal | **3.5789 and 3.6 are two grids' nearest points to the same place, not the same number**, and neither are 1.5789 and 1.6 |
| **two of the four land one grid step off their own dip** | how exact the correspondence is | **Not in T0.** A2 F18 block; FL F18 flag | as above | not applicable | 448 | nominal | the connectome ends at 3.6 against a dip at 3.5789 and degree at 1.6 against 1.5789, but weight-permuted's and Erdős–Rényi's dips are at **2.00** while their optima end at **1.6**. The caption says "migrates **toward**" and does not say "onto" |
| the three nulls' ridge-optimal sigma is **identical at every alpha** | why F18c's markers nest | **Not in T0.** FL F18 flag; A2 F18 block | as above | as above | 448 | nominal | **nothing is offset**: an offset would draw a disagreement the data does not contain |

## 4.6 The anisotropy retraction

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| PR **1.253** / **1.205** / **1.294** | participation ratio, connectome / degree / Erdős–Rényi, over sigma in [2.0, 4.2] | T0 §3.6 | covariance spectra | over the top decile | 448 | nominal | PR is **flat across variants (1.21 to 1.29)** |
| decay exponent **-3.03** / **-3.87** / **-4.16** | covariance decay, same three variants | T0 §3.6 | as above | fitted over the **top** decile | 448 | nominal | the connectome has the **shallowest** decay, so it is **less** anisotropic by decay exponent, not more. The hypothesis is **rejected** |
| top-mode fraction **0.891** / **0.908** / **0.873** | how far one mode dominates | T0 §3.6 | as above | as above | 448 | nominal | every variant is dominated by one mode (0.87 to 0.91) |
| the refit is at the **bottom** of the spectrum | why the rejection does not carry over to the account that survives | T0 §3.6 | design-Gram spectrum | exact sensitivity of `d_eff` to the floor | 448 | nominal | the decay exponent was fitted over the **top** decile while the surviving hypothesis was about the **bottom**. **The rejection stands**; what the section uses is the refit that replaced it. F18 "carries none of the six contributions, deliberately" |

## Forbidden phrasings for this section

- **"minimum"** without **"interior"**, anywhere, in prose or in a caption. The
  connectome's global minimum over non-zero sigma is 0.4211 (2.687), below its interior
  dip; read as a global minimum the claim does not reproduce.
- **"1.8 to 3.9"** as the span of the null minima. It is the span of the sensitivity
  across the minimum region. The minima span **1.8 to 2.4**.
- **"raising alpha costs Erdős–Rényi little."** It costs it **29.1%** of everything it
  has, the most of any substrate on the ladder. The stock is nearly exhausted; the rate is
  the highest here. A sentence conflating the two errs in the direction that flatters the
  connectome, which is the direction this programme has already been caught in three
  times.
- **"Erdős–Rényi is the least floor-sensitive substrate"** without the rate beside it.
- **A low floor sensitivity read as a good sign, or as a bad one, on its own.** The
  sensitivity vanishes at **both** ends of the spectrum, so a low number never interprets
  itself, and the position table is what tells the two cases apart.
- **"the gap puts the Gram spectrum clear of the floor"** as though this section derived
  it. Nothing here derives where the Gram spectrum sits from `W`'s spectrum; the link from
  the gap to the floor **runs through section 3's common-mode account**, and reading this
  section as a derivation skips the step doing the work.
- **"the anisotropy hypothesis is confirmed"**, or any use of the decay exponent as
  support. It is rejected, and the rejection stands.
- **"the migration is fitted"**, "tracks", "predicts", or any regression language.
  Consistent-with, not fitted; direction and endpoint match, nothing else is claimed.
- **"3.58 is 3.6"**, or one sigma axis carrying both grids without saying so.
- **"as alpha rises four orders."** Five orders, four steps.
- Quoting **6.6% or 79.4%** without the zero-strip, or **7.03% or 83.59%** as the
  published values.
- **A stacked bar, or any sentence implying the four per-bin medians sum to 100.** They do
  not; the connectome's come to 102.1%.
- **"compact bulk", "compressed bulk."**

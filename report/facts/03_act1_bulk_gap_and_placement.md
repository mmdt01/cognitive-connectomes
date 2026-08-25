# Fact sheet 03: chapter 4 section 3, "The bulk is everyone's; the gap is not, and it is placement"

**Section:** the **merged** section. `report/act1_structure.md` §4, chapter 4 outline
**items 4 and 5** ("The bulk is everyone's; the gap is not" and "It is placement"), which
audit item 16 of 24 August 2026 records as merging into a single drafted section. Counted
**within chapter 4** they are its **3rd and 4th** sections; counted **in the outline** they
are items **4 and 5**. Outline item 3 ("The spectrum is real, and it has one outlier")
stays separate; a reader who takes "sections 3 and 4" as outline items would merge the
wrong two.
**Claims carried:** A1.2, A1.3, A1.5. Nothing moves with the merge.
**Figures:** F1b, F2a, F2b, F2c (and F1a to F1f as the stack).

Source key: **T0** = `TIER0_STATE_OF_PLAY.md`. **FL** = `report/FIGURE_LIST.md`.
**A1** = `report/act1_structure.md`. **CONV** = `report/CONVENTIONS.md`.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| `bulk95` **0.3249** / **0.5203** / **0.5338** / **0.5535** | the normalised bulk radius, connectome / weight-permuted / degree / Erdős–Rényi | T0 §2.1 | `eigenspectrum/results/scale_448/spectra_per_seed.parquet` | **median over seeds** | 448 | not applicable | medians. The **means** 0.5120 / 0.5238 / 0.5509 are **withdrawn** (T0 §2.1, dated correction of 15 August 2026) and anyone holding them is holding the wrong convention |
| `abs(lambda_1)` **0.1889** / **0.1152** / **0.1115** / **0.1061** | the Perron root in **raw units of `W`** | T0 §3.1 | as above, column `lambda_max_raw` | median over seeds | 448 | not applicable | raw units. `\|lambda_1\|` is `lambda_max_raw`; `perron_root` is 1.0 in every row because the spectra are stored normalised |
| absolute bulk **0.0614** / **0.0599** / **0.0595** / **0.0587** | the bulk radius in raw units | T0 §3.1 | as above | **`median(bulk95) x median(\|lambda_1\|)`**, the product of medians | 448 | not applicable | the aggregation is part of the number. Computing an absolute bulk from `bulk95_radius` returns the ratio and gives a 47.3% spread instead |
| **4.4%** | spread of the absolute bulk across variants | T0 §3.1 | as above | product of medians; **spread = range / mean** | 448 | not applicable | **carries "at N = 448"**. T0 §3.1 states this explicitly, added 15 August 2026 because contribution 1 was carrying "4.4% spread" and "scale-robust" in one sentence. The 4.4% is **not** what survives the change of scale |
| **4.4%** ("identical") | the same spread under the other aggregation | T0 §3.1 | as above | **median of the per-seed products** | 448 | not applicable | at N=448 the two aggregations agree; at N=1000 they do not, which is why the aggregation is quoted with the number there. A1 §2.2 recomputes 4.426% and 4.447% |
| **47.3%** | spread of `bulk95` across variants | T0 §3.1 | as above | medians; range / mean | 448 | not applicable | the contrast against 4.4% **is** the claim: the entire between-variant difference sits in `\|lambda_1\|` |
| gap ratio **3.078** / **1.922** / **1.873** / **1.807** | `\|lambda_1\| / absolute bulk`, the headline structural statistic | T0 §3.1, §2.1 | as above | `1 / median(bulk95)` | 448 | not applicable | the gap ratio, the inverse bulk and the critical scale are **the same number**. The connectome's stands **~1.7x clear of every null** |
| `\|lambda_1\|/abs_bulk = 1/bulk95 = sr_crit` | the identity | T0 §3.1 | as above | holds **only under the product-of-medians aggregation** | 448 and 1000 | not applicable | A1 §2.3 records that taking the median of the per-seed products instead **breaks it by up to 0.055 at N=1000** (degree: 2.356 against `sr_crit` 2.301). A1 §2.3 verifies the identity to **< 1e-15** under the correct aggregation |
| **1.78x** | the connectome's Perron root against Erdős–Rényi's | T0 §3.1 | as above | ratio of medians | 448 | not applicable | the restatement of Act I: placement **does not compress the bulk, it raises the Perron root over a bulk that is essentially everyone's** |
| **0.587** | the connectome/Erdős–Rényi `bulk95` ratio | T0 §2.1 | as above | median convention | 448 | not applicable | quoted **only as a median and only with both scale values** (0.587 -> 0.612), because the direction of change depends on the convention |
| **0.325** against **0.52 to 0.55** | `bulk95` read off the 95th-percentile crossing of the normalised ECDF | A1 F1 caption; FL F1 flag. **Not in T0** at this precision | `spectra_per_seed.parquet`, panel (e) | all 10 seeds | 448 | not applicable | these are the **normalised** units every spectral-radius-matched comparison uses; the caption must tie panel (e) back to the raw-units stack as the same spectra one division apart |
| bulk edges at **0.0587 to 0.0614** | the four bulk bands sitting at the same page coordinate in the F1 stack | FL F1 flag; A1 F1 caption. **Not in T0** as a range | rendered figure | product of medians | 448 | not applicable | the stack is what carries the claim; panels (a) to (d) carry the entire raw-units argument alone |
| weight-permuted `bulk95` **0.5203**, gap ratio **1.922** | the placement control lands with the nulls | T0 §2.1, §3.1 | as above | median over seeds | 448 | not applicable | the control holds **topology and the exact weight multiset** fixed and scrambles only which edge carries which weight. It licenses **placement, not which feature of placement**; no mechanism for why placement produces the gap is claimed |
| "anomalously compact bulk" **->** "anomalously large spectral gap" | the retraction, stated once | T0 §3.1; CONV withdrawn-language table | not applicable | not applicable | 448 | not applicable | stated **in the direction the data supports**, once, in this section. Same fact, different direction |

## Forbidden phrasings for this section

- **"compact bulk", "compressed bulk", "the connectome's bulk is narrow."** Write "large
  spectral gap". This is the section where the phrase would come back, because in the
  units the literature reports (`W / \|lambda_1\|`) the connectome's bulk genuinely does
  look narrower; that appearance is manufactured by dividing by the one quantity that
  differs.
- **"the near-identity of the bulks is scale-robust"**, or any sentence carrying "4.4%
  spread" and "scale-robust" together. T0 §3.1 is explicit that one sentence must not
  carry both. The 4.4% is an N = 448 number.
- **"4.4%"** without "at N = 448" attached, and without its aggregation where the two
  aggregations differ.
- **Any ordering among the three nulls by `bulk95`** stated without a named scale; it
  reverses between scales.
- **The withdrawn means 0.5120 / 0.5238 / 0.5509** as `bulk95` values.
- **"the connectome's gap ratio is the highest, so it is the best substrate."** Act I
  makes no task claim; contributions 1 and 5 are task-free and no task can corroborate or
  refute them.
- **A mechanism for why placement produces the gap.** Act I establishes that it does. The
  connectome against weight-permuted contrast localises it to placement and stops there.
- **"the connectome is a better reservoir."**

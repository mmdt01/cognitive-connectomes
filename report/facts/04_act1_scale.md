# Fact sheet 04: chapter 4 section 4, "Scale"

**Section:** `report/act1_structure.md` §4, chapter 4 outline **item 6**.
**Claims carried:** A1.4.
**Figures:** F2 (both scales), **S1** (F1 rebuilt at N = 1000, appendix, outside the cap).

**The structure of the section is three verbs.** What **carries** is the separation; what
**loosens** is the near-identity of the bulks; what **reverses** is the null ordering,
which is therefore never quoted across scales.

Source key: **T0** = `TIER0_STATE_OF_PLAY.md`. **FL** = `report/FIGURE_LIST.md`.
**A1** = `report/act1_structure.md`.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| `bulk95` **0.2509** / **0.4176** / **0.4346** / **0.4102** | the normalised bulk radius, connectome / weight-permuted / degree / Erdős–Rényi | T0 §2.1 | `eigenspectrum/results/scale_1000/spectra_per_seed.parquet` | **median over seeds** | 1000 | not applicable | medians. The **means** 0.4254 / 0.4449 / 0.4307 are **withdrawn** (T0 §2.1, dated correction) |
| `sr_crit` / gap ratio **3.985** / **2.395** / **2.301** / **2.438** | the critical scale each substrate brings with it | T0 §2.1 | as above | `1 / median(bulk95)` | 1000 | not applicable | the same quantity as the gap ratio and as the inverse bulk. Reading **down the column** here is not monotone; see the S1 row below |
| **3.985 against 2.30 to 2.44** | the gap-ratio separation at the larger parcellation | T0 §3.1 | as above | as above | 1000 | not applicable | quoted as a **separation**, never as a sweep down the column. A1 A1.4 writes the null band as **2.301 to 2.438** |
| **2.2x change in N** | the size of the scale step | T0 §1.4, §2.4; A1 A1.4 | both scale parquets | not applicable | 448 to 1000 | not applicable | this is the whole scope of the scale claim; no third parcellation exists |
| absolute-bulk spread **6.4%** | how far the near-identity loosens | T0 §3.1 | as above | **`median(bulk95) x median(\|lambda_1\|)`**, product of medians; spread = range / mean | 1000 | not applicable | **the aggregation must be quoted with the number at N = 1000**, where the two aggregations differ. T0 §3.1 says so explicitly |
| absolute-bulk spread **6.9%** | the same quantity under the other aggregation | T0 §3.1 | as above | **median of the per-seed products** | 1000 | not applicable | stated **beside** the 6.4%, never instead of it. A1 §2.2 recomputes 6.430% and 6.886%. F2's caption names which one the panel uses |
| `bulk95` spread **48.5%** | the normalised-bulk spread at the larger parcellation | T0 §3.1 | as above | medians; range / mean | 1000 | not applicable | against 47.3% at N = 448; the contrast with the absolute-bulk spread is what the section is about |
| **~1.7x** | the connectome's gap-ratio separation from every null, **at both scales** | T0 §3.1 | both scale parquets | as above | 448 and 1000 | not applicable | **this is what survives the change of scale.** Write "the absolute bulk is essentially everyone's" **of N = 448**, and "the gap ratio separates the connectome from every null at both scales" **of the scale claim**. Do not let one sentence carry both |
| N=448 `perm (0.5203) < degree (0.5338) < ER (0.5535)`; N=1000 `ER (0.4102) < perm (0.4176) < degree (0.4346)` | the null ordering reversal by `bulk95` | T0 §2.1; A1 §2.4 | both scale parquets | medians | 448 and 1000 | not applicable | **the ordering must not be assumed to carry, and is quoted at a named scale or not at all.** The reversal holds under either convention; the ordering of the *other* two nulls does not, which is a further reason to quote medians only |
| **3.99, 2.39, 2.30, 2.44** reading down the S1 rows | the gap ratios in ladder order at N = 1000 | FL, S1 flag; A1 S1 caption. **Not in T0** in this row order | `scale_1000/spectra_per_seed.parquet` | `1/median(bulk95)` | 1000 | not applicable | **the row ordering is NOT monotone at N = 1000 and the caption must not imply it is.** At N = 448 ladder order coincides with descending gap ratio (3.08, 1.92, 1.87, 1.81), which is why F1's caption can say "rises from 1.81 to 3.08". **Quote the separation, never the sweep down the column** |
| **0.587 -> 0.612**, **rising** | the connectome/Erdős–Rényi `bulk95` ratio across scales, median convention | T0 §2.1 | both scale parquets | medians | 448 and 1000 | not applicable | **quote it only as a median and only with both values.** The direction depends on the convention |
| **0.590 -> 0.583**, **falling** | the same ratio on the withdrawn mean convention | T0 §2.1 | as above | per-seed means (withdrawn) | 448 and 1000 | not applicable | named only to say that the **direction of this ratio depends on the aggregator**, which is why the median is quoted. A1 §2.4 reproduces both directions and calls it the strongest single check in its gate |
| **0.251** against **0.410 to 0.435** | `bulk95` read off the 95th-percentile crossing at N = 1000 | A1 S1 caption. **Not in T0** at this precision | `scale_1000/spectra_per_seed.parquet`, panel (e) | all 10 seeds | 1000 | not applicable | normalised units, as at N = 448 |
| max `\|delta\|` = **0.000e+00** on `bulk95`, `lambda_max_raw`, `perron_root` across 40 N=1000 cells | the N=1000 cell-for-cell rebuild | A1 §2.5, §5 item 15. **Not in T0** | `HumanSubstrateBuilder` against `scale_1000/spectra_per_seed.parquet` | exact | 1000 | not applicable | E0.4's own gate **skips at N=1000**; this is what gives the N=1000 numbers the same standing as the N=448 ones. A1 records it as worth a line in T0 §2.1 next time that section is edited |
| peak `d_eff/N`: connectome **0.971**, nulls **0.984 to 0.999** | the ceiling is not escaped at the larger parcellation | T0 §2.4 | `n1000_memory_scale_1000.parquet` | per-variant peak over sigma | 1000 | nominal | quoted only if the section touches the ceiling; it confirms the **robustness-not-capacity** framing rather than adding a scale result. T0 §6 item 6: peak `d_eff` is ceiling-limited at N=448 and will be at any N |

## Forbidden phrasings for this section

- **The null ordering carried across scales**, in either direction, and any sweep read
  down a column of gap ratios at N = 1000. Quote the connectome's separation from every
  null; never the arrangement among them.
- **"the gap ratio rises from 2.30 to 3.99"** or any equivalent, which is the S1 version
  of the same error.
- **"compact bulk", "compressed bulk."**
- **"the near-identity of the bulks holds at both N"**, and any single sentence carrying
  both "4.4% spread" and "scale-robust".
- **"6.4%"** without its aggregation, at this scale, where the two aggregations give 6.4%
  and 6.9%.
- **"scale-invariant"** full stop, of anything. T0 §2.4 forbids it for the memory margin
  on the grounds that it is true of one filter only, and the same discipline applies here:
  what is scale-robust is the **separation**, not the near-identity.
- **"the connectome is a better reservoir."**

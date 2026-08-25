# Fact sheet 02: chapter 4 section 2, "The spectrum is real, and it has one outlier"

**Section:** `report/act1_structure.md` §4, chapter 4 outline **item 3**. It is
decomposition without a control and stays where it is; it does **not** merge with the
following pair.
**Claims carried:** A1.1.
**Figure:** F1a (the F1 stack; panel a is the connectome row).

Source key: **T0** = `TIER0_STATE_OF_PLAY.md`. **FL** = `report/FIGURE_LIST.md`.
**A1** = `report/act1_structure.md`.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| max `\|Im lambda\|` = **0.0** over all 80 ladder cells | the spectrum is entirely real | A1 §2.5; A1 F1 caption ("max \|Im lambda\| = 0 across all 40 cells" at N=448). **Not in T0** | `spectra_per_seed.parquet`, both scales | exact, over every cell | 448 and 1000 | not applicable | the substrate is **symmetric**, so a complex-plane scatter would be degenerate with all mass on one line; that is why F1 is a histogram on the real axis and not an eigenvalue cloud |
| `is_symmetric` **true in every row** | the storage-level check behind the above | A1 §2.5. **Not in T0** | `spectra_per_seed.parquet` | exact | 448 and 1000 | not applicable | stated with the max imaginary part, not instead of it |
| `\|lambda_1\|` = **0.1889** | the connectome's Perron root in raw units of `W` | T0 §3.1 | `spectra_per_seed.parquet`, column `lambda_max_raw` | median over seeds | 448 | not applicable | **raw units of `W`**, not normalised units. The connectome is one fixed graph, so its median is its value |
| **0.188862** | the same Perron root, recomputed live for F15 | FL, F15 flag. **Not in T0** | leading eigenvector of the N=448 self-built consensus, computed live | `eigh`, no aggregation | 448 | not applicable | quoted only as the cross-check that F15 is on the right substrate; it matches `lambda_max_raw` **to six decimals** |
| `bulk95` = the 95th percentile of `\|lambda\|` over the **full** spectrum, divided by `\|lambda_1\|` | the definition, with the Perron outlier **included** in the percentile population | A1 §2.6 finding 1, citing `src/analysis/spectral.py:116` and `common.BULK95_DEFINITION`. **Not in T0** as a definition | `spectra_per_seed.parquet` | one implementation, reached by every caller | 448 and 1000 | not applicable | the outlier is **inside** the population the percentile is taken over; nothing re-derives this |
| max deviation **2.6e-08** (N=448), **2.8e-08** (N=1000) | independent recomputation of `bulk95` from the stored eigenvalue arrays | A1 §2.5. **Not in T0** | `spectra_per_seed.parquet`, column `eig_w_real` | `pct95(\|lambda\|)/max(\|lambda\|)` per row | 448 and 1000 | not applicable | the deviation **is the `float32` storage precision of `eig_w_real`**, not a disagreement |
| stored per-seed `sr_crit == 1/bulk95` **row by row** | the per-row derived column is consistent | A1 §2.5. **Not in T0** | `spectra_per_seed.parquet` | exact, per row | 448 and 1000 | not applicable | this is a **per-row value, not an aggregate**; the reported `sr_crit` is `1/median(bulk95)` and the two must not be confused |
| **1.000000** | the F1 density axis integrates to one over the bins, all four substrates | A1 §3, F1 block. **Not in T0** | rendered figure | `density=True` | 448 | not applicable | quoted only if the density axis is explained; the axis is **derived, not chosen** |
| **0.6220** = `1/(448 * bin width)`; floor **0.3110**; ceiling **52.25** = `2 * 26.126` | the height a bin holding exactly one of the 448 eigenvalues sits at, and the axis limits derived from it | A1 §3, F1 block. **Not in T0** | rendered figure | not applicable | 448 | not applicable | the floor is half a single-eigenvalue bin so that lone eigenvalues out in the gap stay visible as bars rather than being clipped into the spine |
| spectrum runs to **+/-0.215** (N=448), **+/-0.266** (N=1000); density range **(0.310, 50.9)** and **(0.112, 56.3)** | the axis ranges at the two scales | A1 §3, S1 block. **Not in T0** | rendered figures | not applicable | 448 and 1000 | not applicable | recorded because the ticks were hard-coded to N=448 and **survived by luck, not design**; they are now derived from the range |
| each row scaled by the **median** `\|lambda_1\|`, not by its own seed's | the F1 aggregation rule | FL, F1 flag; A1 §5 item 13. **Not in T0** | `spectra_per_seed.parquet` | median over seeds | 448 and 1000 | not applicable | mixing the two put the largest bar off the `lambda_1` rule by **+0.00630** on the Erdős–Rényi row and **-0.00759** on the degree row. **The connectome row is exact either way**, so the row a reader checks first is the one row that cannot reveal the problem |
| each row binned over exactly `[-lambda_1, +lambda_1]` | the F1 binning rule | FL, F1 flag; A1 §5 item 13. **Not in T0** | rendered figure | bin count varies per row, bin width constant to **~0.3%** | 448 and 1000 | not applicable | a shared grid left the bar containing the extreme eigenvalue overhanging by **91.1%** and **93.1%** of a bin width on the weight-permuted and degree rows, and on the negative side for Erdős–Rényi. Assume shared-grid histograms drawn against per-series reference lines are wrong until measured |
| residual **2.8%** (Erdős–Rényi) | the drawn seed's own 95th percentile against the drawn median bulk edge | A1 §5 item 13. **Not in T0** | rendered figure | single seed against median | 448 | not applicable | stated rather than hidden; drawing per-seed bulk edges instead would show a **7.3%** spread across the four rows where the published figure is 4.4% |

## Forbidden phrasings for this section

- **"compact bulk", "compressed bulk"**, and any statement that the connectome's bulk is
  narrow. In raw units it is not; the appearance is manufactured by dividing by
  `\|lambda_1\|`, which is the one quantity that differs.
- **"the spectrum has a complex component"**, or any complex-plane framing. The substrate
  is symmetric and the spectrum is entirely real; a scatter in the plane would be
  degenerate.
- **"the Perron root is an outlier of the bulk distribution"** in the sense of being
  excluded from it. `bulk95` is the 95th percentile over the **full** spectrum with the
  Perron eigenvalue **included** in the population.
- **Quoting a per-row `sr_crit` as the substrate's `sr_crit`.** The reported value is
  `1/median(bulk95)`.
- **Any ordering among the nulls**, which does not belong in this section and reverses
  between scales in any case.
- **"the connectome is a better reservoir."** No task appears in Act I.

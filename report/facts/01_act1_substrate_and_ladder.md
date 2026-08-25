# Fact sheet 01: chapter 4 section 1, "The substrate and the null ladder"

**Section:** `report/act1_structure.md` §4, chapter 4 outline **item 2** (the first
section of chapter 4 proper).
**Claims carried:** none. The outline says **"No results."** Every number below is a
design fact, a grid size or a validation of the ladder, not a finding.
**Figures:** none.

Source key: **T0** = `TIER0_STATE_OF_PLAY.md`. **FL** = `report/FIGURE_LIST.md`.
**A1** = `report/act1_structure.md`. **A2** = `report/act2_manifold.md`.
**CONV** = `report/CONVENTIONS.md`. **CHK** = `report/checks/floor_sensitivity_check.md`.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| **N = 448** | the parcellation the whole thesis sits at | T0 §2.1 (used throughout); FL F1 and F15 for "self-built consensus" | `eigenspectrum/results/scale_448/spectra_per_seed.parquet` | not applicable | 448 | not applicable | the substrate is the **self-built consensus**, empirical weights, all-positive (`f` = 0). F15's flag adds that release node ordering is verified against consensus ordering by node-strength and edge-weight correspondence at **r >= 0.98**, which is an agreement and not an identity |
| **N = 1000** | the larger parcellation used for the scale check | T0 §2.1, §2.5 | `scale_1000/spectra_per_seed.parquet` | not applicable | 1000 | not applicable | a **2.2x change in N**; used for scale robustness, not as a second result |
| **10 seeds** per variant | the resampling replicate count | A1 §2 (40 rows per scale); T0 §2.5 names 10 seeds for the N=1000 grid | `spectra_per_seed.parquet`, both scales | not applicable | 448 and 1000 | not applicable | the **connectome has no seed variation**: it is one fixed graph and its ten seeds coincide exactly. Only the three nulls are resampled |
| **40 rows** per scale | the ladder cell count | A1 §2; FL F1 and S1 rows. **Not in T0** | `spectra_per_seed.parquet` filtered to `condition == "human_empirical"` and `variant in LADDER` | 4 variants x 10 seeds | 448 and 1000 | not applicable | this is the filter every Act I figure uses |
| **four rungs**: `connectome`, `connectome_weight_permuted`, `degree_rewire`, `erdos_renyi` | the criticality-matched ladder | CONV, figure style contract | as above | not applicable | 448 and 1000 | not applicable | these four are "the ladder the criticality-matched programme sweeps and the only variants in 12 of the 13 variant-bearing figure sources". A colour existing for another variant is not licence to add it to a ladder figure |
| weight-permuted: topology and the **exact weight multiset** held fixed, only which edge carries which weight scrambled | what the placement control preserves | A1 A1.5; T0 §2.1 (its `bulk95` 0.5203) | as above | not applicable | 448 and 1000 | not applicable | this is **the** control that isolates placement; it lands with the nulls. What it licenses is **placement, not which feature of placement** |
| degree rewire: the **sorted degree sequence** held fixed by double-edge swaps | what the degree null preserves | A1 §2.6 finding 3 and §5 item 3. **Not in T0** | null generation in `HumanSubstrateBuilder` | not applicable | 448 and 1000 | not applicable | `validate_null(..., "degree_sequence")` checks a property double-edge swaps preserve **by construction after any number of swaps, including zero**, so it is not a convergence test |
| **107,840** accepted swaps against a cap of **1,078,400** attempts | the production rewire setting at N=1000 (`n_swaps_multiplier = 10`) | A1 §5 item 3. **Not in T0** | null generation | not applicable | 1000 | not applicable | **10,784 undirected edges** at N=1000. Reported as the setting, with the convergence evidence beside it |
| retention **15.4% -> 5.2% -> 3.6%**, then flat **3.6 / 3.8 / 3.8 / 3.7%** at multipliers 5 to 40 | convergence of the rewire chain | A1 §5 item 3. **Not in T0** | re-run at multipliers 1, 2, 5, 10, 20, 40 on 5 seeds | retention of the original edge set | 1000 | not applicable | against a **~2.2% chance floor at this density**; the chain is mixed well before the production setting |
| median `bulk95` **0.4288, 0.4281, 0.4189, 0.4172, 0.4210, 0.4280** | stationarity of `bulk95` across rewire multipliers | A1 §5 item 3. **Not in T0** | as above | median over 5 seeds | 1000 | not applicable | total range **0.0116**, which is **0.26 of the between-seed s.d.**, and non-monotone (multiplier 40 lands where multiplier 1 does) |
| **seven rungs** for Probe 3: `random_gaussian` (0), `erdos_renyi` (1), `degree_rewire` (2), `clustering_rewire` (3), `modularity_rewire` (4), plus connectome and weight-permuted | the wider ladder used in chapter 5 only | A2 §2.2; CONV; FL F6 row | `results/scale_448/probe3_deff.parquet` | not applicable | 448 | not applicable | the three extra rungs "appear only in `probe3_deff.parquet`, which feeds **F6 alone**". Naming them here is a forward reference to chapter 5, not a claim that Act I sweeps seven rungs |
| **T = 3000**, warmup **500**, `T_eff/N` = **5.58** | the N=448 protocol | T0 §2.5 | run configuration | not applicable | 448 | not applicable | quoted only where the design Gram's finite-sample tail matters, which is what `d_eff` counts |
| **T = 6000**, warmup **500**, `T_eff/N` = **5.50** | the N=1000 protocol | T0 §2.5 | run configuration | not applicable | 1000 | not applicable | `T` was scaled to hold `T_eff/N`, so the two scales' `d_eff` are comparable |
| **2500 x 448**, no bias column | the memory-capacity design matrix | A2 §2.5, §2.6 finding 4. **Not in T0** | `covariance_spectra.parquet`, `readout_config.json` | post-warmup state matrix | 448 | not applicable | MC has **no bias column**, which is why `eig_gram` has 448 entries for MC and 449 for NARMA-10 and Lorenz |
| **13 spectral radii**: 0, 0.4211, 0.8421, 1.0526, 1.2632, 1.5789, 2.0, 2.5263, 3.0526, 3.5789, 4.1053, 5.1579, 6.0 | the probe capture grid | CHK Task 2. **Not in T0** | `results/scale_448/covariance_spectra.parquet` | not applicable | 448 | nominal | a **different grid** from Task B's 21 points (0 to 8, step 0.4). Any figure putting both on one axis says so |
| **21 points**, 0 to 8, step 0.4 | the Task B sweep grid at N=448 | T0 §2.5 | `taskB_extended_sweep_scale_448.parquet` | not applicable | 448 | nominal | quoted whenever it is read against the probe grid |
| **30 non-uniform sigma points to 10.4** (6 coarse over [0, 3.0], 18 dense over [3.2, 8.0], 6 over [8.4, 10.4]) | the N=1000 grid | T0 §2.5 | `n1000_memory_scale_1000.parquet` | not applicable | 1000 | nominal | `sigma_max` = 10.4 was chosen so the matched peak stayed **interior**; sigma_max = 8 would have reached only 2.007 on the matched axis and hidden the turnover |
| `perron_root == 1.0` in every row; `bulk95_radius` is the **ratio**, not a radius | two storage conventions in the frozen spectra | FL, F1/F2 flag; A1 §2.5. **Not in T0** | `spectra_per_seed.parquet` | not applicable | 448 and 1000 | not applicable | the spectra are stored **normalised**. The absolute bulk radius is `bulk95 * lambda_max_raw`, and `\|lambda_1\|` is `lambda_max_raw`. Computing an absolute bulk from `bulk95_radius` returns the ratio and gives a **47.3% spread where the answer is 4.4%** |
| max `\|delta\|` = **0.000e+00** on `bulk95`, `lambda_max_raw` and `perron_root`, 40 cells at each scale | cell-for-cell rebuild of the frozen parquet from the substrate builder | A1 §2.5 and §5 item 15. **Not in T0** | `HumanSubstrateBuilder` against `spectra_per_seed.parquet` | exact | 448 and 1000 | not applicable | this closes a real gap: E0.4's own reproduction gate **skips at N=1000**, so before this the N=1000 numbers had no cell-for-cell standing. T0 §2.1 states the gate for N=448 only |
| **210 cells** matched to **1.2e-14** | the E0.4 reproduction gate at N=448 | T0 §2.1 | `w_spectra.parquet` | exact comparison | 448 | not applicable | the gate is stated at N=448 only in T0 |

## Forbidden phrasings for this section

- **"compact bulk", "compressed bulk"** in any form, including when describing what the
  ladder was built to test. Write "large spectral gap".
- **Any result at all.** The outline says "No results". Numbers here are design facts,
  grid sizes and null validations; a `bulk95`, a gap ratio or a spread belongs in the
  next section.
- **"the degree rewire is validated by its degree-sequence assertion."** That assertion
  passes after zero swaps. The convergence evidence is the retention plateau and the
  `bulk95` stationarity, and it is stated as such.
- **"the connectome's seeds agree, so the null models are noisy."** The connectome is one
  fixed graph; its zero variance is trivial and is never used as evidence.
- **Any ordering among the three nulls**, by `bulk95` or anything else, stated without a
  named scale. The ordering reverses between N = 448 and N = 1000.
- **Adding a variant to the ladder because a colour exists for it.** The three extra
  Probe 3 rungs belong to F6 alone; if one turns up elsewhere that is a scope question.
- **"the biological cut"** for `f` = 0. `f` = 0 is what the instrument produces, and `f`
  does not appear in chapter 4 at all.

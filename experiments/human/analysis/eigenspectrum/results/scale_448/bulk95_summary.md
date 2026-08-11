# E0.4 -- spectral characterisation of the null ladder (human N=448)

Scale `448`, 10 seeds per cell, eigendecomposition only (no reservoir simulation).

`bulk95 = percentile(|lambda|, 95) / |lambda_1|, over the FULL spectrum of the un-rescaled recurrent matrix W (the Perron outlier is included in the percentile population). Computed by src.analysis.spectral.recurrent_spectrum as `bulk95_radius` on the normalised base W / |lambda_1|; identical formula to spectral_metrics' `bulk95_ratio`.`

`sr_crit = 1 / median_over_seeds(bulk95). The median is used rather than the mean because 1/x is convex: mean(1/bulk95) > 1/mean(bulk95) (Jensen), so a per-seed mean of 1/bulk95 is biased UPWARD -- by up to 0.087 at N=1000. Under the median the two computation orders agree to <= 0.0014, so sr_crit can be reproduced by inverting the reported central bulk95.`

Values are **mean ± sd across seeds**, except `sr_crit`, which is `1 / median(bulk95)` (a single number, not a mean of per-seed values). `lambda_max_raw` is the un-normalised `|λ₁|` the reservoir build divides out; every other column is on the normalised base `W / |λ₁|`. The connectome has sd = 0 by construction in the empirical column -- it is one fixed graph, only the nulls are resampled.


## `human_gaussian`

| variant | bulk95 | sr_crit = 1/median(bulk95) | outlier-to-bulk gap | \|λ₂\|/\|λ₁\| | λ_max (raw) |
|---|---|---|---|---|---|
| connectome | 0.8028 ± 0.0200 | 1.237 | 0.1972 ± 0.0200 | 0.9782 ± 0.0151 | 11.5669 ± 0.3435 |
| weight-permuted | 0.7908 ± 0.0203 | 1.262 | 0.2092 ± 0.0203 | 0.9696 ± 0.0205 | 11.7157 ± 0.2928 |
| rung 0 · random | 0.8579 ± 0.0175 | 1.166 | 0.1421 ± 0.0175 | 0.9814 ± 0.0163 | 10.2657 ± 0.2676 |
| rung 1 · Erdős–Rényi | 0.8521 ± 0.0156 | 1.168 | 0.1479 ± 0.0156 | 0.9844 ± 0.0113 | 10.3279 ± 0.1851 |
| rung 2 · degree | 0.8094 ± 0.0137 | 1.239 | 0.1906 ± 0.0137 | 0.9799 ± 0.0110 | 11.4239 ± 0.2255 |
| rung 3 · clustering | 0.7796 ± 0.0185 | 1.289 | 0.2204 ± 0.0185 | 0.9715 ± 0.0174 | 11.8444 ± 0.3648 |
| rung 4 · modularity | 0.8146 ± 0.0188 | 1.217 | 0.1854 ± 0.0188 | 0.9836 ± 0.0162 | 11.3893 ± 0.2699 |

## `human_empirical_signed`

| variant | bulk95 | sr_crit = 1/median(bulk95) | outlier-to-bulk gap | \|λ₂\|/\|λ₁\| | λ_max (raw) |
|---|---|---|---|---|---|
| connectome | 0.4023 ± 0.0103 | 2.494 | 0.5977 ± 0.0103 | 0.9333 ± 0.0296 | 0.1467 ± 0.0016 |
| weight-permuted | 0.5069 ± 0.0262 | 2.013 | 0.4931 ± 0.0262 | 0.9910 ± 0.0072 | 0.1161 ± 0.0051 |
| rung 0 · random | 0.5560 ± 0.0506 | 1.850 | 0.4440 ± 0.0506 | 0.9974 ± 0.0045 | 0.1053 ± 0.0094 |
| rung 1 · Erdős–Rényi | 0.5656 ± 0.0567 | 1.784 | 0.4344 ± 0.0567 | 0.9989 ± 0.0008 | 0.1040 ± 0.0104 |
| rung 2 · degree | 0.5602 ± 0.0798 | 1.784 | 0.4398 ± 0.0798 | 0.9949 ± 0.0049 | 0.1076 ± 0.0142 |
| rung 3 · clustering | 0.5637 ± 0.0700 | 1.778 | 0.4363 ± 0.0700 | 0.9827 ± 0.0244 | 0.1091 ± 0.0126 |
| rung 4 · modularity | 0.5386 ± 0.0322 | 1.854 | 0.4614 ± 0.0322 | 0.9923 ± 0.0103 | 0.1112 ± 0.0072 |

## `human_empirical`

| variant | bulk95 | sr_crit = 1/median(bulk95) | outlier-to-bulk gap | \|λ₂\|/\|λ₁\| | λ_max (raw) |
|---|---|---|---|---|---|
| connectome | 0.3249 ± 0.0000 | 3.078 | 0.6751 ± 0.0000 | 0.7598 ± 0.0000 | 0.1889 ± 0.0000 |
| weight-permuted | 0.5120 ± 0.0323 | 1.922 | 0.4880 ± 0.0323 | 0.9483 ± 0.0216 | 0.1187 ± 0.0075 |
| rung 0 · random | 0.5457 ± 0.0438 | 1.861 | 0.4543 ± 0.0438 | 0.9808 ± 0.0156 | 0.1070 ± 0.0084 |
| rung 1 · Erdős–Rényi | 0.5509 ± 0.0448 | 1.807 | 0.4491 ± 0.0448 | 0.9788 ± 0.0173 | 0.1060 ± 0.0092 |
| rung 2 · degree | 0.5238 ± 0.0534 | 1.873 | 0.4762 ± 0.0534 | 0.9367 ± 0.0474 | 0.1139 ± 0.0101 |
| rung 3 · clustering | 0.4888 ± 0.0378 | 2.081 | 0.5112 ± 0.0378 | 0.9471 ± 0.0325 | 0.1220 ± 0.0101 |
| rung 4 · modularity | 0.5150 ± 0.0176 | 1.952 | 0.4850 ± 0.0176 | 0.9501 ± 0.0295 | 0.1164 ± 0.0058 |

## Gates

- Reproduction vs committed `w_spectra.parquet`: **passed** (210 cells, max abs diff 1.2e-14)
- Documented N=448 headline values: **passed**

# E0.4 -- spectral characterisation of the null ladder (human N=1000)

Scale `1000`, 10 seeds per cell, eigendecomposition only (no reservoir simulation).

`bulk95 = percentile(|lambda|, 95) / |lambda_1|, over the FULL spectrum of the un-rescaled recurrent matrix W (the Perron outlier is included in the percentile population). Computed by src.analysis.spectral.recurrent_spectrum as `bulk95_radius` on the normalised base W / |lambda_1|; identical formula to spectral_metrics' `bulk95_ratio`.`

`sr_crit = 1 / median_over_seeds(bulk95). The median is used rather than the mean because 1/x is convex: mean(1/bulk95) > 1/mean(bulk95) (Jensen), so a per-seed mean of 1/bulk95 is biased UPWARD -- by up to 0.087 at N=1000. Under the median the two computation orders agree to <= 0.0014, so sr_crit can be reproduced by inverting the reported central bulk95.`

Values are **mean ± sd across seeds**, except `sr_crit`, which is `1 / median(bulk95)` (a single number, not a mean of per-seed values). `lambda_max_raw` is the un-normalised `|λ₁|` the reservoir build divides out; every other column is on the normalised base `W / |λ₁|`. The connectome has sd = 0 by construction in the empirical column -- it is one fixed graph, only the nulls are resampled.


## `human_gaussian`

| variant | bulk95 | sr_crit = 1/median(bulk95) | outlier-to-bulk gap | \|λ₂\|/\|λ₁\| | λ_max (raw) |
|---|---|---|---|---|---|
| connectome | 0.7525 ± 0.0228 | 1.332 | 0.2475 ± 0.0228 | 0.9798 ± 0.0107 | 12.0596 ± 0.3208 |
| weight-permuted | 0.7460 ± 0.0207 | 1.336 | 0.2540 ± 0.0207 | 0.9825 ± 0.0163 | 12.1587 ± 0.3485 |
| rung 0 · random | 0.8491 ± 0.0079 | 1.180 | 0.1509 ± 0.0079 | 0.9922 ± 0.0042 | 9.9071 ± 0.1446 |
| rung 1 · Erdős–Rényi | 0.8490 ± 0.0099 | 1.179 | 0.1510 ± 0.0099 | 0.9919 ± 0.0078 | 9.9244 ± 0.1817 |
| rung 2 · degree | 0.7629 ± 0.0247 | 1.304 | 0.2371 ± 0.0247 | 0.9831 ± 0.0164 | 11.9602 ± 0.3642 |
| rung 3 · clustering | 0.7026 ± 0.0237 | 1.426 | 0.2974 ± 0.0237 | 0.9643 ± 0.0223 | 12.7565 ± 0.4009 |
| rung 4 · modularity | 0.7685 ± 0.0180 | 1.300 | 0.2315 ± 0.0180 | 0.9798 ± 0.0163 | 11.8594 ± 0.2226 |

## `human_empirical_signed`

| variant | bulk95 | sr_crit = 1/median(bulk95) | outlier-to-bulk gap | \|λ₂\|/\|λ₁\| | λ_max (raw) |
|---|---|---|---|---|---|
| connectome | 0.2818 ± 0.0073 | 3.526 | 0.7182 ± 0.0073 | 0.9285 ± 0.0376 | 0.1900 ± 0.0045 |
| weight-permuted | 0.4092 ± 0.0314 | 2.392 | 0.5908 ± 0.0314 | 0.9956 ± 0.0033 | 0.1431 ± 0.0113 |
| rung 0 · random | 0.4288 ± 0.0987 | 2.428 | 0.5712 ± 0.0987 | 0.9993 ± 0.0010 | 0.1359 ± 0.0272 |
| rung 1 · Erdős–Rényi | 0.4339 ± 0.0805 | 2.440 | 0.5661 ± 0.0805 | 0.9994 ± 0.0007 | 0.1323 ± 0.0187 |
| rung 2 · degree | 0.4620 ± 0.0706 | 2.284 | 0.5380 ± 0.0706 | 0.9972 ± 0.0051 | 0.1293 ± 0.0172 |
| rung 3 · clustering | 0.4671 ± 0.0915 | 2.261 | 0.5329 ± 0.0915 | 0.9972 ± 0.0042 | 0.1300 ± 0.0196 |
| rung 4 · modularity | 0.4544 ± 0.0695 | 2.242 | 0.5456 ± 0.0695 | 0.9965 ± 0.0038 | 0.1318 ± 0.0171 |

## `human_empirical`

| variant | bulk95 | sr_crit = 1/median(bulk95) | outlier-to-bulk gap | \|λ₂\|/\|λ₁\| | λ_max (raw) |
|---|---|---|---|---|---|
| connectome | 0.2509 ± 0.0000 | 3.985 | 0.7491 ± 0.0000 | 0.7846 ± 0.0000 | 0.2333 ± 0.0000 |
| weight-permuted | 0.4254 ± 0.0190 | 2.395 | 0.5746 ± 0.0190 | 0.9718 ± 0.0207 | 0.1402 ± 0.0054 |
| rung 0 · random | 0.4252 ± 0.0891 | 2.432 | 0.5748 ± 0.0891 | 0.9937 ± 0.0155 | 0.1364 ± 0.0263 |
| rung 1 · Erdős–Rényi | 0.4307 ± 0.0685 | 2.438 | 0.5693 ± 0.0685 | 0.9923 ± 0.0205 | 0.1330 ± 0.0171 |
| rung 2 · degree | 0.4449 ± 0.0410 | 2.301 | 0.5551 ± 0.0410 | 0.9708 ± 0.0534 | 0.1323 ± 0.0120 |
| rung 3 · clustering | 0.4133 ± 0.0324 | 2.371 | 0.5867 ± 0.0324 | 0.9456 ± 0.0526 | 0.1414 ± 0.0091 |
| rung 4 · modularity | 0.4441 ± 0.0499 | 2.241 | 0.5559 ± 0.0499 | 0.9765 ± 0.0296 | 0.1348 ± 0.0141 |

## Gates

- Reproduction vs committed `w_spectra.parquet`: **skipped**
- Documented N=448 headline values: **skipped**

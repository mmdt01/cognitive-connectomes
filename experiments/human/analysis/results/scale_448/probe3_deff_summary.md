# Probe 3 rebuilt -- ridge effective rank d_eff (human N=448)

d_eff = sum_i g_i / (g_i + alpha) over the design-Gram spectrum (trace of the ridge hat matrix; ESL). PR reported alongside as the contrast.

| analysis | task | y | scope | d_eff r_s | PR r_s | curvature r_s | n |
|---|---|---|---|---|---|---|---|
| (a) ladder ordering | mc | mc | empirical, sr>=3.05, median/variant (7 rungs) | +1.00 | +0.11 | -- | 7 |
| (a) ladder ordering | narma10 | nrmse | empirical, sr>=3.05, median/variant (7 rungs) | -0.96 | -1.00 | -- | 7 |
| (b) within-regime | mc | mc | empirical, sr>=3.05, pooled var/sr/seed | +1.00 | +0.31 | -- | 350 |
| (b) within-regime | narma10 | nrmse | empirical, sr>=3.05, pooled var/sr/seed | -0.71 | -0.74 | -- | 350 |
| (c) task-axis (within-empirical) | lorenz | vpt | empirical, sr>=3.05, pooled | +0.03 | +0.02 | -0.04 | 350 |
| (c) task-axis (pooled conditions) | lorenz | vpt | all conditions, sr>=3.05, pooled | -0.67 | +0.58 | -0.78 | 1050 |
| (d) sign-gating control (gaussian) | mc | mc | gaussian, sr>=3.05, median/variant (7 rungs) | +0.07 | +0.46 | -- | 7 |
| (d) sign-gating control (gaussian) | narma10 | nrmse | gaussian, sr>=3.05, median/variant (7 rungs) | -0.71 | -0.18 | -- | 7 |

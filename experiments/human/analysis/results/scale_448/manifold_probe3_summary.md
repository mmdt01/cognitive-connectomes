# Manifold Probe 3 -- geometry -> performance (human N=448)

## Pooled Spearman r (geometry vs primary performance, supercritical)

| task | performance | geometry | r_s | n |
|---|---|---|---|---|
| mc | mc | pr | +0.41 | 9660 |
| mc | mc | mean_curvature | +0.04 | 9660 |
| mc | mc | spectral_entropy | +0.36 | 9660 |
| narma10 | nrmse | pr | -0.09 | 9660 |
| narma10 | nrmse | mean_curvature | -0.39 | 9660 |
| narma10 | nrmse | spectral_entropy | -0.02 | 9660 |
| lorenz | vpt | pr | +0.54 | 9660 |
| lorenz | vpt | mean_curvature | -0.84 | 9660 |
| lorenz | vpt | spectral_entropy | +0.58 | 9660 |

## Gap-tracking Spearman (connectome-degree geometry gap vs performance gap, supercritical)

| task | dPR vs dPerf | dStraight vs dPerf |
|---|---|---|
| mc | +0.22 | +0.58 |
| narma10 | +0.71 | +0.51 |
| lorenz | +0.33 | +0.20 |

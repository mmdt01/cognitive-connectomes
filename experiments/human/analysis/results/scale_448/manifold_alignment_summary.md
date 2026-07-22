# Manifold Probe 2 -- variance captured by top-10 basis vectors (connectome, supercritical op. point; seed medians)

harmonics = low-freq graph-Laplacian; wmodes = dominant |eigenvalue| of W; random = chance band. Higher = manifold lives in that basis.

| task | condition | sr | harmonics@10 | wmodes@10 | random@10 |
|---|---|---|---|---|---|
| mc | human_gaussian | 1.2632 | 0.02 | 0.04 | 0.02 |
| mc | human_empirical_signed | 2.5263 | 0.02 | 0.06 | 0.02 |
| mc | human_empirical | 3.0526 | 0.06 | 0.01 | 0.02 |
| narma10 | human_gaussian | 1.2632 | 0.01 | 0.89 | 0.02 |
| narma10 | human_empirical_signed | 2.5263 | 0.00 | 0.53 | 0.02 |
| narma10 | human_empirical | 3.0526 | 0.04 | 0.00 | 0.02 |
| lorenz | human_gaussian | 1.2632 | 0.01 | 0.52 | 0.02 |
| lorenz | human_empirical_signed | 2.5263 | 0.02 | 0.08 | 0.02 |
| lorenz | human_empirical | 3.0526 | 0.17 | 0.00 | 0.02 |

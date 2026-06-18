# C. elegans spectral metrics (seed-averaged)

Scale-invariant ratios of the eigenvalue bulk to the dominant mode |λ₁|. Lower bulk₉₅/mean = more compressed bulk = milder effective dynamics at matched spectral radius.


## v2a · undirected gaussian

| condition | variant | spectral_radius | lambda2_ratio | bulk95_ratio | mean_ratio | participation_ratio | n_critical |
|---|---|---|---|---|---|---|---|
| v2a | connectome | 12 | 0.971 | 0.731 | 0.289 | 187.500 | 3 |
| v2a | control (perm. wts) | 12 | 0.966 | 0.721 | 0.286 | 186.406 | 4 |
| v2a | rung 0 (random) | 10 | 0.979 | 0.855 | 0.396 | 210.304 | 9 |
| v2a | rung 1 (ER) | 9 | 0.986 | 0.863 | 0.400 | 209.988 | 10 |
| v2a | rung 2 (degree) | 12 | 0.973 | 0.735 | 0.292 | 185.951 | 4 |
| v2a | rung 3 (clustering) | 13 | 0.957 | 0.674 | 0.277 | 190.257 | 3 |
| v2a | rung 4 (modularity) | 12 | 0.974 | 0.742 | 0.292 | 186.668 | 4 |

## v2b · directed empirical

| condition | variant | spectral_radius | lambda2_ratio | bulk95_ratio | mean_ratio | participation_ratio | n_critical |
|---|---|---|---|---|---|---|---|
| v2b | connectome | 105 | 0.770 | 0.301 | 0.101 | 137.510 | 1 |
| v2b | control (perm. wts) | 87 | 0.701 | 0.383 | 0.166 | 183.184 | 1 |
| v2b | rung 0 (random) | 69 | 0.509 | 0.455 | 0.262 | 239.153 | 1 |
| v2b | rung 1 (ER) | 70 | 0.506 | 0.454 | 0.262 | 239.341 | 1 |
| v2b | rung 2 (degree) | 89 | 0.454 | 0.381 | 0.169 | 190.168 | 1 |
| v2b | rung 3 (clustering) | 89 | 0.666 | 0.373 | 0.166 | 183.778 | 1 |
| v2b | rung 4 (modularity) | 89 | 0.661 | 0.369 | 0.164 | 185.225 | 1 |

## v2d · directed signed

| condition | variant | spectral_radius | lambda2_ratio | bulk95_ratio | mean_ratio | participation_ratio | n_critical |
|---|---|---|---|---|---|---|---|
| v2d | connectome | 104 | 0.773 | 0.311 | 0.102 | 138.545 | 1 |
| v2d | control (perm. wts) | 83 | 0.684 | 0.403 | 0.173 | 185.235 | 1 |
| v2d | rung 0 (random) | 57 | 0.621 | 0.552 | 0.319 | 241.198 | 1 |
| v2d | rung 1 (ER) | 57 | 0.609 | 0.556 | 0.320 | 241.066 | 1 |
| v2d | rung 2 (degree) | 83 | 0.489 | 0.408 | 0.182 | 191.601 | 1 |
| v2d | rung 3 (clustering) | 83 | 0.673 | 0.397 | 0.176 | 185.719 | 1 |
| v2d | rung 4 (modularity) | 82 | 0.616 | 0.399 | 0.178 | 187.782 | 1 |

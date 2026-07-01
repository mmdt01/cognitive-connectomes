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

## v2ae_randsign · undirected empirical ±

| condition | variant | spectral_radius | lambda2_ratio | bulk95_ratio | mean_ratio | participation_ratio | n_critical |
|---|---|---|---|---|---|---|---|
| v2ae_randsign | connectome | 231 | 0.941 | 0.480 | 0.155 | 140.743 | 2 |
| v2ae_randsign | control (perm. wts) | 158 | 0.959 | 0.682 | 0.250 | 170.088 | 3 |
| v2ae_randsign | rung 0 (random) | 133 | 0.983 | 0.766 | 0.317 | 191.810 | 5 |
| v2ae_randsign | rung 1 (ER) | 129 | 0.986 | 0.779 | 0.324 | 191.815 | 6 |
| v2ae_randsign | rung 2 (degree) | 151 | 0.971 | 0.723 | 0.260 | 167.965 | 4 |
| v2ae_randsign | rung 3 (clustering) | 161 | 0.963 | 0.654 | 0.245 | 171.803 | 3 |
| v2ae_randsign | rung 4 (modularity) | 152 | 0.966 | 0.712 | 0.258 | 169.591 | 3 |

## v2ae · undirected empirical

| condition | variant | spectral_radius | lambda2_ratio | bulk95_ratio | mean_ratio | participation_ratio | n_critical |
|---|---|---|---|---|---|---|---|
| v2ae | connectome | 317 | 0.858 | 0.339 | 0.107 | 126.198 | 1 |
| v2ae | control (perm. wts) | 221 | 0.725 | 0.482 | 0.174 | 162.562 | 1 |
| v2ae | rung 0 (random) | 166 | 0.789 | 0.608 | 0.251 | 189.694 | 1 |
| v2ae | rung 1 (ER) | 163 | 0.784 | 0.612 | 0.254 | 189.765 | 1 |
| v2ae | rung 2 (degree) | 213 | 0.673 | 0.500 | 0.182 | 165.374 | 1 |
| v2ae | rung 3 (clustering) | 257 | 0.572 | 0.400 | 0.152 | 167.350 | 1 |
| v2ae | rung 4 (modularity) | 217 | 0.696 | 0.488 | 0.178 | 164.975 | 1 |

## v2bg · directed gaussian

| condition | variant | spectral_radius | lambda2_ratio | bulk95_ratio | mean_ratio | participation_ratio | n_critical |
|---|---|---|---|---|---|---|---|
| v2bg | connectome | 4 | 0.975 | 0.843 | 0.429 | 223.829 | 7 |
| v2bg | control (perm. wts) | 4 | 0.975 | 0.857 | 0.430 | 224.562 | 10 |
| v2bg | rung 0 (random) | 4 | 0.979 | 0.912 | 0.593 | 259.971 | 22 |
| v2bg | rung 1 (ER) | 4 | 0.984 | 0.931 | 0.607 | 260.548 | 29 |
| v2bg | rung 2 (degree) | 4 | 0.990 | 0.874 | 0.441 | 221.054 | 12 |
| v2bg | rung 3 (clustering) | 4 | 0.982 | 0.859 | 0.424 | 214.899 | 9 |
| v2bg | rung 4 (modularity) | 4 | 0.994 | 0.883 | 0.443 | 220.611 | 13 |

## v2b_randsign · directed empirical ±

| condition | variant | spectral_radius | lambda2_ratio | bulk95_ratio | mean_ratio | participation_ratio | n_critical |
|---|---|---|---|---|---|---|---|
| v2b_randsign | connectome | 55 | 0.872 | 0.550 | 0.198 | 174.130 | 2 |
| v2b_randsign | control (perm. wts) | 42 | 0.974 | 0.789 | 0.350 | 200.357 | 6 |
| v2b_randsign | rung 0 (random) | 37 | 0.980 | 0.871 | 0.500 | 243.141 | 14 |
| v2b_randsign | rung 1 (ER) | 35 | 0.985 | 0.916 | 0.525 | 243.795 | 20 |
| v2b_randsign | rung 2 (degree) | 40 | 1.000 | 0.842 | 0.372 | 197.995 | 10 |
| v2b_randsign | rung 3 (clustering) | 42 | 0.970 | 0.800 | 0.352 | 194.636 | 6 |
| v2b_randsign | rung 4 (modularity) | 40 | 0.999 | 0.848 | 0.369 | 196.391 | 11 |

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

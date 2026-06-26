# C. elegans weight-realization summary (connectome)

The same connectome under three realism conditions. `symmetric` encodes directionality (undirected ⇒ symmetric W); `frac_negative` the sign structure; `frac_real_eigenvalues` the spectral consequence (a symmetric matrix has an all-real spectrum).

| condition | topology | symmetric | n_edges | frac_negative | mean\|w\| | max\|w\| | \|λ₁\| | real-eig frac |
|---|---|---|---|---|---|---|---|---|
| v2a | undirected | True | 6000 | 0.521 | 0.80 | 3.9 | 11.86 | 1.00 |
| v2b | directed | False | 3669 | 0.000 | 5.67 | 75.0 | 105.14 | 0.17 |
| v2d | directed | False | 3669 | 0.036 | 5.67 | 75.0 | 103.94 | 0.18 |

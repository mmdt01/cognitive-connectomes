# C. elegans weight-realization summary (connectome)

The same connectome under three realism conditions. `symmetric` encodes directionality (undirected ⇒ symmetric W); `frac_negative` the sign structure; `frac_real_eigenvalues` the spectral consequence (a symmetric matrix has an all-real spectrum).

| condition | topology | symmetric | n_edges | frac_negative | mean\|w\| | max\|w\| | \|λ₁\| | real-eig frac |
|---|---|---|---|---|---|---|---|---|
| undirected_gaussian | undirected | True | 6000 | 0.521 | 0.80 | 3.9 | 11.86 | 1.00 |
| undirected_empirical_signed | undirected | True | 6000 | 0.478 | 6.93 | 75.0 | 238.26 | 1.00 |
| undirected_empirical | undirected | True | 6000 | 0.000 | 6.93 | 75.0 | 316.97 | 1.00 |
| directed_gaussian | directed | False | 3669 | 0.514 | 0.80 | 3.9 | 4.33 | 0.11 |
| directed_empirical_signed | directed | False | 3669 | 0.485 | 5.67 | 75.0 | 52.23 | 0.12 |
| directed_empirical | directed | False | 3669 | 0.000 | 5.67 | 75.0 | 105.14 | 0.17 |
| directed_empirical_dale | directed | False | 3669 | 0.036 | 5.67 | 75.0 | 103.94 | 0.18 |

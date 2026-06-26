# C. elegans structural metrics (directed topology, seed-averaged)

Graph descriptors of the binary mask (topology only, before weights). The connectome is one fixed graph; nulls are averaged over 10 seeds (± sem). Rungs 2-4 preserve the degree sequence exactly, so they match the connectome on degree-derived quantities; each higher rung restores one more descriptor.

| variant | edge count | density | global clustering (transitivity) | directed clustering (mean Fagiolo) | modularity Q (fixed partition) | reciprocity (bidirectional frac.) | mean path length | global efficiency |
|---|---|---|---|---|---|---|---|---|
| connectome | 3669 | 0.0409 | 0.252 | 0.245 | 0.440 | 0.365 | 3.077 | 0.347 |
| rung 0 (random) | 3652 ± 21.493 | 0.0407 ± 0.000 | 0.079 ± 0.001 | 0.041 ± 0.000 | -0.002 ± 0.002 | 0.041 ± 0.001 | 2.555 ± 0.004 | 0.422 ± 0.001 |
| rung 1 (ER) | 3669 ± 0.000 | 0.0409 ± 0.000 | 0.080 ± 0.000 | 0.041 ± 0.000 | -0.002 ± 0.003 | 0.042 ± 0.001 | 2.551 ± 0.001 | 0.423 ± 0.000 |
| rung 2 (degree) | 3669 ± 0.000 | 0.0409 ± 0.000 | 0.135 ± 0.001 | 0.077 ± 0.000 | -0.003 ± 0.002 | 0.069 ± 0.002 | 2.589 ± 0.002 | 0.411 ± 0.000 |
| rung 3 (clustering) | 3669 ± 0.000 | 0.0409 ± 0.000 | 0.178 ± 0.000 | 0.233 ± 0.000 | 0.133 ± 0.002 | 0.176 ± 0.001 | 2.773 ± 0.014 | 0.395 ± 0.001 |
| rung 4 (modularity) | 3669 ± 0.000 | 0.0409 ± 0.000 | 0.196 ± 0.001 | 0.152 ± 0.001 | 0.440 ± 0.000 | 0.141 ± 0.003 | 2.791 ± 0.004 | 0.371 ± 0.000 |

# Task B — extended N=448 sweep (σ → 8)

MC only, `f = 0`, 4 variants × 10 seeds × 21 σ points on the frozen 0.4 step. The **only** simulating step in E0.2.

**Overlap gate**: `passed` — 480 cells shared with the frozen capture; `bulk95` to 6.7e-16, `mean_gain` to 9.3e-15, `d_eff` to 1.8e-05 relative at σ > 0. The substrate and driven states reproduce at machine precision; `d_eff` reproduces to float64-on-different-hardware level.

## MC(α) — the α constraint, resolved

Task A could only sweep `d_eff`. Here the **same frozen evaluator** was re-run at each α, so `MC` and `d_eff` are matched at every grid point.

### The `d_eff` ↔ MC correspondence does not depend on α

| α | Spearman(`d_eff`, MC), supercritical |
|---|---|
| 1e-08 | +0.999 |
| 1e-06 | +0.999 |
| 1e-05 | +0.999 |
| 7e-05 | +0.999 |
| 1e-03 | +0.999 |

**This removes the constraint the task was worried about.** Raising α does not break the `d_eff`↔MC link, provided it is raised in both places — the correspondence is +0.999 across five orders of magnitude. α can therefore be chosen on other grounds.

### Supercritical MC ladder ordering (+1 = connectome highest)

| α | ordering | connectome | weight-perm. | degree | ER |
|---|---|---|---|---|---|
| 1e-08 | **+1.00** | 12.96 | 9.04 | 6.01 | 3.77 |
| 1e-06 | **+1.00** | 12.28 | 7.33 | 4.62 | 2.82 |
| 1e-05 | **+1.00** | 11.73 | 6.44 | 4.04 | 2.39 |
| 7e-05 | **+1.00** | 11.02 | 5.68 | 3.59 | 2.14 |
| 1e-03 | **+1.00** | 9.70 | 4.70 | 3.00 | 1.82 |

Perfect ordering at **every** α, with a large margin (12.3 vs 2.8 at the frozen α). The supercritical memory result is not a ridge artifact — confirming Task A's `d_eff`-only version on the actual task metric.

### Peak MC — the connectome is always the *worst*

| α | Connectome | Weight-permuted | Degree-matching | Erdős–Rényi |
|---|---|---|---|---|
| 1e-08 | 15.02 | 15.36 | 15.44 | 15.55 |
| 1e-06 | 14.54 | 14.64 | 14.32 | 14.72 |
| 1e-05 | 14.07 | 14.50 | 14.14 | 14.66 |
| 7e-05 | 13.33 | 14.09 | 13.79 | 14.12 |
| 1e-03 | 11.70 | 12.69 | 12.27 | 12.51 |

At its own optimum the connectome has the **lowest** memory capacity at every α — 15.02 against ER's 15.55 in the near-pseudoinverse limit (α = 1e-8), and still lowest at α = 1e-3. Exactly mirroring `d_eff` (E0.2 §4.3): no capacity advantage, anywhere.

### Reconciliation with Aceituno, Yan & Liu (arXiv:1707.02469)

They find *spread* eigenvalue modulus maximises memory under OLS/pseudoinverse. That is reproduced here: at α = 1e-8, peak MC orders **ER > degree > weight-permuted > connectome** — the exact reverse of the null ladder, spread-bulk substrates winning. And it is **not** overturned at any α in the grid.

So the two results are not in conflict and the difference is not α. They answer different questions about different parts of the σ axis: *spread wins at the peak*, *compact wins supercritically*. Aceituno et al. optimise the peak; the connectome's edge is that it still has usable memory where a spread-bulk substrate has none. That is the 'most robust, not best' claim, now demonstrated on MC itself rather than inferred from `d_eff`.

### The connectome's optimal σ moves with α; the nulls' does not

| α | Connectome | Weight-permuted | Degree-matching | Erdős–Rényi |
|---|---|---|---|---|
| 1e-08 | 2.4 | 1.2 | 1.2 | 1.2 |
| 1e-06 | 2.8 | 1.6 | 1.6 | 1.6 |
| 1e-05 | 3.2 | 1.6 | 1.6 | 1.6 |
| 7e-05 | 3.2 | 1.6 | 1.6 | 1.6 |
| 1e-03 | 3.6 | 1.6 | 1.6 | 1.6 |

The connectome's best σ shifts 2.4 → 3.6 as α rises four orders, while every null sits at 1.2–1.6 throughout. Its operating point is regularisation-sensitive in a way the nulls' is not — a loose end worth noting, not yet explained.


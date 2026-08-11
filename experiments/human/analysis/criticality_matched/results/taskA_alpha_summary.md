# Task A — `d_eff(α)`: is the ridge effective rank saturated?

Pure reanalysis of the frozen `covariance_spectra.parquet` (MC readout, `human_empirical`, 7 variants × 13 σ × 10 seeds) over 42 log-spaced α from 1e-10 to 1e2. **No reservoir simulated.**

## (a) Is α = 1e-6 in the saturated regime?

**Almost, but not for the connectome.** Peak `d_eff/N` at the frozen α:

| variant | peak `d_eff/N` | saturated (≥ 0.99)? |
|---|---|---|
| connectome | 0.9607 | **no** |
| modularity_rewire | 0.9927 | yes |
| clustering_rewire | 0.9935 | yes |
| connectome_weight_permuted | 0.9943 | yes |
| degree_rewire | 0.9955 | yes |
| erdos_renyi | 0.9958 | yes |
| random_gaussian | 0.9975 | yes |

Every null is at ≥ 0.993 of the ceiling at its peak; the connectome is at 0.961. So the peak comparison is ceiling-limited for the nulls and *nearly* so for the connectome — E0.2 §4.3's reading is confirmed from an independent direction.

## (b) Where do variants actually separate at their peak?

- Peak separation (max − min `d_eff/N` across variants) at α = 1e-6: **0.0369**
- Maximum separation **0.0877** at α = 7.0e-05
- α band retaining ≥ 50% of maximum separation: **[2.0e-06, 2.0e-02]**

The frozen α sits just *below* the band where the peak separates best; raising α ~70× would roughly double peak separation. Whether that is worth doing is answered by (d): no.

## (d) Does the ladder ordering hold across α — and where does it live?

Ordering is Spearman of variant-median `d_eff` against ladder rank, sign-flipped so **+1 = connectome highest** (the published direction).

| σ region | ordering at α = 1e-6 | spread (`d_eff`) | connectome top? |
|---|---|---|---|
| subcritical | -1.00 | 83.4 | no |
| near peak | +0.11 | 82.6 | no |
| supercritical | +0.93 | 351.9 | yes |
| all sigma | +0.96 | 154.7 | yes |

**The puzzle, resolved.** The published +1.00 MC-ladder ordering cannot be coming from peak `d_eff`, and it is not:

- **At the peak** (near-peak region) the ordering is **absent** (+0.11) — every variant is pinned at the ceiling, so there is nothing to order.
- **Subcritically** the ordering is **inverted** (-1.00): the connectome has the *fewest* usable directions. This is the same fact E0.2 found as the (now withdrawn) subcritical deficit.
- **Supercritically** the ordering is +0.93 with the largest spread of any region. **The result lives entirely in the decay region**, which is exactly the region Probe 3 selected (`σ ≥ 3.05`).

The ordering flips sign at σ ≈ 2.3 — between the last subcritical point and the first supercritical one. Reading it off a single σ, or off the peak, would give the wrong answer or no answer.

**And it is not a ridge artifact.** The supercritical ordering is flat across the whole α grid (1e-10 to 1e2); only the near-peak region moves with α, and it moves because raising α un-saturates the peak. So α does not create, destroy or reverse the effect — σ does.

## Recommendation for the N=1000 run: **keep α = 1e-6**

The task set a constraint: if α is raised to escape saturation it must be raised in the readout too, or `d_eff` stops being the readout's effective rank and the `d_eff`↔MC correspondence breaks. That trade does not need to be made, because the saturation is confined to the region the result does *not* live in. Concretely, at α = 1e-6 the supercritical region is already far from the ceiling — `d_eff/N` at σ = 6 is 0.72 (connectome), 0.13 (degree), 0.06 (ER). There is ample dynamic range exactly where the ordering is.

**So the worry that N=1000 'may simply saturate at ~997/1000 and answer nothing' does not apply to the measurement that matters.** It does apply to the peak: peak `d_eff` will be ceiling-limited at any N, and no N will make the peak comparison informative. The N=1000 run should therefore be read on the decay region, and `d_eff/N` should be plotted with the ceiling drawn so that stays visible.

If a separating *peak* is wanted for its own sake, α ≈ 7e-5 maximises it — but MC must then be recomputed at 7e-5 to keep the pair matched.

## Aceituno, Yan & Liu (arXiv:1707.02469)

They find *spread* eigenvalue modulus maximises memory under OLS/pseudoinverse; we find a *compact* bulk under ridge. The α sweep bears directly on this. As α → 0, `d_eff` → the design rank for **every** variant (all curves converge to `d_eff/N` ≈ 1 below α ≈ 1e-8), so in the pseudoinverse limit `d_eff` cannot discriminate substrates at all — memory differences there must come from conditioning, not from rank. The compact-bulk result is therefore a statement about the *ridge* regime specifically, and the two findings are not in contradiction so much as at different points on the same α axis. Settling it properly needs `MC(α)`, not `d_eff(α)` — see the feasibility note below.

## `MC(α)` — scoped, not skipped

- **d eff alpha sweep**: free -- frozen Gram eigenvalues suffice (this module)
- **mc alpha sweep**: needs the driven states, which are not persisted; requires re-running MC
- **cost if folded into task b**: near-zero marginal: one eigendecomposition of the per-lag Gram gives every alpha via w(alpha) = U diag(1/(g+alpha)) U^T X^T y
- **recommendation**: fold MC(alpha) into Task B's sigma=8 extension rather than running it standalone

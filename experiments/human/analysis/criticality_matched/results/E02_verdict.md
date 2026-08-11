# E0.2 — effective-criticality-matched memory panel: verdict

> **Sections 1–3 are a PRE-REGISTRATION.** They were written and fixed *before any
> E0.2 analysis code was written or run*, against E0.4's `bulk95` values only.
> Section 4 (the outcome) is appended afterwards and must be read against them. If
> the outcome contradicts the prediction, the prediction stands as written — it is
> not to be revised.
>
> Written: 8 August 2026. Code state at pre-registration: commit `b8ba26d`
> (working tree carrying the E0.4 package, untracked).

---

## 1. The question

The memory advantage `dD = d_eff(connectome) − d_eff(ER)` was computed at matched
**nominal** spectral radius. Because each substrate's `W` is normalised by its own
`|λ₁|`, and the substrates have very different outlier-to-bulk gaps, matching on
nominal `sr` does **not** match effective criticality. E0.2 asks whether the
advantage survives when the comparison is made on an axis that does.

## 2. Why the concern is well-founded — the pre-registered arithmetic

From E0.4 (human `human_empirical`, N=448, 10 seeds):

| variant | `bulk95` | `sr_crit = 1/bulk95` |
|---|---|---|
| connectome | 0.3249 | 3.078 |
| Erdős–Rényi | 0.5509 | 1.815 |

The wedge opens at nominal `sr ≈ 2.4`. At that nominal radius:

- connectome `sr · bulk95` = **0.780** — still **subcritical**
- Erdős–Rényi `sr · bulk95` = **1.322** — already **supercritical**

So at the point where the memory advantage appears, the two substrates are on
opposite sides of criticality. The wedge opens approximately where **ER's** bulk
crosses 1, which is the signature a normalisation artifact would have.

## 3. The pre-registered prediction

**Matched on `sr · bulk95`, the wedge shrinks substantially or vanishes.**

Recorded commitments:

1. **Primary axis: `sr · bulk95`.** Purely structural, monotone in `sr` (`bulk95` is
   a per-variant, per-seed constant), computable from E0.4 alone. The verdict is
   decided on this axis.
2. **Secondary axis: `σ_eff = bulk95 · sr · ⟨1−x²⟩`.** Reported as a *parametric
   trajectory* traced by `sr`, with the fold retained and marked. `σ_eff` is
   non-monotone in `sr` (it peaks and turns over as the tanh gain collapses), so it
   cannot serve as a matching grid; the fold is a finding, not a nuisance, and is not
   to be removed by restricting to one branch.
3. **Overlap region: `sr · bulk95` ∈ [0, 1.949]** at N=448 over the swept
   `sr ∈ [0, 6]`, bounded by the connectome (smallest `bulk95`, shortest reach). It
   spans criticality comfortably. **No extrapolation beyond it.** Any region without
   genuine coverage for every compared variant is masked and marked.
4. **Per-seed then aggregate.** Interpolate `d_eff` onto the common grid within each
   seed, then aggregate across seeds — not the reverse. Required here because
   `bulk95` for a resampling null is extreme-value noisy (E0.4 §5), so each null seed
   carries its own x-axis. The connectome's `bulk95` has zero seed spread: it is one
   fixed graph.
5. **Interpolation sensitivity.** Linear and cubic must give the same answer; if they
   do not, that is reported rather than resolved by choosing one.
6. **`bulk95` source.** `phase_cells.parquet`'s own per-row `bulk95` column, for the
   cells of that file — not recomputed values (E0.4 §6 portability caveat).
7. **No tuning toward the wedge.** The analysis is not to be adjusted, re-binned or
   re-scoped in response to seeing the wedge shrink. A clean "it does not survive" is
   a valid and valuable outcome.

**Scope of this verdict:** the `f = 0` cut — the non-negative substrate, which is
where the real macro-scale connectome sits and where the memory result is stated.
The full `(f, sr)` heatmap is a separate, later extension.

## 4. Outcome

*Run 2026-08-11 09:37 UTC. Code: `b8ba26d`. Cells from `taskB_extended` — 21 σ points to σ = 8, variants ['connectome', 'connectome_weight_permuted', 'degree_rewire', 'erdos_renyi'].*

### 4.0 Gates

- **Source agreement**: `passed` — `phase_cells.parquet` vs `probe3_deff.parquet`, 120 shared cells at sr = [0.0, 2.0, 6.0], identical ridge `alpha` = 1e-06, max relative difference 1.8e-05. The two sources are the same number.
- **f=0 identity**: `d_eff` is bit-identical across all draws and both sign modes, as it must be when the sign transform is the identity.

### 4.1 Verdict — the advantage **partially survives**, and the matched peak is now measured

| quantity | nominal σ | effective criticality | change |
|---|---|---|---|
| peak `dD` | +343.3 at σ = 4.47 | +196.5 at σ·bulk95 = 1.95 | **57% retained** |
| most negative `dD` | -217.4 at σ = 1.53 | -24.0 at σ·bulk95 = 0.93 | **89% of the deficit removed** |
| fraction of axis with `dD` > 0 | 69% | 77% | — |

**It does not vanish.** Matched on `σ · bulk95` the connectome still holds a substantial memory advantage over ER — peak `dD` = +196.5, which is 57% of the nominal-axis figure. The pre-registered prediction (§3) was that the wedge would *shrink substantially or vanish*; it shrank substantially. The prediction is **partially confirmed**, and the 'vanishes' branch is **rejected**.

**And the peak is a measurement, not a bound.** `dD` rises to +196.5 at σ·bulk95 = 1.949 and then *declines*, reaching +155.5 at the top of the overlap (σ·bulk95 = 2.599). The matched advantage therefore has an interior optimum in effective criticality — it is not monotonically increasing, and 57% is the retained fraction at the true peak rather than a lower bound on an unobserved one. **Task B resolved this.** Extending the sweep to σ = 8 moved the overlap to σ·bulk95 ≤ 2.599, and the matched peak is now **interior** to it (at 1.949), so the figure below is a measurement rather than a lower bound.

**The result in the other direction is larger than the one predicted.** The connectome's *subcritical deficit* — the claim that it is markedly worse than ER below σ ≈ 2.4 — is almost entirely a normalisation artifact: the most negative `dD` collapses from -217.4 to -24.0, i.e. 89% of it disappears once the substrates are compared at matched effective criticality. At low effective criticality the connectome is in fact marginally *better*. Any statement that the connectome is subcritically worse should be withdrawn or restated as an artifact of nominal-σ matching.

### 4.2 Why the shapes differ

At matched effective criticality the two substrates sit at very different nominal radii — the connectome always higher, because its bulk is more compressed:

| σ·bulk95 | connectome σ | ER σ |
|---|---|---|
| 0.78 | 2.40 | 1.41 |
| 1.00 | 3.08 | 1.81 |
| 1.36 | 4.19 | 2.46 |
| 2.60 | 8.00 | 4.70 |

The nominal panel compared both substrates at the same σ (peak at σ = 4.47), where ER has long since collapsed. The matched panel compares them at the same *effective* criticality, which puts the connectome at a much higher nominal σ than the null — a real advantage still, but a smaller one, and reached for a different reason.

### 4.3 Ceiling — read every number against it

| variant | max `d_eff` | as fraction of N |
|---|---|---|
| Connectome | 432.4 | 96.5% |
| Weight-permuted | 445.7 | 99.5% |
| Degree-matching | 444.7 | 99.3% |
| Erdős–Rényi | 446.6 | 99.7% |

All three variants come within a few percent of the hard ceiling `d_eff = N`, and ER effectively reaches it. So part of the nominal-axis wedge is ER *falling off a ceiling it was saturating* rather than the connectome gaining anything. This is exactly the finite-size concern the N=1000 run exists to settle, and it is not resolved here.

**On the matched axis the three curves are nearly the same curve.** They rise together, all reach the ceiling, and separate only on the way down:

| variant | peak `d_eff` | at σ·bulk95 | `d_eff` at top of overlap |
|---|---|---|---|
| Connectome | 432.4 | 1.04 | 204.9 |
| Weight-permuted | 445.7 | 0.93 | 126.8 |
| Degree-matching | 444.7 | 0.91 | 96.4 |
| Erdős–Rényi | 446.6 | 0.97 | 49.5 |

This reframes the result. Matched on effective criticality, the connectome does **not** have a higher memory ceiling — every variant saturates at essentially the same peak, and at N=448 that peak is the finite-size ceiling itself, so it is unresolvable. What differs is the **decay rate past the peak**: the connectome retains readout dimensionality further into the supercritical regime while the nulls shed it. The matched memory advantage is therefore a *robustness* result, not a *capacity* result — which is the framing the rest of the programme already uses ('most robust, not best'), now established on the correct axis rather than assumed.

### 4.4 Robustness

- **nominal axis**, peak `dD` by interpolation: linear +343.3, cubic +344.1 (spread 0.8, 0.2%). Linear and cubic agree; the conclusion does not depend on the choice.
- **effective axis**, peak `dD` by interpolation: linear +196.5, cubic +198.1 (spread 1.5, 0.8%). Linear and cubic agree; the conclusion does not depend on the choice.
- **Per-seed then aggregate** throughout, with `dD` formed within a seed (paired on `Win` and input series). Required because `bulk95` is extreme-value noisy for the resampling nulls (E0.4 §5).
- **No extrapolation.** The common grid is clipped to the range every (variant, seed) covers: σ·bulk95 ∈ [0.000, 2.599], 53% of the full swept range, with all 10 seeds present at every grid point.

### 4.5 The secondary axis, `σ_eff`

`σ_eff = bulk95 · σ · ⟨1−x²⟩` is **non-monotone in σ** and therefore cannot index a matched grid — each value is reached twice per variant. It is reported as a parametric trajectory with the fold retained:

| variant | `σ_eff` peak | at σ | reaches 1? |
|---|---|---|---|
| Connectome | 0.634 | 3.6 | **no** |
| Weight-permuted | 0.585 | 1.6 | **no** |
| Degree-matching | 0.573 | 1.6 | **no** |
| Erdős–Rényi | 0.611 | 1.6 | **no** |

**The variant-specific fold is direct evidence for Perron gain control.** The connectome turns over at σ = 3.6 while both nulls turn over at σ = 1.6. `σ_eff = bulk95 · σ · ⟨1−x²⟩` folds when the tanh gain falls faster than σ rises, so the turning point *is* the point at which the substrate's own gain collapse overtakes its linear growth. The connectome's compact bulk keeps its states off saturation for more than twice as much σ as the nulls manage. This is a mechanism result, not a scoping caveat.

**But it means `σ·bulk95` matches the linear operator, not the dynamics.** Backing the gain out at each variant's fold:

| variant | fold at σ | `σ_eff` there | implied gain ⟨1−x²⟩ |
|---|---|---|---|
| Connectome | 3.6 | 0.634 | 0.542 |
| Weight-permuted | 1.6 | 0.585 | 0.703 |
| Degree-matching | 1.6 | 0.573 | 0.671 |
| Erdős–Rényi | 1.6 | 0.611 | 0.690 |

So at matched `σ·bulk95` the substrates sit at materially different *realised* gain (≈0.54 for the connectome at its fold against ≈0.69 for ER at its own). **This is not to be matched away** — the gain difference is part of the mechanism the compact bulk produces, and removing it would remove the effect being measured. It does mean the phrase "matched effective criticality" must be read narrowly: the *linear operator* is matched, the *dynamics* are not, and any claim that the two substrates are "in the same regime" at a matched x is stronger than the data supports.

Finally, **`σ_eff` never reaches 1 on MC driven states** for any variant — it peaks around 0.57–0.63. The '`σ_eff` crossing 1' criterion from the phase diagram is a property of the *Lorenz* driven states, not the memory ones, and must not be carried across panels.

### 4.6 Handoff — the N=1000 run configuration this implies

From E0.4, at N=1000: connectome `bulk95` = 0.2509 (`sr_crit` = 3.985), ER `bulk95` = 0.4102 (`sr_crit` = 2.438).

**Sweep `σ ∈ [0, 8]`, MC only, `f = 0`, variants {connectome, weight-permuted, degree, ER}.** In the two coordinate systems:

| | nominal σ | σ·bulk95 (connectome) | σ·bulk95 (ER) |
|---|---|---|---|
| lower bound | 0 | 0 | 0 |
| connectome critical | 3.99 | 1.00 | 1.63 |
| ER critical | 2.44 | 0.61 | 1.00 |
| upper bound | 8.00 | 2.007 | 3.282 |

The binding constraint is the connectome (smallest `bulk95`, shortest reach): σ = 7.97 is needed for σ·bulk95 = 2.0, so **σ_max = 8** gives a usable overlap of [0, 2.007] — comparable headroom to N=448 and enough to get past the point where the N=448 analysis was censored.

**The wedge lives supercritically in matched coordinates**, so the grid must be dense above σ·bulk95 ≈ 1. Concentrate points in σ ∈ [4.0, 8] for the connectome; a uniform nominal grid wastes most of its points below criticality.

Carry forward from the roadmap's §2b pre-flight, unchanged and still required: raise `T` to preserve `T_eff/N`, reparameterise the ridge `alpha` with `T_eff`, re-run N=448 under the new `T`/`alpha` first as the control, and report `d_eff / N` with the ceiling drawn (§4.3 above shows why).

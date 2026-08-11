# E0.4 — spectral characterisation and `bulk95` (human SC)

Eigendecomposition of the recurrent matrix `W` across the full null ladder, at N = 448 and 1000, 10 seeds per cell. **No reservoir simulation.**

`bulk95 = percentile(|lambda|, 95) / |lambda_1|, over the FULL spectrum of the un-rescaled recurrent matrix W (the Perron outlier is included in the percentile population). Computed by src.analysis.spectral.recurrent_spectrum as `bulk95_radius` on the normalised base W / |lambda_1|; identical formula to spectral_metrics' `bulk95_ratio`.`

`sr_crit = 1 / median_over_seeds(bulk95). The median is used rather than the mean because 1/x is convex: mean(1/bulk95) > 1/mean(bulk95) (Jensen), so a per-seed mean of 1/bulk95 is biased UPWARD -- by up to 0.087 at N=1000. Under the median the two computation orders agree to <= 0.0014, so sr_crit can be reproduced by inverting the reported central bulk95.`


## 1. Headline — `human_empirical` (the non-negative, f=0 substrate)

| variant | bulk95 (N=448) | sr_crit (N=448) | bulk95 (N=1000) | sr_crit (N=1000) |
|---|---|---|---|---|
| connectome | 0.3249 ± 0.0000 | 3.078 | 0.2509 ± 0.0000 | 3.985 |
| weight-permuted | 0.5120 ± 0.0323 | 1.922 | 0.4254 ± 0.0190 | 2.395 |
| rung 2 · degree | 0.5238 ± 0.0534 | 1.873 | 0.4449 ± 0.0410 | 2.301 |
| rung 1 · Erdős–Rényi | 0.5509 ± 0.0448 | 1.807 | 0.4307 ± 0.0685 | 2.438 |
| rung 0 · random | 0.5457 ± 0.0438 | 1.861 | 0.4252 ± 0.0891 | 2.432 |
| rung 3 · clustering | 0.4888 ± 0.0378 | 2.081 | 0.4133 ± 0.0324 | 2.371 |
| rung 4 · modularity | 0.5150 ± 0.0176 | 1.952 | 0.4441 ± 0.0499 | 2.241 |

## 2. Gates

**N=448** — reproduction vs committed `w_spectra.parquet`: `passed` (210 cells, worst 1.2e-14); documented headline values: `passed`.
**N=1000** — reproduction vs committed `w_spectra.parquet`: `skipped`; documented headline values: `skipped`.

## 3. `bulk95` depends on the sign fraction `f`

Signing edges reshapes the spectrum, so any effective-criticality reindex of the **full (f, sr) panel** must use each cell's own `bulk95`, not one constant per variant. Values at `f` = 0 / 0.25 / 0.5, `stratified` targeting:


**N=448**

| sign mode | variant | f=0 | f=0.25 | f=0.5 |
|---|---|---|---|---|
| `dale` | connectome | 0.3249 | 0.3529 | 0.3747 |
| `dale` | weight-permuted | 0.5120 | 0.4562 | 0.4164 |
| `dale` | rung 2 · degree | 0.5238 | 0.4932 | 0.4479 |
| `dale` | rung 1 · Erdős–Rényi | 0.5509 | 0.5144 | 0.4520 |
| `edge` | connectome | 0.3249 | 0.3969 | 0.4033 |
| `edge` | weight-permuted | 0.5120 | 0.5251 | 0.5244 |
| `edge` | rung 2 · degree | 0.5238 | 0.5626 | 0.5628 |
| `edge` | rung 1 · Erdős–Rényi | 0.5509 | 0.5650 | 0.5637 |

**N=1000**

| sign mode | variant | f=0 | f=0.25 | f=0.5 |
|---|---|---|---|---|
| `dale` | connectome | 0.2509 | 0.2648 | 0.2610 |
| `dale` | weight-permuted | 0.4254 | 0.3625 | 0.3233 |
| `dale` | rung 2 · degree | 0.4449 | 0.4012 | 0.3621 |
| `dale` | rung 1 · Erdős–Rényi | 0.4307 | 0.4055 | 0.3541 |
| `edge` | connectome | 0.2509 | 0.2818 | 0.2830 |
| `edge` | weight-permuted | 0.4254 | 0.4262 | 0.4247 |
| `edge` | rung 2 · degree | 0.4449 | 0.4618 | 0.4617 |
| `edge` | rung 1 · Erdős–Rényi | 0.4307 | 0.4343 | 0.4340 |

## 4. Normality diagnostic — is the sign axis a pure sign axis?

`non_normality = ||WᵀW − WWᵀ||_F / ||W||_F²` (0 ⟺ normal; symmetric ⇒ normal). Mean over seeds × draws, `stratified` targeting.


**N=448**

- **`dale`: non-normality rises with `f`** (0 at f=0 to 0.156 at f=0.5; W symmetric in only 0% of f>0 cells). Per variant, f=0→0.5: connectome 0.000→0.156; weight-permuted 0.000→0.087; rung 2 · degree 0.000→0.077; rung 1 · Erdős–Rényi 0.000→0.068. **This is a confound: on the Dale axis, sign fraction and non-normality co-vary, and they do so *unequally across variants* — the connectome becomes roughly twice as non-normal as its nulls at matched `f`.**
- **`edge`: normal at every `f`** (max non-normality 0.0e+00; W symmetric in 100% of cells). The edge transform flips an undirected edge and mirrors it, so symmetry — and therefore normality — is exactly preserved. **No confound: the edge sign axis is a pure sign axis.**

**N=1000**

- **`dale`: non-normality rises with `f`** (0 at f=0 to 0.127 at f=0.5; W symmetric in only 0% of f>0 cells). Per variant, f=0→0.5: connectome 0.000→0.127; weight-permuted 0.000→0.061; rung 2 · degree 0.000→0.051; rung 1 · Erdős–Rényi 0.000→0.045. **This is a confound: on the Dale axis, sign fraction and non-normality co-vary, and they do so *unequally across variants* — the connectome becomes roughly twice as non-normal as its nulls at matched `f`.**
- **`edge`: normal at every `f`** (max non-normality 0.0e+00; W symmetric in 100% of cells). The edge transform flips an undirected edge and mirrors it, so symmetry — and therefore normality — is exactly preserved. **No confound: the edge sign axis is a pure sign axis.**

**Reading.** Any Dale-arm result attributed to sign composition is also a result about departure from normality, and the two cannot be separated on this design. The edge arm is clean, so it is the right place to make mechanistic claims about sign per se; the Dale arm remains the biologically interpretable one, but its claims must be stated as "node-wise inhibition" (which entails non-normality) rather than "sign fraction" alone. Note the rise saturates by f≈0.2, so the biologically relevant ~20% inhibition sits near the knee, not on the plateau.

## 5. Seed variance — why `bulk95` spread grows with N

Spectral statistics should self-average, so a spread that *grows* with N looks wrong. Decomposing `bulk95 = (absolute bulk radius) / |λ₁|` shows the numerator behaves correctly and the noise is entirely in the normaliser.

| variant | N | rel. sd `bulk95` | rel. sd abs. bulk | rel. sd \|λ₁\| |
|---|---|---|---|---|
| weight-permuted | 448 | 0.060 | 0.019 | 0.060 |
| weight-permuted | 1000 | 0.042 | 0.016 | 0.037 |
| rung 2 · degree | 448 | 0.097 | 0.042 | 0.084 |
| rung 2 · degree | 1000 | 0.087 | 0.026 | 0.086 |
| rung 1 · Erdős–Rényi | 448 | 0.077 | 0.041 | 0.082 |
| rung 1 · Erdős–Rényi | 1000 | 0.151 | 0.035 | 0.122 |
| rung 0 · random | 448 | 0.076 | 0.038 | 0.075 |
| rung 0 · random | 1000 | 0.199 | 0.032 | 0.183 |

**Not a null-generation or density-matching fault.** Matching is exact at both scales — `validate_null` asserts it on every build, and a direct check over 10 seeds confirms every constrained rung at **both** N=448 and N=1000: Erdős–Rényi edge count 10/10, degree rewire degree sequence 10/10, clustering rewire 10/10, modularity rewire 10/10, all at the exact target edge count (5,323 at N=448; 10,784 at N=1000, density 0.0216). Only rung 0 (`random_gaussian`) varies its edge count, by design (density in expectation), and it does so *less* at N=1000 (rel sd 0.016 → 0.008).

**The absolute bulk does self-average**: its relative spread falls with N for every variant (column 3). The rise is in `|λ₁|`, and `bulk95` is a ratio to it — across seeds `corr(bulk95, |λ₁|)` runs −0.87 to −0.97.

**Mechanism: an extreme-value effect in the resampled weights.** The nulls draw weights with replacement from the empirical pool, and on a sparse non-negative graph `|λ₁|` is driven by the largest sampled weights: `corr(max sampled weight, |λ₁|)` = +0.85 to +0.95. The N=1000 pool is *heavier*-tailed than the N=448 pool (Hill α 2.49 → 2.28; max/mean 32 → 38), and at α ≈ 2.3 the sample maximum does not concentrate — so the max-weight spread grows with N (rel sd 0.113 → 0.158) and drags `|λ₁|` with it.

**The control confirms it.** `weight-permuted` *permutes* the connectome's exact weight multiset instead of resampling it, so its maximum weight is identical in every seed (max-weight rel sd exactly 0) — and it is the one variant whose `|λ₁|` spread *falls* with N (0.060 → 0.037), i.e. the one that self-averages as expected. The degree rewire sits in between: it resamples weights but keeps the hub structure, which anchors `|λ₁|` and damps the effect.

**Consequence.** `bulk95` for a resampling null is noisier than it looks, and its noise is dominated by a single sampled weight rather than by the bulk it describes. Per-seed effective-criticality axes (`sr · bulk95`) inherit that noise, so E0.2 must interpolate and aggregate per seed rather than pooling — which is the procedure already specified.

## 6. Caveats to carry forward

- **N=448 flip-pattern portability.** f>0 flip pattern is not machine-portable (unstable np.argsort tie order over a heavily-tied edge score); distributions agree. Use phase_cells.parquet's own bulk95 column when reindexing that file's cells. (f=0 exact to 6.7e-16; f>0 identical in 0/1800 cells; 60/60 groups agree in mean, worst 2.63 SE.)
- **The human substrate is symmetric**, so its spectrum is real to machine precision and the complex-plane scatter is degenerate (see `figS_complex_plane`). The eigenvalue *distribution* on the real axis is the informative view, and is what Figure 1 shows.

## 7. Handoff — the sr band the N=1000 run implies

At N=1000 the connectome turns critical at `sr_crit` = **3.985** (vs 3.078 at N=448), ER at 2.438 and degree at 2.301.

**The `[0, 6]` sweep is too short at this scale — extend it to `sr = 8`.** The comparison happens on the `sr · bulk95` axis, and the connectome has the smallest `bulk95` (0.2509), so it is the variant that runs out of axis first. Over `sr ∈ [0, 6]` it reaches only `sr · bulk95` = 1.505, leaving barely half a unit above criticality — too thin to resolve a wedge. Reaching an effective criticality of 2.0 (the headroom N=448 had) needs `sr = 2.0 / 0.2509` = **7.97**, so a sweep to `sr = 8` gives `sr · bulk95` ∈ [0, 2.007] and a comfortable overlap region.

Converting the band precisely is E0.2's job; the `bulk95` values it needs are in table 1 above.

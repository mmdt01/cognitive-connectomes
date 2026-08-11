# Figure 1 — caption

**Connectome weight placement compresses the eigenvalue bulk.**
Spectra of the recurrent matrix `W` for the human structural connectome and three
controls, human SC consensus, N = 448, 10 seeds per variant. Every
panel is drawn on the **normalised** matrix `W / |λ₁|`, the object the reservoir build
actually rescales, so the leading eigenvalue sits at 1 by construction and all
quantities are scale-invariant ratios. `W` is symmetric here, so the spectrum is real
(exactly 0 imaginary part); the complex-plane view is therefore degenerate and is
given separately as `figS_complex_plane`. No reservoir is simulated anywhere in this
figure — it is eigendecomposition only.

**The four substrates.** *Connectome*: the real weighted SC. *Weight-permuted*: the
connectome's exact topology carrying a random permutation of its own exact weight
multiset — so it differs from the connectome **only in which weight sits on which
edge**. *Degree-matching*: a degree-preserving rewire (rung 2), which randomises
topology while holding the exact degree sequence. *Erdős–Rényi*: a random graph with
the same edge count (rung 1). Reading left to right, the panels strip away first
weight placement, then degree structure, then topology.

**(a)–(d) Eigenvalue distributions.** Histogram (log density) of the normalised
eigenvalues for each substrate, pooled over seeds. The shaded band and dashed lines
mark ±`bulk95`, the radius containing 95% of the spectrum. The bulk is visibly
narrowest for the connectome (`bulk95` = 0.325) and broadens across the controls
(0.512, 0.524, 0.551). **The comparison that carries the claim is (a)
versus (b):** identical topology, identical weight values, yet the bulk widens by
58% once the weights are shuffled between edges. The
compression is therefore a property of *where the weights sit*, not of the graph's
topology alone and not of the weight distribution alone — which (c) and (d) confirm by
moving `bulk95` comparatively little further as degree structure and then topology are
destroyed in turn.

**(e) Cumulative spectrum.** Empirical CDF of `|λ| / |λ₁|` for the four substrates.
The dotted horizontal line marks the 95th percentile and the coloured dashed verticals
drop to each substrate's `bulk95`, so the panel *is* the definition of the statistic
rather than a summary of it: `bulk95` is simply where each curve crosses 0.95. The
connectome's curve rises far more steeply — the great majority of its modes are
strongly sub-dominant — while the three controls are tightly bunched, showing that the
connectome is the outlier and the controls are not meaningfully different from one
another.

**(f) `bulk95` per substrate, with the critical scale.** One point per seed (jittered
horizontally), the bar marking the mean; the right-hand axis converts to
`sr_crit = 1/bulk95`, the nominal spectral radius at which that substrate's bulk
reaches criticality. The connectome shows **zero seed-to-seed spread** — it is a single
fixed graph, and only the nulls are resampled, so its `bulk95` has no sampling
distribution. The gap between the connectome and every control exceeds the controls'
own spread by a wide margin. In `sr_crit` terms the connectome stays subcritical to
3.08 while the controls turn critical between 1.82 and 1.95,
which is why matching substrates on *nominal* spectral radius does not match them on
effective criticality.

**Definition.**

> bulk95 = percentile(|lambda|, 95) / |lambda_1|, over the FULL spectrum of the un-rescaled recurrent matrix W (the Perron outlier is included in the percentile population). Computed by src.analysis.spectral.recurrent_spectrum as `bulk95_radius` on the normalised base W / |lambda_1|; identical formula to spectral_metrics' `bulk95_ratio`. sr_crit = 1 / bulk95.

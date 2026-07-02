# C. elegans · substrate analyses

Characterisations of the connectome and its null ladder **as matrices/graphs**,
independent of any prediction task. This is the analysis tier: connectome-specific
drivers here build the variants via `SubstrateBuilder` and call the generic
`src/analysis/` tools; figures and metric tables land in `figures/` and `results/`.

The first analysis is **spectral**; the same pattern (a generic `src/analysis/*`
module + a thin driver here) extends to deeper topological analyses (degree
distributions, clustering, motifs, modularity, reciprocity).

## Spectral analysis

```bash
python -m experiments.celegans.analysis.spectral
```

Why it matters: the reservoir rescales every variant's `W` to a **matched nominal
spectral radius** (`|λ₁|`), so what differs between variants is the *shape* of the
spectrum below the top — how compressed the bulk is. That compression sets the
effective dynamics (memory, excitability) at the matched operating point, and is
the spectral basis of the prediction-task findings (the placement→memory axis).

**Metrics** (`src/analysis/spectral.py`), all scale-invariant ratios to `|λ₁|`:
`spectral_radius` (raw `|λ₁|`), `lambda2_ratio` (Perron gap), `bulk95_ratio`,
`mean_ratio` (bulk compression — lower = more compressed), `participation_ratio`
(effective # of modes), `n_critical` (modes within 0.9·|λ₁|).

**Outputs:**
- `figures/eigenvalue_spectra.png` — normalized eigenvalues (`λ/|λ₁|`) in the
  complex plane, conditions × the four key variants. The connectome shows a
  dominant mode plus a compressed bulk; nulls spread further out; undirected_gaussian variants are
  near-identical (explaining the undirected_gaussian null).
- `figures/spectral_compression.png` — `bulk₉₅/|λ₁|` and `mean|λ|/|λ₁|` bars per
  variant/condition: connectome most compressed, control ≈ degree, random least.
- `figures/magnitude_decay.png` — sorted `|λ|/|λ₁|` curves (steeper = more
  compressed).
- `results/spectral_metrics.csv` — seed-averaged metrics (all 7 variants × 7
  conditions, with sem). `results/spectral_metrics.md` — a compact table for slides.

**Headline (directed_empirical/directed_empirical_dale):** the connectome's bulk is the most compressed
(`bulk₉₅/|λ₁| ≈ 0.30` vs control/degree ≈ 0.38 vs random ≈ 0.46) with the largest
raw `|λ₁|`; it also carries a sizeable second mode (`λ₂/|λ₁| ≈ 0.77`, a 2-D
dominant subspace) over a deeply compressed bulk. undirected_gaussian variants are spectrally
identical. See `PREDICTION_TASKS_INTERPRETATION.md` §3 for how this grounds the
memory/placement mechanism.

## Structural (graph) analysis

```bash
python -m experiments.celegans.analysis.null_models
```

Why it matters: the spectral analysis above explains the **weight**-placement
axis; this one makes the **topology** axis — the null ladder itself — legible. It
characterises each variant's *binary mask* (topology only, before weights) on
classical graph descriptors, so you can read at a glance **what each rung
preserves vs destroys** relative to the connectome.

Scope: null masks depend only on topology, not the weight condition, so this uses
the **directed** topology (the directed_empirical/directed_empirical_dale family) alone. The placement control
`connectome_weight_permuted` permutes weights only — its mask equals the
connectome's, a no-op on graph structure — so it is omitted. That leaves the clean
ladder: connectome + rungs 0–4.

**Metrics** (`src/analysis/null_models.py`): `n_edges`, `density`,
`clustering_global` (transitivity of the undirected projection),
`clustering_directed_mean` (mean Fagiolo directed clustering — rung 3's target),
`modularity_q` (directed Q under the fixed Louvain partition — rung 4's target),
`reciprocity` (bidirectional-edge fraction), `mean_path_length` (mean geodesic
over reachable ordered pairs), `global_efficiency` (mean inverse geodesic).

**Outputs:**
- `figures/degree_distributions.png` — in/out-degree CCDFs (log-log). Rung 0–1
  (random/ER) fall off fast; rungs 2–4 preserve the degree sequence exactly, so
  they trace the connectome's heavy hub tail.
- `figures/structural_metrics.png` — per-metric bars, connectome as the dashed
  reference line, nulls as seed-mean ± std (with seed dots). The ladder climbs
  back toward the connectome as constraints accumulate.
- `figures/preservation_heatmap.png` — rung × metric staircase, normalised
  `0 = as-random, 1 = matches-connectome`. Green fills in left→right as each rung
  restores another descriptor.
- `figures/preservation_heatmap_slide.png` — the **recommended headline slide**:
  the same staircase, large-font / projection aspect ratio.
- `figures/adjacency_ladder.png` — the **"ladder of pictures"**: community-ordered
  adjacency spy-plots (connectome → rung 0 → rung 2 → rung 4). The connectome's
  diagonal community blocks dissolve into random speckle, survive only as hub
  stripes under degree preservation, then snap back at rung 4. The most intuitive
  single visual — no axes to read.
- `results/structural_metrics.csv` / `.md` — seed-averaged metrics (± sem) for
  every variant.

**Headline (directed topology):** the ladder is a clean staircase. Rung 2 (degree)
restores the degree distribution exactly but leaves clustering, modularity and
reciprocity near-random; rung 3 (clustering) lifts directed clustering to ≈ the
connectome (0.23 vs 0.25) but not Q; rung 4 (modularity) restores Q exactly (0.44,
preserved by construction) but only partial clustering. **Reciprocity is the
feature no rung recovers** — the connectome's 0.37 vs ≤0.18 for every null —
flagging a directed-motif structure the ladder never reaches.

## Weight-realization analysis

```bash
python -m experiments.celegans.analysis.realizations
```

Why it matters: the null-ladder analysis above walks the *topology* axis; this
one fixes the variant to the **connectome** and walks the *weight* axis across the
7-condition factorial. It makes the concrete sub-factors legible — **directionality**
(symmetric/normal vs asymmetric/non-normal), **tail** (homogeneous gaussian vs
heavy-tailed synapse counts), and **sign** (balanced ± vs all-positive vs sparse Dale
inhibition). The weight-distribution figure below is where the **sign × tail confound**
in a naive gaussian-vs-empirical contrast becomes visible at a glance.

**Tools:** `src/analysis/weight_structure.py` (weighted-matrix + distribution
helpers) plus `src/analysis/spectral.py` reused for the eigenvalue view.

**Outputs:**
- `figures/realization_weighted_matrices.png` — the **recommended headline**:
  community-ordered weighted matrices coloured by sign (red = +, blue = −). undirected_gaussian is
  symmetric across the diagonal and balanced ±; directed_empirical is asymmetric and all-red; directed_empirical_dale
  adds visible blue inhibition. The weight-axis analog of the adjacency ladder.
- `figures/realization_weight_distributions.png` — nonzero-weight histograms (log
  count): a symmetric gaussian bell → a one-sided heavy tail → the same tail with
  a negative lobe. The magnitude realism the matrix can't show.
- `figures/realization_eigenvalue_spectra.png` — the dynamical consequence:
  connectome spectra (`λ/|λ₁|`) sit on the real axis (symmetric ⇒ all-real), then
  collapse to a dominant Perron mode over a compressed complex bulk (all-positive),
  then spread slightly once Dale signs break positivity.
- `results/realization_summary.csv` / `.md` — per-condition weight + spectral
  summary (symmetry, `frac_negative`, mean/max `|w|`, `|λ₁|`, real-eigenvalue
  fraction).

**Headline:** the gaussian conditions are balanced (~52% −), light-tailed, and (for
undirected) real-spectrum; the empirical conditions are heavy-tailed (mean `|w|` 5.7,
max 75) and **all-positive**, with a large Perron radius. Crucially, that **non-negativity
— not the heavy tail — is what compresses the bulk**: the signed-empirical controls
(`*_empirical_signed`, identical magnitudes with balanced random signs) de-compress it
back toward the gaussian level. `directed_empirical_dale` differs from `directed_empirical`
by only 3.6% inhibition (26 neurons), so the two are near-identical — the "Dale ≈
all-positive for *C. elegans*" point. See `PREDICTION_TASKS_INTERPRETATION.md` §3.

## Conventions

Raw synapse-count weights (`matrix_config.WEIGHT_TRANSFORM`), matching the
prediction experiments. `figures/*.png` and `results/*.md`/`*.csv` are tracked;
`results/*.parquet` (if any) are gitignored.

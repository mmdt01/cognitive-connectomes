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
  dominant mode plus a compressed bulk; nulls spread further out; v2a variants are
  near-identical (explaining the v2a null).
- `figures/spectral_compression.png` — `bulk₉₅/|λ₁|` and `mean|λ|/|λ₁|` bars per
  variant/condition: connectome most compressed, control ≈ degree, random least.
- `figures/magnitude_decay.png` — sorted `|λ|/|λ₁|` curves (steeper = more
  compressed).
- `results/spectral_metrics.csv` — seed-averaged metrics (all 7 variants × 3
  conditions, with sem). `results/spectral_metrics.md` — a compact table for slides.

**Headline (v2b/v2d):** the connectome's bulk is the most compressed
(`bulk₉₅/|λ₁| ≈ 0.30` vs control/degree ≈ 0.38 vs random ≈ 0.46) with the largest
raw `|λ₁|`; it also carries a sizeable second mode (`λ₂/|λ₁| ≈ 0.77`, a 2-D
dominant subspace) over a deeply compressed bulk. v2a variants are spectrally
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
the **directed** topology (the v2b/v2d family) alone. The placement control
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

## Conventions

Raw synapse-count weights (`matrix_config.WEIGHT_TRANSFORM`), matching the
prediction experiments. `figures/*.png` and `results/*.md`/`*.csv` are tracked;
`results/*.parquet` (if any) are gitignored.

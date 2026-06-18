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

## Conventions

Raw synapse-count weights (`matrix_config.WEIGHT_TRANSFORM`), matching the
prediction experiments. `figures/*.png` and `results/*.md`/`*.csv` are tracked;
`results/*.parquet` (if any) are gitignored.

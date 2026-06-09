# C. elegans · NARMA-10 bridge experiment

Does the connectome's topology help on a task that demands **nonlinear temporal
computation** (NARMA-10 emulation), and does that hold as biological realism is
added? The connectome is compared against its full five-rung null ladder across
three realism conditions and a spectral-radius sweep.

This is the Phase-0 bridge: the same input-driven, readout-only paradigm as
memory capacity, but with the nonlinear computation MC lacked. It is the anchor
cell where the project's scale row and realism column meet.

## The matrix

| Axis | Values |
|---|---|
| Conditions | **v2a** undirected signed-Gaussian · **v2b** directed empirical · **v2d** directed empirical + Dale sign |
| Variants | connectome + rungs 0–4 (random, ER, degree, clustering, modularity) |
| Spectral radius | 20-point sweep, `linspace(0.0, 2.0, 20)` |
| Seeds | 10 |

3 × 6 × 20 × 10 = **3600 evaluations**. Each connectome is compared against its
own five-rung null ladder (directed nulls for v2b/v2d).

## Layout (modular scripts)

- `config.py` — every methodological choice (the audit trail).
- `substrates.py` — `SubstrateBuilder`: connectomes, empirical pool, Dale signs,
  partitions; generates + validates null masks (cached; directed masks shared by
  v2b/v2d); returns the weighted `W` per cell.
- `run_experiment.py` — runs the matrix → `results/results.parquet`,
  `results/null_diagnostics.parquet`, `results/manifest.json`.
- `stats.py` — permutation tests (connectome vs each null), Holm correction,
  Cohen's d on the performance direction → `results/stats.parquet`.
- `plots.py` — NRMSE-vs-sr panels + effect-size summary → `figures/`.
- `run_all.py` — orchestrator.

## Run

```bash
# from the repo root
python notebooks/celegans_narma10/run_all.py --smoke   # ~1 min end-to-end check
python notebooks/celegans_narma10/run_all.py           # full run (~25-30 min)

# or stage by stage
python notebooks/celegans_narma10/run_experiment.py
python notebooks/celegans_narma10/stats.py
python notebooks/celegans_narma10/plots.py
```

## Conventions & decisions

- **Weights:** raw integer synapse counts (no sqrt; `config.WEIGHT_TRANSFORM`
  switch). The connectome variant keeps its real weights (v2b/v2d) or fresh
  symmetric-Gaussian weights (v2a); nulls sample magnitudes from the empirical
  pool (v2b/v2d) or get fresh Gaussian weights (v2a).
- **Dale sign (v2d):** GABA-synthesizing neurons inhibitory (−1), all others
  excitatory (+1); the same sign vector is applied to the connectome and every
  null (see `SIGNED_WEIGHTS_METHODOLOGY.md`).
- **Seeds:** the construction seed drives mask/weights/`Win`; the NARMA input
  uses `seed + 1000`, so the connectome and each null are *paired* on an
  identical input at every seed.
- **Frozen reservoir hyperparameters:** `input_scaling=0.2`, `leak_rate=1.0`
  (tuned once on the v2a rung-0 baseline); only the spectral radius is swept.
- **Metric:** NARMA-10 NRMSE (lower is better). Cohen's d is defined so that
  **d > 0 ⇒ the connectome beats the null** (lower NRMSE) — matching the sign of
  the memory-capacity d-values despite NRMSE and MC pointing oppositely.

`results/*.parquet` are regenerable artefacts (gitignored); `figures/*.png` are
tracked.

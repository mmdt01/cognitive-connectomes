# C. elegans · NARMA-10 bridge experiment

Does the connectome's topology help on a task that demands **nonlinear temporal
computation** (NARMA-10 emulation), and does that hold as biological realism is
added? The connectome is compared against its full five-rung null ladder across
three realism conditions and a spectral-radius sweep.

This is the Phase-0 bridge: the same input-driven, readout-only paradigm as
memory capacity, but with the nonlinear computation MC lacked.

## The matrix

| Axis | Values |
|---|---|
| Conditions | **v2a** undirected gaussian · **v2b** directed empirical (non-negative) · **v2d** directed empirical (signed) |
| Variants | connectome + rungs 0–4 (random, ER, degree, clustering, modularity) |
| Spectral radius | 20-point sweep, `linspace(0.0, 2.0, 20)` |
| Seeds | 10 |

3 × 6 × 20 × 10 = **3600 evaluations**, each connectome vs its own five-rung
(directed for v2b/v2d) ladder.

## Where the code lives

This experiment is deliberately thin — the reusable machinery is shared:

- **Generic, task- & connectome-agnostic** (`src/experiment/`): `runner.py`
  (the matrix), `stats.py` (permutation tests, Holm, Cohen's d), `plots.py`
  (metric-vs-sr + effect-size figures), `config.py` (`ExperimentConfig`).
- **C. elegans-shared, task-agnostic** (`experiments/celegans/`):
  `substrates.py` (`SubstrateBuilder`) and `matrix_config.py` (conditions,
  variants, sr sweep, seeds, substrate/stats settings).
- **This task** (here): `task_config.py` (NARMA params, frozen reservoir
  hyperparameters, metric), `run.py` (wiring), `plot_demo.py` (intuition
  figure), and the `results/` + `figures/` outputs.

## Run

```bash
# from the repo root
python -m experiments.celegans.celegans_narma10.run            # full run (~10 min)
python -m experiments.celegans.celegans_narma10.run --smoke    # tiny check
python -m experiments.celegans.celegans_narma10.plot_demo      # intuition figure
```

`run.py` chains matrix → stats → figures. Outputs land in `results/` (parquet +
manifest) and `figures/`.

## Conventions

- **Weights:** raw integer synapse counts (`matrix_config.WEIGHT_TRANSFORM`).
  The connectome keeps its real weights (v2b/v2d) or gets fresh gaussian (v2a);
  nulls resample magnitudes from the empirical pool (v2b/v2d) or get fresh
  gaussian (v2a).
- **Dale sign (v2d):** GABA-synthesizing neurons inhibitory (−1), all others
  excitatory (+1); applied identically to connectome and nulls.
- **Seeds:** construction seed drives mask/weights/`Win`; the NARMA input uses
  `seed + 1000`, pairing connectome and each null on an identical input.
- **Frozen reservoir hyperparameters:** `input_scaling=0.2`, `leak_rate=1.0`
  (tuned once on the v2a rung-0 baseline); only the spectral radius is swept.
- **Metric:** NARMA-10 NRMSE (lower is better). Cohen's d is defined so that
  **d > 0 ⇒ the connectome beats the null**.

`results/*.parquet` are gitignored (regenerable); `figures/*.png` are tracked.

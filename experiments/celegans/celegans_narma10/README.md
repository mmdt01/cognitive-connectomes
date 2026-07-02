# C. elegans · NARMA-10 bridge experiment

Does the connectome's topology help on a task that demands **nonlinear temporal
computation** (NARMA-10 emulation), and does that hold as biological realism is
added? The connectome is compared against its full five-rung null ladder across
the 7-condition sign × tail × topology factorial and a wide spectral-radius sweep.

This is the Phase-0 bridge: the same input-driven, readout-only paradigm as
memory capacity, but with the nonlinear computation MC lacked.

## The matrix

| Axis | Values |
|---|---|
| Conditions | **7-condition sign × tail × topology factorial**: `undirected_gaussian`, `undirected_empirical_signed`, `undirected_empirical`, `directed_gaussian`, `directed_empirical_signed`, `directed_empirical`, `directed_empirical_dale` |
| Variants | connectome · **weight-placement control** · rungs 0–4 (random, ER, degree, clustering, modularity) |
| Spectral radius | 39-point wide sweep, `linspace(0.0, 4.0, 39)` |
| Seeds | 10 |

7 × 7 × 39 × 10 = **19,110 evaluations**, each connectome vs its own five-rung ladder
plus the weight-placement control.

**Finding (sign-primary).** NARMA's supercritical robustness — the connectome holds
NRMSE ~0.55 while every null climbs to ~0.80 — is driven **primarily by weight SIGN
(non-negativity / the Perron structure of all-positive weights), not directedness**. It
lives in the all-positive-empirical conditions (connectome−degree d **+8 to +10**) and
**collapses when the exact weights are signed** (`*_empirical_signed`, balanced random
±: undirected +10 → +0.5, directed +8 → +3.4). Directed structure adds a secondary
*stability-under-drive* residual that survives signing in the directed case; the heavy
tail alone (signed) does little. The **weight-placement control** decomposes `connectome
vs control` = placement and `control vs degree_rewire` = topology — both secondary to
sign. This supersedes the earlier "mostly topology" reading (the gaussian-vs-empirical
contrast conflated sign with tail). Full account in `PREDICTION_TASKS_INTERPRETATION.md`.

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
  The connectome keeps its real weights (directed_empirical/directed_empirical_dale) or gets fresh gaussian (undirected_gaussian);
  nulls resample magnitudes from the empirical pool (directed_empirical/directed_empirical_dale) or get fresh
  gaussian (undirected_gaussian).
- **Dale sign (directed_empirical_dale):** GABA-synthesizing neurons inhibitory (−1), all others
  excitatory (+1); applied identically to connectome and nulls.
- **Seeds:** construction seed drives mask/weights/`Win`; the NARMA input uses
  `seed + 1000`, pairing connectome and each null on an identical input.
- **Frozen reservoir hyperparameters:** `input_scaling=0.2`, `leak_rate=1.0`
  (tuned once on the undirected_gaussian rung-0 baseline); only the spectral radius is swept.
- **Metric:** NARMA-10 NRMSE (lower is better). Cohen's d is defined so that
  **d > 0 ⇒ the connectome beats the null**.

`results/*.parquet` are gitignored (regenerable); `figures/*.png` are tracked.

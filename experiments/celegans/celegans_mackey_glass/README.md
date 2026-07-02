# C. elegans · Mackey-Glass forecasting experiment

Does the connectome's topology help on **autonomous-system forecasting** — the
complement to NARMA's input-driven emulation — and does that hold as biological
realism is added? The reservoir is driven by the Mackey-Glass series `x(t)` and a
linear readout predicts `x(t+h)` `h` steps ahead. The connectome is compared
against its full five-rung null ladder across three realism conditions and a
spectral-radius sweep, at two forecast horizons.

This is the second prediction task (after the NARMA-10 bridge). It is **driven
(teacher-forced)**: the reservoir always sees the true `x(t)`, never its own
prediction. Closed-loop free-running is deliberately deferred to the Lorenz task;
the only intended change from the NARMA bridge is the task itself.

## The task

Mackey-Glass delay differential equation, canonical mild-chaos parameters
(`a=β=0.2, b=γ=0.1, n=10, τ=17`, RK4 step `h=1.0`):

```
dx/dt = a · x(t−τ) / (1 + x(t−τ)ⁿ) − b · x(t)
```

The local generator (`src/tasks/mackey_glass.py`) reproduces
`reservoirpy.datasets.mackey_glass` bit-for-bit (verified in the test suite); we
keep a local one for control over length, transient discard, normalisation, and a
reproducible per-seed initial history. The series is z-scored with **train-region
statistics only** before driving the reservoir.

## The matrix

| Axis | Values |
|---|---|
| Conditions | **undirected_gaussian** undirected gaussian · **directed_empirical** directed empirical (non-negative) · **directed_empirical_dale** directed empirical (signed) |
| Variants | connectome · **weight-placement control** · rungs 0–4 (random, ER, degree, clustering, modularity) |
| Spectral radius | 20-point sweep, `linspace(0.0, 2.0, 20)` |
| Seeds | 10 (each draws a different Mackey-Glass trajectory; connectome & nulls paired per seed) |
| Horizons | **h = 84** (canonical benchmark, moderate) and **h = 300** (chaos-limited, hard) |

3 × 7 × 20 × 10 = **4200 evaluations per horizon** (8400 total). The two horizons
reuse one `SubstrateBuilder`, so the directed null masks are generated once.

The **weight-placement control** (`connectome_weight_permuted`) keeps the
connectome's exact topology and exact weight multiset but permutes which edge
carries which weight (per seed). It decomposes the topology-vs-weights confound:
`connectome vs control` isolates **weight placement**, `control vs degree_rewire`
isolates **topology**. In undirected_gaussian (already random-weighted) it is a negative control.

## Where the code lives

This experiment is deliberately thin — the reusable machinery is shared:

- **Generic, task- & connectome-agnostic** (`src/experiment/`): `runner.py`
  (the matrix), `stats.py` (permutation tests, Holm, Cohen's d), `plots.py`
  (metric-vs-sr + effect-size figures), `config.py` (`ExperimentConfig`).
- **C. elegans-shared, task-agnostic** (`experiments/celegans/`):
  `substrates.py` (`SubstrateBuilder`) and `matrix_config.py` (conditions,
  variants, sr sweep, seeds, substrate/stats settings).
- **This task** (here): `task_config.py` (MG params, frozen reservoir
  hyperparameters, metric, the two horizons), `run.py` (wiring; loops the two
  horizons), `plot_demo.py` (intuition figure), and the `results/` + `figures/`
  outputs (one `h{horizon}/` subdir each).

## Run

```bash
# from the repo root
python -m experiments.celegans.celegans_mackey_glass.run            # full run, both horizons
python -m experiments.celegans.celegans_mackey_glass.run --smoke    # tiny check
python -m experiments.celegans.celegans_mackey_glass.plot_demo      # intuition figure
```

`run.py` chains matrix → stats → figures for each horizon. Outputs land in
`results/h{horizon}/` (parquet + manifest) and `figures/h{horizon}/`.

## Conventions

- **Weights:** raw integer synapse counts (`matrix_config.WEIGHT_TRANSFORM`),
  matching the NARMA bridge (one variable at a time = the task). The connectome
  keeps its real weights (directed_empirical/directed_empirical_dale) or gets fresh gaussian (undirected_gaussian); nulls resample
  magnitudes from the empirical pool (directed_empirical/directed_empirical_dale) or get fresh gaussian (undirected_gaussian).
- **Dale sign (directed_empirical_dale):** GABA-synthesizing neurons inhibitory (−1), all others
  excitatory (+1); applied identically to connectome and nulls.
- **Seeds:** construction seed drives mask/weights/`Win`; the MG initial history
  uses `seed + 1000`, pairing connectome and each null on an identical trajectory.
- **Frozen reservoir hyperparameters:** `input_scaling=0.5`, `leak_rate=0.3`
  (tuned once on the undirected_gaussian rung-0 baseline; the smooth MG series wants a far lower
  leak than NARMA's 1.0). Only the spectral radius is swept.
- **Metric:** NRMSE (lower is better). Cohen's d is defined so that
  **d > 0 ⇒ the connectome beats the null**.

## Caveats carried forward (from the NARMA bridge)

- **Topology vs weights (directed_empirical/directed_empirical_dale) — addressed by the `connectome_weight_permuted`
  control.** The connectome keeps its *real* weights while the rung nulls resample,
  conflating directed topology with the connectome's real weight placement. The
  control keeps the connectome's exact topology and weight multiset but permutes
  placement, decomposing the two. Probe finding (h=84, n=50): the connectome's
  supercritical deficit is **weight placement** (`connectome vs control` d ≈ −2 to
  −3); the topology leg (`control vs degree_rewire`) is null — consistent with undirected_gaussian.
- **Divergence-robustness.** Some supercritical reservoirs can blow up (huge or
  non-finite NRMSE → reported as no-skill); a median-based or NRMSE-capped
  statistic would harden the permutation tests against those outliers.
- **Driven, not free-running.** A teacher-forced single-scalar drive lets the
  reservoir reconstruct the delay embedding, so MG forecasting is comparatively
  easy at short/medium horizons — hence the long hard horizon. Autonomous
  free-running (the harder, more on-message setup) is the Lorenz task.

`results/*.parquet` are gitignored (regenerable); `figures/*.png` are tracked.

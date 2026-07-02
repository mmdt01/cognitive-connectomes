# C. elegans · Lorenz attractor experiment (closed-loop free-running)

The final and most on-message prediction task: can the connectome reservoir act
as a **world model** for a chaotic system — generating the Lorenz attractor
**autonomously**, with its own prediction fed back as its next input, no teacher
forcing? This is qualitatively harder than the two driven tasks (NARMA emulation,
Mackey-Glass forecasting), where the reservoir always sees the true signal: here
errors compound through the feedback loop, and a mildly-unstable reservoir
diverges. That fragility *is* the experiment — it is what the two metrics measure.

## The task

Lorenz '63, canonical chaotic parameters (`σ=10, ρ=28, β=8/3`, `λ_max ≈ 0.9056`):

```
dx/dt = σ(y − x)      dy/dt = x(ρ − z) − y      dz/dt = xy − βz
```

A local fixed-step **RK4** generator (`src/tasks/lorenz.py`, step `h=0.03`) gives
the reservoir a clean, constant-Δt one-step map to learn. `reservoirpy.datasets.
lorenz` instead uses adaptive `scipy.solve_ivp` (RK45) on a non-constant grid, so
the two **cannot** be bit-exact — and Lorenz chaos decorrelates any two
integrators within a few Lyapunov times regardless. The test suite therefore
cross-checks **short-horizon agreement** (tight over the first steps), not the
bit-exact identity the driven tasks could assert. The trajectory is z-scored
per-coordinate with **train-region statistics only**; the per-seed initial
condition is a small perturbation of `[1,1,1]`.

**Protocol (closed-loop).** Teacher-force the reservoir on the true trajectory and
fit a ridge readout `state(t) → s(t+1)` (predict the **next state directly**),
then synchronise on a short held-out segment and cut it loose to **free-run**: its
own 3-D output becomes its next 3-D input, stepped manually through the leaky-tanh
update with feedback.

> **Readout target — direct, not increment.** The increment form
> `s(t+1) = s(t) + readout(x)` was tried first (the standard small-Δt choice) but,
> at the connectome-fixed **N=300**, its small corrections let the free-run drift
> off the attractor and blow up — the climate metric sat at the divergence cap for
> *every* hyperparameter. Direct next-state prediction self-corrects toward the
> attractor each step, stays bounded, and makes climate discriminative (faithful
> nulls reach a climate of ~0.06). Logged here because it reverses an initial
> design choice.

## The two metrics (both reported)

One matrix cell yields **both**, so the matrix runs **once** and `stats`/`plots`
run once per metric over the shared `results.parquet`:

- **`vpt` — valid-prediction time (higher = better).** Mean over `n_windows`
  free-runs of the first step where the normalised error
  `‖pred − true‖ / rms(‖true‖)` exceeds `ε=0.4`, reported in **Lyapunov time**
  `t·λ_max`. A *stability* metric; bounded by the roll-out length (never blows up).
- **`climate_error` — attractor-climate fidelity (lower = better).** Mean over
  x/y/z of the **Wasserstein-1** distance between one long free-run's per-coordinate
  marginal and the true attractor's. A *fidelity* metric: a run can be stable yet
  collapse to a fixed point or limit cycle (right stability, wrong climate). A
  free-run that leaves the attractor → huge/∞ → capped at `10` (z-scored units) and
  counted in the divergence rate.

## The matrix

| Axis | Values |
|---|---|
| Conditions | **undirected_gaussian** undirected gaussian · **directed_empirical** directed empirical (non-negative) · **directed_empirical_dale** directed empirical (signed) |
| Variants | connectome · **weight-placement control** · rungs 0–4 (random, ER, degree, clustering, modularity) |
| Spectral radius | 20-point sweep, `linspace(0.0, 2.0, 20)` |
| Seeds | 10 (each draws a different Lorenz trajectory; connectome & nulls paired per seed) |

3 × 7 × 20 × 10 = **4200 evaluations** (each scored on both metrics).

The **weight-placement control** (`connectome_weight_permuted`) keeps the
connectome's exact topology and exact weight multiset but permutes which edge
carries which weight (per seed): `connectome vs control` isolates **weight
placement**, `control vs degree_rewire` isolates **topology**. In undirected_gaussian it is a
negative control.

## Where the code lives

Deliberately thin — the reusable machinery is shared:

- **Generic** (`src/experiment/`): `runner.py` (the matrix), `stats.py`
  (divergence-robust rank tests, Holm, Cliff's δ, Cohen's d, divergence rate),
  `plots.py`, `config.py`. *Lorenz touches:* `build_from_adjacency` gained an
  `input_dim` arg (3 channels here; default 1 leaves the driven tasks
  byte-identical); `stats`/`plots` output filenames are metric-tagged so the two
  metrics don't overwrite each other.
- **C. elegans-shared** (`experiments/celegans/`): `substrates.py`
  (`SubstrateBuilder`), `matrix_config.py` (conditions, variants, sweep, seeds) —
  used **unchanged**.
- **This task** (here): `task_config.py` (Lorenz params, frozen hyperparameters,
  both metrics' metadata), `run.py` (matrix once → stats+plots per metric),
  `plot_demo.py` (intuition figure), `results/` + `figures/`.

## Run

```bash
# from the repo root
python -m experiments.celegans.celegans_lorenz.run            # full run (~1–1.5 h)
python -m experiments.celegans.celegans_lorenz.run --smoke    # tiny check
python -m experiments.celegans.celegans_lorenz.plot_demo      # intuition figure
```

`run.py` runs the matrix once (under the `vpt` config, which carries
`climate_error` along), then chains stats → figures for each metric. Outputs:
`results/stats_<metric>.parquet`, `figures/<metric>_vs_spectral_radius.png`,
`figures/effect_sizes_<metric>_vs_spectral_radius.png`.

## Conventions

- **Weights:** raw integer synapse counts (`matrix_config.WEIGHT_TRANSFORM`),
  matching NARMA/MG (one variable at a time = the task). Connectome keeps its real
  weights (directed_empirical/directed_empirical_dale) or gets fresh gaussian (undirected_gaussian); nulls resample from the
  empirical pool (directed_empirical/directed_empirical_dale) or get fresh gaussian (undirected_gaussian).
- **Dale sign (directed_empirical_dale):** GABA-synthesizing neurons inhibitory (−1), others (+1);
  applied identically to connectome and nulls.
- **Seeds:** construction seed drives mask/weights/`Win`; the Lorenz trajectory
  uses `seed + 1000`, pairing connectome and each null on an identical trajectory.
- **Frozen reservoir hyperparameters:** `input_scaling=0.1`, `leak_rate=1.0`,
  `ridge_alpha=1e-7`, `n_train=10000` (tuned once on the undirected_gaussian rung-0 baseline;
  closed-loop free-running wants a far lower input scaling than the driven tasks).
  Only the spectral radius is swept.
- **Cohen's d** is defined so **d > 0 ⇒ the connectome beats the null**, on each
  metric's own direction.

## The pre-registered prediction

From `PREDICTION_TASKS_INTERPRETATION.md` §4 (low confidence): the connectome
should **trade fidelity for stability** — relatively divergence-resistant (decent
`vpt`) but a **less faithful attractor** (poor `climate`), its compressed spectrum
starving the dynamical richness needed to *sustain* chaos (collapse to a fixed
point / limit cycle). The falsifiable hook: **the connectome's ranking should
depend on the metric** (better on vpt, worse on climate). If both metrics agree,
the two-mechanism picture is wrong. As in both prior tasks, the connectome is
expected **not** to be best at the canonical operating point; any effect is a
supercritical-regime phenomenon, and the placement control decomposes it into
placement vs topology automatically.

`results/*.parquet` are gitignored (regenerable); `figures/*.png` are tracked.

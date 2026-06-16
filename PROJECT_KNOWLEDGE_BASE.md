# Cognitive Connectomes — Project Knowledge Base

A research project on connectome-constrained reservoir computing. Uses
empirically measured connectomes as the recurrent matrix of an echo-state
network and asks what biological connectivity contributes beyond random or
degree-matched baselines.

This document is the single canonical reference for the project. It is intended
to be loaded into fresh Claude conversations as the starting context. Companion
docs: `PROJECT_PLAN.md` (the forward plan), `NULL_MODELS_METHODOLOGY.md` and
`SIGNED_WEIGHTS_METHODOLOGY.md` (method references), `MACKEY_GLASS_KICKOFF.md`
(the next build's brief).

---

## 1. TL;DR

The central question: does the topology of biological connectomes — beyond
degree sequence — confer computational properties that random or degree-matched
null graphs do not?

On **memory capacity** (Jaeger MC) the answer is **no at canonical operating
points** (edge-of-chaos) and **yes in the supercritical regime**, where the
connectome maintains higher MC than its degree-preserving rewire. This effect
is **regime-independent on MC**: it reproduces across undirected signed-Gaussian
(v2a) and directed empirical (v2b) weights, and v2c attributes it to clustering
and/or modularity (degree-only mechanism ruled out).

The project has since turned the task axis from passive memory toward
**dynamical-system prediction** (north star: a connectome-as-JEPA world model).
The **Phase-0 NARMA-10 bridge is complete**, and the prediction picture is more
nuanced than MC. The supercritical advantage is **regime-dependent** on NARMA:
strong in the directed empirically-weighted conditions (v2b/v2d — the connectome
beats *every* null including clustering and modularity, Cohen's d up to ~+10)
but **absent in the clean undirected-topology condition (v2a)**. It manifests as
supercritical *robustness*, not superiority (nulls are better at canonical sr),
and in v2b/v2d it is **confounded with the connectome's real weight placement**
(nulls resample weights; only v2a is a clean topology-only test). Next builds:
**Mackey-Glass** then **Lorenz**.

---

## 2. Research motivation

Reservoir computing uses a fixed random recurrent matrix as a computational
substrate; readouts are linearly trained. The question for neuroscience-inspired
ML: does a *real* biological connectome work better than a random matrix, and
which structural features matter? Connectomes are the substrate of biological
cognition; if their topology is computationally meaningful beyond random or
degree-matched baselines, this informs both network architecture and what the
brain's wiring is doing.

The *C. elegans* connectome (Cook et al. 2019, *Nature* 571:63–71) is the only
complete cell-resolution wiring diagram of a behaving animal. At N≈300 it is
computationally tractable and partially understood functionally — the obvious
starting point. Two literature anchors (Suárez 2021, Damicelli 2022) show
connectome-constrained RC beating random RC, primarily through anatomical I/O
routing. This project takes a more granular route: establish the controlled
topology comparison first (does the recurrence itself matter?), then add
biological features one at a time.

---

## 3. Methodological principles

Load-bearing and non-negotiable.

- **Continuous weights everywhere, never binary.** The recurrent matrix W is
  always continuous-valued. Binary topology is the *mask*; continuous values are
  applied via a weight scheme. (v1 violated this and cost the whole v2 cleanup.)
- **One variable at a time.** Each experiment changes exactly one thing relative
  to the previous (v1 → v2a → v2c → v2b → v2d → prediction tasks). Multi-variable
  changes silently confound attribution.
- **Null ladder, not single null.** The connectome is compared against a graded
  ladder of nulls, each preserving more structure than the last (§5). It
  "clears" a rung if it beats that null statistically; failing means the
  preserved feature is sufficient to explain the result.
- **Honest null reporting.** Null results are reported plainly; effect size and
  significance together; confounds surfaced even when they weaken the headline.
- **Tooling decisions are experimental variables.** BLAS threads, spectral-radius
  method, RNG seed derivation, weight-scheme symmetry — all logged.
- **Stage-0 config is the audit trail.** Every experiment pins every
  methodological choice in one place (`config.py` / the `EXPERIMENT` dict).

---

## 4. Repository structure

Repo: `~/imperial/thesis/cognitive-connectomes/`. Linux/WSL2; Python 3.12 venv
at `.venv/`; editable-installed via `pyproject.toml` (only `src*` is packaged).

```
cognitive-connectomes/
├── PROJECT_KNOWLEDGE_BASE.md / PROJECT_PLAN.md / IMPLEMENTATION_PHASE0_BRIDGE.md
├── NULL_MODELS_METHODOLOGY.md / SIGNED_WEIGHTS_METHODOLOGY.md / MACKEY_GLASS_KICKOFF.md
├── data/
│   ├── cook2019_connectome.xlsx              (Cook 2019 SI, corrected July 2020)
│   └── celegans_neurotransmitters.csv        (v2d Dale signs; eLife 95402)
├── src/                                       (the library; editable-installed)
│   ├── connectomes/  celegans_cook2019.py (load modes), neurotransmitters.py
│   ├── nulls/        random_gaussian, erdos_renyi, degree_rewire, clustering_rewire,
│   │                 modularity_rewire, validation.py        (all directed-aware)
│   ├── reservoir/    blas.py, weights.py, build.py
│   ├── tasks/        memory_capacity.py, narma.py
│   └── experiment/   GENERIC runner.py / stats.py / plots.py / config.py
├── experiments/
│   ├── celegans/                              (connectome-shared, task-agnostic)
│   │   ├── substrates.py   (SubstrateBuilder), matrix_config.py
│   │   └── celegans_narma10/   task_config.py, run.py, plot_demo.py, results/, figures/
│   ├── v2a_continuous_weights/   (legacy MC: notebook + probe scripts)
│   └── v2b_directed_weighted/    (legacy MC: notebook + probe scripts)
└── tests/test_smoke.py
```

**Experiment infrastructure is split into three reuse tiers** (refactored June
2026): generic, task- & connectome-agnostic code lives in `src/experiment/`
(the conditions × variants × sr × seeds matrix runner, permutation stats,
figures, and the `ExperimentConfig` dataclass); connectome-shared, task-agnostic
code in `experiments/<connectome>/` (the `SubstrateBuilder` and `matrix_config`);
each task is a thin `experiments/<connectome>/<task>/` (a `task_config.py`, a
~15-line `run.py`, a `plot_demo.py`, and outputs). A run assembles its config as
`ExperimentConfig(**matrix_config.shared(), **task_config.task())` and is
launched with e.g. `python -m experiments.celegans.celegans_narma10.run`.

The legacy memory-capacity experiments (v2a/v2c, v2b) remain as Jupyter
notebooks + probe scripts under `experiments/v2*_*/`. All `*.parquet` outputs are
gitignored as regenerable; `figures/*.png` are tracked.

**Key library interfaces.**
- Connectome loader `load(processing=...)`: `binary_undirected_chemical` (v2a),
  `directed_weighted_chemical` (v2b/v2d; reservoir convention `W[i,j]`=j→i).
- Null generators `generate(adjacency, seed, directed=False, **kwargs)` returning
  a binary mask. Rungs 2–4 accept `directed=True`.
- `validate_null(original, generated, preserved_property, ...)` properties:
  `edge_count`, `degree_sequence`, `in/out_degree_sequence`, `density`,
  `clustering`, `modularity`, `directed_clustering`, `directed_block_matrix`.
- `apply_weight_scheme(mask, scheme, seed, **kwargs)` schemes: `symmetric_gaussian`
  (v2a), `asymmetric_empirical` (v2b), `asymmetric_empirical_signed` (v2d Dale).
- `load_neuron_signs(node_labels)` → per-neuron ±1 Dale vector + coverage.
- Task evaluators `evaluate(reservoir, seed, **cfg) -> dict`: `memory_capacity`
  (returns `mc`), `narma` (returns `nrmse`).

---

## 5. The null model ladder

Each rung preserves more structure than the last; if the connectome beats a
null, structure beyond that rung's preserved feature is doing work. Rungs 2–4
have directed paths (`directed=True`); full reference in
`NULL_MODELS_METHODOLOGY.md`.

- **Rung 0 — Random Gaussian.** Preserves N and (in expectation) density.
- **Rung 1 — Erdős–Rényi.** Preserves N and exact edge count.
- **Rung 2 — Degree-preserving rewire.** + exact degree (in/out, directed).
  Undirected: `double_edge_swap`; directed: `directed_edge_swap`.
- **Rung 3 — Clustering-preserving rewire.** Rung 2 + global clustering within
  tolerance (default 5%). Directed uses two-edge head-swaps with an *incremental
  numpy directed-triangle update* and mean Fagiolo clustering as the constraint.
- **Rung 4 — Modularity-preserving rewire.** Rung 2 + the (directed) block
  edge-count matrix of a fixed Louvain partition, preserved exactly by
  construction (hence directed modularity Q exact).

Rungs 3 and 4 are parallel (triangles vs blocks), both built on rung-2 degree
preservation. Self-loops are forced to zero everywhere.

---

## 6. Experimental history

**v1 (pre-framework).** Connectome ≈ degree_rewire on MC at sr=0.95, both far
below random_Gaussian. Caught post-hoc to be a confound stack (binary-vs-
continuous weights, symmetry, self-loops, miscounted edges). Prompted the entire
v2 framework: controlled comparisons, unified pipeline, validation hooks.

**v2a (controlled foundation).** Same design through the unified pipeline (binary
symmetric mask → symmetric Gaussian weights → rescale sr). All four conditions
cluster within ~0.6 MC at sr=0.95 — v1's gap was *entirely* the confound stack.
Extended sweep revealed the **spectral-shift effect** (broad-degree topologies
peak at higher nominal sr; hub-driven outlier eigenvalues depress the bulk). A
supercritical probe (n=50, sr∈{1.25,1.5,1.75}) found the first real signal:
connectome > degree_rewire, **Cohen's d = 0.64→1.02→1.47**.

**v2c (rung-3/4 disambiguation).** Added clustering/modularity rewires. Rung-2
shows the supercritical gap; rungs 3 and 4 both **close it** → the degree-only
mechanism is ruled out, clustering and/or modularity is sufficient (the two are
confounded on this connectome).

**v2b (directed + empirical weights, MC).** Directed topology, weights sampled
from Cook 2019's distribution (sqrt and raw). ~20% MC reduction at canonical sr
(Perron–Frobenius compression of all-positive matrices). The supercritical
connectome–degree_rewire d crosses zero and reaches **d≈+1.04 at sr=1.50**,
matching v2c despite a structurally different reservoir → **the supercritical
effect is regime-independent on MC**. Transform choice (sqrt vs raw) shifts
*where* the crossover sits, not *whether* it appears.

**Phase-0 NARMA-10 bridge (complete).** First prediction task: NARMA-10
emulation across three realism conditions (**v2a** undirected gaussian, **v2b**
directed empirical non-negative, **v2d** directed empirical signed/Dale) ×
full 5-rung ladder × 20-point sr sweep (0→2) × 10 seeds = 3600 evals; raw
weights. Findings:
- **v2a: clean null.** Connectome ≈ every null across the whole sweep (degree
  supercritical d≈0, all p_holm≈1). The MC supercritical advantage did **not**
  transfer to NARMA in the undirected-topology regime.
- **v2b/v2d: strong supercritical advantage.** Connectome beats degree_rewire
  (d +3.9→+10.5 for v2b, +2.1→+9.9 for v2d, all Holm-significant) **and** beats
  clustering/modularity (rungs 3–4 do **not** close the gap, unlike MC).
  Crossover at sr≈1.26; nulls are *better* at canonical sr.
- **Mechanism: robustness, not superiority.** The connectome's NRMSE is flat
  (~0.5) across sr; nulls are U-shaped — better canonically, then destabilise
  supercritically. The connectome wins only by being robust where nulls fail.
- **Confound: topology vs weights.** In v2b/v2d the connectome keeps its *real*
  weights while nulls resample from the pool, so those conditions conflate
  directed topology with the connectome's real weight placement. v2a (all-random
  weights) is the clean topology test and is null → the NARMA effect is
  plausibly weight-driven, not pure topology. v2d's inhibition is sparse (~3.6%
  of edges) so v2d ≈ v2b spectrally.

---

## 7. Key findings to date

1. **Degree sequence is sufficient to explain MC at canonical sr**, across both
   weight regimes (v2a, v2b).
2. **Higher-order structure matters in the supercritical regime on MC**
   (connectome > degree_rewire, d up to 1.47); v2c attributes it to clustering
   and/or modularity, degree-only ruled out.
3. **The MC supercritical effect is regime-independent** (v2b reproduces v2c's
   d≈1.0 in a structurally different reservoir).
4. **Spectral-radius matching ≠ effective-criticality matching when degree
   distributions differ** — a generalisable methodological contribution.
5. **Perron–Frobenius compression** shifts the crossover location for all-
   positive weights but does not eliminate the effect.
6. **On NARMA prediction the supercritical advantage is regime-dependent** —
   strong in directed empirical conditions (v2b/v2d, beating *all* nulls), absent
   in the clean undirected-topology test (v2a). It is supercritical *robustness*
   rather than superiority, and in v2b/v2d is confounded with the connectome's
   real weight placement (the headline open question for prediction tasks).

---

## 8. Methodological lessons learned

Caught at specific stages; recorded so future iterations don't repeat them.

- **Binary-vs-continuous weights, symmetric-vs-asymmetric W, and drifting
  self-loops are silent confounds at fixed sr.** Standardise all three across
  conditions; force zero diagonal. (v1 → v2a.)
- **Spectral-radius matching understates broad-degree topologies** (depressed
  bulk vs λ_max). Sweep sr or control on bulk criticality. (v2a.)
- **Perron–Frobenius compression** in all-positive matrices shifts the effective
  regime upward in sr; sign assignment (E/I) mitigates it. (v2b → v2d.)
- **Heavy-tailed raw weights kneecap reservoirs** (a few large edges dominate the
  spectral radius). sqrt/log transform mitigates; the current NARMA bridge uses
  raw, so v2b/v2d there carry this caveat. (v2b.)
- **Compare connectome vs null at *matched* sr, not best-over-sweep.** Each
  variant's own optimum lives at a different sr; a "best NRMSE per variant"
  glance inverts the real story. (NARMA bridge.)
- **NMSE vs NRMSE.** Report NRMSE = √(MSE/Var); many RC papers report NMSE (no
  root), so a literature "NARMA-10 ≈ 0.3" is NRMSE ≈ 0.55.
- **n=10 sweeps predict n=50 probe direction and zero-crossings** to within
  |Δd|≤0.5; reserve n=50 for magnitude/significance. (v2b.)
- **BLAS thread limiting must be called *after* numpy import**, or it silently
  no-ops.
- **The connectome is one fixed graph; nulls are sampled.** Inference is "is
  *this* connectome anomalous vs the null distribution?", not connectomes in
  general. In v2b/v2d the connectome also keeps real weights while nulls resample
  (the topology-vs-weights confound above).

---

## 9. Next iteration roadmap

`PROJECT_PLAN.md` is canonical: the thirteen-week schedule, the Stage-A
scale-row/realism-cross design, decision gates, conference targets, and the task
progression (NARMA-10 ✓ → Mackey-Glass → Lorenz, toward the connectome-as-JEPA
world model). The immediate next build is the **Mackey-Glass** experiment;
`MACKEY_GLASS_KICKOFF.md` is its full brief (a thin task module + task dir on the
shared infra). Lorenz (closed-loop free-running) follows on the same
infrastructure.

---

## 10. Open methodological questions

- **Topology vs weights in v2b/v2d (highest priority for prediction).** The
  connectome keeps real weights; nulls resample. A "connectome topology +
  resampled weights" null would isolate topology from weight placement.
- **Divergence-robust statistics.** Some supercritical nulls blow up (huge
  NRMSE); a median-based or NRMSE-capped statistic would harden the permutation
  tests against those outliers.
- **Weight transform for prediction.** The NARMA bridge uses raw synapse counts;
  sqrt is a one-line switch (`matrix_config.WEIGHT_TRANSFORM`) and the documented
  heavy-tail mitigation.
- **Clustering vs modularity disambiguation** (from v2c) — still confounded on
  this connectome; needs a dual-constraint null or decoupled block model.
- **Asymmetric mask sampling** between the fixed connectome and the sampled nulls
  (inference scope).

---

## 11. Working conventions

- **Experiments live under `experiments/<connectome>/<task>/`**; generic
  infrastructure under `src/experiment/`; launch with `python -m
  experiments.<connectome>.<task>.run` (`--smoke` for a tiny check).
- **A new task = a `src/tasks/<task>.py` evaluator + a thin task dir.** Do not
  duplicate the runner/stats/plots/substrates; if you think you must edit them,
  reconsider.
- **Variable names full and readable** (`spectral_radius`, not `sr`, in code).
- **Seed convention:** the construction seed drives mask/weights/`Win`; the task
  input/series uses `seed + INPUT_SEED_OFFSET` (1000), pairing connectome and
  null on identical input per seed.
- **Cohen's d on the performance direction:** d > 0 ⇒ connectome better,
  whatever the metric's direction.
- **Figures at 300 dpi** to each task's `figures/`; `results/*.parquet`
  gitignored; commits conventional, no Claude attribution trailer.
- **Push back on disagreements; honest reads beat positive spin.**

---

## 12. Quick reference

- **Connectome data:** `data/cook2019_connectome.xlsx`, sheet "hermaphrodite
  chemical" (SI corrected July 2020). N=300; 3000 undirected / 3669 directed
  off-diagonal edges; 38 autaptic self-loops dropped. Reservoir convention
  `W[i,j]` = weight j→i (the directed loader transposes Cook's native layout).
- **Dale signs (v2d):** `data/celegans_neurotransmitters.csv` — GABA-synthesizing
  neurons (DD, VD, RME, AVL, DVB, RIS = 26) inhibitory (−1), all else +1; source
  eLife 95402. See `SIGNED_WEIGHTS_METHODOLOGY.md`.
- **MC hyperparameters (v1-pinned):** `T=3000, warmup=500, max_lag=50,
  ridge_alpha=1e-6, leak=1.0, input_scaling=1.0, n_seeds=10`, BLAS threads 2.
- **MC spectral sweep:** `[0.5,0.7,0.85,0.9,0.95,1.0,1.05,1.1,1.25,1.5,1.75]`;
  supercritical probes at sr∈{1.25,1.5,1.75}, n=50, 10k-permutation Holm tests.
- **Prediction sweep (NARMA bridge):** 20-point `linspace(0,2,20)`, n=10, 3
  conditions × 6 variants; NARMA frozen reservoir hyperparameters
  `input_scaling=0.2, leak=1.0` (tuned on rung-0).
- **Realism conditions:** v2a `symmetric_gaussian`/undirected, v2b
  `asymmetric_empirical`/directed, v2d `asymmetric_empirical_signed`/directed.

---

## 13. How to use this document in a new conversation

Paste this document as the first message, then state the task. Recommended extra
context per task:
- **Continuing/analysing a prediction experiment:** also load `PROJECT_PLAN.md`
  and the task's `task_config.py` + `results/`; the methodology docs
  (`NULL_MODELS_METHODOLOGY.md`, `SIGNED_WEIGHTS_METHODOLOGY.md`) for the nulls
  and Dale signs.
- **Starting the next task:** `MACKEY_GLASS_KICKOFF.md` is a self-contained brief
  (which docs/code to read, the thin deliverables, decisions to lock).
- **Continuing a legacy MC experiment:** load that notebook's `results.parquet`
  and the relevant `src/` modules.

The progression v1 → v2a → v2c → v2b → v2d → prediction tasks is a controlled
chain; breaking the one-variable-at-a-time discipline is the single failure mode
most likely to cost weeks. Hold the line.

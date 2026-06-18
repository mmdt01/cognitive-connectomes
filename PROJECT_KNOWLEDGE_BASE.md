# Cognitive Connectomes — Project Knowledge Base

A research project on connectome-constrained reservoir computing. Uses
empirically measured connectomes as the recurrent matrix of an echo-state
network and asks what biological connectivity contributes beyond random or
degree-matched baselines.

This document is the single canonical reference for the project. It is intended
to be loaded into fresh Claude conversations as the starting context. Companion
docs: `PROJECT_PLAN.md` (the forward plan), `NULL_MODELS_METHODOLOGY.md` and
`SIGNED_WEIGHTS_METHODOLOGY.md` (method references),
`PREDICTION_TASKS_INTERPRETATION.md` (mechanism interpretation of the NARMA/MG
results + pre-registered Lorenz predictions; an uncommitted working doc),
`MACKEY_GLASS_KICKOFF.md` (the completed Mackey-Glass build's brief).

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
The **NARMA-10 bridge and the Mackey-Glass forecasting task are both complete**,
and the prediction picture is more nuanced than MC. The supercritical advantage
is **regime-dependent**: on NARMA it is strong in the directed empirically-weighted
conditions (v2b/v2d — the connectome beats *every* null, Cohen's d up to ~+10) but
**absent in the clean undirected condition (v2a)**, manifesting as supercritical
*robustness* not canonical superiority.

The **topology-vs-weights confound is now resolved** by a weight-placement control
(`connectome_weight_permuted`: the connectome's exact topology + a permutation of
its exact weights), which splits the effect into a topology leg (control vs
degree_rewire) and a placement leg (connectome vs control). The answer
**dissociates by task**: on **NARMA** the advantage is *mostly topology*
(control vs degree d ≈ +4.3–4.9, v2b/v2d) with a smaller weight-placement bonus
(connectome vs control d ≈ +1, Holm-sig in v2b) — so it is **topology-led**, not
"plausibly weight-driven" as previously feared. On **Mackey-Glass** the connectome
is instead *worse* supercritically, and that deficit is **entirely weight
placement** (connectome vs control d ≈ −2 to −3) with a **null topology leg** — the
mirror image of NARMA. v2a is a null negative control in both. Net: the connectome's
directed topology helps input-driven emulation and is neutral for autonomous
forecasting; its weight placement helps emulation slightly and *hurts* forecasting.
Next build: **Lorenz** (closed-loop free-running).

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
├── PREDICTION_TASKS_INTERPRETATION.md        (mechanism interpretation; uncommitted)
├── data/
│   ├── cook2019_connectome.xlsx              (Cook 2019 SI, corrected July 2020)
│   └── celegans_neurotransmitters.csv        (v2d Dale signs; eLife 95402)
├── src/                                       (the library; editable-installed)
│   ├── connectomes/  celegans_cook2019.py (load modes), neurotransmitters.py
│   ├── nulls/        random_gaussian, erdos_renyi, degree_rewire, clustering_rewire,
│   │                 modularity_rewire, validation.py        (all directed-aware)
│   ├── reservoir/    blas.py, weights.py, build.py
│   ├── tasks/        memory_capacity.py, narma.py, mackey_glass.py
│   ├── experiment/   GENERIC runner.py / stats.py (divergence-robust) / plots.py / config.py
│   └── analysis/     spectral.py  (substrate analysis, connectome-agnostic; first of a series)
├── experiments/
│   ├── celegans/                              (connectome-shared, task-agnostic)
│   │   ├── substrates.py   (SubstrateBuilder + weight-placement control), matrix_config.py
│   │   ├── celegans_narma10/        task_config.py, run.py, plot_demo.py, results/, figures/
│   │   ├── celegans_mackey_glass/   task_config.py (2 horizons), run.py, plot_demo.py, results/, figures/
│   │   └── analysis/                spectral.py driver (uses src/analysis); figures/, results/
│   ├── v2a_continuous_weights/   (legacy MC: notebook + probe scripts)
│   └── v2b_directed_weighted/    (legacy MC: notebook + probe scripts)
└── tests/test_smoke.py
```

**Experiment infrastructure is split into three reuse tiers** (refactored June
2026): generic, task- & connectome-agnostic code lives in `src/experiment/`
(the conditions × variants × sr × seeds matrix runner, divergence-robust rank
stats, figures, and the `ExperimentConfig` dataclass); connectome-shared,
task-agnostic code in `experiments/<connectome>/` (the `SubstrateBuilder` and
`matrix_config`); each task is a thin `experiments/<connectome>/<task>/` (a
`task_config.py`, a ~15-line `run.py`, a `plot_demo.py`, and outputs). A run
assembles its config as `ExperimentConfig(**matrix_config.shared(),
**task_config.task())` and is launched with e.g. `python -m
experiments.celegans.celegans_narma10.run`.

A parallel **substrate-analysis tier** characterises the recurrent matrices
themselves (independent of any task): generic, connectome-agnostic tools in
`src/analysis/` (first module: `spectral.py`) with connectome-specific drivers
in `experiments/<connectome>/analysis/`. `spectral.py` grounds the
placement→memory mechanism (the connectome's eigenvalue bulk is the most
compressed); it is the template for the planned deeper topological analyses
(degree, clustering, motifs, modularity, reciprocity).

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
- **Confound: topology vs weights (since resolved — see below).** In v2b/v2d the
  connectome keeps its *real* weights while nulls resample from the pool, so those
  conditions conflate directed topology with the connectome's real weight
  placement. This was the headline open question for prediction; the
  weight-placement control (next entry) resolves it — and contrary to the prior
  guess that the effect was "plausibly weight-driven," it is **topology-led**.
  v2d's inhibition is sparse (~3.6% of edges) so v2d ≈ v2b spectrally.

**Weight-placement control (topology-vs-weights confound resolved).** Added a
shared control variant `connectome_weight_permuted` — the connectome's *exact*
topology and *exact* weight multiset, but a per-seed **permutation** of which edge
carries which weight (Dale signs re-applied for v2d; v2a is a
distribution-preserving negative control). Because the connectome, the control,
and the rung nulls all share the empirical weight distribution, two comparisons
decompose the effect cleanly: **connectome vs control = weight placement**;
**control vs degree_rewire = topology**. Confirmed first by an n=50 probe, then by
the full n=10 matrix (each task re-run with the 7-variant ladder). v2a is a null
negative control throughout (permuting already-random weights changes nothing),
validating the construction.

**Mackey-Glass forecasting (complete).** Second prediction task: *driven
(teacher-forced) k-step-ahead* forecasting of the mildly chaotic Mackey-Glass
delay system (β=0.2, γ=0.1, n=10, τ=17), same 3 conditions × 7-variant ladder ×
20-point sr sweep × 10 seeds, at two horizons (h=84 canonical benchmark, h=300
chaos-limited). Local generator bit-exact vs `reservoirpy.datasets.mackey_glass`;
frozen `input_scaling=0.5, leak_rate=0.3` (MG's smooth series wants a far lower
leak than NARMA's 1.0). Findings:
- **Driven MG is easy at the classic horizons** (rung-0 NRMSE ≈ 0.09 at h=84): a
  single-scalar drive lets the reservoir reconstruct the delay embedding. The
  discriminative regime is long horizons (NRMSE ≈ 0.47 at h=300).
- **The supercritical sign flips vs NARMA.** v2a is null; in v2b/v2d the connectome
  is *worse* than its nulls at h=84 (connectome vs degree d down to ≈−3.3,
  Holm-sig), and the deficit **washes out at h=300**.
- **The h=84 deficit is entirely weight placement.** Connectome vs control
  d ≈ −2 to −3 (Holm-sig, v2b/v2d); the topology leg (control vs degree_rewire) is
  **null**. So the connectome's *real weight placement* is anomalously bad for this
  forecasting task; its topology is indistinguishable from a degree-matched random
  graph. Mirror image of NARMA, where topology is the dominant *positive* effect.

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
   rather than superiority.
7. **The topology-vs-weights confound is resolved, and the answer dissociates by
   task** (via the `connectome_weight_permuted` placement control). NARMA's
   advantage is **mostly topology** (control vs degree d ≈ +4.3–4.9) plus a smaller
   weight-placement bonus (connectome vs control d ≈ +1) — i.e. topology-led, not
   weight-driven. Mackey-Glass is the **mirror image**: the connectome is *worse*
   supercritically, the deficit is **entirely weight placement** (d ≈ −2 to −3) and
   the topology leg is null. The connectome's directed topology helps input-driven
   emulation and is neutral for autonomous forecasting; its weight placement helps
   emulation slightly and *hurts* forecasting. v2a is a null negative control in
   both. **Mechanism (diagnostics):** the placement effect is spectrally grounded
   — the connectome's heavy weights compress its eigenvalue bulk, giving it the
   least linear memory (shown via the `src/analysis/` spectral tier +
   memory-capacity + a sqrt-weight sensitivity check); the topology effect is real
   but mechanistically open. Full account in `PREDICTION_TASKS_INTERPRETATION.md`.

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
  — the topology-vs-weights confound, now decomposed by the
  `connectome_weight_permuted` placement control (§6).
- **To isolate weight *placement*, permute — don't resample.** The rung nulls draw
  weights *with replacement* (a bootstrap, so the distribution is preserved only in
  expectation). The placement control instead **permutes the connectome's exact
  weights** onto its exact topology, holding the multiset fixed so the comparison
  isolates placement alone. As the highest-variance null (heavy weights on
  high-leverage edges), it warrants more seeds; n=50 confirmed the n=10 read.

---

## 9. Next iteration roadmap

`PROJECT_PLAN.md` is canonical: the thirteen-week schedule, the Stage-A
scale-row/realism-cross design, decision gates, conference targets, and the task
progression (NARMA-10 ✓ → Mackey-Glass ✓ → Lorenz, toward the connectome-as-JEPA
world model). The immediate next build is the **Lorenz** task (closed-loop
free-running prediction), on the same shared infrastructure — only a new task
module + task dir, inheriting the substrate pipeline and the weight-placement
control unchanged.

---

## 10. Open methodological questions

- **Topology vs weights in v2b/v2d — RESOLVED** by the `connectome_weight_permuted`
  placement control (§6–7): NARMA is topology-led, Mackey-Glass placement-driven.
- **Divergence-robust statistics — DONE.** `src/experiment/stats.py` now caps
  blow-ups (`cfg.metric_divergence_cap`, default 2.0 for NRMSE), reports a
  per-variant divergence rate, and tests significance with a rank-based
  permutation test (Cliff's delta + median alongside the capped Cohen's d).
  Re-running NARMA/MG left the headlines unchanged — the effects are clean rank
  separations (δ≈±1) at ~0% divergence. Built ahead of Lorenz, where closed-loop
  divergence is the primary failure mode.
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
- **Prediction sweep (NARMA + Mackey-Glass):** 20-point `linspace(0,2,20)`, n=10,
  3 conditions × **7 variants** (connectome + `connectome_weight_permuted`
  placement control + 5-rung ladder). Frozen reservoir hyperparameters tuned on
  rung-0: NARMA `input_scaling=0.2, leak=1.0`; Mackey-Glass `input_scaling=0.5,
  leak=0.3`. MG is *driven k-step-ahead* (teacher-forced) at horizons h=84
  (benchmark) and h=300 (chaos-limited); local generator bit-exact vs `reservoirpy`.
- **Weight-placement control:** `connectome_weight_permuted` — connectome's exact
  topology + a per-seed permutation of its exact weights (Dale signs kept; v2a a
  negative control). `connectome vs control` = placement, `control vs degree` =
  topology.
- **Prediction statistics:** divergence-robust — rank-based permutation test
  (Holm-corrected) for significance, with Cliff's delta, capped Cohen's d, median,
  and a per-variant divergence rate; `metric_divergence_cap=2.0` (NRMSE).
- **Substrate analysis tier:** `src/analysis/spectral.py` (connectome-agnostic
  spectral metrics + plots) + `experiments/celegans/analysis/spectral.py` driver
  (`python -m experiments.celegans.analysis.spectral`). Grounds the
  placement→memory mechanism; first of the planned topological-analysis series.
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
- **Starting the next task (Lorenz):** no kickoff brief yet, but the infra is
  ready (substrate pipeline + placement control + divergence-robust stats);
  `PREDICTION_TASKS_INTERPRETATION.md` §4 holds the pre-registered Lorenz
  predictions and the metric decision to lock first (valid-time vs climate).
  `MACKEY_GLASS_KICKOFF.md` is the template for a thin task build.
- **Running a substrate analysis:** `src/analysis/` + the
  `experiments/celegans/analysis/` drivers; see that dir's README.
- **Continuing a legacy MC experiment:** load that notebook's `results.parquet`
  and the relevant `src/` modules.

The progression v1 → v2a → v2c → v2b → v2d → prediction tasks is a controlled
chain; breaking the one-variable-at-a-time discipline is the single failure mode
most likely to cost weeks. Hold the line.

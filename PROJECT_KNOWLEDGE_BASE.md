# Cognitive Connectomes — Project Knowledge Base

A research project on connectome-constrained reservoir computing. Uses
empirically measured connectomes as the recurrent matrix of an echo-state
network and asks what biological connectivity contributes beyond random or
degree-matched baselines.

This document is the single canonical reference for the project. It is intended
to be loaded into fresh Claude conversations as the starting context. Companion
docs: `PROJECT_PLAN.md` (the forward plan) and
`PREDICTION_TASKS_INTERPRETATION.md` (the reference summary + mechanism
interpretation of all four tasks, evaluated on the wide spectral-radius sweep).

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
and/or modularity (degree-only mechanism ruled out). A later **unified wide-sweep
re-run** (7-variant ladder × `[0,4]` sweep) reproduces all of this and reframes it
through the operating-point lens: the connectome's MC is the *lowest* at canonical
and the *highest* deep supercritically (an operating-point shift), and its
supercritical "advantage" is a **robustness crossover** — a wide flat memory plateau
where the disk-like nulls peak sharply and collapse — not a higher ceiling (its peak
MC sits *below* theirs). Full account in `PREDICTION_TASKS_INTERPRETATION.md`.

The project then turned the task axis from passive memory toward **dynamical-system
prediction** (north star: a connectome-as-JEPA world model), adding three prediction
tasks — NARMA-10 (input-driven emulation), Mackey-Glass (driven forecasting), and
Lorenz (closed-loop free-running) — on the same shared infrastructure. All four tasks
(MC + the three) are now evaluated across a **wide spectral-radius sweep**
(`linspace(0, 4, 39)`), which is the key methodological correction: a narrow `[0,2]`
sweep compares variants at *different effective criticalities*, because the
connectome's heavy weights compress its eigenvalue bulk so its operating point sits at
a **higher nominal spectral radius** than the disk-like nulls (`sr_crit = 1/bulk₉₅_ratio
≈ 3.3` vs `≈ 2.2–2.7`).

**Read curve-vs-curve across the wide sweep, the four tasks tell one story.** At the
canonical operating point (sr ≈ 0.95) the connectome is **worse-or-equal** on every
task. In the supercritical regime — once the sweep reaches each variant's operating
point — the connectome is the **most robust** variant: where the disk-like nulls peak
**sharply** and collapse, it rises slowly to a **wide, flat plateau** slightly below
the nulls' peak but holding far into the regime. This is a **robustness–performance
trade-off** rooted in the connectome's spectral heterogeneity (a likely signature of
biological connectivity statistics): best on the driven tasks (NARMA flat where nulls
destabilise; MC/MG best-and-holding where nulls collapse) and at parity with the best
structured null on closed-loop Lorenz.

The **topology-vs-weights confound is resolved** by a weight-placement control
(`connectome_weight_permuted`: the connectome's exact topology + a per-seed permutation
of its exact weights), splitting the effect into a **placement** leg (connectome vs
control) and a **topology** leg (control vs degree_rewire). The wide sweep reframes
both. (1) **Weight placement is an operating-point shift, not a handicap:** the
placement leg is a deficit at low–mid sr and **reverses to advantage/parity at high
sr** on every task — the connectome's apparent supercritical "deficits" on MG and
Lorenz under the old narrow sweep were an artifact of comparing *below* its operating
point. (2) **Directed topology is a separate, task-dependent advantage** that **emerges
supercritically**: large for memory (MC) and input-driven emulation (NARMA), emergent
under strong drive for forecasting (MG tail), and absent for closed-loop generation
(Lorenz, where degree-rewiring matches it). v2a is a spectral negative control
throughout. Full account in `PREDICTION_TASKS_INTERPRETATION.md`.

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
├── PROJECT_KNOWLEDGE_BASE.md / PROJECT_PLAN.md
├── PREDICTION_TASKS_INTERPRETATION.md        (four-task interpretation summary)
├── data/                                     (per-species subdirs)
│   ├── celegans/
│   │   ├── cook2019_connectome.xlsx          (Cook 2019 SI, corrected July 2020)
│   │   └── celegans_neurotransmitters.csv    (v2d Dale signs; eLife 95402)
│   └── human/                                (Suárez 2021 Lausanne SC/FC; .mat gitignored)
│       └── README.md                         (dataset provenance + structure)
├── src/                                       (the library; editable-installed)
│   ├── connectomes/  celegans_cook2019.py (load modes), neurotransmitters.py
│   ├── nulls/        random_gaussian, erdos_renyi, degree_rewire, clustering_rewire,
│   │                 modularity_rewire, validation.py        (all directed-aware)
│   ├── reservoir/    blas.py, weights.py, build.py
│   ├── tasks/        memory_capacity.py, narma.py, mackey_glass.py, lorenz.py
│   ├── experiment/   GENERIC runner.py / stats.py (divergence-robust) / plots.py / config.py
│   └── analysis/     spectral.py  (substrate analysis, connectome-agnostic; first of a series)
├── experiments/
│   └── celegans/                              (connectome-shared, task-agnostic)
│       ├── substrates.py   (SubstrateBuilder + weight-placement control), matrix_config.py
│       ├── celegans_mc/             task_config.py, run.py, results/, figures/  (Jaeger memory capacity)
│       ├── celegans_narma10/        task_config.py, run.py, plot_demo.py, results/, figures/
│       ├── celegans_mackey_glass/   task_config.py (2 horizons), run.py, plot_demo.py, results/, figures/
│       ├── celegans_lorenz/         task_config.py (2 metrics), run.py, plot_demo.py, results/, figures/
│       └── analysis/                spectral.py driver (uses src/analysis); figures/, results/
└── tests/test_smoke.py
```

**Experiment infrastructure is split into three reuse tiers** (refactored June
2026): generic, task- & connectome-agnostic code lives in `src/experiment/`
(the conditions × variants × sr × seeds matrix runner, divergence-robust rank
stats, figures, and the `ExperimentConfig` dataclass); connectome-shared,
task-agnostic code in `experiments/<connectome>/` (the `SubstrateBuilder` and
`matrix_config`); each task is a thin `experiments/<connectome>/<task>/` (a
`task_config.py`, a ~15-line `run.py`, an optional `plot_demo.py`, and outputs). A run
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

All `*.parquet` outputs are gitignored as regenerable; `figures/*.png` are tracked.

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
  (returns `mc`), `narma` (`nrmse`), `mackey_glass` (`nrmse`), `lorenz` (`vpt` +
  `climate_error`).

---

## 5. The null model ladder

Each rung preserves more structure than the last; if the connectome beats a
null, structure beyond that rung's preserved feature is doing work. Rungs 2–4
have directed paths (`directed=True`).

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

*The v1→v2b entries below are the framework's methodological provenance (confound
cleanup, the null ladder, directed weights); their narrow-sweep MC numbers are
reproduced and reframed by the unified wide-sweep runs — the four task entries that
follow (NARMA, Mackey-Glass, Lorenz, and the MC re-run), which hold the current
results.*

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

**NARMA-10 (input-driven emulation, complete).** First prediction task: NARMA-10
across three realism conditions (**v2a** undirected gaussian, **v2b** directed
empirical non-negative, **v2d** directed empirical signed/Dale) × the 7-variant ladder
× 39-point `[0,4]` sweep × 10 seeds; raw weights; frozen `input_scaling=0.2, leak=1.0`.
Findings (wide sweep):
- **v2a: clean null** — connectome ≈ every null across the sweep.
- **v2b/v2d: supercritical robustness.** The connectome's NRMSE is **flat (~0.55)
  across the entire `[0,4]` sweep** — the only variant that never destabilises — while
  every null (including the placement control) climbs to ~0.80 supercritically. So the
  connectome **beats every null** supercritically and the margin **widens in the
  tail**. Both legs favour it supercritically: placement reverses to an advantage
  (connectome vs control d ~+3 at sr 3) and topology is a large advantage (control vs
  degree d ~+4.3 in the mid-band, +1 in the tail). NARMA is noise-driven and prone to
  supercritical blow-up; the connectome's compressed-bulk **stability** is exactly what
  it rewards. (v2d's inhibition is sparse, ~3.6% of edges, so v2d ≈ v2b spectrally.)

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
(teacher-forced) k-step-ahead* forecasting of the mildly chaotic Mackey-Glass delay
system (β=0.2, γ=0.1, n=10, τ=17), 3 conditions × 7-variant ladder × 39-point `[0,4]`
sweep × 10 seeds, at two horizons (h=84 canonical, h=300 chaos-limited). Local
generator bit-exact vs `reservoirpy.datasets.mackey_glass`; frozen `input_scaling=0.5,
leak_rate=0.3`. Findings (wide sweep):
- **v2a null; a v2b/v2d phenomenon.** Driven MG is easy at the classic horizons
  (rung-0 NRMSE ≈ 0.09 at h=84).
- **The connectome's deficit is an operating-point artifact.** At matched low–mid sr it
  is *worse* (the narrow-sweep finding: connectome vs control/degree d ~−2.5 at sr 1.5),
  but its NRMSE **improves monotonically with sr** to the best of all variants at its
  operating point (h=84: 0.15 → **0.03** by sr ≈ 3, vs nulls degrading to 0.07–0.24;
  h=300 similar). The placement leg reverses (d −2.5 → +2.0 by sr 3), and a **topology
  advantage emerges in the tail** (control vs degree d ~+1.7 at sr 3, h=84) invisible at
  low sr. MG is memory-limited; the connectome's memory peaks at its higher operating
  sr, so once the sweep reaches it the connectome is the best-and-most-robust forecaster
  (nulls degrade past their own optima while it holds). *(At each variant's own optimum
  the variants are roughly tied; the connectome's distinction is its later optimum and
  graceful degradation.)*

**Lorenz attractor (complete).** Third prediction task: *closed-loop free-running*
generation of the chaotic Lorenz attractor (σ=10, ρ=28, β=8/3) — teacher-force a ridge
readout, then cut the reservoir loose to feed its own 3-D output back as input. 3
conditions × 7-variant ladder × 39-point `[0,4]` sweep × 10 seeds; local RK4 generator
(short-horizon cross-check vs `reservoirpy` only — chaos precludes bit-exactness against
its adaptive `solve_ivp`); 3-channel `Win`; **direct next-state** readout (the increment
form blows the climate metric up at N=300); frozen `input_scaling=0.1, leak_rate=1.0,
ridge=1e-7`. Two metrics: **VPT** (valid-prediction time, Lyapunov units, higher=better)
and **climate** (per-coordinate marginal Wasserstein-1, lower=better). Findings (wide
sweep):
- **The connectome recovers at its operating point.** Under the old narrow `[0,2]` sweep
  it looked *worse on both metrics* supercritically — an artifact of stopping below its
  `sr_crit ≈ 3.3`. On the wide sweep it **recovers at sr ≈ 3.0–3.3 to parity with the
  best structured null** (degree): VPT 1.6 → ~4.6 (vs degree ~4.6, random ~2.6), climate
  6.5 → ~2 (vs random *diverged* to 20+); and it is the **most divergence-robust**
  variant — **0%** closed-loop blow-ups in v2b/v2d vs **26–31%** for random/ER. The
  placement leg reverses from a mid-sweep deficit (d −2 at sr 1.5) to parity (d ~+0.5 at
  sr 3).
- **Topology does not favour the connectome on Lorenz** in the tail (control vs degree
  d ≈ −0.8 — degree-rewiring matches it), unlike MC/NARMA. So on the autonomous task the
  connectome's structure is **sufficient and robust, but not superior** — the
  pre-registered fidelity-for-stability trade did not occur (the metrics agree, and
  below sr ≈ 0.8 the connectome is *better* on climate).

**Memory capacity (unified re-run, complete).** Re-ran MC on the shared 7-variant
ladder × 3 conditions × `[0,4]` wide sweep × 10 seeds (v1-pinned MC params,
`experiments/celegans/celegans_mc/`), putting the foundational task on the same footing
as the prediction tasks. Reproduces the original findings — connectome lowest at
canonical (v2b MC 9.1, d≈−6 vs degree), connectome > degree supercritically in v2a
(d≈+1.3 at sr≈1.8, the v2a/v2c result) — and unifies them under the operating-point
picture: the connectome's MC peaks late (sr≈2) on a **flat plateau that holds to sr=4**
while the disk-like nulls peak sharply near sr≈1.2 and collapse, so the connectome
**dominates supercritically** (connectome−degree d≈+8.5 at sr 3) by **robustness, not
ceiling** (peak MC ~11.7 < nulls' ~12.3–13.0; lower participation ratio). New beyond the
original: in the *directed* conditions the topology leg (control vs degree) is ~0 at
canonical but grows to a **large emergent** memory advantage (d≈+3.5 at sr 2.5). Full
account — plus the robustness–performance trade-off and its biology — in
`PREDICTION_TASKS_INTERPRETATION.md` §3 and §5.

---

## 7. Key findings to date

1. **Degree sequence is sufficient to explain MC at canonical sr**, across both
   weight regimes (v2a, v2b).
2. **Higher-order structure matters in the supercritical regime on MC**
   (connectome > degree_rewire, d up to 1.47); v2c attributes it to clustering
   and/or modularity, degree-only ruled out. The wide-sweep re-run reproduces this
   (v2a d≈+1.3) and adds a **large emergent topology advantage in the directed
   conditions** (control > degree d≈+3.5 supercritically), reframing the supercritical
   "advantage" as a **robustness crossover** (flat memory plateau vs the nulls' sharp
   peak-and-collapse), not a higher ceiling.
3. **The MC supercritical effect is regime-independent** (v2b reproduces v2c's
   d≈1.0 in a structurally different reservoir).
4. **Spectral-radius matching ≠ effective-criticality matching when degree
   distributions differ** — a generalisable methodological contribution, now the basis
   of the operating-point analysis across all four tasks (`sr_crit = 1/bulk95_ratio`;
   compare curve-vs-curve, not at a single matched sr).
5. **Perron–Frobenius compression** shifts the crossover location for all-
   positive weights but does not eliminate the effect.
6. **At the canonical operating point the connectome is worse-or-equal on all four
   tasks; its distinctive behaviour is supercritical.** Read curve-vs-curve across the
   wide `[0,4]` sweep it is the **most robust** variant on every task — a wide flat
   plateau where the disk-like nulls peak sharply and collapse. This is a
   **robustness–performance trade-off**: it wins supercritically by robustness, *not* a
   higher ceiling (its peak performance is at or below the best null's). The cause is
   spectral heterogeneity (heavy weights on hubs spread the eigenvalue radii), a likely
   signature of biological connectivity statistics.
7. **The topology-vs-weights confound is resolved** (via the `connectome_weight_permuted`
   placement control), and the wide sweep reframes both legs. **Placement is an
   operating-point shift, not a handicap:** the placement leg reverses from a low–mid-sr
   deficit to high-sr advantage/parity on every task — the connectome's compressed bulk
   moves its optimum to a higher nominal sr (`sr_crit ≈ 3.3`), so its old narrow-sweep
   "deficits" on MG/Lorenz were an artifact of comparing *below* that point. **Directed
   topology is a separate, task-dependent advantage that emerges supercritically:** large
   for memory (MC, control vs degree d ~+3.5) and input-driven emulation (NARMA, ~+4.3),
   emergent for forecasting (MG tail, ~+1.7), and absent for autonomous generation
   (Lorenz, where degree-rewiring matches it). v2a is a spectral negative control
   throughout. **Mechanism:** placement is spectrally grounded — the connectome's heavy
   weights compress its eigenvalue bulk (`src/analysis/spectral.py`), which both shifts
   its operating point higher and grants the wide stable operating range; the topology
   effect is real but mechanistically open. Full account in
   `PREDICTION_TASKS_INTERPRETATION.md`.

---

## 8. Methodological lessons learned

Caught at specific stages; recorded so future iterations don't repeat them.

- **Binary-vs-continuous weights, symmetric-vs-asymmetric W, and drifting
  self-loops are silent confounds at fixed sr.** Standardise all three across
  conditions; force zero diagonal. (v1 → v2a.)
- **Spectral-radius matching ≠ effective-criticality matching** when degree/weight
  distributions differ (the connectome's heavy hub weights depress its bulk vs λ_max).
  A variant's bulk becomes critical at `sr_crit = 1/bulk₉₅_ratio` — connectome ≈ 3.3 vs
  nulls ≈ 2.2–2.7 — so sweep **wide** (`[0,4]`) and compare at operating points. (v2a →
  operating-point analysis.)
- **Perron–Frobenius compression** in all-positive matrices shifts the effective
  regime upward in sr; sign assignment (E/I) mitigates it. (v2b → v2d.)
- **Heavy-tailed raw weights kneecap reservoirs** (a few large edges dominate the
  spectral radius). sqrt/log transform mitigates; the current NARMA bridge uses
  raw, so v2b/v2d there carry this caveat. (v2b.)
- **Compare curve-vs-curve at operating points, not at a single nominal sr.** Each
  variant's optimum lives at a different sr (the connectome's is higher — its bulk
  reaches criticality later), so *both* naive readings mislead: best-over-sweep-per-
  variant inverts the story, and a single "matched nominal sr" compares variants at
  *different effective criticalities* (this is what manufactured the connectome's
  apparent MG/Lorenz deficits on the old `[0,2]` sweep). Sweep wide and read whole
  curves. (NARMA bridge → operating-point analysis.)
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
progression (memory capacity ✓ → NARMA-10 ✓ → Mackey-Glass ✓ → Lorenz ✓, all on the
wide `[0,4]` sweep, toward the connectome-as-JEPA world model). The four-task arc is
**complete and unified** under the operating-point / robustness framework. Open
threads: the `sqrt`-vs-`raw` weight-transform sensitivity (§10); a possible
Lyapunov-exponent analysis module (an autonomous-LLE probe was explored and parked as a
future JEPA collapse-diagnostic — it is top-dominated, so not a substitute for the
spectral operating-point analysis); the MC evaluator speedup (it refits a Gram per lag,
~50× the other tasks' linear algebra); and the **scale row** (fly optic lobe, mouse) per
`PROJECT_PLAN.md`.

---

## 10. Open methodological questions

- **Topology vs weights — RESOLVED** by the `connectome_weight_permuted` placement
  control and reframed by the wide sweep (§6–7): placement is an **operating-point
  shift** (the placement leg reverses deficit→advantage as sr reaches the connectome's
  operating point, not a fixed handicap); directed topology is a **separate
  task-dependent advantage** that emerges supercritically (large MC/NARMA, emergent
  MG-tail, absent Lorenz).
- **Operating-point normalisation — ADOPTED.** Shared normaliser = top-eigenvalue
  matching with a **Suárez-width `[0,4]` sweep** (`matrix_config.SPECTRAL_RADII =
  linspace(0,4,39)`), with curve-vs-curve comparison; `sr_crit = 1/bulk₉₅_ratio` per
  variant. Top-matching is field-standard (Suárez et al. 2021) and the only cheap
  normaliser at scale (λ₁ via sparse eigs); just sweep wide enough to cover every
  variant's operating point.
- **Divergence-robust statistics — DONE.** `src/experiment/stats.py` caps blow-ups
  (`cfg.metric_divergence_cap`), reports a per-variant divergence rate, and tests
  significance with a rank-based permutation test (Cliff's delta + median alongside the
  capped Cohen's d). Used across all four tasks; it earns its keep on Lorenz, where
  closed-loop divergence is the primary failure mode (MC's bounded metric rarely
  diverges).
- **Weight transform.** All four tasks use raw synapse counts; `sqrt` is a one-line
  switch (`matrix_config.WEIGHT_TRANSFORM`) and the documented heavy-tail mitigation. It
  compresses the spectrum less, *raising* `bulk₉₅_ratio` and so *lowering* `sr_crit` —
  the connectome would recover at a lower nominal sr. Sign/structure of the results
  should survive; the exact operating points are a weight-transform choice. (Untested on
  the wide sweep.)
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

- **Connectome data:** `data/celegans/cook2019_connectome.xlsx`, sheet "hermaphrodite
  chemical" (SI corrected July 2020). N=300; 3000 undirected / 3669 directed
  off-diagonal edges; 38 autaptic self-loops dropped. Reservoir convention
  `W[i,j]` = weight j→i (the directed loader transposes Cook's native layout).
- **Dale signs (v2d):** `data/celegans/celegans_neurotransmitters.csv` — GABA-synthesizing
  neurons (DD, VD, RME, AVL, DVB, RIS = 26) inhibitory (−1), all else +1; source
  eLife 95402.
- **MC hyperparameters (v1-pinned):** `T=3000, warmup=500, max_lag=50,
  ridge_alpha=1e-6, leak=1.0, input_scaling=1.0, n_seeds=10`, BLAS threads 2.
- **Shared spectral-radius sweep (all four tasks):** 39-point `linspace(0,4,39)`
  (Suárez-width, strict superset of the old `[0,2]` 20-point grid);
  `experiments/celegans/matrix_config.SPECTRAL_RADII`. `sr_crit = 1/bulk₉₅_ratio` locates
  each variant's operating point (connectome ≈ 3.3, nulls ≈ 2.2–2.7).
- **Task matrix (all four tasks):** 3 conditions × **7 variants** (connectome +
  `connectome_weight_permuted` placement control + 5-rung ladder) × the 39-point sweep ×
  n=10 seeds. Frozen reservoir hyperparameters: MC (v1-pinned) `input_scaling=1.0,
  leak=1.0, ridge=1e-6`; NARMA `input_scaling=0.2, leak=1.0`; Mackey-Glass
  `input_scaling=0.5, leak=0.3` (h=84/h=300, driven teacher-forced, local generator
  bit-exact vs `reservoirpy`); Lorenz `input_scaling=0.1, leak=1.0, ridge=1e-7`
  (closed-loop free-running, 3-channel `Win`, direct next-state readout, metrics
  VPT + climate, local RK4 short-horizon cross-check only).
- **Weight-placement control:** `connectome_weight_permuted` — connectome's exact
  topology + a per-seed permutation of its exact weights (Dale signs kept; v2a a
  negative control). `connectome vs control` = placement, `control vs degree` =
  topology.
- **Statistics:** divergence-robust — rank-based permutation test (Holm-corrected) for
  significance, with Cliff's delta, capped Cohen's d, median, and a per-variant
  divergence rate; `metric_divergence_cap` = 2.0 (NRMSE), 10.0 (Lorenz climate), none for
  VPT/MC (bounded).
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
  and the task's `task_config.py` + `results/`.
- **Reviewing the task results:** `PREDICTION_TASKS_INTERPRETATION.md` is the
  reference summary across all four tasks (the operating-point + robustness picture and
  per-task results); each task's `task_config.py` + `results/` + `figures/` hold the
  specifics.
- **Running a substrate analysis:** `src/analysis/` + the
  `experiments/celegans/analysis/` drivers; see that dir's README.

The progression v1 → v2a → v2c → v2b → v2d → prediction tasks is a controlled
chain; breaking the one-variable-at-a-time discipline is the single failure mode
most likely to cost weeks. Hold the line.

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

**Headline (all four tasks).** At the canonical operating point (sr ≈ 0.95) the
connectome is **worse-or-equal** on every task. In the supercritical regime it is the
**most robust** variant: where the disk-like nulls peak sharply and **collapse** (or,
in closed loop, blow up), the connectome holds a wide flat plateau. The load-bearing
result — established by a **7-condition factorial** that crosses weight **sign**
(balanced ± vs all-positive), weight **tail** (homogeneous gaussian vs heavy-tailed
empirical), and **topology** (undirected/normal vs directed/non-normal) — is that this
robustness is driven **primarily by weight SIGN: the non-negative (Perron) structure of
real synaptic weights**, with heavy-tailedness a **secondary, task- and
topology-gated** contributor and **directedness minimal** (its one decisive role is
stabilising closed-loop Lorenz rollout). Full account in
`PREDICTION_TASKS_INTERPRETATION.md`.

**Mechanism — collapse-resistance in an all-positive substrate.** A non-negative matrix
has a large, isolated Perron eigenvalue over a compressed bulk; under global-gain
scaling its all-positive random nulls synchronise into that mode and **collapse off a
knife-edge** supercritically (MC of the rung-0 null falls from ~13 to ~4–5 by sr = 4),
while the connectome's heavy hub weights spread its operating point (`sr_crit =
1/bulk₉₅_ratio ≈ 3.3` vs nulls ≈ 2.2–2.7) so it rides through. **Sign the exact same
weights** (balanced ±, mean → 0): the Perron mode vanishes, the nulls stop collapsing,
and the connectome's advantage disappears (MC connectome−degree d +10.7 → +0.2
directed). The connectome is therefore *never the best substrate* — a directed-signed
random reservoir (a Girko-circular-law eigenvalue disk) beats it on raw memory — its
edge is **robustness against the collapse that non-negative random matrices suffer**,
which is biologically relevant because structural connectome weights *are* non-negative
(and *C. elegans* is 96% excitatory, so its Dale-signed matrix stays effectively
all-positive).

**This supersedes the earlier framing.** The pre-factorial account read the effect as
an **operating-point shift** with **directed topology a separate task-dependent
advantage**. That rested on a `gaussian-vs-empirical` contrast which **silently
conflated sign with tail** (gaussian weights are balanced ±, empirical weights are
all-positive); a one-variable **sign control** (`*_signed`: exact empirical magnitudes
with balanced random signs) showed sign is the larger lever and directedness is
minimal. The wide-sweep / curve-vs-curve methodology and the `connectome_weight_permuted`
placement control still stand — only the *attribution* changed (sign, not directedness).

**External replication (human connectome).** The sign-primary account now holds on a
**second, independent connectome**: the human structural connectome (Suárez 2021 dMRI SC —
undirected/normal, macro-scale, N=448/1000) reproduces the supercritical robustness
crossover on **memory capacity** (connectome−degree d **+13 to +15**, *strengthening* with
parcellation resolution) and **sustains closed-loop Lorenz** as an undirected non-negative
substrate (peak VPT ~4.5; edge = divergence resistance). This confirms the mechanism is a
property of **non-negative connectivity statistics**, not of *C. elegans* specifics or
directedness. Account in `PREDICTION_TASKS_INTERPRETATION.md` §7.

The three prediction tasks (NARMA-10 input-driven, Mackey-Glass driven-forecast, Lorenz
closed-loop) were added to bridge passive memory toward the north-star
connectome-as-JEPA world model; all four are evaluated across a wide sweep
`linspace(0, 4, 39)` (`sr_crit = 1/bulk₉₅_ratio` per variant), read curve-vs-curve.

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
**Two compute environments:** the **laptop** (WSL2) for development + `--smoke` checks,
and the **ada cluster** (Imperial, 128 CPU cores) for full runs — details in §12.

```
cognitive-connectomes/
├── PROJECT_KNOWLEDGE_BASE.md / PROJECT_PLAN.md
├── PREDICTION_TASKS_INTERPRETATION.md        (four-task interpretation summary)
├── data/                                     (per-species subdirs)
│   ├── celegans/
│   │   ├── cook2019_connectome.xlsx          (Cook 2019 SI, corrected July 2020)
│   │   └── celegans_neurotransmitters.csv    (Dale E/I signs; eLife 95402)
│   └── human/                                (Suárez 2021 Lausanne SC/FC; .mat + built_consensus/ gitignored)
│       └── README.md                         (dataset provenance + consensus construction)
├── src/                                       (the library; editable-installed)
│   ├── connectomes/  celegans_cook2019.py (load modes), neurotransmitters.py (Dale);
│   │                 human_suarez.py, consensus.py (Betzel/Suárez group consensus)
│   ├── nulls/        random_gaussian, erdos_renyi, degree_rewire, clustering_rewire,
│   │                 modularity_rewire, validation.py        (all directed-aware)
│   ├── reservoir/    blas.py, weights.py, build.py
│   ├── tasks/        memory_capacity.py, narma.py, mackey_glass.py, lorenz.py
│   ├── experiment/   GENERIC runner.py / stats.py (divergence-robust) / plots.py / config.py
│   └── analysis/     spectral.py  (substrate analysis, connectome-agnostic; first of a series)
├── experiments/
│   ├── celegans/                              (cellular scale; full directed factorial)
│   │   ├── substrates.py   (SubstrateBuilder + weight-placement control), matrix_config.py
│   │   ├── celegans_mc/             task_config.py, run.py, results/, figures/  (Jaeger memory capacity)
│   │   ├── celegans_narma10/        task_config.py, run.py, plot_demo.py, results/, figures/
│   │   ├── celegans_mackey_glass/   task_config.py (2 horizons), run.py, plot_demo.py, results/, figures/
│   │   ├── celegans_lorenz/         task_config.py (2 metrics), run.py, plot_demo.py, results/, figures/
│   │   └── analysis/                spectral.py driver (uses src/analysis); figures/, results/
│   └── human/                                 (macro-scale probe; undirected-only sub-factorial)
│       ├── substrates.py (HumanSubstrateBuilder), matrix_config.py, build_consensus.py
│       ├── human_mc/ human_narma10/ human_mackey_glass/ human_lorenz/  (scale-tagged results/scale_<N>/)
│       └── analysis/   spectral.py, brain_overlay.py, network_matrix.py, realizations.py; figures/, results/
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
experiments.celegans.celegans_narma10.run`. The framework now spans **two connectomes**:
the cellular *C. elegans* (the full directed factorial) and the macro-scale **human SC**
(`experiments/human/`, an undirected-only sub-factorial reusing the same runner, null
ladder, and symmetric weight schemes; its `run.py`s add `--scale {448,1000}` / `--sr-max`
/ `--jobs` flags for the ada cluster).

A parallel **substrate-analysis tier** characterises the recurrent matrices
themselves (independent of any task): generic, connectome-agnostic tools in
`src/analysis/` (first module: `spectral.py`) with connectome-specific drivers
in `experiments/<connectome>/analysis/`. `spectral.py` grounds the
placement→memory mechanism (the connectome's eigenvalue bulk is the most
compressed); it is the template for the planned deeper topological analyses
(degree, clustering, motifs, modularity, reciprocity).

All `*.parquet` outputs are gitignored as regenerable; `figures/*.png` are tracked.

**Key library interfaces.**
- Connectome loader `load(processing=...)`: `binary_undirected_chemical` (undirected
  conditions), `directed_weighted_chemical` (directed conditions; reservoir convention
  `W[i,j]`=j→i).
- Null generators `generate(adjacency, seed, directed=False, **kwargs)` returning
  a binary mask. Rungs 2–4 accept `directed=True`.
- `validate_null(original, generated, preserved_property, ...)` properties:
  `edge_count`, `degree_sequence`, `in/out_degree_sequence`, `density`,
  `clustering`, `modularity`, `directed_clustering`, `directed_block_matrix`.
- `apply_weight_scheme(mask, scheme, seed, **kwargs)` — seven schemes spanning the
  sign × tail × topology factorial: `symmetric_gaussian` / `asymmetric_gaussian`
  (homogeneous, balanced ±); `symmetric_empirical` / `asymmetric_empirical`
  (heavy-tailed, all-positive); `symmetric_empirical_randsign` /
  `asymmetric_empirical_randsign` (heavy-tailed, balanced ± sign controls);
  `asymmetric_empirical_signed` (heavy-tailed, per-neuron Dale E/I).
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
cleanup, the null ladder, directed weights) — historical phase labels, kept as
provenance (old↔new condition-name map in §12). Their narrow-sweep numbers were
reproduced by the wide-sweep prediction-task runs, whose **first-pass**
operating-point / directedness reading was then **superseded** by the sign-primary
account of the **7-condition factorial** (final entry) — which holds the current
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

**Prediction tasks + wide sweep (first pass).** Added three prediction tasks on the
shared infrastructure, each run over the 7-variant null ladder × 39-point `[0,4]` sweep
× 10 seeds: **NARMA-10** (input-driven emulation; frozen `input_scaling=0.2, leak=1.0`);
**Mackey-Glass** (driven teacher-forced forecast of the β=0.2, γ=0.1, n=10, τ=17 delay
system at h=84/h=300; `input_scaling=0.5, leak=0.3`; local generator bit-exact vs
`reservoirpy`); **Lorenz** (closed-loop free-running of σ=10, ρ=28, β=8/3; direct
next-state readout, 3-channel `Win`, `input_scaling=0.1, leak=1.0, ridge=1e-7`; metrics
**VPT** + **climate** marginal-Wasserstein). MC was re-run on the same footing. The
methodological win was sweeping wide enough to reach each variant's operating point
(`sr_crit = 1/bulk₉₅_ratio`): read curve-vs-curve the connectome is worse-or-equal at
canonical and the **most robust** supercritically on every task (flat plateau where
disk-like nulls peak sharply and collapse; 0% closed-loop blow-ups on Lorenz vs 26–31%
for random/ER). **First-pass attribution — an operating-point *placement* shift plus a
separate *directed-topology* advantage — was later superseded** (next entry): the
realism contrast (undirected-gaussian vs directed-empirical) conflated sign with tail.

**Weight-placement control (`connectome_weight_permuted`).** A shared control variant:
the connectome's *exact* topology and *exact* weight multiset, but a per-seed
**permutation** of which edge carries which weight (Dale signs re-applied for the Dale
condition; the gaussian conditions are distribution-preserving negative controls).
Because the connectome, the control, and the rung nulls all share the weight
distribution, two comparisons decompose the effect: **connectome vs control = weight
placement**; **control vs degree_rewire = topology**. Still valid and used throughout.

**Sign confound + 7-condition factorial (current results).** The realism contrast
bundled two differences: weight **sign** (gaussian weights are balanced ±; empirical
weights are all-positive) and weight **tail** (homogeneous vs heavy-tailed). A
one-variable **sign control** — the connectome's *exact* empirical magnitudes with
balanced random signs (`*_empirical_signed`) — plus a **directed-gaussian** cell
completed a **sign × tail × topology 2×3 factorial**, giving the **7 core conditions**
(`undirected_gaussian`, `undirected_empirical_signed`, `undirected_empirical`,
`directed_gaussian`, `directed_empirical_signed`, `directed_empirical`, +
`directed_empirical_dale` as the Dale anchor). Re-running all four tasks on the full
factorial shows the supercritical robustness is **primarily a weight-SIGN
(non-negativity / Perron) effect**: it lives in the all-positive-empirical column
(MC/NARMA connectome−degree d **+8 to +11** at sr≈3–4), and **signing the exact same
weights collapses it** (entirely in the directed case, ~60% undirected). Heavy tail is a
**secondary, task-gated residual** (normal-gated for MC, directed-gated for NARMA/MG);
**directedness is minimal** except that it strongly stabilises closed-loop Lorenz
rollout (Lorenz is *parity* with degree on fidelity, its edge is 0% divergence). The
connectome is never the top substrate — a directed-signed random reservoir (a
Girko-circular-law eigenvalue disk) beats it on raw memory — its edge is
**collapse-resistance in an all-positive substrate**, biologically relevant because
structural weights are non-negative and *C. elegans* is 96% excitatory. Full per-task
account in `PREDICTION_TASKS_INTERPRETATION.md`.

**Human macro-scale probe (cross-connectome generalisation).** The account was then tested
on a **second, independent connectome** — the human structural connectome (Suárez 2021 dMRI
SC), an undirected/normal, macro-scale graph. Substrate = a **self-built distance-dependent
group consensus** (Betzel 2018 / Suárez procedure) from the `.mat` individual SC, cortical
**N=448 and N=1000** (validated against the published consensus, r≈0.99); design = the
**undirected sub-factorial** (`human_gaussian` → `human_empirical_signed` →
`human_empirical`) × the same 7-variant ladder × a wide `[0,6]` sweep × 10 seeds, run on
ada. **MC reproduces the sign-primary crossover and it *strengthens* with parcellation
resolution** (connectome−degree d +13.2@448 / +15.1@1000; the sign step is scale-invariant
~+8, the tail step grows +2.9→+4.1). **Lorenz: an undirected non-negative substrate
sustains closed-loop rollout** (peak VPT ~4.5, faithful climate; divergence 7%@448 →
0%@1000; parity with degree on fidelity) — sharpening the directedness reading (closed-loop
stability tracks weight SIGN, not directedness). NARMA-10 also run (results present);
Mackey-Glass infrastructure in place (not yet run). Held out of the cellular scale row. Full
account in `PREDICTION_TASKS_INTERPRETATION.md` §7.

---

## 7. Key findings to date

1. **Canonical: worse-or-equal; supercritical: most robust.** At sr ≈ 0.95 the
   connectome is worse-or-equal on all four tasks; read curve-vs-curve on the wide
   `[0,4]` sweep it is the **most robust** variant — a wide flat plateau where disk-like
   nulls peak sharply and collapse (or, on closed-loop Lorenz, blow up). Robustness, not
   a higher ceiling (its peak sits at or below the best null's).
2. **That robustness is primarily a weight-SIGN (non-negativity / Perron) effect** —
   the load-bearing current finding. Established by the **7-condition sign × tail ×
   topology factorial** plus a one-variable **sign control**: the effect lives in the
   all-positive-empirical column (MC/NARMA connectome−degree d **+8 to +11** at sr≈3–4),
   and **signing the exact same weights collapses it** (entirely directed, ~60%
   undirected; gaussian ≈ flat). This **supersedes** the earlier "operating-point shift +
   directed-topology advantage" reading, which was a **sign×tail confound** (the
   gaussian-vs-empirical realism contrast bundled sign with tail).
3. **Mechanism — collapse-resistance.** All-positive random matrices have a Perron mode
   that synchronises and collapses at criticality (rung-0 MC ~13 → ~4–5 by sr 4); the
   connectome's heavy hub weights spread its operating point (`sr_crit ≈ 3.3` vs nulls
   ≈ 2.2–2.7) so it holds while they collapse. By **Girko's circular law** a
   directed-signed random reservoir is the raw-memory-optimal eigenvalue *disk*, so the
   connectome is **never the best substrate** — its edge is resisting a collapse that
   only non-negative random matrices suffer.
4. **Heavy tail — secondary, task-and-topology-gated.** A real but smaller residual that
   survives signing in one cell per task, and the cell flips: **normal-gated for MC**
   (undirected), **directed-gated for NARMA/MG** (driven). Sign is the larger lever
   (~2× the tail spectrally).
5. **Directedness — minimal for passive/driven skill, decisive for closed-loop
   stability.** ~+1 on MC/NARMA/MG; on Lorenz it is the difference between ~50–77% and
   ~0–31% closed-loop divergence. (*Refined by finding 9:* the human probe shows an
   **undirected** non-negative substrate also sustains Lorenz, so closed-loop stability
   tracks weight **sign** — directedness proxied it in the *C. elegans* factorial.)
6. **Lorenz — parity, not dominance.** On fidelity (VPT, climate) the connectome *ties*
   degree_rewire in the biological (all-positive) conditions; its unambiguous edge is
   **0% closed-loop divergence** (vs 26–31% for random/ER). And non-negativity is
   *required* for the autonomous task to function at all (signing collapses VPT ~4.5 →
   ~0.5).
7. **Methodology holds; only the attribution moved.** Spectral-radius matching ≠
   effective-criticality matching when degree/weight distributions differ (`sr_crit =
   1/bulk₉₅_ratio`); sweep wide and compare curve-vs-curve. The wide sweep, the
   `connectome_weight_permuted` placement control, and the divergence-robust stats all
   stand — the change from the prior framing is mechanistic attribution (**sign, not
   directedness**), grounded in `src/analysis/spectral.py` + the sign control.
8. **Historical (still valid):** degree sequence is sufficient to explain MC *at
   canonical* sr across both weight regimes; higher-order structure (clustering/
   modularity, from the v2c disambiguation) matters supercritically — now understood as
   part of the sign/collapse-resistance story rather than a standalone topology effect.
9. **The sign-primary account replicates on a second connectome (human macro-scale).** The
   human structural connectome (Suárez 2021 dMRI SC; undirected, N=448/1000) reproduces the
   supercritical robustness on **MC** (connectome−degree d **+13→+15**, *strengthening* with
   parcellation resolution; sign step scale-invariant ~+8) and on **closed-loop Lorenz** (an
   undirected non-negative substrate sustains the attractor — peak VPT ~4.5, divergence
   7%@448 → 0%@1000, parity with degree on fidelity). This is **external validation** on an
   independent organism, imaging modality (dMRI), and scale, and it **sharpens the
   directedness reading**: closed-loop stability tracks weight SIGN, not directedness (finding
   5's "decisive for closed-loop stability" is really non-negativity, which directedness
   proxied in *C. elegans*). Full account in `PREDICTION_TASKS_INTERPRETATION.md` §7.

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
- **Perron–Frobenius compression** in all-positive matrices concentrates a large
  isolated eigenvalue over a compressed bulk — now understood as the **primary driver**
  of the connectome's supercritical robustness (it makes all-positive *random* nulls
  collapse at criticality; the connectome's hub weights let it hold). Balanced signs
  remove the Perron mode and the effect. (v2b phase → the sign control.)
- **A "gaussian vs empirical" weight contrast conflates SIGN with TAIL.** Gaussian
  schemes are balanced ±; empirical (synapse-count) schemes are all-positive — so a
  contrast that varies "weight realism" silently varies both sign and heavy-tailedness.
  Add an explicit **sign control** (empirical magnitudes + balanced random signs) to
  decouple them; here it revealed sign, not tail or directedness, as the primary lever.
  (The lesson that reframed the whole four-task account.)
- **Heavy-tailed raw weights kneecap reservoirs** (a few large edges dominate the
  spectral radius). sqrt/log transform mitigates; the tasks use raw synapse counts, so
  the empirical conditions carry this caveat.
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
  general. In the empirical conditions the connectome also keeps real weights while
  nulls resample — the topology-vs-weights confound, decomposed by the
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
**complete and unified** under the **sign-primary robustness account** (7-condition
factorial; §6–7). Open threads:
- **Human macro-scale probe (Suárez 2021 dMRI SC) — DONE for MC + Lorenz** (§6–7;
  interpretation doc §7). The sharpened, reversed prediction was **confirmed**: the
  non-negative, heavy-tailed human SC shows the **strong** robustness crossover (MC d
  +13→+15, *strengthening* with resolution), and the undirected non-negative substrate
  **sustains closed-loop Lorenz**. Held out of the cellular scale row. Remaining human
  threads: the **full four-task interpretation pass** (NARMA-10 is run; Mackey-Glass not
  yet run); anatomical **I/O routing** (subcortical input + intrinsic-network readout with
  a placement null — see `HUMAN_IO_ROUTING_PLAN.md`); **per-subject variability** (70
  subjects, a population inference distinct from the single-consensus one); and the finer
  **within-connectome scale sweep** (N=68→1000).
- **Cross-species E/I prediction.** A more inhibition-heavy connectome (mammalian ~20%)
  would push the effective matrix toward balanced signs → weaker robustness — testable
  with E/I-resolved connectomes.
- The `sqrt`-vs-`raw` weight-transform sensitivity (§10); the MC evaluator speedup (it
  refits a Gram per lag, ~50× the other tasks' linear algebra); and the **scale row**
  (fly optic lobe, mouse) per `PROJECT_PLAN.md`.

---

## 10. Open methodological questions

- **What drives the robustness — REFRAMED to weight SIGN (§6–7).** The 7-condition
  factorial + one-variable sign control show the supercritical robustness is **primarily
  a non-negativity (Perron) effect**, with heavy-tail a secondary task-gated residual and
  directedness minimal (its one role: stabilising closed-loop Lorenz). This **supersedes**
  the earlier reading — an operating-point *placement* shift plus a separate
  *directed-topology* advantage — which rested on a **sign×tail confound** in the
  gaussian-vs-empirical realism contrast. The `connectome_weight_permuted` placement leg
  still decomposes placement vs topology, but the headline attribution is now sign.
- **Tail-gating mechanism — OPEN.** *Why* the secondary heavy-tail residual is
  normal-gated for MC (undirected) but directed-gated for NARMA/MG (driven) is
  characterised, not mechanistically pinned.
- **Operating-point normalisation — ADOPTED.** Shared normaliser = top-eigenvalue
  matching with a **Suárez-width `[0,4]` sweep** (`matrix_config.SPECTRAL_RADII =
  linspace(0,4,39)`), with curve-vs-curve comparison; `sr_crit = 1/bulk₉₅_ratio` per
  variant. Top-matching is field-standard (Suárez et al. 2021) and the only cheap
  normaliser at scale (λ₁ via sparse eigs); just sweep wide enough to cover every
  variant's operating point. **Corollary from the human probe:** `sr_crit` *rises with
  parcellation resolution* (the bulk compresses further with N: ~3.1@448 → ~4.0@1000), so
  `[0,4]` truncated N=1000 — the human runs widen to `[0,6]` via the `--sr-max` flag (a
  strict superset whose first 39 points reproduce `[0,4]`).
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
- **Dale signs (`directed_empirical_dale`):** `data/celegans/celegans_neurotransmitters.csv`
  — GABA-synthesizing neurons (DD, VD, RME, AVL, DVB, RIS = 26) inhibitory (−1), all else
  +1; source eLife 95402. Only 3.6% of edges → the Dale matrix is effectively all-positive.
- **Human macro-scale probe:** substrate = a **self-built distance-dependent group
  consensus** (Betzel 2018 / Suárez 2021) from the `.mat` individual SC, cortical **N=448 /
  N=1000** (cached at `data/human/built_consensus/`, gitignored); loaders
  `src/connectomes/human_suarez.py` + `consensus.py`; provenance in `data/human/README.md`.
  **3 undirected conditions** (`human_gaussian` → `human_empirical_signed` →
  `human_empirical`) × the same 7-variant ladder × a **`[0,6]`** sweep (`--sr-max`; `sr_crit`
  rises with N) × 10 seeds; runs on ada (`--jobs 128`). **MC + NARMA-10 + Lorenz run** (MC +
  Lorenz interpreted, interpretation doc §7); Mackey-Glass infra in place (not yet run).
- **ada cluster (compute for full runs):** repo at
  `/vol/bitbucket/mmd25/thesis/cognitive-connectomes`, venv `.venv`
  (`source .venv/bin/activate`). **CPU-only** — pure numpy/scipy, so the node's 2× L40 GPUs
  are unused; 128 cores → pass `--jobs 128` (fork-parallel grid, bit-identical to
  sequential). Launch full runs in `tmux`, then **rsync results/figures back to the
  laptop**. Treat ada as **run-only**: commit from the laptop after rsync (committing on ada
  causes pull conflicts). The laptop does development + `--smoke`. Typical wall-clock:
  human MC ~2 min, Lorenz N=448 ~7 min / N=1000 ~90 min.
- **MC hyperparameters (v1-pinned):** `T=3000, warmup=500, max_lag=50,
  ridge_alpha=1e-6, leak=1.0, input_scaling=1.0, n_seeds=10`, BLAS threads 2.
- **Shared spectral-radius sweep (all four tasks):** 39-point `linspace(0,4,39)`
  (Suárez-width, strict superset of the old `[0,2]` 20-point grid);
  `experiments/celegans/matrix_config.SPECTRAL_RADII`. `sr_crit = 1/bulk₉₅_ratio` locates
  each variant's operating point (connectome ≈ 3.3, nulls ≈ 2.2–2.7).
- **Task matrix (all four tasks):** **7 conditions** × **7 variants** (connectome +
  `connectome_weight_permuted` placement control + 5-rung ladder) × the 39-point sweep ×
  n=10 seeds. Frozen reservoir hyperparameters: MC (v1-pinned) `input_scaling=1.0,
  leak=1.0, ridge=1e-6`; NARMA `input_scaling=0.2, leak=1.0`; Mackey-Glass
  `input_scaling=0.5, leak=0.3` (h=84/h=300, driven teacher-forced, local generator
  bit-exact vs `reservoirpy`); Lorenz `input_scaling=0.1, leak=1.0, ridge=1e-7`
  (closed-loop free-running, 3-channel `Win`, direct next-state readout, metrics
  VPT + climate, local RK4 short-horizon cross-check only).
- **Weight-placement control:** `connectome_weight_permuted` — connectome's exact
  topology + a per-seed permutation of its exact weights (Dale signs kept; the gaussian
  conditions are distribution-preserving negative controls). `connectome vs control` =
  placement, `control vs degree` = topology.
- **Statistics:** divergence-robust — rank-based permutation test (Holm-corrected) for
  significance, with Cliff's delta, capped Cohen's d, median, and a per-variant
  divergence rate; `metric_divergence_cap` = 2.0 (NRMSE), 10.0 (Lorenz climate), none for
  VPT/MC (bounded).
- **Substrate analysis tier:** `src/analysis/spectral.py` (connectome-agnostic
  spectral metrics + plots) + `experiments/celegans/analysis/spectral.py` driver
  (`python -m experiments.celegans.analysis.spectral`). Grounds the
  placement→memory mechanism; first of the planned topological-analysis series. The human
  probe adds `experiments/human/analysis/` drivers (spectral, brain-overlay, Yeo-network,
  weight-realizations).
- **Conditions (7-condition sign × tail × topology factorial):** `undirected_gaussian`,
  `undirected_empirical_signed`, `undirected_empirical`, `directed_gaussian`,
  `directed_empirical_signed`, `directed_empirical`, `directed_empirical_dale`. The
  per-topology weight ladder gaussian → signed-empirical → empirical isolates the **tail**
  (gaussian→signed) and **sign** (signed→empirical) sub-factors; `*_signed` are balanced
  random-sign controls, `directed_empirical_dale` the biological Dale anchor.
- **Old↔new condition-name map** (legacy `v2x` labels retired): `v2a`=`undirected_gaussian`,
  `v2ae`=`undirected_empirical`, `v2ae_randsign`=`undirected_empirical_signed`,
  `v2bg`=`directed_gaussian`, `v2b`=`directed_empirical`,
  `v2b_randsign`=`directed_empirical_signed`, `v2d`=`directed_empirical_dale`. The
  experimental-history phase labels (`v1 → v2a → v2c → v2b → v2d`) are kept in §6 as
  provenance.

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
- **Continuing the human macro-scale probe:** also load `data/human/README.md` (dataset +
  consensus construction) and `experiments/human/`; for the I/O-routing thread,
  `HUMAN_IO_ROUTING_PLAN.md`.

The progression v1 → v2a → v2c → v2b → v2d → prediction tasks is a controlled
chain; breaking the one-variable-at-a-time discipline is the single failure mode
most likely to cost weeks. Hold the line.

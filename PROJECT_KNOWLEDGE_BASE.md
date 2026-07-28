# Cognitive Connectomes — Project Knowledge Base

A research project on connectome-constrained reservoir computing. Uses
empirically measured connectomes as the recurrent matrix of an echo-state
network and asks what biological connectivity contributes — through the geometry
of the activity manifold — beyond random or degree-matched baselines.

This document is the single canonical reference for *what is implemented and what
has been found*. Load it into fresh Claude conversations as starting context; the
forward plan and open direction live in `PROJECT_PLAN.md`. Detail companions:
`PREDICTION_TASKS_INTERPRETATION.md` (the four-task substrate floor),
`MANIFOLD_PROBES_IMPLEMENTATION.md` and `PHASE_DIAGRAM_EXPERIMENT.md` (the
manifold-geometry and sign-composition experiments).

---

## 1. TL;DR

Connectome-constrained reservoir computing: use an empirically measured connectome
as the fixed recurrent matrix of an echo-state network, train only a linear readout,
and ask what biological connectivity contributes beyond random or degree-matched
baselines. The current question: **which structural and weight properties of
biological connectomes shape the geometry of the reservoir's activity manifold, and
how does that geometry set computational capacity?** Primary substrate for the
manifold work: the human structural connectome, N=448 (Suárez 2021 Lausanne).
Companion detail docs: `MANIFOLD_PROBES_IMPLEMENTATION.md` and
`PHASE_DIAGRAM_EXPERIMENT.md` (this term's experiments);
`PREDICTION_TASKS_INTERPRETATION.md` (the four-task substrate floor).

**The floor — a sign-primary robustness account.** A 7-condition sign × tail ×
topology factorial (four tasks, replicated on two connectomes) established that the
connectome's one robust edge is supercritical and driven **primarily by weight
SIGN**: a non-negative (Perron) matrix has a large isolated eigenvalue over a
compressed bulk; its all-positive random nulls synchronise into that mode and
collapse at criticality, while the connectome's compact bulk (`sr_crit = 1/bulk₉₅`)
lets it ride through. Sign the same weights and the effect vanishes; heavy tail is a
secondary residual, directedness minimal. The connectome is never the *best*
substrate — its edge is **collapse-resistance in an all-positive substrate**,
biologically relevant because structural weights are non-negative. Full account in
`PREDICTION_TASKS_INTERPRETATION.md`.

**Manifold geometry (Probes 1–3).** Recasting the floor geometrically: weight sign
gates a supercritical **manifold** transition — non-negativity freezes a
low-dimensional, temporally coherent, spatially low-frequency manifold; balanced sign
collapses it into a saturated period-2 state. Within the non-negative regime,
**topology sets memory through readout dimensionality**, measured by the **ridge
effective rank** `d_eff = Σᵢ gᵢ/(gᵢ+α)` — *not* participation ratio, which misses it.
`d_eff` orders the memory-capacity null ladder perfectly (Spearman +1.00) and predicts
MC within-regime (+0.998); its spectral origin is the connectome's anomalously
**compact eigenvalue bulk** (bulk₉₅ 0.325 vs 0.48–0.55 for nulls). Two computational
axes emerge: **memory reads out effective rank; generative (Lorenz) prediction reads
out trajectory straightness (curvature).**

**Sign-composition phase diagram.** Grading the negative-weight fraction *f* from 0
(all-positive) to 0.5 (balanced) × spectral radius maps where topology controls the
manifold geometry computation reads out. Headline: a **memory ↔ generation
dissociation** — the two advantages occupy opposite regions of (*f*, σ) space,
governed by **different spectral controllers** (memory ← the hub-localised common
mode; generation ← the global effective radius `σ_eff = bulk₉₅·σ·⟨1−x²⟩` crossing 1).
Sign composition is thus a single knob trading memory capacity against generative
robustness. Under a biological **Dale** sweep the connectome sustains a faithful
straight Lorenz attractor up to **~20% inhibition** then collapses — a tolerance
ceiling (not a tuned optimum) sitting at the biological E/I ratio. A **placement**
study shows the memory effect is **hub-gated**: making hub neurons inhibitory collapses
it ~2× faster than peripheral, robust to whether "hub" means degree or eigenvector
centrality — confirming the memory controller is the Perron/common mode carried by the
hubs. Full account in `PHASE_DIAGRAM_EXPERIMENT.md`.

Direction — which of these results to build into the paper — is open and lives in
`PROJECT_PLAN.md`.

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

The programme has since moved from *whether* the connectome scores better to *why* —
from performance comparisons toward the **geometry of the reservoir's activity
manifold**: how connectivity structure and weight sign shape the manifold's
dimensionality and temporal predictability, and how that geometry sets computational
capacity (§6–7).

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
│   ├── tasks/        memory_capacity.py (+ _routing), narma.py, mackey_glass.py, lorenz.py
│   │                 (evaluators take an opt-in `collect_states` → driven-state capture)
│   ├── experiment/   GENERIC runner.py / stats.py (divergence-robust) / plots.py / config.py
│   └── analysis/     connectome-agnostic substrate + driven-state analysis:
│                     spectral.py, null_models.py, weight_structure.py (substrate structure);
│                     manifold.py (state geometry: d_eff, curvature, PR);
│                     sign_composition.py (graded edge/Dale sign transform)
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
│       └── analysis/   spectral.py, brain_overlay.py, network_matrix.py, realizations.py,
│                       connectogram.py, brain_glass_interactive.py; figures/, results/;
│                       manifold/       (driven-state geometry Probes 1-3; __main__ CLI)
│                       phase_diagram/  (sign-fraction × spectral-radius phase-diagram experiment)
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

A parallel **substrate-and-state analysis tier** characterises both the recurrent
matrices and the activity they drive, independent of the task runner: generic,
connectome-agnostic tools in `src/analysis/` with connectome-specific drivers in
`experiments/<connectome>/analysis/`. Three module groups: **substrate structure**
(`spectral.py` — eigenvalue bulk, the `bulk₉₅`/`sr_crit` mechanism; `null_models.py`
— graph-structural measures over the null ladder; `weight_structure.py` — value/sign
structure across weight realisations); **driven-state geometry** (`manifold.py` —
ridge effective rank `d_eff`, trajectory curvature, participation ratio, on the
reservoir states captured via the evaluators' opt-in `collect_states` hook); and the
**`sign_composition.py`** transform (a graded edge-wise / node-wise-Dale sign flip on
a non-negative substrate, with degree / eigenvector-centrality placement scores).

Two substantial human-scale analysis **programs** build on these (both under
`experiments/human/analysis/`, each a self-contained package with its own `__main__`
CLI): the **manifold probes** (`manifold/`, Probes 1–3, linking state geometry to
memory and generation) and the **sign-composition × spectral-radius phase diagram**
(`phase_diagram/`, a `capture → analyse → plots → eigcheck` package mapping where
topology controls the manifold geometry that computation reads out, over the
negative-weight-fraction × spectral-radius plane; edge + Dale sign modes, stratified /
hub / periphery placement, degree + eigenvector scores). Detailed working notes live
in `MANIFOLD_PROBES_IMPLEMENTATION.md` and `PHASE_DIAGRAM_EXPERIMENT.md` (untracked).
This tier remains the template for the planned deeper topological analyses (motifs,
reciprocity, richer modularity).

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
  `climate_error`). Each also accepts `collect_states=True` to return the driven
  post-warmup state matrix under `states` (the additive manifold-probe capture path;
  off by default, so committed task runs are byte-identical).
- Manifold geometry `src/analysis/manifold.py` (on a driven state matrix `x`):
  `gram_spectrum(design)` → `ridge_effective_rank(gram, alpha)` (the `d_eff` memory
  order parameter), `mean_curvature(x)` (trajectory straightness), `participation_ratio`.
- Sign transform `src/analysis/sign_composition.py`: `sign_fraction_matrix` (edge-wise,
  symmetry-preserving) / `sign_fraction_matrix_dale` (node-wise Dale — negates an
  inhibitory neuron's outgoing **column**, breaking symmetry), selected by
  `node_importance(W, mode="degree"|"eigenvector")` with `stratified` / `hub_first` /
  `periphery_first` placement; `f=0` is the identity.

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

*The v1→v2 entries are the framework's methodological provenance — confound cleanup,
the null ladder, directed weights — kept terse (old↔new condition map in §10). The
four-task sign factorial and its human replication are the **substrate floor**; the
manifold-geometry and phase-diagram programmes are the current work, recasting that
floor in terms of activity-manifold geometry.*

**Framework provenance (v1 → v2).** v1 found connectome ≈ degree_rewire on MC, both
below random — caught post-hoc as a confound stack (binary-vs-continuous weights,
symmetry, self-loops, miscounted edges), which prompted the whole v2 controlled
pipeline. v2a reproduced the four conditions within ~0.6 MC at sr=0.95 (v1's gap was
*entirely* the confound), and a supercritical probe found the first real signal
(connectome > degree_rewire, Cohen's d 0.64→1.47). v2c added clustering/modularity
rewires (both close the rung-2 gap → degree-only ruled out); v2b added directed +
empirical weights (the supercritical MC effect is regime-independent). A strict
one-variable-at-a-time chain; breaking it is the project's main failure mode.

**The four-task sign factorial (the substrate floor).** Three prediction tasks
(NARMA-10, Mackey-Glass, Lorenz) were added and MC re-run, each over a 7-variant null
ladder × wide `[0,4]` sweep × 10 seeds, read curve-vs-curve at each variant's operating
point (`sr_crit = 1/bulk₉₅`). A first-pass reading (operating-point shift +
directed-topology advantage) was **superseded** on finding that the `gaussian-vs-empirical`
realism contrast **silently conflated weight sign with weight tail**. A one-variable
sign control (`*_empirical_signed`: exact empirical magnitudes, balanced random signs)
plus a directed-gaussian cell completed a **sign × tail × topology factorial (7 core
conditions)**, localising the connectome's supercritical robustness **primarily to
weight SIGN (non-negativity / Perron)**: it lives in the all-positive-empirical column
(MC/NARMA connectome−degree d +8 to +11 at sr≈3–4) and signing the same weights
collapses it; heavy tail is a secondary task-gated residual, directedness minimal (its
one role: stabilising closed-loop Lorenz). The `connectome_weight_permuted` placement
control decomposes the effect (connectome vs control = placement; control vs degree =
topology). Full account: `PREDICTION_TASKS_INTERPRETATION.md`.

**Human macro-scale replication.** The sign-primary account holds on a second,
independent connectome — the human structural connectome (Suárez 2021 dMRI SC;
undirected, self-built distance-dependent group consensus, N=448/1000). MC reproduces
the supercritical crossover and it *strengthens* with parcellation resolution
(connectome−degree d +13.2@448 → +15.1@1000); an undirected non-negative substrate
sustains closed-loop Lorenz (peak VPT ~4.5), sharpening the directedness reading —
closed-loop stability tracks weight **sign**, not directedness. External validation
across organism, imaging modality, and scale. Account:
`PREDICTION_TASKS_INTERPRETATION.md` §7. **The human N=448 consensus is the substrate
for all manifold-geometry work below.**

**Manifold probes 1–3 (activity-manifold geometry).** Characterise the *geometry of
the driven activity manifold* across the null ladder and sign conditions, on states
captured via the evaluators' opt-in `collect_states` hook (bit-for-bit identical to the
committed task runs). Full working notes: `MANIFOLD_PROBES_IMPLEMENTATION.md`.
- **Probe 1 (shape).** Weight sign gates a supercritical *manifold* transition:
  balanced-sign nets transition; all-positive nets stay frozen across the whole sweep.
  Curvature is trimodal — ~0.25 rad (straight Lorenz), ~2.09 = 2π/3 (a quasi-static map
  of white noise; the σ=0 no-recurrence row lands here too), ~π (a saturated period-2
  flip-flop, *ordered*, not a random walk).
- **Probe 2 (basis).** Sign selects where activity lives: balanced sign → dominant
  W-eigenmodes; all-positive → low-frequency connectome harmonics. Mechanism: the
  Perron/DC common mode carries the mean and is removed by time-centring (top-mode
  fluctuation variance ≈0.000), leaving a smooth low-frequency residual. The inversion
  also appears in the all-positive degree null — a sign effect, not connectome-specific.
- **Probe 3 (geometry → performance).** The readout-relevant dimensionality is the
  **ridge effective rank** `d_eff = Σᵢ gᵢ/(gᵢ+α)` (effective d.o.f. of the ridge
  solution), not participation ratio. `d_eff` orders the MC null ladder perfectly
  (Spearman +1.00) and predicts MC within-regime (+0.998); PR fails (+0.11 / +0.31).
  Spectral origin: the connectome's anomalously compact eigenvalue bulk (bulk₉₅ 0.325 vs
  0.48–0.55 for nulls; orders the MC ladder at −0.96; bulk₉₅ = 1/sr_crit). Two axes:
  **memory ← effective rank; generation (Lorenz) ← trajectory straightness (curvature)**.
  (Caveat: `d_eff`'s advantage over PR is MC-specific — PR also orders NARMA.)

**Sign-composition × spectral-radius phase diagram.** Grade the negative-weight
fraction *f* ∈ [0, 0.5] (edge-wise and node-wise **Dale**) × σ, and map where topology
controls the manifold geometry computation reads out. Two mirrored panels: memory order
parameter ΔD = `d_eff`(conn) − `d_eff`(ER); generative ΔS = curvature(ER) −
curvature(conn). Sign flips are **stratified** by an edge-importance score (hub
composition held fixed across *f*) to decouple *how much* sign from *where*; placement
is then its own axis (hub-first / periphery-first). Grid: 11 *f* × 16 σ × {connectome,
degree, ER} × 10 seeds × 3 draws × {MC, NARMA, Lorenz}; edge + Dale sign modes; degree +
eigenvector-centrality placement scores. All arms complete. Full working notes:
`PHASE_DIAGRAM_EXPERIMENT.md`.
- **Memory panel.** ΔD is a low-*f*, supercritical wedge, extinguished by *f* ~0.15–0.20;
  below σ~2.4 the connectome is *worse* than ER. The collapse is ER rising to the N=448
  rank ceiling (partly finite-size), not the connectome degrading.
- **Generative panel.** Curvature *un-freezes*: ΔS = 0 at *f*=0 and emerges once *f*>0
  (an onset). The advantage is a *resistance margin* (the connectome stays straight while
  ER collapses to period-2), not an operating optimum (best generation is at *f*=0). The
  effective radius σ_eff = bulk₉₅·σ·⟨1−x²⟩ crossing 1 predicts the onset.
- **Cross-panel dissociation (headline).** The two boundaries run opposite in σ and
  cross near (σ≈4, *f*≈0.12): **memory and generation dissociate**, governed by different
  controllers (memory ← common mode; generation ← σ_eff→1). Sign composition trades
  memory capacity against generative robustness.
- **Dale (biological) arm.** Memory identical to edge (robustness); generation
  broader/stronger. The connectome sustains a faithful straight-attractor Lorenz up to
  **~20% inhibition** then collapses — a **tolerance ceiling, not a tuned optimum** (best
  at *f*=0; collapse σ-dependent) — placing the biological E/I ratio at the upper edge of
  faithful generation.
- **Placement (mechanistic capstone).** Memory is **hub-gated**: on the Dale axis
  hub-first < stratified < periphery-first (degree 0.087/0.124/0.164; eigenvector-centrality
  0.103/0.118/0.219 — effect *larger* under the direct Perron score), ~2× more efficient,
  placement-driven not count-driven. Generation placement is noisy (its controller is
  global), independently corroborating the two-controller dissociation. The edge arm is
  muddy (ER has no hubs to target — the d_eff-ceiling confound), so the clean test is the
  biological node-wise axis.

---

## 7. Key findings to date

**The substrate floor (four-task factorial + human replication).**

1. **Canonical: worse-or-equal; supercritical: most robust.** At sr≈0.95 the connectome
   is worse-or-equal on all four tasks; read curve-vs-curve on the wide sweep it is the
   *most robust* variant (a flat plateau where disk-like nulls peak and collapse).
   Robustness, not a higher ceiling.
2. **That robustness is primarily a weight-SIGN (non-negativity / Perron) effect** — the
   7-condition factorial + one-variable sign control localise it to the
   all-positive-empirical column (MC/NARMA connectome−degree d +8 to +11); signing the
   same weights collapses it. Heavy tail is a secondary task-gated residual; directedness
   minimal, except that non-negativity (which directedness proxied in *C. elegans*) is
   required for closed-loop Lorenz stability. The connectome is never the *best* substrate
   — a directed-signed random disk (Girko) beats it on raw memory — its edge is
   collapse-resistance in an all-positive substrate.
3. **Replicated on a second connectome (human macro-scale).** The human dMRI SC reproduces
   the supercritical MC crossover (d +13→+15, strengthening with resolution) and sustains
   closed-loop Lorenz — external validation across organism, modality, and scale.

**Manifold geometry (Probes 1–3).**

4. **Weight sign gates a supercritical manifold transition:** non-negativity freezes a
   low-dimensional, temporally coherent (Probe 1), spatially low-frequency (Probe 2)
   manifold; balanced sign collapses it to a saturated period-2 state. This is the
   geometric face of the floor's collapse-resistance.
5. **Memory is readout dimensionality, measured by ridge effective rank** (Probe 3):
   `d_eff` orders the MC ladder perfectly (+1.00) and predicts MC within-regime (+0.998);
   PR fails. Spectral origin: the connectome's compact eigenvalue bulk (bulk₉₅ 0.325 vs
   0.48–0.55; = 1/sr_crit). This makes the floor's memory advantage a specific, quantified
   geometric mechanism. (Caveat: the d_eff-over-PR advantage is MC-specific.)
6. **Two computational axes:** memory reads out effective rank; generative (Lorenz)
   prediction reads out trajectory straightness (curvature). `d_eff` ≈ 0 for Lorenz VPT.

**Sign composition (phase diagram).**

7. **Memory ↔ generation dissociation** (the headline): grading sign, the memory and
   generative advantages occupy opposite regions of (*f*, σ) space with opposite
   σ-dependence, governed by different spectral controllers (memory ← hub-localised common
   mode; generation ← global effective radius σ_eff→1). Sign composition is a single knob
   trading memory capacity against generative robustness.
8. **Biological E/I sits at a tolerance ceiling** (Dale arm): the connectome sustains
   faithful straight-attractor Lorenz generation up to ~20% inhibition then collapses — a
   tolerance ceiling, *not* a tuned optimum (best generation at *f*=0; collapse
   σ-dependent).
9. **Memory is hub-gated** (placement): making hub neurons inhibitory collapses the memory
   advantage ~2× faster than peripheral (placement-driven, not count-driven), robust to
   degree vs eigenvector-centrality hub definition — the memory controller is the
   Perron/common mode carried by the hubs. Generation placement is noisy (global
   controller), independently corroborating the dissociation.

**Standing caveats (do not overclaim).** The memory boundary is partly a finite-size
(N=448) rank ceiling (ER catching up) — pending N=1000. The ~20% Dale result is a
*tolerance*, not a tuned optimum. The generative advantage is *robustness of* generation,
not generation quality; climate-error magnitudes are unreliable (ER divergence) — use
bounded curvature. The connectome is *subcritically worse* than ER. Why the connectome's
bulk is anomalously compact (the topology → spectrum link) is not yet derived.

---

## 8. Methodological lessons learned

Caught at specific stages; recorded so future iterations don't repeat them.

- **Binary-vs-continuous weights, symmetric-vs-asymmetric W, and drifting
  self-loops are silent confounds at fixed sr.** Standardise all three; force zero
  diagonal. (v1 → v2a.)
- **Spectral-radius matching ≠ effective-criticality matching** when degree/weight
  distributions differ. A variant's bulk becomes critical at `sr_crit = 1/bulk₉₅`
  (connectome ≈ 3.3 vs nulls ≈ 2.2–2.7), so sweep **wide** and compare curve-vs-curve
  at operating points, never at a single nominal sr. (v2a; the human probe widened to
  `[0,6]` as `sr_crit` rises with N.)
- **Perron–Frobenius compression is the mechanism, not a nuisance.** A non-negative
  matrix concentrates a large isolated eigenvalue over a compressed bulk; all-positive
  *random* nulls collapse into it at criticality, the connectome's compact bulk holds.
  Balanced signs remove the Perron mode and the effect. (v2b → the sign control; recast
  geometrically in Probes 1–3.)
- **A "gaussian vs empirical" weight contrast conflates SIGN with TAIL** (gaussian
  balanced ±, empirical all-positive). Add an explicit sign control (empirical
  magnitudes + balanced random signs) to decouple them — it revealed sign, not tail or
  directedness, as the primary lever.
- **Heavy-tailed raw weights kneecap reservoirs** (a few large edges dominate λ_max);
  sqrt/log mitigates. The tasks use raw synapse counts, so empirical conditions carry
  this caveat.
- **Participation ratio is the wrong dimensionality measure for memory.** It is
  variance-weighted and misses the low-variance directions the ridge readout uses; the
  **ridge effective rank** `d_eff = Σᵢ gᵢ/(gᵢ+α)` is the memory-relevant measure
  (Probe 3). PR remains a valid *shape* descriptor. (Manifold probes.)
- **Random sign-flipping confounds *amount* of sign with *placement*.** Because the
  common mode lives on hubs, a uniform flip lets hub coverage vary with the draw.
  **Stratify** the flip by edge-importance to hold placement fixed, then make placement
  its own axis. (Phase diagram.)
- **Mirror the order-parameter to the phenomenon.** The memory advantage *collapses*
  with *f* (a boundary from above); the generative advantage *emerges* (an onset from
  zero). The boundary operator must match, or the generative panel reads as null.
  (Phase diagram.)
- **Climate-error magnitudes are unreliable when a null diverges** (differences inflate
  as ER blows up); use bounded curvature/straightness as the trustworthy generative
  order parameter.
- **n=10 sweeps predict n=50 direction and zero-crossings** (|Δd|≤0.5); reserve n=50
  for magnitude/significance.
- **BLAS thread limiting must be called *after* numpy import**, or it silently no-ops.
- **The connectome is one fixed graph; nulls are sampled** — inference is "is *this*
  connectome anomalous vs the null distribution?". To isolate weight *placement*,
  **permute** the connectome's exact weights onto its exact topology
  (`connectome_weight_permuted`), don't resample.
- **NMSE vs NRMSE.** Report NRMSE = √(MSE/Var); many RC papers report NMSE, so a
  literature "NARMA-10 ≈ 0.3" is NRMSE ≈ 0.55.

---

## 9. Working conventions

- **Experiments live under `experiments/<connectome>/<task>/`**; generic
  infrastructure under `src/experiment/`; launch with `python -m
  experiments.<connectome>.<task>.run` (`--smoke` for a tiny check).
- **A new task = a `src/tasks/<task>.py` evaluator + a thin task dir.** Do not
  duplicate the runner/stats/plots/substrates; if you think you must edit them,
  reconsider.
- **Analysis tier is additive.** Driven-state capture is opt-in (`collect_states`,
  off by default → committed task runs byte-identical); generic geometry lives in
  `src/analysis/`, connectome-specific drivers in `experiments/<connectome>/analysis/`.
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

## 10. Quick reference

- **C. elegans data:** `data/celegans/cook2019_connectome.xlsx`, sheet "hermaphrodite
  chemical" (SI corrected July 2020). N=300; 3000 undirected / 3669 directed
  off-diagonal edges; 38 self-loops dropped. Reservoir convention `W[i,j]` = j→i. Dale
  signs (`directed_empirical_dale`): `celegans_neurotransmitters.csv` (GABA neurons
  inhibitory; source eLife 95402); only 3.6% of edges → effectively all-positive.
- **Human macro-scale substrate (current primary):** self-built distance-dependent
  group consensus (Betzel 2018 / Suárez 2021) from the `.mat` individual SC, cortical
  **N=448 / N=1000** (cached `data/human/built_consensus/`, gitignored); loaders
  `src/connectomes/human_suarez.py` + `consensus.py`; provenance `data/human/README.md`.
  3 undirected conditions (`human_gaussian` → `human_empirical_signed` →
  `human_empirical`) × the 7-variant ladder × a `[0,6]` sweep × 10 seeds.
- **ada cluster (full runs):** repo `/vol/bitbucket/mmd25/thesis/cognitive-connectomes`,
  venv `.venv`. **CPU-only** (pure numpy/scipy; the node's 2× L40 GPUs are unused);
  128 cores → `--jobs 128` (fork-parallel, bit-identical to sequential). Run in `tmux`,
  rsync results/figures to the laptop, commit from the laptop (committing on ada causes
  pull conflicts). Wall-clock: human MC ~2 min, Lorenz N=448 ~7 min / N=1000 ~90 min.
- **Task matrix (four tasks):** 7 conditions × 7 variants (connectome +
  `connectome_weight_permuted` placement control + 5-rung ladder) × the sweep × n=10.
  Frozen hyperparameters: MC (v1-pinned) `T=3000, warmup=500, max_lag=50, ridge=1e-6,
  input_scaling=1.0, leak=1.0`; NARMA `input_scaling=0.2, leak=1.0`; Mackey-Glass
  `input_scaling=0.5, leak=0.3` (h=84/300); Lorenz `input_scaling=0.1, leak=1.0,
  ridge=1e-7` (closed-loop, 3-channel `Win`, metrics VPT + climate). `sr_crit =
  1/bulk₉₅` locates operating points.
- **Weight-placement control:** `connectome_weight_permuted` — exact topology +
  per-seed permutation of exact weights. `connectome vs control` = placement;
  `control vs degree` = topology.
- **Statistics:** divergence-robust — rank-based permutation test (Holm-corrected) +
  Cliff's delta, capped Cohen's d, median, per-variant divergence rate;
  `metric_divergence_cap` = 2.0 (NRMSE), 10.0 (Lorenz climate), none for VPT/MC.
- **7-condition factorial (C. elegans):** `undirected_{gaussian, empirical_signed,
  empirical}`, `directed_{gaussian, empirical_signed, empirical}`,
  `directed_empirical_dale`. The ladder gaussian → signed-empirical → empirical isolates
  **tail** (gaussian→signed) and **sign** (signed→empirical). Legacy `v2x` labels
  retired (`v2a`=undirected_gaussian, `v2ae`=undirected_empirical,
  `v2ae_randsign`=undirected_empirical_signed, `v2bg`=directed_gaussian,
  `v2b`=directed_empirical, `v2b_randsign`=directed_empirical_signed,
  `v2d`=directed_empirical_dale).
- **Manifold probes (human N=448):** `experiments/human/analysis/manifold/` (`__main__`
  CLI). Metrics in `src/analysis/manifold.py` — `ridge_effective_rank(gram, alpha)` (the
  `d_eff` memory order parameter), `mean_curvature(x)` (straightness),
  `participation_ratio`. States captured via the evaluators' opt-in `collect_states`
  (off by default → committed runs byte-identical). 36,540 state matrices (3 tasks × 3
  conditions × 7 variants × 58 σ × 10 seeds); bit-for-bit validated against the
  committed runs.
- **Phase diagram (human N=448):** `experiments/human/analysis/phase_diagram/`
  (`capture → analyse → plots → eigcheck`). Transform `src/analysis/sign_composition.py`
  — `sign_fraction_matrix` (edge) / `_dale` (node-wise Dale),
  `node_importance(mode="degree"|"eigenvector")`, `stratified`/`hub_first`/
  `periphery_first`, `f=0` = identity. Grid: 11 `f` ∈ [0,0.5] × 16 σ ∈ [0,6] ×
  {connectome, degree, ER} × 10 seeds × 3 draws × {MC, NARMA, Lorenz}; edge + Dale
  modes; degree + eigenvector scores. Order parameters ΔD = `d_eff`(conn)−`d_eff`(ER),
  ΔS = curvature(ER)−curvature(conn); generative predictor `σ_eff = bulk₉₅·σ·⟨1−x²⟩`.

---

## 11. How to use this document in a new conversation

Load this document as the starting context, then state the task. It is the canonical
record of *what is implemented and what has been found*; the **forward plan and open
direction live in `PROJECT_PLAN.md`**. Recommended extra context per task:

- **The substrate floor (four-task factorial):** `PREDICTION_TASKS_INTERPRETATION.md`
  (the reference summary + mechanism across all four tasks); each task's
  `task_config.py` + `results/` + `figures/`.
- **Manifold geometry:** `MANIFOLD_PROBES_IMPLEMENTATION.md` (Probes 1–3 working notes +
  Findings); code in `src/analysis/manifold.py` and `experiments/human/analysis/manifold/`.
- **Sign-composition phase diagram:** `PHASE_DIAGRAM_EXPERIMENT.md` (design + Findings);
  code in `src/analysis/sign_composition.py` and
  `experiments/human/analysis/phase_diagram/`.
- **A substrate/state analysis:** `src/analysis/` + the
  `experiments/<connectome>/analysis/` drivers.
- **The human macro-scale substrate:** `data/human/README.md` (dataset + consensus
  construction) and `experiments/human/`.

The controlled one-variable-at-a-time chain (v1 → v2 → four-task factorial → manifold
probes → phase diagram) is the project's spine; breaking that discipline is the single
failure mode most likely to cost weeks. Hold the line.

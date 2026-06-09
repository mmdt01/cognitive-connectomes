# Cognitive Connectomes — Project Knowledge Base

A research project on connectome-constrained reservoir computing. Uses
empirically measured connectomes as the recurrent matrix of an echo-state
network and asks what biological connectivity contributes beyond
random or degree-matched baselines.

This document is the single canonical reference for the project. It
supersedes earlier PROJECT_HANDOFF.md drafts and is intended to be
loaded into fresh Claude conversations as the starting context.

---

## 1. TL;DR

The central question: does the topology of biological connectomes
 — beyond degree sequence — confer computational properties
that random or degree-matched null graphs do not? Across the
experiments to date the answer is **no at canonical operating points**
(memory capacity at edge-of-chaos) and **yes in the supercritical
regime**, where the connectome maintains higher MC than its
degree-preserving rewire across two structurally different weight
regimes (v2a undirected signed-Gaussian; v2b directed sqrt-empirical),
attributable to higher-order structure (clustering and/or modularity).
The supercritical effect is now established as regime-independent, not
a quirk of any specific weight scheme. As of June 2026 the project has
turned the task axis from passive memory capacity toward dynamical-system
prediction and, as its north star, a connectome-as-JEPA world model.
PROJECT_PLAN.md is now the canonical forward plan (see §9);
IMPLEMENTATION_PHASE0_BRIDGE.md is the
current build (a NARMA-10 prediction bridge across a bounded biological-realism
cross on the *C. elegans* connectome).

---

## 2. Research motivation

Reservoir computing uses a fixed random recurrent matrix as a
computational substrate; readouts are linearly trained. The natural
question for neuroscience-inspired ML is: does a *real* biological
connectome work better than a random matrix as a reservoir? If yes,
which structural features matter? Connectomes are the substrate of
biological cognition; if their topology is computationally meaningful
beyond random or degree-matched baselines, this has implications for
both neural network architecture design and for understanding what
the brain's wiring is doing.

The *C. elegans* connectome (Cook et al. 2019, *Nature* 571:63–71) is
the only complete cell-resolution wiring diagram of a behaving animal.
At N≈300 neurons it's tractable computationally, and its biological
function is partially understood, which makes it the obvious starting
point.

Two literature anchors: Suárez et al. (2021) and Damicelli et al.
(2022) both show connectome-constrained RC outperforming random RC,
primarily through anatomical input/output routing (not just
recurrence). This project takes a more granular approach: build the
controlled topology comparison first (does the recurrence itself
matter?), then progressively add biological features.

---

## 3. Methodological principles

These are load-bearing and non-negotiable.

**Continuous weights everywhere, never binary.** The recurrent matrix
W is always continuous-valued. Binary topology is the *mask*;
continuous values are applied to it via a weight scheme. v1 violated
this and produced an uninterpretable result that took the entire v2
program to clean up.

**One variable at a time.** Each experiment changes exactly one thing
relative to the previous. Multi-variable changes silently confound
attribution. The progression v1 → v2a → v2c → v2b → v2d → … is
explicitly designed around this discipline.

**Null model ladder, not single null.** Comparison against any single
null is uninterpretable. The connectome is compared against a graded
ladder of nulls, each preserving more biological structure than the
last. The connectome "clears" a rung if it outperforms that null
statistically; failing to clear a rung means the preserved feature
is sufficient to explain whatever was tested. See §5.

**Honest null reporting.** Null results are reported plainly. The
project's most defensible finding to date is that the connectome ≈
its degree-preserving rewire on memory capacity across the canonical
ESN range; this is the headline of v2a regardless of which biological
features eventually move the needle.

**Tooling decisions are experimental variables.** BLAS thread
limiting, spectral radius computation method, RNG seed derivation,
weight scheme symmetry — all are decisions that affect results and
are logged explicitly in each experiment's `EXPERIMENT` dict.

**Stage 0 EXPERIMENT dict.** Every notebook starts with a single dict
specifying every methodological choice. Reading the dict tells a
reader exactly what was run. This is the audit trail.

---

## 4. Repository structure

Repo: `~/imperial/thesis/cognitive-connectomes/`. Linux/WSL2;
Python 3.12 venv at `.venv/`; editable-installed via `pyproject.toml`.

```
cognitive-connectomes/
├── PROJECT_KNOWLEDGE_BASE.md       (this document)
├── pyproject.toml
├── data/cook2019_connectome.xlsx   (Cook 2019 SI, corrected July 2020)
├── presentations/
│   └── 01-cognitive-connectomes.ipynb  (v1 — do not modify)
├── src/
│   ├── connectomes/
│   │   └── celegans_cook2019.py    load() with processing modes
│   ├── nulls/
│   │   ├── random_gaussian.py      rung 0
│   │   ├── erdos_renyi.py          rung 1
│   │   ├── degree_rewire.py        rung 2
│   │   ├── clustering_rewire.py    rung 3
│   │   ├── modularity_rewire.py    rung 4
│   │   └── validation.py           validate_null()
│   ├── reservoir/
│   │   ├── blas.py                 threadpool_limits, must import after numpy
│   │   ├── weights.py              apply_weight_scheme()
│   │   └── build.py                rescale_spectral_radius(), build_from_adjacency()
│   ├── tasks/
│   │   └── memory_capacity.py      evaluate() — Jaeger MC
│   └── viz/
│       ├── connectome_overview.py
│       └── results.py              mc_vs_spectral_radius, eigenvalue_spectra, etc.
├── tests/test_smoke.py             tripwire tests (13+/13+ passing)
└── notebooks/
    ├── v2a_continuous_weights/
    │   ├── notebook.ipynb           (v2a + v2c probe in Stages 7/7b)
    │   ├── _run_probe.py            v2a Stage 7 probe runner
    │   ├── _run_probe_v2c.py        v2c rung-3/4 probe runner
    │   ├── probe_supercritical.parquet, probe_v2c.parquet
    │   ├── results.parquet
    │   └── figures/
    └── v2b_directed_weighted/
        ├── notebook.ipynb           (v2b Stages 0-6 + supercritical Stages 7/8)
        ├── _run_probe_v2b.py        v2b Stage 8 supercritical probe runner
        ├── results_sqrt.parquet, results_raw.parquet
        ├── probe_v2b_supercritical.parquet
        └── figures/
```

Note: v2c is implemented as Stages 7b/extension cells within v2a's
notebook directory (sharing the connectome and base infrastructure),
not as a separate notebook folder.

Each notebook directory contains `notebook.ipynb`, `figures/`,
`results.parquet`, and any probe runners (`_run_probe.py`,
`_run_probe_v2c.py`) plus their parquet outputs.

The five null modules all expose the same interface:
`generate(adjacency, seed, **kwargs) -> np.ndarray`. Inputs and
outputs are binary symmetric matrices by default; rung-2 accepts a
`directed=True` kwarg (added in v2b) for directed variants.

`validate_null` supports `preserved_property` values:
`edge_count`, `degree_sequence`, `density`, `clustering`, `modularity`,
`in_degree_sequence`, `out_degree_sequence`.

`apply_weight_scheme` supports `scheme` values:
`symmetric_gaussian` (v2a), `asymmetric_empirical` (v2b).

---

## 5. The null model ladder

Each rung preserves more structure than the last. A null model that
preserves feature X tests whether the connectome's performance depends
on X. If the connectome beats the null, the connectome's structure
beyond X is doing work. If the connectome matches the null, feature X
is sufficient to explain the connectome's performance.

**Rung 0 — Random Gaussian.** Preserves N and approximately the
density. Constructed by independent Bernoulli draws per off-diagonal
pair at the target density.

**Rung 1 — Erdős–Rényi.** Preserves N and exact edge count. Built via
`nx.gnm_random_graph(N, M)`.

**Rung 2 — Degree-preserving rewire.** Preserves N, edge count, and
every node's exact degree. Built via `nx.double_edge_swap` for
`10 × n_edges` accepted swaps.

**Rung 3 — Clustering-preserving rewire.** Preserves degree sequence
*and* the global clustering coefficient (within 5%). Built via
constrained double-edge swap with incremental triangle counting.

**Rung 4 — Modularity-preserving rewire.** Preserves degree sequence
*and* the intra/inter-community edge counts of a fixed Louvain
partition (so Q is preserved exactly). Built by detecting communities
once on the connectome with Louvain (fixed seed), then block-wise
constrained double-edge swap.

Rungs 3 and 4 are parallel, not strictly ordered — they disambiguate
different higher-order features (triangles vs blocks).

---

## 6. Experimental history

### v1 (pre-framework)
*Same connectome, four conditions, MC at three spectral radii.*

- **Result.** Connectome (7.26 ± 0.24) statistically indistinguishable
  from degree_rewire (6.89 ± 0.35) at sr=0.95. Both far below
  random_Gaussian (14.17 ± 0.22).
- **Confounds caught post-hoc.** Three of four conditions used binary
  {0,1} weights; random_Gaussian used continuous Gaussian. Asymmetric
  weights for random_Gaussian (ReservoirPy default), symmetric for
  the other three. Self-loops handled inconsistently across
  conditions. Edge count reported as 3019; actual off-diagonal
  undirected count is 3000.
- **Methodological lesson.** v1 prompted the entire v2 framework
  design: controlled comparisons, unified pipeline, explicit
  Stage 0 EXPERIMENT dict, validation hooks.

### v2a (controlled-comparison foundation)
*Same v1 design, but all four conditions go through the unified
pipeline: binary symmetric mask → symmetric Gaussian weights →
rescale spectral radius.*

- **Result.** Four conditions cluster within ~0.6 MC at sr=0.95
  (connectome 12.01 ± 0.18, degree_rewire 12.14 ± 0.22,
  erdos_renyi 12.58, random_gaussian 12.50). v1's "big gap" was
  entirely the binary-vs-continuous + symmetry + self-loop confound
  stack.
- **Extended sweep (10 spectral radii).** Revealed the
  **spectral-shift effect**: narrow-degree conditions peak at sr ≈
  0.95–1.00; broad-degree (connectome, degree_rewire) peak at sr ≈
  1.10–1.25. All four reach the same peak MC at their own optimum.
  Eigenvalue spectrum diagnostic confirmed the depressed-bulk
  mechanism: hub-driven outlier eigenvalues compress the bulk below
  λ_max in broad-degree topologies.
- **Stage 7 probe (n=50, sr ∈ {1.25, 1.50, 1.75}).** Found the first
  real signal: connectome maintains higher MC than degree_rewire in
  the supercritical regime. Cohen's d = 0.64, 1.02, 1.47.
  Monotonically growing with sr. Suggests higher-order structure
  buys dynamical stability under supercritical perturbation.

### v2c (rung-3/4 disambiguation)
*Added clustering_rewire and modularity_rewire; reran the Stage 7
probe with all four supercritical comparisons.*

- **Pre-flight check.** Connectome's clustering 2.11× the rung-2
  rewire's; modularity Q +0.42 above rung-2. Both features
  meaningfully elevated.
- **Result.** Rung-2 (degree_rewire) shows the gap as before
  (d=0.64→1.02→1.47). Rungs 3 and 4 both close it (all p_holm > 0.05
  except clustering_rewire at sr=1.75 with d=0.37).
- **Mechanistic ambiguity.** modularity_rewire implicitly retains
  ~half the connectome's excess clustering without explicit
  constraint (T=0.175 vs degree_rewire's 0.115); clustering_rewire
  does *not* implicitly retain modularity (Q ≈ 0). The two features
  are confounded on this connectome.
- **What this rules out cleanly.** The degree-only mechanism for the
  supercritical gap is definitively ruled out. Either clustering or
  modularity (or both, additively) is sufficient to close the gap;
  disambiguating further requires a dual-constraint null or a
  decoupled block model.

### v2b (directed + empirical weights — complete)
*Directed binary topology with weights sampled from Cook 2019's
empirical weight distribution. Rungs 0–2 only. Both `sqrt` and
`raw` weight transformations tested; sr extended to include 1.75.*

- **Canonical-sr result (sr=0.95).** All four conditions cluster
  ~9.1–11.0; connectome 9.09 ± 0.37, degree_rewire 9.30 ± 0.56 (gap
  within seed noise). Consistent with v2a's canonical-sr null at the
  same operating point.
- **Magnitude shift v2a → v2b.** Universal ~20% MC reduction across
  all conditions, attributable to Perron–Frobenius compression: all-
  positive weight matrices have a real positive λ_max but compressed
  spectrum bulk after rescaling.
- **Supercritical probe (Stage 8, n=50, sr ∈ {1.25, 1.50, 1.75},
  both transforms).** The connectome–degree_rewire Cohen's d rises
  monotonically with sr and crosses zero in the supercritical range,
  in both transforms. v2b sqrt at sr=1.50 yields **d=+1.04**, matching
  v2c's d=+1.02 to two significant figures despite v2b being a
  structurally different reservoir regime (directed asymmetric all-
  positive vs undirected signed-Gaussian). All p_holm < 0.0001.
- **Transformation choice controls *where*, not *whether*.** sqrt
  crossover lies between sr=1.25 and 1.50; raw crossover lies between
  1.50 and 1.75 (one sweep step later). Raw regime sub-crossover d
  values are more negative (d=−8.44 at sr=1.25) reflecting stronger
  PF compression. Interpretation: connectome's weight-degree coupling
  produces sharper Perron eigenvalue separation in raw, requiring
  higher nominal sr to escape, but eventually becoming advantageous
  in supercritical where degree_rewire's near-critical bulk
  destabilises.
- **Stage 7 (n=10 from existing data) predicted Stage 8 (n=50)
  faithfully.** d-values changed by ≤0.5 in any cell; direction and
  zero-crossing locations carried over exactly. Methodological note
  for future probes: n=10 sweep data is sufficient for direction-of-
  trend calibration; n=50 is needed only for magnitude pinning and
  significance.
- **What v2b establishes.** The supercritical higher-order-structure
  effect from v2c is regime-independent — it survives the transition
  from undirected signed-Gaussian to directed all-positive empirical
  weighting. The transformation choice modulates the operating
  regime's location but not the underlying topological signal.

---

## 7. Key findings to date

1. **Degree sequence is sufficient to explain MC at canonical sr.**
   The connectome's memory capacity at edge-of-chaos is reproduced
   by any null model that preserves N and degree sequence, across
   both undirected signed-Gaussian (v2a) and directed empirical
   (v2b) weight regimes.

2. **Higher-order structure matters in the supercritical regime.**
   The connectome maintains higher MC than degree_rewire at
   supercritical sr (v2a Stage 7: d=0.64→1.47 across sr ∈ {1.25,
   1.50, 1.75}). v2c attributes this to clustering and/or
   modularity; degree-only mechanism ruled out.

3. **The supercritical effect is regime-independent.** v2b's directed
   all-positive empirical-weighted reservoir reproduces v2c's
   d=+1.02 at sr=1.50 to two significant figures (v2b sqrt d=+1.04)
   despite structurally different dynamics. The effect is a property
   of the connectome's higher-order topology, not of any specific
   weight scheme. Weight-distribution choice (sqrt vs raw) shifts
   *where* in sr-space the crossover appears (sqrt: between 1.25 and
   1.50; raw: between 1.50 and 1.75) but not whether it appears.

4. **Spectral-radius matching is a cross-condition confound when
   degree distributions differ.** Different degree distributions
   produce different effective bulk criticalities at the same nominal
   sr. Fair comparison requires either sweeping sr or controlling on
   bulk spectral measure. Generalisable methodological contribution
   beyond the connectome question itself.

5. **Perron–Frobenius compression shifts crossover location, does
   not eliminate the supercritical effect.** v2b's ~20% MC reduction
   at canonical sr vs v2a is attributable to PF compression of all-
   positive weight matrices. Originally hypothesised to potentially
   wash out the v2c effect; v2b directly disproves this — the effect
   re-emerges at slightly higher nominal sr instead. Sign assignment
   remains the highest-yield next biological feature to test, but
   the prior is now that MC magnitudes will recover toward v2a levels
   while preserving the regime-independent supercritical signal.

---

## 8. Methodological lessons learned

Each was caught at a specific stage; documented here so future
iterations don't reproduce them.

- **Binary-vs-continuous weights at the same spectral radius is a
  silent confound.** ρ-rescaling fixes the largest eigenvalue but
  not the distribution of weights. Continuous weights produce richer
  state diversity than binary at the same ρ. (v1 → v2a fix.)

- **Symmetric vs asymmetric W on the same topology is a silent
  confound.** v1's `random_gaussian` was incidentally asymmetric
  (ReservoirPy default), the other three v1 conditions symmetric.
  Standardise weight symmetry across all conditions in any
  comparison. (v1 → v2a fix.)

- **Self-loops drift across null implementations unless explicitly
  forced to zero everywhere.** `nx.double_edge_swap` preserves
  self-loops as invariants; some null generators zero diagonals,
  others don't. Force `np.all(np.diag(M) == 0)` as an explicit
  cross-condition check. (Discovered during v2a; caught 38 silent
  self-synapses inherited from Cook 2019 that v1 had silently
  retained for some conditions but not others.)

- **Spectral radius matching ≠ effective criticality matching when
  degree distributions differ.** Broad-degree topologies have a
  depressed bulk relative to λ_max; their effective bulk criticality
  sits at nominal sr > 1. Fixed-sr comparisons systematically
  understate broad-degree conditions. (Discovered in v2a extended
  sweep; confirmed via eigenvalue diagnostic.)

- **Perron–Frobenius compression in all-positive weight matrices
  shifts the effective dynamical regime upward in sr-space.**
  Affects every all-positive weighted reservoir; lowers MC at
  canonical sr but does not eliminate topology-dependent effects —
  v2b confirmed the v2c supercritical effect re-emerges at slightly
  higher nominal sr instead of vanishing. Sign assignment (E/I
  balance) would mitigate the compression. (Discovered in v2b
  initial, characterised in v2b Stage 8.)

- **n=10 effect-size sweeps reliably predict n=50 probe outcomes
  for direction and zero-crossing location.** v2b Stage 7 (n=10
  analysis from existing sweep) predicted Stage 8 (n=50 probe) to
  within |Δd| ≤ 0.5 in every cell; zero-crossing locations carried
  over exactly. Magnitude refinement and significance require n=50,
  but the cheap n=10 analysis is sufficient for deciding whether a
  probe is warranted. (Validated in v2b.)

- **Dual-transform comparisons surface mechanism that single-
  transform analyses miss.** v2b's parallel sqrt/raw runs revealed
  that transformation choice controls *where* in sr-space a
  topology effect appears, not *whether* it appears. Running both
  transforms doubled compute cost but produced the regime-shift
  interpretation directly. Worth considering for any future
  transformation choice. (Discovered in v2b.)

- **BLAS thread limiting must be called AFTER numpy import**, or it
  silently does nothing (no BLAS library loaded yet to constrain).
  Force-import numpy in any `blas.py` setup module. (Discovered
  during v2a implementation, cost ~17 minutes of confused debugging.)

- **Heavy-tailed weight distributions silently kneecap reservoir
  experiments.** A handful of large edges dominate the spectral
  radius after rescaling; rest of the network is effectively silent.
  Mitigate via sqrt or log transformation before rescaling, applied
  uniformly to all conditions (including the empirical pool used for
  null sampling). (Caught in v2b planning, applied in v2b
  implementation.)

- **Asymmetric mask sampling between conditions.** The connectome is
  one fixed graph; null models are sampled across seeds. The
  connectome's seed dispersion reflects weight noise only; null
  dispersions reflect mask + weight noise. Inferentially this means
  "is *this* connectome anomalous vs the null distribution?", not
  "are connectomes-in-general anomalous." Acknowledged in v2b prose;
  not yet addressed methodologically.

---

## 9. Next iteration roadmap

All forward planning lives in `PROJECT_PLAN.md`: the thirteen-week schedule,
the Stage A scale-row and realism-cross design, the decision gates, the
conference targets, and the task progression (NARMA-10, then Mackey-Glass,
then Lorenz, toward the connectome-as-JEPA world model). The current build is
detailed in `IMPLEMENTATION_PHASE0_BRIDGE.md`. This section is intentionally a
pointer, so that next steps and roadmap ideas are organised in one place rather
than spread across documents.

---

## 10. Open methodological questions

- **Asymmetric mask sampling between connectome and nulls.** Connectome
  is fixed; nulls are sampled. Inferential consequences are minor at
  current effect sizes but become relevant if a v2d+ result is near
  the significance boundary.

- **Log weight transformation in v2b.** sqrt and raw were tested in
  Stage 8 (both reproduce the supercritical effect). log was not. A
  third transform column would be a quick addition via the existing
  `TRANSFORM_TAG` toggle; useful for triangulating where in
  transform-space the canonical-sr null collapses.

- **Clustering vs modularity disambiguation from v2c.** Requires a
  dual-constraint null (preserve both T and Q) or a block model
  decoupling them. Open whether this is worth the implementation
  effort. v2b-ext will test whether the same ambiguity persists in
  the directed regime, which informs whether the dual-constraint
  null is methodologically warranted.

- **Reservoir convention orientation for v2b's directed loader.**
  Verified directly against the Cook 2019 spreadsheet, but downstream
  null modules' behaviour on transposed matrices should be sanity-
  checked if any new directed analyses are done.

---

## 11. Working conventions

For implementing or reasoning about the project.

- **Variable names: full and readable.** `spectral_radius`, not `sr`,
  in code. `sr` is acceptable only in axis labels and conventional
  shorthand.
- **One Stage 0 EXPERIMENT dict per notebook.** Audit trail.
- **Validation runs inside notebooks, not as separate test scripts.**
  Validation belongs with the experiment, not in a side tool.
- **Save figures at 300 dpi to `figures/` subdirectory of each
  notebook.**
- **`results.parquet` for tabular outputs.** Pandas-readable, lossless.
- **Implementation plans before Claude Code prompts.** Multi-step
  implementations get a planning document (`V2{x}_IMPLEMENTATION_PLAN.md`
  pattern) and a focused Claude Code prompt (`V2{x}_PROMPT.md`)
  separately.
- **Push back on disagreements; honest reads beat positive spin.**
  Null results are reported plainly; effect-size + significance
  reported together; confounds surfaced explicitly even if they
  weaken the headline.

---

## 12. Quick reference

- **Repo:** `~/imperial/thesis/cognitive-connectomes/`
- **Connectome data:** `data/cook2019_connectome.xlsx`, sheet
  "hermaphrodite chemical"; SI version corrected July 2020.
- **MC hyperparameters (pinned from v1):** `T=3000`, `warmup=500`,
  `max_lag=50`, `ridge_alpha=1e-6`, `leak_rate=1.0`,
  `input_scaling=1.0`, `n_seeds=10`, BLAS threads = 2.
- **Standard spectral radius sweep:**
  `[0.5, 0.7, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.25, 1.5, 1.75]`.
  (sr=1.75 added during v2b extension; for direct v2a comparability
  on canonical-sr questions, slice to the first 10 values.)
- **Probe convention:** higher-n (n=50) at sr ∈ {1.25, 1.50, 1.75}
  for supercritical follow-ups; 10,000-permutation two-sided tests
  with Holm correction when comparing multiple conditions.
- **Reservoir convention:** `W[i, j]` is the weight from node `j` to
  node `i`. v2b's loader transposes Cook 2019's natural
  `[presynaptic, postsynaptic]` layout into this convention.
- **Self-loops:** zeroed universally (Cook 2019's 38 autaptic
  self-synapses excluded).

---

## 13. How to use this document in a new Claude conversation

Paste this document as the first message of a new conversation, then
state what you want to do. Recommended additional context per task:

- **For continuing an experiment:** also load that notebook's
  `results.parquet` and the relevant code modules.
- **For drafting a new experiment:** this document is sufficient;
  Claude will draft an implementation plan and Claude Code prompt
  in the established pattern.
- **For analysing a result:** load the relevant parquet and figure
  paths; Claude can interpret without needing the full notebook.
- **For forward planning, Phase 0 onward:** also load `PROJECT_PLAN.md` (the
  canonical thirteen-week plan) and `IMPLEMENTATION_PHASE0_BRIDGE.md` (the
  current build); the forward plan lives there (see §9).

The progression v1 → v2a → v2c → v2b → v2d+ is a controlled chain;
breaking the one-variable-at-a-time discipline is the single failure
mode most likely to cost weeks of work to clean up. Hold the line.

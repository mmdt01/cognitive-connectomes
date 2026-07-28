# Manifold Probes 1 to 3: Implementation Plan

*Task specification for implementing the first three manifold-geometry probes in
the `cognitive-connectomes` repository. This is the operational "how".
`PROJECT_KNOWLEDGE_BASE.md` is the canonical reference for repository structure,
conventions, the null ladder, the seven-condition factorial, the spectral-radius
sweep, and the pinned hyperparameters. This
document is self-contained: it does not depend on any external proposal. Complete
the `Findings` block under each probe as results arrive.*

---

## 0. Scope and order of execution

**Substrate order (do not deviate without discussion).**

1. **Human connectome, N=448 first.** All of Probes 1 to 3 are implemented,
   debugged, and interpreted on the human N=448 substrate before anything else.
   It is the cleanest starting point: undirected and normal (so eigenvector
   bases are well defined without the non-normal complications of a directed
   matrix), macro-scale, and it already reproduces the supercritical
   collapse-resistance crossover, so the geometry has something to explain.
2. **Human N=1000** next, as a strict scale extension (same code, `--scale 1000`,
   the wider `[0,6]` sweep).
3. **C. elegans** last, where the directed non-normal matrix needs the extra
   handling flagged in Probe 2.

**Experimental matrix per substrate (reuse the existing runs, do not re-tune).**
Conditions and variants exactly as the four-task floor: the connectome, the
`connectome_weight_permuted` placement control, the five-rung null ladder, and
the seven-condition sign-by-tail-by-topology factorial (for human, the
undirected sub-factorial: `human_gaussian`, `human_empirical_signed`,
`human_empirical`). The existing spectral-radius sweep (human uses the `[0,6]`
grid), n=10 seeds. Tasks that have results for human N=448: memory capacity,
NARMA-10, and Lorenz (Mackey-Glass infrastructure exists but has not been run;
skip it until it has).

**Discipline (carried from the floor, non-negotiable).**

- Reservoir as control: nothing is trained in Probes 1 to 3. The recurrent matrix
  stays frozen and the readout is not involved in these probes at all (they
  operate on reservoir states, not on task predictions).
- Do not modify frozen hyperparameters or the run matrix. State capture is
  additive and opt-in.
- One variable at a time; reuse the runner, substrates, null ladder, and sweep.
- Honest null reporting: a negative result (for example, the manifold does not
  align with connectome harmonics) is reported plainly and is informative.

**Conventions.** New generic analysis lands in the `src/analysis/` tier
(connectome-agnostic), alongside `spectral.py`, with a connectome-specific driver
under `experiments/human/analysis/`. British spelling; no em or en dashes;
guarded string-replacement edits with assertion checks; read source files before
editing; smoke-test (`--smoke`) before any full run; figures at 300 dpi to the
driver's `figures/`; `results/*.parquet` gitignored.

---

## 1. I/O routing decision (read before implementing)

**Use the existing all-node input and full-node readout convention: a dense
random `Win` that injects the task input into every node, and reservoir states
read from all N nodes.** Do not use anatomically selected input or output nodes
for Probes 1 to 3. First confirm this matches what the existing task configs
actually use (check each `task_config.py` / the `Win` construction); if any task
already uses a restricted `Win`, stop and flag it, because Probe 3 depends on the
routing matching the runs that produced the performance results.

Rationale, and why it matters for these specific metrics:

- **Isolates topology.** All-node injection does not privilege any anatomical
  location, so the emergent manifold reflects how the recurrent topology reshapes
  an unstructured drive. That is exactly the "what does topology do to the
  manifold" question these probes ask.
- **Avoids an input-rank confound in the dimensionality metric.** Injecting into
  only a few nodes is a low-rank drive, and the dimensionality of a driven
  response is bounded by the rank of the input. Localised injection would
  therefore compress the participation ratio for reasons that are about the input,
  not the topology, contaminating the headline metric. A high-rank (all-node)
  drive lets the recurrent structure set the dimensionality.
- **Keeps Probe 3 valid.** Probe 3 correlates manifold geometry against the
  existing task-performance curves. The geometry must be measured under the same
  driving that produced those curves, or the correlation is meaningless.

Anatomically-informed routing (for example subcortical or sensory input regions,
intrinsic-network readout) is deliberately deferred to a separate variable and
belongs with the existing `HUMAN_IO_ROUTING_PLAN.md` thread. When introduced
later it becomes its own clean one-variable question, and a geometric one: does
anatomical routing reshape the manifold in a topology-dependent way (that is,
more for the connectome than for a degree-matched null)? That directly re-frames
the Suarez / Damicelli routing advantage in manifold terms and is a strong
candidate follow-up, but it must not be entangled with the intrinsic-geometry
baseline established here.

---

## 2. Step 0: reservoir state capture (the one dependency)

The probes operate on the driven reservoir state matrix. First determine whether
the task evaluators already expose it.

- Inspect the evaluators (`src/tasks/memory_capacity.py`, `narma.py`,
  `mackey_glass.py`, `lorenz.py`) and the generic runner for an existing
  `return_states` path or any hook that surfaces the collected state matrix.
- If one exists, target it. If not, add a minimal opt-in flag (for example
  `collect_states=False`) threaded from the run config through the evaluator, that
  returns the post-warmup driven state matrix without altering the default
  code path, the frozen hyperparameters, or the run matrix. Default off.

**What to capture.** For each (condition/variant, spectral radius, task, seed):
the driven reservoir state matrix `states` of shape `(T_effective, N)`, warmup
discarded (use the task's existing warmup count). For memory capacity and the
driven tasks this is the response to the standard task input. Persist to a
gitignored parquet keyed by `(substrate, scale, condition, variant, task,
spectral_radius, seed)` so the three probes and the join in Probe 3 can all read
it without re-running reservoirs.

**Cost note.** State matrices are large. Capture once, cache, and read from the
cache in all three probes. For human N=1000 confirm `T_effective > N` so the
state covariance is full rank (memory capacity `T=3000` satisfies this at both
scales); if any task has `T_effective <= N`, note it, since the participation
ratio is then bounded by `T_effective` rather than by the geometry.

---

## 3. Analysis module: `src/analysis/manifold.py`

A new generic, connectome-agnostic module (sibling to `spectral.py`). Pure
numpy/scipy, no task or connectome specifics. Suggested functions and exact
definitions:

**Preprocessing.** Centre the state matrix over time (subtract the per-column
mean) before any covariance. Let `X` be the centred `(T, N)` matrix and
`C = (X.T @ X) / (T - 1)` its `(N, N)` covariance. Obtain covariance eigenvalues
with a symmetric solver (`scipy.linalg.eigvalsh`); clip tiny negative eigenvalues
(numerical noise) to zero.

- `participation_ratio(states) -> float`
  With covariance eigenvalues `lambda_i >= 0`:
  `PR = (sum lambda_i)^2 / sum(lambda_i^2)`. Spatial effective dimensionality.
  Optionally also return `PR / N`.

- `spectral_entropy(states, normalise=True) -> float`
  With `p_i = lambda_i / sum_j lambda_j`:
  `H = - sum_i p_i * log(p_i)` (define `0 * log 0 = 0`). If `normalise`, divide by
  `log(rank)` so `H` lands in `[0, 1]`. Sits on the same spatial axis as PR but
  weights the tail differently; included because heavy-tailed empirical weights
  can make PR under-report a long low-variance tail. PR and H diverging is itself
  a signal the tail is reshaping the geometry.

- `mean_curvature(states, min_speed=1e-8) -> float`
  Velocities `v_t = x_{t+1} - x_t`. Turning angle
  `c_t = arccos( clip( (v_t . v_{t+1}) / (||v_t|| ||v_{t+1}||), -1, 1 ) )`.
  Skip any step where `||v_t|| < min_speed` or `||v_{t+1}|| < min_speed`. Return
  the mean of `c_t`. Temporal predictability: lower means straighter means more
  linearly extrapolable. This is the straightening measure and the bridge to the
  prediction thread. Report in radians.

- `manifold_metrics(states) -> dict`
  Convenience wrapper returning `{pr, pr_norm, spectral_entropy, mean_curvature}`
  in one pass over the covariance/trajectory.

- `basis_alignment(states, basis, k_grid) -> dict` (for Probe 2)
  Given a centred `X` and an orthonormal `basis` (`N x N`, columns ordered as
  intended, for example Laplacian eigenvectors by ascending frequency), for each
  `k` in `k_grid` compute the fraction of total state variance captured by the
  top-k basis vectors: with `U_k` the first `k` columns,
  `captured(k) = trace(U_k.T @ C @ U_k) / trace(C)`. Return the curve over
  `k_grid`. Provide a random-basis baseline: average `captured(k)` over several
  random orthonormal bases (QR of a Gaussian matrix), returning mean and a spread
  band.

Optional (held in reserve, do not implement yet unless asked): temporal spectral
flatness (Wiener entropy of the per-channel power spectrum) for an explicit
frequency-domain regime read.

Report robustly across seeds, consistent with the existing stats tier: median and
interquartile range across the n=10 seeds, and for connectome-versus-null
contrasts reuse the rank-based permutation test in `src/experiment/stats.py`
(Cliff's delta) rather than assuming normality.

---

## 4. Probe 1: manifold dimensionality and shape

**Driver.** `experiments/human/analysis/manifold.py` (new), launched as
`python -m experiments.human.analysis.manifold --scale 448` with a `--smoke`
path. Reads the cached state matrices, calls `manifold_metrics` for every
(condition/variant, spectral radius, task, seed), writes a tidy
`results/scale_448/manifold_metrics.parquet`.

**Figures** (to the driver's `figures/`, 300 dpi):

- The headline plot: participation ratio versus spectral radius, one line per
  condition/variant, per task. The prediction is a connectome plateau where the
  disk-like nulls rise and then collapse toward `PR -> 1`.
- Mean curvature versus spectral radius, same layout.
- Spectral entropy versus spectral radius, same layout.

**Interpretation to record.** Does the connectome hold effective dimensionality
across the supercritical regime where nulls collapse? Does curvature distinguish
a collapsed line (low PR, low curvature) from a genuinely straightened
high-dimensional trajectory (high PR, low curvature)? Do PR and entropy agree, or
does the heavy-tailed `empirical` column split them?

**Findings.** *(human N=448)*

*Run.* Full `[0, 6]` sweep (58 sr) x 7 variants x 3 conditions x 10 seeds x
{MC, NARMA-10, Lorenz teacher-forced} = 36,540 rows
(`results/scale_448/manifold_metrics.parquet`). Captured states reproduce the
committed four-task runs **bit-for-bit** (max relative difference 0.0 across all
12,180 rows per task), so this is the identical reservoir set the floor measured.
`sr_crit` (= 1/bulk95): gaussian 1.25, empirical_signed 2.49, empirical 3.08.

*Headline: weight SIGN gates a supercritical geometric transition.* The
pre-registered prediction (connectome holds a high-PR plateau while nulls collapse
to `PR -> 1`) is wrong. What happens is set by weight sign, and it is cleanest in
curvature. In the balanced-sign conditions (`gaussian`, and the one-variable
`empirical_signed` control) the manifold undergoes a supercritical transition as sr
crosses ~1; in the all-positive `empirical` condition it is **frozen** across the
entire sweep. Signing the connectome's own weights (`empirical` -> `empirical_signed`,
sign only) restores the transition. This is the manifold face of the sign-primary /
Perron account: non-negativity holds activity on a low-dimensional, temporally
coherent manifold that resists the supercritical disordering the balanced-sign
substrates undergo.

*The geometry occupies three discrete states (curvature is trimodal).* Mean turning
angle takes essentially three values across all 36,540 rows, with almost nothing
between 0.5 and 2.0 rad:

- **~0.25 rad (empirical Lorenz):** a smooth, near-straight, genuinely straightened
  low-D trajectory (Henaff/Simoncelli), the geometric basis of closed-loop stability.
- **~2.09 rad (empirical MC / NARMA):** the analytic signature of a quasi-static map
  of white-noise input. For a memoryless map of white noise consecutive state
  increments anti-correlate at -0.5, giving a mean turning angle of 2*pi/3 = 2.094
  rad; the frozen empirical values sit exactly here, and the sr = 0 row (`W = 0`, no
  recurrence) gives the same 2.10 rad, confirming the reading. The frozen non-negative
  reservoir behaves as a near-static input map.
- **~pi rad (balanced-sign supercritical):** consecutive velocities anti-parallel on
  a collapsed (`PR -> 1`) line, i.e. a saturated **period-2 flip-flop**. This is a
  highly *ordered* saturation state, NOT a random walk (a random walk gives
  pi/2 = 1.571 rad; no rows sit there). Earlier "disordered / random-walk"
  descriptions are corrected by this.

*Dimensionality: PR is the wrong instrument here (resolved in Probe 3).* Within the
frozen empirical column the connectome holds a rank-consistent PR margin over the
degree null (Cliff's delta +1.00 MC/NARMA per seed), but the absolute PR gap is tiny
(~1.4 vs ~1.2) because PR is variance-weighted and the memory lives in low-variance
directions it cannot see. The real dimensionality effect is large and only becomes
visible through the ridge effective rank (Probe 3 rebuild). Read Probe 1 PR as a
manifold *shape* descriptor, not the memory measure.

*PR vs entropy.* They agree (both compressed in `empirical`, both inflate-then-decline
in `gaussian`); no heavy-tail-driven PR/entropy split at N=448 (revisit at N=1000,
where the tail is heavier).

*Two axes carried forward.* Curvature freezing is the sign-gated generative / stability
axis; effective dimensionality is the memory axis, measured properly by `d_eff` in
Probe 3.

---

## 5. Probe 2: manifold alignment with structural modes

**Bases to compare, per substrate/condition** (all orthonormal so projections are
well defined):

- **Connectome harmonics.** Eigenvectors of the unnormalised graph Laplacian
  `L = D - A` of the substrate, sorted by ascending eigenvalue (low spatial
  frequency first). For the human undirected substrate `L` is symmetric, use
  `eigh`. Decide and record whether `A` is the binary mask or the weighted matrix;
  start with the weighted symmetric connectivity that actually defines the
  reservoir, and optionally also compute the binary-mask variant.
- **`W` modes.** For undirected human, `W` is symmetric, use `eigh` for an
  orthonormal eigenbasis. (For directed C. elegans later, `W` is non-normal and
  its right eigenvectors are not orthonormal; use an orthonormal surrogate then,
  either the eigenvectors of the symmetric part `(W + W.T) / 2` or the left
  singular vectors of `W`. Record the choice. This is why human goes first.)
- **Random baseline.** Several random orthonormal bases, averaged.

**Driver work.** Extend the same driver with a Probe 2 mode. For each
condition/variant at each spectral radius, call `basis_alignment` for the three
bases over a shared `k_grid`, write `results/scale_448/manifold_alignment.parquet`.

**Figure.** Cumulative variance captured versus `k`, three curves (harmonics, `W`
modes, random) with the random band shaded, faceted by condition and spectral
radius (or a representative operating point).

**Interpretation to record.** Does the activity manifold live in the
low-frequency connectome-harmonic subspace, in the `W`-mode subspace, or neither?
This tests, as a measurement, the assumption that harmonics are the natural basis.
A likely and still-useful outcome is that the manifold aligns with the leading
`W` modes rather than the low-frequency harmonics, which would cleanly rule out
the harmonic-basis direction before any effort is spent on it.

**Findings.** *(human N=448)*

*Run.* `connectome` + `degree_rewire` null x 3 conditions x 10 seeds x
{MC, NARMA-10, Lorenz} at each condition's canonical (~0.95) and supercritical
(`sr_crit`) operating point; captured state variance vs top-k for three orthonormal
bases, low-frequency graph-Laplacian **harmonics** (of |W|), dominant **W-eigenmodes**,
and a **random** band (`manifold_alignment.parquet`, 15,120 rows). States time-centred.

*Headline: weight SIGN selects which structural basis the manifold occupies.* The
pre-registered prediction (manifold aligns with leading W-modes, not harmonics) holds
only under balanced sign and inverts under non-negativity. Balanced sign (`gaussian`,
`empirical_signed`): activity lives in the dominant W-eigenmodes (top-10 capture up to
0.89 for NARMA gaussian; MC is broadband so spread even here). All-positive `empirical`:
the ordering inverts, low-frequency connectome harmonics beat W-modes and chance across
the whole k-range, bridging to connectome-harmonic decomposition of cortical activity
(Atasoy).

*Mechanism (confirmed).* For a non-negative W the dominant eigenmode is the all-positive
**Perron / DC mode**, which carries the mean and is removed by time-centring (top W-mode
fluctuation variance ~0.000 for every empirical task, vs 0.17-0.18 for balanced-sign
NARMA / Lorenz, whose top mode is a genuine oscillatory mode). With the Perron direction
centred out, the residual fluctuation manifold falls on the smooth low-frequency
harmonics.

*Sign effect, not connectome topology.* The all-positive `degree_rewire` null shows the
same inversion (and in MC/NARMA aligns with harmonics slightly *more* than the
connectome). So "activity lives in the harmonic basis" is a property of the non-negative
regime generically; the connectome's slightly lower harmonic concentration is consistent
with its slightly higher effective dimensionality.

*Scope.* Only the balanced-sign + W-mode case is a *sharp* alignment (up to 0.89). In
the empirical column variance is spread across many low-frequency harmonics (above chance
throughout but not concentrated in a few), so the harmonic-basis direction is
*conditionally* true (real under non-negativity, absent under balanced sign) rather than
cleanly ruled out. Combined with Probe 1: the non-negative manifold is low-D and
temporally smooth (Probe 1) and spatially low-frequency (Probe 2), all sign-driven.

---

## 6. Probe 3: geometry to performance link

**Join.** Load the existing human N=448 performance results
(`experiments/human/human_mc/results/...`, `human_narma10/...`,
`human_lorenz/...`) and inner-join to `manifold_metrics.parquet` on
`(condition, variant, spectral_radius, seed)`. Metrics on the performance side:
memory capacity, NARMA-10 NRMSE, Lorenz VPT and climate error (and the Lorenz
divergence rate per variant).

**Analyses.**

- Correlate `{pr, mean_curvature, spectral_entropy}` against each performance
  metric, both across the sweep and at each variant's operating point
  (`sr_crit = 1 / bulk95_ratio`, already computed in the spectral analysis tier).
- The targeted question: at the spectral radii where the connectome shows its
  robustness plateau, is its PR higher (and/or curvature lower) than the
  collapsing nulls, and does that geometric gap track the performance gap across
  conditions?

**Figures.** Geometry-versus-performance scatters coloured by condition; and the
overlay that tells the story, `PR(sr)` and the performance curve on shared axes
for the connectome versus a representative collapsing null.

**Interpretation to record.** Is there a geometric signature that predicts where
each substrate wins? Does collapse-resistance in performance coincide with
preserved dimensionality (and/or straightened trajectories) in geometry? This is
what converts the existing performance curves into a mechanistic, geometric
account, and it is the result that stands on its own for the workshop even if
Probes 4 and 5 are never run.

**Findings.** *(human N=448)*

*Setup.* No new reservoir runs; geometry and the co-recorded, bit-exact performance
metrics are joined by construction. Spearman rank correlations, supercritical
(sr >= `sr_crit`), pooled and per condition.

*Motivation (PR-based first pass, superseded).* With PR as the dimensionality metric
the geometry-to-performance link was weak and largely BETWEEN-regime: pooled
MC <- PR +0.41, Lorenz VPT <- curvature -0.84, NARMA <- curvature -0.39, but within the
frozen empirical column these mostly vanish (curvature has no variance there). Sign sets
both the geometry and the outcome, so PR-geometry read as a between-regime readout of the
sign mechanism rather than a within-regime predictor. This motivated a rebuild around a
readout-relevant dimensionality measure.

*Rebuild: memory capacity <- RIDGE EFFECTIVE RANK (the headline).* The right measure is
`d_eff = sum_i g_i / (g_i + alpha)` over the design-Gram eigenvalues `g_i` with each
task's own `alpha`, i.e. the effective degrees of freedom of the ridge solution (trace of
the hat matrix; Hastie & Tibshirani). `src/analysis/manifold.py::ridge_effective_rank`;
rebuild in `probe3.run_deff` (reads `covariance_spectra.parquet` + `manifold_metrics.parquet`;
writes `probe3_deff.parquet` + figures; no reservoir runs). Validation gate: PR recomputed
from `eig_cov` reproduces the published PR to 1.4e-8.

| analysis | task | d_eff r_s | PR r_s | n |
|---|---|---|---|---|
| (a) ladder ordering (median/variant, 7 rungs) | MC | **+1.00** | +0.11 | 7 |
| (a) ladder ordering (median/variant, 7 rungs) | NARMA | -0.96 | -1.00 | 7 |
| (b) within-regime (var/sr/seed pooled) | MC | **+0.998** | +0.31 | 350 |
| (b) within-regime (var/sr/seed pooled) | NARMA | -0.71 | -0.74 | 350 |
| (c) task-axis, within-empirical | Lorenz VPT | +0.03 | curv -0.04 | 350 |
| (c) task-axis, pooled (sign-confounded) | Lorenz VPT | -0.67 | curv -0.78 | 1050 |

For memory capacity the rebuild is decisive: `d_eff` orders the null ladder **perfectly**
(`r_s = +1.00`: connectome > weight-permuted control > clustering > modularity > degree >
ER > random) where PR does not (`+0.11`), and predicts MC **within the frozen non-negative
regime** at `r_s = +0.998` (PR `+0.31`). The connectome holds ~430 usable readout directions
vs random's ~215 at sr = 3.05, tracking MC 14.5 vs 8.9, while PR sees only ~1.2-1.4 for both.
This dissolves the original PR-based between-regime caveat for memory.

*Spectral origin (from `w_spectra.parquet`).* The connectome has an anomalously **compact
eigenvalue bulk** (bulk95 = 0.325 vs 0.48-0.55 for the nulls; bulk95 orders the MC ladder at
`r_s = -0.96`). Compact bulk -> high ridge effective rank -> memory. bulk95 = 1/`sr_crit`, a
quantity already in the framework, so the mechanism needs no new machinery. (A near-degeneracy
hypothesis, that the connectome has many near-equal leading eigenvalues, was tested and
FALSIFIED: it has the fewest, and the count correlates -0.84 with MC, backwards.)

*Sign-gating control.* Under balanced sign no topology ordering survives (gaussian ladder,
n = 7, all p > 0.1, for both MC and NARMA), against the empirical column's MC `r_s = +1.00`
at p < 1e-4. The well-powered, decisive contrast is MC; the individual n = 7 gaussian
coefficients are noise and their sign is not meaningful.

*Two-axis account.* Memory tasks read out effective rank (within-regime); the generative
Lorenz task reads out trajectory **straightness** (curvature), and only BETWEEN regimes.
Within the empirical column `d_eff` reads MC (`+0.998`) but not VPT (`+0.03`), and curvature
reads neither (no variance there, `-0.04`); the curvature-VPT axis is real only pooled across
sign regimes (`-0.78`), where `d_eff` also correlates with VPT (`-0.67`) via the same sign
confound. Distinct axes, not one metric for everything.

*Honest departures from the pre-registered expectation (data over expectation).*
1. **NARMA is not a PR failure.** PR orders the NARMA ladder perfectly (`-1.00`) and predicts
   it within-regime as well as `d_eff` (`-0.74` vs `-0.71`). The `d_eff` advantage is
   **specific to memory capacity** (deep linear recall, the task that most demands the
   low-variance tail); NARMA needs less memory depth, so PR's top directions suffice. The
   claim is "d_eff is the measure that works for both, and PR fails on the task that most
   demands memory depth", not "PR is wrong everywhere".
2. **Curvature does not predict VPT within regime**, only pooled via the sign confound, so no
   geometric axis is a clean within-regime predictor for the generative task at N=448.

*Read (Probes 1-3, one account).* Weight sign is the master switch: non-negativity splits the
spectrum into a saturating Perron / common mode plus a fluctuation bulk and freezes the
manifold, which becomes low-D and temporally coherent (Probe 1) and spatially low-frequency
(Probe 2). Within the non-negative regime, topology sets memory through readout dimensionality:
the connectome's compact spectral bulk gives it the most usable readout directions, and
**memory capacity <- ridge effective rank** is a sharp, sign-gated, within-regime result
(Probe 3). Generative prediction lives on a separate straightness axis. The connectome is not
geometrically special *per se*, sign is the lever, but within the biological non-negative
regime its topology buys a real, consistent, readout-relevant dimensionality margin that PR
had hidden.

---

## 7. Execution checklist

1. Confirm the I/O routing convention in the task configs (Section 1). Flag any
   mismatch before proceeding.
2. Step 0: locate or add opt-in state capture; cache state matrices for human
   N=448 across conditions, sweep, tasks, seeds.
3. Implement `src/analysis/manifold.py` with a `--smoke`-scale unit check.
4. Probe 1 driver, smoke, then full N=448 run; write metrics parquet and figures;
   complete Findings.
5. Probe 2 mode, smoke, then full; write alignment parquet and figure; complete
   Findings.
6. Probe 3 join, correlations, figures; complete Findings.
7. Pause and return to the strategy discussion (direction for Probes 4 and 5)
   before extending to N=1000 or C. elegans.

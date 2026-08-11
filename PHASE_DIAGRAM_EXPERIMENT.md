# Phase Diagram Experiment: Sign Composition x Spectral Radius

*Main implementation reference for the headline phase-diagram experiment. This
document is self-contained on the science and does not depend on any external
proposal or chat context. Its companions in the repository are
`PROJECT_KNOWLEDGE_BASE.md` (repository structure, conventions, the null ladder,
the seven-condition factorial, the spectral-radius sweep, pinned hyperparameters)
and `MANIFOLD_PROBES_IMPLEMENTATION.md` (the parked Probe 1 to 3 findings and the
mechanism this experiment extends). Complete the `Findings` block under each panel
as results arrive.*

---

## 1. Established mechanism (what this experiment extends)

On the human N=448 connectome, Probes 1 to 3 established a two-part account:

- **Weight sign is the master switch.** With all-positive (non-negative) weights
  the recurrent matrix has a dominant Perron / common mode plus a compact
  fluctuation bulk, and the activity manifold freezes into a low-dimensional,
  temporally coherent state. With balanced sign it undergoes a supercritical
  transition into a saturated period-2 collapse (curvature to pi, effective
  dimensionality to 1).

- **Within the non-negative regime, topology sets memory through readout
  dimensionality.** The right measure is the ridge effective rank
  `d_eff = sum_i g_i / (g_i + alpha)` over the design-matrix Gram eigenvalues
  `g_i` with each task's own `alpha` (the effective degrees of freedom of the
  ridge solution). `d_eff` orders the null ladder for memory capacity perfectly
  (connectome ~430 usable directions vs Erdos-Renyi ~215 at sr = 3.05, tracking
  MC 14.5 vs 8.9) and predicts MC within-regime at Spearman +0.998. Participation
  ratio misses this. The spectral origin is bulk compactness (connectome
  bulk95 = 0.325 vs 0.48 to 0.55 for nulls; bulk95 orders the MC ladder at -0.96;
  bulk95 = 1/sr_crit). Under balanced sign, topology is inert.

So far "sign" is binary (all-positive vs balanced). This experiment makes it
**graded** and maps where topology controls computation.

**Two computational axes, mirrored panels.** Probes 1 to 3 also showed the two
task families read out different geometry: memory tasks read out effective rank;
the generative Lorenz task reads out trajectory straightness (curvature), not
rank. Crucially, curvature was *frozen* within the non-negative regime at f = 0,
so the probes could not use it as a within-regime order parameter. This experiment
varies sign continuously, which **un-freezes curvature** and makes it a live order
parameter across the (f, sr) plane. Both task families are therefore treated as
equal first-class axes here, in two mirrored panels.

---

## 2. Hypothesis

There is a region of (negative-weight-fraction x spectral-radius) space in which
network topology controls the manifold geometry that computation reads out, and
outside it topology is inert. The boundary of that region is predictable from a
spectral / common-mode quantity. The memory and generative axes may share that
boundary or occupy different regions; determining which is a central result.

---

## 3. The sign-composition axis

The fraction `f` of negative weights is the primary axis. A naive design would flip
`f * nnz` edges chosen uniformly at random, but that is confounded: it lets *where*
the negative weights land vary with the luck of the draw, and where they land
matters enormously. The mechanism is spectral -- the common mode is the Perron
eigenvector, and the leading eigenvalue of a non-negative graph is dominated by
high-degree / rich-club nodes -- so flipping an edge incident on a hub perturbs the
Perron structure far more than flipping a peripheral edge. Under uniform flipping,
the *effective* spectral perturbation at a fixed `f` would depend on hub coverage,
injecting uncontrolled noise into exactly the axis whose spectral meaning the phase
diagram is trying to read. The design below removes that confound as the primary,
and then promotes placement to a deliberate secondary axis.

**Edge importance score.** Rank each nonzero edge by an importance score of its
endpoints. Use endpoint degree as the primary, legible score (for the undirected,
symmetric human W, degree, weighted strength and eigenvector centrality correlate
strongly, so degree is a fine first choice). Compute the score on the FIXED base
topology per variant, and hold it fixed across `f`, `sr` and seeds, so "hub edges"
are a stable set for a given variant. Also compute an eigenvector-centrality-product
score for a robustness check (it is closer to what actually moves the leading
eigenvalue). Note that Erdos-Renyi has no hubs to target: that is the point, and the
contrast "targeting matters on the connectome but there is nothing to target in ER"
is itself a clean statement about why structured topology is special.

**PRIMARY -- stratified (placement-neutral) edge-wise flipping.** This is the
mandatory confound fix and the design the headline phase diagram uses.
- Base weights: the all-positive empirical magnitudes (the `human_empirical` weight
  scheme) for each topology variant.
- Stratify edges into bins by the importance score (for example deciles of endpoint
  degree). At fraction `f`, flip the sign of a fraction `f` of the edges *within
  each stratum*, chosen by a reproducible seeded RNG (keyed by variant, seed, f).
  This holds hub-to-periphery composition of the flipped set constant across the
  whole `f` sweep, so `f` means "how much sign, holding where fixed". Average over a
  few stratified draws per cell for the residual randomness.
- CRITICAL: apply the flip to the base matrix BEFORE spectral-radius rescaling, and
  hold the flip pattern FIXED across the sr sweep for a given (variant, seed, f,
  draw). Only sr rescales (`W(sr) = W_base * sr / max(|eig(W_base)|)`).
- Record `targeting = stratified` on every output row.

**SECONDARY -- placement as its own axis (run after the primary is validated).**
Same `f` grid, but choose *which* edges flip by the importance score rather than
neutrally, under two additional regimes:
- `hub_first`: flip the highest-importance edges first, so hub weights turn negative
  before peripheral ones as `f` rises.
- `periphery_first`: the reverse; hubs stay positive longest.
The hypothesis, straight from the mechanism: if the Perron / common mode gates
topology-relevance, a small fraction of hub-targeted negative weights should
collapse the phase boundary at much lower `f` than the same fraction placed
peripherally, i.e. the boundary in (f, sr) should shift strongly with targeting and
`hub_first` should be the most efficient way to destroy the non-negative regime. If
targeting does not move the boundary, the effect is genuinely distributed and only
the count matters -- also a clean finding. Record `targeting` in
{stratified, hub_first, periphery_first}.

**SECONDARY arm -- Dale node-wise sign fraction** (biological robustness; run after
the edge-wise primary). Select `floor(f * N)` NEURONS to be inhibitory and negate
all of their OUTGOING weights (confirm from the reservoir build code whether a
neuron's outgoing weights are a column or a row of `W`), leaving the rest positive.
`f` is then the inhibitory fraction (cortical E/I is ~0.2; f = 0.5 is balanced).
The stratified-vs-targeted distinction also applies here (random inhibitory nodes vs
hub / periphery inhibitory nodes) but start with random inhibitory selection. Tag
every output row with `sign_mode` in {edge, dale}.

---

## 4. Grid

- `f`: 0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50  (11 values)
- spectral radius: 16 points evenly over `[0, 6]` (a phase diagram needs a smooth
  boundary, not the full 58-point sweep)
- variants: `connectome`, `degree_rewire`, `erdos_renyi` (both order parameters
  need connectome and ER; degree_rewire is the intermediate rung)
- seeds: 10 (plus a few stratified draws per cell, averaged)
- tasks: memory capacity and NARMA-10 (memory panel), Lorenz (generative panel)
- `sign_mode`: `edge` (primary), `dale` (secondary)
- `targeting`: `stratified` (primary), then `hub_first` and `periphery_first`
  (secondary)

**Sequence the run so the mandatory part lands first, then the bonus:**
1. `sign_mode=edge`, `targeting=stratified` -- the headline phase diagram. This is
   the confound-fixed primary and must be complete and interpreted before anything
   else. ~11 x 16 x 3 x 10 = 5,280 instantiations per task; cheap on CPU.
2. `sign_mode=edge`, `targeting` in {`hub_first`, `periphery_first`} -- the
   placement study (two more copies of the grid). Bonus that sharpens the
   mechanism; do not let it block the primary.
3. `sign_mode=dale`, `targeting=stratified` -- the biological robustness arm.

Smoke-test on a 3 x 3 sub-grid, 2 seeds, 1 variant, 1 task, `stratified` only,
first.

**Scope: human N=448 only for now.** Do not extend to N=1000 or C. elegans until
the N=448 result is interpreted.

---

## 5. Per-cell measurements

Write a tidy parquet, one row per
(`sign_mode`, `targeting`, `f`, `variant`, `spectral_radius`, `seed`, `task`), keys
plus:

- `d_eff` (ridge effective rank from the captured design-Gram spectrum with the
  task's `alpha`) -- the memory-panel geometric quantity
- `mean_curvature` (turning-angle straightness of the driven trajectory) -- the
  generative-panel geometric quantity (the Lorenz value is the one the generative
  panel uses)
- performance: `mc`, `nrmse`, `vpt`, `climate_error` (as applicable per task)
- `pr` (participation ratio, kept only as the contrast)
- `mean_state` (signed mean over units and time of the driven state -- the
  common-mode magnitude, the sign signature), `mean_gain` (mean of `1 - x^2`),
  `frac_saturated` (fraction of `|x| > 0.99`)

W-spectrum scalars, computed once per (`sign_mode`, `targeting`, `f`, `variant`,
`seed`) since sr only rescales but the flipped-edge set differs by targeting (store
in a small separate table keyed without sr/task, or repeat per row):

- `bulk95` (pct95(|lambda|) / |lambda_1| of the normalised base matrix)
- `leading_gap` = |lambda_1| - |lambda_2|
- `lead_is_real` (whether the leading eigenvalue is real -- the Perron signature,
  which should disappear as f rises)

**Reuse existing code; do not reimplement.** `ridge_effective_rank` and
`participation_ratio` in `src/analysis/manifold.py`; `mean_curvature` from the same
tier; `bulk95` from `src/analysis/spectral.py`; the reservoir builder and
`rescale_spectral_radius` in the reservoir build module; the MC/NARMA/Lorenz
evaluators and the opt-in state-capture hook added for the manifold probes. The new
code is only the sign-fraction weight transform, the sweep driver, and the
phase-diagram analysis and plots.

---

## 6. Analysis: two mirrored panels

Both panels take medians over the 10 seeds (and the few stratified draws) per
(`sign_mode`, `targeting`, `f`, `sr`) cell, and report the connectome-vs-ER contrast
per cell as a Cliff's delta over seeds (reuse the rank stats in
`src/experiment/stats.py`) so boundaries can be drawn on significance as well as
magnitude. Unless stated otherwise, the panels and their boundaries are computed on
the `sign_mode=edge`, `targeting=stratified` primary; the placement analysis below
uses the `hub_first` and `periphery_first` runs.

### Panel A -- Memory (geometric order parameter: ridge effective rank)

- Order parameter: `dD(f, sr) = d_eff(connectome) - d_eff(erdos_renyi)`, on memory
  capacity (primary) and NARMA (secondary). Higher = larger connectome advantage.
- Performance validation: `dMC`, `dNARMA` (same contrast on the task scores).
- Candidate spectral predictors of the boundary: `bulk95` and the common-mode
  magnitude `|mean_state|`.

### Panel B -- Generative (geometric order parameter: straightness)

- Straightness `s = -mean_curvature` (equivalently `pi - mean_curvature`; higher =
  straighter = more linearly predictable). Order parameter:
  `dStraight(f, sr) = mean_curvature(erdos_renyi) - mean_curvature(connectome)`,
  on Lorenz. Positive = connectome holds a straighter, more predictable manifold =
  connectome advantage (defined so higher = connectome advantage, mirroring
  Panel A).
- Performance validation (secondary here; raw-prediction-quality anchoring is a
  planned later extension, not this run): `dVPT`, `dClimate`.
- Candidate spectral predictor of the boundary: the effective spectral radius of
  the fluctuation dynamics, `effective_radius = bulk95 * sr * mean_gain`, and its
  crossing of ~1 (the onset of the period-2 curvature blow-up), plus the
  common-mode magnitude `|mean_state|` as the self-limiting agent.

The two panels deliberately hypothesise *different* spectral predictors: memory set
by how compact the bulk is, prediction set by whether the closed-loop rollout stays
stable. Whether they in fact share a predictor (for example the common mode) is
part of the cross-panel question.

### Observed boundary (each panel)

The locus in (f, sr) where the order parameter collapses. Draw two ways and report
both: (i) the contour where the order parameter falls to 25% of its global maximum;
(ii) the contour where the connectome-vs-ER Cliff's delta drops below a stated
threshold / loses significance.

### Predicted boundary (each panel, the key deliverable)

For each candidate predictor of that panel, define its own collapse contour (for
example where `|mean_state|` falls to 25% of its f = 0 value, or where
`effective_radius` crosses 1) and overlay it on the order-parameter heatmap. Report
which predictor best matches the observed boundary, quantitatively (agreement of
the two contours in (f, sr), or correlation of the order parameter with the
predictor across all cells). Report this honestly even if no predictor matches
well: a clean phase diagram with an unexplained boundary is still a result.

### Cross-panel comparison (central result)

Overlay Panel A's and Panel B's observed boundaries on one (f, sr) plane. Do
topology's grip on memory and on prediction occupy the same region of
sign-composition space, or different ones?

- If they coincide, the master statement is that sign composition gates
  topology-relevance for computation generally (and, if the common-mode predictor
  wins both panels, the common mode is the single controlling quantity).
- If they differ, the two computational axes have distinct operating points; report
  where each boundary sits and where the real connectome / biological E-I fraction
  (edge f approximately 0.5 balanced is not biological; Dale f approximately 0.2 is)
  falls relative to both.

### Placement / targeting analysis (secondary axis)

For the `hub_first` and `periphery_first` runs, compare the observed boundary
location against the `stratified` baseline, for both panels. The quantity of
interest is the critical fraction `f*` at which the order parameter collapses
(at a representative sr, or as a curve over sr). Report `f*` for each targeting
regime. Expectation: `f*(hub_first) < f*(stratified) < f*(periphery_first)` -- hub
targeting collapses the regime with the fewest negative weights. Quantify how few
hub edges suffice (the `f*` gap between hub_first and periphery_first is the size of
the placement effect). If the three regimes give the same `f*`, the effect is
count-driven, not placement-driven; report that plainly.

---

## 7. Figures (300 dpi, to the driver's `figures/`)

Panel A (memory), all on the `edge` / `stratified` primary:
1. `dD(f, sr)` heatmap (MC) with observed and best predicted boundary overlaid.
   Headline for Panel A.
2. `dMC(f, sr)` heatmap (performance), same overlay.

Panel B (generative), all on the `edge` / `stratified` primary:
3. `dStraight(f, sr)` heatmap (Lorenz) with observed and best predicted boundary
   overlaid. Headline for Panel B.
4. `dVPT(f, sr)` heatmap (performance validation), same overlay.

Cross-panel and support:
5. Both observed boundaries on one (f, sr) plane -- the cross-panel figure.
6. Predictor panels: `|mean_state|`, `bulk95`, `leading_gap`, `effective_radius`
   vs f (showing the common-mode / Perron / stability collapse), plus a scatter of
   observed vs predicted boundary location for each panel.
7. Line cuts: each order parameter vs f at fixed sr (2, 4, 6) and vs sr at fixed f
   (0, 0.1, 0.25, 0.5).
8. Placement study: `f*` (critical collapse fraction) vs targeting regime
   (`hub_first`, `stratified`, `periphery_first`) for both panels, showing how few
   hub edges suffice to collapse the regime; optionally the three `dD` heatmaps
   side by side.
9. Secondary: the Dale-arm `dD` and `dStraight` heatmaps beside the edge-wise ones
   (robustness).

---

## 8. Conventions

Additive changes only: reuse the builder, evaluators, state-capture hook,
`ridge_effective_rank`, `mean_curvature`, and `bulk95`; do not modify frozen
hyperparameters or the existing run matrix. New generic code in `src/analysis/` or
the reservoir tier as appropriate; driver under `experiments/human/analysis/`
mirroring the existing pattern. British spelling; no em or en dashes; guarded
string-replacement edits with assertion checks; read source files before editing;
`--smoke` before any full run; parquet outputs gitignored. Propose a plan of attack
and file layout before writing code, and flag anything in this spec that conflicts
with the codebase rather than guessing.

---

## 9. Findings

### Panel A -- Memory (d_eff)

*(append: the `dD` heatmap values at representative cells -- f in {0, 0.25, 0.5} x
sr in {2, 4, 6}; the observed boundary; which spectral predictor matched and how
well; whether `dMC` tracks `dD`.)*

**Run.** Edge / stratified primary, human N=448, on ada. 47,520 rows
(11 f x 16 sr x 3 variants x 10 seeds x 3 draws x 3 tasks), `phase_cells.parquet`
3.4 MB. f=0 correctness gate passed at machine precision (median rel = 0.0 exactly,
120 rows per strict task; Lorenz reproduced bit-for-bit too) so the transform is a
clean no-op at f=0 and the sweep is trustworthy.

**`dD = d_eff(connectome) - d_eff(erdos_renyi)`, representative cells:**

| f \ sr | 2 | 4 | 6 |
|---|---|---|---|
| 0    | -134.75 | +329.44 | +295.95 |
| 0.25 |  -86.37 |   -0.70 |   +4.33 |
| 0.5  |  -75.54 |   -0.09 |   +2.35 |

The connectome memory advantage is a low-f, supercritical wedge: maximal at f=0 for
sr >~ 3 (dD ~ +330 at sr=4, Cliff delta +1.00), extinguished by f ~ 0.15 to 0.20.
Below sr ~ 2.4 the connectome is *worse* than ER (dD < 0), so the advantage exists
only above the critical spectral radius. Observed collapse boundary f*(sr) rises
with sr: 0 for sr < 2.4, then 0.023 (sr 2.8) -> 0.115 (sr 4) -> 0.184 (sr 6); the
magnitude (25%-max) and significance (Cliff delta) contours agree to within ~0.06 in
f.

**Mechanism (important nuance).** The collapse is ER *rising to the d_eff ceiling*,
not the connectome degrading. At sr=4 the connectome d_eff barely moves
(416 -> 448 over the f-sweep) while ER climbs 87 -> 200 -> 325 -> 416 -> 448; both
saturate at the N=448 ceiling by f ~ 0.2. So `dD` measures how many negative weights
ER needs to de-correlate its bulk up to the rank ceiling the connectome already sits
at with all-positive weights (the parked bulk-compactness result).

**Predictor.** `|mean_state|` (common-mode magnitude) collapse tracks the boundary
directionally (Spearman +0.79 with dD, supercritical) but lags it (predicts
f* ~ 0.25 vs observed ~ 0.11 to 0.18; mean |df*| = 0.167). `mean_gain` is the
strongest single across-cell correlate (-0.94) but is just the saturation flip-side
of the same common mode. Net: the common mode is the right family of predictor,
directionally, but does not pin the boundary tightly.

**`dMC` tracks `dD` but outlives it.** dMC is +8.65/+9.01 at f=0 (sr 4/6) and
collapses with dD, but retains a small positive edge (~ +1 to +1.5) at high f after
dD has saturated to 0 -- the performance advantage survives the geometric one,
because raw MC is not ceiling-bound the way d_eff is.

### Panel B -- Generative (straightness)

*(append: the `dStraight` heatmap at the same representative cells; the observed
boundary; whether curvature genuinely un-froze across the f-sweep and became a live
order parameter; which spectral predictor matched; whether `dVPT` tracks
`dStraight`. Note the prior expectation that the Lorenz topology effect may be weak
per-seed -- a memory-specific-advantage null here is a valid finding, not a
failure.)*

**Curvature genuinely un-froze -- the central Panel B claim holds.**
`dStraight = curvature(ER) - curvature(connectome)` is exactly 0 at f=0 across every
sr (connectome and ER have identical curvature in the non-negative regime, ~0.26 rad,
both straight), and becomes a live, positive order parameter once f > 0. It is an
*emergent* order parameter (rises from 0 with f), the mirror of Panel A's collapse,
so its boundary is an ONSET contour, not a collapse contour (see "Honest departures").

**`dStraight` representative cells (and `dClimate`, the stronger signal):**

| f \ sr | dStraight 2/4/6 | dClimate 2/4/6 |
|---|---|---|
| 0    | +0.00 / +0.00 / +0.00 | -0.00 / -1.62 / -9.30 |
| 0.25 | +2.32 / +0.11 / +0.06 | +3.22 / +7.02 / +30.98 |
| 0.5  | +1.41 / +0.07 / +0.03 | +1.27 / +38.85 / +15.36 |

Onset boundary f*(sr) descends with sr: 0.215 (sr 2) -> 0.163 (sr 3.2) -> 0.113
(sr >~ 4.4), i.e. higher gain makes the generative advantage appear at lower f.

**`dStraight` is a resistance margin, not an operating optimum (see departures).**
The connectome's OWN absolute Lorenz performance is best at f=0 (sr=4: VPT 2.81, climate
1.77) and degrades monotonically with f; the intermediate-f `dStraight` peak is where
ER has collapsed to curved period-2 (curv ~ 3.0) but the connectome is still straight
(curv 0.26). The connectome's curvature-collapse threshold f_c(sr) is ~0.35 to 0.40
at sr=2, ~0.15 to 0.20 at sr=4, ~0.15 at sr=6; the dStraight peak drifts with it
(f=0.35 at sr=2 -> 0.15 at sr >= 4.4), so there is no privileged f ~ 0.2.

**Predictor: `effective_radius` crossing 1 matches well.** Best Panel B predictor:
`B_effective_radius` (Spearman +0.72 with dClimate, +0.57 with dStraight,
supercritical); its =1 crossing predicts the onset to mean |df*| = 0.103 (crosses 1
at f ~ 0.25 for sr >= 3.2, exactly where dClimate switches on). `bulk95` is second
(+0.65 with dClimate).

**`dVPT` does NOT track `dStraight`; `dClimate` does.** Short-horizon prediction
(dVPT) is weak and mostly confined to sr ~ 2 (near 0 at high sr). The connectome
generative advantage lives in long-run climate fidelity (dClimate up to +30 to +40 at
supercritical sr, f >= 0.25), which needs BOTH sign and supercritical gain -- the
mirror of memory.

### Cross-panel comparison

*(append: do the two observed boundaries coincide or diverge in (f, sr)? Does one
spectral quantity, for example the common mode, predict both? Where does the real
connectome and the biological E-I fraction sit relative to each boundary?)*

**The boundaries diverge and cross -- a dissociation, not a shared boundary.** The
memory-collapse boundary (advantage below it) and the generative-onset boundary
(advantage above it) run in *opposite* directions in sr and cross near
(sr ~ 4, f ~ 0.12):

| sr | memory collapse f* (below = adv) | generative onset f* (above = adv) |
|---|---|---|
| 2 | -- (connectome worse)  | 0.215 |
| 4 | 0.115 | 0.126 |
| 6 | 0.184 | 0.112 |

- Low sr (2 to 3): no memory region; generative advantage only, at high f (~0.16 to
  0.21).
- High sr (>= 4): the boundaries cross and open a narrow overlap band
  (~0.11 < f < 0.18) where both advantages coexist -- memory-only below it,
  generative-only above.
- Mean |fA - fB| = 0.092, but that average hides the sr-dependent crossover.

**No single spectral quantity predicts both.** As hypothesised, the panels have
distinct predictors: memory follows the common mode `|mean_state|` (how compact /
coherent the bulk is), generation follows `effective_radius` -> 1 (whether the
closed-loop rollout stays sub-critical). They are not the same quantity.

**Biological anchors.** The real connectome (edge f=0) is memory-only across all
supercritical sr; edge f=0.5 (balanced) is generative-only. The two computational
regimes are genuinely separated in sign space. NB the biological E/I ratio is a
*Dale/node* quantity (~0.2 inhibitory neurons), not the edge fraction swept here; its
placement relative to these boundaries is now given by the Dale arm below.

### Dale arm (node-wise E/I, biological)

*(sign_mode = `dale`: a fraction f of NEURONS made inhibitory, all their outgoing
weights negated (a column of W; ReservoirPy computes `W @ s`), deliberately breaking
symmetry per Dale's law. Here f is the inhibitory-NEURON fraction, so f ~ 0.2 is the
biological cortical ratio, unlike the edge arm where f is an edge fraction. Run
`--sign-mode edge,dale`, one combined parquet, 95,040 rows; f=0 gate exact (edge and
Dale identical no-ops).)*

**Memory is essentially identical to the edge arm.** The `dD` wedge, the subcritical
(sr < 2.4) connectome penalty, the collapse by f ~ 0.15 to 0.2, and the predictors
(`mean_gain` Spearman -0.87, `|mean_state|` +0.75) all match the edge arm
(dD at sr=4: +329 at f=0 -> ~0 by f=0.25 under both). So the memory result depends on
*how much* negativity, not on whether it is placed edge-wise or by whole-neuron sign
-- a clean robustness confirmation of Panel A.

**Generation is broader and stronger under Dale.** The straightness advantage, a
narrow diagonal sliver in the edge arm, fills a much wider region of (f, sr) under
Dale (fig9, bottom row); the biologically correct structure makes the connectome's
generative resistance *more* prominent, not less. `dClimate` is large and positive at
supercritical sr for f >~ 0.25 (up to +26 at sr=6/f=0.25, +79 at sr=6/f=0.5, though
the largest values are partly ER's climate diverging). Dale `dStraight` now tracks
`perron_root` (Spearman +0.57) -- sensible, since the broken symmetry revives the
Perron root (and `lead_is_real`) as a live quantity that the symmetric edge arm could
not use.

**The biological ~20% inhibitory fraction is a survivable ceiling, NOT an optimum.**
Now that f is a neuron fraction the E/I question is fair, and the connectome's own
absolute Lorenz fidelity under Dale at near-critical sr=2 answers it:

| f (inhibitory) | VPT | climate err | curvature |
|---|---|---|---|
| 0.10 | 3.74 | 0.19 | 0.26 (straight) |
| 0.20 | 2.75 | 0.12 | 0.27 (straight) |
| 0.25 | 2.53 | 3.35 | 1.08 (collapsed) |
| 0.50 | 1.09 | 7.86 | 1.57 |

The connectome sustains a faithful, straight Lorenz attractor up to ~20% inhibition,
then collapses just beyond it -- so 80/20 sits at the *upper edge* of the
faithful-generation regime. But it is a ceiling, not a tuned optimum: the connectome
generates *best* at f=0 (VPT 4.43 vs 2.75 at f=0.2), and the collapse point is
sr-dependent (~f=0.15 at sr=4). The honest statement is that this topology *tolerates*
about the biological amount of inhibition before losing the straight manifold, and
tolerates more of it than ER does (the positive `dClimate` / `dStraight`), not that it
is optimised for 20%.

### Placement / targeting

*(append: the critical fraction `f*` for `hub_first`, `stratified` and
`periphery_first`, for each panel; how few hub-targeted negative edges collapse the
regime vs peripheral ones; whether the effect is placement-driven or count-driven.
Report both the degree score and the eigenvector-centrality robustness check.)*

*(Run: `--targeting stratified,hub_first,periphery_first --sign-mode edge,dale`, the
full 285,120-row parquet, degree score. The eigenvector-centrality robustness check
is the one remaining deferred extension -- see below.)*

**Placement matters, and the effect is clean on the biological (Dale) axis, muddy on
the edge axis.** Memory-collapse `f*` (higher = advantage survives to more sign), mean
over supercritical sr (>= 3):

| sign mode | hub_first | stratified | periphery_first |
|---|---|---|---|
| edge | 0.179 | 0.133 | 0.248 |
| dale | **0.087** | **0.124** | **0.164** |

- **Dale follows the predicted ordering exactly: `hub_first < stratified <
  periphery_first`.** Making the hub NEURONS inhibitory collapses the connectome
  memory advantage at ~9% inhibition, versus ~16% for peripheral neurons -- hub
  targeting is roughly **2x more efficient**, and the ordering holds at every
  supercritical sr (e.g. at sr=6: hub 0.118, strat 0.161, peri 0.207). This is the
  mechanism prediction confirmed: the Perron / common mode is concentrated on the
  high-degree hubs, so making those neurons inhibitory disrupts it with the fewest
  inhibitory nodes.
- **The edge arm is muddier**: periphery_first does preserve the regime longest
  (0.248, as expected), but `hub_first` (0.179) is NOT the fastest to collapse --
  `stratified` (0.133) is. This is the d_eff-ceiling confound (Panel A): the edge
  memory boundary is set by ER rising to the rank ceiling, and ER has no hubs to
  target, so edge-targeting is not a clean test of hub-gating. Placement reveals its
  true, count-beating effect on the node-wise (biological) axis, not the edge axis.
- **Effect is placement-driven, not count-driven** (on the Dale axis): the same total
  inhibitory fraction collapses the regime at very different points depending on
  whether the hubs or the periphery are inhibited (the ~0.09 vs ~0.16 gap).
- Generative onset is noisier: Dale hub_first onsets earliest (mean f* 0.075 vs strat
  0.111, peri 0.109); the edge periphery_first onset is degenerate. See fig8 (now one
  row per sign mode).

**Eigenvector-centrality robustness (score check).** Repeating the placement grid with
eigenvector centrality instead of degree to define a hub (`--score eigenvector`, own
285,120-row parquet, fig10) shows the result is not a proxy artifact: on the Dale axis
the `hub_first < stratified < periphery_first` ordering holds under both scores
(eigenvector 0.103 < 0.118 < 0.219 vs degree 0.087 < 0.124 < 0.164; the effect is if
anything larger under eigenvector), while the edge arm stays muddy under both (the
d_eff-ceiling confound, not a score effect). Placement is robust to the hub definition,
closing the experiment: all arms (edge / Dale x stratified / hub_first / periphery_first
x degree / eigenvector) are complete and interpreted.

### Honest departures from expectation

*(append: anything the data contradicts -- for example topology staying live at
f = 0.5, no spectral quantity predicting a boundary, or the two panels behaving
identically when different predictors were hypothesised. Data over expectation.)*

1. **Panel B is emergent, not collapsing -- the boundary machinery had to be
   mirrored.** The spec's boundary operators (`observed_boundary`,
   `significance_boundary`) assume an order parameter that is high at f=0 and
   collapses as f rises (Panel A's shape). Panel B is the opposite: ~0 at f=0 and
   *created* by sign. The collapse operator spuriously pinned Panel B's boundary at
   f=0, corrupting fig3, fig5 and the A-vs-B agreement. Fixed additively with an
   `onset_boundary` / `significance_onset` operator (first f rising above 25% of
   global max). This is a real conceptual asymmetry between the two axes, not just a
   code bug.

2. **The intermediate-f `dStraight` peak is a resistance margin, NOT a biological
   E/I optimum.** It is tempting to read the ~0.2 peak as the connectome being tuned
   to the 80/20 E/I ratio. The data does not support this: (a) the connectome's own
   absolute Lorenz performance is best at f=0 and degrades with every negative
   weight; (b) the peak is a difference-of-collapses (ER curves before the connectome
   does), so it marks how much longer the connectome resists curvature collapse, not
   an operating optimum; (c) the peak f drifts 0.35 -> 0.15 with sr, so there is no
   privileged 0.2; (d) f here is an *edge* fraction (symmetric stratified flips), not
   the *neuron* inhibitory fraction that the biological 80/20 refers to. The
   legitimate E/I-ratio test is the pending Dale arm.

3. **The memory boundary is a d_eff-ceiling effect.** dD collapses because ER rises
   to the N=448 rank ceiling, not because the connectome degrades (see Panel A). The
   geometric order parameter therefore saturates while the performance edge (dMC)
   persists -- so the "boundary" is where ER catches up, and the connectome retains a
   residual advantage past it.

4. **The common mode does not tightly pin the memory boundary.** `|mean_state|`
   collapse lags the observed dD collapse by ~0.1 in f (agreement 0.167). A clean
   phase diagram with a directionally-correct but loose predictor is the honest
   result; the boundary is not perfectly spectral.

5. ~~**Connectome subcritically worse.**~~ **WITHDRAWN by E0.2.** The original reading
   — below sr ~ 2.4 the connectome has *lower* d_eff / MC than ER (dD < 0) — was an
   artifact of comparing at matched **nominal** sr. Because each `W` is normalised by
   its own `|λ₁|` and the substrates have very different bulk-to-outlier gaps, at any
   nominal sr the connectome sits far below its own critical point while ER is already
   past its own. Re-indexed on effective criticality (`σ·bulk₉₅`), **89% of the deficit
   disappears** (min dD −217 → −24) and the connectome is marginally *better* at low
   effective criticality. Correct statement: **parity below criticality, advantage
   above.** The supercritical advantage itself survives matching (peak dD +344 → +197,
   57% retained) but is a **decay-rate** difference, not a capacity difference — all
   variants peak at the `d_eff = N` ceiling. See `criticality_matched/results/
   E02_verdict.md` §4.1 and §4.3.

---

## 10. Report-back checklist

Report: the smoke-test result; the grid actually run and file sizes; the `dD` and
`dStraight` heatmap values at the representative cells; the predicted-vs-observed
boundary comparison for each panel; and the cross-panel result. Flag any departure
from the hypothesis plainly.

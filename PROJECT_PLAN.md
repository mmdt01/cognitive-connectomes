# Connectome-Constrained World Models — Project Plan

*Operational thirteen-week plan from early June to thesis submission (first
week of September 2026). Companion to `RESEARCH_PROPOSAL.md` (the why) and
`PROJECT_KNOWLEDGE_BASE.md` (the how). This document is the schedule and the
decision structure; it should be updated as gates are passed and scope is
adjusted.*

---

## 1. Target and floor

**Target (B).** A working connectome-as-JEPA-predictor proof of concept: a
V-JEPA-style world model in which a frozen encoder produces frame latents, a
fixed connectome reservoir is the predictor, and only a linear readout is
trained. The substrate is the *Drosophila* optic lobe and the demonstration
task is future-latent prediction on optic-flow video, with optic flow read
off the latent by a linear probe. The null ladder is applied to the
predictor's wiring to attribute predictive capability to specific topological
features. Action-conditioning is an explicit stretch goal, the first thing
dropped under time pressure.

**Floor (A).** A thorough, null-controlled account of whether connectome
structure helps generic dynamical-system prediction, mapped along two
intersecting lines: a *scale row* across cellular connectomes of increasing
size, and a *realism column* walking up biological detail on a single
connectome. The two lines form a cross, not a grid (see section 3). This
stands alone as a thesis that satisfies the one-line statement even if (B)
does not converge. (A) is completed before (B) begins, and its core is also
the scientific content of the ECCV submission.

**The asymmetry that justifies the ambition.** (A) is built on mature
infrastructure and is low risk. (B) is genuine research risk concentrated in
one place (the JEPA integration). Because (A) is the floor, pushing hard on
(B) is sensible rather than reckless: the downside is bounded by a complete,
defensible thesis.

---

## 2. Why dynamical-system prediction bridges to the JEPA

Stage (A) and Stage (B) are the same computation in two coordinate systems. In
both, a fixed connectome reservoir ingests the recent history of a temporal
trajectory, folds it into a high-dimensional state, and a trained linear readout
maps that state to the next point; the reservoir machinery is identical and only
the input and target change. In (A) they are an observable signal (NARMA, a
Lorenz coordinate); in (B) they are encoder latents z(t) = encoder(frame_t),
with the target the future latent z(t+k). A latent trajectory is itself a
dynamical system, so predicting the next latent is the same problem as
predicting the next state of an attractor, in a learned high-dimensional
coordinate system rather than a hand-specified one. This is why the build
inherits the substrate pipeline unchanged and only the task module differs.

The progression is therefore a de-risking probe, not a warm-up. The thesis
premise (that connectome wiring is a useful inductive bias for predicting how a
representation evolves) splits into two claims: that the connectome is a good
predictive substrate at all, and that it stays good when the target is a learned
latent. The dynamical tasks test the first claim with every confound removed: no
encoder, no latent geometry, no collapse, and benchmark targets whose answers
are known. Because the mechanism is substrate-level (memory depth, nonlinear
mixing, echo-state separation, all set by wiring), the null-ladder attribution
transfers: a structural feature that Stage (A) shows is responsible for
predictive skill becomes a pre-registered hypothesis for what should help latent
prediction in Stage (B).

**A ladder of world-model-likeness within the three tasks.** NARMA-10 is
input-driven emulation, the tightest step up from memory capacity but not yet
autonomous. Mackey-Glass is autonomous forecasting of an evolving system.
Closed-loop free-running Lorenz feeds the reservoir's own predictions back as
input, so it must sustain a model of the dynamics with no ground-truth crutch,
which is mechanically what a world model does when it rolls a latent trajectory
forward in imagination. The sequence is a march from passive memory, to driven
nonlinear computation, to autonomous forecasting, to self-sustaining rollout;
the JEPA is that last capability applied to latent observations.

**Two honest caveats.** First, it is the frozen encoder that makes the analogy
tight: with the encoder fixed, the latent target trajectory is fixed and
known-in-principle, exactly like Lorenz, which is why the de-risking transfers.
Unfreezing the encoder sets the target moving and admits collapse, and the
analogy weakens. Second, success on low-dimensional known systems is necessary
evidence, not sufficient proof: latent space is high-dimensional and its
geometry is shaped by the encoder's objective rather than by physics. And as
section 3 notes, the dynamical tasks validate the mechanism and the methodology,
not the fly's specific advantage, which is ecological and only testable in the
optic-flow JEPA itself.

---

## 3. Load-bearing decisions already taken

- **V-JEPA-style latent prediction, not optic-flow regression.** The training
  objective is self-supervised prediction of future or masked latents; optic
  flow is a linear probe on the latent, not the regression target. This is
  what keeps it a world model and preserves the "only the readout is trained"
  claim.
- **Stage (A) is a cross, not a grid.** Biological realism is a second line of
  enquiry, but it is *not* crossed with the connectome set. Taking the full
  product (connectome by realism by null-rung by spectral-radius by task,
  times seeds) is intractable at fly scale, threatens Gate 1, and recreates
  the Movement I trap on a prediction task. Instead, two lines share one
  anchor cell:
  - *Scale row.* Vary the connectome (*C. elegans*, fly, optionally mouse)
    while holding a single canonical substrate condition fixed, and run the
    full five-rung null ladder. The canonical condition is directed empirical
    weights (v2b): each connectome carries its own empirically measured
    weights, so every organism is evaluated at the same level of biological
    realism. Because empirical weights differ across organisms, the
    cross-organism comparison reflects both topology and weight statistics; the
    within-organism null ladder is what isolates the contribution of topology,
    and it remains the primary inferential comparison. The anchor cell is
    therefore *C. elegans* at v2b, which is also the middle rung of the realism
    column below.
  - *Realism column.* Hold the connectome fixed at *C. elegans* and walk up
    biological realism one step at a time on the prediction task, through
    three named conditions: undirected signed-Gaussian (v2a), directed
    empirical weights (v2b), and directed empirical plus E/I sign under Dale's
    principle (v2d, Pereira 2015 atlas).
  - The column and row meet at *C. elegans* in the canonical condition, so the
    design is additive, not multiplicative.
- **The realism column lives on *C. elegans*, not the fly.** The data already
  exists and is validated through the v2a/b/c chain, so the column is mostly
  re-running existing code paths with the prediction task swapped in (the only
  genuinely new build is v2d sign, already on the roadmap); compute is trivial
  at N around 300; and the established regime-independence-across-weight-schemes
  result on memory capacity is precisely what licenses holding the expensive
  scale row at a single canonical condition without it being a weight-scheme
  artefact. The fly's own directedness, weights and E/I are explored where
  they matter, inside Stage (B) on the task its wiring was shaped for, rather
  than duplicated here.
- **Full ladder at each column step.** At each enrichment step, run the
  complete five-rung null ladder regardless of whether a supercritical gap
  appears at rung 2. The column is cheap at N around 300, so completeness
  costs little and avoids prematurely concluding that a feature is inert.
- **Cellular-only comparison set for (A).** *C. elegans*, *Drosophila* optic
  lobe, and (if feasible) mouse visual cortex, all run at the canonical v2b
  (directed empirical) condition on the scale row. The macro-scale human graph is
  excluded from the main comparison to avoid confounding organism with scale
  and resolution; it may appear only as an explicit, separate macro-scale
  generalisation probe if time allows.
- **Frozen encoder for the (B) proof of concept.** Encoder weights fixed,
  reservoir weights fixed, only the readout trained. No backpropagation
  through the reservoir. Joint encoder training is stated future work.
- **Generic ranking does not predict task-matched advantage.** A weak fly
  showing in (A)'s generic tasks does not undermine (B); the fly earns its
  place in (B) on ecological grounds. The dissociation is itself a reportable
  finding.

---

## 4. Decision gates

These are the moments where the plan branches. Each has an explicit trigger
and a fallback.

- **Gate 0 (end of Week 1) — JEPA viability.** Does a JEPA train with a fixed
  reservoir in the predictor slot on toy data, or does it collapse? If it
  trains, (B) proceeds as planned. If it collapses, Weeks 2 to 5 absorb extra
  effort on the collapse problem in parallel with (A), and the (B) scope is
  reconsidered before any fly work begins.
- **Gate 1 (end of Week 4) — ECCV results freeze.** Are the ECCV-scoped (A)
  results in hand and clean: the scale row across two connectomes
  (*C. elegans* plus fly) on two tasks with the null ladder, plus whatever of
  the *C. elegans* realism column is ready? If yes, write-up proceeds. If
  marginal, narrow the claim rather than chase more experiments into the
  writing window.
- **Gate 2 (end of Week 8) — (B) viability.** Is the fly-JEPA producing
  above-baseline future-latent prediction? If yes, Week 9 runs the null-ladder
  attribution. If no, action-conditioning is cut entirely and a decision is
  made between a focused rescue and reporting (B) honestly as a partial or
  negative result, which remains thesis-worthy under the project's
  null-reporting ethos.

---

## 5. Phase and week schedule

Week 1 begins the week of 8 June. Date ranges are Monday to Sunday.

### Phase 0 — Week 1 (8 to 14 June): pivot and de-risk

Three parallel tracks, all aimed at retiring risk before committing to the
long phases.

- **Bridge experiment.** On the existing *C. elegans* pipeline, swap the task
  from memory capacity to one-step-ahead prediction (NARMA-10 and a Lorenz
  coordinate). Run at least the rung-2 (degree_rewire) comparison across the
  standard spectral-radius sweep including the supercritical points. Question:
  does the supercritical higher-order-structure advantage survive the jump
  from retention to prediction? This reuses almost everything and produces the
  conceptual hinge result. It is also the anchor cell where the scale row and
  realism column will meet.
- **JEPA spike.** Smallest possible throwaway: toy data (drifting shapes or
  moving MNIST), a tiny encoder, a small random reservoir as predictor, the
  V-JEPA latent-prediction objective, readout-only training. Watch for
  collapse. Code is discarded; only the verdict carries forward. Feeds Gate 0.
- **Stage (A) preparation.** Confirm the fly optic lobe dataset (FlyWire
  versus the Janelia optic lobe release) and lock the cellular comparison
  list. Scope the scale problem: null generation and reservoir simulation at
  tens of thousands of nodes is two orders of magnitude past *C. elegans* and
  is the technical crux of Phase 1.

*Deliverables:* bridge result (does the effect survive into prediction);
spike verdict (Gate 0); locked connectome list and dataset.

### Phase 1 — Weeks 2 to 5 (15 June to 12 July): Stage (A), the cross

The foundational, title-satisfying result and the scientific core of ECCV.
The scale row (across organisms) and the realism column (on *C. elegans*) are
built around their shared anchor cell.

- **Week 2 (15 to 21 June): anchor and column.** Generalise the W1 prediction
  task into a proper evaluation module (the analogue of `memory_capacity.py`
  for forecasting). Build the cross-connectome loading pipeline. Get
  *C. elegans* fully through the new pipeline with the full five-rung ladder
  at the canonical condition (the anchor cell), then start the realism column:
  v2a and v2b reuse existing weight-scheme code; implement and run v2d sign.
  The column is cheap compute at N around 300, so its only real cost is the
  v2d build. Begin solving null-ladder scaling for large connectomes (sparse
  operations, swap-count and Louvain cost, seed and sweep budget).
- **Week 3 (22 to 28 June): scale row.** Run the fly optic lobe through the
  prediction pipeline with the full null ladder, at the single canonical
  condition only. This is the scale test; expect to subsample (single optic
  lobe, or a neuropil or column) and to trim the sweep density and seed count
  for the large graph. Produce the first cross-connectome comparison.
- **Week 4 (29 June to 5 July): complete and freeze.** Finish the realism
  column (the full five-rung ladder at each of the three conditions). Add
  mouse visual cortex (MICrONS) to the scale row only if it comes cheaply, at
  the canonical condition; otherwise lock the row to *C. elegans* plus fly.
  Run the statistics (permutation tests, Holm correction, effect sizes per the
  established convention); produce paper-grade figures. **Gate 1: ECCV results
  freeze.** (MICCAI deadline 1 July falls here and is being skipped; see
  section 7.)
- **Week 5 (6 to 12 July): consolidate and draft.** Robustness and sensitivity
  checks; finalise figures. Begin the ECCV draft (framing and methods adapt
  heavily from the existing interim report Chapters 1 to 3). Any (A) breadth
  beyond the ECCV core (mouse, extra column conditions, extra tasks) is
  non-blocking and may spill here or defer to the thesis.

*Deliverables:* complete Stage (A) cross with scale-row cross-connectome
attribution and the *C. elegans* realism column; ECCV draft underway.

### ECCV write-up — Weeks 5 to 6, submit by 15 July

Lead with the scale row (*C. elegans* plus fly cross-connectome prediction
with null-ladder attribution); fold in whatever of the *C. elegans* realism
column is ready by Gate 1; defer the rest to the thesis. Add the JEPA framing
and the spike as preliminary evidence the world-model step is buildable. Sold
on the interpretability and trustworthiness angle the null ladder provides: a
predictor whose capability is attributable to named structural features. Keep
the submission tightly scoped. Final polish and submission occupy the first
half of Week 6; the remainder of Week 6 begins Phase 2.

### Phase 2 — Weeks 6 to 11 (mid July to 23 August): Stage (B), connectome-as-JEPA-predictor proof of concept

Effective start is mid Week 6, after ECCV submission.

- **Week 6 (second half, 16 to 19 July).** Stand up Stage (B). Choose the
  frozen encoder and the optic-flow video dataset (a controlled synthetic
  flow dataset is the cleaner PoC choice and matches the fly's ecological
  stimulus; decide here). Define the future-latent prediction setup and the
  linear optic-flow probe.
- **Week 7 (20 to 26 July).** Build the real frozen-encoder to reservoir to
  readout pipeline (the fly version of the spike). Pour the fly optic lobe
  connectome into the predictor slot. First end-to-end training runs.
- **Week 8 (27 July to 2 August).** Make it work: debug collapse, tune the
  readout, establish that the predicted latent tracks the target above a
  trivial baseline. Stand up the optic-flow probe. **Gate 2: (B) viability.**
- **Week 9 (3 to 9 August).** The scientific payoff: apply the null ladder to
  the predictor's wiring. Compare the fly connectome predictor against degree,
  clustering and modularity-matched nulls on latent prediction. Which
  topological features help world-model prediction of optic flow?
- **Week 10 (10 to 16 August).** Consolidate (B) results and robustness. If
  clearly ahead, attempt the action-conditioning stretch goal; otherwise
  deepen the attribution analysis. Action-conditioning is dropped first if
  time is tight.
- **Week 11 (17 to 23 August).** Freeze (B) results; produce figures. This is
  the primary buffer week: if earlier experiments overran, they land here. If
  on track, begin the results chapters.

*Deliverables:* working fly-JEPA proof of concept with null-ladder
attribution; action-conditioning result or documented decision to defer.

### Phase 3 — Weeks 12 to 13 (24 August to 6 September): consolidation, writing, buffer

The interim report already carries Chapters 1 to 4, so end-stage writing is
results and discussion on an existing scaffold, not a cold start.

- **Week 12 (24 to 30 August).** Write the new results and discussion chapters.
  Reframe the introduction toward the delivered world-model result. Assemble
  Stage (A) and Stage (B) into a single narrative spanning the two axes.
- **Week 13 (31 August to 6 September).** Final polish, buffer, submission.

---

## 6. Risk register

- **Combinatorial blow-up in Stage (A).** Crossing biological realism with the
  full connectome set is intractable at fly scale and would threaten Gate 1.
  Mitigation: the cross-not-grid design (section 3). The realism column is
  three named conditions on *C. elegans* only; the scale row holds every
  organism at one canonical condition. No cell outside the cross is run.
- **Fly-scale compute (Phase 1, Weeks 2 to 3).** The largest concrete risk in
  the scale row. Mitigation: sparse linear algebra, subsampling to one optic
  lobe or neuropil, reduced sweep and seed budget for the large graph, and
  accepting n=10 direction-of-trend runs where n=50 is not affordable (the
  knowledge base already validates n=10 for trend calibration).
- **JEPA will not train (Phase 2).** Surfaced in Week 1 by the spike rather
  than discovered late. Mitigation: frozen encoder removes backprop through
  the reservoir; Gate 0 and Gate 2 force early decisions.
- **Latent collapse with a fixed predictor.** A known JEPA pathology that the
  fixed predictor changes in ways needing explicit analysis. Budget debugging
  time in Week 8; this is what Gate 2 protects.
- **ECCV write-up colliding with experiments.** Mitigation: Gate 1 freezes
  results at end of Week 4; the paper claim is narrowed rather than the
  experiment window extended.
- **Scope creep on the biological-realism ladder (v2e to v2j).** These are a
  quarry, not a path. The realism column stops at v2d; gap junctions,
  multi-timescale dynamics, anatomical routing and pharyngeal decomposition
  are not admitted to a foundational prediction chapter. Only a feature that
  earns its place in the prediction or JEPA story is implemented.

---

## 7. Conference targets

- **MICCAI GRAIL, 1 July.** Skipping. Weakest fit, tightest deadline; chasing
  it would spend a writing week on a marginal-fit venue during the (A) to (B)
  transition.
- **ECCV Safe World Models, 15 July, workshop 8 September, Malmö.** Primary
  near-term anchor. Content is the Stage (A) scale row (plus ready column
  conditions) with the JEPA framing and spike.
- **NeurIPS 2026 workshops, calls expected August to September, event
  December.** Post-thesis. Better-odds, better-fit home for the full
  two-stage story; timing lets the thesis and paper be nearly one artefact.
- **ICLR, 19 September (the 2027 cycle).** Post-thesis reach target for the
  complete story, submitted in the knowledge that main-conference odds may
  route it to a workshop.

---

## 8. Scope guardrails (what this project will not do)

- Will not cross biological realism with the full connectome set: Stage (A) is
  a cross, not a grid. The fly and mouse run at one canonical condition; the
  realism column is three named conditions on *C. elegans*.
- Will not extend the realism column past v2d (sign); v2e to v2j stay in the
  quarry.
- Will not put cellular and macro-scale connectomes on a single comparison
  axis.
- Will not train the encoder jointly with the reservoir in the proof of
  concept.
- Will not let a weak generic-task fly result override the ecological
  rationale for the fly in (B).
- Will not extend experiment windows into writing windows past the gates.

# Connectome-Constrained World Models — Project Plan

*Living forward plan, early July 2026. Companions: `RESEARCH_PROPOSAL.md` (the
why), `PROJECT_KNOWLEDGE_BASE.md` (the how and the record),
`PREDICTION_TASKS_INTERPRETATION.md` (the four-task account), and
`STAGE_B_KICKOFF_DOUBLE_PENDULUM.md` (the Stage B build spec). Milestone- and
gate-driven through to submission.*

---

## 1. Where things stand

The Stage A core is done on *C. elegans*: four tasks (memory capacity, NARMA-10,
Mackey-Glass, closed-loop Lorenz) on the wide `[0,4]` operating-point sweep,
across a seven-condition sign x tail x topology factorial.

**The finding.** The connectome is worse-or-equal at the canonical operating
point and the most robust variant supercritically, a flat plateau where
disk-like nulls peak and collapse. That robustness is primarily a weight-sign
(non-negativity / Perron) effect, with heavy tail a secondary task-gated
contributor and directedness minimal (its one role is stabilising closed-loop
Lorenz). The connectome is never the best substrate; its edge is
collapse-resistance in an all-positive matrix, biologically meaningful because
real structural weights are non-negative. Full account in the knowledge base and
`PREDICTION_TASKS_INTERPRETATION.md`.

One step remains before Stage B: a cross-connectome test of how general that
finding is (section 2). With it in hand, the thesis floor is a complete,
self-contained result, which is what lets Stage B be genuine exploration.

---

## 2. Finishing Stage A: cross-connectome generality (about one week)

The sign-driven collapse-resistance is established on a single connectome.
Before Stage B, test whether it holds across scale and organism, which is what
turns it from a *C. elegans* curiosity into a claim about connectomes. Two
connectomes go onto the existing framework, on the memory and
dynamical-prediction tasks:

- **Human macro-scale structural connectome (dMRI).** Undirected, non-negative,
  heavy-tailed: the full-effect cell of the factorial. The prediction is sharp
  and pre-registered, a strong robustness crossover by the same Perron mechanism,
  at macro scale and with no directedness. The cheapest, highest-value probe.
- **Drosophila optic-lobe module.** A larger directed cellular connectome that
  extends the comparison beyond *C. elegans* in scale. Standing up its loader now
  also de-risks any later fly capstone (section 3), though here it is a substrate
  on abstract tasks, not a JEPA.

Reuse is near-total: the generic runner, null ladder, factorial, and
divergence-robust statistics all carry over; the factorial is instantiated per
connectome (human supports the undirected conditions only; the fly supports the
directed conditions, with Dale if neurotransmitter labels are available). The
only new code is minimal loaders and substrate builders.

**Gate A.** Does the sign / non-negativity effect reproduce across connectomes
and scale? Confirmation strengthens the thesis and the workshop paper; a
departure is itself a reportable finding. Either way, Stage B follows.

---

## 3. The target (Stage B), reframed and open-ended

**Spine question.** Does the sign-driven collapse-resistance transfer from
predicting observable dynamics to predicting learned-latent dynamics, that is,
does it help when the connectome reservoir is the predictor of a JEPA world
model?

**Anchor.** The double pendulum in latent-space prediction (see
`STAGE_B_KICKOFF_DOUBLE_PENDULUM.md`): known physics, full ground truth,
interpretable in physical units, fast to iterate.

**Open-ended beyond the anchor.** What follows is chosen by what the double
pendulum reveals: further physical systems, the conservative-versus-dissipative
contrast, a scale probe. The narrative is the transfer question, not a fixed
final system.

**Fly optic flow, optional capstone.** Retained only as a closing flourish if the
latent-space mechanism holds and time remains. It is not the committed endpoint:
Stage A found the connectome's edge to be a generic weight-sign effect rather
than a task-specific topological one, so a fly-optic-flow JEPA would most likely
re-demonstrate that generic effect at the highest cost on the board, for
uncertain marginal payoff.

---

## 4. Why the bridge holds

Stage A and Stage B are the same computation in two coordinate systems: a fixed
connectome reservoir folds a trajectory's history into a state and a linear
readout predicts the next point. In A the trajectory is an observable signal; in
B it is encoder latents z(t), with the target the future latent. A latent
trajectory is itself a dynamical system, so the substrate pipeline is inherited
unchanged and only the task module differs, and the pre-registered hypothesis is
the Stage A one: the advantage, if it transfers, should live in the non-negative
weight conditions and collapse under a balanced-sign control. The frozen encoder
is what makes the analogy tight (the latent target is fixed and
known-in-principle, like Lorenz); the caveat is that success on low-dimensional
known systems is necessary evidence, not sufficient proof.

---

## 5. Stage B build

Full spec in `STAGE_B_KICKOFF_DOUBLE_PENDULUM.md`; the essentials:

- **Architecture.** Frozen encoder, fixed connectome reservoir as predictor,
  trained linear readout; V-JEPA-style future-latent prediction; physical
  quantities (angles, energy) read off the latent by linear probes. The same
  ridge-readout reservoir as Stage A, with latent vectors as input and target.
- **Carry the factorial, not just the ladder.** The effect to look for is the
  sign one, so the latent experiment must isolate sign, tail and topology, not
  only run the topology ladder.
- **Viability first.** Damped, short-horizon teacher-forced, on *C. elegans*;
  confirm the JEPA trains and beats persistence and a random-ESN reference in
  physical units. The frozen encoder is the primary anti-collapse mechanism; the
  real bar is beating persistence.
- **Then mechanism transfer**, then optional breadth (frictionless contrast, more
  systems, the fly capstone), chosen by results and time.

---

## 6. Milestones and gates

- **Now, about one week: cross-connectome generality (section 2).** Human macro
  connectome and fly optic-lobe module on the memory and prediction tasks.
  **Gate A.**
- **Then, Stage B.** Stand up the double-pendulum pipeline. **Gate B0** (JEPA
  viability: trains and beats persistence and a random-ESN reference in physical
  units). **Gate B1** (mechanism transfer: the factorial on latent prediction
  shows whether the sign effect carries over).
- **Late August: consolidate and write the workshop paper** (NeurIPS NeuroAI, 29
  August): the sign-primary robustness finding, its cross-connectome generality,
  and its transfer (or not) to latent prediction.
- **Thesis, first week September.** Results and discussion on the existing
  Chapters 1 to 4 scaffold; introduction reframed around the mechanism.
- **ICLR 2027, 19 September (post-thesis).** The fuller version, with whatever
  breadth has materialised.

Branch: if transfer is clean and early, spend the remaining time on breadth or
the fly capstone; if marginal, spend it explaining why in the controlled
double-pendulum setting, itself a strong result.

---

## 7. Conference targets

- **NeurIPS NeuroAI Workshop, 29 August.** Primary near-term anchor: a
  neuroscience-grounded substrate result with a mechanistic account (Stage A plus
  cross-connectome generality plus Stage B transfer).
- **ICLR 2027, 19 September (post-thesis).** The fuller two-stage story.

---

## 8. Risks and guardrails

- **Mechanism may not transfer.** A finding, not a failure; the controlled
  double-pendulum setting is where it gets explained rather than merely observed.
- **Open-ended drift.** Mitigated by the single spine question and the gates:
  every Stage B system must earn its place by testing transfer, not by being
  interesting alone.
- **Predictor degeneracy.** The frozen encoder removes the classic collapse mode;
  the residual risk (a mean or persistence readout) is caught by the baselines at
  Gate B0.
- **Write-up compression.** The workshop deadline (29 August) and the thesis
  (first week September) nearly coincide; freeze results early enough to write
  both from one frozen set.
- **Guardrails.** Latent prediction only (no pixel track beyond one motivating
  figure); the encoder is never trained jointly with the reservoir; the fly
  capstone is opt-in from strength and dropped if it pulls time from the spine;
  no experiment is chased past the write-up gates.

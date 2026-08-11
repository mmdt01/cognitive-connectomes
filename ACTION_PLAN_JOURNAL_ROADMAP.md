# Action plan: thesis as journal paper (NMI), with NeuroAI workshop stepping stone

**Status:** v1, drafted 29 July 2026. To be iterated.
**Targets:** NeurIPS NeuroAI workshop (29 Aug, non-archival, 5pp) -> Nature Machine Intelligence.
**Dropped:** ICLR 2027.

---

## 0. Framing decisions

**Core question (unchanged):** which structural and weight properties of biological
connectomes shape the geometry of the reservoir's activity manifold, and how does
that geometry set computational capacity?

**Positioning relative to Suarez 2021.** They established that connectome topology
shapes computation in a fixed reservoir. Three deltas:

1. It is not topology alone. It is the *placement of weights on* the topology
   (the `connectome_weight_permuted` control is the evidence).
2. We give the mechanism: placement -> anomalously compact spectral bulk plus a
   hub-loaded Perron mode -> a two-part manifold decomposition -> capacity.
3. We close the loop back to empirical function: the same decomposition that
   explains the reservoir's computation also organises empirical FC.

Delta 3 is what converts this from a simulation study into a structure-function
study, and it is the difference between a good specialist paper and an NMI paper.

---

## 1. The story: five acts

**Act I - Structure sets the spectrum.** *(restated Aug 2026 — see
`TIER0_STATE_OF_PLAY.md` §3.1)*
Connectome weight placement produces an **anomalously large spectral gap**: the
*absolute* bulk radius is near-identical across variants (4.4% spread) and the entire
difference sits in the Perron root. Headline statistic: the **gap ratio**
`|λ₁| / absolute bulk` = **3.08** for the connectome vs **1.81-1.92** for the nulls
(identically `1/bulk95` = `sr_crit`). Placement, not weight statistics, not topology
alone. Do *not* say "compact bulk" — the bulk is everyone's; the gap is the connectome's.

**Act II - The spectrum decomposes the manifold.**
The Perron mode carries the mean (a common mode); the bulk carries the
fluctuations. Sign gates which basis the fluctuations occupy (W-eigenmodes vs
low-frequency graph harmonics). `sigma_eff = bulk95 * sr * mean_gain` crossing 1
marks where the geometry leaves the faithful regime.

**Act III - Manifold geometry sets computational capacity.**
Two dissociable readouts with opposite sr-dependence: effective dimensionality of
the fluctuation subspace sets memory; the faithful-geometry window sets closed-loop
generation. The compact bulk widens the usable window rather than raising a peak
("most robust, not best").

**Act IV - Where the sign axis is biologically real.**
Macro dMRI connectome is non-negative by construction, so it sits at f=0 and the
sweep on it is a mechanistic counterfactual. C. elegans has real Dale signs, so the
~20% tolerance ceiling is an anatomical claim only there. Being explicit about this
turns the field's standard objection into a scale-precision result.

**Act V - The same decomposition organises empirical function.** *(the closer)*
Common-mode removal is not a modelling convenience. Removing the reservoir's Perron
mode should reveal Yeo-network structure in the simulated FC, mirroring what global
signal regression does to empirical fMRI. If it holds, the mechanism is validated
against real functional data.

---

## 2. Experiments

### Tier 0 - gating reanalyses (no new runs; ~2-3 days)

These decide what the story can claim. Do them first.

| id | experiment | decides |
|----|-----------|---------|
| E0.1 | **Mediation test.** Partial correlation of Lorenz VPT and curvature controlling for `sigma_eff`; or the same within narrow `sigma_eff` bands. | Whether curvature is a cause or a symptom. Gates all straightness language in Acts III and V. |
| E0.2 | **Effective-criticality-matched Panel A.** Recompute dD indexed by `sigma_eff` (or `sr * bulk95`) instead of nominal sr. | Whether the memory wedge survives correct normalisation. Gates Act III's memory arm. |
| E0.3 | **Absolute (MC, VPT) frontier.** Within-substrate absolute values across the (f, sr) grid, not differences from ER. | Whether there is an achievable trade-off frontier or only a resistance margin. Fixes the language throughout. |
| E0.4 | **Eigenvalue distribution figure.** Plot the real connectome's spectrum from `w_spectra` `eig_w_real`, alongside nulls and weight-permuted. | Act I currently asserts what it should show. This is Figure 1. |

### Tier 1 - the closer (~2 weeks, the highest-value new work)

**E1: Does common-mode removal recover empirical functional network structure?**

Design:
- Drive the connectome reservoir (f=0, non-negative, real anatomy) with noise input.
- Compute simulated FC = state correlation matrix.
- Compare to empirical FC: (a) edge-wise correlation, (b) within- vs between-Yeo-network
  contrast (system segregation), (c) whether Yeo assignments are recoverable by
  clustering simulated FC.
- **Key manipulation:** with vs without common-mode (Perron) removal. Prediction:
  with the common mode in, simulated FC is dominated by one global factor and Yeo
  block structure is weak; after removal, it emerges.
- **Null ladder:** the same across all five rungs. If ER also recovers Yeo structure,
  the result is trivial and must be reported as such.
- **sr sweep:** does the structure-function match peak near `sr_crit`? A peak at the
  edge of the faithful regime would connect Act V back to Act III.

Sub-analysis (cheap, potentially striking): **which Yeo networks load the Perron mode?**
The common mode is hub-localised; if its loading concentrates on specific intrinsic
networks, that is a concrete, quotable result and a direct answer to a sceptic asking
what any of this says about brains.

**Scope discipline.** Predicting FC from SC is a large, mature field (Honey 2009,
Hansen 2015, Deco, Messe). We are *not* claiming a better FC predictor, and simulated-
to-empirical correlations in this literature sit around r = 0.3-0.5, so do not expect
or claim more. The claim is narrower and sharper: the *same spectral decomposition*
that explains computational capacity also explains the FC structure, and the common
mode is the global-signal analogue. The mechanism link is the novelty.

**E1.5: Mackey-Glass as an out-of-sample test of the two-controller model.**

Not a third benchmark. A prediction test. MC and Lorenz sit at opposite ends of the
dissociation: MC needs memory and no rollout, Lorenz needs rollout and (being
Markovian in its 3-D state) little memory. **Mackey-Glass is a delay system, so
closed-loop rollout requires holding the state at lag tau.** It needs both capacities
at once, which makes it the task the two-controller model should be able to predict.

Protocol:
1. Fit the two controllers on existing MC and Lorenz data (common mode -> memory;
   `sigma_eff` -> generation).
2. **Predict, before running, where in the (f, sr) grid MG performance should peak.**
   The prediction is an interior optimum, unlike MC (edge) and Lorenz (f=0).
3. Run MG on the same grid. Compare.
4. **Vary tau (e.g. 17 and 30) as a dial on the task's memory demand.** The model
   predicts the optimum shifts toward the memory-favouring region as tau grows.

Step 4 is the payoff: a dose-response curve for the theory. It turns Act III from a
description of two axes into a model that predicts task performance on a task it was
not fitted to, which is rare in this literature and is the strongest single thing you
could add.

Watch for ceiling effects — MG is famously easy for reservoirs at short horizons, so
use closed-loop rollout with a horizon long enough to separate conditions.

### Tier 2 - completing the existing programme (parallel, cluster)

- **E2.1 N=1000.** Finite-size check on the memory ceiling. **Pre-flight changes
  required before launching — see below.** Launch early and let it run.
- **E2.2 C. elegans Dale arm.** Real neurotransmitter signs. Makes Act IV an anatomical
  claim rather than a counterfactual.

### Tier 3 - journal only, if time allows

- **E3.1** Why does connectome weight placement produce a compact bulk? The open
  mechanistic question a reviewer will certainly ask. Even a partial answer
  (degree-weight correlation? spatial embedding? rich-club?) is worth a paragraph.
- **E3.2** Additional geometry measures (intrinsic dimensionality, tangling) if
  curvature proves too coarse in E0.1.

---

## 2b. N=1000 pre-flight (do not launch without these)

The infrastructure already supports it (`--scale {448,1000}`), but the frozen MC
hyperparameters were pinned at N=448 and two of them break the comparison at N=1000.

0. **Run E0.4 then E0.2 first.** E0.2 gates this experiment twice over: if the memory
   wedge does not survive effective-criticality matching at N=448, the finite-size
   question is the wrong one to ask, and even if it does survive, the wedge may sit in
   a different band in `sigma_eff` coordinates than in nominal sr — which sets the grid
   in item 5 below. Do not launch before E0.2 reports.
1. **Raise T to preserve the T/N ratio.** MC is pinned at `T=3000, warmup=500`, so
   `T_eff = 2500` and `T_eff/N = 5.6` at N=448. At N=1000 that falls to **2.5**. The
   design Gram is a *sample* covariance, and its small-eigenvalue tail — precisely the
   directions `d_eff` counts — is the part most distorted by finite T/N
   (Marchenko-Pastur spreading). d_eff at ratio 2.5 is not comparable to d_eff at
   ratio 5.6. Set `T = 6000, warmup = 500` (`T_eff = 5500`, ratio 5.5).
2. **Rescale the ridge.** `ridge=1e-6` is absolute, and `trace(G)` scales with T, so
   doubling T halves the effective regularisation and pushes d_eff toward the ceiling
   for free. Scale alpha with T_eff, or better, reparameterise as
   `alpha = lambda * trace(G) / N` and pin lambda to reproduce the N=448 value.
3. **Re-run N=448 under the new T and alpha first.** MC is ~2 min at N=448, so this is
   nearly free, and without it a null result at N=1000 is uninterpretable — you would
   not know whether the wedge closed because the ceiling lifted or because the protocol
   changed. This is the control that makes the whole experiment readable.
4. **Recompute `bulk95` at N=1000 before the sweep.** One eigendecomposition of W, no
   reservoir runs. `sr_crit = 1/bulk95` was 3.08 at N=448 and will differ under a
   different parcellation. The wedge lives supercritically, so the sr grid must cover
   the right region — and E0.2 needs this number anyway.
5. **Scope the run to the question.** Do not reproduce the full 7-variant x 58-sr x
   3-condition x 10-seed matrix. The question is narrow: does the memory wedge survive
   the ceiling? So MC only (not Lorenz, NARMA or MG), {connectome, weight-permuted,
   degree, ER}, low-f only, sr restricted to the supercritical wedge region. A few
   percent of the full grid.
6. **Do not persist states.** d_eff needs only the Gram eigenvalues (N floats per
   cell), not the `(T_eff, N)` state matrix (44 MB per cell at N=1000 in float64).
   Confirm the `collect_states` hook is off for this run.
7. **Regenerate the nulls at N=1000** with matched density and degree sequence, and
   check the degree-preserving rewire actually converges at the N=1000 density.
8. **Report `d_eff / N` alongside `d_eff`,** and plot distance-from-ceiling explicitly.
   Absolute d_eff is not comparable across N; the ceiling is the whole point.

**Compute note.** Lorenz went ~7 min at N=448 to ~90 min at N=1000, roughly 13x. MC is
cheaper (open loop) but scales the same way, and doubling T doubles it again. Time a
single cell before launching the sweep. Only consider porting the eigendecompositions
to the idle L40s if that estimate blows the budget — a `cupy.linalg.eigvalsh` swap is
small, but it is not worth the risk speculatively.

---

## 3. Timeline

**Hard constraint: thesis due 9 September, workshop 29 August.** Those are 11 days
apart, which means they cannot be sequential. The workshop paper is carved out of the
thesis draft, not written separately. Working time from return is about 5.5 weeks.

| when | what |
|------|------|
| 30 Jul - 1 Aug | Amsterdam. Nothing. |
| 7 - 8 Aug | E0.4 (eigenspectra + bulk95 at both N) -> E0.2 (criticality-matched Panel A). Cheap N=448 control re-run under new T/alpha alongside. **Then** launch N=1000 with the config E0.2 implies. |
| 9 - 11 Aug | E0.1 (mediation) and E0.3 (absolute frontier) while N=1000 runs. |
| 11 - 18 Aug | E1 (structure-function). Launch C. elegans in parallel if capacity allows. |
| 18 - 20 Aug | E1.5 (Mackey-Glass) — first thing to compress or slip if behind. |
| **20 Aug** | **EXPERIMENT FREEZE.** Anything not producing figures by now does not go in. |
| 20 Aug - 29 Aug | Write. Workshop paper (5pp) extracted from the emerging thesis draft; submit 29 Aug. |
| 29 Aug - 9 Sept | Finish thesis. Submit 9 Sept. |
| Sept - Nov | Post-thesis: C. elegans, Tier 3, then convert to NMI submission. |

**The thesis is a checkpoint, not the paper.** The journal version goes out in
Oct-Nov, so anything that misses 20 August is not lost, it is simply post-thesis work
that strengthens the submission. This is what relieves the pressure: the thesis needs
to be complete and honest, not maximal.

**Non-negotiable:** thesis chapters get drafted as paper sections from the start.
Chapter = Act. The conversion should then be weeks, not a restart.

**Priority order if time runs short** (cut from the bottom):
1. Tier 0 - gates everything, 3 days, non-optional.
2. E1 - the structure-function closer, the NMI delta.
3. E1.5 - Mackey-Glass, the theory test.
4. N=1000 - runs in background, costs attention only at analysis.
5. C. elegans - first candidate to slip to post-thesis.
6. Tier 3 - journal revision, not thesis.

---

## 4. Workshop paper (29 Aug, 5pp)

Content: Acts I-III, with the memory/generation dissociation as the headline and the
Tier 0 corrections already applied. This is the spine of the journal paper, not a
different artefact.

Include Act V only if E1 lands cleanly by ~20 Aug. It would strengthen the workshop
paper considerably and lets you test the structure-function framing on a NeuroAI
audience before committing it to NMI, but the paper must not depend on it.

---

## 5. Open questions for the next iteration

1. **FC data specifics.** How many subjects; group-average or individual-level; same
   parcellation and N as the SC (448 / 1000)? Critically: **was global signal
   regression applied during preprocessing?** If yes, the empirical FC is already
   common-mode-removed and E1's comparison is cleaner but the manipulation changes
   shape. This determines the whole design of E1.
2. **Which input drive for E1?** Noise input is the standard choice for resting-state
   comparison, but the task-driven states are what all other results use. Possibly both.
3. Does the workshop paper lead with the dissociation or with structure-function?
4. NMI scope check: is the ML-facing angle strong enough for NMI, or does the paper
   drift toward PLOS CB / Network Neuroscience as it becomes more neuro? Worth
   revisiting once E1 lands.

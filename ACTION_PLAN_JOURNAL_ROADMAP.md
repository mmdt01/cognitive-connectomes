# Action plan: thesis as journal paper (NMI), with NeuroAI workshop stepping stone

**Last revised:** 13 August 2026.
**Targets:** NeurIPS NeuroAI workshop (29 Aug, non-archival, 5pp) -> Nature Machine Intelligence.
**Not pursuing:** ICLR 2027.

**Division of labour between documents.** `TIER0_STATE_OF_PLAY.md` is canonical for
*results*: every number, every withdrawal, every artifact trail. This document is
canonical for *plan and narrative*: what the contribution is, how the thesis is
structured, what is still to be done and in what order. Where they overlap on a number,
`TIER0_STATE_OF_PLAY.md` wins.

---

## 1. The contribution

**One sentence.** Biological weight placement buys a large spectral gap rather than a
compact bulk; non-negativity pins every substrate to a dominant common mode that costs
memory and protects generation, so the same axis is read out with opposite sign by the
two capacities, and the connectome's gap makes it the substrate least dominated by that
mode. The trade is invisible under the field's standard spectral-radius-matched
comparison.

**The biological claim that makes it computational neuroscience.** The connectome is not
organised for capacity. It is organised for not needing to be tuned.

### The contributions, in the order they should appear in the introduction

1. **The spectral difference is a gap, not a bulk.** The absolute bulk radius is
   near-identical across variants (4.4% spread); the entire between-variant difference
   sits in `|λ₁|`. Gap ratio `|λ₁|/abs_bulk` = 3.08 (connectome) vs 1.81 to 1.92 (nulls),
   identically `1/bulk95` = `sr_crit`. Identifies weight-topology alignment as the causal
   structural feature. Scale-robust. *(Act I)*

2. **The memory/generation dissociation is one axis read out with opposite sign, not two
   controllers** (`TIER0` §3.9). Each unit is `x -> tanh(gain·x + input)`: gain above +1
   gives a stable fixed point, below -1 a period-2 orbit, nothing stable between.
   Perron-Frobenius pins a non-negative matrix to the positive branch, which wastes
   readout dimensions (bad for memory) and holds the trajectory smooth (good for
   generation). That is *why* the two advantages had to occupy opposite regions of
   (f, sigma), rather than a fact reported about them. The boundaries cross at
   (`sigma·bulk95` = 2.938, f = 0.153) on the matched-bulk axis and not at all on the
   nominal axis past sigma = 6, so **the crossing is only ever quoted with its axis**.
   *(Act III, unifying section)*

3. **The memory advantage is a rescue from Perron domination, not a capacity gain**
   (`TIER0` §3.7). The connectome is the *least* common-mode dominated substrate despite
   the largest Perron root (`|mean_state|` 0.759 vs nulls 0.949 to 0.989 at sigma = 6,
   f = 0), because a large gap lets the leading mode be driven without the bulk following.
   Peak memory is 2 to 6% *below* the nulls — reliable against ER and weight-permuted,
   **not** against degree-matching, so write "parity", never "always worst" (`TIER0`
   §3.4). The supercritical margin is 4.4x and holds across a 2.2x change in N
   (ratio 4.40 -> 4.42) while the normalised advantage grows (`dD/N` 0.445 -> 0.613).
   Nobody degrades with f: supercritical MC rises for every substrate and the advantage
   narrows because the nulls gain ~4x what the connectome gains from a much lower start.
   **This also reconciles the spread-versus-compact disagreement** (Aceituno, Yan & Liu): their ordering reproduces exactly at
   alpha = 1e-8 on our substrates, so spread wins at the peak and compact wins across the
   range. Defensible one-liner: the connectome does not make memory better, non-negativity
   makes it worse for everyone, and the connectome's gap makes it least worse.
   *(Act III, memory arm; the reconciliation is the closing section and the paper's hook)*

4. **The generative advantage is present at the biologically real cut, and capacity there
   is gated rather than graded.** Read as VPT the connectome is the only substrate still
   predicting from f ~ 0.20 (+1.0 to +2.2 Lyapunov times over all three nulls, clearing
   the weight-permuted placement control, so it is a *placement* effect). At f = 0 the
   resistance margin is real but far supercritical: ER collapses in 5 of 10 seeds at
   sigma ~ 7.6 to 8, the connectome in 0 of 10 (Fisher p = 0.033). The earlier
   "onset in f" reading was an artifact of stopping the sweep at sigma = 6. And the
   relationship is a **switch**, not a dose: curvature is bimodal (98% of cells in two
   spikes, 0.56% between), so a binary collapsed-or-not bit explains R2 = 0.364 of VPT
   against continuous curvature's 0.371. **Scope limit stated up front** (`TIER0` §3.11):
   this holds at f > 0. At f = 0 curvature is flat at 0.26 across the whole sweep while
   VPT falls ~10x, so what sets generation there is open. *(Act III, prediction arm)*

5. **Spectral-radius-matched comparison is not neutral.** Normalising `W` by `|λ₁|`
   anchors the nominal-sigma axis to an extreme-value statistic that does not concentrate
   (Hill alpha ~ 2.3). Since variants differ *only* in `|λ₁|`, nominal matching fixes the
   Perron root and `sigma·bulk95` matching fixes the bulk, and the memory mechanism under
   test *is* the Perron mode, so each axis flatters a different answer. Report both, say
   what each holds fixed, rest the claim on surviving both. Applies to the whole
   connectome-reservoir literature, not just to this work. *(Chapter 3, methods)*

6. **Variance-weighted dimensionality misses readout-relevant structure.** PR orders the
   memory ladder at +0.11; `d_eff` at +0.998, because memory lives in roughly 400
   low-variance directions PR discounts. Pitch as an empirical demonstration (Dambre 2012
   is the parent bound; Clark 2025 collides on terminology). *(Act II)*

### What must NOT be claimed

- Connectome reservoirs as a field are Suarez's, not ours.
- Sign-gating of the manifold transition is largely pre-empted by Krauss 2019. Present
  as confirmatory.
- Hub-gating of memory is a solid empirical result whose proposed mechanism was
  falsified (non-normality, `TIER0` §3.5). Report without a mechanistic story attached.
- **"Hub inhibition collapses memory."** Nothing collapses (`TIER0` §3.8): inhibiting the
  connectome's hubs *raises* its own absolute memory, most of any placement. The advantage
  narrows because ER gains +8.5 against the connectome's +3.4. The ordering is real; the
  collapse is the null moving.
- **"`sigma_eff` crosses 1 at the generative transition."** Falsified (`TIER0` §3.10): 1 of
  38 brackets contains 1, the transition sits at 0.77 to 0.90, and `sigma_eff` cannot reach
  1 at all for f <= 0.20 while transitions happen throughout. It survives as the best
  empirical **locator** (CV 0.209 against nominal sigma's 0.667) with a variant-dependent
  offset ordered by spectral gap. Write "locator", never "criterion" or "law".
- **A graded straightness account of generation.** Within the straight cluster the residual
  VPT/curvature correlation is +0.145, the *opposite* sign to the graded story. The pooled
  -0.78 was cluster mixing.
- **That the single-axis account explains generation at f = 0.** It demonstrably does not
  (contribution 4). Name it as an open problem in the discussion rather than letting the
  f > 0 mechanism read as general.
- **The crossing, quoted without its axis.** It is at (2.938, 0.153) on `sigma·bulk95` and
  absent on the nominal axis once the sweep passes sigma = 6.
- "The connectome is a better reservoir." It is not, at the peak, and the data says so.

---

## 2. The narrative spine: four acts

Acts I to III are a causal chain: each act's output is the next act's input. Act IV is
not the next link; it is an **anchor**, and it is conditional.

**Act I: structure sets the spectrum.**
Connectome weight placement produces an anomalously large spectral gap. Placement, not
weight statistics, not topology alone (the `connectome_weight_permuted` control is the
evidence). Do not write "compact bulk".

**Act II: the spectrum decomposes the manifold.**
The Perron mode carries the mean (a common mode); the bulk carries the fluctuations.
Sign gates which basis the fluctuations occupy. `sigma_eff = bulk95·sigma·mean_gain`
**locates** where the geometry leaves the faithful regime — best of the candidates tested,
~3x more invariant than nominal sigma — but it does **not** cross 1 there: the transition
sits at 0.77 to 0.90, and `sigma_eff` folds so it never reaches 1 at all for f <= 0.20
(`TIER0` §3.10, §6.3). Lorenz-driven states only. Write "locator", never "criterion".

**Act III: manifold geometry sets computational capacity.**
**One axis, read out with opposite sign** (`TIER0` §3.9) — not two controllers. Where the
leading effective gain sits relative to +/-1 decides both: a dominant positive mode wastes
the readout dimensions memory needs while holding the trajectory on a smooth fixed point
that generation needs, so effective dimensionality of the fluctuation subspace sets memory
and the faithful-geometry window sets closed-loop generation *from the same cause*. That is
why the two advantages occupy opposite regions of (f, sigma). The gap widens the usable
window rather than raising a peak. **Both arms
carry equal weight in this chapter.** The sign-axis scale argument (macro dMRI is
non-negative by construction, so f > 0 is a mechanistic counterfactual; C. elegans is
where it would be anatomical) lives here as a framing section.

**Act IV: the same decomposition organises empirical function.** *(anchor, conditional)*
Everything in Acts I to III is simulation on a substrate derived from brain data. Act IV
is the only place simulated dynamics meet measured dynamics. It answers "why should
anyone believe the manifold you characterised has anything to do with brains", which is
exactly what a sceptical computational neuroscientist asks. Nothing in Acts I to III
depends on it.

---

## 3. Thesis chapter mapping

Chapter = act, drafted as paper sections from the start. **The introduction gives away
the answer in the first two pages.** Examiners read the introduction and conclusion
carefully and skim the middle; the contribution must survive that reading pattern.

| ch | title | content | status |
|----|-------|---------|--------|
| 1 | Introduction | Question; the five contributions as a numbered list; the "not organised for capacity" sentence | to write |
| 2 | Background | Connectome reservoirs (Suarez); chaotic-attractor RC (Pathak, Lu, Hunt, Ott, Hart) even though not pursued; memory bounds (Dambre); spectral structure and memory (Aceituno; Rajan-Abbott; Landau & Sompolinsky); E/I structure (Cornford, Li, Srinivasan); neural manifolds (Sadtler, Feulner, Henaff). Name the two competitor papers explicitly | adapt from interim report |
| 3 | Methods and the comparison problem | Substrates, null ladder, tasks, measures. **Then the two-axis argument as a methods result**: `sigma·W/|λ₁|` has spectral radius exactly sigma, so nominal matching fixes the Perron root and `sigma·bulk95` fixes the bulk. Close on "we therefore report both throughout" | mostly written, needs the two-axis section |
| 4 | Act I: structure sets the spectrum | Gap-ratio decomposition; E0.4; scale robustness; the `|λ₁|/abs_bulk = 1/bulk95 = sr_crit` identity; extreme-value forensics on `|λ₁|` | results in hand |
| 5 | Act II: spectrum decomposes the manifold | Probes 1 and 2; Perron as common mode; time-centring; basis inversion; PR versus `d_eff` | results in hand |
| 6 | Act III: geometry sets capacity | **Memory arm:** E0.2, Tasks A and B, N=1000 scaling, the crossing table as lead figure, peak parity with CIs, hub-gating. **Prediction arm:** curvature onset, resistance margin, ~20% tolerance ceiling, `effective_radius` predictor, E0.1 mediation, E0.3 frontier. **Closing section:** the Aceituno reconciliation | memory complete; prediction arm pending |
| 7 | Act IV: structure recovers function | Common-mode removal against Yeo-partitioned empirical FC | conditional |
| 8 | Discussion | The biological argument; limits from `TIER0` §6; future work (C. elegans, Mackey-Glass, trained networks) | to write |

**Negative results are load-bearing and get figures.** Place them where the claim they
bound is made, not in an appendix: the crossing not surviving goes in Act III beside the
dissociation; non-normality failing to explain hub-gating goes beside hub-gating; peak
parity with its CIs goes beside the trade-off. A thesis that shows three of its own
hypotheses dying reads as more trustworthy, not less.

---

## 4. Work remaining

### 4a. Reanalyses — complete (12 Aug)

The `f > 0` extension, E0.1 and E0.3 all landed. Outcomes are in
`TIER0_STATE_OF_PLAY.md` §2.3, §2.6, §3.7, §3.8, §3.10 and §3.11, and the E0.1
pre-registration record — the prediction as it stood before fitting, against a value that
was then falsified — is held in §3.10; the claims they license are in §1 above. Two items survive into the writing phase:

- **Bridge paragraph (nearly free).** NARMA-10 sits between pure memory and pure
  prediction, and both `d_eff` and PR order the ladder on it. One paragraph showing the
  trade-off varies continuously across MC -> NARMA -> Lorenz strengthens Act III at almost
  no cost.
- **Presentation rule for the crossing.** Quote it as (`sigma·bulk95` = 2.938, f = 0.153)
  with the axis named, and state that it does not survive on the nominal axis once the
  sweep passes sigma = 6. The contour level is taken over fully covered cells; the raw
  global max is set by a cell backed by 1 replicate of 30, and that convention gives no
  crossing at all.

### 4b. The front-to-back sweep (13 to 20 Aug)

A single front-to-back pass through Acts I to III doing five things at once: crystallise
the narrative, audit the code behind each claim, collect the full task set so no large run
is needed near the deadline, produce publication-ready figures, and outline the chapters.
Run as **five Claude Code sessions**, sequential (Act I's restatement propagates
downstream), each starting from `report/CONVENTIONS.md`.

| session | scope | output |
|---|---|---|
| **0** | Figure list, style contract, claim-to-task mapping, MG pre-registration | `report/FIGURE_LIST.md`, `report/CONVENTIONS.md`, `report/PREREG_MACKEY_GLASS.md` |
| **1** | Act I: structure sets the spectrum | `report/act1_structure.md` + its figures |
| **2** | Act II: spectrum decomposes the manifold | `report/act2_manifold.md` + its figures |
| **3** | Act III memory arm | `report/act3a_memory.md` + its figures |
| **4** | Act III prediction arm | `report/act3b_prediction.md` + its figures |

Act III is split because contributions 2, 3 and 4 all live there; it is roughly half the
thesis and one session will exhaust its context.

**Session 0 is not optional and comes first.** If each act session picks its own figures
the chapters will not sit together, cross-act figures (the crossing needs both arms) have
no owner, and the count drifts past twenty. Half a day, fixing: the master figure list
(cap 15, each with a chapter, a claim, a data source and a caption sketch, with the
workshop subset marked); the style contract (one colour per variant held across every
figure, fonts, panel labels, dpi, output paths); and the two pre-commitments below.

> **The cap was 14 and was raised to 15 in session 0, once.** The draft list left
> contribution 2 without a figure, on the reasoning that the memory and prediction
> figures carry it jointly; they do not, since each is a 1-D slice and the claim is that
> the two advantage regions occupy opposite regions of the (f, sigma) plane. F16 (the two
> phase boundaries on both axes, with the replicate-coverage mask drawn) was added for
> it. `report/FIGURE_LIST.md` is canonical for the count.

#### The audit is claim-driven, not a code review

For each act, a **reproduction gate** before any figure work: recompute that act's
headline numbers from the frozen artifacts and check them against `TIER0` to a stated
precision. Then read only the functions those claims depend on:

| act | functions under audit |
|---|---|
| I | `bulk95` computation, the `\|lambda_1\|` normalisation, null generation and its assertions |
| II | time-centring, Gram construction, `participation_ratio`, `ridge_effective_rank` |
| III-memory | MC evaluator, ridge `alpha` reparameterisation, `d_eff` at both scales |
| III-prediction | VPT definition and horizon, `mean_curvature`, closed-loop rollout, `sigma_eff` |

**A failed reproduction is the finding and it stops the act.** Do not paper over a
mismatch by regenerating the artifact.

#### Task collection policy: collect everything, decide later

**Every run in this sweep uses all four tasks (MC, NARMA-10, Mackey-Glass, Lorenz)**, so
the data is banked and no large run is needed near the deadline. Final figures need not
use all four; that is a write-up decision. Marginal cost is small (the `f > 0` extension
was 14.5 core-hours for two tasks), and the cost of needing a run on 4 September is not.

Three conditions attach:

1. **Pre-register Mackey-Glass before running it** (`report/PREREG_MACKEY_GLASS.md`,
   written and committed in session 0). **Revised in session 0**: MG as the out-of-sample
   test of contribution 2 required a *closed-loop* rollout, and the implemented task is
   teacher-forced. Under teacher-forcing the reservoir never sees its own prediction, so
   the regime switch cannot affect the metric and the interior-optimum prediction is
   untestable in both directions. MG is therefore **a corroborating memory-side task
   beside NARMA-10**, carrying a narrower registered prediction: the connectome's paired
   NRMSE advantage is largest at f = 0 and closes with f (the §2.6 shape, transferred to a
   task it was not fitted to). Both horizons are collected; **h = 300 is the pre-declared
   primary and is not swappable after the data is seen**. A horizon dose-response was
   registered and withdrawn the same day — it is confirmable by a ceiling artifact at
   h = 84, which is the fourth instance of the delta-without-levels failure this project
   has already been caught by three times. Closed-loop MG is deferred to §5. It is still
   worth nothing if the MG data is inspected first.
2. **Declare the primary task per claim in session 0.** MC is primary for memory, Lorenz
   for generation, NARMA and MG are corroboration. With four tasks and two axes there is
   always a task where any claim holds; this project has already been caught **three
   times** by a difference that moved because a null moved. Declaring the mapping in advance closes the
   forking-paths objection at zero cost.
3. **Persist Gram eigenvalue spectra, never states.** A per-cell Gram spectrum is N floats
   (~4 KB) and yields `d_eff` at *any* alpha forever; states are 10 to 44 MB per cell and a
   four-task grid would run to hundreds of gigabytes. Extend the `covariance_spectra.parquet`
   pattern to all four tasks. Curvature and PR cannot be recovered from the spectrum, so
   **decide in session 0 which manifold measures are computed inline for NARMA and MG** —
   that is the one thing a re-run would be needed for.

**The audit budget does not scale with tasks.** Reproduction gates run on the primary task
per act only. For NARMA and MG, validate integrity (runs completed, no NaNs, all seeds
present, hyperparameters recorded) and stop. If the audit scales, the freeze slips and the
point of collecting early is lost.

#### Scope rules

- **A run happens only if a figure on the list needs it.** Everything else goes to §5.
  Exception: the four-task collection above, which is banked deliberately.
- **No figure is created that is not on the list.** If a session thinks one is missing, it
  reports and stops rather than adding it.
- **Write the caption first.** If the caption cannot be written defensibly against
  `TIER0_STATE_OF_PLAY.md`, the figure should not exist in that form. This is the fastest
  test for figures that encode withdrawn claims, and there is no inventory of which ones
  do: anything predating 8 August may still show the subcritical deficit as real, "compact
  bulk" as the structural story, `sr_crit` on the old per-seed convention, or memory as
  capacity rather than robustness.
- **Regenerate from a module, not by hand.** One figure module reading the frozen parquets,
  so that when a number moves every affected figure rebuilds.

#### The `report/` folder

Claims-first, not prose-first. Each act file carries a **claims register** (numbered claim
-> figure ID -> `TIER0` section -> artifact path), then figure specs with captions, then a
section outline, then an audit log and open issues. The chapter falls out of the register,
every claim has a figure and a source, and drift is visible.

> **On drafting.** Claim registers, figure captions, audit logs and section outlines are
> the right use of these sessions. Connected chapter prose is not: check Imperial's
> position on generative AI in assessed work before going further than an outline, and
> note that prose generated from a register reads flat and would be rewritten anyway.
> Writing the chapters is also what delivers the first goal of this sweep.

**Minimal Act IV** (which Yeo networks load the Perron mode) is one entry on the master
figure list, not a session.

### 4c. Act IV, full version (29 Aug to 3 Sept window only)

**Runs only if the thesis draft is genuinely on track after the workshop is submitted.**

Design (from v1, unchanged):
- Drive the connectome reservoir (f = 0, non-negative, real anatomy) with noise input.
- Simulated FC = state correlation matrix.
- Compare to empirical FC: edge-wise correlation; within- versus between-Yeo-network
  contrast; whether Yeo assignments are recoverable by clustering simulated FC.
- **Key manipulation:** with versus without common-mode (Perron) removal. Prediction:
  with the common mode in, simulated FC is dominated by one global factor and Yeo block
  structure is weak; after removal it emerges.
- **Null ladder across all rungs.** If ER also recovers Yeo structure, the result is
  trivial and must be reported as such.
- **sigma sweep:** does the match peak near `sr_crit`? A peak at the edge of the faithful
  regime connects Act IV back to Act III.

**Scope discipline.** Predicting FC from SC is a large mature field (Honey 2009, Hansen
2015, Deco, Messe) where simulated-to-empirical correlations sit around r = 0.3 to 0.5.
We are not claiming a better FC predictor and must not appear to. The claim is narrower:
the *same spectral decomposition* that explains computational capacity also explains FC
structure, and the common mode is the global-signal analogue.

**Blocking question to answer first:** was global signal regression applied during
preprocessing of the empirical FC? If yes, it is already common-mode-removed and the
manipulation changes shape. This determines the whole design.

> **PRE-COMMITTED STOPPING RULE: if the full Act IV has not produced a result by
> 3 September, it becomes a future-work paragraph.** Write this down now; it will be
> needed when it is 2 September, it nearly works, and you are tired.

---

## 5. Deferred to post-thesis (explicitly, not by omission)

The thesis is a checkpoint, not the paper. The journal version goes out in October or
November, so nothing here is lost.

- **C. elegans Dale arm.** New substrate, new pipeline, new sign conventions. Cannot be
  done well in a week alongside writing, and the macro story does not need it because the
  sign axis is already framed as a counterfactual at f = 0. One deferring sentence in the
  discussion is the right treatment.
- **Closed-loop Mackey-Glass** as the out-of-sample test of contribution 2. **Withdrawn
  from the thesis in session 0, on design grounds, before any MG data was inspected.** The
  implemented MG task is teacher-forced, so the reservoir is re-anchored by the true input
  at every step and the regime switch has no consequence for the metric — which makes both
  branches of the interior-optimum prediction uninterpretable rather than merely hard to
  detect. Testing it needs a rollout that feeds the prediction back (~150 to 250 lines
  mirroring the Lorenz protocol, plus a null-tuned hyperparameter check and ~23 core-hours).
  Full reasoning preserved in `report/PREREG_MACKEY_GLASS.md` §1.1.
  **Consequence to state plainly in the discussion: contribution 2 has no out-of-sample
  test in this thesis.** The driven MG data *is* still collected in §4b and carries a
  narrower registered prediction on the memory side, but it does not fill that gap.
- **Why weight placement produces the gap** (degree-weight correlation? spatial
  embedding? rich-club? Landau & Sompolinsky 2018 the likely source). The open
  mechanistic question a reviewer will certainly ask.
- **What sets generation at f = 0** (`TIER0` §3.11). At the biologically real cut,
  prediction decays ~10x with the trajectory geometry completely flat, so the geometric
  gating account does not apply there — and neither does memory (the connectome has ~4.7x
  ER's MC at sigma = 6 and slightly *lower* VPT). Currently unexplained, and it is the
  regime the thesis actually claims to be about.
- **The closed-loop Jacobian.** Generation feeds the readout back, so the operative map is
  `x -> tanh((W + Win*W_out)x)`; every stability quantity computed so far omits that
  rank-3 term, which is the most likely reason both `sigma_eff` and the exact reservoir
  Jacobian fire *early* (at 67% and 85% of their critical values). Needs the evaluator to
  expose `W_out`.
- **Additional geometry measures** (intrinsic dimensionality, tangling) if curvature
  proves too coarse.
- **The `bulk95`-as-ladder-controller question.** Do not run more seeds. Restate at the
  resolution the data supports: `bulk95` orders connectome against nulls robustly at both
  scales (~40% separation); it does not resolve fine distinctions among nulls, where the
  degree/ER separation is itself within noise (p = 0.16). The Spearman dropping 1.00 to
  0.80 is then expected rather than damaging. One free strengthening if the MC data
  exists: check whether `bulk95` predicts MC across all seven E0.4 variants rather than
  the four-rung ladder.

---

## 6. Timeline

| when | what |
|------|------|
| 11 to 15 Aug | Reanalyses 1 to 3 (`f > 0` extension, E0.1, E0.3) |
| 13 to 20 Aug | Front-to-back sweep, sessions 0 to 4 (§4b): figure list and pre-registrations, then Acts I, II, III-memory, III-prediction. All runs collect the full four-task set. Minimal Act IV (Yeo loading) folded in as one figure |
| **20 Aug** | **EXPERIMENT FREEZE.** Anything not producing figures by now does not go in |
| 20 to 29 Aug | Workshop paper (5pp) assembled from swept figures; submit 29 Aug |
| 29 Aug to 3 Sept | Act IV full version, if and only if the thesis draft is on track |
| **3 Sept** | **ACT IV CUTOFF.** Becomes future work if no result |
| 3 to 9 Sept | Finish thesis. Submit 9 Sept |
| Sept to Nov | Post-thesis: Mackey-Glass, C. elegans, mechanism of the gap, then convert to NMI |

**Priority order if time runs short (cut from the bottom):**

1. Reanalyses 1 to 3. They rebalance Act III and gate its language. Non-optional.
2. Figure sweep. Non-optional: it is a correctness audit, not polish.
3. Workshop paper.
4. Act IV minimal (Yeo loading).
5. Act IV full.
6. Everything in §5.

---

## 7. Workshop paper (29 Aug, 5pp)

**Acts I to III, with the trade-off as the headline.** Lead with the gap ratio, then the
supercritical robustness margin, then the Aceituno reconciliation as the hook: our
substrate loses at the thing the field optimises for, and here is why that is the wrong
thing to optimise for a brain.

**This paper does not depend on Act IV.** It can be drafted starting now, in parallel
with Act IV running. If Act IV lands cleanly it strengthens the workshop considerably and
lets the structure-function framing be tested on a NeuroAI audience before committing it
to NMI. If it does not, nothing is lost that was already committed to print.

---

## 8. Open questions

1. **FC data specifics** (blocking for Act IV): how many subjects; group-average or
   individual-level; same parcellation and N as the SC (448 / 1000); and critically, was
   global signal regression applied?
2. **Which input drive for Act IV?** Noise is standard for resting-state comparison, but
   task-driven states are what every other result uses. Possibly both.
3. **NMI scope check.** Is the ML-facing angle strong enough for NMI, or does the paper
   drift toward PLOS CB / Network Neuroscience as it becomes more neuro? Contribution 4
   (the methodological critique) and contribution 5 (dimensionality measures) are the two
   most ML-facing; if they carry weight in the final draft, NMI holds. Revisit once Act IV
   resolves.

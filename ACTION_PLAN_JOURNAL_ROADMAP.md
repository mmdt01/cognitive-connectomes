# Action plan: thesis as journal paper (NMI), with NeuroAI workshop stepping stone

**Status:** v2, revised 11 August 2026 (v1 drafted 29 July, archived as
`ACTION_PLAN_JOURNAL_ROADMAP_v1_superseded.md`).
**Targets:** NeurIPS NeuroAI workshop (29 Aug, non-archival, 5pp) -> Nature Machine Intelligence.
**Dropped:** ICLR 2027.

**Division of labour between documents.** `TIER0_STATE_OF_PLAY.md` is canonical for
*results*: every number, every withdrawal, every artifact trail. This document is
canonical for *plan and narrative*: what the contribution is, how the thesis is
structured, what is still to be done and in what order. Where they overlap on a number,
`TIER0_STATE_OF_PLAY.md` wins.

---

## 0. What changed in v2

1. **Tier 0 is essentially complete** and it reshaped the story. E0.2, E0.4, Task A,
   Task B and the N=1000 run all landed. The supercritical margin scales (4.40 -> 4.42).
2. **Act I is restated.** Not "compact bulk", but "large spectral gap". The absolute
   bulk is everyone's; the Perron root is the connectome's.
3. **The five-act structure collapses to four.** Old Act IV (where the sign axis is
   biologically real) is a framing section, not a chapter, because C. elegans is now
   post-thesis. Old Act V (structure-function) becomes Act IV.
4. **Act III is rebalanced.** Tier 0 drifted almost entirely onto the memory panel
   because every gating question happened to be a memory question. The generation arm
   now gets matched treatment before writing starts. This is the most important change
   in v2.
5. **A figure sweep is scheduled as a work item**, not left to the writing phase.
6. **Act IV is scoped as conditional** with a pre-committed stopping rule.

---

## 1. The contribution

**One sentence.** Biological weight placement buys a large spectral gap rather than a
compact bulk, and that gap trades peak memory capacity for capacity retained across the
operating range: a trade invisible under the field's standard spectral-radius-matched
comparison, and one that reconciles a standing disagreement about whether spread or
compact spectra maximise memory.

**The biological claim that makes it computational neuroscience.** The connectome is not
organised for capacity. It is organised for not needing to be tuned.

### The five contributions, in the order they should appear in the introduction

1. **The spectral difference is a gap, not a bulk.** The absolute bulk radius is
   near-identical across variants (4.4% spread); the entire between-variant difference
   sits in `|λ₁|`. Gap ratio `|λ₁|/abs_bulk` = 3.08 (connectome) vs 1.81 to 1.92 (nulls),
   identically `1/bulk95` = `sr_crit`. Identifies weight-topology alignment as the causal
   structural feature. Scale-robust.
2. **A measured trade-off with a scale-invariant mechanism.** Peak memory 2 to 6% below
   the nulls (reliable against ER, not against degree); supercritical margin 4.4x;
   invariant across a 2.2x change in N while the normalised advantage grows
   (`dD/N` 0.444 -> 0.613).
3. **Reconciliation of the spread-versus-compact disagreement.** Aceituno, Yan & Liu's
   ordering is reproduced exactly at alpha = 1e-8 on our own substrates. Both results
   hold, at different points on the sigma axis. Spread wins at the peak; compact wins
   across the range.
4. **A methodological critique of spectral-radius-matched comparison.** Normalising `W`
   by `|λ₁|` anchors the nominal-sigma axis to an extreme-value statistic that does not
   concentrate (Hill alpha ~ 2.3). Since variants differ *only* in `|λ₁|`, nominal
   matching fixes the Perron root and `sigma·bulk95` matching fixes the bulk. Neither is
   neutral. Applies to the whole connectome-reservoir literature, not just to this work.
5. **Variance-weighted dimensionality misses readout-relevant structure.** PR orders the
   memory ladder at +0.11; `d_eff` at +0.998, because memory lives in roughly 400
   low-variance directions PR discounts. Pitch as an empirical demonstration (Dambre 2012
   is the parent bound; Clark 2025 collides on terminology).

### What must NOT be claimed

- Connectome reservoirs as a field are Suarez's, not ours.
- Sign-gating of the manifold transition is largely pre-empted by Krauss 2019. Present
  as confirmatory.
- Hub-gating of memory is a solid empirical result whose proposed mechanism was
  falsified (non-normality, `TIER0` §3.5). Report without a mechanistic story attached.
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
crossing 1 marks where the geometry leaves the faithful regime (Lorenz-driven states
only, see `TIER0` §6.3).

**Act III: manifold geometry sets computational capacity.**
Two dissociable controllers with opposite sigma-dependence: effective dimensionality of
the fluctuation subspace sets memory; the faithful-geometry window sets closed-loop
generation. The gap widens the usable window rather than raising a peak. **Both arms
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

### 4a. Reanalyses (to ~15 Aug)

**Why these three and no others.** Tier 0 landed almost entirely on the memory panel,
because every gating question was a memory question: E0.2 was the `f = 0` cut, Task A was
`d_eff(alpha)`, Task B was `MC(alpha)`, the N=1000 run was MC-only by the §4.6 handoff.
So memory now has effective-criticality matching, an alpha sweep, paired seed statistics
and a scaling test at two N; generation has none of them. That is a hole in a claim
already being made (a dissociation needs both arms measured comparably), not a gap in
page count.

| id | experiment | why it matters | cost |
|----|-----------|----------------|------|
| **1** | **`f > 0` extension and Panel B reindex.** Run to sigma ~ 11 (x ~ 3.57), not sigma = 8 (x = 2.599), so the extrapolated crossing at x ~ 3.5 is actually observable. Confirm the cost estimate covers Lorenz and curvature, not MC only. Resolve the `TIER0` §2.3 open flag (Panel B negative region at x ~ 1.0, f ~ 0.35 to 0.45) in the same pass | Gives generation the matched axis memory already has; closes `TIER0` §2.3 and §6.1 | ~73 min (re-costed; the original 17 min was 4.3x under) |
| **2** | **E0.1 mediation.** Partial correlation of Lorenz VPT and curvature controlling for `sigma_eff`, or the same within narrow `sigma_eff` bands | Converts the -0.78-pooled / -0.04-within embarrassment into a result. **Licenses "geometry sets predictive capacity" as a chapter claim.** Reanalysis, no new runs | ~1 day |
| **3** | **E0.3 absolute (MC, VPT) frontier.** Within-substrate absolute values across the (f, sigma) grid, not differences from ER | Answers the objection the Aceituno section invites: robust at what level? Preliminary arithmetic is favourable: supercritical MC at N=1000 is 13.93 against a global peak of roughly 14.5 to 15.5, so the connectome's supercritical average is ~90 to 95% of the best any substrate reaches at its own tuned optimum, while ER supercritically is 3.15. If that survives, it belongs in the abstract | ~1 day |

**Stop rule for item 1:** if the crossing appears within the extended coverage, report it
and update the cross-panel headline. If it does not, "dissociation survives, crossing not
observable within the swept range" is final. Mark the coverage limit on the figure and
stop. Do not extend further, do not add sigma points chasing it, do not extrapolate into
a claim.

**Bridge task, nearly free.** NARMA-10 faded because both `d_eff` and PR order the ladder
on it, so it could not discriminate the measures (Probe 3's purpose). That makes it a
useful *bridge*, not a dead end: it sits between pure memory and pure prediction. One
paragraph showing the trade-off varies continuously across MC -> NARMA -> Lorenz
strengthens Act III at almost no cost.

### 4b. Figure sweep (to 20 Aug)

**This is an audit, not tidying.** Figures predating 8 August potentially encode claims
that have since been withdrawn or reversed: the subcritical deficit as a real effect;
"compact bulk" as the structural story; `sr_crit` on the old per-seed convention; memory
framed as capacity rather than robustness; weight-permuted `bulk95` at 0.520 rather than
0.512. A figure carrying a withdrawn claim into the thesis is worse than a missing
figure, and there is currently no inventory of which ones do.

It also de-risks the workshop. Five pages is roughly four figures; if the sweep produces
publication-ready figures with captions, the workshop becomes assembly rather than
production, from material already checked against the canonical record.

**Three disciplines to keep it bounded:**

1. **Fix the figure list before making any figure.** One list, roughly 10 to 12 figures,
   each mapped to a chapter and a claim. Nothing gets built that is not on the list;
   nothing on the list gets beautified twice.
2. **Write the caption first.** If the caption cannot be written defensibly against
   `TIER0_STATE_OF_PLAY.md`, the figure should not exist in that form. Fastest way to
   find figures encoding withdrawn claims: the caption will not write.
3. **Regenerate from a script, not by hand.** One figure module reading the frozen
   parquets, so that when a number moves every affected figure rebuilds. A day's
   investment that pays for itself the first time something shifts.

**Fold the minimal Act IV into the sweep:** which Yeo networks load the Perron mode is
half a day and produces a figure, so it earns a place on the figure list regardless of
whether the full Act IV ever runs.

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
- **E1.5 Mackey-Glass** as an out-of-sample test of the two-controller model (predict the
  interior optimum before running; vary tau = 17 and 30 as a memory-demand dial). This is
  the strongest single addition available and it is the first thing to add post-thesis.
- **Why weight placement produces the gap** (degree-weight correlation? spatial
  embedding? rich-club? Landau & Sompolinsky 2018 the likely source). The open
  mechanistic question a reviewer will certainly ask.
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
| 15 to 20 Aug | Figure sweep: fix the list, write captions, script the module, regenerate. Minimal Act IV (Yeo loading on the Perron mode) folded in |
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

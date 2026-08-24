# Cross-act spine — Acts I to IV

**Written 24 August 2026, after the sign-axis restructure.** This document is the
grounding reference for writing chapters 4 to 7. It is canonical for **narrative
structure only**: what each act claims, what it hands to the next, and where each claim
lives. It is **not** canonical for numbers.

> **Moved to `report/` on 24 August 2026.** It was written at the repository root beside
> `TIER0_STATE_OF_PLAY.md` and `ACTION_PLAN_JOURNAL_ROADMAP.md`, which is where its
> precedence puts it, but **every one of its thirteen consumers is inside `report/`** and
> none of the two root-level canonical documents refers to it at all. It governs the
> chapter structure the `report/` folder is written to, so it now lives with the files it
> governs. Every reference to it is by bare filename or repo-relative path, so nothing
> broke; the canonical path is **`report/CROSS_ACT_SPINE.md`**.

## Precedence

1. `TIER0_STATE_OF_PLAY.md` — every result, number, withdrawal and artifact path.
2. `ACTION_PLAN_JOURNAL_ROADMAP.md` §1 — the six contributions and the withdrawn-claims
   list.
3. **This document** — cross-act structure and the argument each chapter carries.
4. The four act files (`act1_structure.md`, `act2_manifold.md`, `act3a_memory.md`,
   `act3b_prediction.md`) — per-act section detail, claims registers, figure flags.
5. `report/FIGURE_LIST.md` — which figures exist.

Where this document disagrees with `TIER0` on a number, `TIER0` wins. Where it disagrees
with an act file on **section ordering**, this document wins, because the restructure
below post-dates all four act files.

---

## The one-sentence claim

Biological weight placement buys a large spectral gap rather than a compact bulk. The gap
keeps the substrate from being dominated by the Perron common mode, which keeps its Gram
spectrum clear of the readout floor, which is what preserves usable dimensionality as the
operating point rises. The trade is invisible under the field's standard
spectral-radius-matched comparison.

**The biological claim that makes it computational neuroscience.** The connectome is not
organised for capacity. It is organised for not needing to be tuned.

---

## The chain, with the measured link at every step

Every arrow below is a measured quantity, not an inference. This is the spine; if a
section does not serve one of these arrows, it is decoration.

| step | from | to | measured link | where |
|---|---|---|---|---|
| 1 | weight placement | spectral gap | gap ratio 3.078 vs 1.807 to 1.922; weight-permuted control at 1.922 | Act I |
| 2 | spectral gap | weak common-mode domination | `\|mean_state\|` 0.759 vs 0.949 to 0.989 at sigma = 6 | Act II |
| 3 | weak domination | Gram spectrum clear of the ridge floor | 89.0% of the connectome's directions more than a decade clear of the floor vs ER's 11.4% | Act II |
| 4 | clear of the floor | usable dimensionality | `d_eff` 412.9 vs 74.8 supercritically | Act II |
| 5 | usable dimensionality | memory | `d_eff` against measured MC, +0.998 pooled within-regime | Act II into Act III |
| 6 | operating point | how much of the chain survives | retention 47% vs 28 / 22 / 11% at the top of the overlap | Act III |

Step 3 is the link that was missing until 24 August and is the reason Act II was
restructured. It comes from `TIER0` §3.6, filed there under a **rejected** anisotropy
hypothesis; the rejection stands and the refit at the correct end of the spectrum is what
is used. **Verified 24 August 2026** against the frozen parquet: all sixteen published
cells of `TIER0` §3.6 reproduce, and no run was required. See
`report/checks/floor_sensitivity_check.md`.

---

## The primary variable and the intervention

> **"The two axes" is not this pair.** In this project the phrase is an established term
> for the **matching** pair, nominal sigma against `sigma*bulk95` (`CONVENTIONS`, and
> every act file), and it stays reserved for it. Sigma against `f` is a primary variable
> and an intervention, which is a different relationship and gets different words. This
> section was headed "The two axes, and which is primary" until 24 August 2026 and was
> renamed for exactly that collision.

**Spectral radius (sigma) is the primary variable of the thesis.** It is the operating
point, the thing neuromodulation, arousal and plasticity move in a real brain, and the
variable along which every headline claim is made. Subcritical, near-critical and
supercritical are the regimes the whole comparison is run across.

**Sign fraction (f) is an intervention, not a peer.** It appears in exactly one place,
chapter 6 §6.3, and it is introduced there as a **lesion**: it is the only manipulation in
the thesis that removes the proposed cause and checks whether the effect goes with it.
Grading f destroys the Perron guarantee, the spectrum becomes symmetric about zero, the
most negative eigenvalue grows toward `lambda_1`, and `|mean_state|` falls by two orders
of magnitude.

**The plausibility framing, stated once and used consistently.** Macro dMRI is
non-negative because of the *measurement*, not because cortex is: tractography cannot
represent sign, while real cortical circuits have inhibition. So f = 0 is the substrate
the instrument produces, not the biological ground truth, and f > 0 asks what the missing
half of the biology would do. Never write f = 0 as "the biological cut" against f > 0 as a
departure from biology.

**Consequence for writing.** Chapters 4, 5 and §6.1 to §6.2 are entirely at f = 0 along
sigma. f is not mentioned before §6.3, except as a forward reference in the methods
paragraph that defines it.

---

## Act I — structure sets the spectrum (chapter 4)

**Claim.** Connectome weight placement produces an anomalously large spectral gap.
Placement, not weight statistics, not topology alone.

**Sections.**
- The substrate and the null ladder. No results.
- The spectrum is real, it has one outlier, and the bulk is everyone's. Absolute bulk
  spread 4.4% at N = 448 against `bulk95`'s 47.3%; the entire between-variant difference
  sits in `|lambda_1|`. Gap ratio 3.078 against 1.807 to 1.922. The identity
  `|lambda_1|/abs_bulk = 1/bulk95 = sr_crit`.
- It is placement. The weight-permuted rung at 1.922 is the evidence, and the limit is
  named: placement, not which feature of placement.
- Scale. What carries is the separation (3.985 against 2.30 to 2.44 at N = 1000); what
  loosens is the near-identity of the bulks; what reverses is the null ordering, which is
  therefore never quoted across scales.
- What Act I hands to Act II.

**Act I also owns one section in chapter 3**, which this spine names but does not detail:
**the comparison problem** (F3, contribution 5, the two matching axes and what each holds
fixed). Chapter 6 §6.1.1 carries it forward rather than re-deriving it. The spine covers
chapters 4 to 7, so the section is detailed in `act1_structure.md` §4 item 1 instead.

**Hands on.** `sr_crit` as the criticality scale each substrate brings with it, which is
what makes the second matching axis available at all; and the Perron mode as the object
Act II decomposes.

**Figures.** F1, F2, S1.

---

## Act II — the spectrum decomposes the manifold (chapter 5)

**Claim.** The Perron mode carries the mean and the bulk carries the fluctuations; how
much of the bulk clears the readout floor is what sets usable dimensionality; and a
variance-weighted count cannot see it.

**Sections.**
- What Act I handed over, and the question it leaves. The readout sees a `T x N` state
  matrix: which part of the spectrum ends up where in it?
- The probes and their limits, as methods. Stated up front: Probe 2 covers **two**
  substrates at **four** spectral radii and cannot speak to the ladder. `mean_state` is
  signed, so the absolute value is taken before aggregating.
- **The Perron mode carries the mean.** After time-centring the top W-eigenmode holds
  0.0001 of the fluctuation variance, below the random-orthonormal baseline of 0.0023. The
  inversion that is the real finding: `|mean_state|` 0.759 against the nulls' 0.949 to
  0.989, so the substrate with the largest Perron root is the least dominated by it.
- **The Gram spectrum against the ridge floor.** The spectral account of dimensionality
  and the chain's missing link, in the position framing the chapter leads with: **89.0%**
  of the connectome's directions stand more than a decade clear of the floor against
  Erdős–Rényi's **11.4%**, and `d_eff` is **412.9** against **74.8**. Floor mass is
  radius-dependent and each substrate's **interior** minimum sits at a different spectral
  radius, which is what explains the moving optimum. "Interior" is load-bearing and is
  never dropped: see open flag 1.
- **Which counting scheme sees it.** `d_eff` against PR: the range is the argument
  (5.5-fold against 16% across the same seven substrates), and the failure of PR is a
  consequence of the previous section rather than a separate finding.
- Sign selects the basis. Short, confirmatory of Krauss 2019, and framed as a statement
  about the decomposition: with non-negative weights the W-eigenmode alignment has been
  absorbed into the mean, so the fluctuations are organised by graph structure; balancing
  signs hands it back.
- What Act II hands to Act III.

**Hands on.** The common-mode account; `d_eff` as the measure, now earned; the floor
account that makes it spectral; and **the temporal axis, stated as flat at f = 0**, which
is the seam between the two halves of the thesis and does not go in an appendix.

**Figures.** F4, F5, F6 and **F18**, the floor-sensitivity figure, which the check of
24 August cleared and which was built the same day. **S2 prints in this chapter too**, but
it is Act III's figure: it is listed and owned there, and this is the only place its
chapter is named.

---

## Act III — manifold geometry sets computational capacity (chapter 6)

**Claim.** Where the leading effective gain sits relative to +/-1 sets both capacities,
with opposite sign. The gap widens the usable window rather than raising a peak.

**Structure, and why it is in this order.** Memory and prediction are each reported along
sigma at f = 0 first. Only then is f introduced, as the intervention that removes the
common mode, and it delivers both consequences from one manipulation. The unifying claim
is therefore the **conclusion** of a causal test rather than a frame the reader must
accept up front.

- **§6.1 Memory along the regime axis, f = 0.** The crossing (peaks lowest at 432.4,
  retains most at 47% against 28 / 22 / 11%); peak parity with its interval, with the
  Aceituno reconciliation on the panel that reproduces their ordering; the N = 1000
  margin under both thresholds; and what the gap buys, with `|mean_state|` rising 0.114 to
  0.759 across sigma against ER's 0.593 to 0.989.
- **§6.2 Prediction along the regime axis, f = 0.** Prediction decays roughly tenfold
  with sigma while curvature stays flat at 0.26; collapse resistance far supercritically
  (0 of 10 seeds against ER's 5 of 10, sigma 7.6 to 8.0, Fisher p = 0.033) and no
  advantage at all near criticality; then the named open problem, with three candidate
  explanations ruled out on the data and no fourth offered.
- **§6.3 Is the common mode the cause? Remove it.** f introduced as a lesion. Memory:
  nobody degrades, everyone gains, and the advantage closes because the nulls gain about
  four times as much from a much lower start. Hub-targeted inhibition as the most
  efficient way to destroy the mode. Generation: the switch appears once negative weights
  make the period-2 branch reachable, and the VPT advantage clears the placement control.
  `sigma_eff` as a locator, not a criterion. The free-running rollout, with its refuted
  half reported at length.
- **§6.4 One axis, two readouts.** The map argument, now earned; the crossing quantified
  with its axis and its coverage; the scope limit back onto §6.2's open problem; and the
  statement that contribution 2 has no out-of-sample test in this thesis.

**Hands on.** The dissociation as one axis, and one named open problem.

**Figures.** F7, F9, F10, F11, F12, F13, F14, F16, F17 and **S2**, which
`act3_prediction.py` holds. S2 is Act III's and this is the only place its module is
named; the chapter it prints in is named under Act II.

---

## Act IV — the same decomposition organises empirical function (chapter 7)

**Status: anchor, conditional. Nothing in Acts I to III depends on it.**

**Claim, narrowly.** The same spectral decomposition that explains computational capacity
also organises measured functional structure, with the common mode as the global-signal
analogue. **Not** a claim to a better SC-to-FC predictor; that is a large mature field and
the thesis must not appear to be competing in it.

**Tiers, with a pre-committed stopping rule.**
- **Tier A.** Which Yeo networks load the Perron mode. Hours, no simulation. A paragraph
  and a figure, descriptive on its own.
- **Tier B.** Simulated FC from the noise-driven connectome reservoir at f = 0, compared
  to empirical FC with and without common-mode removal, across the null ladder. This is
  the anchor. The prediction is pre-statable: with the common mode in, simulated FC is
  dominated by one global factor and Yeo block structure is weak; after removal it
  emerges. If ER also recovers Yeo structure the result is trivial and is reported as
  such.
- **Tier C.** Sigma sweep, asking whether the match peaks near `sr_crit`. This is the tier
  that would tie Act IV back to Act III.

**Blocking questions, to be answered before any run.** Was global signal regression
applied to the empirical FC? Does it use the same parcellation and N as the SC?
Group-average or individual-level, and how many subjects?

**Stopping rule.** If Tier B has produced no result by **3 September**, Act IV is Tier A
plus a future-work paragraph.

**Figures.** F15, plus whatever Tier B produces.

---

## Withdrawn language — never write these

| do not write | write instead |
|---|---|
| "compact bulk", "compressed bulk" | "large spectral gap" |
| "the connectome is subcritically worse than ER" | "parity below criticality, advantage above", with the axis named |
| "hub inhibition collapses memory" | "hub-targeted inhibition closes the advantage fastest; nothing collapses, the null moves" |
| "`sigma_eff` crosses 1 at the transition" | "`sigma_eff` is the best empirical **locator**"; the criterion is falsified |
| "generation tracks trajectory straightness" | "capacity is gated by which dynamical regime the manifold is in", and only of f > 0 |
| the crossing, quoted bare | always with its axis: the first crossing inside full replicate coverage, at (`sigma·bulk95` = 2.938, f = 0.153); absent on the nominal axis |
| "the connectome is a better reservoir" | it is not, at the peak; the advantage is supercritical robustness |
| "the biological cut" for f = 0 against f > 0 | f = 0 is what the instrument produces; f > 0 is the missing half of the biology |

Further standing rules: peak memory is **parity**, never "always worst"; every margin is
quoted with its levels (4.40 to 4.42 always beside 12.28 against 2.82); every sigma-bearing
claim names its sigma; every crossing names its axis.

---

## Open flags carried into writing

1. **The floor-sensitivity link is verified and the figure is built.** Chain step 3
   reproduced in all sixteen cells on 24 August 2026, the coverage for a four-variant,
   radius-resolved figure was already in frozen data, and the figure was built the same
   day as **F18** with no run (`report/FIGURE_LIST.md`, count 16 to 17). This flag stays
   open because what it now carries is not a task but **two wording constraints**, and
   they travel into every caption and every sentence of §5.4:
   the per-substrate minima are **interior** minima of a two-humped curve, since floor
   sensitivity also falls to zero as the spectral radius falls to zero; and
   Erdős–Rényi's low absolute floor sensitivity is **degenerate**, since relative to
   surviving dimensionality it is the **most** floor-sensitive substrate on the ladder,
   losing 29.1% per decade of alpha against the connectome's 5.6%. Both are the same trap:
   the sensitivity vanishes at *both* ends of the spectrum, so a low number never
   interprets itself.
2. **§6.2's decay result has no figure.** The f = 0 curvature-flat against VPT-falling
   table is `TIER0` §3.11 and is not on `FIGURE_LIST`. Either it is stated inline or a
   figure is proposed through the amendment procedure.
3. **F11's panels split across §6.1 and §6.3** under the new ordering. Whether that is a
   reference split or a re-cut is a session-3 decision, not a writing decision.
4. **The driven Mackey-Glass registered prediction** was collected and may never have been
   inspected. It is either reported in §6.1 as corroboration, or the thesis states plainly
   that it was collected and not analysed, and why.
5. **The f = 0 collapse asymmetry rests on n = 10 seeds** (Fisher p = 0.033). It carries
   the biological half of the prediction claim, and the weight it carries relative to its
   sample is stated in the text rather than left to inference.

# Mackey-Glass: scope, a withdrawn pre-registration, and a narrower one

> **Sections 1 to 3 are the PRE-REGISTRATION.** Written, dated and committed **before any
> Mackey-Glass result from the §4b sweep was inspected**. Section 4 (the outcome) is
> appended afterwards. If the outcome contradicts the prediction, the prediction stands as
> written. It is not to be revised.
>
> Written: **15 August 2026**, session 0 of the §4b sweep.
> Code state at pre-registration: commit `5fbe250`.
>
> **Revised twice on 15 August 2026, both times before any Mackey-Glass data was
> inspected, and both times only to weaken or disambiguate what is claimed.** Nothing here
> is revised once an outcome exists.
>
> 1. The secondary horizon dose-response prediction was **withdrawn** and replaced by a
>    diagnostic with no claim attached (§2.1).
> 2. The direction of the predicted quantity was **ambiguous and is now pinned** (§2).
>    "Advantage" was defined as *connectome minus null* on a lower-is-better metric, so an
>    advantage was a negative number, while the trend was predicted "negative" meaning
>    *shrinking* — under which reading the prediction and its own falsifier
>    ("flat or increasing") pointed the same way. `advantage` is now defined as
>    `NRMSE_null - NRMSE_connectome`, positive means the connectome is better, and the
>    prediction and falsifier are restated against that. The null family is also now named
>    in full rather than left as "every null".

---

## 1. What Mackey-Glass is in this thesis, and what it is not

**It is a driven, teacher-forced forecasting task**: the reservoir is fed the true `x(t)`
at every step and is trained to read out `x(t + h)`. It never sees its own prediction.
This is what `src/tasks/mackey_glass.py` implements, in its own words: *"the reservoir
always sees the true x(t), never its own prediction. Closed-loop free-running is
deliberately deferred to the Lorenz task."*

**So it probes memory and nonlinear expressivity, not closed-loop generation.** It sits
beside NARMA-10 as a second bridge task, with more memory loading (the delay term at
lag tau = 17 means `x(t+h)` depends on values the reservoir must still be holding) and a
chaotic rather than a stochastic target.

**It is a corroborating task. No claim in this thesis rests on it.** The primary-task
mapping in `report/FIGURE_LIST.md` is what governs; MG appears there only in the
corroborating column, on the memory side.

### 1.1 The original pre-registration, and why it is withdrawn

Held here in full because a prediction that is quietly dropped is worse than one that
fails. **It was withdrawn on 15 August 2026 in session 0, before any MG data was
inspected, on design grounds rather than evidential ones.**

> **As it stood:** MG is the out-of-sample test of contribution 2. Being a delay system,
> closed-loop rollout must hold state at lag tau, so it needs both capacities at once:
> **the prediction is an interior optimum in f**, unlike MC (edge) and Lorenz (f = 0), and
> running tau = 17 and 30 makes memory demand a dial whose optimum should shift toward
> higher f. Falsified by: no interior optimum, an optimum that does not move with tau, or
> one that moves the wrong way.

**Why it cannot be tested by the implemented task.** Under teacher-forcing the reservoir
is re-anchored by the true input at every step, so it cannot leave the attractor and the
period-2 collapse — the switch that contribution 2 *is* — has no consequence for the
metric. What remains is memory plus static nonlinearity, which is what MC and NARMA
already measure. That makes **both branches uninterpretable**: "no interior optimum" is
what the protocol predicts by construction whether or not contribution 2 holds, and an
interior optimum could arise from expressivity peaking in f without bearing on the
mechanism. A test whose every outcome is unreadable is not a test.

Testing it properly needs a closed-loop MG rollout, which the repo does not implement.
**Decision taken in session 0: not built for the thesis; recorded in the roadmap §5 as
deferred work.** Contribution 2 therefore has **no out-of-sample test in this thesis**,
and the discussion must say so rather than let MG's presence imply otherwise.

---

## 2. The prediction

The narrower claim the driven design *can* carry. It transfers the §2.6 account — that
supercritical memory rises with `f` for every substrate and the connectome's advantage
narrows because **the nulls catch up, not because the connectome degrades** — to a third
memory-loaded task that was not used to derive it.

**Declared quantity, with its sign fixed.** NRMSE is lower-is-better, so "advantage" is
defined here once and used only in this direction:

> **`advantage = NRMSE_null - NRMSE_connectome`, paired within seed.
> Positive means the connectome is better.**

The prediction is about that quantity, not about absolute NRMSE: absolute NRMSE is not
comparable across `f` because the target series is unchanged while the reservoir's
operating point is not.

**The null family is all three, named:** `erdos_renyi`, `connectome_weight_permuted` and
`degree_rewire`. Degree-matching is **in**, and is named explicitly because it is the null
that does not cooperate elsewhere — the peak-memory deficit is reliable against ER and
weight-permuted but **not** against degree (`TIER0` §3.4, 1 of 5 alphas). Leaving it
unstated would let the family be chosen after the fact, which is the whole thing this
document exists to prevent.

**Primary.** At the supercritical operating point (sigma >= 3.078), `advantage` is
**positive and largest at `f` = 0** against all three nulls, and **decreases toward zero
as `f` rises**, reaching zero within noise by `f` ≈ 0.25 — the same shape MC shows
(`TIER0` §2.6), on a task the account was not fitted to.

- predicted at `f` = 0: `advantage` > 0 against **all three** nulls, paired 95% CI
  excluding zero for at least ER and weight-permuted
- predicted at `f` >= 0.25: **all three contrasts within noise**, paired 95% CI including
  zero
- predicted **sign of the trend of `advantage` against `f`: negative** — that is,
  `advantage` *shrinks* from a positive value at `f` = 0 toward zero, it does not become
  large and negative

**What would falsify this.** Either: `advantage` at `f` = 0 is zero or negative (the
connectome no better than the nulls, or worse); or the trend of `advantage` against `f` is
flat or **positive** (the advantage failing to close, or widening).

**There is no secondary prediction.** `h` = 84 is collected but nothing is predicted of
it — see §2.1.

### 2.1 The horizon dose-response, withdrawn

A secondary prediction was registered and then withdrawn on the same day, before any run:
*horizon replaces tau as the memory-demand dial, so the connectome's advantage at `f` = 0
is larger at h = 300 than at h = 84.* Held here because a prediction that is quietly
dropped is worse than one that fails.

**Why it was withdrawn: it is confirmable by an artifact.** `h` = 84 is the easy horizon
(NRMSE ~0.09 at rung 0 on C. elegans; see the disclosure in §3, commitment 1). If it sits
near the floor for every substrate
on the human connectome too, the connectome-minus-null advantage there is compressed
toward zero *because every substrate is nearly perfect* — and then
`advantage(h=300) > advantage(h=84)` returns **confirmed for a ceiling reason with nothing
to do with memory demand**.

That is the failure mode `TIER0` §1.2, §1.1b and §3.8 each record: a delta read without
its levels, where the null moved rather than the substrate. This project has been caught by
it three times. A prediction likely to be confirmed by the fourth instance is worth less
than no prediction, because it has to be defended with a known confound attached.

**What `h` = 84 is for instead.** A saturation diagnostic and a hedge against choosing the
horizon blind: it shows whether the task sits in a regime where substrates can differ at
all. **Descriptive reporting only.** No claim rests on it, and it may not be promoted (see
§3.2).

**What this does *not* test.** Contribution 2. Nothing here distinguishes the single-axis
account from any account in which the connectome simply has more memory. It is a
consistency check on the transfer, and must be reported as one.

---

## 3. Recorded commitments

1. **The MG grid is not inspected** until this section is committed. As of writing, no
   human Mackey-Glass results exist in the repo: `experiments/human/human_mackey_glass/`
   has code and no results directory. C. elegans MG results *do* exist
   (`experiments/celegans/celegans_mackey_glass/results/{h84,h300}/`) on a different
   substrate with no `f` axis; they cannot inform a prediction about the shape in `f`.
   **Disclosure:** while establishing that in session 0, C. elegans MG NRMSE values were
   read from a comment in `task_config.py`. They are recorded here so the exposure is on
   the record: h = 84 NRMSE ~0.09, h = 300 NRMSE ~0.47, at rung 0 on the C. elegans
   substrate. No parquet or figure, on either substrate, was opened.
2. **Primary metric and horizon declared in advance, and not swappable.** The metric is
   **NRMSE at the forecast horizon**, paired within seed as connectome minus null. The
   primary horizon is **h = 300**, the chaos-limited regime where substrates can separate;
   h = 84 is a diagnostic (§2.1).

   > **h = 300 may not be swapped for h = 84 after the data is seen**, and h = 84 may not
   > be promoted to primary because it happens to look better. Both horizons are collected
   > so the *data* exists, not so the *claim* can pick its ground afterwards — with two
   > horizons, four variants and eleven `f` there is always somewhere a difference holds,
   > which is the whole reason this mapping is declared in advance. If h = 300 turns out to
   > sit at the no-skill ceiling for every substrate, the honest report is **"MG was
   > uninformative at the pre-declared horizon"**, with h = 84 shown descriptively beside
   > it and labelled as not pre-declared. That is a publishable sentence. Quietly leading
   > with h = 84 is not.
3. **`mean_curvature`, `participation_ratio` and `mean_gain` are computed inline on MG
   driven states**, since they cannot be recovered from the persisted Gram spectra. Done:
   `phase_diagram/capture.py` computes all three for every task in the list.
4. **Same grid, seeds and null ladder** as the other three tasks, so the comparison is
   paired: 4 variants x 11 `f` x 29 sigma x 10 seeds x 3 draws.
5. **The delay is fixed at tau = 17 and is not a manipulated variable.** It was one in the
   withdrawn design; it is now frozen at the canonical mild-chaos value in `MG_PARAMS`
   alongside a = 0.2, b = 0.1, n = 10. **tau = 30 is not run**, and no claim in this
   thesis may reference a tau dose-response. Memory demand is varied by forecast horizon
   only, and that variation carries no prediction (§2.1).
6. **No tuning toward the prediction.** The reservoir hyperparameters
   (`input_scaling` = 0.5, `leak_rate` = 0.3) are the frozen C. elegans values and are not
   re-tuned. If they are ever re-tuned it must be on a null, never the connectome, and the
   re-tune must be recorded here before the grid is re-read.
7. **Scope.** This tests the transfer of the §2.6 memory account to a driven delay task.
   It says nothing about the `f` = 0 generation regime (`TIER0` §3.11), nothing about
   closed-loop rollout, and nothing about contribution 2.

---

## 4. Outcome

*(appended after the run; do not write until sections 1 to 3 are committed)*

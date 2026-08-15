# Mackey-Glass: scope, a withdrawn pre-registration, and a narrower one

> **Sections 1 to 3 are the PRE-REGISTRATION.** Written, dated and committed **before any
> Mackey-Glass result from the §4b sweep was inspected**. Section 4 (the outcome) is
> appended afterwards. If the outcome contradicts the prediction, the prediction stands as
> written. It is not to be revised.
>
> Written: **15 August 2026**, session 0 of the §4b sweep.
> Code state at pre-registration: commit `5fbe250`.

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

**Declared quantity.** The prediction is about the **connectome's advantage over the
nulls** (NRMSE, connectome minus null, paired within seed), not absolute NRMSE. Absolute
NRMSE is not comparable across `f` because the target series is unchanged while the
reservoir's operating point is not.

**Primary.** At the supercritical operating point, the connectome's NRMSE advantage over
every null is **largest at `f` = 0 and decreases monotonically with `f`**, closing to
within noise by `f` ≈ 0.25 — the same shape MC shows (`TIER0` §2.6), on a task the account
was not fitted to.

- predicted advantage at `f` = 0: **connectome better than ER**, and better than
  weight-permuted, at sigma ≥ 3.078
- predicted at `f` ≥ 0.25: **all three contrasts within noise** (paired 95% CI includes 0)
- predicted direction of the trend in `f`: **negative** (advantage shrinking)

**Secondary — the horizon dose-response.** Horizon replaces tau as the memory-demand dial:
`h` = 300 requires holding more of the trajectory than `h` = 84. So the connectome's
advantage at `f` = 0 is **larger at h = 300 than at h = 84**.

- predicted sign of `advantage(h=300) - advantage(h=84)` at `f` = 0: **positive**

**What would falsify this.** Any of: the advantage at `f` = 0 absent or reversed; the
trend in `f` flat or increasing; the advantage at `h` = 84 exceeding that at `h` = 300 at
`f` = 0.

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
2. **Primary metric declared in advance:** **NRMSE at the forecast horizon**, paired
   within seed as connectome minus null, at **h = 300 primary** and h = 84 secondary.
   h = 300 is the chaos-limited regime; h = 84 risks a floor effect, so **check for
   saturation before reading the trend**, and if h = 84 is at the floor for every
   substrate, report the dose-response as untestable rather than as a null result.
3. **`mean_curvature`, `participation_ratio` and `mean_gain` are computed inline on MG
   driven states**, since they cannot be recovered from the persisted Gram spectra. Done:
   `phase_diagram/capture.py` computes all three for every task in the list.
4. **Same grid, seeds and null ladder** as the other three tasks, so the comparison is
   paired: 4 variants x 11 `f` x 29 sigma x 10 seeds x 3 draws.
5. **No tuning toward the prediction.** The reservoir hyperparameters
   (`input_scaling` = 0.5, `leak_rate` = 0.3) are the frozen C. elegans values and are not
   re-tuned. If they are ever re-tuned it must be on a null, never the connectome, and the
   re-tune must be recorded here before the grid is re-read.
6. **Scope.** This tests the transfer of the §2.6 memory account to a driven delay task.
   It says nothing about the `f` = 0 generation regime (`TIER0` §3.11), nothing about
   closed-loop rollout, and nothing about contribution 2.

---

## 4. Outcome

*(appended after the run; do not write until sections 1 to 3 are committed)*

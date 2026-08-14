# Mackey-Glass as an out-of-sample test of the single-axis model

> **Sections 1 to 3 are a PRE-REGISTRATION.** They must be written, committed and dated
> **before any Mackey-Glass result from the §4b sweep is inspected**. Section 4 (the
> outcome) is appended afterwards. If the outcome contradicts the prediction, the
> prediction stands as written. It is not to be revised.
>
> Written: <DATE>. Code state at pre-registration: commit `<HASH>`.

---

## 1. Why MG is a test and not a fourth benchmark

Contribution 2 says the memory/generation dissociation is **one axis read out with
opposite sign**. Each unit is `x -> tanh(gain·x + input)`: gain above +1 gives a stable
fixed point, below -1 a period-2 orbit, nothing stable between. Perron-Frobenius pins a
non-negative matrix to the positive branch, which wastes readout dimensions (bad for
memory) and holds the trajectory smooth (good for generation).

MC and Lorenz sit at opposite ends of that axis and the model was **fitted on them**. MG
is different in kind: it is a **delay** system, so closed-loop rollout requires holding
state at lag tau. It needs both capacities at once, on a grid the model has never seen.

## 2. The prediction

**First, declare the quantity.** The prediction below is about **absolute MG performance**
of the connectome, not its advantage over the nulls. The two behave differently in f and
conflating them makes the test unreadable, so fix one here:

- [ ] absolute performance (the reading assumed below), or
- [ ] connectome minus best null

**Primary.** MG performance peaks at an **interior optimum in f**, unlike the two tasks the
model was fitted on, *both* of which are optimal at an edge — and at **opposite** edges:
absolute MC *rises* with f (11.43 -> 14.35 at sigma = 6, `TIER0` §2.6; flat in f at each
f's own best sigma), while Lorenz VPT is best at f = 0 and decays monotonically. An
interior optimum is therefore not a weaker version of either, it is a shape neither task
shows. State the predicted band before running:

- predicted optimum: f\* in [ , ]
- predicted at sigma: [ , ]

**Secondary — the dose-response.** Running **tau = 17 and tau = 30** makes memory demand
a dial. Longer delay means more state must be held, so:

- **the optimum shifts toward higher f as tau grows** (toward the memory-favouring side)
- predicted shift: f\*(tau=30) - f\*(tau=17) = ______ , sign positive

**What would falsify this.** Any of: no interior optimum (MG rises monotonically like MC,
or decays monotonically like Lorenz); an optimum that does not move with tau; an optimum
that moves the wrong way.

## 3. Recorded commitments

1. **The MG grid is not inspected** until this section is committed.
2. **Primary metric declared in advance:** ______ (closed-loop VPT / NRMSE at horizon h),
   with the horizon fixed at ______. MG is famously easy for reservoirs at short horizons,
   so the horizon must be long enough to separate conditions; check for ceiling effects
   before reading the optimum.
3. **`mean_curvature` and `mean_gain` are computed inline on MG driven states**, since they
   cannot be recovered from the persisted Gram spectra and the regime-switch reading
   depends on them.
4. **Same grid, seeds and null ladder** as the Lorenz arm, so the comparison is paired.
5. **No tuning toward the prediction.** The analysis is not adjusted, re-binned or
   re-scoped after seeing where the optimum falls. A clean "no interior optimum" is a valid
   and valuable outcome and would bound contribution 2 rather than destroy it.
6. **Scope.** This tests the single-axis account at f > 0. It says nothing about the f = 0
   regime, where what sets generation is open (`TIER0` §3.11).

---

## 4. Outcome

*(appended after the run; do not write until sections 1 to 3 are committed)*

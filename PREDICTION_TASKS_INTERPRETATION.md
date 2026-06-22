# Interpreting the C. elegans prediction-task results: topology, weight placement, and closed-loop generation

*The reference summary of the three C. elegans connectome prediction tasks —
NARMA-10 (input-driven emulation), Mackey-Glass (driven forecasting), and Lorenz
(closed-loop free-running) — after the weight-placement control resolved the
topology-vs-weights confound. Section 1 reports what was measured across the three
tasks; Section 2 develops the two candidate mechanisms; Section 3 reports the four
diagnostics that tested them; Section 4 reports the Lorenz task in full. Bottom
line: **weight placement (Mechanism A) is the connectome's active ingredient —
confirmed across all three tasks, now on both stability and fidelity — a small
asset for input-driven emulation but a liability for autonomous forecasting and
chaotic generation; directed topology (Mechanism B) helps only the noisy
input-driven task and is neutral for both autonomous tasks. At the canonical
operating point the connectome is worse-or-equal everywhere.** Confidence is
flagged throughout.*

---

## 1. What we actually measured (the solid part)

Three prediction tasks, three realism conditions, the connectome vs a five-rung
null ladder **plus** a `connectome_weight_permuted` control (real topology, real
weight multiset, placement scrambled). The control splits the v2b/v2d effect:
`connectome vs control` = **placement**, `control vs degree_rewire` = **topology**.
The three tasks span the task axis: input-driven emulation (NARMA), driven
forecasting (MG), and autonomous closed-loop generation (Lorenz, two metrics).

| Supercritical (sr≈1.47), v2b/v2d | NARMA-10 (driven emulation, i.i.d. input) | Mackey-Glass (driven forecast, smooth input) | Lorenz (closed-loop free-run; VPT / climate) |
|---|---|---|---|
| **Topology** (control vs degree) | **large +** (d ≈ +4.3 to +4.9) | **null** | **null** on both metrics (d ≈ 0) |
| **Placement** (connectome vs control) | small **+** (d ≈ +1) | **large −** (d ≈ −2 to −3) | **large −** on both metrics (d ≈ −2) |
| Connectome behaviour | robustness: nulls *blow up*, connectome stays flat | none — nulls *improve*, connectome stays flat | nulls *reach the rich regime*; connectome stays flat → worse on both |

**The load-bearing honest caveat:** at the **canonical** operating point (sr≈0.95,
the edge-of-chaos regime you would actually use) the connectome is **worse than or
equal to its nulls on all three tasks** (NARMA ~0.55 vs nulls ~0.4; MG ~0.15 vs
nulls ~0.10; Lorenz roughly tied — VPT ~1.6 Lyapunov times, no significant climate
difference). Its only "wins" are *supercritical*, and only on NARMA, and only by
not destabilising where the nulls do. So nothing here says the connectome is a
*better* reservoir — it says its directed structure is *more stable* in a regime
you would normally avoid. I state that plainly before interpreting, because the
tidy story below could otherwise read as a connectome victory lap. It isn't one.

---

## 2. Interpretation: two largely-separate mechanisms

The cleanest reading that fits the dissociation is **two** effects on different
axes — a single "effective spectral radius" axis cannot explain it, because that
would make topology matter (oppositely) on *both* tasks, and topology is null on MG.

### Mechanism A — weight **placement** sets effective gain / memory *(CONFIRMED — §3)*

The connectome's real weights are heavy-tailed raw synapse counts, concentrated on
a few strong pathways. Placing them on their real edges plausibly **maximises
Perron–Frobenius compression** (one dominant eigenvalue, a depressed bulk), so at a
matched *nominal* spectral radius the connectome's *effective* dynamics are the
mildest — least memory, least excitable. Permuting the weights (the control)
scatters the heavy entries, relaxes the compression, and restores effective
dynamics. This is a single monotonic axis, **rewarded oppositely** by the two tasks:

- NARMA is noise-driven and prone to supercritical blow-up → **mild/compressed = stable = good** (a small bonus, since topology already supplies most of the stability).
- MG forecasting is memory-hungry and never blows up (smooth input) → **mild/compressed = less memory = bad** (a large penalty, since memory is the whole game).

This is consistent with the ordering *both* tasks imply for "effective dynamics":
connectome (most compressed) < control < degree < random (most energetic) — NARMA
rewards the low end supercritically, MG rewards the high end.

### Mechanism B — directed **topology** suppresses broadband instability *(tested, NOT established — §3)*

Topology matters a lot for NARMA and not at all for MG, with the **same weight
distribution** on both sides of the comparison (control vs degree). So topology is
doing something that *only the noisy task cares about*. The most plausible candidate:
the connectome's directed organisation (hierarchy / feed-forward bias / modular and
motif structure beyond the degree sequence) **suppresses the recurrent, high-frequency
instabilities that broadband i.i.d. input excites** at high nominal sr. A
degree-randomised graph keeps the degree sequence but scrambles that organisation,
leaving loops that amplify noise into blow-up.

MG's drive is smooth and low-frequency, so it never excites those modes — and
suppressing them is therefore invisible to MG → topology neutral. This frequency-
domain framing is the speculative part; what I'm more confident of is the weaker
claim that **topology buys noise-robustness specifically, not general computational
power or memory** (otherwise it would help MG too).

### Putting them together

- **Placement → effective gain/memory** (a stability⇄memory trade-off, rewarded oppositely).
- **Topology → robustness to broadband-driven instability** (an asset only when there *is* destabilising broadband input — NARMA yes, MG no).

The dissociation falls out: NARMA cares about both axes (topology-led stability +
a placement bonus); MG cares only about the memory axis (placement-driven, harmful)
and is indifferent to the noise-robustness axis (topology null).

---

## 3. Diagnostic results (the mechanisms, tested)

Four cheap diagnostics were run to confirm or kill Section 2. **Mechanism A is
confirmed four independent ways; Mechanism B is not established.**

**(1) Spectra (eigenvalues of each weighted `W`).** The connectome's bulk is the
**most compressed** — `bulk₉₅/λ₁ ≈ 0.30` vs control/degree ≈ 0.38 vs random ≈ 0.46
(v2b) — and it has the **largest raw λ₁** (~105), so rescaling to a matched sr
shrinks its bulk the most. v2a variants are spectrally **identical** (explains the
v2a null). One correction to my guess: the connectome is *not* a clean single-Perron
mode — it carries a sizeable λ₂ (~0.77), a 2-D dominant subspace, *then* a deeply
compressed bulk. Topology (control vs degree) shows **no** bulk-compression
difference.

**(2) Memory capacity (standard Jaeger MC, leak=1.0, swept over sr).** The
connectome has the **least** linear memory at the operating point (v2b MC ≈ 9.2 vs
nulls ≈ 11–12.6), and its MC is **spectral-shifted** to higher sr (it peaks
supercritically while the nulls peak canonically and decline, crossing only near
sr≈1.75). The placement signature is explicit: permuting the connectome's weights
(control) **restores ≈2 units of MC**; topology (control ≈ degree) is MC-neutral.
**MG performance tracks the MC ordering across variants** → MG is *memory-limited*,
and the connectome's placement-driven memory deficit explains its MG deficit.
*(This vindicates the naive compression→less-memory prediction I'd second-guessed
in favour of the memory-nonlinearity tradeoff; the tidier theory was wrong here.)*

**(3) ESP / noise-response (state distance from two initial conditions; 0 = ESP
holds).** **Partial and noisy.** Robust parts: canonically ESP holds for all; smooth
drive destabilises far less than i.i.d.; random is the most ESP-fragile; and at
strong supercriticality (sr=1.75, i.i.d.) v2b orders connectome < control < degree <
random — the NARMA order. But near the ESP bifurcation the metric is noisy (sr=1.5
scrambles the order, v2d is messier), so it **does not cleanly attribute** the
control-vs-degree NARMA gap to ESP-stability. Mechanism B stays plausible but
**unconfirmed**; a cleaner probe (local Lyapunov exponent, or NARMA-feature
conditioning) would be needed.

**(4) `sqrt`-weight sensitivity.** The placement effect is **largely a heavy-tailed
raw-weight phenomenon**: switching raw→`sqrt` collapses the connectome-vs-control
compression gap (0.10 → ~0) and roughly **halves** the MG placement penalty
(d ≈ −2.9/−2.1/−1.6 → −1.8/−0.8/−0.4 across sr). It doesn't vanish entirely (residual
−1.8 at sr=1.37), so it's *largely*, not *entirely*, an artefact. The topology leg is
untouched by `sqrt` — consistent with it being a separate, non-compression axis.

**Net.** The placement→compression→memory axis (Mechanism A) is solid and
mechanistically grounded across spectra, memory, MG-tracks-MC, and `sqrt`. The
topology axis (Mechanism B) is real in the task data but **mechanistically open** —
invisible to spectra and memory, not killed by `sqrt`, not cleanly captured by ESP.
And the **magnitude** of the placement effect is inflated by the `raw`-weight choice
(`sqrt` ~halves it) — a live methodological decision for the prediction tasks.

**One alternative still not dismissed:** the "two clean axes" picture is the kind of
tidy narrative that can over-fit limited data; the diagnostics support the *placement*
axis strongly but leave the *topology* axis a labelled gap, not a mechanism.

---

## 4. The Lorenz task: results (closed-loop free-running)

Lorenz is **closed-loop free-running** generation of a strongly chaotic 3-D
attractor: teacher-force a ridge readout on the true trajectory, then cut the
reservoir loose so its own 3-D prediction is fed back as its next input, with no
further teacher forcing. It is the most on-message task (the
connectome-as-world-model framing) and the one where the two mechanisms were
expected to pull in opposite directions. Each matrix cell is scored on **two**
metrics: **VPT** (valid-prediction time, in Lyapunov time, **higher = better** — a
*stability* metric) and **climate** (mean per-coordinate Wasserstein-1 between the
long free-run's marginals and the true attractor's, **lower = better** — a
*fidelity* metric). Same 3 conditions × 7-variant ladder × 20-point sr sweep × 10
seeds; reservoir size is **fixed at the connectome's N=300**. Frozen operating
point tuned on the v2a rung-0 baseline (input_scaling=0.1, leak=1.0, ridge=1e-7,
**direct next-state** readout); baseline canonical VPT ≈ 2.2 Lyapunov times,
climate ≈ 5.2.

*(Two methodological notes. The readout predicts the next state **directly**, not
the increment: at N=300 the increment form's small corrections let the free-run
drift off the attractor and blow the climate metric to its cap for every
hyperparameter, while direct prediction self-corrects and is discriminative. And
the local RK4 generator is cross-checked against `reservoirpy.datasets.lorenz`
only over a **short** pre-divergence horizon — bit-exactness is impossible because
reservoirpy uses adaptive `solve_ivp` and chaos decorrelates any two integrators
within a few Lyapunov times.)*

### The result: worse on both metrics, and it is weight placement

The pre-registered guess was a **fidelity-for-stability trade** — decent VPT, poor
climate, a *metric-dependent ranking flip*. **That is refuted.** In the directed
conditions (v2b/v2d), supercritically (sr ≥ 1.25), the connectome is significantly
**worse than its nulls on both metrics at once** — VPT in **88/96** cells, climate
in **79/96** cells — and the deficit is **entirely weight placement**:

| Supercritical (sr ≥ 1.25), v2b/v2d | VPT (stability, higher=better) | Climate (fidelity, lower=better) |
|---|---|---|
| **Placement** — connectome vs control | d ≈ **−2.0**, δ ≈ −0.85 | d ≈ **−2.0**, δ ≈ −0.73 |
| **Topology** — control vs degree_rewire | d ≈ **0** | d ≈ **0** |

The magnitudes are stark: supercritically the nulls **and the placement control**
lift off into the regime that reconstructs Lorenz (VPT ~1.6 → ~4.8 Lyapunov times;
climate ~7 → ~0.6, a near-faithful attractor), while the connectome stays **flat**
regardless of nominal sr (VPT ~2, climate ~6 — a collapsed attractor). On the
sweep figures every variant rises in the supercritical band except the connectome.

This is the **Mackey-Glass result repeated and doubled**: a placement-driven
deficit with a null topology leg — but now on *stability and fidelity together*,
not fidelity alone. It is exactly the alternative the prediction flagged as
possible — *"if closed-loop feedback makes the connectome's mild dynamics collapse
fast, it could be both unstable-in-shape and low-fidelity — worse on everything."*
Mechanistically it is the confirmed **Mechanism A acting alone**: the connectome's
heavy weights compress its spectrum, so at any matched *nominal* sr its *effective*
dynamics stay the mildest — too mild to enter the rich regime that sustains the
attractor. Permuting the weights (the control) relaxes the compression, and the
control then behaves like the nulls. There is no separate stability axis rescuing
VPT, so the two metrics **agree** — and by the falsification criterion stated when
this was a prediction (*"if both metrics agree, the two-mechanism picture is
wrong"*), Lorenz says directed topology contributes **no autonomous-stability axis
of its own**: its topology leg is null on both Lorenz metrics, just as on MG.

### Three honest nuances

- **A low-sr crossover.** Below sr ≈ 0.8 the connectome is significantly *better*
  on climate (31 significant cells, v2b/v2d): where the nulls are too weak or
  unstructured to hold the attractor, the connectome's mild dynamics help. The
  deficit is purely a *supercritical* phenomenon — consistent with NARMA/MG, where
  the connectome's only distinctive regime is supercritical.
- **Canonical sr: tied, not best.** At sr ≈ 0.95 the connectome is statistically
  indistinguishable from its nulls (2 marginal VPT cells, 0 climate cells
  significant) — the same "worse-or-equal at the operating point" as the prior two
  tasks.
- **A faint robustness echo (v2a only).** Supercritically in the undirected
  condition the connectome blows up in **3%** of seeds vs **20–25%** for the
  random/ER nulls — it fails less catastrophically (a NARMA-like robustness trace).
  But this buys **no** better central-tendency performance, which is exactly why
  the "stability" half of the prediction does not carry: divergence-resistance ≠
  longer valid prediction or a truer attractor.

### Where this leaves the picture

Lorenz **strengthens Mechanism A and further empties Mechanism B for autonomous
tasks.** Across all three tasks the active ingredient is the connectome's real
**weight placement**: a small asset for input-driven emulation (NARMA, +), a
liability for driven forecasting (MG, −), and a liability for closed-loop chaotic
generation on *both* stability and fidelity (Lorenz, −/−). Its **directed
topology** helps only the noisy input-driven task (NARMA) and is **neutral for both
autonomous tasks** (MG and Lorenz topology legs null). The single mechanistic
through-line is spectral: placing the connectome's heavy weights on its real
high-leverage edges maximally compresses the eigenvalue bulk, which is memory-poor
and richness-poor — punished by anything that must *sustain* dynamics autonomously,
and rewarded only where mildness happens to mean stability under broadband drive
(the NARMA supercritical robustness). The connectome is not a better reservoir; its
biological weight placement is, if anything, a handicap for world-model-style
closed-loop tasks.

**One open methodological lever (untested here).** Lorenz was run with `raw`
weights, for continuity with NARMA/MG. Diagnostic 4 showed `sqrt` ~halves the
placement penalty on MG; since Lorenz fidelity is governed by the same compression
axis, a `sqrt` connectome should reconstruct the attractor noticeably better, so
the *magnitude* of the Lorenz placement deficit is partly a weight-transform
artefact. The **sign and structure** of the result (placement-driven, topology
null, worse on both supercritically) would be expected to survive; the headline
should be read against the `raw` choice. Confirming this is a one-line switch
(`matrix_config.WEIGHT_TRANSFORM`) plus a re-run — a clean next step, not done.

---

## 5. One-line summary

Weight **placement** is the connectome's defining knob — **confirmed across all
three tasks**: its heavy weights on real hub edges maximally compress its spectrum
(Diagnostic 1), starving linear memory (Diagnostic 2) and dynamical richness; a
lighter `sqrt` tail ~halves it (Diagnostic 4). That single axis is a small asset
for input-driven emulation (NARMA +) and a liability for both autonomous tasks —
driven forecasting (MG −) and closed-loop chaotic generation (Lorenz −, on *both*
valid-prediction time and attractor-climate, refuting the predicted
fidelity-for-stability trade: the metrics agree). Directed **topology** buys
noise-robustness for NARMA only and is **neutral** for MG and Lorenz (both
autonomous topology legs null) — a real NARMA effect with no established mechanism.
At the canonical operating point the connectome is worse-or-equal on all three
tasks; any "advantage" is a supercritical-regime, NARMA-only phenomenon. The honest
headline: the connectome's real weight placement is a **handicap** for autonomous
world-modelling, not an asset.

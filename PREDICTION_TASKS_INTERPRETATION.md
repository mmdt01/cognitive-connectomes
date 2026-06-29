# Interpreting the C. elegans connectome-reservoir results: operating points, weight placement, and a robustness–performance trade-off

*Reference summary of four C. elegans connectome reservoir tasks — Jaeger **memory
capacity** (the foundational passive-memory probe), then NARMA-10 (input-driven
emulation), Mackey-Glass (driven forecasting), and Lorenz (closed-loop free-running) —
evaluated across a wide spectral-radius sweep. The connectome and a five-rung null
ladder are compared, plus a `connectome_weight_permuted` control that splits the effect
into **placement** (connectome vs control) and **topology** (control vs degree_rewire).
**Bottom line:** at the canonical operating point the connectome is worse-or-equal; in
the supercritical regime — once the sweep is wide enough to reach each variant's
operating point — the connectome is the **most robust** variant on every task: where the
disk-like nulls peak **sharply** and then collapse, the connectome rises slowly to a
**wide, flat plateau** that sits slightly below the nulls' peak but holds far into the
supercritical regime. That is a **robustness–performance trade-off**: the connectome
sacrifices peak height for a broad stable operating range. Three threads carry the
story: **weight placement sets the operating point** (it shifts the connectome's optimal
spectral radius higher — not a handicap); **directed topology is a separate,
task-dependent advantage** (helps memory and input-driven emulation, emerges for
forecasting, absent for autonomous generation); and the trade-off itself follows from
the connectome's **spectral heterogeneity** — a likely signature of biological
connectivity statistics (§5). Confidence flagged throughout.*

---

## 1. Design and why the sweep reaches sr = 4

Four tasks — Jaeger memory capacity (MC) plus the three prediction tasks — × three
realism conditions (v2a undirected-Gaussian, v2b directed-empirical, v2d
directed-signed) × a 7-variant ladder (connectome + placement control + 5 null rungs) ×
spectral-radius sweep `linspace(0, 4, 39)` × 10 seeds. The
placement control holds the connectome's exact topology and exact weight multiset but
permutes which edge carries which weight, so two comparisons decompose the effect:

- **Placement** = connectome vs control (topology + multiset fixed; only placement differs).
- **Topology** = control vs degree_rewire (placement randomised in both; only topology differs).

**Why sr = 4.** Every variant is normalised to a common operating point by scalar
top-eigenvalue rescaling (`W → (sr/|λ₁|)·W`). The connectome's heavy, hub-concentrated
weights compress its eigenvalue **bulk** the most — `bulk₉₅/|λ₁| ≈ 0.30`, vs `≈ 0.38`
for the control/degree and `≈ 0.46` for random — so under a scalar rescale its bulk
reaches the unit circle (criticality) only at a **higher nominal sr** than the
disk-like nulls. Each variant's bulk-critical radius is `sr_crit = 1/bulk₉₅_ratio`
(one over the committed spectral metric): connectome **≈ 3.3**, nulls **≈ 2.2–2.7**
(v2b). A sweep stopping near sr ≈ 2 therefore compares the nulls *at* their operating
point against the connectome *below* its own. Sweeping to sr = 4 lets every variant
pass through its operating regime, so the comparison is read **curve-vs-curve** rather
than at a single (misleading) matched sr.

*v2a is a spectral negative control — its variants are near-identical spectrally, so
placement and operating-point effects vanish there; the effects below are v2b/v2d
(directed) phenomena, with v2d (Dale signs) tracking v2b closely. Numbers are quoted
for v2b unless noted.*

---

## 2. The unifying observation: placement is an operating-point shift, not a handicap

Across all four tasks the **placement** leg (connectome vs control) traces the same
arc — the connectome looks **deficient at low–mid sr** and **reverses to
parity-or-advantage at high sr**, around its `sr_crit ≈ 3.3` (Cohen's d, + = connectome
better, * = Holm-significant):

| placement d (connectome vs control), v2b | sr ≈ 0.95 | sr ≈ 1.47 | sr ≈ 3.05 |
|---|---|---|---|
| Memory capacity   | −5.7* | −2.5* | **+3.5\*** |
| NARMA-10        | −3.7* | +1.7* | **+3.0\*** |
| Mackey-Glass h=84 | −1.8* | −2.5* | **+2.0\*** |
| Mackey-Glass h=300 | −0.2 | −0.7 | +0.5 |
| Lorenz VPT      | −1.2 | −2.0* | +0.7 |
| Lorenz climate  | +0.1 | −1.5 | +0.2 |

This is the signature of an **operating-point shift**: the connectome's compressed
bulk moves its memory/criticality optimum to a higher nominal sr, so at matched
low–mid sr it sits *below* its optimum (apparent deficit) while at its own operating
point the deficit vanishes or reverses. It is **not** a fixed performance handicap —
and **memory capacity** (§3), the most direct measure of near-unit-circle memory modes,
shows it most starkly: the connectome holds the **lowest** MC at canonical and the
**highest** deep in the supercritical regime, the largest reversal of any task.

---

## 3. Per-task results (wide sweep)

### Memory capacity — the foundational passive-memory probe
Feed white noise, train a ridge readout per lag to reconstruct `u(t−k)` from the state,
sum the squared correlations (higher = better). MC is the *direct* measure of how many
near-unit-circle modes carry memory, so the operating-point picture shows most cleanly
here. The connectome is the **lowest** at canonical (v2b MC 9.1; d **−6.3** vs degree at
sr 0.95) — its crushed bulk gives it the least memory at the point you would tune to. As
sr rises it climbs to a **flat plateau (~11) that holds from sr 2 to 4**, while every
disk-like null **peaks sharply (~12–13) near sr 1.2 and then collapses** (random
13.0 → 4.9 by sr 4.0). So the connectome **dominates the supercritical regime**
(connectome − degree d **+8.5** at sr 3) — not by a higher ceiling (its peak ~11.7 is
*below* the nulls' peaks ~12.3–13.0; its effective dimensionality is structurally lower)
but by **robustness**: a wide stable memory plateau where the nulls collapse. Both legs
reverse/emerge supercritically: placement d **−5.7 → +3.5** (canonical → sr 3); topology
(control vs degree) is ~0 at canonical and grows to d **+3.5** at sr 2.5 — a *large
emergent* memory advantage for the connectome's directed wiring (control and degree
share the same operating point, so this is genuine topology). In **v2a** (undirected,
minimal operating-point shift) the topology effect appears at modest gain — connectome
> degree d **+1.3** at sr 1.8 — **reproducing the project's foundational MC result**
(v2a/v2c: connectome beats degree_rewire supercritically, attributable to
clustering/modularity). MC thus recovers the original finding *and* reframes it as the
cleanest instance of the operating-point + robustness story.

### NARMA-10 — input-driven emulation
The connectome's NRMSE is **flat at ~0.55 across the entire [0, 4] sweep** — it is the
only variant that never destabilises. Every null, **including the placement control**,
climbs to ~0.80 supercritically. So supercritically the connectome **beats every
null**, and the margin widens in the tail (sr 4.0: connectome 0.59 vs nulls ~0.80).
Both axes favour it: placement reverses to a large advantage (d +3.0 at sr 3), and
**topology is a large advantage** (control vs degree d +4.3 at sr 1.47, +1.0 in the
tail). NARMA is noise-driven and prone to supercritical blow-up, and the connectome's
compressed-bulk **stability** is exactly what the task rewards.

### Mackey-Glass — driven forecasting (h = 84, h = 300)
The connectome's NRMSE **improves monotonically with sr** to the best of all variants
at its operating point — h=84: 0.15 → **0.03** by sr ≈ 3 (vs nulls degrading to
0.07–0.24); h=300: 0.49 → **0.34** (vs nulls climbing to 0.43–0.48). The placement leg
reverses from a clear deficit (d −2.5 at sr 1.47) to an advantage (d +2.0 at sr 3), and
a **topology advantage emerges in the tail** (control vs degree d +1.7 at sr 3, h=84)
that was invisible at low sr. MG is memory-limited; the connectome's memory peaks at
its higher operating sr, so once the sweep reaches it the connectome is the best
forecaster — and the most robust (nulls degrade past their own optima while it holds).
*(At each variant's own optimum the variants are roughly tied — ~0.02–0.03 at h=84 —
so the connectome's distinction is that its optimum sits at higher sr and it degrades
the least beyond it.)*

### Lorenz — closed-loop free-running (VPT, climate)
The connectome **recovers at sr ≈ 3.0–3.3** to **parity with the best structured null**
(degree_rewire): VPT 1.6 → ~4.6 (vs degree 4.6, control 3.1, random 2.6); climate
6.5 → ~2 (vs degree ~2.9; random *diverged* to 20+). It is the **most
divergence-robust** variant — **0 %** closed-loop blow-ups in v2b/v2d vs **26–31 %**
for random/ER. But here the **topology leg does not favour the connectome** in the tail
(control vs degree d ≈ −0.8 at sr 3 — degree-rewiring matches or beats the connectome's
own topology), and the placement leg only reaches parity (d +0.2–0.7, NS). So on the
autonomous task the connectome's structure is **sufficient and robust, but not
superior**.

---

## 4. What it means: the connectome's topology advantage, by task

Two separable axes:

- **Weight placement → operating point.** The connectome's real (heavy,
  hub-concentrated) weight placement maximally compresses its spectral bulk, which
  **shifts its optimal operating sr higher** — a *relocation* of where it works best,
  not a deficit. Grounded in the spectral metrics and the operating-point recovery on
  all four tasks (memory capacity makes it most explicit).
- **Directed topology → a separate, task-dependent computational advantage.** Holding
  weights fixed (control vs degree), the connectome's directed organisation *beyond the
  degree sequence* helps **where the task rewards memory or stability under drive**:
  **large** for memory capacity (d ~+3.5 supercritically) and input-driven emulation
  (NARMA, d ~+4.3), **emergent under strong drive** for forecasting (MG tail), but
  **absent** for closed-loop generation (Lorenz), where degree-preserving rewiring is as
  good. The pattern: topology helps the **retain-and-transform** tasks (MC, NARMA, MG)
  and not **autonomous generation** (Lorenz) — and in every case it **emerges
  supercritically**, invisible at the canonical point.

The **robustness through-line** is the connectome's most consistent edge: on every task
with a destabilising supercritical regime it has the widest stable operating range —
a flat memory plateau where nulls collapse (MC), flat NRMSE where nulls climb (NARMA),
best-and-holding where nulls degrade (MG), zero divergence where nulls blow up (Lorenz).
The same spectral compression that delays its recovery is what keeps it stable far into
the supercritical regime — developed as a trade-off in §5.

**For the tasks (and the JEPA north star).** The connectome is a **competitive, robust
predictive substrate**, strongest where prediction is **input-driven** (NARMA best, MG
best at its operating point) and **at parity** where it is **autonomous** (Lorenz ties
the best structured null). Its directed topology is a genuine asset for driven
prediction; for self-sustaining rollout — the world-model-relevant regime — it is
*sufficient and exceptionally stable*, but its specific wiring is not superior to a
degree-matched graph. The connectome-as-predictor story is therefore a
**robustness-and-competitiveness** story, not a dominance story.

---

## 5. The universal pattern: a robustness–performance trade-off, and its biology

All four tasks share one shape: **the disk-like nulls peak sharply and high over a
narrow gain window, then collapse; the connectome rises slowly to a wide, flat plateau
that is slightly below the nulls' peak but holds far into the supercritical regime.**
This through-line has a clean mechanistic cause, a plausible biological reading, and a
falsifiable prediction for other connectomes.

### The mechanism — synchronised vs graded criticality
The shape follows from spectral *heterogeneity*. A disk-like spectrum (the nulls) has
all eigenvalues at a similar radius (bulk ≈ top), so as the global gain is scaled **all
modes cross the unit circle together** — they reach the edge of chaos simultaneously (a
sharp performance peak) and destabilise simultaneously (a sharp collapse). The
connectome's spiked spectrum spreads eigenvalues across a wide range of radii (one large
λ₁, λ₂ ≈ 0.77, then a long compressed tail), so modes cross criticality **gradually**:
some subset always sits near the unit circle across a wide band of nominal sr → a wide
plateau, with no single sr where *everything* is optimal (lower peak) but none where
*everything* collapses (graceful degradation). Crucially the **same** structural feature
— heavy weights concentrated on hub edges — causes *both* signatures: it concentrates
dynamical "resources" into a few dominant modes (low effective dimensionality,
participation ratio ~137 vs ~239 → **lower peak**) *and* spreads the eigenvalue radii
(graded criticality → **wider range**). The lower ceiling and the robustness are two
faces of one cause.

So "robust" here means, precisely, **insensitive to the operating-point (gain)
parameter**: the connectome computes well over a broad range of spectral radii and
degrades gracefully, where the nulls need near-exact tuning to a knife-edge.

### A robustness–performance trade-off
Read as a trade-off: the nulls **specialise** — concentrate all eigenvalues at one
criticality for a high peak, payable only in a narrow window — while the connectome
**generalises** — spreads them, trading peak height for a broad stable operating range.
It is a specialisation–generalisation / peak–robustness axis, with biological
connectivity on the robust-generalist end. Which end is "better" is context dependent:
at a tuned operating point the nulls win; across un-tuned, fluctuating conditions the
connectome wins. *(Scope: we have shown robustness to **gain**; whether it extends to
robustness against noise or lesions is untested, though a broad stable dynamical regime
plausibly correlates.)*

### Biological intuition (interpretation, not demonstration)
The honest boundary first: this is a reservoir abstraction — the connectome is used as a
recurrent matrix with *imposed* weights and a *synthetic* task, not a model of
*C. elegans* computation. The claim is about what biological **connectivity statistics**
confer dynamically. With that boundary:

- **Real circuits have no global gain knob tuned to a sharp optimum.** They operate
  under neuromodulation, fluctuating input statistics, plasticity, noise, and
  development. A substrate sharply peaked at one precise gain would be fragile to all of
  that; a wide flat plateau is robust to it — the "**criticality without fine-tuning**"
  idea, where heterogeneous wiring keeps a network near-critical across a *range* of
  states rather than at a single tuned point.
- **The features that create the heterogeneity are canonical biology** — heavy-tailed
  (log-normal) synaptic weights, hub neurons, rich-club organisation. And the effect is
  **strongest in our most biologically faithful condition** (v2b/v2d, real directed
  empirical weights) and weak in the artificial one (v2a, Gaussian): *more biological
  substrate → more robust*, within our own data.
- It reads as a very biological bargain — **give up peak optimisation for graceful,
  generalising performance** across uncertain conditions, where the cost of catastrophic
  collapse is high. Brains may carry broad weight/degree distributions *because* this
  confers dynamical robustness, lower peak notwithstanding.

### Will it generalise to other connectomes?
The mechanism predicts **yes qualitatively, with magnitude set by directedness /
non-normality**. The driver is spectral heterogeneity from heavy-tailed weights + hubs,
which any biological connectome has — so the qualitative pattern (more robust than its
nulls, lower peak) should recur. But the *strength* depends on how compressed the
spectrum is, and we have an internal control for that: **our v2a (undirected) is the
symmetric analog**, and it shows a much weaker effect than the directed v2b/v2d
(connectome `sr_crit` ≈ 1.4 vs ≈ 3.3; topology d ~1.3 vs ~3.5). A **symmetric macro-scale
human connectome** (dMRI — a *normal* matrix, bulk tracks top, little compression) should
therefore behave like our v2a: the robustness effect present but **substantially
weaker**. The **directed cellular connectomes the scale row targets** (fly optic lobe,
mouse cortex), non-normal like *C. elegans*, should show the **strong** version. The
falsifiable prediction: *the effect scales with directedness / non-normality — strong for
directed cellular connectomes, weak for symmetric macro-scale ones* — which is partly why
the macro-scale human graph is held out of the main scale-row comparison (it confounds
scale with directedness/normality).

---

## 6. Caveats (load-bearing)

1. **Canonical point: worse-or-equal.** At a single fixed sr ≈ 0.95 the connectome is
   worse-or-equal on all four tasks; every advantage is supercritical and requires
   comparing variants at their operating points.
2. **Parity, not dominance, on the autonomous task.** Lorenz is a tie with the best
   structured null; the unambiguous win is robustness, not central-tendency
   superiority.
3. **The comparison axis is a commitment.** The picture rests on reading curve-vs-curve
   (operating-point-matched) rather than matched-nominal-sr — appropriate because the
   variants' spectra differ in shape, but a stated methodological choice, not a
   neutral default.
4. **Raw weights.** All tasks use raw synapse counts; a `sqrt` transform compresses the
   tail less, raising `bulk₉₅_ratio` and so lowering `sr_crit` — the connectome would
   recover at a lower nominal sr. Sign/structure expected to survive; the exact
   operating points are a weight-transform choice.
5. **Topology mechanism open.** *Why* the directed topology helps memory, NARMA and the
   MG tail but not Lorenz is characterised but not mechanistically pinned.
6. **Lower ceiling, not higher.** The connectome's *peak* performance is at or below the
   best null's peak (clearest on MC: peak ~11.7 vs nulls ~12.3–13.0); its supercritical
   advantage is a **crossover** — it holds while the nulls collapse — not a higher
   ceiling. The win is robustness, not raw capability.

---

## 7. One-line summary

Across all four tasks — memory capacity, NARMA-10, Mackey-Glass, Lorenz — the
connectome's heavy weight **placement** compresses its spectral bulk and **shifts its
optimal operating point to a higher spectral radius**, so its apparent supercritical
"deficits" are an artifact of comparing *below* that point. At its operating point it is
the **most robust** variant on every task: where the disk-like nulls peak sharply and
collapse, it holds a **wide flat plateau** — slightly below their peak but far more
stable — a **robustness–performance trade-off** rooted in its spectral heterogeneity (a
likely signature of biological connectivity). Its directed **topology** is a separate
advantage for memory and input-driven prediction that emerges supercritically and is
absent for autonomous generation. At the canonical point it remains worse-or-equal; its
edge is supercritical, operating-point-matched, and robustness-led — it trades peak
capability for a broad, biologically-plausible stable regime.

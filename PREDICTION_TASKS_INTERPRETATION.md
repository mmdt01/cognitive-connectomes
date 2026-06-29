# Interpreting the C. elegans prediction-task results: operating points, weight placement, and the connectome's topology advantage

*Reference summary of the three C. elegans connectome prediction tasks — NARMA-10
(input-driven emulation), Mackey-Glass (driven forecasting), and Lorenz (closed-loop
free-running) — evaluated across a wide spectral-radius sweep. The connectome and a
five-rung null ladder are compared, plus a `connectome_weight_permuted` control that
splits the effect into **placement** (connectome vs control) and **topology** (control
vs degree_rewire). **Bottom line:** at the canonical operating point the connectome is
worse-or-equal; in the supercritical regime — once the sweep is wide enough to reach
each variant's operating point — the connectome is the **most robust** variant,
**best on the two driven tasks** (NARMA, MG) and **at parity with the best structured
null on closed-loop Lorenz**. Two axes carry the story: **weight placement sets the
operating point** (it shifts the connectome's optimal spectral radius higher — not a
handicap), and **directed topology is a separate, task-dependent advantage** (strong
for input-driven emulation, absent for closed-loop generation). Confidence flagged
throughout.*

---

## 1. Design and why the sweep reaches sr = 4

Three tasks × three realism conditions (v2a undirected-Gaussian, v2b
directed-empirical, v2d directed-signed) × a 7-variant ladder (connectome + placement
control + 5 null rungs) × spectral-radius sweep `linspace(0, 4, 39)` × 10 seeds. The
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

Across all three tasks the **placement** leg (connectome vs control) traces the same
arc — the connectome looks **deficient at low–mid sr** and **reverses to
parity-or-advantage at high sr**, around its `sr_crit ≈ 3.3` (Cohen's d, + = connectome
better, * = Holm-significant):

| placement d (connectome vs control), v2b | sr ≈ 0.95 | sr ≈ 1.47 | sr ≈ 3.05 |
|---|---|---|---|
| NARMA-10        | −3.7* | +1.7* | **+3.0\*** |
| Mackey-Glass h=84 | −1.8* | −2.5* | **+2.0\*** |
| Mackey-Glass h=300 | −0.2 | −0.7 | +0.5 |
| Lorenz VPT      | −1.2 | −2.0* | +0.7 |
| Lorenz climate  | +0.1 | −1.5 | +0.2 |

This is the signature of an **operating-point shift**: the connectome's compressed
bulk moves its memory/criticality optimum to a higher nominal sr, so at matched
low–mid sr it sits *below* its optimum (apparent deficit) while at its own operating
point the deficit vanishes or reverses. It is **not** a fixed performance handicap.
The memory-capacity diagnostic foreshadowed this — the connectome's MC peaks
supercritically while the nulls' peak canonically — and the wide sweep is where that
prediction pays off on the tasks themselves.

---

## 3. Per-task results (wide sweep)

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
  not a deficit. Grounded in the spectral metrics, the MC spectral-shift, and now the
  operating-point recovery on all three tasks.
- **Directed topology → a separate, task-dependent computational advantage.** Holding
  weights fixed (control vs degree), the connectome's directed organisation *beyond the
  degree sequence* helps **where the task rewards it**: a **large** advantage for
  input-driven emulation (NARMA), an advantage that **emerges under strong drive** for
  forecasting (MG tail), but **none** for closed-loop generation (Lorenz), where
  degree-preserving rewiring is as good.

The **robustness through-line** is the connectome's most consistent edge: on every task
with a destabilising supercritical regime it has the widest stable operating range —
flat NRMSE where nulls climb (NARMA), best-and-holding where nulls degrade (MG), zero
divergence where nulls blow up (Lorenz). The same spectral compression that delays its
recovery is what keeps it stable far into the supercritical regime.

**For the tasks (and the JEPA north star).** The connectome is a **competitive, robust
predictive substrate**, strongest where prediction is **input-driven** (NARMA best, MG
best at its operating point) and **at parity** where it is **autonomous** (Lorenz ties
the best structured null). Its directed topology is a genuine asset for driven
prediction; for self-sustaining rollout — the world-model-relevant regime — it is
*sufficient and exceptionally stable*, but its specific wiring is not superior to a
degree-matched graph. The connectome-as-predictor story is therefore a
**robustness-and-competitiveness** story, not a dominance story.

---

## 5. Caveats (load-bearing)

1. **Canonical point: worse-or-equal.** At a single fixed sr ≈ 0.95 the connectome is
   worse-or-equal on all three tasks; every advantage is supercritical and requires
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
5. **Topology mechanism open.** *Why* the directed topology helps NARMA and the MG tail
   but not Lorenz is characterised but not mechanistically pinned.

---

## 6. One-line summary

Across all three prediction tasks the connectome's heavy weight **placement** compresses
its spectral bulk and **shifts its optimal operating point to a higher spectral
radius** — so its apparent supercritical "deficits" were an artifact of comparing
*below* that point; at its operating point it is the **most robust** variant, **best on
the driven tasks** (NARMA, Mackey-Glass) and **at parity with the best structured null
on closed-loop Lorenz**, while its directed **topology** is a separate advantage that is
**large for input-driven emulation, emerges for forecasting under strong drive, and is
absent for autonomous generation**. At the canonical point it remains worse-or-equal;
its edge is a supercritical, operating-point-matched, robustness-led phenomenon.

# Interpreting the C. elegans connectome-reservoir results: a sign × tail × topology factorial and a non-negativity-driven robustness

*Core reference for the four C. elegans reservoir tasks — Jaeger **memory capacity**
(passive memory), NARMA-10 (input-driven emulation), Mackey-Glass (driven
forecasting), and Lorenz (closed-loop free-running) — evaluated across a wide
spectral-radius sweep and a **7-condition factorial** that crosses weight **sign**
(balanced ± vs all-positive), weight **tail** (homogeneous gaussian vs heavy-tailed
empirical), and **topology** (undirected/normal vs directed/non-normal). **Bottom
line:** the connectome's supercritical robustness — the property that distinguishes it
from its null ladder — is driven **primarily by weight SIGN (the non-negative / Perron
structure of real synaptic weights)**, with heavy-tailedness a **secondary, task- and
topology-dependent** contributor and directedness **minimal** except for closed-loop
stability. This **supersedes** the earlier reading that "the effect scales with
directedness / non-normality": that contrast (gaussian vs empirical) silently
**conflated sign with tail**, and a sign control shows sign is the larger lever.
Confidence flagged throughout.*

---

## 1. Design: the 7-condition factorial

Every substrate is the same object — a weighted recurrent matrix `W` used as a fixed
echo-state reservoir with a trained linear readout — rescaled to a common operating
point by top-eigenvalue matching (`W → (sr/|λ₁|)·W`) and swept over
`sr ∈ linspace(0, 4, 39)`. Each condition is compared against a 5-rung null ladder
(rung 0 random → rung 4 modularity-preserving) plus a `connectome_weight_permuted`
**placement control** (exact topology + exact weight multiset, permuted onto edges),
n = 10 seeds.

The **weight axis decomposes into two orthogonal sub-factors**, crossed with topology,
giving a per-topology **ladder** gaussian → signed-empirical → empirical:

| key | topology | weights | sign | tail |
|---|---|---|---|---|
| `undirected_gaussian`  | undirected (normal) | symmetric gaussian | balanced ± | homogeneous |
| `undirected_empirical_signed` | undirected | symmetric empirical, random ± | balanced ± | heavy |
| `undirected_empirical` | undirected | symmetric empirical | **all-positive** | heavy |
| `directed_gaussian` | directed (non-normal) | asymmetric gaussian | balanced ± | homogeneous |
| `directed_empirical_signed` | directed | asymmetric empirical, random ± | balanced ± | heavy |
| `directed_empirical`  | directed | asymmetric empirical | **all-positive** | heavy |
| `directed_empirical_dale`  | directed | asymmetric empirical + Dale sign | ~all-positive (3.6% inhib.) | heavy |

Reading the ladder isolates each sub-factor cleanly: **gaussian → signed-empirical** is
the *tail* step (sign held balanced); **signed-empirical → empirical** is the *sign*
step (tail held heavy). `undirected_empirical_signed`/`directed_empirical_signed` carry the connectome's **exact**
heavy-tailed magnitudes with only the sign randomised, so they are one-variable sign
controls in the spirit of the placement control. `directed_empirical_dale` (Dale) is the biological anchor.

**Why the sweep reaches sr = 4, and the operating points.** Top-eigenvalue rescaling
pins `|λ₁| = sr`, but a variant's *bulk* becomes critical only at
`sr_crit = 1/bulk₉₅_ratio`. These differ sharply by **sign**, not directedness
(connectome, seed-averaged):

| | gaussian (signed) | signed-empirical | empirical (positive) |
|---|---|---|---|
| undirected `sr_crit` | 1.37 | ~2.1 | **2.95** |
| directed `sr_crit`   | 1.23 | ~1.8 | **3.32** (Dale 3.22) |

All-positive weights push the operating point to a much higher nominal `sr`; signing
the same magnitudes brings it most of the way back. So the sweep must reach sr ≈ 4 to
cover the positive conditions' operating regime, and comparisons are read
**curve-vs-curve**, not at a single matched `sr`.

*Naming: conditions use descriptive snake_case keys (renamed from the legacy `v2x`
labels). Old→new: `v2a`=`undirected_gaussian`, `v2ae`=`undirected_empirical`,
`v2ae_randsign`=`undirected_empirical_signed`, `v2bg`=`directed_gaussian`,
`v2b`=`directed_empirical`, `v2b_randsign`=`directed_empirical_signed`,
`v2d`=`directed_empirical_dale`. The project's experimental-history chain
(`v1 → v2a → v2c → v2b → v2d`) keeps its original phase labels as provenance.*

---

## 2. The central result: weight sign is the primary robustness driver

Across the passive and driven tasks the connectome's supercritical advantage over its
degree-preserving null (Cohen's *d*, + = connectome better) lives almost entirely in
the **all-positive-empirical** column, and **signing the exact same weights removes
most or all of it**:

**Memory capacity** (*d* at sr ≈ 4):

| | gaussian | signed-empirical | empirical (positive) |
|---|---|---|---|
| undirected | +1.0 | **+3.5** | **+9.0** |
| directed | +1.7 | **+0.2** | **+10.7** |
| Dale | | | **+8.9** |

**NARMA-10** (*d* at sr ≈ 3):

| | gaussian | signed-empirical | empirical (positive) |
|---|---|---|---|
| undirected | −0.1 | +0.5 | **+10.0** |
| directed | +2.0 | **+3.4** | **+8.1** |
| Dale | | | **+10.3** |

The pattern is consistent: the big effect is in the positive column; the sign step
(positive → signed) collapses it — **entirely** in some cells (MC directed +10.7 → +0.2)
and by ~60% in others (MC undirected +9.0 → +3.5); the gaussian column is ~flat.
Directedness (gaussian undirected vs directed) is small everywhere (~+1). So the
"gaussian vs empirical" contrast that the earlier framing read as "directedness /
non-normality" is really **sign, then tail, then (barely) directedness**.

### The mechanism: resisting a Perron collapse
A **non-negative** matrix has a large, isolated **Perron eigenvalue** far above a
compressed bulk. Under global-gain scaling its disk-like *nulls* (random/ER, also
all-positive) synchronise into that one mode and **collapse off a knife-edge**
supercritically — MC of the rung-0 null falls to **4.9** (directed) / **3.5**
(undirected) by sr = 4, from a peak near 13. The connectome's heavy weights, placed on
its real hubs, **spread its operating point** (higher `sr_crit`) so it rides through
where its all-positive nulls collapse — a wide flat plateau (~11) vs a sharp
peak-and-collapse. **Sign the weights** (balanced ±, mean → 0): the Perron mode
vanishes, the nulls no longer collapse (rung-0 MC holds ~13.6 in directed-signed), and
there is **nothing for the connectome to outlast** → the crossover disappears. The
robustness is therefore, precisely, **collapse-resistance in an all-positive substrate**
— which matters only because real structural weights *are* non-negative.

---

## 3. Spectral basis, and why the *nulls* peak highest in directed-signed

Two scale-invariant facts about the rescaled spectrum explain both the operating-point
shift and an initially surprising observation (the disk-like nulls attain the **highest
raw MC of any variant anywhere** in the directed-signed conditions):

- **Bulk compression tracks sign, ~2× the tail.** Holding magnitude fixed and flipping
  only sign moves `bulk₉₅/|λ₁|` from 0.73 → 0.37 (undirected) / 0.82 → 0.31 (directed);
  the heavy tail alone (signed) moves it far less. All-positive-homogeneous weights
  alone reproduce ~100% of the directed connectome's compression.
- **Girko's circular law sets the null MC peaks.** A random matrix whose entries are
  (a) **independent across the two directions** (directed → non-normal → *complex*
  eigenvalues filling a 2-D **disk**, not a 1-D real line) and (b) **zero-mean**
  (signed → no Perron spike) has eigenvalues spread ~uniformly over the unit disk. That
  packs the **most modes near the unit circle** — and near-critical modes are exactly
  what store delayed inputs. Measured directly on the rung-0/1 nulls:

  | condition | n_critical (modes near \|λ₁\|) | frac complex | eff. dim (PR) |
  |---|---|---|---|
  | directed gaussian | **22 / 29** | 0.92 (disk) | 260 |
  | directed signed-empirical | **14 / 20** | 0.93 (disk) | 243 |
  | undirected (any) | 5–10 | 0.00 (real line) | 190–210 |
  | all-positive (empirical/Dale) | **1** | 0.93 but Perron-spiked | 239 |

  Every non-directed-signed condition loses the disk: **symmetric** → eigenvalues
  collapse onto the **real line** (no rotational modes; the classic poor reservoir);
  **all-positive** → a **Perron spike over a crushed bulk** (n_critical = 1). Directed +
  signed dodges both → maximal near-critical modes → the highest MC. And the
  **least-structured** nulls (random/ER) realise the *cleanest* disk, so they peak above
  even rungs 2–4 and the connectome — the standard RC result that **unstructured random
  reservoirs are near-optimal for raw linear memory; structure trades memory for
  task-specific computation.**

**Consequence for interpretation.** The connectome is **never** the highest-performing
substrate — a directed-signed random reservoir beats it on MC. Its interest is
robustness *relative to a handicapped, all-positive null*. "The connectome is robust"
means "**non-negative connectome weights resist the collapse/divergence that afflicts
non-negative random matrices**," not "connectome structure is a better computer."

---

## 4. Per-task results (7 conditions)

### Memory capacity — cleanest instance of the sign mechanism
Positive-empirical shows the large crossover (undirected *d* +9.0, directed +10.7, Dale
+8.9); signing collapses it (directed → +0.2). The connectome's *peak* MC sits **below**
its nulls' peaks (directed_empirical 11.7 vs random 13.0) — the lower-ceiling half of the trade-off —
while the signed conditions have *higher* peaks (directed_empirical_signed 13.8, random 16.2): E/I-
style balance restores dynamical richness but removes the collapse-and-crossover
entirely. **Secondary tail residual is normal-gated** — it survives signing only in the
*undirected* cell (+3.5; its placement leg still reverses −6.4 → +3.9), and dies
directed (+0.2; placement stays negative).

### NARMA-10 — sign primary, but directedness earns a role
Same core: positive-empirical strong (+8 to +10), signing undirected → +0.5, directed →
+3.4. **The tail residual is directed-gated here — the mirror image of MC** (residual in
the directed cell, gone undirected). The failure mode is **graceful de-skilling, not
blow-up** (connectome divergence ~0%): nulls climb to NRMSE ~0.8–1.0 (= no better than
predicting the mean), and the **signed/gaussian directed nulls degrade *worse* (~1.0)
than the all-positive nulls (~0.8)** — the disk spectrum that maximised MC memory goes
effectively chaotic under continuous drive. Directedness matters more than for MC
(gaussian undirected −0.1 vs directed +2.0): NARMA rewards directed structure for
**stability under drive**. Dale is strongest (+10.3).

### Mackey-Glass — the weakest, most horizon-dependent signal
At **h = 84** the undirected column is cleanly sign-driven (positive +8.2, signed −0.1).
The directed picture is **messy and carries an honest metric caveat**: the *largest* *d*
is directed-**signed** (+9.2), but that is a **"the null fails harder" artefact** — under
teacher-forced drive the disk-spectrum directed nulls go chaotic (degree_rewire → 0.60–
0.92) while all-positive nulls stay accurate (0.06–0.15), inflating the connectome's
*relative* advantage. Reading the connectome's *own* curve is cleaner and recovers the
story: it holds its forecast supercritically only when heavy-tailed — positive best
(~0.03), signed-empirical holds (~0.1), **directed-gaussian fails outright (0.66 →
0.79)**. At **h = 300** (chaos-limited) the advantage **largely washes out** (*d* ~+0.6
everywhere): once the horizon exceeds the connectome's memory the edge evaporates. So MG
robustness is real at the easy horizon and fades at the hard one — the connectome is not
a better chaotic forecaster in general, it just holds its **memory-bounded** skill over a
wider `sr` range (its late operating point = the sign/Perron effect).

### Lorenz — pure robustness, parity on fidelity, non-negativity *required*
The primary axis is **closed-loop divergence**. The connectome has the **lowest blow-up
rate in every condition** (0% in all directed, 1–7% undirected-empirical, 52% only
undirected-gaussian), and the original directed_empirical headline reproduces exactly (connectome **0%**
vs random **26%** / ER **31%**). Two structural effects: **directedness strongly
stabilises rollout** (undirected blows up 52–77%, directed 0–31%), and the **all-positive
disk nulls are the most blow-up-prone** (the Perron mode is amplified by the output
feedback). But on **fidelity the connectome is at parity, not dominant** — VPT ~4.5 ≈
degree ~4.5 (*d* ≈ 0), climate ~2.5 ≈ degree (*d* ≈ 0–0.5) in the positive/Dale
conditions — reproducing the pre-existing "sufficient and robust, but not superior"
finding, unchanged by the sign controls. Uniquely, **non-negativity here is required for
the task to *function*, not merely for robustness**: signing collapses VPT from ~4.5 to
~0.5. (The eye-catching signed-condition *d*'s — VPT +3.3, climate −5.0 for dir emp± —
are comparisons *among poor performers* and VPT/climate disagree there; do not
over-read.)

---

## 5. Synthesis: what drives what

- **Weight sign (non-negativity / Perron structure) — the primary driver.** Consistent
  across all four tasks: it sets the operating-point shift, causes the disk-null
  collapse (MC/NARMA/MG) and closed-loop blow-up (Lorenz) that the connectome resists,
  and on the autonomous task is **required for the substrate to reconstruct the attractor
  at all**. Confidence: high (a one-variable sign control, spectrally grounded).
- **Heavy tail — secondary, and task-/topology-gated.** A real but smaller residual that
  survives signing in *one* cell per task, and the cell flips: **normal-gated for MC**
  (undirected), **directed-gated for NARMA/MG** (driven). Intuition (not pinned): passive
  memory rewards the symmetric hub spread; driven tasks reward directed hub structure
  that damps blow-up under drive.
- **Directedness — minimal for passive/driven skill, decisive for closed-loop
  stability.** ~+1 on MC/NARMA/MG, but on Lorenz it is the difference between ~50–77% and
  ~0–31% divergence. Non-normality helps *only* where the reservoir must sustain its own
  dynamics.
- **The connectome vs its nulls — robustness, not raw superiority.** It is never the
  best substrate at any task; its edge is collapse-/divergence-resistance in the
  biologically-real all-positive regime, and on autonomous fidelity it is at **parity**
  with a degree-matched graph. The apparent "wins" are the connectome outlasting a
  handicapped null, not out-computing a good one.

---

## 6. Biology, and the human-connectome prediction

The honest boundary first: this is a reservoir abstraction — imposed weights, synthetic
tasks, and an **all-positive (all-excitatory) recurrent matrix is not a realistic neural
circuit** (real dynamics have inhibition). With that boundary:

- **Non-negativity is a genuine property of structural connectomes.** Measured synaptic
  counts / streamline densities are non-negative; sign (E/I) is a separate Dale layer.
  So the driver we identify is a real feature of the data, not an artefact — but its
  *dynamical* relevance is strongest when the effective matrix stays ~non-negative.
- **It holds for *C. elegans* specifically.** The biologically-faithful Dale condition
  (`directed_empirical_dale`) is only **3.6% inhibitory** (26 GABAergic neurons), so it is effectively
  all-positive → keeps the Perron structure → keeps the effect (Dale ≈ directed_empirical throughout).
- **Clean cross-species prediction.** A more inhibition-heavy brain (mammalian cortex
  ~20% inhibitory) would push the effective matrix toward balanced signs → toward the
  disk regime → **weaker robustness, higher raw capacity**. Falsifiable if E/I-resolved
  connectomes are run.
- **Human structural connectome (Suárez 2021 dMRI SC) — prediction reversed and
  sharpened.** The original guess was "symmetric/normal → behaves like the weak
  undirected-gaussian case." That is **wrong**: the human SC is **non-negative and
  heavy-tailed**, i.e. the `undirected_empirical` (`undirected_empirical`) cell — which shows the **full**
  robustness effect here (MC *d* +9). So the human SC is predicted to show a **strong**
  robustness crossover, driven by the Perron mechanism, **independent of tail or
  directedness**. `undirected_empirical` (and its sign control) is the internal proof-of-concept, and the
  human run is the external test.

---

## 7. Caveats (load-bearing)

1. **Robustness, not dominance.** The connectome never has the highest raw performance;
   a directed-signed random reservoir beats it (Girko-optimal). Every advantage is a
   crossover against a collapsing/diverging all-positive null.
2. **Cohen's *d* confounds "connectome good" with "null bad."** Where the null fails
   catastrophically (MG directed-signed, some Lorenz signed cells) the *d* inflates or
   flips; read the connectome's own curve, and treat signed-cell effect sizes with care.
3. **The comparison axis is a commitment.** Curve-vs-curve at operating points, not at a
   single matched `sr` — appropriate because the conditions' spectra differ in shape, but
   a stated choice.
4. **All-positive is a modelling regime, not a realistic circuit.** The mechanism is
   about what non-negative connectivity *statistics* confer dynamically; the biological
   dynamical system has inhibition (partially captured only by the sparse Dale layer).
5. **Raw weights; scale is rescaled away.** Magnitude range (gaussian ~±4 vs empirical
   ~75) does not enter — top-eigenvalue rescaling divides it out; only sign and relative
   tail shape survive. A `sqrt` transform would compress the tail and lower `sr_crit`;
   sign/structure of the results should survive.
6. **Tail mechanism open.** *Why* the secondary heavy-tail residual is normal-gated for
   MC but directed-gated for NARMA/MG is characterised, not mechanistically pinned.

---

## 8. One-line summary

Across memory capacity, NARMA-10, Mackey-Glass, and Lorenz, the connectome's
supercritical robustness is driven **primarily by the non-negative (Perron) structure of
its weights** — which makes all-positive random nulls collapse (or, in closed loop, blow
up) at criticality while the connectome's heavy hub weights let it hold — with
**heavy-tailedness a secondary, task-and-topology-gated** contributor and **directedness
minimal except for closed-loop stability**. Signing the exact weights removes the effect;
a directed-signed random reservoir (a Girko-optimal disk) out-performs the connectome
outright. So the finding is **collapse-resistance conferred by non-negative connectivity
statistics**, biologically real for near-all-excitatory *C. elegans* (Dale ≈ all-positive)
— which reverses the earlier framing (it is sign, not directedness) and predicts the
non-negative human structural connectome should show a **strong**, not weak, version of
the effect.

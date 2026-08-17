# Act II — the spectrum decomposes the manifold

**Session 2 of the §4b sweep.** Read `report/CONVENTIONS.md` first. Canonical results
live in `TIER0_STATE_OF_PLAY.md`; canonical claims in `ACTION_PLAN_JOURNAL_ROADMAP.md` §1.

**The withdrawn phrase this act must not resurrect:** "generation tracks **trajectory
straightness**". Write **"capacity is gated by which dynamical regime the manifold is
in"** (`CONVENTIONS`). This is the act where it would come back, because Probe 3's own
code still carries it in a figure title, a docstring and a column name — see §5 item 4
for the full list. Curvature is a **bimodal regime indicator**, not a graded readout; the
graded account is explicitly on the roadmap's "what must NOT be claimed" list, where the
within-cluster residual is +0.145, the *opposite* sign to the graded story.

---

## 1. Claims register

Every claim this chapter makes, each with a figure and a source. The chapter is written to
this register, not the other way round.

| # | claim (one sentence, as it will appear) | figure | TIER0 § | artifact |
|---|---|---|---|---|
| A2.1 | The Perron mode is a **common mode**: it carries the time-average, and once the mean over time is removed the dominant `W` eigenmodes capture *less* of the remaining variance than a random orthonormal direction does (10 of 10 seeds at every `k` ≤ 5), reaching chance only by `k` ≈ 20. | F4a | §3.12(1) | `results/scale_448/manifold_alignment.parquet` |
| A2.2 | The connectome is the **least** common-mode dominated substrate despite carrying much the largest Perron root — `\|mean_state\|` 0.759 against the nulls' 0.949 to 0.989 at σ = 6 — because a large spectral gap lets the leading mode be driven hard without the bulk following. | F4b | §3.7, §3.12(1) | `saturation_diagnostics.parquet` |
| A2.3 | **Weight sign composition selects which structural basis the fluctuations occupy**: with non-negative weights the low-frequency graph harmonics lead, and once signs are balanced the `W` eigenmodes do. The claim is the *swap*, not the amount either basis captures. | F5 | §3.12(2) | `manifold_alignment.parquet` |
| A2.4 | **Variance-weighted dimensionality misses readout-relevant structure.** Both measures are exact sums of a per-direction weight over the same 2500 × 448 state matrix; the ridge weight is above 0.5 for 438 of 448 directions while two directions carry 95% of PR. | F6a | §3.12(3) | `covariance_spectra.parquet` |
| A2.5 | Against **measured MC** across seven substrates, `d_eff` orders the ladder at **+1.000** and PR at **+0.107**; pooled within-regime the pair is **+0.998** against **+0.308**. `d_eff` moves 5.5-fold over the same substrates while PR moves 16%. *(contribution 6)* | F6b, F6c | §3.12(3) | `probe3_deff.parquet` |

**Claims deliberately NOT made here** (and why):

- **"The manifold lives in low-frequency graph harmonics."** Overstates it, and `TIER0`
  §3.12 says so in terms. On the all-positive substrate *neither* basis captures much at
  `k` = 10 (0.04 to 0.17). A2.3 is the replacement and it claims only the ordering.
- **Anything about the four-variant ladder from Probe 2.** `manifold_alignment.parquet`
  holds `connectome` and `degree_rewire` only, at four spectral radii. F4a and F5 draw
  the connectome; the degree rung is used once, as a cross-check inside a caption, and
  neither figure may be read as a ladder result.
- **That sign-gating of the manifold transition is novel.** Largely pre-empted by Krauss
  2019; presented as **confirmatory** (roadmap, "what must NOT be claimed"). A2.3 is the
  one claim in this act that is deliberately not a contribution.
- **Any graded account of curvature or "trajectory straightness".** Withdrawn. No
  curvature quantity appears in F4, F5 or F6 at all — see §5 item 4 for where the
  language still survives in code.
- **Any claim at all about the *temporal* structure of the manifold**, which is the
  larger omission and is deliberate. `src/analysis/manifold.py` defines the manifold on
  two axes — spatial (PR, `d_eff`, entropy) and temporal (`mean_curvature`) — and Probe 1
  captures both across the full sweep. **Act II reports only the spatial axis**, for a
  reason that is a property of the substrate rather than a matter of scope: at `f` = 0 on
  the all-positive substrate, which is where every figure in this act sits, **curvature
  does not move.** Measured on this act's own capture, the Lorenz seed-median is flat at
  **0.261 rad for the connectome and 0.263 for Erdős–Rényi across the whole σ = 0 to 6
  sweep** (maximum 0.26 for both). There is no signal to draw. The variation Act III's
  prediction arm uses lives at `f` > 0, in a different capture. See §5 item 15 and the
  hand-over paragraph in §4.
- **That curvature is bimodal**, which is true but is **not** a task-independent property
  of the manifold and must not be stated as one here. On this act's 12,180 Lorenz cells
  the "between" band [0.6, 2.2] rad holds **0.82%**, reproducing `TIER0` §3.10's picture
  on an independent capture. On the same act's MC and NARMA-10 cells it holds **49.6%**
  and **45.0%** — no bimodality whatever. Curvature is a property of the manifold *and
  the input driving it*: Lorenz is a smooth low-dimensional signal, so the trajectory is
  smooth until the network flips to the period-2 branch, whereas white-noise-driven MC
  turns sharply at every step regardless. F12 states the bimodality on Lorenz and is
  right to; a general statement would not be.
- **That `d_eff` is a better measure *in general*.** The demonstration is empirical and on
  one task (MC) on one substrate family. Dambre 2012 is the parent bound and is cited as
  such; Clark 2025 collides on terminology and is distinguished, not claimed against.
- **That PR is wrong.** PR measures what it says it measures. The claim is that the
  quantity it measures is not the one a ridge readout can use, which is a statement about
  fit-for-purpose, not about correctness.
- **A mechanism for *why* the low-variance directions carry memory.** F6a shows that they
  clear the ridge floor and that MC tracks how many do. Nothing here explains what the
  information in them is.

---

## 2. Reproduction gate

Run before any figure work. A failed reproduction is the finding and stops the act.

**Verdict: PASSED.** Every `TIER0` §3.12 number returns at the precision it is published
to. Recomputed from the frozen `manifold_alignment.parquet`,
`saturation_diagnostics.parquet` and `probe3_deff.parquet` at `scale_448`. One published
number needed its aggregation recovered before it would reproduce (§2.1); one figure
*builder* was found to be on the wrong aggregation and is fixed in §3.

### 2.1 The Perron mode is a common mode (TIER0 §3.12 item 1)

Connectome, `human_empirical`, supercritical operating point sigma = 3.0526, `k = 1`.

| quantity | TIER0 | recomputed | agrees to |
|---|---|---|---|
| top `W`-eigenmode share of time-centred variance | 0.0001 | 0.000143 | 1 s.f., on the pooled median |
| random-orthonormal baseline | 0.0023 | 0.002316 | 2 s.f. |

**The aggregation is the pooled median over 3 tasks x 10 seeds (n = 30), and it had to be
recovered — `TIER0` does not state it.** It is the only aggregation that returns both
numbers. Per-task medians are 0.000642 (MC), 0.000030 (NARMA-10), 0.000098 (Lorenz)
against random baselines 0.002521 / 0.002455 / 0.002079, so the median of per-task
medians gives 0.000098 (-> 0.0001 ✓) but 0.002455 (-> 0.0025 ✗). MC alone — the task
every other Act II number is measured on — is 0.00064, **4.5x the quoted digit**, and
still 3.9x *below* its own baseline. The claim is direction, not magnitude, and it is
robust to the choice: **29 of 30 (task, seed) cells sit below their own random
baseline.** For scale, `1/N` = 0.002232, so the random band is at chance as expected.

See audit-log item 6 for why the *median* is load-bearing here and the mean must not be
substituted.

### 2.2 `d_eff` against PR, both against measured MC (TIER0 §3.12 item 3, contribution 6)

`task == "mc"`, `condition == "human_empirical"`, `spectral_radius >= 3.05`,
`alpha == 1e-6`. **350 rows: 7 variants x 5 sigma x 10 seeds**, exactly as
`FIGURE_LIST` specifies, and 1e-6 is confirmed the only alpha present under that filter.

| statistic | TIER0 `d_eff` | recomputed | TIER0 PR | recomputed | agrees to |
|---|---|---|---|---|---|
| ladder ordering vs measured MC (7 rungs, median per variant) | +1.000 | +1.000000 | +0.107 | +0.107143 | all published digits |
| within-regime, pooled (n = 350) vs measured MC | +0.998 | +0.998172 | +0.308 | +0.308132 | all published digits |
| range across the seven rungs | 75 to 413 | 74.769 to 412.940 | 1.19 to 1.38 | 1.1895 to 1.3821 | all published digits |

**These are four numbers, not two, and each pair has its own unit.** The ladder statistic
is a 7-point correlation over per-variant medians; the within-regime statistic is a
350-point correlation over cells. Quoting +0.107 against +0.998 mixes the PR value from
one with the `d_eff` value from the other. `TIER0` §3.12 and roadmap contribution 6 both
say so; this gate confirms all four independently.

**The rung-index control reproduces, and exposes a sign error.** Against the `rung`
column the pair is **-0.180 / -0.541**. `TIER0` §3.12 and `FIGURE_LIST`'s F6 flag both
write "-0.18 and +0.54": the magnitudes are right and **PR's sign is wrong in both** — PR
is *negatively* rank-correlated with the index, under every index definition tried
(`rung`: -0.541; position in `matrix_config.VARIANTS`: -0.607). Nothing rests on it, since
this is the number that must **not** be quoted, but it should be corrected. See audit-log
item 3.

Per-rung medians, which are the argument:

| variant | rung | `d_eff` | PR | MC |
|---|---|---|---|---|
| connectome | — | 412.94 | 1.3821 | 13.622 |
| weight-permuted | — | 223.13 | 1.2233 | 9.178 |
| random_gaussian | 0 | 81.32 | 1.2778 | 4.795 |
| erdos_renyi | 1 | 74.77 | 1.2859 | 4.577 |
| degree_rewire | 2 | 138.18 | 1.1895 | 6.797 |
| clustering_rewire | 3 | 260.32 | 1.2241 | 9.832 |
| modularity_rewire | 4 | 167.43 | 1.1909 | 7.452 |

`d_eff` moves **5.52-fold** (74.77 to 412.94 of N = 448) while PR moves **16.2%** (1.1895
to 1.3821) and MC moves 2.98-fold (4.58 to 13.62). That is the figure.

### 2.3 The basis-swap table (TIER0 §3.12 item 2)

Captured variance at `k = 10`, connectome, each condition at its own supercritical
operating point (`human_empirical` 3.0526, `human_empirical_signed` 2.5263,
`human_gaussian` 1.2632), seed medians over 10 seeds.

| task | condition | harmonics (TIER0) | wmodes (TIER0) | ahead |
|---|---|---|---|---|
| MC | all-positive | 0.0555 (0.056) | 0.0087 (0.009) | harmonics |
| MC | signed | 0.0171 (0.017) | 0.0598 (0.060) | wmodes |
| MC | gaussian | 0.0202 (0.020) | 0.0397 (0.040) | wmodes |
| NARMA-10 | all-positive | 0.0402 (0.040) | 0.0022 (0.002) | harmonics |
| NARMA-10 | signed | 0.0050 (0.005) | 0.5271 (0.527) | wmodes |
| NARMA-10 | gaussian | 0.0064 (0.006) | 0.8863 (0.886) | wmodes |
| Lorenz | all-positive | 0.1679 (0.168) | 0.0040 (0.004) | harmonics |
| Lorenz | signed | 0.0194 (0.019) | 0.0812 (0.081) | wmodes |
| Lorenz | gaussian | 0.0120 (0.012) | 0.5222 (0.522) | wmodes |

**Worst absolute deviation across all 18 cells: 0.00045.** The swap reproduces in all
three tasks.

### 2.4 `|mean_state|`, and the signed-median gotcha (TIER0 §3.7 table, §3.12 gotcha)

MC, `human_empirical`, seed medians. `TIER0` §3.12 warns that `mean_state` is signed with
an arbitrary sign and must be absolute-valued **before** aggregating.

| variant | TIER0 sigma = 6 | abs-then-median | median-then-abs (wrong) | TIER0 sigma = 2 | recomputed |
|---|---|---|---|---|---|
| connectome | 0.759 | **0.7590** | 0.6384 | 0.114 | 0.1142 |
| weight-permuted | 0.949 | **0.9486** | 0.5754 | 0.532 | 0.5319 |
| degree_rewire | 0.959 | **0.9594** | 0.9331 | 0.586 | 0.5856 |
| erdos_renyi | 0.989 | **0.9892** | 0.9876 | 0.593 | 0.5932 |

Both `TIER0` §3.7 rows return to all published digits. **The gotcha is worse than `TIER0`
states** — see audit-log item 1.

### 2.5 Integrity checks beyond the published numbers

| check | result |
|---|---|
| `alpha` in `probe3_deff` == the MC solver's `ridge_alpha` | identical, `1e-6`, and the *same dict* (§2.6 finding 1) |
| filter yields exactly the specified 350 rows / 7 variants / 5 sigma / 10 seeds | holds |
| `d_eff` recomputed from freshly regenerated states vs the frozen column | worst \|Δ\| = **7.5e-05** over 4 cells (the `float32` storage of `eig_gram`) |
| MC `eig_cov` and `eig_gram` are the same state matrix | holds: `captured_state_rows` == `T_effective` == 2500, `n_design_cols` == 448 (no bias) |
| time-centring removes the mean over time, not over units | holds; verified against `np.cov(rowvar=False)` to 3.3e-16 |
| MC per-lag Gram offset (`k = 0` reported, `k = 1..50` solved) | worst measured shift **0.816** `d_eff` units, 0.24% of the ladder range (§2.6 finding 3) |

### 2.6 Code audit

**Functions audited:** time-centring (`manifold.covariance_eigenvalues`,
`manifold._covariance`), Gram construction (`manifold.gram_spectrum`,
`spectra.design_matrix`, `memory_capacity._measure`), `manifold.participation_ratio`,
`manifold.ridge_effective_rank`.

**Findings:**

1. **The Gram is the ridge solver's own Gram, and `alpha` is literally the same value.**
   `spectra.capture_cell` takes `alpha = spec["params"]["ridge_alpha"]` from the *same*
   `params` dict it then passes to `spec["evaluate"]`, which is the call that produces the
   `mc` column. There is no second copy of the number to drift. For MC that value is
   `1e-6`, matching `human_mc/task_config.py`, `readout_config.json`,
   `covariance_spectra.parquet` and `probe3_deff.parquet`. `CONVENTIONS`' requirement that
   ridge `alpha` be identical in `d_eff` and MC is met by construction, not by
   coincidence. (NARMA-10 is at `1e-8` and Lorenz at `1e-7`; each task carries its own and
   F6 uses MC only.)
2. **Time-centring removes the mean over time.** `states` is `(T, N)` and both
   implementations subtract `states.mean(axis=0, keepdims=True)`, i.e. each *unit's* mean
   over time. Verified on a synthetic matrix with large per-unit offsets: after centring
   the per-unit (column) means are 8.8e-14 and the per-timestep (row) means are **not**
   zero (1.23), which is the correct direction; the offsets contribute nothing to the
   spectrum, and `covariance_eigenvalues` matches `np.cov(rowvar=False)` to 3.3e-16.
   `gram_spectrum` correctly does **not** centre — the ridge solver inverts the un-centred
   `A^T A`, and centring it would not be the readout's Gram.
3. **The MC design is per-lag and nested; `eig_gram` is reported at `k = 0`. Quantified
   here for the first time.** `readout_config.json` documents the offset ("representative
   of all lags to within `k/T_eff` rows") but nowhere is it measured. The solver's Gram at
   lag `k` is `G_0` minus a PSD rank-`k` term, so Weyl bounds the shift at
   `0 <= d_eff(0) - d_eff(k) <= k`, i.e. up to 50 units. Measured on real cells at
   sigma = 3.0526 (connectome seeds 0 and 1, ER seed 0, degree seed 0), the shift from
   `k = 0` to the deepest lag `k = 50` is **0.31 to 0.82 `d_eff` units** — 1.6% of the
   rigorous bound and **0.24% of the 75-to-413 ladder range**. The reported `d_eff` is a
   valid stand-in for every lag; the approximation cannot move the ordering.
4. **`participation_ratio` and `ridge_effective_rank` measure the same object two ways,
   on the same rows.** For MC the covariance and the Gram are formed on one and the same
   2500 x 448 post-warmup state matrix — PR on its time-centred covariance spectrum,
   `d_eff` on its un-centred Gram spectrum. The PR-vs-`d_eff` contrast is therefore a
   difference of *weighting*, not of data slice, which is exactly what contribution 6
   claims. (This is not true of NARMA-10, where 2800 rows are captured and 2000 enter the
   design; F6 does not use it.)
5. **`ridge_effective_rank` ridges the unregularised bias direction — harmless, and not
   MC's.** NARMA-10 and Lorenz set `reg[-1, -1] = 0` so the intercept is unpenalised,
   while `ridge_effective_rank` applies `alpha` to every Gram eigenvalue. The error is
   bounded by 1.0 `d_eff` unit and is in practice ~1e-12 (the bias column's Gram mass is
   `n_train` = 2000 against `alpha` = 1e-8). MC has no bias column, so F6 is untouched.

---

## 3. Figures

One block per figure ID from `FIGURE_LIST.md`. **Caption written before the figure.**

### F4 — the Perron mode carries the mean

- **Claim carried:** A2.1, A2.2
- **Source:** (a) source `alignment` = `results/scale_448/manifold_alignment.parquet`,
  no row filter at load; the panel selects `condition == "human_empirical"`,
  `variant == "connectome"`, `task == "mc"` and the larger of the two operating points
  Probe 2 captured (σ = 3.0526). (b) source `saturation` =
  `saturation_diagnostics.parquet` filtered to the four ladder variants; the panel
  selects `task == "mc"`, `condition == "human_empirical"` and the full 58-point sweep.
- **Panels:** (a) captured variance against `k` for the three bases, log-log, with the
  chance band; (b) `|mean_state|` against nominal σ for the four ladder variants, with
  the supercritical region shaded from the connectome's `sr_crit`.
- **`|.|` comes before the median, and this is not a detail.** `TIER0` §3.12 warns that a
  signed median shrinks the connectome's σ = 6 value from 0.759 to 0.638. It does worse
  than that: under median-then-abs the weight-permuted null reads **0.575**, *below* the
  connectome, and the panel would show the connectome as the second-least dominated
  substrate — arguing against its own caption. The builder asserts the connectome is
  lowest at the top of the sweep, so this fails the build rather than the reader.
  See §5 item 1.
- **Why the harmonics curve is in (a) at all**, when A2.1 is only about `W` modes against
  chance: without it, "the dominant modes are at or below chance" is uninterpretable —
  it could mean no structural basis aligns with the fluctuations. Harmonics sit **7.6x
  above** chance at `k` = 1 on the same data, so the shortfall is specific to the modes
  the Perron root belongs to, not a property of structural bases. It also hands F5 its
  starting point.
- **The chance band is the across-seed range of the per-seed 20-basis mean, not the
  across-basis s.d.** The comparison is paired per seed against the chance *mean*, so the
  band has to be that mean's spread (0.00136 to 0.00321 at `k` = 1). The spread of a
  *single* random direction is much wider — s.d. 0.0029 against a mean of 0.0025 — which
  is simply what one direction out of 448 does, is not the quantity being compared, and
  cannot be drawn on a log axis because the lower edge is negative. Stated in the caption
  rather than left as a silent choice.
- **The y floor is derived, not fixed.** A constant floor clipped F5a's first three
  points, which sit at 1e-4 to 2e-4. Both figures now set the floor from the smallest
  median they draw.
- **(b) draws all four substrates solid, and names them with `VARIANT_TITLE`.** Both were
  changed on the author's review after the figure was first built. The contract's
  per-variant dashes were encoding a distinction the curves' vertical separation already
  makes, and they broke up the two lines the panel is about; the override is **local to
  F4**, so no other act's figure moved. The plain names replaced `VARIANT_LABEL`'s rung
  numbering because the panel contrasts the substrates themselves rather than their
  ladder position — F2's case — and because at `VARIANT_LABEL` widths the legend is 3.85
  σ-units across and fits nowhere inside the axes. Audit items 11 and 12 carry the
  measured greyscale cost and the legend geometry.
- **The legend is placed by assertion, not by eye.** `_assert_legend_clear` measures the
  rendered legend box in data coordinates and fails the build if it covers a plotted
  point. It rejected two placements I had already argued for in a comment. A legend
  position is a geometric claim about the data, and the data moves; a comment about it
  survives the change that invalidates it, so the check is code.
- **This is not F11.** F11 carries the same `|mean_state|` numbers for contribution 3,
  from the `f`-extension parquets, **against `f` at σ = 6**. F4b is **against σ at
  `f` = 0**, from Probe 1's independent capture. `TIER0` §3.12 records that the two
  captures agree to three decimals at their shared point, which is a cross-validation
  rather than a duplication — and the caption says so. Session 3 owns F11; this session
  did not touch it.
- **Caption (final wording):**

  > **Figure F4. The Perron mode is a common mode: it carries the time-average, and the
  > fluctuations the readout uses are orthogonal to it.** Human N = 448 self-built
  > consensus, all-positive (empirical, `f` = 0) weights, memory-capacity task, 10 seeds.
  > **(a)** Fraction of the **time-centred** state variance captured by the top `k`
  > vectors of three orthonormal bases, at the supercritical operating point σ = 3.05
  > (medians over seeds; both axes logarithmic). Time-centring removes each unit's mean
  > over time, so what is left is the fluctuation subspace. In it the **dominant `W`
  > eigenmodes fall below chance**: 0.0006 at `k` = 1 against a random orthonormal
  > 0.0025, and below the random curve in **10 of 10 seeds at every `k` ≤ 5**. They reach
  > chance only around `k` = 20 and track it thereafter. The low-frequency graph
  > harmonics, on the same states, sit 7.6x *above* chance at `k` = 1, so this is a
  > property of the leading dynamical modes and not of structural bases in general. The
  > grey band is the across-seed range of the chance curve; a *single* random direction
  > is far more variable (s.d. 0.0029 about a mean of 0.0025 at `k` = 1), which is why
  > the comparison is made per seed against the chance mean rather than against one draw.
  > Pooled over the three tasks the leading mode holds 0.0001 of the fluctuation variance
  > against a 0.0023 baseline, which is the value of record (`TIER0` §3.12); the MC-only
  > figure here is 0.0006, still four-fold below its own baseline. **(b)** The
  > complementary half: the **common-mode amplitude** — the grand mean of the state
  > matrix over both time and units, `|x̄|`, absolute-valued per seed and then
  > seed-medianed — against nominal σ, for the connectome and its three nulls. The connectome is the **least** common-mode dominated
  > substrate at every σ above ~1.5 — 0.759 at σ = 6 against 0.949, 0.959 and 0.989 —
  > *despite* carrying much the largest Perron root (F1, F2). That is what the spectral
  > gap buys: the leading mode can be driven hard without the bulk following, so the
  > network never fully synchronises and tanh never fully saturates. The nulls rise first
  > because they become supercritical first, at `sr_crit` 1.81 to 1.92 against the
  > connectome's 3.08 (dotted). `mean_state` is signed with an arbitrary sign that
  > depends on the input realisation, so seeds are absolute-valued **before** the median;
  > taking the median first would report 0.638 here and reverse two of the four
  > substrates.

### F5 — sign selects the basis

- **Claim carried:** A2.3
- **Source:** source `alignment`; panels select `task == "lorenz"`,
  `variant == "connectome"`, one panel per `condition`, each at that condition's own
  supercritical operating point (3.0526 / 2.5263 / 1.2632, read from the data).
- **Panels:** (a) all-positive, (b) signed empirical, (c) gaussian. Same three curves as
  F4a, shared log y, a rule at `k` = 10 with both values in the corner. **One x label
  under the middle panel and one figure-level legend below all three**, rather than three
  copies of each: at this panel width an in-panel legend lands on the `k` = 10
  annotations it would sit beside. F2's treatment, for F2's reason.
- **The numbers sit in a corner box, not beside their markers.** Every curve converges on
  1.0 by `k` = N, so the lower-right corner is empty in all three panels, while the space
  beside a marker is on a steeply rising curve in at least one of them: a label that
  cleared the curve in (a) landed on it in (b). Measured on the render, not judged.
- **`k` = 10 is drawn because it is where `TIER0` §3.12's table is quoted**, not because
  anything happens there. The swap is visible across the whole curve; the rule exists so
  the figure and the table can be read against each other.
- **The task is Lorenz, per `FIGURE_LIST`.** The swap reproduces in MC and NARMA-10 too
  (§2.3) — Lorenz is the clearest, not the only, case, and the caption says so rather
  than letting one task look like the whole result.
- **Confirmatory, and labelled as such in the caption.** Krauss 2019 has the sign-gating
  of the manifold transition. This figure is included because Act II's argument needs the
  basis established before F6 uses it, not as a contribution.
- **Caption (final wording):**

  > **Figure F5. Which structural basis the fluctuations occupy is set by the weight
  > signs, not by the topology.** Fraction of time-centred state variance captured by the
  > top `k` vectors of each basis, connectome substrate, Lorenz task, N = 448, medians
  > over 10 seeds, each panel at its own condition's supercritical operating point.
  > **(a)** With **non-negative** weights the low-frequency graph harmonics lead
  > throughout and the dominant `W` eigenmodes run far below chance. **(b)** With the
  > **same empirical weight magnitudes** and balanced signs the ordering has already
  > reversed. **(c)** With **gaussian** weights the `W` eigenmodes dominate outright,
  > holding 0.52 of the variance in 10 of 448 directions. At `k` = 10 the pair runs
  > 0.168 / 0.004, then 0.019 / 0.081, then 0.012 / 0.522: **the ordering swaps and the
  > topology never changes.** What is claimed is the swap. On the all-positive substrate
  > neither basis captures much in absolute terms, so "the manifold lives in graph
  > harmonics" would overstate it — and the low capture is exactly what the other probe
  > predicts, since supercritical `d_eff` there is ~413 of 448 (F6), leaving the
  > fluctuations spread over hundreds of directions that no 10-vector basis can hold.
  > Where `d_eff` is low the capture is high, and the two probes agree on that without
  > being fitted to each other. The same swap holds for the degree-matched null
  > (0.168 / 0.002, 0.011 / 0.102, 0.011 / 0.355), which is the only other substrate this
  > capture covers; it is a two-substrate result and implies nothing about the null
  > ladder. Sign-gating of the manifold transition is largely pre-empted by Krauss (2019)
  > and is reported here as **confirmatory**, and because Act II needs the basis fixed
  > before asking how many directions the readout can use.

### F6 — variance-weighted dimensionality misses readout-relevant structure

- **Claim carried:** A2.4, A2.5 — **contribution 6.** The figure that travels furthest
  beyond this project, and the one written to be legible to a reader who has never seen a
  reservoir.
- **Source:** (a) source `gram_spectra` — **new this session**, see §5 item 2 — reading
  `covariance_spectra.parquet` at `task == "mc"`, `condition == "human_empirical"`,
  `variant == "connectome"`, σ = 3.0526, then the one seed whose `d_eff` is nearest the
  median of the ten. 448 rows, one per direction. (b, c) source `probe3` =
  `probe3_deff.parquet` at `task == "mc"`, `condition == "human_empirical"`,
  `spectral_radius >= 3.05`, `alpha == 1e-6` — 350 rows, 7 substrates x 5 σ x 10 seeds.
- **Panels:** (a) the per-direction weight each measure assigns, one cell, linear axes,
  with a zoom inset over the first twelve directions; (b) MC against `d_eff` and (c) MC
  against PR, per-substrate medians over 50 cells each.
- **(a) is the panel that carries the contribution, and it works because the two measures
  are *exactly* sums of per-direction weights.** `d_eff = Σᵢ gᵢ/(gᵢ+α)` is one by
  definition. PR is one too, less obviously: with `pᵢ = λᵢ/Σλ`,
  `Σᵢ pᵢ/Σⱼpⱼ² = 1/Σⱼpⱼ² = PR`. So each curve's **area is the number it is labelled
  with**, and the panel needs no reservoir vocabulary at all — it says "here are two ways
  of counting how many directions this system uses, applied to the same data; one counts
  to 431 and the other to 1.28." The builder asserts both areas against the frozen
  scalars, so the reading cannot silently become false.
- **Linear x, and an inset rather than a log axis.** A log x would make the variance
  weight visible but would destroy area-as-count, which is the panel's whole licence.
  Linear x keeps it and costs the variance curve its visibility — a sliver a pixel wide
  reads as a *missing* curve, not a small one. The inset is the same two quantities over
  directions 1 to 12 on the same linear axes, so area-as-count still holds inside it.
  No zoom connectors: the magnified region sits on the y axis, so they swept across the
  panel to point at its own left edge.
- **(a) is one cell and nothing median is drawn on it.** That is Act I audit item 13
  applied in advance: F1 mixed a single seed's spectrum with median reference lines and
  the defect survived several inspections. The cell is chosen by rule (nearest the median
  `d_eff` of the ten seeds at that σ), the rule lives in the source, and the seed is
  never named in code. Its `d_eff` is 431 and its PR 1.28; the **per-substrate medians in
  (b) and (c) are over all 50 supercritical cells**, so the connectome sits at 413 and
  1.38 there. The caption states the difference rather than leaving a reader to find 431
  in one panel and 413 in the next.
- **Panel widths are 40 : 30 : 30 and the two gaps are not equal.** (a) carries the
  argument and needs the width; (b) and (c) share one y axis, so the gap between them is
  closed to **0.27x** the (a)|(b) gap and (c) draws no y tick labels. A `subplots(1, 3)`
  has a single `wspace` and cannot do this, so the figure uses a five-column gridspec
  with two spacer columns — the asymmetry is structural rather than a nudge, and the
  rendered widths were measured back at 40.0 / 30.0 / 30.0. The gaps differ because they
  carry different furniture: (a)|(b) must clear panel (b)'s y label *and* its tick
  labels, (b)|(c) carries neither. Closing it is what makes the shared axis read as
  shared rather than as two panels that happen to agree.
- **(a)'s title is "one connectome cell", and that wording was chosen over a more
  descriptive one on purpose.** A title naming the substrate, task and σ was tried during
  the figure review and **reverted**: the substrate and task are the whole figure's and
  already sit in the caption's opening line, so a descriptive title spends the one line
  the panel has restating what is not in doubt. What a reader genuinely cannot recover
  from the panel is that (a) is a **single reservoir** while (b) and (c) are medians over
  fifty — and the two disagree visibly, `d_eff` 431 here against 413 for the same
  substrate in (b). Putting that in the title keeps the caveat in the figure rather than
  resting it on a caption sentence that a journal edit may cut. This is the
  mixed-aggregation trap of Act I items 5 and 13, and the cheapest guard against it is
  two words of title. σ = 3.05 moved into the caption, where it costs nothing.
- **Both (b) and (c) are zero-based, and that is the second half of the argument.** The
  headline correlations are +1.00 and +0.11, but a correlation says nothing about *range*
  — and the range is the mechanism. On zero-based axes the seven `d_eff` points spread
  across the panel while the seven PR points sit in a clump at the right, so
  "5.5-fold against 16%" is read off the figure instead of taken from the caption. This
  is F2's reasoning: an axis crop would have hidden exactly the quantity the figure
  exists to show. Panel (b)'s limit is the `d_eff = N = 448` ceiling required by
  `CONVENTIONS`, which is also the natural scale for a count of directions; panel (c)
  gets explicit ticks at 0, 0.5, 1.0 and 1.5, because with one labelled gridline the
  clump reads as a plotting failure rather than as a result.
- **Caption (final wording):**

  > **Figure F6. Memory lives in hundreds of low-variance directions, which a
  > variance-weighted measure discounts.** Memory-capacity task on the all-positive human
  > substrate, N = 448, supercritical (σ ≥ 3.05), ridge α = 1e-6 — the same α the readout
  > itself is solved with. **(a)** Both dimensionality measures are *exactly* sums of one
  > weight per direction of the state matrix, so each shaded area is the number beside
  > it. The ridge effective rank weights direction `i` by `gᵢ/(gᵢ+α)` — how far its Gram
  > eigenvalue clears the regularisation floor — and the participation ratio weights it
  > by `pᵢ/Σⱼpⱼ²`, its share of variance. On **one connectome cell** at σ = 3.05 the
  > ridge weight is above 0.5 for **438 of the 448 directions** and sums to
  > `d_eff` = 431, while the variance weight has collapsed by the fifth direction:
  > **two directions carry 95% of PR = 1.28** (inset, directions 1 to 12 on the same
  > linear scale). Both are computed
  > on one and the same 2500 x 448 post-warmup state matrix — PR on its time-centred
  > covariance, `d_eff` on the un-centred Gram the solver actually inverts — so the
  > difference is one of weighting, not of data. **(b, c)** The consequence, across the
  > seven substrates of Probe 3's ladder (medians over 50 supercritical cells each).
  > Against **measured** memory capacity, `d_eff` orders the ladder at `r_s` = **+1.00**
  > and PR at **+0.11**; pooled over all 350 cells the pair is **+0.998** against
  > **+0.308**. Both axes are zero-based, so the spread of the points is comparable
  > between the panels: over the same seven substrates `d_eff` moves **5.5-fold** (75 to
  > 413 of N = 448) while PR moves **16%** (1.19 to 1.38) and MC itself moves 3-fold
  > (4.6 to 13.6). Panel (a)'s cell is a single reservoir and its `d_eff` of 431 is that
  > cell's; the connectome's median over all 50 cells, plotted in (b), is 413. Both
  > correlations are against measured MC, never against the rung index, which is a
  > different quantity and is not the claim.

---

## 4. Section outline

Structure only, at the level of section headings and the argument each carries. Prose is
written by hand, not generated (see the roadmap §4b note on drafting).

**Chapter 5 — Act II proper.** The act sits between the two halves of the thesis: Act I
established what the spectrum *is*, Act III asks what it *buys*. Act II's job is the
bridge — to take the object Act I handed over, the Perron mode standing clear of a bulk,
and show what each half of that spectrum does to the activity the readout sees. It ends
by replacing the measure Act III will use.

1. **What Act I handed over, and the question it leaves.** One paragraph. `sr_crit` as
   the criticality scale each substrate carries with it; the Perron mode as the object to
   be decomposed. The question: a reservoir's readout sees a `T x N` state matrix, so
   which part of the spectrum ends up where in that matrix? No results.
2. **The probes, and what each can and cannot support.** Methods. The three captures
   (basis alignment, saturation diagnostics, covariance/Gram spectra), the operating
   points, and — stated up front, not in a limitations section — that Probe 2 covers
   **two** substrates at **four** spectral radii and therefore cannot speak to the ladder.
3. **The Perron mode carries the mean.** *Carries A2.1, A2.2.* Figure F4.
   1. Time-centring as the operation that separates the two, and what is left after it.
   2. The dominant modes against chance (F4a): below it to `k` = 5, at it by `k` = 20.
      The harmonics curve as the control that makes the shortfall mean something.
   3. The common-mode amplitude (F4b), and the inversion that is the real finding: the
      largest Perron root gives the *least* dominated substrate. Forward-reference to
      Act III, where this becomes the memory mechanism — the number is the same, the
      axis is not.
   4. The aggregation warning, stated once in methods: `mean_state` is signed.
4. **Sign composition selects the basis.** *Carries A2.3.* Figure F5. Deliberately short.
   1. The swap, in one paragraph and one figure.
   2. What it is not: neither basis captures much where weights are non-negative, and no
      claim is made about the ladder.
   3. Krauss 2019, and why this is here anyway — the basis has to be fixed before §5 can
      ask how many directions the readout uses.
   4. The agreement with Probe 3 that neither probe was fitted to: low `d_eff` goes with
      high capture. One paragraph, and it is the strongest thing in this section.
5. **How many directions can the readout use?** *Carries A2.4, A2.5 — contribution 6.*
   Figure F6. The chapter's argumentative peak.
   1. The two measures, defined as what they are: weighted counts over the same matrix.
      PR's identity `Σpᵢ/Σpⱼ² = PR` written out, because it is what licenses F6a.
   2. Why the difference is not academic (F6a): the ridge floor sits ten orders of
      magnitude below the leading variance, so hundreds of directions clear it while
      carrying almost none of the variance.
   3. The test (F6b, c): ordering against **measured** MC, at both aggregation units,
      with the rung-index control named and set aside.
   4. The range, which is the mechanism: 5.5-fold against 16%.
   5. Scope, stated in the text and not deferred: one task, one substrate family, one
      readout. Dambre 2012 as the parent bound; Clark 2025 as a terminology collision to
      be distinguished rather than a result to be claimed against.
6. **What Act II hands to Act III.** One paragraph, and it hands over **three** things,
   the third being a boundary rather than a result.
   1. The **common-mode account** of what supercriticality does to a non-negative
      substrate, which Act III's memory arm turns into a mechanism.
   2. **`d_eff`** as the dimensionality measure every later figure uses, now earned
      rather than assumed.
   3. **The temporal axis, and the fact that it is flat here.** This has to be said
      explicitly, in this chapter, and it is the one part of the hand-over that is easy
      to leave out. The manifold was defined on two axes and this act measured both;
      only the spatial one varies at `f` = 0, where curvature sits at 0.26 rad for every
      substrate across the whole σ sweep. Saying so converts a silent omission into a
      stated scope boundary, and it pre-loads Act III's prediction arm — which otherwise
      has to introduce curvature cold in chapter 6 *and* deliver two caveats at once
      ("it is a switch, not a dose" and "and at `f` = 0 it does not apply"). A reader
      who finished this chapter believing the manifold had been fully characterised
      would read that as a reversal instead of as a boundary they were warned about.
      **Do not let this become an appendix sentence**: it is the seam between the two
      halves of the thesis and it belongs at the end of chapter 5.

---

## 5. Audit log and open issues

Anything that did not reproduce, any number that moved, any claim that had to be weakened,
and anything a later session needs to know.

1. **F4b was built on the aggregation `TIER0` warns against, and it inverted the ladder.**
   The session-0 builder did `.groupby(...).mean_state.median().abs()` — median first,
   absolute value second. `TIER0` §3.12's gotcha says this shrinks the connectome's σ = 6
   value from 0.759 to 0.638. The consequence is worse than the gotcha states:

   | variant | abs-then-median (`TIER0`) | median-then-abs (as built) |
   |---|---|---|
   | connectome | **0.759** | 0.638 |
   | weight-permuted | 0.949 | **0.575** |
   | degree_rewire | 0.959 | 0.933 |
   | erdos_renyi | 0.989 | 0.988 |

   The weight-permuted null lands *below* the connectome, so the panel would have shown
   the connectome as the **second**-least common-mode dominated substrate and argued
   against its own caption and against `TIER0` §3.7. The maximum discrepancy over the
   sweep is 0.676 (weight-permuted, σ = 2.42). **Fixed**, and the builder now asserts the
   connectome is lowest at the top of the sweep, so a regression fails the build. The
   defect was invisible on three of the four curves — degree and ER move by 0.026 and
   0.001 — which is the same shape as Act I item 13: the rows that could show the problem
   were not the rows one checks.
2. **F6a needed a source that did not exist, and `FIGURE_LIST`'s F6 row has been updated.**
   `probe3_deff.parquet` carries `d_eff` and `pr` as scalars only. The mechanism panel
   draws the spectra they are summed from, which live in `covariance_spectra.parquet`.
   Added as source `gram_spectra` (pyarrow-filtered read, 0.21 s of a 27 MB file) with a
   placeholder; the `FIGURE_LIST` F6 source cell now names both files and which panels
   use which. The additions to `sources.py` and `style.py` are additive, and a full
   re-render of all 16 figures moved **only F4, F5 and F6** — verified by `git status`,
   not assumed.
3. **`TIER0` §3.12 and `FIGURE_LIST`'s F6 flag shared a sign error — CORRECTED.**
   Both wrote the rung-index control as "-0.18 and +0.54". Recomputed it is **-0.180 and
   -0.541**; PR is negatively rank-correlated with the index under every index definition
   tried (`rung` -0.541, position in ladder order -0.607). That `d_eff` matches exactly
   and PR matches in magnitude pins it as a transcription slip rather than a different
   computation. The magnitudes are right and nothing rests on the number — it is the one
   that must **not** be quoted — but two canonical documents stated a wrong sign, and a
   later session recomputing it would have had to work out which of the two was wrong.

   **Both corrected on the author's decision**, each carrying a dated note recording what
   it used to say. `TIER0` §3.12 now carries the recomputed pair with the alternative
   index conventions; `FIGURE_LIST`'s F6 flag points at it. This follows the precedent of
   session 0's `TIER0` §2.1 correction and session 1's `FIGURE_LIST` F3 correction: the
   generator of a wrong number is fixed in place, with the old value on the record.
4. **The withdrawn "trajectory straightness" survives in Probe 3's code, and in one
   rendered figure title.** Full list, in the order it should be fixed:

   | # | location | what it says | why it must change |
   |---|---|---|---|
   | 1 | `manifold/probe3.py:476-477` | figure suptitle "memory reads effective rank, generation reads **straightness**" | the withdrawn phrase, verbatim, **rendered into a committed PNG** |
   | 2 | `manifold/probe3.py:442-443` | docstring "the generative Lorenz task reads out **trajectory straightness**" | same phrase |
   | 3 | `manifold/probe3.py:472` | panel title "Generative axis: curvature → VPT" | the arrow asserts a graded mapping |
   | 4 | `manifold/probe3.py:467-469` | annotates the **pooled** curvature/VPT Spearman on the figure (frozen value **-0.84**) | the roadmap names the pooled -0.78 as cluster mixing; this plots the artifact as the result |
   | 5 | `manifold/probe1.py:35` | suptitle "Manifold curvature (**trajectory straightening**) vs spectral radius" | graded framing of a step function, on a continuous 0-to-π axis |
   | 6 | `src/analysis/manifold.py:16-21` | module docstring "how predictable motion along the manifold is", "lower = straighter = more linearly extrapolable" | the graded claim, in the shared metric module every act imports |
   | 7 | `src/analysis/manifold.py:168` | `mean_curvature` docstring "Lower = straighter = more linearly predictable" | same |
   | 8 | `manifold/probe3.py:102-104, 168, 264-275` | `dStraight`, labelled "Δstraightness", rank-correlated against a performance gap | a signed *continuous* gap in a bimodal indicator: the graded story in variable-name form |
   | 9 | `manifold/probe3.py:163-165, 193-194` | "does the geometry gap **track** the performance gap?" | dose language |
   | 10 | `manifold_probe3_summary.md` (generated) | publishes the -0.84 row and a `dStraight` column uncaveated | regenerates from the code above |

   **Out of scope, flagged and not touched:** `report/figlib/style.py:147`,
   `phase_diagram/analysis.py:11, 45, 51, 56` and `FIGURE_LIST`'s F16 row use `dStraight`
   as the generative-boundary key — Act III/IV's, sessions 3 and 4.
   `MANIFOLD_PROBES_IMPLEMENTATION.md:154-155, 200-201` is a tracked plan document that
   predates the withdrawal.

   **Explicitly must NOT change:** `src/analysis/manifold.py:334-338` and `:390`, the
   self-test comments ("straight motion should have ~0 curvature"). Those assert a
   mathematical property of the metric on synthetic data and are correct. Recorded so a
   later session does not over-correct them.

   **Items 6 and 7 are DONE; items 1 to 5 and 8 to 10 are not, deliberately.**

   *Done, in the shared metric module.* `src/analysis/manifold.py`'s module docstring and
   `mean_curvature`'s own now state the bimodality and name the graded account as
   withdrawn, with the +0.145 within-cluster residual and the 0.364-against-0.371 bit
   comparison. **The self-test comments were left alone**, per the "must NOT change" note
   above. Docstrings only: no behaviour, no signature, no rendered artifact moved.

   *Done at the same time, closing Act I's item 8.* That item flagged
   **`src/analysis/spectral.py`** — a *sibling* of `manifold.py`, not the same file; this
   act file previously conflated the two, and the earlier wording is corrected here. Its
   module docstring still asserted the withdrawn direction as fact ("more compressed bulk
   => milder effective dynamics"). It now reads "a larger spectral gap", states that the
   absolute bulk is near-identical across variants (4.4% at N=448), and names the
   division by `|lambda_1|` as what manufactures the appearance of compression. Act I
   deferred this to "when that file is next opened for a substantive reason"; that
   condition was **not** met this session — the Act II code audit read `manifold.py`, not
   `spectral.py` — so it was done on the author's decision rather than on the trigger.
   With it, the last place in the repo stating a withdrawn claim as fact is closed.

   *Not done, and why.* Items 1 to 5 and 8 to 10 all live in `manifold/probe1.py` and
   `manifold/probe3.py`, whose entry points rewrite the frozen parquets F6 reads (item 7
   below), and items 1 to 4 concern the *generative* axis — contribution 4, Act III's
   prediction arm, sessions 3 and 4. Rewording another act's figure titles is the
   cross-act edit `CONVENTIONS` warns against, and none of it is needed for F4, F5 or F6.
   The list above is the handover.
5. **Act I's item 8 called `src/analysis/spectral.py` "the last place in the repo that
   states the withdrawn direction as fact". It is not — there are six more.** Found by
   grepping for the phrase after fixing that file, i.e. the fix is what exposed the
   claim's scope. None was touched: all belong to other acts.

   | location | what it says | whose |
   |---|---|---|
   | `experiments/human/analysis/spectral.py:96` | written into the generated markdown: "Lower bulk₉₅/mean = more compressed bulk = milder effective dynamics" | Act I / session 1 |
   | `experiments/human/analysis/spectral.py:212` | stdout header "bulk95/\|λ₁\| (lower = more compressed bulk)" | Act I / session 1 |
   | `experiments/celegans/analysis/spectral.py:101, 176` | the same two, in the C. elegans twin of that module | Act IV |
   | `experiments/celegans/matrix_config.py:122` | comment, "the connectome's compressed bulk finally reaches criticality" | Act IV |
   | `experiments/celegans/celegans_lorenz/plot_sr_crit_overlay.py:5, 99` | module docstring and comment, same phrasing | Act IV |
   | `experiments/celegans/analysis/realizations.py:166` | "Perron + compressed bulk → signed spread" | Act IV |

   The first two are the ones that matter, because they are **written into a generated
   `.md`** rather than living in a comment, so the withdrawn direction is restated every
   time that summary is rebuilt. `experiments/human/analysis/eigenspectrum/figure1.py:232,
   253` also carries it, but as the *title of the committed E0.4 figure* that F1 exists to
   replace — Act I's F1 block quotes it deliberately, and it should be left as the record
   of what was superseded.
6. **The 0.0001 in `TIER0` §3.12 is a pooled-over-tasks median and the document does not
   say so.** It is the median over 3 tasks x 10 seeds (0.000143), against a baseline of
   0.002316. It is the only aggregation returning both published digits: the median of
   the per-task medians gives 0.000098 (→ 0.0001 ✓) but 0.002455 (→ 0.0025 ✗). **MC alone
   is 0.00064**, 4.5x the quoted digit. The claim's *direction* is robust — 29 of 30
   cells sit below their own baseline — but the **median is load-bearing**: one Lorenz
   seed at 0.0558 pulls the mean to 0.00217 against a random mean of 0.00232, so on means
   the "below baseline" statement is nearly degenerate. F4a therefore draws MC, quotes
   0.0006 for what it draws, and quotes the pooled 0.0001 as the value of record. Worth a
   line in `TIER0` §3.12 naming the aggregation.
7. **`probe3.run_deff` describes itself as "No reservoir runs" and rewrites
   `probe3_deff.parquet`.** Act I's item 11 found this and it bears repeating at the top
   of Act II's own log, because this is the act whose figures read that file: the
   docstring is true of *compute* and false of *artifacts*. Anything that needs Probe 3's
   plotting must call the private `_plot_*` functions directly, as
   `tools/replot_task_figures.py` does, and fingerprint the parquets either side. That is
   also why the language fixes in item 4 were not made by re-running the driver.
8. **The MC design is nested and `eig_gram` is reported at `k` = 0 — now quantified.**
   `readout_config.json` documents the approximation ("representative of all lags to
   within `k/T_eff` rows") but nobody had measured it. Weyl bounds the shift at
   `0 ≤ d_eff(0) - d_eff(k) ≤ k`, i.e. up to 50 units at the deepest lag. Measured on
   four real cells at σ = 3.0526 it is **0.31 to 0.82 `d_eff` units** — 1.6% of the bound
   and 0.24% of the 75-to-413 ladder range. F6 is unaffected and the note belongs beside
   `readout_config.json`'s claim.
9. **`ridge_effective_rank` ridges the unregularised bias direction.** NARMA-10 and Lorenz
   set `reg[-1,-1] = 0` so the intercept is unpenalised, while `ridge_effective_rank`
   applies α to every Gram eigenvalue. Bounded by 1.0 `d_eff` unit and in practice ~1e-12
   (the bias column's Gram mass is `n_train` = 2000 against α = 1e-8). **MC has no bias
   column, so F6 is untouched** — but session 3 or 4 quoting `d_eff` on NARMA or Lorenz
   should know the function is off by that direction's true contribution.
10. **`style.py` gained a basis/measure accent pair, after a monochrome version was built
    first and rejected on the author's review.** The constraint is real: Okabe-Ito has
    eight hues, the variant contract spends seven, and the eighth (#F0E442 yellow) is
    unusable on white — so a basis palette must either reuse a substrate colour, which
    F4 cannot afford because it draws bases in (a) beside variants in (b), or leave the
    wheel. The first build resolved that by going all-black and separating the three
    bases on dash and marker alone. **It was unreadable**: three near-identical curves in
    one panel, which is the whole content of F4a and F5. Safety against a collision had
    been bought by destroying the discrimination the figures exist to provide.

    **Resolved by leaving the wheel and measuring the result.** Candidates were scored on
    CIE76 ΔE in Lab after Viénot/Brettel dichromacy simulation, against three criteria at
    once — separation among the bases, distance from all seven substrate colours, and
    greyscale luminance separation:

    | palette | min ΔE among bases | min ΔE vs variants | greyscale ΔL |
    |---|---|---|---|
    | **indigo `#33356B` / brick `#A63603` (adopted)** | **50.8** | **11.5** | 14.5 |
    | violet / gold | 42.8 | 1.6 | 4.4 |
    | navy / rust | 35.9 | 7.3 | 15.7 |
    | petrol / crimson | 30.5 | 5.5 | 2.3 |
    | monochrome (as first built) | **0.0** | — | 0.0 |

    Indigo/brick dominates on all three simultaneously, which is why no trade-off had to
    be argued; every runner-up buys one criterion with another. Worst-case separation
    between any two basis curves under normal vision or any of the three dichromacies is
    50.8, against a just-noticeable difference of ~2.3. **Dash and marker were kept as
    well as hue**, so the encoding is redundant and the series still separate in
    greyscale — the monochrome version's one virtue, retained without its cost.

    `check_basis_palette()` re-derives both floors and is run by the smoke entry point
    beside `check_colour_consistency()`, so the palette cannot drift back into either
    failure. Floors are set *below* the measurement (25.0 and 8.0) so a later deliberate
    tweak need not reproduce these exact hexes, only stay legible and un-clashing.
    **The variant contract is untouched**: this is a namespace beside it, not an
    amendment to it, and `CONVENTIONS`' "report and stop" clause governs substrate
    colours, which these are not.
11. **F4b overrides the contract's per-variant dashes to all-solid, and that has a
    bounded greyscale cost worth recording.** On the author's review the mixed dashes
    (`-`, `-.`, `-`, `--`) were reading as a distinction between substrates that the
    curves' vertical separation already makes, and they broke up the two lines the panel
    is actually about. All four are now drawn solid, **locally in F4 only** —
    `VARIANT_LINESTYLE` is untouched, so F7, F9, F11 and every other act's figure keep
    the contract dashes. If plain solid is wanted thesis-wide, that is a cross-act
    decision for sessions 3 and 4, not one this act can take.

    **The cost, measured.** `CONVENTIONS` justifies Okabe-Ito partly on the grounds that
    it "separates by luminance in greyscale". For the four-rung ladder that is only
    partly true:

    | substrate | hex | CIE L* |
    |---|---|---|
    | connectome | `#000000` | 0.0 |
    | degree-matching | `#0072B2` | 46.0 |
    | weight-permuted | `#D55E00` | 54.2 |
    | Erdős–Rényi | `#009E73` | 57.7 |

    Weight-permuted against Erdős–Rényi is **ΔL\* = 3.6** — indistinguishable in
    greyscale. The dashes were the only thing separating that pair in print, and solid
    lines lose it. **The cost is bounded and does not touch the claim**: F4b asserts that
    the connectome sits lowest and the three nulls bunch high, and the connectome is
    black at L\* 0 against nulls at 46 to 58, so the one contrast the panel rests on is
    the most greyscale-robust one available. Telling the three nulls apart from each
    other is not something the panel claims. Worth flagging that `CONVENTIONS`' greyscale
    sentence is stronger than the palette supports for this quartet.
12. **F4b's legend is placed by assertion, and the first two placements were wrong.**
    `_assert_legend_clear` measures the rendered legend box, converts it to data
    coordinates and checks every drawn point against it, so a legend sitting on a curve
    fails the build. It earned its keep immediately. Upper-left (as first built) sat on
    the nulls' rise; lower-right *also* failed, because at `VARIANT_LABEL` widths the box
    is **3.85 σ-units across — two thirds of the panel — and there is nowhere inside the
    axes it does not cover a curve.** Both were placements I had reasoned about in a
    comment and got wrong.

    Fixed by shortening the labels to `VARIANT_TITLE`'s plain names, which is
    independently the right scheme here: the panel contrasts the substrates themselves
    rather than their ladder positions, which is exactly the case F2 adopted plain names
    for. The `σ_crit` rule label was rotated hard against its own rule (F6b's idiom) to
    clear the corner the legend now occupies. **The two empty regions were measured, not
    judged**: below σ = 1.35 every curve is under 0.002 but the strip is far too narrow
    for these labels; right of σ = 3.2 the lowest curve is 0.373, and that box takes it.
13. **`style.draw_ceiling` gained an `on` argument.** F6 plots `d_eff` on x, where the
    existing `axhline` would have marked nothing. Default is `on="y"`, so F3
    (`act1_structure`) and F7 (`act3_memory`) take the identical path; both were
    re-rendered and are byte-identical.
14. **`--smoke` now distinguishes structural from content assertions.** F4, F5 and F6
    assert their claims (the W-modes are below chance; harmonics lead only where weights
    are non-negative; the connectome is least dominated). Those are claims about the
    frozen result, so they are skipped on placeholder data. The **arithmetic**
    assertion — that the area under each F6a curve equals the frozen scalar it is
    labelled with — is *not* skipped, and the `probe3` / `gram_spectra` placeholders were
    made mutually consistent so it runs under `--smoke` too. A placeholder that carries no
    claim should still exercise the maths.
15. **Act II reports one of the manifold's two axes, and the reason is the substrate, not
    the scope — FOR SESSION 4.** Raised on the author's review: the act called "the
    spectrum decomposes the manifold" produces no figure of trajectory curvature, which
    Act III's prediction arm then depends on. Investigated rather than assumed, and the
    answer is more decisive than the framing arguments that were already on record:

    | check, on this act's own Probe-1 capture (36,540 cells) | result |
    |---|---|
    | Lorenz curvature at `f` = 0, all-positive, connectome | **flat at 0.261 rad**, σ = 0 to 6, max 0.26 |
    | same, Erdős–Rényi | **flat at 0.263 rad**, max 0.26 |
    | Lorenz cells in the "between" band [0.6, 2.2] rad | 0.82% (n = 12,180) |
    | **MC** cells in the same band | **49.6%** |
    | **NARMA-10** cells in the same band | **45.0%** |

    Two conclusions. First, **at Act II's operating point the metric is a constant** —
    there is nothing to draw, and this is `TIER0` §3.11's scope limit confirmed on an
    independent capture. Second, **the bimodality is Lorenz-specific**, not a property of
    the manifold: curvature is a property of the manifold *and* its input, and on the two
    noise-driven tasks roughly half the cells sit in the band that Lorenz leaves empty.
    The 0.82% here against §3.10's 0.56% is a different population (this act's 58-σ grid
    against E0.1's Jacobian capture), not a disagreement.

    Those reasons sit *upstream* of the two already on record — that §3.9 withdrew the
    two-axis framing, and that F12 owns curvature under the cap. Even with a free figure
    slot and no withdrawn language, there would be nothing to plot.

    **What was done:** no figure, and none proposed. The omission is now stated in §1's
    "claims deliberately NOT made" and handed over as the third item of §4's hand-over
    paragraph, so the boundary is declared in chapter 5 rather than discovered in
    chapter 6. **What session 4 should know:** F12 introduces curvature to a reader who
    has met the manifold but not this axis, and must carry both caveats itself. If the
    prediction arm ever wants an Act II-side run-up, the data for it is the `f` > 0
    phase-diagram capture, not any Probe 1-3 artifact, and it would need a cap slot.
16. **E1 — the two curvature regimes made visible. Not built here; handed to session 4,
    ranked below E2.** The natural follow-up to item 15: a trajectory plot showing a
    smooth orbit against an antiparallel zig-zag, i.e. what curvature's two spikes *look
    like*. It would give Act II the temporal intuition item 15 says it currently hands
    over as a boundary rather than a result, and it would do it in the chapter where the
    manifold is decomposed rather than in the chapter that needs it.

    **Ownership, and a mistake worth recording.** This was first written as "an option for
    this act", which gave it **no owner**: Act II is session 2, session 2 is the one
    closing, and an option parked in a finished act can only evaporate — the exact failure
    the E2 specification was written to prevent, reproduced a paragraph later. Corrected:
    **session 4 builds it** (it owns curvature, F12 and contribution 4), the figure would
    **print in chapter 5**, and it lives in `figures/act3_prediction.py` as a **cross-act
    figure** with `FIGURE_LIST` naming its owner explicitly — the F3 and F16 arrangement,
    not a new one. Act II does not own it and this session did not build it.

    **What it must not be drawn from.** Not `f` = 0 on the all-positive substrate — the
    condition every current Act II figure uses — where curvature is flat at 0.26 rad
    across the whole σ sweep. It needs the **signed or gaussian** columns, which this
    act's own capture holds and which do transition, or `f` > 0 from the phase-diagram
    capture.

    **Why it is an option and not a plan.** Three costs, none fatal and none free. States
    are not persisted, so it needs a regeneration pass. It needs its own builder, which
    means it goes **through the cap** rather than qualifying as a supplementary figure
    under `FIGURE_LIST`'s bar ("no claim the main text does not already make, and an
    existing builder at different parameters") — and the cap is 15 and full. And the
    claim it would carry, that curvature is bimodal, is F12's and belongs to contribution
    4, so an Act II version is an illustration of someone else's result unless it is
    scoped to the *manifold* reading rather than the VPT one.

    **Constraint inherited from the E2 work-up** (roadmap §4d): a top-3 PCA trajectory is
    faithful to 96-99% of the fluctuation variance but is nearly substrate-invariant
    (PCs-to-95% is 2 for every rung on MC, 3 on Lorenz, while `d_eff` spans 75 to 413).
    **A trajectory figure in this act may not be captioned as the subspace the readout
    computes in** — that contradicts F6, which is this act's own contribution. If E1 is
    built it shows a *regime*, not a capacity.

    Roadmap §4d carries both this and E2; E2's full specification is in
    `report/act3b_prediction.md` §6, addressed to session 4.

# Act III (prediction arm) — geometry gates predictive capacity

**Session 4 of the §4b sweep.** Read `report/CONVENTIONS.md` first. Canonical results
live in `TIER0_STATE_OF_PLAY.md`; canonical claims in `ACTION_PLAN_JOURNAL_ROADMAP.md` §1.

**Two phrases must never come back in this half**, because this is the chapter where each
would return:

| withdrawn | what replaced it |
|---|---|
| "`σ_eff` crosses 1 at the generative transition" | **`σ_eff` is the best empirical locator, and the unit crossing is falsified.** Two independent grounds: 1 of 38 brackets contains 1, the transition sitting at 0.77–0.90 for every variant; and `σ_eff` *folds*, so its maximum over the sweep is below 1 for every variant at `f` ≤ 0.20 while transitions happen throughout. Write "locator", never "criterion" or "law". **Draw no line at 1** |
| "generation tracks trajectory straightness" | **capacity is gated by which dynamical regime the manifold is in.** Within the smooth cluster the residual rank correlation is **+0.145**, the *opposite* sign to a graded account; the pooled −0.78 was cluster mixing. And the whole statement is scoped to `f` > 0 |

---

## 1. Claims register

Every claim this chapter makes, each with a figure and a source. The chapter is written to
this register, not the other way round.

| # | claim (one sentence, as it will appear) | figure | TIER0 § | artifact |
|---|---|---|---|---|
| A3P.1 | **Generation is gated, not graded**: curvature is a two-spike distribution with 216 of 38,280 cells (0.56%) between the modes, so a binary collapsed-or-not bit explains **R² = 0.364** of VPT variance against continuous curvature's **0.370** — the whole 0.25 → 3.14 rad range is worth 0.7 percentage points beyond the bit. | F12a, F12b | §3.10 | `e01_jacobian_scale_448.parquet` |
| A3P.2 | **A graded straightness account is not merely unsupported but wrong-signed**: within the smooth cluster the residual Spearman correlation is **+0.145** (n = 15,866), and within the collapsed cluster, excluding the 67% at the VPT floor, **−0.151**. | F12c | §3.10 | same |
| A3P.3 | **Read as VPT the generative advantage is real and it is a weight-placement effect**: at σ = 2 the connectome leads all three nulls by **+1.0 to +2.2** Lyapunov times from `f` = 0.25, clearing the weight-permuted placement control, and is the only substrate still predicting (1.3–2.8 against 0.1–0.9). | F13a, F13b | §2.6 | `e03_frontier_scale_448.parquet`, `e03_frontier_paired_scale_448.csv` |
| A3P.4 | **The advantage exists at the biologically real cut, far supercritically**: at `f` = 0, σ ≈ 7.6–8.0, Erdős–Rényi collapses to period-2 in **5 of 10 seeds** and the connectome in **0 of 10** (Fisher exact *p* = 0.033). The earlier "onset in `f`" reading was an artifact of stopping the sweep at σ = 6; the onset is in σ. | F13c | §2.3 | `item2_collapse_loci_scale_448.csv` |
| A3P.5 | **`σ_eff` is the best empirical locator of the transition and is not a stability law**: robust CV **0.209** against nominal σ's 0.667 and `σ·bulk95`'s 0.746, with the pre-registered variant-dependent offset present and ordered by spectral gap (connectome [0.71, 0.82] lowest, ER [0.87, 0.95] highest) — but 1 of 38 brackets contains 1 and the transition sits at 0.77–0.90. | F14 | §3.10 | `e01_threshold_invariance_scale_448.csv`, `e01_threshold_table_scale_448.csv` |
| A3P.6 | **The two advantages occupy opposite regions of the (`f`, σ) plane, and the boundaries cross once inside coverage**: at (`σ·bulk95` = 2.938, `f` = 0.153) on the matched-bulk axis, and **not at all** on the nominal axis once the sweep passes σ = 6. | F16 | §2.3 | `e02_heatmap_boundaries_extension*.csv` |
| A3P.7 | **The connectome's free-run attractor keeps the true Lorenz climate to a higher `f` than the nulls do**: 0.43 of cells against the nulls' 0.14 at `f` ≥ 0.30, σ = 2. Pre-registered before the capture existed. | F17a, F17b, F17d | new (E2) | `e2_free_run_scale_448.parquet`, `e01_jacobian_scale_448.parquet` |
| A3P.8 | **The closed-loop failure is a collapse of scale onto a fixed point, not a distortion of shape** — which **refutes** the second clause of E2's pre-registration and confirms §3.9's fixed-point branch in the closed loop. `sd_ratio` is bimodal: 229 of 440 cells below 0.05, 158 between 0.90 and 1.10, 11 anywhere between. | F17c, F17e | new (E2), bears on §3.9 | `e2_free_run_scale_448.parquet` |
| A3P.9 | **What sets generation at `f` = 0 is open.** Not geometry (curvature flat at 0.26 rad while VPT falls ~10×), not the locator (ER transitions at `σ_eff` = 0.014, on the descending branch), not memory (the connectome has ~4.7× ER's MC at σ = 6 and slightly *lower* VPT). | prose; §5 item 6 | §3.10, §3.11 | `e01_jacobian_scale_448.parquet`, `e03_frontier_scale_448.parquet` |

**Claims deliberately NOT made here** (and why):

- **"`σ_eff` crosses 1."** Falsified on two independent grounds (A3P.5). F14 draws the
  0.77–0.90 band and the builder asserts that no reference line is drawn at 1.
- **A graded straightness account.** A3P.2 is the data saying so, and the sign is wrong,
  not merely the magnitude.
- **That the single-axis account explains generation at `f` = 0.** It demonstrably does
  not. A3P.9 states it as a named open problem in the discussion, per roadmap §1's
  "what must NOT be claimed".
- **Any generative statement without its σ.** The `f` = 0 advantage is far supercritical
  (σ ≈ 7.6–8.0); there is *no* VPT advantage near criticality at `f` = 0 (+0.28, −0.01,
  +0.44, none significant). Written without the σ the two read as a contradiction.
- **The crossing quoted bare.** Always (`σ·bulk95` = 2.938, `f` = 0.153), always named as
  the first crossing inside full replicate coverage, always with the statement that the
  nominal axis has none past σ = 6.
- **Anything read off F16's uncovered region.** Five further crossings exist between
  x = 3.5 and 4.3; they are one oscillation of a boundary resting on a `bulk95`-selected
  subsample, and their number and position are not quantities.
- **Any per-cell `climate_error` value.** It is chaotic in the BLAS reduction order over
  the 81.5 Lyapunov times of the rollout (§2.6 finding 5). Seed medians and rates only.
- **A PR-versus-`d_eff` statement on NARMA-10.** Its captured states and its design matrix
  are different row sets (2,800 against 2,000), which is why F6 is MC-only. §5's bridge
  paragraph says so rather than quietly transferring the claim.

---

## 2. Reproduction gate

### 2.0 What a "cell" is, since every number in this act is counted in them

A **cell** is one row of the capture: one complete Lorenz evaluation of one reservoir at
one operating point. It is the unit F12, F13, F14 and F17 all plot, and the unit every
count in the gate table below is expressed in, so it is worth stating once rather than
leaving a reader to infer it.

A cell is keyed by five coordinates:

| coordinate | values | what it changes |
|---|---|---|
| `variant` | 4 | which substrate: connectome, weight-permuted, degree-matching, Erdős–Rényi |
| `f` | 11 (0 to 0.50, step 0.05) | the fraction of edges given a negative sign |
| `spectral_radius` σ | 29 (0 to 11.2, step 0.4) | how hard `W` is driven |
| `seed` | 10 | the null instance, `Win`, and the Lorenz initial condition |
| `draw` | 3 | which stratified realisation of the sign-flip pattern |

4 × 11 × 29 × 10 × 3 = **38,280**, which is the cell count `TIER0` §3.10 quotes.

**What happens inside one cell.** Build the reservoir from that (`variant`, `f`, `seed`,
`draw`) matrix, rescaled to σ; teacher-force 10,000 Lorenz steps to get a 10,000 × 448
driven state matrix, from which `mean_curvature`, `σ_eff`, `mean_state` and
`frac_saturated` are read; fit the ridge readout on those states; then cut the reservoir
loose and free-run it, from which `vpt` and `climate_error` are read. **A cell is
therefore already an aggregate** — `mean_curvature` is a mean over ~10,000 steps and `vpt`
a mean over 20 rollouts — and it contributes exactly **one point**, not a distribution, to
any figure.

> **A cell is not an independent observation, and the figures must not be read as though
> 38,280 of them were.** The three draws of a seed share its mask, its `Win` and its input
> series; only the flip pattern differs. At `f` = 0 the sign transform is the identity, so
> the draws are **literally identical** — checked here, and **100%** of (variant, σ, seed)
> groups return the same `mean_curvature` and the same `vpt` across all three draws. At
> `f` = 0.25, curvature differs across draws in 96.6% of groups but `vpt` is still
> identical in **45.1%**, mostly because both sit on the VPT = 0 floor. **The independent
> unit is the seed**, so the effective n is nearer 12,760 than 38,280, and nearer a third
> of that again at low `f`. This is `TIER0` §2.3's "quote seeds, not replicates" rule, and
> it is why F13's collapse panel counts **seeds** (5/10, 0/10) and why the Fisher test is
> on 10 units per substrate rather than 30.

**Where this bites and where it does not.** It does not threaten F12: panels (a) and (b)
describe the *shape* of a distribution — a two-spike histogram and an R² comparison — and
triplicating each seed inflates the count without moving the bimodality or shifting either
R² materially, because the duplication is symmetric across the two clusters. It would bite
any figure quoting a **standard error, a confidence interval or a p-value** over pooled
cells, which is exactly why every such statement in this act comes from
`e03_frontier_paired_scale_448.csv`, where the pairing is within seed, or from a seed
count. **F12's panel labels quote the raw cell count**, which is the honest description of
what is drawn; the caption states the unit so the count cannot be mistaken for a sample
size.

### 2.1 The gate

Run before any figure work. **Result: PASSES.** Every quantity recomputed from the frozen
artifacts; two small discrepancies logged rather than smoothed away.

| quantity | TIER0 value | recomputed | agrees to | verdict |
|---|---|---|---|---|
| cells in the between-mode band [0.6, 2.2] rad | 215 (0.56%) | **216 (0.5643%)** | 1 cell | **near-miss, logged** (§5 item 1) |
| two spikes | 98% | **99.44%** | — | pass; 98% understates |
| binary-bit R² | 0.364 | **0.36361** | 4e-4 | pass |
| continuous-curvature R² | 0.371 | **0.37049** | 5e-4 | pass (rounds to 0.370, §5 item 1) |
| within-smooth residual correlation | +0.145, n = 15,866 | **+0.1449, n = 15,866** | exact n, 1e-4 | pass |
| within-collapsed, excluding the floor | −0.151, 67% at floor | **−0.1506, 67.1%** | 5e-4 | pass |
| `f` = 0 collapse, ER / connectome | 5/10, 0/10 | **5/10, 0/10** | exact | pass |
| Fisher exact *p* | 0.033 | **0.03251** | 5e-4 | pass |
| VPT paired margins at σ = 2 | +0.28 / −0.01 / +0.44 (`f` = 0); +1.71 / +1.62 / +2.20 (`f` = 0.25) | **identical to 2 dp at all 11 `f`** | 0.005 | pass |
| `σ_eff` transition band | 0.77–0.90 | **[0.774, 0.904]** | exact | pass |
| brackets containing 1 | 1 of 38 | **1 of 38** | exact | pass |
| `σ_eff` CV / nominal σ / `σ·bulk95` | 0.209 / 0.667 / 0.746 | **0.209207 / 0.666667 / 0.745724** | 1e-5 | pass |
| per-variant `σ_eff` brackets | 0.71–0.82 / 0.79–0.91 / 0.82–0.91 / 0.87–0.95 | **exact to 3 dp** | 1e-3 | pass |
| the six matched-axis crossings | 2.943, 3.525, 3.598, 3.670, 3.743, 4.361 | **identical, grid-snapped** | exact | pass |
| the published crossing | (2.938, 0.153) | **(2.938, 0.1527)** by root-solve | 5e-4 | pass, improved (§5 item 4) |
| nominal crossing on `f_star` | none | **none** | — | pass |
| `f` = 0 curvature / VPT, connectome | flat 0.26; VPT falls ~10× | **0.258 → 0.261 over σ 2→11.2; VPT 4.43 → 0.44 = 10.0×** | 1e-3 | pass |
| MC at σ = 6, `f` = 0 | 11.43 / 5.02 / 4.11 / 2.42 | **identical** | 1e-3 | pass |

**Functions audited:** VPT definition and horizon, `mean_curvature`, closed-loop rollout,
`σ_eff`.

**Findings:**

1. **The straight/collapsed separator is curvature = 1.0, and the residual correlations
   are Spearman. Neither was recorded anywhere.** `CURV_COLLAPSE = 1.0`
   (`extend_f.py:51`) sits in the empty band and is the repo's canonical separator, but
   `TIER0` §3.10 quotes the between-band as [0.6, 2.2], so the natural reading is that
   the clusters are the band's complement. They are not. Splitting at the band edges
   gives n = 15,761 and +0.155; splitting at 1.0 gives **n = 15,866 and +0.1449**, which
   is `TIER0`'s published pair exactly. And the correlation is a **rank** correlation:
   Pearson within the smooth cluster is **+0.006**, essentially zero. The published
   +0.145 must be labelled as Spearman — as a Pearson it would be a much weaker claim
   that happens to have the same sign. F12 asserts the R² pair so the figure fails rather
   than the reader.

2. **"CV" is `IQR / median`, not `sd / mean`** (`threshold.py:147`). Under `sd/mean` the
   three criteria read **0.256 / 0.540 / 0.589**: `σ_eff` still wins, by ~2.3× instead of
   ~3×, and the *ordering of the two alternatives reverses* (nominal σ becomes the worst,
   not `σ·bulk95`). The claim survives either definition, but 0.209 cannot be quoted
   without naming the statistic. F14's y axis now says "robust CV (IQR / median)".

3. **The VPT horizon is not binding; the floor is.** Ceiling = `free_run_len` × `h` ×
   `λ_max` = 600 × 0.03 × 0.9056 = **16.301** Lyapunov times. **Zero of 38,280 cells reach
   it**; the observed maximum is 7.952, 48.8% of ceiling. So the horizon cannot be
   compressing differences at the top and lengthening it would buy nothing. What *is*
   live is the floor: **41.3% of cells read exactly 0**, rising from 7.2% at `f` = 0 to
   ~65% at `f` ≥ 0.30. Since VPT is the mean over 20 windows, a 0 means all 20 windows
   failed at the first predicted step — a strong statement, not a marginal one. The
   threshold convention is `‖pred − true‖₂ / rms_norm > ε` with `rms_norm` = 1.7321 (= √3,
   the z-scored 3-D series) and ε = 0.4, i.e. 0.693 in z-scored units.

4. **Curvature and `σ_eff` are teacher-forced quantities; VPT and `climate_error` are
   free-run quantities.** `mean_curvature` is the mean turning angle between successive
   velocity vectors of the **driven** state trajectory in ℝ⁴⁴⁸ (π = antiparallel steps),
   and `σ_eff = bulk95 · σ · ⟨1−x²⟩` averages the gain over units and time on the same
   driven states. So F12 relates a driven-manifold diagnostic to a closed-loop outcome.
   That is not a defect — the switch is a property of the operator and is visible under
   drive — but the chapter must say it, because a reader will otherwise assume curvature
   is measured on the thing being predicted.

5. **`climate_error` is not reproducible per cell, even on one machine.** Rebuilding one
   frozen cell on the real code path returned VPT, `mean_curvature`, `σ_eff`, `bulk95`
   and `mean_state` **bit-exactly**, and `climate_error` did not:

   | | σ = 2 | σ = 6 |
   |---|---|---|
   | frozen (ada) | 0.0570 | 8.262 |
   | here, 1 BLAS thread | 0.0721 | 8.270 |
   | here, 4 BLAS threads | 0.0289 | 15.586 |

   Deterministic within a thread count, 2.5× apart across them. The cause is not in
   doubt: the climate rollout is `climate_len` = 3000 steps = **81.5 Lyapunov times**, so
   a machine-epsilon difference in the BLAS reduction order is amplified by ~e⁸¹ and the
   trajectory decorrelates completely. VPT survives because its windows terminate at ~2.6
   Lyapunov times. The knowledge base already called `climate_error` "unreliable" on
   ER-divergence grounds; this is a second and sharper reason, and it governs E2's design
   (§6.1). The faithful/collapsed separation is 20–40× on seed medians against ~2.5×
   per-cell scatter, so the claim is safe — stated on medians, never on a cell.

6. **`TIER0` §6.4's flip-pattern non-portability is real, was measured here, and it bit.**
   At connectome / `f` = 0.25 / seed 4 the laptop gives `bulk95` = 0.3804 against the
   frozen capture's 0.3974, and the σ = 2.8 cell is already collapsed here (2.78 rad)
   where the frozen one is smooth (0.26 rad). The `f` = 0 probe in finding 5 reproduced
   bit-exactly for the opposite reason: at `f` = 0 the sign transform is the identity, so
   there is no flip pattern to differ. **Consequence for E1**: its cell is selected by a
   scan on the capturing machine, not read off the frozen panel (§6.2).

---

## 3. Figures

One block per figure ID from `FIGURE_LIST.md`. **Caption written before the figure.**

### F12 — curvature is bimodal: generation is gated, not graded

- **Claim carried:** A3P.1, A3P.2
- **Source:** `e01_jacobian_scale_448.parquet`, no row filter — all **38,280 cells**
  (§2.0 defines the unit: 4 variants × 11 `f` × 29 σ × 10 seeds × 3 draws, one Lorenz
  evaluation each). Two columns only, and they come from **different regimes**:
  `mean_curvature` from the teacher-forced driven states, `vpt` from the autonomous
  free-run.
- **Panels:** (a) curvature histogram, 160 bins over [0, π], log counts, with the
  between-mode band shaded and the separator dashed; (b) VPT against curvature as a
  log-density hexbin, same band shaded; (c) the smooth cluster alone, binned into
  curvature deciles, median and IQR
- **Why it leads:** without it the entire switch framing reads as asserted.
- **Panel (c) is deciles, not a scatter, and that is a decision not a default.** 99% of
  the smooth cluster sits in a ~0.017 rad column, so a hexbin of it is one dark stripe
  and the *sign* of the trend — which is the whole claim — is invisible. Deciles put the
  rank statistic on the page as something a reader can see running upward. Note that ρ is
  computed on all 15,866 raw cells, **not** on the ten decile points; the deciles are the
  display, not the statistic.

> **One-line titles, no other in-panel text (author's decision, 20 August 2026, revised
> the same day).** The five floating annotations — the two mode names, the gap count, the
> VPT floor fraction and the "straighter is not better" verdict — were removed and have
> **not** come back; they are in the caption. The **titles have**, one per panel, each
> stating that panel's own finding: *bimodal: 0.56% between the modes* / *binary bit R²
> 0.364, curvature 0.370* / *smooth cluster: Spearman ρ = +0.145*. The reasoning for the
> reversal is that a panel which states its result stays readable away from its caption,
> which is how a figure is actually met — skimmed first, read second. Panel (a) gained a
> title it never had, so the three read as a set.
>
> **Every number in a title is computed, never typed**, and each is additionally guarded
> by an assertion: the gap fraction, both R² against `TIER0`'s published pair, the VPT
> floor fraction, and the sign of ρ. A title cannot drift from the data, and neither can
> the caption, without the build failing.

> **Colour encodes the binary bit** (added 20 August 2026; see §5 item 13 for the palette
> decision). Panels (a) and (b) are drawn as **two** series split at the collapse
> separator, in the two `style.REGIME_COLOUR` inks, and panel (c) — which *is* the smooth
> cluster — takes the smooth ink. So the colour a cell carries is exactly the
> collapsed-or-not bit whose R² panel (b) reports: the figure shows the reader what the
> bit is rather than asking them to take it on trust. The band and the separator dropped
> to neutral grey in the same change, because furniture in an accent colour would have
> competed with the two colours that now mean something.

- **Caption (final wording):** *Predictive capacity is gated by a regime, not graded by
  curvature.* Each point is one **cell**: one Lorenz evaluation of one substrate at one
  sign fraction, spectral radius, seed and flip realisation (38,280 in all; the
  independent unit is the seed, of which there are ten per condition). Curvature is
  measured on the teacher-forced state trajectory in ℝ⁴⁴⁸ — the mean turning angle
  between successive velocity vectors, so π means successive steps are antiparallel — and
  valid-prediction time on the autonomous free-run, so the figure relates a property of
  the driven manifold to a closed-loop capacity.
  **(a)** Mean curvature is a two-spike distribution: a smooth mode at ~0.25 rad and a
  period-2 mode at ~π. The shaded band marks the interval [0.6, 2.2] rad between them,
  which holds **216 cells, 0.56% of the panel**; the dashed line at 1 rad is the
  collapsed-or-not separator, which sits inside that empty band and is therefore not a
  tuned threshold. **Colour throughout the figure is that separator** — indigo for cells
  the bit calls smooth, crimson for cells it calls collapsed. Curvature is not a quantity
  this substrate takes intermediate values of.
  **(b)** Against valid-prediction time, a single binary "has it collapsed" bit explains
  **R² = 0.364** of the variance; the continuous quantity manages **0.370**. The entire
  0.25 → 3.14 rad range is worth **0.7 percentage points** beyond the bit. **41% of cells
  sit at the VPT floor of exactly zero**, all of them in the collapsed mode.
  **(c)** Within the smooth cluster alone (curvature < 1 rad, **n = 15,866**), binned into
  curvature deciles with median and interquartile range, the residual relation runs the
  *wrong way* for a graded account: **Spearman ρ = +0.145**. Straighter is not better.
  The line rises over eight deciles and falls in the last, which is the widest bin and the
  one reaching up to the separator.
  **Scope: this holds for `f` > 0.** At `f` = 0 — the biologically real cut — curvature is
  flat at 0.26 rad across the entire σ sweep while prediction falls roughly tenfold, so
  geometry gates nothing there (`TIER0` §3.11, and §5 item 6 of this act).

### F13 — generation read as VPT, including at the biologically real cut

- **Claim carried:** A3P.3, A3P.4
- **Source:** (a) `e03_frontier_scale_448.parquet`, `metric == "vpt"`,
  `spectral_radius == 2.0`; (b) `e03_frontier_paired_scale_448.csv`, same filter;
  (c) `item2_collapse_loci_scale_448.csv`, `f == 0`
- **Panels:** (a) absolute seed-median VPT against `f`; (b) the paired advantage with
  95% CIs and the `f` ≥ 0.25 band shaded; (c) seeds collapsed to period-2 at `f` = 0
- **Panel (c) is the one a draft would drop, and it is what moves the arm into the
  biologically real regime**, since macro dMRI weights are non-negative by construction.
  The unit is the **seed**, never the replicate: the three draws of a seed share its mask,
  `Win` and input series, and at `f` = 0 the sign transform is the identity, so the draws
  are literal duplicates.
- **The shading starts at 0.25, not 0.20, and that is a precision fix** (§5 item 2).
- **Caption (final wording):** *The generative advantage is real when read as prediction
  rather than as geometry, and it exists at `f` = 0.* (a) Seed-median valid-prediction
  time at σ = 2, near every substrate's own peak. (b) The same comparison paired within
  seed, with 95% confidence intervals; from **`f` = 0.25** the connectome leads all three
  nulls by **+1.0 to +2.2 Lyapunov times** and is the only substrate still predicting
  (1.3–2.8 against the nulls' 0.1–0.9). At `f` = 0.20 the margin clears two of the three
  (+1.46 and +1.82) but not degree-matching (+0.28). Clearing the weight-permuted control
  makes this a **weight-placement** effect rather than a topological one. (c) At `f` = 0
  the advantage is not absent but far supercritical: over σ ≤ 11.2, Erdős–Rényi collapses
  to a period-2 orbit in **5 of 10 seeds** (σ ≈ 7.6–8.0) and the connectome in **0 of 10**
  (Fisher exact *p* = 0.033). The earlier reading that the advantage *emerges* with `f`
  was an artifact of stopping the sweep at σ = 6: the onset is in σ. Weight-permuted and
  degree-matching sit between, at 3 of 10 and 1 of 10.

### F14 — `σ_eff` is a locator, not a criterion

- **Claim carried:** A3P.5
- **Source:** `e01_threshold_invariance_scale_448.csv` filter `scope == "f > 0"` (n = 37);
  `e01_threshold_table_scale_448.csv` (44 rows)
- **Panels:** (a) the robust CV of the three candidates; (b) `σ_eff` at the transition
  against `f` per substrate, in-scope cells joined and out-of-scope drawn as open
  markers; (c) each substrate's median bracket, ordered
- **Panel (b) now carries panel (a)'s scope, and the builder asserts the counts match.**
  The session-0 draft plotted every row of the threshold table — including `f` = 0 and
  the under-half-transitioning cells — beside a CV computed on 37 of them. That put the
  regime where the locator explicitly *does not apply* into the panel arguing that it
  works, and dragged the curves well below the band.
- **Panel (c) exists because the per-`f` curves cross.** The ordering by spectral gap is
  a statement about each substrate's **median** bracket; the connectome is lowest on the
  median and is not lowest at every `f`. A title on (b) asserting the ordering would be
  read as the stronger claim.
- **No line is drawn at 1, and the builder asserts it.**
- **Caption (final wording):** *`σ_eff` locates the generative transition about three
  times better than either alternative, and does not cross one.* (a) Robust coefficient
  of variation (IQR / median) of each candidate's own value at the transition, over the
  37 (variant, `f`) cells where at least half the seeds transition: `σ_eff` **0.209**
  against nominal σ's 0.667 and the linear gain `σ·bulk95`'s 0.746. A predictor should
  take the same value wherever the transition happens. (b) Where each substrate
  transitions. Open markers are cells outside that scope, drawn but not joined: at
  `f` = 0 the locator does not apply at all — Erdős–Rényi transitions at `σ_eff` = 0.014,
  two orders of magnitude below its own peak of 0.607 and on the *descending* branch, and
  the connectome never transitions inside σ ≤ 11.2. (c) The variant-dependent offset that
  was **pre-registered before fitting** is present and ordered by spectral gap: the
  connectome, with much the largest gap, transitions lowest. **The pre-registered value
  of 1 is falsified**: 1 of 38 brackets contains it, the transition sits in the shaded
  0.77–0.90 band, and `σ_eff` folds — its maximum over the sweep is below 1 for every
  substrate at `f` ≤ 0.20 while transitions happen throughout. `σ_eff` survives as an
  empirical locator, not a stability law, and it is Lorenz-only.

### F16 — the crossing, with its axis and its coverage

- **Claim carried:** A3P.6 (contribution 2, the unifying claim). Cross-act figure: it
  needs both Act III arms, so session 4 renders it with session 3's memory arm validated.
- **Source:** `e02_heatmap_boundaries_extension.csv` +
  `..._extension_nominal.csv` concatenated with an `axis` column; `panel == "dD"` is the
  memory boundary and `"dStraight"` the generative one; **`f_star`** is the convention.
  Coverage mask from `e02_heatmap_coverage_extension.csv`.
- **Panels:** (a) both boundaries on `σ·bulk95` with the per-`f` coverage mask hatched;
  (b) both on nominal σ
- **Four flags, all handled:** the coverage mask is drawn **per `f`**, not at the global
  minimum, because `x_hi` runs 3.58 to 4.36 and a single vertical line misstates it;
  `f_star` is the convention plotted and the other two columns were run as the robustness
  check (§5 item 5); the published nominal crossing is marked as a **quoted** number with
  a leader, since it comes from re-running the boundary operator on the σ ≤ 6 sub-panel;
  and the boundary is **broken** at gaps, never bridged.
- **Caption (final wording):** *The memory and generative advantages occupy opposite
  regions of the (`f`, σ) plane, and the boundaries cross once inside full replicate
  coverage.* (a) On `σ·bulk95`, which holds the bulk radius fixed, the memory boundary
  rises and the generative boundary falls, and they cross at **(2.938, 0.153)** — the
  first crossing and the only clean one. The hatched region lies beyond each `f`'s own
  all-replicates coverage edge, where the panel is populated only by the replicates whose
  own `bulk95` reached that far; the boundary there rests on a selected subsample and
  oscillates, producing five further crossings between x = 3.5 and 4.3 whose number and
  position must not be read. (b) On nominal σ, which holds the spectral radius fixed, the
  two boundaries **never meet** once the sweep passes σ = 6: the generative panel's true
  maximum sits at `f` ≈ 0–0.05, σ ≈ 7–11, which σ = 6 never saw, and including it drops
  the generative boundary below the memory boundary throughout. The published nominal
  crossing (4.392, 0.1309) is marked as a quoted value; it comes from re-running the
  boundary operator on the σ ≤ 6 sub-panel, not from these curves. **Neither axis is
  neutral** — nominal matching pins the Perron root and matched-bulk matching pins the
  bulk, and the mechanism under test is the Perron mode — so the crossing is only ever
  quoted with its axis.

### F17 — the free-running attractor, and how it fails  (E2)

- **Claim carried:** A3P.7, A3P.8
- **Source:** `e2_free_run_scale_448.parquet` (440 rows, new capture) for (a), (b), (c),
  (e); **the frozen `e01_jacobian_scale_448.parquet` for (d)**, which carries 30 cells per
  (variant, `f`) against the fresh capture's 10
- **Panels:** (a) generated attractors at `f` = 0; (b) the same at `f` = 0.25; (c) the
  distribution of free-run spread over true spread; (d) the fraction of cells keeping a
  faithful climate against `f`, frozen; (e) the fixed-point rate per substrate, fresh
- **The seed drawn in (a) and (b) is the one nearest its own cell's median**, the rule
  F1 and F6 already use — the only rule that cannot be accused of picking a flattering
  realisation.
- **The fixed points are mostly off the panel, and drawing them naively was a bug that
  looked like a finished figure.** A collapsed free-run does not settle somewhere inside
  the attractor; it leaves and stops far outside it. Measured over all 229 collapsed
  cells: **87% rest more than 3 z-scored units from the origin, median 11.5, furthest
  38.5**, against a true attractor spanning about ±2.5 per coordinate. Drawn as a plain
  ring at its true position, a fixed point at *z* = +14 is simply absent — so the first
  version of this panel named three collapsed substrates and showed the reader one
  marker. Out-of-range points are now clamped to the panel edge and drawn as an outward
  arrowhead. The window is **not** widened to contain them: the furthest would squash the
  attractor to a smudge.
- **A single shared substrate key** sits above the figure. Placing it inside (a) was
  tried and abandoned on measurement — a search over every legend-sized window of that
  panel found none free, the emptiest (the notch between the butterfly's wings) still
  carrying ~100 trajectory points, and every corner worse. One key serves all five
  panels, so (d)'s duplicate legend went with it and both panels got their space back.
  The (a) and (b) titles dropped to one line in the same pass, which cleared the
  collision the wider two-line titles had with the neighbouring panel labels.
- **`f` = 0.25 rather than 0.30 in (b)**: at 0.30 every substrate's median seed has
  collapsed, so the panel is four invisible dots — a true picture and a useless one.
- **Caption (final wording):** *What a given climate error looks like, in the regime the
  prediction arm is actually about.* Every persisted state matrix in this work is
  teacher-forced, so this is the first look at the trajectory the reservoir produces when
  it drives itself. (a) At `f` = 0 and σ = 2 every substrate reproduces the Lorenz
  attractor. (b) At `f` = 0.25 only the connectome still does; all three nulls have
  collapsed onto a fixed point (open markers; an arrowhead means that point lies outside
  the plotted window). (c) That failure mode is **bimodal, as curvature is**: of 440
  free-runs, 229 retain under 5% of the true attractor's spread and 158 retain 90–110%,
  with 11 anywhere between. The point they stop at is typically **outside the attractor
  altogether** — 87% of the 229 sit more than 3 z-scored units from the origin, median
  11.5, against a true span of about ±2.5 — which is why those cells' climate errors run
  to 8 and beyond rather than to some modest value. (d) On the frozen capture, the fraction of
  cells holding a faithful climate: at `f` ≥ 0.30 the connectome keeps **0.43** against
  the nulls' **0.14**. (e) Read as the fixed-point rate over `f` ≥ 0.20, the same
  ordering. **Registered before the capture existed: the first clause holds and the
  second is refuted.** The collapse is a loss of *scale*, not a distortion of shape —
  which is the fixed-point branch of the one-dimensional map argument (a gain above +1
  gives a stable fixed point; below −1, a period-2 orbit; nothing stable between),
  observed in the closed loop for the first time. Per-cell climate values are chaotic
  over the 81.5 Lyapunov times of the rollout and are never read individually.

### S2 — the two curvature regimes made visible  (E1; supplementary, prints in chapter 5)

- **Claim carried:** none of its own. It illustrates A3P.1, which is F12's.
- **Source:** `e1_curvature_regimes_scale_448.parquet`; connectome, `f` = 0.25, one seed,
  two σ **one grid step apart**
- **Panels:** (a) unit traces in the smooth regime; (b) the same units in the collapsed
  regime; (c) the per-step turning-angle distributions
- **Panel (c) is what earns the figure.** F12 plots one *mean* curvature per cell and
  shows the means are bimodal **across** cells. It cannot show that **within** a single
  cell the per-step angles are concentrated rather than spread — i.e. that the mean
  describes a regime rather than averaging over one. That is "gated, not graded" seen
  from inside one cell, and it is the intuition Act II hands over as a boundary
  (`act2_manifold.md` §5 item 15).
- **Deliberately no PCA.** A top-3 projection is faithful to 96–99% of the fluctuation
  variance but nearly substrate-invariant (PCs-to-95% is 3 on Lorenz for every rung while
  `d_eff` spans 75 to 413), so captioning one as the subspace the readout computes in
  would contradict F6, which is Act II's own contribution. Raw traces and turning angles
  carry no such implication.
- **Caption (final wording):** *What the two curvature regimes look like in time.* One
  substrate (connectome, `f` = 0.25, one seed) at two spectral radii **one grid step
  apart**, so the regime is the only thing that differs. Colour is the regime throughout,
  and is the same pair F12 uses: indigo for smooth, crimson for collapsed. Within a
  panel, lightness separates the six units and means nothing else. (a) Below the transition the
  most active units trace smooth, slowly turning trajectories; mean curvature 0.26 rad,
  VPT 0.37, climate error 0.06. (b) One grid step above, the same units alternate sign
  every step — successive velocity vectors antiparallel; mean curvature 2.82 rad, VPT
  0.02, climate error 5.00. (c) The per-step turning angles behind those two means are
  tightly concentrated in each case, near 0.26 rad and near π, with nothing between. The
  mean curvature F12 plots is therefore a label for a regime, not an average over a
  spread. Not drawn at `f` = 0, where curvature is flat at 0.26 rad across the entire σ
  sweep and there is nothing to see.

---

## 4. Section outline

Structure only, at the level of section headings and the argument each carries. Prose is
written by hand, not generated (see the roadmap §4b note on drafting).

1. **What the closed loop asks that the driven tasks do not.** One paragraph plus methods.
   In generation the reservoir's own prediction is fed back, so errors compound and a
   mildly unstable substrate diverges; that fragility is what VPT and `climate_error`
   measure. State the two metrics, the horizon (600 steps = 16.3 Lyapunov times, never
   reached) and the floor (41% of cells at exactly 0), and state up front that curvature
   and `σ_eff` are measured on the **teacher-forced** states while VPT and climate come
   from the **free run**.

2. **Generation is a switch.** *Carries A3P.1, A3P.2.* Figure F12, with S2 as the
   chapter-5 run-up a reader will already have met. The chapter's opening result and the
   one that licenses everything after it: curvature is not a graded quantity on this
   substrate, so the question is never "how curved" but "which side". Close with the
   wrong-signed within-cluster residual, because that is what forbids the graded reading
   rather than merely failing to support it.

3. **Read it as prediction and the advantage is there.** *Carries A3P.3.* Figure F13a, b.
   The order parameter was wrong, not the phenomenon: against the 0.032 rad curvature
   residual the matched-axis panel was contouring, VPT gives +1.0 to +2.2 Lyapunov times.
   Name the σ every time. Clearing the weight-permuted control is what makes it placement
   rather than topology.

4. **And it is there at the biologically real cut.** *Carries A3P.4.* Figure F13c. Short
   and load-bearing: macro dMRI weights are non-negative, so `f` = 0 is the substrate that
   exists. The advantage is a collapse-resistance asymmetry far supercritically, not a
   near-critical capacity gain — attach σ ≈ 7.6–8.0, and say in the same breath that near
   criticality at `f` = 0 there is no advantage at all.

5. **What locates the transition, and what does not.** *Carries A3P.5.* Figure F14. Give
   the pre-registration first, in the form it had before fitting, then the outcome: the
   offset was predicted and found, the value was predicted and falsified. The section
   exists as much to retire a criterion as to establish a locator.

6. **The free-running attractor.** *Carries A3P.7, A3P.8.* Figure F17. New evidence, so
   it gets its own section rather than a footnote to §3. Pre-registration, then both
   clauses, then the refuted one at length: the failure is a collapse to a fixed point,
   which is the branch §3.9's map argument names, observed in the closed loop. This is
   also where the reproducibility limit on `climate_error` is stated plainly.

7. **One axis, read with opposite sign.** *Carries A3P.6.* Figure F16. The unifying
   section, and the only place contribution 2 is argued. Memory's advantage is
   supercritical and maximal at `f` = 0; generation's is near-critical and emerges from
   `f` ≈ 0.20–0.25. They had to occupy opposite regions because they are the same
   quantity read from both ends. Quote the crossing with its axis, draw the coverage, and
   say that contribution 2 has **no out-of-sample test** in this thesis.

8. **The bridge: MC → NARMA-10 → Lorenz.** *Carries no new claim.* One paragraph (§5
   item 7), placed here because it is what makes the dissociation look like an axis rather
   than two tasks.

9. **What sets generation at `f` = 0 — a named open problem.** *Carries A3P.9.* Closing
   section of the half. Three candidate explanations, all ruled out on the data, and no
   fourth offered.

---

## 5. Audit log and open issues

1. **The between-band count is 216, not 215, and the continuous R² rounds to 0.370, not
   0.371.** Both stable and both tiny. The band count is 216 under all four open/closed
   conventions (0.5643% of the panel, against `TIER0`'s 0.56%), so the one-cell gap is not
   a boundary convention; it is one cell out of 38,280, or 0.0026%. The continuous R² is
   0.37049, which rounds down. Neither moves any claim, and F12 prints what it computes
   rather than the published rounding. **Logged, not reconciled**: a rank-4 document does
   not instruct `TIER0`, and regenerating an artifact to close a one-cell gap is exactly
   what `CONVENTIONS` working rule 1 forbids.

2. **The "+1.0 to +2.2 from `f` ≈ 0.20" margin holds against all three nulls only from
   `f` = 0.25.** At `f` = 0.20 the paired margins are +1.46 (weight-permuted), +1.82 (ER)
   and **+0.28** (degree-matching) — two of three, not three of three. `TIER0` §2.6 is
   careful ("from `f` ≈ 0.20–0.25"); roadmap §1 contribution 4 compresses it to "from
   f ~ 0.20" with "over all three nulls" attached, and those two cannot both be true.
   F13's shading starts at 0.25 and its caption states the `f` = 0.20 exception.

3. **`TIER0` §2.3's "only the first lies inside it" does not hold on its own arithmetic.**
   The six recomputed crossings are 2.943, 3.525, 3.598, 3.670, 3.743, 4.361 (reproduced
   here exactly) and the stated all-replicates edge is `x_hi` = 3.58 at its minimum over
   `f`. **3.525 < 3.58**, so two lie inside that edge, not one. Under the *per-`f`* edge —
   which is the honest test, since `x_hi` runs 3.58 to 4.36 — **five** of the six lie
   inside their own `f`'s coverage. Neither reading gives one.

   **What is defensible, and what F16 says instead.** The published crossing is the first
   by a clear margin (the next is 0.56 further out on x) and is inside coverage under
   *both* conventions. Crossings 2 to 5 span x = 0.22 and are not five independent
   features: they are one oscillation of the generative boundary crossing zero repeatedly,
   in the region where it rests on a `bulk95`-selected subsample. In that region the
   coverage test itself is not decisive, which is the point — it is why §6.10 says the
   region is drawn but must not be read. F16 therefore labels them "one oscillation of the
   generative boundary, not to be read" rather than "in the unreadable region", which
   would be false of two of them. **`TIER0` §2.3 should be amended by whoever owns it**;
   this act does not, and no claim in the thesis depends on the count.

4. **Solving for the crossing root removes the 0.005 gap `TIER0` attributes to
   interpolation.** Snapping to the right-hand bracketing grid point reproduces §2.3's six
   values exactly; solving the root between the bracketing points returns
   **(2.938, 0.1527)**, which is the published coordinate of record. So the 2.943/2.938
   discrepancy is the snap, and F16 computes and labels the published value directly
   rather than marking a nearby point and explaining the difference. `FIGURE_LIST`'s F16
   flag anticipated the opposite and can be relaxed.

5. **`FIGURE_LIST`'s F16 flag overstates the nominal-axis result, in the safe direction.**
   It says all three level conventions give no nominal crossing. Two do:
   `f_star` gives none and `f_star_level_raw_max` gives none, but
   **`f_star_level_on_subrange` gives a crossing at σ = 4.382**, against the published
   4.392 from the σ ≤ 6 sub-panel re-run. That is a 0.01 agreement, not a contradiction,
   and it *strengthens* §2.3's "what moved is the panel, not the method": pinning the
   level back to the old range recovers the old answer almost exactly. The headline claim
   — **no nominal crossing on the `f_star` convention** — is untouched, and it is what
   F16 asserts.

6. **The `f` = 0 open problem, with its bounding evidence assembled.** Stated as a named
   open question in the discussion, not worked around. Three candidate explanations, each
   ruled out on this act's own recomputation:

   | candidate | what it predicts at `f` = 0 | measured |
   |---|---|---|
   | geometry (the F12 switch) | prediction falls when the manifold changes regime | **connectome curvature is flat at 0.258–0.261 rad over the entire σ = 0 → 11.2 sweep while its VPT falls 4.43 → 0.44, a factor of 10.0.** Curvature is blind to the loss |
   | the `σ_eff` locator | the transition sits at `σ_eff` ≈ 0.77–0.90 | **ER transitions at `σ_eff` = 0.014**, two orders of magnitude below its own peak of 0.607 and on the *descending* branch (0.014 before the step, 0.011 after). The connectome never transitions at all inside σ ≤ 11.2 |
   | memory doing the work | the substrate with more memory predicts better | **at σ = 6 the connectome has ~4.7× ER's MC (11.425 vs 2.420) and slightly *lower* VPT (0.807 vs 1.175).** The ordering is inverted |

   The exact Jacobian confirms two phenomena rather than one. Recomputed here at the
   **draw** level (n = 1,069 for `f` > 0, n = 27 for `f` = 0), `λ_min(J)` at the
   transition is tight at −0.881 [−0.922, −0.793] over `f` > 0 but −0.165, scattered over
   [−0.367, −0.044], at `f` = 0. `TIER0` §3.11 quotes the same contrast at the **seed**
   level (−0.849 [−0.898, −0.769], n = 378), and the `f` = 0 interval is identical in
   both because the three draws of a seed are literal duplicates there. **Quote one unit
   or the other** — the same trap §3.11 flags for `σ_eff`'s two CVs. And `λ_min(J)` never
   reaches −1 in either
   regime, so generation breaks while the fixed point is still linearly stable. The likely
   missing piece is the closed loop itself: the operative map is
   `x → tanh((W + Win·W_out)x)`, carrying a rank-3 readout term nothing in the repository
   computes, and testing it needs a `W_out` the evaluator does not expose. **F17 is the
   nearest this thesis gets** — it measures the closed-loop trajectory directly and finds
   the fixed-point collapse — but it does not compute that Jacobian, and it does not close
   the question. Logged as open rather than as a fourth guess.

7. **The bridge paragraph: MC → NARMA-10 → Lorenz, written from the frozen parquets.**
   No run; none permitted. **Three tasks, not four** — Mackey-Glass on the human substrate
   has never been run and stays post-thesis by roadmap §6, which is a **schedule decision
   and not a gap in the argument**, and must be described that way. Each task carries its
   own ridge α (**MC 1e-6, NARMA-10 1e-8, Lorenz 1e-7**) and every number below is a
   task-native performance metric at that task's own α, so no cross-task `d_eff`
   comparison at mixed α is made. **No figure**: NARMA-10 has no slot in `FIGURE_LIST` and
   is not given one.

   > **The paragraph, in substance.** The memory and generative advantages are not two
   > phenomena but one axis read from opposite ends, and NARMA-10 — which sits between
   > pure recall and pure prediction — sits between them on the axis that matters, which
   > is σ. Taking the connectome-minus-Erdős–Rényi advantage as a function of σ on the
   > phase-diagram grid and asking where it is largest: at `f` = 0.25 the memory
   > advantage peaks at **σ = 6.0**, the top of the grid; NARMA-10's at **σ = 4.0**; and
   > the Lorenz VPT advantage at **σ = 2.0**, near criticality. Over the whole `f` axis
   > the median locations are **6.0, 5.2 and 2.0**. So the trade-off does vary
   > continuously across the three tasks, and it varies along the spectral-radius axis
   > that contribution 2 is about, rather than merely reflecting that NARMA-10 is harder
   > than recall.
   >
   > **The `f` axis tells a different and equally useful story, and it must be given.**
   > On `f`, NARMA-10 does *not* interpolate: its supercritical advantage is largest at
   > low `f` (+0.12 to +0.23 in NRMSE over `f` ≤ 0.15) and decays, exactly like MC's
   > (+8.95 at `f` = 0 falling to +0.50 at `f` = 0.50), while the Lorenz advantage is
   > ~0 at `f` = 0 and *emerges* from `f` = 0.20 (+0.05 → +1.54). NARMA-10 groups with
   > memory, and the reason is mechanical rather than a matter of degree: **NARMA-10 is
   > teacher-forced**, so the reservoir is re-anchored by the true input every step and
   > the regime switch has no closed-loop consequence for it. That is the same argument
   > `FIGURE_LIST`'s "Addition 2" used to move Mackey-Glass onto the memory side, now
   > confirmed on a task that was already collected. The discontinuity in this programme
   > is at the closed loop, not on the memory-to-prediction spectrum.
   >
   > **One robustness note.** NARMA-10's supercritical advantage at high `f` is partly
   > Erdős–Rényi *diverging* rather than the connectome improving: at `f` = 0.45, σ = 6
   > the ER NRMSE reaches 127.0, 22.8 and 17.4 on three of ten seeds against the
   > connectome's 0.51–1.02 throughout. The seed median absorbs it, but the effect is a
   > robustness statement, not a capacity one — the same shape as the Lorenz
   > collapse-resistance result, and worth saying rather than letting a large median
   > difference read as a large capacity difference.
   >
   > **What is not said.** No PR-versus-`d_eff` statement is transferred to NARMA-10.
   > Its captured states and its ridge design matrix are different row sets — 2,800
   > captured, 2,000 entering the design plus an unregularised bias column
   > (`act2_manifold.md` §2.6 finding 4) — which is exactly why F6 uses MC only. The
   > caveat cannot be dropped and the statement is therefore not made.

8. **Substrate naming brought into line with F1 to F11.** `act3_prediction.py` was the
   last builder on the rung-numbered `VARIANT_LABEL` / `VARIANT_TICK` scheme, so F12 to
   F14 and F16 would have named three substrates one way in chapter 6's prediction half
   and another way everywhere else. All builders now use `VARIANT_TITLE` and
   `VARIANT_TITLE_TICK`. Both layout consequences session 3 recorded (`act3a_memory.md`
   item 12) appeared here too and were handled the same way. **Rotation rather than
   shrinking**, where a categorical axis is narrower than the names: F17e's substrate
   ticks are rotated **30°** and F14a's criterion ticks **20°** — 20 because three
   criterion labels in a narrow panel need less than four substrate names in a narrower
   one, and the rule is "rotate enough to clear, never shrink below the contract".
   **Two-column legends** where four entries would not fit: F14b and F17d. F13's three
   panels needed neither — its (c) uses the wrapped two-line `VARIANT_TITLE_TICK`, which
   fits at two bars, and its legends are 4 and 3 entries in wide panels. F12 and F16 are
   unaffected entirely: F12 pools all cells and F16 draws boundaries, so neither names a
   substrate anywhere. `VARIANT_TICK` and `VARIANT_LABEL` are untouched in `style.py`:
   this is a per-figure choice, as it was for F1, F4b and session 3's four figures.

9. **One shared-module addition, and a full re-render proving it changed nothing.**
   `style.ANNOTATION_ACCENT` names a colour already in use as a literal in
   `act1_structure.py` and `act4_anchor.py`; it exists so the prediction arm's several
   in-panel claim marks cannot drift apart. Adding a name for an existing value cannot
   move a rendered figure, and a full 18-figure re-render confirmed it: only the figures
   this session owns changed. `sources.py` gained a `climate_error` column on the
   `jacobian` **placeholder** (F17 panel d reads it); the real loader was untouched and
   F12 and F14 read other columns.

10. **`--smoke` needed content assertions gated, structural ones kept.** Following
    `act2_manifold.md` item 14: the published-value assertions (F12's R² pair and residual
    sign, F14's ordering, F16's crossing coordinate and nominal non-crossing, F17's
    pre-stated claim) are skipped on placeholder data, which carries no claim. The
    **structural** ones stay live on both paths — F14's assertion that panels (a) and (b)
    hold the same population, F16's assertion that a crossing exists at all on the
    effective axis and that no line is drawn at `σ_eff` = 1, S2's straddle check.

13. **A fourth colour namespace, chosen by measurement — and the measurement overturned
    the first choice.** F12's colour now encodes the collapsed-or-not bit rather than
    decorating, which needed a regime pair distinct from the substrate palette, so
    `style.REGIME_COLOUR` joins `VARIANT_COLOUR`, `BASIS_COLOUR`, `BOUNDARY_COLOUR` and
    `AXIS_COLOUR` as its own small namespace, on the same principle: a regime is not a
    substrate, and one regime is one colour wherever it appears.

    **The first pick was wrong and only measurement caught it.** ColorBrewer RdBu's
    blue/red (#2166AC / #D6604D) was chosen on the reasoning that RdBu is a certified
    colourblind-safe scheme — which is true, and irrelevant to the question actually being
    asked. Run through `style._lab`, the module's existing Vienot/Brettel dichromacy
    simulation, that pair sits **dE 0.7** from a substrate colour: under one of the
    dichromacies it is indistinguishable from degree-matching's #0072B2. It would have put
    a substrate hue on a non-substrate quantity, thesis-wide, and it looked entirely
    defensible.

    A grid search over 384 candidate inks, scored on worst-case CIE76 dE across normal
    vision and all three dichromacies, returns **indigo #17158c / crimson #a5103d**:
    dE **22.9** from every substrate colour (the comparable existing floor,
    `BASIS_VARIANT_FLOOR`, is 8.0), dE **10.4** from every furniture colour, dE **56.5**
    between the two regimes. `check_regime_palette()` re-derives all of it and is run by
    the smoke entry point, so the choice cannot silently drift — the same guard
    `check_basis_palette()` provides for Act II.

    **One property is knowingly not met, and it is asserted nowhere for that reason.**
    Greyscale separation is weak: relative luminance 0.026 against 0.087. The variant and
    basis palettes need luminance separation because their series overlap inside a panel
    and colour is the only thing separating them. Regimes never overlap — in F12 they sit
    at opposite ends of the curvature axis with a near-empty band between, and in S2 they
    are in different panels — so position disambiguates and hue is reinforcing rather than
    load-bearing. If a figure ever needs the two regimes interleaved along one axis, this
    pair is wrong for it, and that is a scope question rather than a palette one.

    **S2 follows, and the loose end is closed.** It contrasts the same two regimes and
    drew them in neutral grey and the generic accent; it now uses `REGIME_COLOUR` too.
    One regime, one colour, across both figures — a reader who has learned
    indigo-is-smooth and crimson-is-collapsed in F12 reads S2 without relearning
    anything. Within an S2 trace panel, **lightness separates the six units and carries
    no other meaning**, sampled over the saturated half of `regime_cmap` because the pale
    end exists for F12b's density maps and is too faint for a line. **The panel titles stay
    black** — colouring them was tried and dropped, since a title that already names its
    regime in words gains nothing from being tinted the same colour, and coloured body
    text reads as emphasis rather than as a key. Two small tidies came with it:
    the legend was quoting the same n twice, so it moved to the y axis, and an assertion
    now guards that the two regimes really are read over the same window.

11. **What this act ran, and what it deliberately did not.** Two captures, both on the
    laptop, both costed from a measured cell of the real code path (**1.27 s/cell**, not a
    component estimate — `TIER0` §2.5's lesson): E2 at 440 cells and E1's scan plus two
    cells, ~9 core-minutes in total. Nothing queued on ada and the 20 August freeze was
    never in play at this scale. Mackey-Glass was not inspected. No frozen artifact was
    regenerated, overwritten or spliced onto.

12. **For whoever writes chapter 6.** The prediction arm is validated: F12's bimodality,
    F13's margins and collapse rates, F14's invariance table and F16's crossing all
    reproduce and all assert against `TIER0` in their builders. Three things to carry
    forward. **(i)** The generative-boundary key is still `dStraight` — the withdrawn word
    — in `report/figlib/style.py` and `phase_diagram/analysis.py`. Act II item 4 flagged
    it for sessions 3 and 4; it is a data-column name rather than any rendered string
    (F16 prints "generative boundary" via `BOUNDARY_LABEL`), so renaming it means
    rewriting frozen parquets and it is **deliberately not done here**. It is a naming
    debt, not a correctness one. **(ii)** `climate_error` should never be quoted per cell,
    at any point in the thesis (§2.6 finding 5). **(iii)** Contribution 2 still has no
    out-of-sample test; F16 plus the joint reading of F7 and F13 is what it rests on, and
    closed-loop Mackey-Glass is deferred work rather than a gap MG's presence in the task
    list quietly fills.

---

## 6. Inherited specifications — two manifold-trajectory experiments

**Handed down from session 2 (17 Aug), roadmap §4d. Both built.**

> **AMENDMENT, 19 August 2026, on the author's decision — recorded here because the
> governance change is itself the thing to write down.** The rule this section carried was
> **"one slot, first past the post"**: E1 and E2 competed for a single cap slot, E2
> resolved first, and E1 was to be dropped with the reason recorded. That rule is
> **replaced by "build both, then place each on what it turns out to show"**. Placement is
> decided after the figures exist, not before, and the cap of 15 is no longer a gate on
> whether the work happens.
>
> **What changed in the repository, in the same commit that landed the figures**
> (`CONVENTIONS` working rule 3 still binds — no figure exists outside `FIGURE_LIST.md`):
>
> * `report/FIGURE_LIST.md` now says **count 16, not cap 15**, and the old "a session that
>   wants a sixteenth reports and stops" paragraph is struck through rather than deleted,
>   because the reasoning in its first half is still live.
> * `report/figlib/figures/__init__.py` asserts `len(FIGURES) == 16`. **The assertion is
>   kept, and its purpose is restated**: it records the count rather than enforcing a
>   ceiling. It survives because it is still the one place a session must edit — and
>   therefore justify — to add a figure, which is the drift `FIGURE_LIST`'s cap existed to
>   prevent.
> * **The S-figure bar lost a clause.** It required an S-figure to make no claim the main
>   text does not already make **and** to be built by an existing builder at different
>   parameters. The second clause is dropped: it was a *proxy* for the first, and it
>   excluded exactly the case a supplementary figure is most useful for — supplying
>   intuition for a claim the main text asserts but cannot illustrate. S1, a scale
>   replicate, satisfied both clauses and made the proxy look free; S2 is the case that
>   shows it was not.
>
> **The cap becoming a soft count is the substantive change**, and it is worth stating
> why it is safe: what stopped figure-count drift was never the number, it was the
> requirement to edit two files and write down a reason. That requirement is intact.

### 6.1 E2 — closed-loop faithful geometry. **ACCEPTED, built, main text as F17.**

**Placement, and why.** E2 produces evidence the thesis does not otherwise have. Every
persisted state matrix in the repository is teacher-forced, so nothing had ever looked at
the free-running trajectory — the regime the whole arm is about. It carries a
pre-registered, falsifiable claim, and it **refuted half of it**. That is evidence rather
than illustration, so it takes a main-text slot.

**Outcome against the pre-registration.** The claim, as written by session 2 before any of
this code existed: *the connectome's free-run attractor retains the true Lorenz climate to
a higher `f` than the nulls do, and the collapse when it comes is a change of shape rather
than a drift of scale.*

- **First clause: CONFIRMED.** At `f` ≥ 0.30, σ = 2, the connectome holds a faithful
  climate in **0.43** of cells against the nulls' **0.14** (frozen capture, 30 cells per
  (variant, `f`)). Read instead as the fixed-point rate over `f` ≥ 0.20 on the fresh
  capture: connectome **0.43**, weight-permuted 0.64, degree-matching 0.66, ER 0.70.
- **Second clause: REFUTED, and this is the more interesting half.** The collapse is
  overwhelmingly a loss of **scale**: the free-run falls onto a fixed point and the
  attractor's spread goes to zero. The ratio of free-run spread to true spread is itself
  **bimodal** — 229 of 440 cells below 0.05, 158 between 0.90 and 1.10, **11 anywhere
  between** — and it agrees with `climate_error` (206 of the 229 point-collapsed cells
  have climate error > 2). "Wrong shape, right scale" describes 34 cells out of 440.
- **Why the refutation strengthens the chapter.** `TIER0` §3.9's one-dimensional map
  argument says a gain above +1 gives a stable non-zero **fixed point** and below −1 a
  period-2 orbit, with nothing stable between. A free-run collapsing to a point *is* that
  fixed-point branch — now observed in the closed loop, on a measurement never made
  before, with an order parameter that turns out to be binary in exactly the way curvature
  is. Two independent order parameters, one under teacher forcing and one under autonomous
  rollout, both two-valued.

**Two reductions of the specification, both on stated grounds.**

1. **The object is the 3-D generated trajectory, not a PCA of the free-run reservoir
   states.** The specification asked for "PCA on the time-centred free-run states". The
   generated trajectory is strictly better: it is *exactly* what `climate_error` scores,
   so the figure explains the existing scalar instead of introducing a rival to it; and
   the Lorenz x/y/z coordinates are a common basis for every substrate **by
   construction**, which **dissolves the specification's own constraint 2** (rotation and
   sign making "connectome looks different from ER" a possible basis artifact) rather than
   managing it. It also cannot be misread as the subspace the readout computes in, which
   is constraint 1 and would contradict F6. Constraints 3 (Lorenz only) and 4 (governance)
   were honoured as written.
2. **The metric path is reused, not reimplemented.** `free_run.py` imports `lorenz.py`'s
   own `_fit_ridge_readout`, `_extract_reservoir`, `_sync_state`, `_free_run` and
   `_climate_error` and drives them in the evaluator's order, and asserts in-process that
   the reused path returns `evaluate()`'s `climate_error` to floating point. No frozen
   evaluator, hyperparameter or artifact was touched.

**Cost, measured before the capture.** 1.27 s per Lorenz cell at N = 448 on one BLAS
thread, median of three on the real code path — not a component estimate (`TIER0` §2.5).
440 cells → 338 s wall at 4 workers. Laptop; ada never involved; the 20 Aug freeze was
never in play.

**The limit this capture found, and why it shapes everything above.** Per-cell
`climate_error` is chaotic in the BLAS reduction order over the rollout's 81.5 Lyapunov
times (§2.6 finding 5). So: seed medians only; the capture runs in one pass at a pinned
thread count and is never spliced onto the frozen capture; the integrity gate against the
frozen parquet is **distributional** (which side of the faithful/collapsed separation each
cell falls on — 39 of 44 agree), never cell-for-cell; and **the scalar claim is quoted
from the frozen capture**, which carries 30 cells per (variant, `f`) against this
capture's 10. The fresh capture's job is the trajectories, which nothing else holds.

### 6.2 E1 — the two curvature regimes made visible. **ACCEPTED, built, supplementary as S2.**

**Placement, and why.** E1 makes **no claim the main text does not already make**:
curvature is bimodal is F12's claim and contribution 4's. What it adds is temporal
intuition — the gap `act2_manifold.md` §5 item 15 records, where Act II characterises only
the *spatial* axis of the manifold and hands the temporal one over as a boundary, so that
F12 currently introduces curvature to a reader with no run-up. Under the amended S-figure
bar ("no new claim" being the whole test), that is a supplementary figure. It prints in
**chapter 5** and lives in `figures/act3_prediction.py` — the F3 and F16 arrangement,
where the act decides the module and the chapter is stated separately.

**What it turned out to add beyond illustration.** Panel (c) does something F12 cannot:
F12 plots one *mean* curvature per cell and shows the means are bimodal **across** cells,
which leaves open whether each mean is averaging a spread. The per-step turning-angle
distributions show they are not — within a single cell the angles are tightly concentrated
near 0.26 rad or near π. That is "gated, not graded" seen from inside one cell.

**Both inherited constraints honoured.** It shows a **regime**, not a capacity, and it is
captioned that way; and it is not a PCA at all, so the F6 contradiction the constraint
warns about cannot arise. Drawn at `f` = 0.25 on the connectome, never at `f` = 0 where
curvature is flat at 0.26 rad across the whole sweep.

**One thing went wrong and the gate caught it — worth recording.** The cell was first
hard-coded from the frozen panel (connectome, `f` = 0.25, seed 4, σ = 2.8 → 3.2, curvature
0.2597 → 2.7591). On this machine that cell is **already collapsed at σ = 2.8** (2.78 rad)
and `bulk95` reads 0.3804 against the frozen 0.3974. This is `TIER0` §6.4 exactly: the
`f` > 0 flip pattern is not machine-portable, because `np.argsort` breaks ties unstably on
a heavily-tied edge score, and the frozen capture came from ada. **Selecting a cell from
the frozen panel is precisely the cross-machine splice §6.4 forbids.** The fix is to scan
on the capturing machine and assert the straddle it finds; E1's claim is about the
*phenomenon* — curvature steps between two regimes in one grid step — not about any
particular realisation of it. The scan chose seed 1, σ = 2.0 → 2.4, curvature 0.257 →
2.822, VPT 0.37 → 0.02, climate error 0.06 → 5.00. **A hard-coded frozen cell would have
produced a figure with two collapsed panels and no visible defect.**

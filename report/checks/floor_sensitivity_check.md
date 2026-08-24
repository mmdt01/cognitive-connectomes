# Verification check: the Gram spectrum against the ridge floor

**Written 24 August 2026.** Verification only. No figure was built, no figure was
registered, no canonical document was edited, and no simulation was run. Every number
below comes from frozen artifacts under the 20 August experiment freeze.

**What is being checked.** `TIER0_STATE_OF_PLAY.md` §3.6 records, under a *rejected*
anisotropy hypothesis, a refit at the correct end of the spectrum: where each substrate's
design-Gram spectrum sits relative to the ridge floor, measured by the exact sensitivity
of `d_eff` to that floor. `report/CROSS_ACT_SPINE.md` makes this step 3 of the causal chain and
Act II's restructure depends on it, but it has never been made into a figure and the
spine records it as "pending verification". This check answers whether it reproduces and
whether a figure is feasible without a run.

**Verdict in one line.** Task 1 reproduces in all sixteen cells once one undocumented
definition is recovered; the coverage in Task 2 is a complete four-variant,
sigma-resolved, three-task factorial with `eig_gram` present in every row; Task 3's
sigma-resolved claim reproduces with one correction to how "minimum" must be worded; a
standalone figure is buildable from frozen data alone, so **(b)** holds and **(c)** is
refuted.

---

## Provenance: which file supplied the Gram spectra, and which alpha

**Source of record:** `experiments/human/analysis/results/scale_448/covariance_spectra.parquet`
(27 MB, 8,190 rows, one row per cell, columns `eig_cov` and `eig_gram` as per-cell arrays).
It is the **only** artifact in the repository carrying Gram spectra.
`probe3_deff.parquet` carries `d_eff` and `pr` as scalars only and has no spectrum column,
so it cannot supply any of the four statistics; `manifold_metrics.parquet` and
`saturation_diagnostics.parquet` carry neither.

**Second artifact, derived not independent.**
`experiments/human/analysis/criticality_matched/results/closeout_floor_mass.csv`
(910 data rows) is the per-cell table §3.6's numbers were aggregated from. It is written by
`criticality_matched/closeout.py:floor_mass` and is gitignored
(`.gitignore:255`), as is the parquet (`.gitignore:229`); both are local regenerable
artifacts, which is this repository's norm. The CSV was **not** trusted: every one of its
910 rows was recomputed from the parquet and agrees to floating point (see §1.1). It is a
derivative of the parquet, not a second source.

**Alpha.** The MC ridge `alpha` is **1e-6**, and it is the same value in every place it
appears:

| where | value | note |
|---|---|---|
| `experiments/human/human_mc/task_config.py:26` | `ridge_alpha=1e-6` | the task's own hyperparameter |
| `results/scale_448/readout_config.json`, `tasks.mc.alpha` | `1e-06` | the recorded readout configuration |
| `covariance_spectra.parquet`, `alpha` column | `1e-06` for all 2,730 MC rows | the file's own column |
| `probe3_deff.parquet` filter used by F6(b, c) | `alpha == 1e-6` | the only alpha captured supercritically |
| `closeout.py:floor_mass(alpha=1e-6)` | `1e-6` | hard-coded default, equal to the column |

`manifold/spectra.py:173` reads `params, alpha = spec["params"], spec["params"]["ridge_alpha"]`
and passes that same `params` dict to `spec["evaluate"]`, the call that produces the `mc`
column, so the ridge floor `d_eff` is measured against and the ridge the readout is solved
with are literally the same float, not two copies of one number. This is Act II's §2.6
finding 1, re-confirmed here because the +0.999 `d_eff`/MC correspondence
(`TIER0` §3.3) is what licenses reading the floor account as a memory account, and it is
void if the two alphas ever drift.

**One caveat on the hard-coded alpha, stated rather than left implicit.**
`closeout.py:floor_mass` takes `alpha` as a default argument and does *not* read the
file's own `alpha` column. For MC the two are equal, so nothing in §3.6 is affected. They
are **not** equal for the other two tasks in the same file (NARMA-10 is at 1e-8, Lorenz at
1e-7), so any sigma-resolved extension to another task must read the column rather than
inherit the default.

---

## Task 1: the supercritical table of `TIER0` §3.6

### 1.0 Definitions, taken from `TIER0` §3.6 and the code that produced it

`TIER0` §3.6 states the measure and the filter but not the aggregation or the treatment of
zero eigenvalues. Both were recovered from `closeout.py:floor_mass`, which is the
generator, and both are load-bearing:

1. **Object:** the design-Gram spectrum `eig_gram`, not the covariance spectrum. For MC the
   design is the raw 2500 x 448 post-warmup state matrix with no bias column, so
   `eig_gram` has 448 entries.
2. **Floor sensitivity:** `-d(d_eff)/d(log alpha) = sum_i g_i*alpha/(g_i+alpha)^2`, a
   derivative with respect to the **natural** log of alpha, so its units are `d_eff`
   units per e-fold.
3. **Zeros are stripped first.** `floor_mass` does `g = g[g > 0]` before computing all four
   statistics. This is the definition `TIER0` does not state, and without it the fraction
   below alpha does not reproduce for any variant (see §1.3).
4. **Modes within a decade of alpha:** `(g > alpha/10) & (g < alpha*10)`, strict at both ends.
5. **Fraction below alpha:** `(g < alpha).mean()` over the **zero-stripped** spectrum.
6. **Filter:** `task == "mc"`, `condition == "human_empirical"`, `spectral_radius >= 3.05`.
   On this file's sigma grid that selects 5 grid points (3.0526, 3.5789, 4.1053, 5.1579,
   6.0000), so 50 cells per variant.
7. **Aggregation:** median over those 50 cells, per variant. This is `CONVENTIONS`' median
   rule and it is the only aggregation that returns the published table; the mean over the
   same cells gives 10.77% for the connectome's fraction below alpha against a published
   6.6%.

### 1.1 Cell-for-cell check of the derived table against the parquet

All 910 rows of `closeout_floor_mass.csv` recomputed from `covariance_spectra.parquet`:

| column | max absolute deviation over 910 rows |
|---|---|
| `d_eff` | 5.7e-14 |
| `floor_sensitivity` | 7.1e-15 |
| `n_within_decade` | 0 (exact) |
| `n_below_floor` | 0 (exact) |
| `frac_below_floor` | 1.1e-16 |

The derived CSV is therefore a faithful function of the frozen parquet and adds no
information of its own. Everything below is quoted from the recomputation, not from the CSV.

### 1.2 The reproduction table

Supercritical (`spectral_radius >= 3.05`), `condition == "human_empirical"`,
`task == "mc"`, `alpha == 1e-6`, median over 50 cells per variant. Recomputed values are
given to more digits than `TIER0` publishes, then to three significant figures.

| variant | quantity | `TIER0` §3.6 | recomputed | to 3 s.f. | reproduces |
|---|---|---|---|---|---|
| connectome | floor sensitivity | **8.85** | 8.8502 | 8.85 | **yes**, every published digit |
| connectome | modes within a decade | 36 | 36.0 | 36.0 | **yes**, exact |
| connectome | fraction below alpha | **6.6%** | 6.614% | 6.61% | **yes**, at the published precision |
| connectome | `d_eff` | 412.9 | 412.940 | 413 | **yes**, every published digit |
| weight-permuted | floor sensitivity | 18.09 | 18.0910 | 18.1 | **yes**, every published digit |
| weight-permuted | modes within a decade | 84 | 83.5 | 83.5 | **yes**, with the rounding convention named below |
| weight-permuted | fraction below alpha | 48.8% | 48.800% | 48.8% | **yes**, every published digit |
| weight-permuted | `d_eff` | 223.1 | 223.125 | 223 | **yes**, every published digit |
| degree | floor sensitivity | 17.75 | 17.7524 | 17.8 | **yes**, every published digit |
| degree | modes within a decade | 82 | 82.0 | 82.0 | **yes**, exact |
| degree | fraction below alpha | 65.8% | 65.786% | 65.8% | **yes**, every published digit |
| degree | `d_eff` | 138.2 | 138.182 | 138 | **yes**, every published digit |
| Erdős–Rényi | floor sensitivity | **10.26** | 10.2617 | 10.3 | **yes**, every published digit |
| Erdős–Rényi | modes within a decade | 48 | 47.5 | 47.5 | **yes**, with the rounding convention named below |
| Erdős–Rényi | fraction below alpha | **79.4%** | 79.381% | 79.4% | **yes**, every published digit |
| Erdős–Rényi | `d_eff` | 74.8 | 74.769 | 74.8 | **yes**, every published digit |

**All sixteen cells reproduce.** Fourteen return every digit `TIER0` publishes. The two
that need a convention named are the weight-permuted and Erdős–Rényi mode counts: the
median of an even number (50) of integer counts lands on a half, and `TIER0`'s 84 and 48
are 83.5 and 47.5 rounded half-up. Under that convention both are exact; at a bare three
significant figures they read 83.5 and 47.5. This is a display convention, not a
disagreement, and a figure drawing these counts should plot the halves and let the caption
carry the integers, or say which it is doing.

**The `d_eff` column cross-validates against a second artifact.** The connectome's 412.940
is identical to `probe3_deff.parquet`'s per-variant supercritical median as reproduced in
`report/act2_manifold.md` §2.2 (412.94), and so are the other three (223.13, 138.18,
74.77). The two files were captured by different code paths onto the same cells, so the
agreement is a genuine cross-check that the filter and aggregation here are the ones Act II
already validated.

### 1.3 The one definition that had to be recovered, and what it costs if missed

Computed over the **full** 448-direction spectrum, without the zero-strip, the fraction
below alpha reads:

| variant | published (zero-stripped) | full 448 denominator | difference |
|---|---|---|---|
| connectome | 6.6% | 7.03% | +0.4 points |
| weight-permuted | 48.8% | 50.00% | +1.2 points |
| degree | 65.8% | 69.53% | +3.7 points |
| Erdős–Rényi | 79.4% | 83.59% | +4.2 points |

None of the four reproduces, and the error grows down the ladder because the number of
exactly-zero Gram eigenvalues does: median 1.0 for the connectome, 11.5 weight-permuted,
44.5 degree, 91.5 Erdős–Rényi. The other three statistics are unaffected, because a zero
eigenvalue contributes exactly 0 to `d_eff`, exactly 0 to the sensitivity, and is never
inside a decade of alpha; only the fraction has a denominator to move.

**This should be recorded in `TIER0` §3.6 by whoever owns it.** It is the same class of
gap Act II recorded for §3.12's pooled median and session 3 recorded for §1.2's per-seed
reindex: a published number that only one unstated aggregation returns. It is flagged, not
edited, because this file is not canonical for results.

**It also matters for the substance, not only for reproduction.** Those zeros are
numerically rank-deficient directions, already stripped past any recovery, and the
denominator choice decides whether they are counted as "below the floor" or excluded from
the population. Erdős–Rényi's headline 79.4% is on the smaller denominator, so it
*understates* how much of its spectrum is unusable: on all 448 directions the figure is
83.6%. Task 5 uses this.

---

## Task 2: coverage of `covariance_spectra.parquet`

Read from the file itself, not from `FIGURE_LIST`'s description of it.

**The grid is a complete factorial with no holes.**

| axis | levels | values |
|---|---|---|
| task | 3 | `mc`, `narma10`, `lorenz` |
| condition | 3 | `human_empirical`, `human_empirical_signed`, `human_gaussian` |
| variant | 7 | connectome, connectome_weight_permuted, degree_rewire, erdos_renyi, random_gaussian, clustering_rewire, modularity_rewire |
| spectral_radius | 13 | 0, 0.4211, 0.8421, 1.0526, 1.2632, 1.5789, 2.0, 2.5263, 3.0526, 3.5789, 4.1053, 5.1579, 6.0 |
| seed | 10 | 0 to 9 |

3 x 3 x 7 x 13 x 10 = **8,190**, which is exactly the row count. Zero duplicate keys, so
every cell of the grid is present exactly once.

**Counts, as a table.** Every cell below is a count of rows.

| task | condition | per variant | per (variant, sigma) | rows |
|---|---|---|---|---|
| mc | human_empirical | 130 | 10 | 910 |
| mc | human_empirical_signed | 130 | 10 | 910 |
| mc | human_gaussian | 130 | 10 | 910 |
| narma10 | human_empirical | 130 | 10 | 910 |
| narma10 | human_empirical_signed | 130 | 10 | 910 |
| narma10 | human_gaussian | 130 | 10 | 910 |
| lorenz | human_empirical | 130 | 10 | 910 |
| lorenz | human_empirical_signed | 130 | 10 | 910 |
| lorenz | human_gaussian | 130 | 10 | 910 |

Restricted to the four-rung ladder the same table reads 40 rows per (task, condition,
sigma), i.e. 4 variants x 10 seeds, at **every one of the 13 spectral radii**, for all
nine (task, condition) pairs.

**`eig_gram` is present for all of them.** 8,190 of 8,190 rows carry a non-null, non-empty,
NaN-free `eig_gram` array, with no negative entries. Lengths are 448 for MC and 449 for
NARMA-10 and Lorenz, which is the bias column those two designs carry
(`readout_config.json`); `eig_cov` is 448 everywhere. It is **not** restricted to the
subset F6 panel (a) uses.

**Alpha varies by task and is a single value within each:** MC 1e-6, NARMA-10 1e-8,
Lorenz 1e-7. There is one `alpha` per row and no alpha sweep in this file.

**How much of the file F6(a) touches.** F6(a)'s source (`sources.py:_gram_spectra`) filters
to `task == "mc"`, `condition == "human_empirical"`, `variant == "connectome"`,
`spectral_radius == 3.0526`, which is 10 rows, and then selects the **one** seed whose
`d_eff` is nearest the median. So F6(a) reads **1 row of 8,190**, 0.012% of the file.

### The blocking question, answered directly

**Is a four-variant, sigma-resolved version available without a run? Yes.**

The four ladder variants are all present, at all 13 spectral radii, with 10 seeds each and
a usable `eig_gram` in every row, on the all-positive `human_empirical` condition that
Act II's chapter sits at. That is 520 cells for MC, of which the 200 supercritical ones are
what Task 1 aggregates and all 520 are what Task 3 uses. Nothing has to be simulated,
recaptured or regenerated. The sigma coverage is 13 points rather than the Task B sweep's
21, and it stops at sigma = 6 rather than 8, which bounds what a figure can draw but does
not block it.

---

## Task 3: the sigma-resolved claim

Task 2 shows the coverage exists, so this section computes rather than declines.

### 3.1 Floor sensitivity as a function of sigma, per variant

Median over 10 seeds at each of the 13 spectral radii, MC, `human_empirical`, alpha = 1e-6,
zero-stripped as in §1.0.

| variant | 0 | 0.42 | 0.84 | 1.05 | 1.26 | 1.58 | 2.00 | 2.53 | 3.05 | 3.58 | 4.11 | 5.16 | 6.00 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| connectome | 0.00 | 2.69 | 7.82 | 11.55 | 15.83 | 22.39 | 25.79 | 20.58 | 9.39 | **5.79** | 6.20 | 12.21 | 16.69 |
| weight-permuted | 0.00 | 4.48 | 20.16 | 30.96 | 33.72 | 2.82 | **2.38** | 19.18 | 26.12 | 22.49 | 18.31 | 12.47 | 8.96 |
| degree | 0.00 | 4.99 | 22.05 | 33.99 | 31.40 | **1.84** | 3.93 | 28.68 | 29.55 | 23.20 | 17.75 | 10.40 | 7.35 |
| Erdős–Rényi | 0.00 | 4.93 | 22.55 | 34.94 | 34.43 | 2.43 | **1.82** | 28.72 | 28.60 | 18.70 | 11.24 | 5.40 | 2.63 |

Floor sensitivity is **strongly sigma-dependent**, as §3.6 states, and the curve is
two-humped for every variant with a deep interior dip between the humps. That first claim
reproduces without qualification.

### 3.2 Argmin per variant

| variant | `TIER0` §3.6 | interior argmin, median curve | value | per-seed argmin (10 seeds) |
|---|---|---|---|---|
| connectome | sigma approx 3.6, value 5.8 | **sigma = 3.5789** | **5.785** | 8/10 at 3.5789, 2/10 at 4.1053 |
| weight-permuted | sigma approx 1.6 to 2.0, value in 1.8 to 3.9 | sigma = 2.0000 | 2.383 | 7/10 at 2.0000, 3/10 at 1.5789 |
| degree | same | sigma = 1.5789 | 1.837 | 7/10 at 1.5789, 3/10 at 2.0000 |
| Erdős–Rényi | same | sigma = 2.0000 | 1.815 | 5/10 at 1.5789, 5/10 at 2.0000 |

"Interior" means the argmin taken over `sigma >= 1.2632`, past the low-sigma hump for every
variant. The per-seed column is not in `TIER0` and is computed here as a robustness check:
the connectome's dip is at 3.5789 in 8 of 10 seeds, and **every null's dip is at 1.5789 or
2.0000 in 10 of 10 seeds**. The separation is a seed-level fact, not an artifact of
medianing.

**The locations reproduce exactly.** The connectome's 3.5789 is `TIER0`'s "approx 3.6" and
its 5.785 is the published 5.8; the nulls sit at 1.5789 and 2.0000, which is the published
"1.6 to 2.0".

**One correction to how "minimum" must be worded, and it is not cosmetic.** The dips above
are **interior local minima**, not global minima over the sigma grid. Every variant's floor
sensitivity falls monotonically to 0 as sigma goes to 0, because a dead reservoir has
almost no spectrum above the floor to be sensitive about: at sigma = 0.4211 the connectome
reads 2.687, *below* its interior minimum of 5.785, with `d_eff` = 20.8. So on the median
curve the connectome's global minimum over non-zero sigma is at 0.4211, not 3.5789. Read as
a global minimum the connectome's half of the claim does **not** reproduce; read as the
interior minimum of the two-humped curve, which is what the argument needs and what the
data supports, it reproduces exactly. **Any figure must draw the whole sigma curve and the
caption must say "interior minimum", never "minimum".** This is the same trap Task 5 is
about, one variable over: low sensitivity has two causes, and only one of them is the one
the chapter means.

**On the published value band for the nulls, "1.8 to 3.9".** The three null interior
minima are 2.383, 1.837 and 1.815, spanning **1.8 to 2.4**, not 1.8 to 3.9. The published
band is recovered only as the span of all six values the three nulls take across the two
grid points 1.5789 and 2.0000: those run 1.815 (Erdős–Rényi at 2.0) to 3.925 (degree at
2.0), i.e. **1.8 to 3.9** exactly. So the band reproduces under the reading "the null
minima sit somewhere in sigma 1.6 to 2.0 and the sensitivity across that region runs 1.8 to
3.9", and does not reproduce under the reading "the three null minima are 1.8 to 3.9". A
caption must not use the second. Flagged for whoever owns §3.6; not edited here.

### 3.3 The migration half of the claim

`TIER0` §3.6 says the measured ridge-optimal sigma migrates toward each substrate's own
floor-mass minimum as alpha rises, quoting connectome 2.4 to 3.6 and nulls 1.2 to 1.6.
That half lives in a different artifact,
`criticality_matched/results/taskB_extended_sweep_scale_448.parquet`, on a different sigma
grid (0 to 8, step 0.4). Recomputed from the parquet as the argmax over sigma of the
seed-median MC at each of the five stored alpha columns:

| alpha | connectome | weight-permuted | degree | Erdős–Rényi |
|---|---|---|---|---|
| 1e-8 | 2.4 | 1.2 | 1.2 | 1.2 |
| 1e-6 | 2.8 | 1.6 | 1.6 | 1.6 |
| 1e-5 | 3.2 | 1.6 | 1.6 | 1.6 |
| 7e-5 | 3.2 | 1.6 | 1.6 | 1.6 |
| 1e-3 | **3.6** | **1.6** | **1.6** | **1.6** |

This reproduces the frozen `taskB_mc_alpha_peaks.csv` exactly (max deviation 0.0 on the
peak sigma, 1.8e-15 on the peak MC across all 20 rows), and it reproduces `TIER0` §3.3's
"2.4 to 3.6" and "1.2 to 1.6" to the digit. The connectome's optimum moves monotonically
across five orders of magnitude of alpha; the nulls move once, at the first step, and then
stop.

### 3.4 Does the migration claim reproduce?

**Yes, in the form `TIER0` states it, and with two qualifications that must be carried into
any figure.**

- The connectome's optimum ends at sigma = 3.6, and its floor-sensitivity interior minimum
  is at 3.5789. The nulls' optima end at 1.6, and their interior minima are at 1.5789 and
  2.0000. Each substrate's measured optimum migrates toward, and lands on, its own
  floor-mass minimum. Both endpoints match for all four variants.
- **Qualification 1: two grids, two captures.** The floor-sensitivity curve is on the
  probe grid (13 points, 0 to 6) and the migration is on the Task B grid (21 points, 0 to
  8, step 0.4). 3.5789 and 3.6 are different grids' nearest points to the same place, not
  the same number, and so are 1.5789 and 1.6. A figure putting both on one sigma axis must
  say so rather than let the coincidence read as an identity.
- **Qualification 2: the tracking is not fitted.** `TIER0` §3.6 already states this as
  "consistent-with rather than proven", and this check does not improve on it. What is
  verified is that the migration direction and the endpoint match for all four variants.
  Nothing here fits the optimum to the sensitivity curve or bounds the residual, and a
  caption must not imply that it does.

---

## Task 4: feasibility

### The verdict

**(b) is true: a new standalone figure can be built from existing frozen data.**
**(c) is refuted.** (a) is also data-feasible but is the wrong form, for reasons given
below.

### The evidence

| requirement | status |
|---|---|
| Gram spectra for all four ladder variants | present, `covariance_spectra.parquet` |
| sigma resolution | 13 points, 0 to 6, complete for every variant |
| seeds | 10 per (variant, sigma), complete, no holes |
| `eig_gram` usable | 8,190 of 8,190 rows, no nulls, no NaNs |
| the four §3.6 statistics | reproduce in all sixteen published cells (Task 1) |
| the sigma-resolved claim | reproduces (Task 3), with the interior-minimum wording |
| the migration half | reproduces exactly from `taskB_extended_sweep_scale_448.parquet` |
| run needed | **none** |

### Why (b) and not (a)

(a) is possible on the data: F6's source module already opens the same parquet, and a
fourth panel could read a broader filter from it. It is the wrong form for three reasons,
all of which are governance rather than data:

1. **It is another session's module.** `report/figlib/figures/act2_manifold.py` is session
   2's, session 2 closed on 17 August, and `CONVENTIONS`' "edit your own act's module and
   nothing else" clause reserves cross-module edits to cross-act figures whose owner
   `FIGURE_LIST` names explicitly (the F3 and F16 arrangement).
2. **It would put two arguments in one figure.** F6 carries contribution 6, which is that
   a variance-weighted count cannot see readout-relevant structure. The floor account is a
   different claim: it is the chain's step 3, about *where the spectrum sits*, not about
   *which counting scheme sees it*. Session 1 cut the merged F3+F8 for exactly this reason
   and recorded that two arguments in one figure read as two half-figures.
3. **F6's layout has no room.** It is a five-column gridspec at 40:11:30:3:30 with two
   spacer columns and two independently tuned gaps, sized so that (b) and (c) share a y
   axis; a fourth panel means re-tuning all of it, and the panel-width reasoning in
   `report/act2_manifold.md` would have to be redone.

A standalone figure also fits the spine: `report/CROSS_ACT_SPINE.md` gives chapter 5 a section
called "The Gram spectrum against the ridge floor", separate from "Which counting scheme
sees it", and lists Act II's figures as "F4, F5, F6, plus the floor-sensitivity figure if
the check clears".

### What would have to change, and where. None of it has been done.

**1. `report/figlib/sources.py`** (additive; the existing `gram_spectra` source cannot be
reused, because it returns one cell tidied to one row per direction and the new figure
needs one row per cell across four variants and 13 sigma).

- A new loader, one row per cell, computing per cell from `eig_gram`:
  `d_eff`, `floor_sensitivity`, `n_within_decade`, `n_below_floor`, `frac_below_floor`.
- It **must** carry the zero-strip `g = g[g > 0]` and a comment saying why, since without it
  the fraction below alpha does not reproduce `TIER0` (§1.3 above).
- It **must** read `alpha` from the file's own column rather than hard-coding 1e-6, so a
  later extension to NARMA-10 or Lorenz cannot silently inherit the MC value.
- Filter: `task == "mc"`, `condition == "human_empirical"`, `variant in LADDER`. No sigma
  filter at load; the panels select.
- A matching `_ph_` placeholder with the identical schema, so `--smoke` renders the layout
  with no frozen data present. This is the house pattern for every source.
- A `Source(...)` entry in the `SOURCES` dict carrying the filter note, which `--verify`
  prints. The note should state the zero-strip and the median-over-cells aggregation.
- If the migration panel is wanted, either a second source over
  `taskB_mc_alpha_peaks.csv`, or a derived column on the existing `taskb` source. The
  existing `taskb` source already loads the parquet that contains the five alpha columns.

**2. `report/figlib/figures/act2_manifold.py`** (session 2's module; a builder function
plus its registry import).

- The builder, with the caption written first per `CONVENTIONS` working rule 2.
- Assertions against `TIER0` §3.6, in the house style: the four published floor
  sensitivities to 0.01, the connectome's interior argmin at 3.5789, and that every null's
  interior argmin is at 1.5789 or 2.0000. Content assertions gated off under `--smoke`,
  structural ones live on both paths, per Act II item 14.
- The caption must say **interior minimum**, must name the two grids if the migration panel
  is included, and must not use "1.8 to 3.9" as the span of the three null minima.
- **Ownership has to be recorded**, because session 2 is closed. The house precedent is the
  F3 and F16 arrangement: the act decides the module, and `FIGURE_LIST` names the owning
  session explicitly. That naming is part of the change, not an afterthought.

**3. `report/FIGURE_LIST.md`.**

- A new row: id, chapter 5, the contribution it carries, the claim in one sentence, the
  source with columns and the exact filter, and a status.
- The count line at the head of the file, currently "Count 16", updated with a stated
  reason. The 19 August amendment made the cap a soft count but kept the requirement that a
  session adding a figure edits this file and the registry **together** and writes down why.
- The builder-module table (`act2_manifold.py`, session 2) updated, with the cross-session
  ownership stated the way F3's and F16's are.

**4. `report/figlib/figures/__init__.py`.**

- The import of the new builder from `act2_manifold`.
- A `FIGURES` entry.
- `assert len(FIGURES) == 16` updated to 17, with the reason added to the comment block
  above it, in the same style as the 15-to-16 note. That assertion is the one place a
  session must edit and therefore justify, which is the part of the old cap rule that
  survived.

**5. Recommended but not required for the figure, and not this file's to make:**
`TIER0` §3.6 should gain a line naming the zero-strip aggregation, for the reason §1.3
gives. It is rank 1 and this is a check file; sessions 0, 2 and 3 each amended `TIER0` only
on the author's explicit decision, and this is logged for the same.

---

## Task 5: is Erdős–Rényi's low floor sensitivity degenerate?

**The claim under test:** Erdős–Rényi's floor sensitivity (10.26) is low for a degenerate
reason, namely that it has almost nothing left to strip.

**Verdict: CONFIRMED, and by a wide margin.** Two independent measurements say so.

### 5.1 Where each substrate's spectrum sits relative to the floor

**Per-bin medians over the 50 supercritical cells**, as a percentage of all 448
directions. The four bins partition each *individual* cell exactly, but four medians taken
separately are not constrained to sum to 100, and they do not: the connectome's four come
to 102.1%. An earlier draft of this line called them "the median cell", which is a
different statistic (one cell selected as the median) and would return different numbers;
corrected 24 August 2026, the values below were always the per-bin medians.

| variant | exactly zero | more than a decade below alpha | within a decade of alpha | more than a decade above alpha |
|---|---|---|---|---|
| connectome | 0.2% | 4.9% | 8.0% | **89.0%** |
| weight-permuted | 2.6% | 36.0% | 18.6% | 38.1% |
| degree | 9.9% | 49.3% | 18.3% | 22.0% |
| Erdős–Rényi | **20.4%** | **52.8%** | 10.6% | **11.4%** |

**73.2% of Erdős–Rényi's directions are already gone** before the floor is raised at all:
one fifth are numerically rank-deficient and another half sit more than a decade below the
floor, where the sensitivity term `g*alpha/(g+alpha)^2` is under 0.09 of its maximum and
falling. Only 11.4% of its spectrum stands clear of the floor by a decade. The connectome's
profile is the reverse: 89.0% stands more than a decade clear, and only 5.1% is at or below
the floor.

So the two low sensitivities have opposite causes. The connectome's is low because its
spectrum is **above** the floor; Erdős–Rényi's is low because its spectrum is **below** it.
The sensitivity term vanishes at both ends, which is precisely why a single number cannot
distinguish them and why the chapter must say which end each substrate is at.

### 5.2 The supporting check: 79.4% below alpha against `d_eff` = 74.8

These are two views of the same fact and they agree quantitatively.

- The published 79.4% is on the zero-stripped denominator of 356.5 positive modes, so it
  counts 266 modes below alpha and leaves about 90 above it.
- On all 448 directions, 83.6% are below alpha, leaving about 73 above.
- `d_eff` = 74.769. So `d_eff` is essentially a count of the directions that clear the
  floor, and 448 minus 74.8 = 373 directions, **83% of the reservoir**, contribute nothing
  a ridge readout can use.
- The connectome's arithmetic runs the other way: 6.6% below alpha and `d_eff` = 412.9 of
  448, so 92% of its directions are usable.

Erdős–Rényi therefore has about **75 directions left to lose**, against the connectome's
about **413**. That is the "almost nothing left to strip" statement, quantified.

### 5.3 The decisive measurement: sensitivity relative to what survives

| variant | `d_eff` | floor sensitivity | sensitivity as % of `d_eff` | `d_eff` lost per decade of alpha | as % of `d_eff` |
|---|---|---|---|---|---|
| connectome | 412.94 | 8.85 | **2.14%** | 23.3 | **5.6%** |
| weight-permuted | 223.13 | 18.09 | 8.11% | 52.1 | 23.3% |
| degree | 138.18 | 17.75 | 12.85% | 37.6 | 27.2% |
| Erdős–Rényi | 74.77 | 10.26 | **13.72%** | 21.8 | **29.1%** |

**Erdős–Rényi is the most floor-sensitive substrate in the ladder, not the least.** Per unit
of surviving dimensionality it is 6.4 times as sensitive as the connectome. Its absolute
sensitivity is low only because `d_eff` is low: raising alpha by a decade costs it 21.8
`d_eff` units against the connectome's 23.3, almost the same absolute loss, but that is 29%
of everything Erdős–Rényi has against 5.6% of what the connectome has.

### 5.4 The wording this licenses, and the wording it forbids

- **Defensible:** Erdős–Rényi's floor sensitivity is low because most of its spectrum has
  already fallen below the floor, so there is little left for the floor to remove. Only 75
  of 448 directions survive, against the connectome's 413, and 73% of its spectrum is
  already a decade or more below alpha. The connectome's low sensitivity has the opposite
  cause: its spectrum stands clear of the floor.
- **Not defensible, and easy to write by accident:** that raising alpha costs Erdős–Rényi
  little. It costs it 29% of its remaining dimensionality, the most of any substrate in the
  ladder. The stock is nearly exhausted; the *rate* is the highest on the ladder. A
  sentence that conflates the two would be wrong in the direction that flatters the
  connectome, which is the direction this project has already been caught in three times.

---

## Summary of what reproduced

| item | verdict |
|---|---|
| §3.6 floor sensitivity, all four variants | reproduces, every published digit |
| §3.6 modes within a decade, all four | reproduces; two are half-integers rounded half-up |
| §3.6 fraction below alpha, all four | reproduces, but only with the undocumented zero-strip |
| §3.6 `d_eff`, all four | reproduces, every published digit, and cross-checks against `probe3_deff.parquet` |
| derived `closeout_floor_mass.csv` against the parquet | reproduces cell for cell, 910 rows, to floating point |
| four-variant sigma-resolved coverage | exists in full; no run needed |
| "floor sensitivity is strongly sigma-dependent" | reproduces |
| "each substrate's minimum sits at a different sigma" | reproduces as an **interior local** minimum; fails as a global minimum |
| connectome minimum at sigma approx 3.6, value 5.8 | reproduces exactly (3.5789, 5.785), 8 of 10 seeds |
| nulls' minima at sigma approx 1.6 to 2.0 | reproduces exactly, 10 of 10 seeds for all three |
| nulls' value band "1.8 to 3.9" | reproduces only as the span across the minimum region, not as the span of the three minima |
| migration of the measured optimum with alpha | reproduces exactly (2.4 to 3.6; 1.2 to 1.6) |
| Erdős–Rényi's low sensitivity is degenerate | confirmed |

**Nothing failed the reproduction gate.** Two items needed a definition or a reading
recovered before they returned, and both are recorded above with what should be added to
`TIER0` §3.6: the zero-strip, and the interior-minimum wording.

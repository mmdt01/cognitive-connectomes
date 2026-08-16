# Master figure list

**Fixed in session 0, 15 August 2026. Cap 15 — the list is at the cap.** No session
creates a figure that is not here; if one seems missing, report and stop. `W` marks the
workshop subset (5pp, 4 figures).

**The cap was 14 and was raised to 15 in session 0, deliberately and once.** The draft
list gave contribution 2 — the unifying claim, and the crossing it turns on — no figure
of its own, on the reasoning that F7 and F13 carry it jointly. They do not: F7 is memory
against `sigma·bulk95` at f = 0 and F13 is VPT against f at sigma = 2, two orthogonal 1-D
slices, and no pair of slices shows that the two advantage regions occupy *opposite
regions of the (f, sigma) plane*. F16 was added for that. The cap is 15 now; it is not a
precedent, and a session that wants a sixteenth reports and stops.

Every entry has been checked against the frozen artifacts: the file exists, the named
filter returns rows, and where `TIER0` states a number the filter reproduces it. Every
figure is built by `report/figlib` (`python -m report.figlib --only F7`), and the filters
below are the ones encoded in `report/figlib/sources.py`, not a parallel description of
them.

**Where a figure's builder lives.** `report/figlib/figures/` is a package with the
registry in `__init__.py` and the builders in **one module per act, which is one module
per sweep session** — so a session edits its own module and nothing else:

| module | session | figures |
|---|---|---|
| `act1_structure.py` | 1 | F1, F2, **F3**, S1 |
| `act2_manifold.py` | 2 | F4, F5, F6 |
| `act3_memory.py` | 3 | F7, F9, F10, F11 |
| `act3_prediction.py` | 4 | F12, F13, F14, **F16** |
| `act4_anchor.py` | — | F15 |

**The act decides the module, not the chapter**, and the two cross-act figures are why
that matters: F3 prints in chapter 3 but is Act I's argument and Session 1 renders it;
F16 prints in chapter 6 but needs both Act III arms, so Session 4 renders it. The
per-figure ownership flags below remain canonical.

**Cut made:** the draft's F3 and F8 both served contribution 5 and were merged into one
two-panel F3 in chapter 3 where contribution 5 lives. **F8 is retired and its ID left
unused** rather than renumbering, so references elsewhere still resolve. **Session 1 then
cut the merged-in panel too** (see the F3 flag): the two panels argued different things
and read as two half-figures, so F3 is now a single panel and F8's content is methods
prose. The ID count is unchanged — F8 stays retired either way. **F16 added** for
contribution 2. Rendered figures: F1 to F7, F9 to F16 = 15. IDs are stable identifiers,
not a reading order, so F16 sitting in chapter 6 after chapter 7's F15 is intended.

Status: `confirmed` = source verified and filter reproduces `TIER0`; `confirmed*` = source
verified, see the flag below the table.

| id | ch | contr. | claim it carries | source, columns, filter | status | W |
|----|----|--------|------------------|-------------------------|--------|---|
| F1 | 4 | 1 | The spectrum is one large real Perron eigenvalue separated from a bulk that is essentially the nulls' bulk | `eigenspectrum/results/scale_448/spectra_per_seed.parquet`; `eig_w_real` (448 floats/row), `bulk95`, `lambda_max_raw`; filter `condition == "human_empirical"` and `variant in LADDER` (40 rows) | confirmed* | W |
| F2 | 4 | 1 | The difference is a **gap**, not a bulk: absolute bulk near-identical (4.4% spread at N=448), gap ratio 3.078 vs 1.81-1.92 | same file at `scale_448` **and** `scale_1000`; `abs_bulk = median(bulk95) * median(lambda_max_raw)`, `gap_ratio = 1/median(bulk95)` | confirmed* | W |
| F3 | 3 | 5 | **Neither axis is neutral.** (a) connectome and ER on nominal sigma, (b) the same two on `sigma·bulk95`, (c) the deltas: +343.3 at nominal 4.47 / -217.4, against +196.5 at 1.949 / -24.0 | `criticality_matched/results/e02_panel.parquet` filter `interp == "linear"`, cols `x, axis, d_eff_connectome, d_eff_erdos_renyi, dD_median, dD_q25, dD_q75`; plus `e02_axis_summary.csv` (2 rows) | confirmed* | |
| F4 | 5 | (Act II) | The Perron mode is a common mode: it carries the mean, and after time-centring the dominant W-eigenmodes carry ~0 of the fluctuation variance | `results/scale_448/manifold_alignment.parquet` filter `condition == "human_empirical"`, `variant == "connectome"`, `task == "mc"`, supercritical operating point; plus `saturation_diagnostics.parquet` `mean_state` | confirmed* | |
| F5 | 5 | (Act II) | Sign selects the basis: balanced -> W-eigenmodes, all-positive -> low-frequency graph harmonics | `manifold_alignment.parquet`; one panel per `condition`, curves over `basis in {harmonics, wmodes, random}`, `task == "lorenz"` | confirmed* | |
| F6 | 5 | 6 | PR misses readout-relevant structure: against measured MC across the seven rungs, `d_eff` orders at **+1.000** and PR at **+0.107**; pooled within-regime +0.998 against +0.308 | `results/scale_448/probe3_deff.parquet`; filter `task == "mc"`, `condition == "human_empirical"`, `spectral_radius >= 3.05`, `alpha == 1e-6` (350 rows, 7 variants) | confirmed | |
| F7 | 6 | 3 | **The crossing**: the connectome peaks lowest (432.4) yet retains most (47% at the top of the overlap, against 28/22/11%, `TIER0` §1.2); `d_eff` decay on the matched axis, ceiling drawn | `criticality_matched/results/taskB_extended_sweep_scale_448.parquet`; `variant, spectral_radius, bulk95, d_eff`; no row filter (f = 0, MC, 4 variants, sigma 0 to 8 step 0.4, 10 seeds); `x = spectral_radius * bulk95` from the file's own column | confirmed | W |
| ~~F8~~ | | | **RETIRED — merged into F3.** Do not render. | | retired | |
| F9 | 6 | 3 | The supercritical margin holds across a 2.2x change in N: **4.40 -> 4.42** on the connectome's `sr_crit` applied to all, **3.56 -> 3.85** on each variant's own. Both panels, per `TIER0` §2.4 | `n1000_memory_scale_448.parquet` + `n1000_memory_scale_1000.parquet`; supercritical = `spectral_radius >= 3.078` (N=448) / `>= 3.985` (N=1000), i.e. **the connectome's `sr_crit`, applied to every variant** | confirmed* | |
| F10 | 6 | 3 | Peak parity, not deficit: paired per-seed differences with CIs across the alpha grid; 2-6%, reliable against ER and weight-permuted, **not** against degree-matching | `criticality_matched/results/closeout_peak_parity.csv`; 15 rows = 5 alpha x 3 contrasts, cols `mean_diff, ci_lo, ci_hi, wilcoxon_p` | confirmed | |
| F11 | 6 | 3 | Rescue from Perron domination: `\|mean_state\|` 0.759 against the nulls' 0.949-0.989 at sigma = 6, f = 0; and matching on `sigma·bulk95` absorbs only **26%** of the f = 0 gap | (a) `item2_f_extension_scale_448.parquet` + `item3_f_extension_nulls_scale_448.parquet`, filter `task == "mc"`, `spectral_radius == 6.0`, col `mean_state` by `f`. (b) `e03_mechanism_matched_scale_448.csv` cols `median_abs_gap_matched_x` vs `..._sigma` (6.42 -> 4.75 at f = 0) | confirmed | |
| F12 | 6 | 4 | Curvature is **bimodal**: 215 of 38,280 cells (0.56%) lie in [0.6, 2.2] rad; a binary collapsed-or-not bit explains R2 = 0.364 against continuous curvature's 0.371 | `criticality_matched/results/e01_jacobian_scale_448.parquet`; cols `mean_curvature, vpt`; no row filter (38,280 Lorenz cells = 4 variants x 11 f x 29 sigma x 10 seeds x 3 draws) | confirmed | W |
| F13 | 6 | 4 | Generation read as VPT: +1.0 to +2.2 Lyapunov times from f ~ 0.20 at sigma = 2, clearing the weight-permuted placement control; **plus the f = 0 collapse panel** (ER 5/10 seeds, connectome 0/10) | (a) `e03_frontier_scale_448.parquet` filter `metric == "vpt"`, `spectral_radius == 2.0`. (b) `e03_frontier_paired_scale_448.csv` same filter — paired within seed, so all connectome-minus-null statements come from here. (c) `item2_collapse_loci_scale_448.csv` filter `f == 0`, cols `n_seeds_collapsed / n_seeds` | confirmed | |
| F14 | 6 | 4 | `sigma_eff` is a **locator, not a criterion**: transition at 0.77-0.90 with variant offsets ordered by spectral gap; CV 0.209 against nominal sigma's 0.667 | `e01_threshold_invariance_scale_448.csv` filter **`scope == "f > 0"`** (n = 37); plus `e01_threshold_table_scale_448.csv` cols `effective_radius_lo/hi` per (variant, f) | confirmed* | |
| F15 | 7 | anchor | Which Yeo networks load the Perron mode (minimal Act IV) | **computed live, no frozen parquet**: leading eigenvector of the N=448 self-built consensus (`eigh`) x release RSN labels from `data/human/Suarez2021_Data`, restricted to cortical nodes. Seconds, not a run | confirmed* | |
| F16 | 6 | **2** | **The crossing, with its axis and its coverage.** The memory and generative boundaries on both axes: on `sigma·bulk95` they cross at (2.938, 0.153) inside full replicate coverage; on nominal sigma they do not cross at all once the sweep passes sigma = 6 | `e02_heatmap_boundaries_extension.csv` + `..._extension_nominal.csv` concatenated with an `axis` column; `panel == "dD"` is the memory boundary and `"dStraight"` the generative one; use `f_star` (level over fully covered cells). Coverage mask from `e02_heatmap_coverage_extension.csv` (`x_hi` per f, minimum 3.58) | confirmed* | |

Contributions 1 to 6 are the roadmap §1 list. F1/F2 carry 1, **F16 carries 2**, F7/F9/F10/F11
carry 3, F12/F13/F14 carry 4, F3 carries 5, F6 carries 6. Contribution 2's *out-of-sample*
test remains the Mackey-Glass pre-registration rather than a panel; F16 carries the claim
itself.

---

## Supplementary figures — appendix, outside the cap

**Added 15 August 2026 (session 1), at the author's request.** These are **not** part of
the numbered main-text list and do **not** consume a main-text slot: `FIGURES` in
`report/figlib/figures/__init__.py` still holds exactly 15 and still carries the
assertion that enforces it. S-figures live in a separate `SUPPLEMENTARY` registry, and
`python -m report.figlib` renders both. The rule that no figure exists outside this file
still binds, which is why they are listed here.

**The bar for an S-figure, so this does not become a way around the cap:** it makes **no
claim the main text does not already make**, and it is built by an **existing builder at
different parameters**. Anything needing its own builder is a new figure and goes through
the cap — report and stop.

| id | main-text twin | what it adds | source, columns, filter | status |
|----|----|----|----|----|
| S1 | F1 | F1 rebuilt at **N = 1000**. Same builder, same claim, larger parcellation; shows the gap-ratio separation surviving a 2.2x change in N, and makes the null-ordering reversal visible | `eigenspectrum/results/scale_1000/spectra_per_seed.parquet` (source `spectra_1000`); `eig_w_real` (1000 floats/row), `bulk95`, `lambda_max_raw`; filter `condition == "human_empirical"` and `variant in LADDER` (40 rows) | confirmed |

**S1 — the row ordering is NOT monotone at N=1000, and the caption must not imply it
is.** Rows a-d are in ladder order, and at N=448 that happens to coincide with descending
gap ratio (3.08, 1.92, 1.87, 1.81), which is why F1's caption can say "rises from 1.81 to
3.08". At N=1000 the same rows read **3.99, 2.39, 2.30, 2.44** — the ER row's gap ratio
exceeds the degree row's, because the null ordering by `bulk95` reverses between scales
(`TIER0` §2.1). The connectome's ~1.7x separation from every null holds at both. Quote
the separation, never the sweep down the column.

**S1 — the builder is shared, so F1's flags all apply.** Median-`|lambda_1|` scaling,
per-row `[-lambda_1, +lambda_1]` binning and the two assertions that guard them are in
the common code path; S1 cannot drift from F1 without both moving together.

---

## Flags — read these before rendering

Each is a place a session would otherwise get a defensible-looking figure that is wrong.

**F1 — REBUILT 15 August 2026 (session 1), on the E0.4 figure's layout.** F1 now uses
the small-multiples layout of the committed `eigenspectrum/figures/fig1_spectrum.png` —
one substrate per panel, an ECDF, a per-seed strip — with **every axis re-pointed from
`bulk95` to the gap**. That source figure is titled "Connectome weight placement
compresses the eigenvalue bulk" and draws all six panels in units of `|lambda_1|`;
normalising each substrate by its own Perron root, which is the only thing that differs,
is exactly what makes the connectome's band look narrow.

**(a-d) are stacked vertically down the left on one shared raw-units axis**, so the four
bulk bands sit at the same page coordinate and the reader sights down the column: the
bulk edges align (0.0587 to 0.0614, 4.4% spread) while the grey gap out to `lambda_1`
grows from row d to row a. That stacking is what carries the claim. **(e) is top right
and is the NORMALISED ECDF** — the units every spectral-radius-matched comparison in the
thesis uses — where the curves separate everywhere and `bulk95` is readable off the
95th-percentile crossing (0.325 against 0.52 to 0.55). **(f) is bottom right**: the
per-seed gap ratio, with `bulk95` on the right-hand axis.

A raw-units ECDF was tried as (e) and dropped: with the panels stacked it made the same
"common bulk, different tail" point less directly than the stack itself, so (e) was
freed for the normalised view instead. The consequence is that **a-d carry the entire
raw-units argument alone**, and the caption must tie (e) back to them as the same
spectra one division apart rather than leaving the two unit systems to sit unremarked.

**Panels a-d draw one spectrum each** — for the nulls, the seed whose `bulk95` is
nearest the median — so all four carry 448 eigenvalues at equal sampling noise rather
than the connectome's 448 against the nulls' pooled 4,480. Panels e and f use all 10
seeds.

**That spectrum is scaled by the MEDIAN `|lambda_1|`, not by its own seed's, and the
builder asserts it.** Mixing the two puts the bars and the furniture on different
aggregations: the seed is chosen for `bulk95`, which constrains its `|lambda_1|` not at
all, so the largest eigenvalue lands off the `lambda_1` rule — it overshot by 0.0063 on
the ER row and fell 0.0076 short on the degree row before this was fixed. **The
connectome row is exact either way**, because it is one fixed graph, so the row a reader
checks first is the one row that cannot reveal the problem. `eig_w_real` is stored
normalised, so median-scaling puts the largest bar exactly on the rule by construction.
See `report/act1_structure.md` §5 for the residual this does *not* remove.

**Each row is binned over exactly `[-lambda_1, +lambda_1]`, and the builder asserts it.**
A shared bin grid leaves the bar *containing* the extreme eigenvalue overhanging the
`lambda_1` rule by whatever fraction of a bin width the grid happens to impose — measured
at 91% and 93% on the weight-permuted and degree rows, and on the negative side too for
ER. Binning each row over its own `[-lambda_1, +lambda_1]` makes the histogram's support
exactly the shaded gap, since `lambda_1` is the largest modulus. Bin *count* varies per
row so bin *width* stays constant to ~0.3%. **Both this and the median-scaling defect
above were invisible on the connectome row**, which is the row a reader checks first;
assume shared-grid histograms drawn against per-series reference lines are wrong until
measured from the rendered artists.

**F1, F2 — the spectra are stored normalised, and one column is mis-named.**
`perron_root` is 1.0 in every row (the spectrum is stored with `|lambda_1|` divided out),
and `bulk95_radius` is the **ratio**, not a radius, despite the name. The absolute bulk
radius is `bulk95 * lambda_max_raw`, and `|lambda_1|` is `lambda_max_raw`. Computing an
"absolute bulk" from `bulk95_radius` returns the ratio and gives a 47.3% spread where
`TIER0` §3.1 reports 4.4%.

**F2 — "holds at both N" needs qualifying.** Promoted to `TIER0` §3.1 on 15 August
2026, which is now the canonical home; this entry points at it. The 4.4% absolute-bulk
spread is an **N=448** number; at N=1000 it is **6.4%** (or 6.9% under the other
aggregation — §3.1 states both). The gap-ratio separation does hold at both
(3.985 against 2.30-2.44), but the *null ordering* reverses between scales (`TIER0` §2.1),
so the caption must state the scale for the spread and must not carry the null ordering
across.

**F3 — REDUCED TO ONE PANEL, 15 August 2026 (session 1).** The draft's F8 had been merged
in as a second panel (relative s.d. of `|lambda_1|` across seeds). It is now cut. The two
panels argued **different things**: panel (a) argues *neither axis is neutral*, which
follows geometrically from F1/F2's finding that the substrates differ in only one
quantity; the merged-in panel argued *the normaliser is itself unstable*, a related but
separate criticism. Two arguments in one figure read as two half-figures. Panel (a) makes
contribution 5's claim on its own, so **F8's content is now methods prose** with its
numbers inline (`report/act1_structure.md`, claim A1.7), and F3 has no panel letters.

**The numbers the prose must carry, so cutting the panel does not lose them.** All
recomputed in `act1_structure.md` §5, on the non-negative substrate:

* `|lambda_1|` relative s.d. across seeds — connectome **0** (one fixed graph, nothing
  resampled); weight-permuted **0.0628** at N=448, 0.0385 at N=1000; degree 0.0885 /
  0.0908; ER 0.0867 / 0.1285. The permuted control freezes the weight draw, so its
  residual is the **placement** contribution alone.
* Largest sampled weight — relative s.d. **0** under permutation (identical multiset every
  seed), **0.119** at N=448 and 0.167 at N=1000 for the resampling nulls, taking only
  **2 distinct values across 10 seeds** at N=448 (3 at N=1000), and correlating **+0.854
  to +0.949** with `|lambda_1|`.
* **Do not write** "`|lambda_1|` is an extreme-value statistic with Hill alpha ~2.3": E0.4
  §5 attributes the Hill index (2.49 at N=448 -> 2.28 at N=1000) to the **empirical weight
  pool**, not to `|lambda_1|`. And `TIER0` §1.1 is explicit that the simulated operator's
  spectral radius is **exactly sigma for every variant**, so the nominal axis is *not*
  noisy in sigma. Defensible wording: *the normaliser is a single non-concentrating order
  statistic, so what nominal matching equalises rests on one sampled weight, and the bulk
  radius each seed actually realises inherits the spread.*
* **Do not write** "the permuted-multiset control has relative s.d. exactly 0" without
  saying of what. It is exactly 0 for the largest sampled **weight**, and 0.0628 for
  `|lambda_1|`. An earlier version of this entry conflated the two.

**F3 — (a) and (b) are NOT expected to subtract to (c).** `dD_median` is the median over
seeds of the **per-seed difference**; `d_eff_connectome` and `d_eff_erdos_renyi` are the
medians of each substrate **separately**, and the median of differences is not the
difference of medians. They part by up to **9.4** on the nominal axis and **8.3** on the
matched one; at the peak, +343.3 against +338.1. (c) keeps the paired per-seed statistic
because that is the correct one for a paired comparison and is what `TIER0` §2.2
publishes; **the caption states the discrepancy** rather than hiding it. Do not "fix" it
by redrawing (c) as the difference of medians — that would abandon the published numbers.

**F3 — the `d_eff = N` ceiling is load-bearing, not decoration.** ER runs along it (peak
0.997 of N = 448, against the connectome's 0.965), so the connectome "advantage" in (c)
is largely how far below ceiling the connectome sits and where. `CONVENTIONS` requires
the ceiling on every memory figure; here it is also the reason panels (a) and (b) earn
their space.

**F3 — the one cross-act figure.** The data is E0.2's, but the figure sits in chapter 3
and Session 1 owns contribution 5. **Session 1 renders it; Session 3 must not re-render
it**, and Session 3's E0.2 reproduction gate is what validates it.

**F4, F5 — RESOLVED 15 Aug 2026: Act II now has a `TIER0` section.** Probe 2 and Probe 3
were promoted into **`TIER0` §3.12**, with every number recomputed from the frozen
parquets at promotion. Both captions are now written against `TIER0` like every other
figure. Two constraints come with it:

* **F5 states the *swap*, not the capture.** On the all-positive substrate neither basis
  captures much at k = 10 (0.04 to 0.17), so "the manifold lives in graph harmonics"
  overstates it. The claim is which basis wins. The low capture is consistent with
  supercritical `d_eff` ~413 of 448 on that substrate, and where `d_eff` is low the
  capture is high (gaussian NARMA, 0.886) — the two probes agree without being fitted
  to each other, which is worth a caption sentence.
* **F5 is confirmatory, not novel.** Sign-gating of the manifold transition is largely
  pre-empted by Krauss 2019 (roadmap, "what must NOT be claimed").

**F4, F5 — Probe 2 is a two-variant, four-sigma capture.** `manifold_alignment.parquet`
holds `connectome` and `degree_rewire` only, at four spectral radii. Neither figure can
show the four-variant ladder, and neither should imply it.

**F6 — the statistic is a correlation with measured MC, not with rung index.** Over the
seven rungs, `spearman(d_eff, mc) = +1.000` and `spearman(pr, mc) = +0.107`; pooled
within-regime, `+0.9982` against `+0.308`. Correlating against the rung *index* gives
-0.18 and +0.54 and is not the claim. `alpha == 1e-6` is the only alpha this file carries
at `spectral_radius >= 3.05`.

**F9 — the supercritical threshold is the connectome's, applied to everyone.** With
`sigma >= sr_crit` per variant the margins are 3.56 and 3.85; with `sigma >=` the
connectome's `sr_crit` they are **4.40 and 4.42**, which is `TIER0` §2.4. Same data,
different filter, and only one of them is the published number.

**F14 — two aggregation units, do not read them against each other.** CV 0.209 is per
(variant, f) with under-half-transitioning cells dropped (n = 37, `TIER0` §3.10). The
seed-level unit (n = 378, §3.11) gives `sigma_eff` 0.304 against the exact Jacobian's
0.152. `TIER0` §3.11 says this explicitly: *do not read 0.209 against 0.152.* The panel
shows the §3.10 comparison; if the Jacobian is added it needs its own axis and its own n.

**F14 — no line at 1.** The unit crossing is withdrawn. Draw the 0.77-0.90 band.

**F16 — the coverage mask is the point, not decoration.** Promoted to `TIER0` §2.3 on
15 August 2026, which is now the canonical home; this entry points at it. Recomputed from
the frozen boundaries, the matched-bulk axis has **six** crossings, not one: x = 2.943,
3.525, 3.598, 3.670, 3.743 and 4.361.

**The two coordinates are the same object, and the figure quotes the published one.**
(2.938, 0.153) is the value of record; the 2.943 above is a coarse linear interpolation on
the union of the two boundaries' grids, not a competing estimate, and the 0.005 gap is
that interpolation. `CONVENTIONS` mandates quoting the coordinate exactly, so **the caption
quotes (2.938, 0.153)** and the builder marks the crossing it finds without relabelling
it. Only the first lies inside the all-replicates coverage edge
(minimum `x_hi` = 3.58); the rest are the noisy region TIER0 §6.10 says is "drawn but
should not be read quantitatively", where the boundary rests on a `bulk95`-selected
subsample and oscillates. **So the published crossing is the first and only one inside
coverage, and the figure must make that visible.** Quoted as a bare coordinate it looks
like a clean feature; hatch the uncovered region and it becomes an honest one. The nominal
axis needs no mask — every nominal cell carries all 30 replicates (§2.3).

**F16 — the three contour-level conventions reproduce §2.3 exactly.** On the effective
axis `f_star` and `f_star_level_on_subrange` both give the crossing;
`f_star_level_raw_max` — the level set by a cell backed by 1 replicate of 30 — gives
**none**, which is precisely what §2.3 reports. Use `f_star`. The other two columns are
the robustness check, not alternatives to plot.

**F16 — the published nominal crossing cannot be drawn from this file.** All three
conventions give no nominal crossing on the extended sweep, which is the claim. But the
(sigma = 4.392, f = 0.1309) point that reproduces the published value requires re-running
the boundary operator on the sigma <= 6 **sub-panel**, which is a different computation
from pinning the level to a subrange. Annotate it as a quoted TIER0 number or leave it to
the caption; do not imply it came from these curves.

**F16 — the boundaries have gaps.** `f_star` is NaN where no contour exists (the
generative boundary is defined at 84 of 121 effective-axis points and 46 of 121 nominal).
Break the line at the gaps; never interpolate across them.

**F16 — ownership.** Chapter 6, contribution 2, the unifying section. It needs both arms,
so **Session 4 renders it** (it has Session 3's memory arm already validated). Like F3, it
is a cross-act figure and only one session may own it.

**F15 — no frozen parquet, and one soft assumption.** The leading eigenvector is not
persisted anywhere, so this figure recomputes it. It also assumes the release node
ordering matches the consensus ordering; the loader documents that as verified by
node-strength and edge-weight correspondence at **r >= 0.98**, which is an agreement, not
an identity. State it in the caption. (Recomputed here: Perron root 0.188862, matching
`lambda_max_raw` to six decimals, so the substrate is the right one.)

**Repo contradiction — FIXED IN `TIER0`, not pending.** `TIER0` §2.1's `bulk95`
columns held per-seed **means** beside `1/median` `sr_crit` values, at both scales. They
were corrected to medians on 15 August 2026 (commit `861984e`) and §2.1 carries a dated
note listing the withdrawn values. **Nothing here instructs `TIER0`** — this entry records
where the fix landed, because a rank-4 document may not carry a correction a rank-1 one has
not absorbed.

---

## Claim-to-primary-task mapping

Declared before any data is inspected, so that "there is always a task where it holds"
cannot be said. **Confirmed in session 0, unchanged from the draft**, with two additions.

| claim | primary | corroborating |
|---|---|---|
| memory capacity, ladder ordering, decay-rate advantage | **MC** | NARMA-10, **Mackey-Glass** |
| closed-loop generation, regime switch, resistance margin | **Lorenz** | **none** |
| the two capacities are one axis read with opposite sign | **MC + Lorenz jointly** | **none — no out-of-sample test** |
| readout dimensionality vs PR | **MC** | NARMA-10 |
| the spectral decomposition (contributions 1 and 5) | **no task** — structural | — |

NARMA-10 also carries the **bridge paragraph**: it sits between pure memory and pure
prediction, and one paragraph showing the trade-off varies continuously across
MC -> NARMA -> Lorenz strengthens Act III at almost no cost.

**Addition 1 — the structural claims are task-free.** Contributions 1 and 5 are
properties of `W` and of the matching axis. No task can corroborate or refute them, and
none should be cited as if it could.

**Addition 2 — MG moved to the memory side, and contribution 2 lost its out-of-sample
test.** Resolved 15 August 2026. The implemented MG task is **teacher-forced**, so the
reservoir is re-anchored by the true input every step and the regime switch has no
consequence for the metric. It therefore probes memory and nonlinear expressivity, and
corroborates **MC**, not Lorenz. The original pre-registration — an interior optimum in
`f`, testing contribution 2 — is **withdrawn on design grounds before any data was
inspected**, and is preserved verbatim in `PREREG_MACKEY_GLASS.md` §1.1 with the reason.
A narrower prediction the driven design can carry is registered in its place.

**Consequence to state in the discussion, not to paper over: contribution 2 has no
out-of-sample test in this thesis.** It rests on F16 plus the joint reading of F7 and
F13. Closed-loop MG is deferred work, not a gap that MG's presence in the task list
quietly fills.

---

## Inline manifold measures for NARMA and MG

Gram spectra give `d_eff` at any alpha forever **wherever they are persisted**. Curvature
and PR cannot be recovered afterwards. Decided here:

- [x] `mean_curvature` on NARMA driven states
- [x] `mean_curvature` on MG driven states  (**needed for the MG pre-registration test**)
- [x] `participation_ratio` on both
- [x] `mean_gain` / `sigma_eff` on both

**All four ticked. The marginal cost is zero.**
`experiments/human/analysis/phase_diagram/capture.py:capture_cell` already computes
`mean_curvature`, `pr`, `mean_gain`, `mean_state`, `frac_saturated` and
`effective_radius` for **every task in the task list**, from states it has already
captured. Adding a task to the list gets all six; there is nothing to switch on and no
reason to economise.

**But the premise behind this section is currently false, and that raises the stakes.**
`capture_cell` computes the Gram spectrum, reduces it to `d_eff`, and **discards the
array** — so on the f x sigma grid `d_eff` is *not* recoverable at another alpha either.
Persisting it is a storage change, not a compute change (the eigendecomposition already
runs). See the session-0 report, Task 5.

**One measure is deliberately not ticked: `d_eff` on MG.** It is not a decision that can
be reversed by re-running, it is free once the Gram spectrum is persisted, and it should
be read off the spectrum rather than computed inline against a hard-coded alpha.

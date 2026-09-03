# Master figure list

**Fixed in session 0, 15 August 2026. Count 18.** No session creates a figure that is
not here; if one seems missing, report and stop. `W` marks the workshop subset (5pp, 4
figures).

> **AMENDED 2 September 2026 (Act II). Count 18 to 19, for F20.** The reason, stated as
> the 19 August amendment requires. Chapter 5 opened on its first **result**. The object
> the chapter measures — a `T_eff x N` state matrix, and the split of `A^T A` into a
> fluctuation term and a rank-one time-average term — reached the reader as prose and
> equation 5.1 and was drawn nowhere, so the thing being measured existed only as
> notation while every measurement of it had a figure. F20 draws it: the real drive, the
> recorded state matrix, three units followed from a trace into a trajectory, and
> equation 5.1 as three matrices.
>
> **It carries no contribution and makes no claim**, which is F19's position. No null
> substrate appears, no comparison is made between substrates or among the three units,
> and the caption says in terms that three units on one cell support no claim about which
> units do what. The one number it quotes — the rank-one term carries **51.3%** of the
> trace — is a property of the single cell it draws, quoted so the reader can see the
> split has two comparable halves. **Whether substrates differ in that share is section
> 5.2's finding (A2.1, A2.2, F4), and the figure is built so it cannot pre-empt it**: (b)
> and (c) share one vertical scale, (d)'s two sub-panels share one box, and (e) is on one
> shared scale with no inset, so no panel makes either term look larger than it is.
>
> **It is the one figure in the sweep that re-runs a reservoir.** Working rule 5 forbids
> persisting state matrices, so a figure drawing one has to regenerate it through the
> evaluators' opt-in `collect_states` path — 0.3 s, writing nothing.
> `report/act2_manifold.md` §2.7 is the reproduction gate that licenses it, and a cheaper
> form of it runs on every build. **The figure was specified, gated and STOPPED once**,
> on 2 September, because its first caption could not be written against the cell
> (`act2_manifold.md` audit item 21, kept in the record); this row is the rebuilt figure
> under the rewritten caption.
>
> **A colour namespace was added for it, and that is not a palette amendment.**
> `style.UNIT_COLOURS` (`#3333BB`, `#779955`, `#886699`) colours individual *units*,
> which are not substrates. `VARIANT_COLOUR` and `src/experiment/plots._VARIANT_STYLE`
> are untouched and every other figure re-renders unchanged. See `CONVENTIONS.md`'s
> style contract for the measured separations and the four floors
> `style.check_colour_consistency()` now asserts.

> **AMENDED 1 September 2026 (Act I). Count 17 to 18, for F19.** The reason, stated as
> the 19 August amendment requires. Chapter 4's **first** section sets out the substrate
> and the null ladder and had only a preservation table to do it with: the chapter
> described four graphs in prose and drew none of them, so a reader met the
> weight-permuted control as a sentence rather than as a picture of the connectome's own
> graph with its weights reordered. F19 draws all four as matrices under one node
> ordering, with the four binary-graph statistics beneath.
>
> **It carries no contribution and makes no claim.** It prints in the section
> `report/act1_structure.md` §4 registers as carrying **no results**, and its statistics
> strip is a set of design facts about four graphs, not a measurement. That is also why
> it quotes no spectral quantity: the gap belongs to the sections after it.
>
> **Its sources did not exist and were built for it.** No frozen parquet in the
> repository held adjacency, so `report/artifacts/build_substrate_graphs.py` was written
> and committed to freeze one. It verifies the edge count and the degree sequence, then
> runs a reproduction gate (connectome against control: byte-identical binary adjacency,
> **exact** equality on all four statistics) **before** it writes anything. The numbers
> are promoted into `TIER0` §3.13, which is their canonical home. **No run happened and
> none was needed.**

> **AMENDED 24 August 2026 (floor-sensitivity session). Count 16 to 17, for F18.** The
> reason, stated as the 19 August amendment requires. `CROSS_ACT_SPINE.md` sets out the
> thesis as a six-step chain, and **step 3 is the Gram spectrum's position relative to
> the ridge floor**: the link between Act II's common-mode account and the `d_eff` that
> Act III's memory arm reads. It was the one step in the chain with no figure, because
> the result sits in `TIER0` §3.6 filed under a **rejected** anisotropy hypothesis and
> had never been drawn. Chapter 5's outline commits to a section on it, so the chapter
> would otherwise have argued its central link in prose alone.
>
> **Verified before it was built, not after.** `report/checks/floor_sensitivity_check.md`
> recomputed all sixteen published cells of §3.6's supercritical table from the frozen
> artifacts (every one reproduces), established that `covariance_spectra.parquet` already
> carries the four-variant, sigma-resolved coverage a figure needs (a complete 3 tasks x
> 3 conditions x 7 variants x 13 spectral radii x 10 seeds factorial with `eig_gram` in
> every one of 8,190 rows), and recorded the verdict as "a standalone figure is buildable
> from frozen data alone". **No run happened and none was needed.**
>
> **It is Act II's own claim, so it lives in `act2_manifold.py`, but session 2 closed on
> 17 August.** This session owns and renders it, and is named as its owner in the module
> table below, which is the F3 and F16 arrangement rather than a new one.

> **AMENDED 19 August 2026 (session 4), on the author's decision. The cap is now a soft
> count, not a gate.** The rule this list carried was "one slot, first past the post":
> E1 and E2 (roadmap §4d) competed for a single cap slot, E2 resolved first, and E1 was
> to be dropped with the reason recorded. That rule is replaced by **build both, then
> place each on what it turns out to show**. The cap no longer decides whether work
> happens; it records how many main-text figures exist, and a session that adds one must
> still edit this file and `figures/__init__.py` together and say why.
>
> **What that produced.** E2 became **F17** in the main text: the free-running rollout is
> a measurement no other artifact in the repository holds, it carries a pre-registered
> claim, and it *refuted* half of that claim — evidence, not illustration. E1 became
> **S2**, supplementary: it makes no claim the main text does not already make.
> Count 15 → 16 main-text figures, plus a second S-figure. The amendment is recorded in
> `report/act3b_prediction.md` §6.

**The cap was 14 and was raised to 15 in session 0, deliberately and once.** The draft
list gave contribution 2 — the unifying claim, and the crossing it turns on — no figure
of its own, on the reasoning that F7 and F13 carry it jointly. They do not: F7 is memory
against `sigma·bulk95` at f = 0 and F13 is VPT against f at sigma = 2, two orthogonal 1-D
slices, and no pair of slices shows that the two advantage regions occupy *opposite
regions of the (f, sigma) plane*. F16 was added for that. ~~The cap is 15 now; it is not
a precedent, and a session that wants a sixteenth reports and stops.~~ **Superseded by
the 19 August amendment above**: the sixteenth was wanted, was argued for, and was added
— by editing this file and the registry together, which is the part of the old rule that
survived. The paragraph is kept struck through rather than deleted, because the reasoning
in its first half (why two 1-D slices cannot carry contribution 2) is still live.

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
| `act1_structure.py` | 1 | F1, F2, **F3**, **F19**, S1, **S3**, **S4** |
| `act2_manifold.py` | 2, the **floor-sensitivity session (24 Aug) for F18**, the **F20 session (2 Sep)** | F4, F5, F6, **F18**, **F20** |
| `act3_memory.py` | 3 | F7, F9, F10, F11 |
| `act3_prediction.py` | 4 | F12, F13, F14, **F16**, F17, **S2** |
| `act4_anchor.py` | — | F15 |

**The act decides the module, not the chapter**, and the two cross-act figures are why
that matters: F3 prints in chapter 3 but is Act I's argument and Session 1 renders it;
F16 prints in chapter 6 but needs both Act III arms, so Session 4 renders it. **F18 is
the third case and it is a different one**: it prints in chapter 5 *and* is Act II's
argument, so the module is not in question, but Act II's session had already closed when
the check that licenses it cleared. The rule that survives both cases is the same one:
the module follows the act, and whoever renders a figure is named here. The per-figure
ownership flags below remain canonical.

**Cut made:** the draft's F3 and F8 both served contribution 5 and were merged into one
two-panel F3 in chapter 3 where contribution 5 lives. **F8 is retired and its ID left
unused** rather than renumbering, so references elsewhere still resolve. **Session 1 then
cut the merged-in panel too** (see the F3 flag): the two panels argued different things
and read as two half-figures, so F3 is now a single panel and F8's content is methods
prose. The ID count is unchanged — F8 stays retired either way. **F16 added** for
contribution 2. **F17 added** in session 4 for E2. **F18 added** on 24 August for the
chain's step 3. **F19 added** on 1 September for chapter 4's opening section. **F20
added** on 2 September for chapter 5's opening section. Rendered
figures: F1 to F7, F9 to F20 = 19. IDs are stable identifiers,
not a reading order, so F16 and F17 sitting in chapter 6 after chapter 7's F15 is
intended, and so is F18 returning to chapter 5 after both. **F8 stays retired**: the next
free number was taken rather than the retired one reused, so every reference to F8
elsewhere still resolves to "merged into F3".

Status: `confirmed` = source verified and filter reproduces `TIER0`; `confirmed*` = source
verified, see the flag below the table.

| id | ch | contr. | claim it carries | source, columns, filter | status | W |
|----|----|--------|------------------|-------------------------|--------|---|
| F1 | 4 | 1 | The spectrum is one large real Perron eigenvalue separated from a bulk that is essentially the nulls' bulk | `eigenspectrum/results/scale_448/spectra_per_seed.parquet`; `eig_w_real` (448 floats/row), `bulk95`, `lambda_max_raw`; filter `condition == "human_empirical"` and `variant in LADDER` (40 rows) | confirmed* | W |
| F2 | 4 | 1 | The difference is a **gap**, not a bulk: absolute bulk near-identical (4.4% spread at N=448), gap ratio 3.078 vs 1.81-1.92 | same file at `scale_448` **and** `scale_1000`; `abs_bulk = median(bulk95) * median(lambda_max_raw)`, `gap_ratio = 1/median(bulk95)` | confirmed* | W |
| F3 | 3 | 5 | **Neither axis is neutral.** (a) connectome and ER on nominal sigma, (b) the same two on `sigma·bulk95`, (c) the deltas: +343.3 at nominal 4.47 / -217.4, against +196.5 at 1.949 / -24.0 | `criticality_matched/results/e02_panel.parquet` filter `interp == "linear"`, cols `x, axis, d_eff_connectome, d_eff_erdos_renyi, dD_median, dD_q25, dD_q75`; plus `e02_axis_summary.csv` (2 rows) | confirmed* | |
| F4 | 5 | (Act II) | The Perron mode is a common mode: it carries the mean, and after time-centring the dominant W-eigenmodes carry ~0 of the fluctuation variance | `results/scale_448/manifold_alignment.parquet` filter `condition == "human_empirical"`, `variant == "connectome"`, `task == "mc"`, supercritical operating point; plus `saturation_diagnostics.parquet` `mean_state` | confirmed* | |
| F5 | 5 | (Act II) | Sign selects the basis: balanced -> W-eigenmodes, all-positive -> low-frequency graph harmonics | `manifold_alignment.parquet`; one panel per `condition`, curves over `basis in {harmonics, wmodes, random}`, `task == "lorenz"` | confirmed* | |
| F6 | 5 | 6 | PR misses readout-relevant structure: against measured MC across the seven rungs, `d_eff` orders at **+1.000** and PR at **+0.107**; pooled within-regime +0.998 against +0.308 | **(b, c)** `results/scale_448/probe3_deff.parquet`; filter `task == "mc"`, `condition == "human_empirical"`, `spectral_radius >= 3.05`, `alpha == 1e-6` (350 rows, 7 variants). **(a)** `results/scale_448/covariance_spectra.parquet`, same task/condition, `variant == "connectome"`, `spectral_radius == 3.0526`, then the ONE seed whose `d_eff` is nearest the median of the ten; cols `eig_cov, eig_gram, alpha` (448 rows, one per direction) | confirmed | |
| F7 | 6 | 3 | **The crossing**: the connectome peaks lowest (432.4) yet retains most (47% at the top of the overlap, against 28/22/11%, `TIER0` §1.2); `d_eff` decay on the matched axis, ceiling drawn | `criticality_matched/results/taskB_extended_sweep_scale_448.parquet`; `variant, seed, spectral_radius, bulk95, d_eff`; no row filter (f = 0, MC, 4 variants, sigma 0 to 8 step 0.4, 10 seeds); `x = spectral_radius * bulk95` from the file's own column, **per seed**, then interpolated onto the common grid and medianed across seeds (see the F7 flag) | confirmed* | W |
| ~~F8~~ | | | **RETIRED — merged into F3.** Do not render. | | retired | |
| F9 | 6 | 3 | The supercritical margin holds across a 2.2x change in N: **4.40 -> 4.42** on the connectome's `sr_crit` applied to all, **3.56 -> 3.85** on each variant's own. Both panels, per `TIER0` §2.4 | `n1000_memory_scale_448.parquet` + `n1000_memory_scale_1000.parquet`; supercritical = `spectral_radius >= 3.078` (N=448) / `>= 3.985` (N=1000), i.e. **the connectome's `sr_crit`, applied to every variant** | confirmed* | |
| F10 | 6 | 3 | Peak parity, not deficit: paired per-seed differences with CIs across the alpha grid; 2-6%, reliable against ER and weight-permuted, **not** against degree-matching | `criticality_matched/results/closeout_peak_parity.csv`; 15 rows = 5 alpha x 3 contrasts, cols `mean_diff, ci_lo, ci_hi, wilcoxon_p` | confirmed | |
| F11 | 6 | 3 | Rescue from Perron domination: `\|mean_state\|` 0.759 against the nulls' 0.949-0.989 at sigma = 6, f = 0; and matching on `sigma·bulk95` absorbs only **26%** of the f = 0 gap | (a) `item2_f_extension_scale_448.parquet` + `item3_f_extension_nulls_scale_448.parquet`, filter `task == "mc"`, `spectral_radius == 6.0`, col `mean_state` by `f`. (b) `e03_mechanism_matched_scale_448.csv` cols `median_abs_gap_matched_x` vs `..._sigma` (6.42 -> 4.75 at f = 0) | confirmed | |
| F12 | 6 | 4 | Curvature is **bimodal**: 215 of 38,280 cells (0.56%) lie in [0.6, 2.2] rad; a binary collapsed-or-not bit explains R2 = 0.364 against continuous curvature's 0.371 | `criticality_matched/results/e01_jacobian_scale_448.parquet`; cols `mean_curvature, vpt`; no row filter (38,280 Lorenz cells = 4 variants x 11 f x 29 sigma x 10 seeds x 3 draws) | confirmed | W |
| F13 | 6 | 4 | Generation read as VPT: +1.0 to +2.2 Lyapunov times from f ~ 0.20 at sigma = 2, clearing the weight-permuted placement control; **plus the f = 0 collapse panel** (ER 5/10 seeds, connectome 0/10) | (a) `e03_frontier_scale_448.parquet` filter `metric == "vpt"`, `spectral_radius == 2.0`. (b) `e03_frontier_paired_scale_448.csv` same filter — paired within seed, so all connectome-minus-null statements come from here. (c) `item2_collapse_loci_scale_448.csv` filter `f == 0`, cols `n_seeds_collapsed / n_seeds` | confirmed | |
| F14 | 6 | 4 | `sigma_eff` is a **locator, not a criterion**: transition at 0.77-0.90 with variant offsets ordered by spectral gap; CV 0.209 against nominal sigma's 0.667 | `e01_threshold_invariance_scale_448.csv` filter **`scope == "f > 0"`** (n = 37); plus `e01_threshold_table_scale_448.csv` cols `effective_radius_lo/hi` per (variant, f) | confirmed* | |
| F15 | 7 | anchor | Which Yeo networks load the Perron mode (minimal Act IV) | **computed live, no frozen parquet**: leading eigenvector of the N=448 self-built consensus (`eigh`) x release RSN labels from `data/human/Suarez2021_Data`, restricted to cortical nodes. Seconds, not a run | confirmed* | |
| F17 | 6 | 4 | **The free-running rollout, which no other artifact captures.** Every persisted state matrix is teacher-forced. Pre-stated claim: the connectome retains the true climate to higher `f` (**confirmed**: 0.43 of frozen cells against the nulls' 0.14 at `f` >= 0.30) and the collapse is a change of shape not of scale (**refuted**: `sd_ratio` is bimodal, 229 of 440 cells at a fixed point against 158 keeping the spread, 11 between) | `criticality_matched/results/e2_free_run_scale_448.parquet` (source `free_run`), 440 rows = 4 variants x 11 `f` x 10 seeds at sigma = 2, cols `climate_error, sd_ratio, trajectory`; **panel (d) reads the frozen `e01_jacobian_scale_448.parquet` instead**, which carries 30 cells per (variant, `f`) against this capture's 10 | confirmed* | |
| F16 | 6 | **2** | **The crossing, with its axis and its coverage.** The memory and generative boundaries on both axes: on `sigma·bulk95` they cross at (2.938, 0.153) inside full replicate coverage; on nominal sigma they do not cross at all once the sweep passes sigma = 6 | `e02_heatmap_boundaries_extension.csv` + `..._extension_nominal.csv` concatenated with an `axis` column; `panel == "dD"` is the memory boundary and `"dStraight"` the generative one; use `f_star` (level over fully covered cells). Coverage mask from `e02_heatmap_coverage_extension.csv` (`x_hi` per f, minimum 3.58) | confirmed* | |
| F18 | 5 | (Act II) | **The Gram spectrum against the ridge floor**, the chain's step 3. Supercritically the connectome holds **89.0%** of its directions more than a decade clear of the floor against Erdős–Rényi's **11.4%** (`d_eff` 412.9 against 74.8); floor sensitivity is strongly sigma-dependent and each substrate's **interior** dip sits at a different sigma (connectome 3.58, every null 1.58 or 2.00), which is where each one's measured ridge optimum migrates to as alpha rises | **(a, b)** `results/scale_448/covariance_spectra.parquet` (source `floor_mass`); filter `task == "mc"`, `condition == "human_empirical"`, `variant in LADDER`, **no sigma filter at load** (520 rows = 4 variants x 13 spectral radii x 10 seeds); cols `eig_gram`, `alpha`, reduced per cell to `d_eff, floor_sensitivity, n_within_decade, n_below_floor, frac_below_floor` plus the four position bins. Exact zeros STRIPPED first, alpha from the file's own column. Panel (a) then cuts to `spectral_radius >= 3.05` (50 cells per variant). **(c)** `criticality_matched/results/taskB_extended_sweep_scale_448.parquet` (source `alpha_peaks`); argmax over sigma of the seed-median `mc_alpha_*` column, 20 rows = 5 alpha x 4 variants | confirmed* | |
| F20 | 5 | (none) | **From a driven network to a Gram spectrum.** The object chapter 5 measures, drawn: the real white-noise drive, the recorded state matrix `A`, three units followed from a trace to a trajectory, and equation 5.1 as three matrices. **Carries no claim, deliberately; it defines the object chapter 5 measures.** It prints first, in the chapter's opening section; no null substrate appears and no comparison is made, between substrates or among the three units. The one number it quotes — the rank-one term carries **51.3%** of `trace(A^T A)` on this cell — is that cell's, and whether substrates differ in it is §5.2's claim (A2.2, F4), which the panel scales are built not to pre-empt | **The only figure in the sweep that re-runs a reservoir**: states are never persisted (working rule 5), so the cell is regenerated through the evaluators' opt-in `collect_states` path. The cell identity is not re-derived — it is source `gram_spectra`'s, i.e. F6a's cell (connectome, `task == "mc"`, `condition == "human_empirical"`, sigma = 3.0526, alpha = 1e-6, the seed whose `d_eff` is nearest the median of the ten, resolving to **seed 7**). The graph and the three units come from `report/artifacts/substrate_edges.parquet` (source `substrate_edges`) filtered to `variant == "connectome"`, node strength at the 10th/50th/90th percentiles giving nodes **119, 346, 262**; node ordering from source `substrate_order`, the same as F19's. Gate: `act2_manifold.md` §2.7 | confirmed* | |
| F19 | 4 | (none) | **The four substrates, as graphs.** The ladder drawn rather than described: binary and weighted adjacency under one node ordering, with the degree marginal above each column, plus one diagonal block magnified on the same colour scale. **Carries no claim**: it prints in chapter 4's no-results opening section. Connectome and weight-permuted control are one binary graph, which is the gate that the placement control is a placement control | `report/artifacts/substrate_edges.parquet` (source `substrate_edges`), 117,106 rows = 22 (variant, seed) cells x 5,323 edges, cols `variant, seed, i, j, weight`, no row filter. Node ordering from source `substrate_order`, **computed live**. The four binary-graph statistics are **not drawn here**: they are `substrate_topology.parquet` (source `substrate_topology`, 22 rows) rendered as chapter 4's `tab:act1-topology` | confirmed* | |

Contributions 1 to 6 are the roadmap §1 list. F1/F2 carry 1, **F16 carries 2**, F7/F9/F10/F11
carry 3, F12/F13/F14/**F17** carry 4, F3 carries 5, F6 carries 6.
**F19 and F20 carry none of the six, and neither carries a claim at all.** Each opens
its own chapter's first section by drawing what that chapter is about — F19 the four
substrates, F20 the driven state matrix and its Gram split — and each prints in a
section its act file registers as carrying no results.
**F18 carries none of the six, deliberately.** It is `CROSS_ACT_SPINE.md`'s step 3, the
measured link from weak common-mode domination to usable dimensionality, and it is the
mechanism *behind* contribution 6 rather than a seventh claim. `TIER0` §3.6 files it under a
**rejected** anisotropy hypothesis, and the rejection stands: what F18 draws is the refit at
the correct end of the spectrum, not the hypothesis that refit replaced. Contribution 2's *out-of-sample*
test remains the Mackey-Glass pre-registration rather than a panel; F16 carries the claim
itself.

---

## Supplementary figures — appendix, outside the cap

**Added 15 August 2026 (session 1), at the author's request.** These are **not** part of
the numbered main-text list and do **not** consume a main-text slot: `FIGURES` in
`report/figlib/figures/__init__.py` holds exactly **17** and still carries the
assertion that records the count. S-figures live in a separate `SUPPLEMENTARY`
registry, and `python -m report.figlib` renders both. The rule that no figure exists
outside this file still binds, which is why they are listed here.

> **Count corrected 25 August 2026.** This paragraph read "still holds exactly 15 and
> still carries the assertion that **enforces** it", which was true when it was written
> and is a present-tense claim, so it is corrected outright rather than annotated. The
> registry has since gone 15 to 16 (19 August, F17) and 16 to 17 (24 August, F18), and
> `report/figlib/figures/__init__.py` now reads
> `assert len(FIGURES) == 17, f"registry holds {len(FIGURES)} figures, not 17"`,
> **verified by reading it on 25 August 2026; the file was not edited.** [It reads **18**
> since 1 September 2026, when F19 was added; the sentence is left as the record of what
> was read on 25 August, and the S-figure separation it is about is unaffected.] "Enforces"
> also became wrong on 19 August, when the cap became a soft count: the assertion
> records the number rather than gating it, which is what the amendment at the head of
> this file says. The S-figure separation is unaffected, which is the point the
> paragraph was making.

> **AMENDED 1 September 2026 (Act I), for S4.** An appendix figure, outside the cap and
> outside `FIGURES`, so the count of 18 is untouched. Appendix
> section `app:wider-ladder` carries the three off-ladder substrates as a table of
> numbers and the chapter draws only the ladder's four, so the two rungs that hold the
> most of the connectome's topology appear nowhere as pictures. S4 is F19 widened from
> four substrates to the full family of seven, in the column order of the methods
> chapter's preservation table.
>
> **It clears the bar because it makes no claim at all**, which is F19's position too.
> It compares nothing among the seven, quotes no spectral quantity, and carries no
> statistics strip: the four binary-graph statistics stay the ladder's in
> `tab:act1-topology`, and the three additional rungs' spectra stay in
> `tab:act1-offladder`. `TIER0` §3.1(b)'s scope guard on those three rungs holds over
> this figure. `substrate_topology.parquet` and `TIER0` §3.13 are unchanged.
>
> **Its source is a new file rather than a widened one.** F19 takes its columns from
> `edges.variant.unique()`, so three extra variants in `substrate_edges.parquet` would
> have turned a four-column figure into a seven-column one with no error raised.
> `build_substrate_graphs.py` gained a second output,
> `substrate_edges_full.parquet`, and asserts the four ladder variants come through it
> unchanged; `substrate_edges.parquet` is byte-identical after the extension and F19
> re-renders byte-identical. **No run happened and none was needed.**

**The bar for an S-figure, so this does not become a way around the count:** it makes
**no claim the main text does not already make**.

> **AMENDED 19 August 2026 (session 4).** The bar used to carry a second clause — "and
> it is built by an **existing builder at different parameters**" — and S2 fails it: E1
> needs its own builder. The clause is dropped, because it was a *proxy* for the test
> that matters and it excluded exactly the case a supplementary figure is most useful
> for: supplying intuition for a claim the main text asserts but cannot illustrate. S1
> (a scale replicate) satisfied both clauses and made the proxy look free; S2 is the
> case that shows it was not. **"No claim the main text does not already make" is now
> the whole bar**, and it is the clause doing the work — a figure that makes a new claim
> is a main-text figure and goes in the numbered list, whoever built it.

| id | main-text twin | what it adds | source, columns, filter | status |
|----|----|----|----|----|
| S1 | F1 | F1 rebuilt at **N = 1000**. Same builder, same claim, larger parcellation; shows the gap-ratio separation surviving a 2.2x change in N, and makes the null-ordering reversal visible | `eigenspectrum/results/scale_1000/spectra_per_seed.parquet` (source `spectra_1000`); `eig_w_real` (1000 floats/row), `bulk95`, `lambda_max_raw`; filter `condition == "human_empirical"` and `variant in LADDER` (40 rows) | confirmed |
| S2 | F12 | **E1 — the two curvature regimes made visible. Prints in chapter 5**, built in `act3_prediction.py` (session 4 owns it; the act decides the module, as for F3 and F16). Unit traces either side of one substrate's transition plus the per-step turning-angle distributions — the temporal intuition Act II hands over as a boundary rather than a result (`act2_manifold.md` §5 item 15). Makes **no** claim F12 does not | `criticality_matched/results/e1_curvature_regimes_scale_448.parquet` (source `curvature_regimes`); 2 rows, cols `regime, spectral_radius, mean_curvature, turning_angles, unit_traces`; connectome, `f` = 0.25, one seed, two sigma one grid step apart | confirmed* |
| S3 | none | **The pre-registered placement-mechanism test, drawn where it fails. Prints in the appendix**, at `width=\textwidth`; built in `act1_structure.py` (session 1 owns it, and it is Act I's own measurement). Mean edge weight against the endpoint degree product, connectome and weight-permuted control, in the twenty equal-count bins `TIER0` §3.14(b) publishes the rank correlation of. `PREREG_PLACEMENT_MECHANISM.md` registered a **positive** correlation in the connectome before it was measured; the connectome's is **negative** and the control's covers zero, so the weighted rich club is refuted as an account of the gap on this substrate. Makes **no** claim the register does not already make: the prereg's verdict was EQUIVOCAL, A1.5 is unchanged and still carries no mechanism | `report/artifacts/placement_mechanism_degree_weight.parquet` (source `placement_degree_weight`), 40 rows = 2 substrates x 20 bins, cols `variant, bin_index, bin_lower, bin_upper, n_edges, median_degree_product, mean_weight, sem_weight`; plus `..._rank_correlation.parquet` (source `placement_rank_correlation`), 2 rows, for the two rho and their bootstrap intervals. No row filter on either; N = 448, `condition == "human_empirical"`, one seed per substrate | confirmed |

| S4 | F19 | **The full substrate family, as graphs. Prints in the appendix**, full page and rotated a quarter turn, at `width=\textheight`; built in `act1_structure.py` (session 1 owns it, and it is Act I's own figure). F19 widened from the ladder's four substrates to all seven, in the column order of the methods chapter's full preservation table (`tab:methods-preservation`), most preserved first. Two rows by seven columns: binary adjacency with the degree marginal above each panel, then weighted adjacency, all seven on one logarithmic colour scale under one colour bar. Same node ordering as F19, same community boundaries, same representative-seed rule, so the four columns the two figures share are the same four matrices. **No zoom row**: F19's magnified block is chosen from the connectome's partition and carries an argument about the control, and neither transfers to a figure that compares nothing. Makes **no** claim, as F19 makes none: no comparison among the seven, no spectral quantity quoted, no statistics strip | `report/artifacts/substrate_edges_full.parquet` (source `substrate_edges_full`), 276,572 rows = 52 (variant, seed) cells x the columns `variant, seed, i, j, weight`; plus `substrate_order` for the node ordering and `spectra_448_full` (70 rows) for the seed rule and nothing else. No row filter on any of the three; N = 448, `condition == "human_empirical"` | confirmed |

**S1 — the row ordering is NOT monotone at N=1000, and the caption must not imply it
is.** Rows a-d are in ladder order, and at N=448 that happens to coincide with descending
gap ratio (3.08, 1.92, 1.87, 1.81), which is why F1's caption can say "rises from 1.81 to
3.08". At N=1000 the same rows read **3.99, 2.39, 2.30, 2.44** — the ER row's gap ratio
exceeds the degree row's, because the null ordering by `bulk95` reverses between scales
(`TIER0` §2.1). The connectome's ~1.7x separation from every null holds at both. Quote
the separation, never the sweep down the column.

**S3, one panel: the other two of the three-panel sketch are deliberately not built.** The masking curve was posed as a fraction of each cell's own `|lambda_1|`, which divides by the one quantity the substrates differ in and is **not interpretable as posed** (`TIER0` §3.14(d)); no number from it is published anywhere. The strength sandwich would give a figure to the account `TIER0` §3.14(c) records as **untested**, which is the post-hoc move the registration exists to prevent. Neither omission is a layout problem and neither is to be revisited: the prereg's §3 fixes one session and no second analysis.

**S3, two intervals in one figure, and they must not be confused.** The shaded band around each line is ±1 standard error of that bin mean, named on the y-axis; the bracketed pairs in the legend, and the "95% percentile intervals" the caption quotes, are the **bootstrap** intervals on the two Spearman correlations, over 10,000 resamples of the 5,323 edges. The x-axis is logarithmic because the bins are equal-count on a heavy-tailed product; the rank correlation is invariant to that.

**S3, both series are drawn solid, and that is deliberate.** The style contract's dash for `connectome_weight_permuted` is overridden here and **only** here: two dashed, capped series crossing each other twenty times read as a thicket, and the panel is about a trend. **No colour is varied**, so the substrate encoding is the thesis-wide one, and the contract's redundancy is carried by marker shape (circle against square) plus the luminance gap between black and vermillion, which survives greyscale and all three dichromacies. Axis titles and the legend sit one point below the contract's sizes, at `AXIS_LABEL_SIZE - 1` and `LEGEND_SIZE - 1`: this legend carries two correlations and their intervals, which is more text than any other legend in the sweep, and one point keeps it to three rows. Both are written relative to the contract constants, not as literals, so they follow any change to it. The panel is built at 7.4 x 3.4 in and placed at `\textwidth`, which on this class (`hscale=0.77` on A4, so `\textwidth` = 6.37 in) prints at 0.86 scale, the same scale factor F1, F2 and F19 print at.

**S3, what the panel may not be read as saying.** It carries a negative result and nothing else. It licenses **no mechanism claim**, no derivation of `|lambda_1|` from a structural statistic, no sufficiency claim and no task claim, and it says nothing about the absolute bulk: this concerns `|lambda_1|` only.

**S4 draws seven substrates and does not widen the ladder.** `TIER0` §3.1(b) puts
`random_gaussian`, `clustering_rewire` and `modularity_rewire` on the record and guards
their scope, and the guard holds over this figure. It makes no comparison among the
seven, quotes no spectral quantity, and recomputes nothing across the wider set.
`substrate_topology.parquet` and `TIER0` §3.13 hold the four binary-graph statistics of
the four-substrate ladder and are **not** extended: the ladder's statistics stay in
`tab:act1-topology`, the three additional rungs' spectra stay in `tab:act1-offladder`,
and S4 carries no statistics strip of its own.

**S4, the column order is the preservation table's, so the ladder is not contiguous.**
Columns run connectome, weight-permuted, clustering rewire, modularity rewire, degree
rewire, Erdős–Rényi, random gaussian, which reproduces `tab:methods-preservation` row for
row. The criticality-matched ladder is therefore columns **one, two, five and six**, and
the caption names them by number. Calling them the four leftmost would be wrong under
this ordering, and preservation order is worth more here than contiguity because what
each substrate keeps is the figure's whole subject.

**S4, all seven substrates are non-negative, and a draft of this figure assumed
otherwise.** At `condition == "human_empirical"` every randomised graph, rung 0
included, takes its weights by drawing with replacement from the connectome's own weight
pool, so no substrate in the family carries a signed weight; the build script and the
figure both assert it rather than assuming it. A first draft of the caption put
`random_gaussian` on a diverging scale of its own on the belief that its weights were
signed, which is false at this condition, and which `TIER0` §3.1(b) contradicts anyway by
publishing a Perron-based quantity for that rung. All seven weighted panels are therefore
on **one** logarithmic scale under one colour bar. Chapter 3's ladder prose and
`app:wider-ladder` carried the same belief and are being corrected by hand, outside this
session.

**S4, rung 0 is the one substrate whose edge count is not 5,323.** `random_gaussian`
draws each pair independently at the connectome's density, so it matches the density in
expectation rather than the count and its count is Binomial: the ten seeds run 5,180 to
5,439 against an expectation of 5,323 and a binomial standard deviation of 71.0. The
exact-count assertion both the artifact and the figure carry is **exempted for that
variant alone**, replaced by a five standard deviation band, and the ten per-seed counts
are printed by the build so the variation is on the record. `clustering_rewire` and
`modularity_rewire` are exact and are asserted exactly.

**S4 is the one figure in the sweep printed at `\textheight`, and both the canvas and
the type sizes follow from that.** It is placed full page and rotated a quarter turn, so
its printed width is `\textheight` (676.04 pt, 9.35 in) rather than `\textwidth`
(6.37 in). Two consequences, both handled in the builder rather than by scaling the
include. **The canvas is drawn at the printed width**, so the figure prints at scale 1.0
and its 300 dpi raster is 300 dpi on the page; a 7.6 in canvas magnified to `\textheight`
would fall to 244 dpi, which is the wrong direction for seven columns of 448 x 448
matrices. **Every type size is then set at `TYPE_SCALE` = `\textwidth` / 7.6 in = 0.84
times the contract's size**, because the contract's sizes are a statement about the
printed page: a 9pt label in a figure reduced to 0.84 prints at 7.5pt, and the same label
in a figure printed at 1.0 would print at 9pt, larger than that label anywhere else in
the thesis. The factor puts S4's printed type exactly where F1's, F2's and F19's is.
Every size is written relative to a contract constant and none as a literal, so they
follow any change to the contract; this is S3's arrangement, which sets two sizes one
point below the contract with the reason stated, at a different factor and for a
different reason. **The contract's fixed sizes are not being relaxed** and nothing here
licenses a second figure setting its own type: the deviation exists only because the
placement is unique, and it is calculated from the placement rather than chosen.

**S4, the panel labels are placed by measurement, not by eye.** Fourteen labels in
seven columns sit in the inter-column and inter-row gaps, and at F19's spacing the gaps
are narrower than the letters, so each one lands on the panel above or to its left.
`hspace`, `wspace` and the label offset are set together so that every letter's box
clears every panel by at least 2.5 pt, the tightest being the 'm', whose glyph is the
widest of the fourteen. The clearances were read off the drawn figure.

**S4 reads a source of its own, and that is why F19 is safe.** F19 takes its columns from
`edges.variant.unique()`, so adding the three rungs to `substrate_edges.parquet` would
have widened a four-column figure to seven with no error raised.
`build_substrate_graphs.py` writes a second file instead,
`substrate_edges_full.parquet`, and asserts the four ladder variants come through the
concatenation unchanged. Verified on the extension: `substrate_edges.parquet` and
`substrate_topology.parquet` are byte-identical before and after, and F1, S1, S3 and F19
all re-render byte-identical.

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

**F3 — 0.997 / 0.965 is this panel's pair, and `TIER0` §3.2 has a different one. Added
25 August 2026.** `TIER0` §3.2 reports peak `d_eff/N` as **≥0.993 for every null and
0.961 for the connectome**, at α = 1e-6 over the taskA α sweep, per-variant peak over
σ. The 0.997 / 0.965 above is read off **this figure's own source**,
`e02_panel.parquet`, as per-substrate medians over seeds on the nominal axis. Different
source, different filter, **neither is wrong**, and neither is edited. **The thesis
quotes `TIER0`'s pair**; 0.997 / 0.965 appears only in F3's caption, where its filter is
stated, and must not be carried into body prose as though it were the published value.

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
-0.18 and -0.54 and is not the claim (published as +0.54; the sign was corrected in
session 2 against `probe3_deff.parquet`, and `TIER0` §3.12 carries the note). `alpha == 1e-6` is the only alpha this file carries
at `spectral_radius >= 3.05`.

**F7 — `bulk95` is per seed, so the aggregation order is part of the filter. Added 17
August 2026 (session 3).** For the connectome `bulk95` is one number (one fixed graph);
for the three resampling nulls it is a **per-seed** extreme-value statistic, spreading
0.41 to 0.61 across ten degree-rewire seeds. So on the matched axis each seed sits on
its own `x` grid, and E0.2 aggregates **per seed then across seeds** throughout
(`E02_verdict` §4.4, which states the reason). `TIER0` §1.2's crossing table is that
statistic and reproduces to all published digits under it.

Medianing `d_eff` at fixed nominal σ and calling `σ · median(bulk95)` the x coordinate
is a *different* statistic — it collapses ten x values into one — and the session-0
builder did exactly that. Measured, it moves the published peak **locations** by up to
0.15 on x (degree 0.91 → 0.85, ER 0.97 → 1.11), the peaks by up to 1.3 `d_eff`, and the
retained fractions by a point (ER 11% → 12%). **The connectome row is unaffected**,
because its `bulk95` is a constant — so the row a reader checks first is again the one
row that cannot reveal the problem (Act I item 13, Act II item 1, now here).

**F9 — the supercritical threshold is the connectome's, applied to everyone.** With
`sigma >= sr_crit` per variant the margins are 3.56 and 3.85; with `sigma >=` the
connectome's `sr_crit` they are **4.40 and 4.42**, which is `TIER0` §2.4. Same data,
different filter, and only one of them is the published number. **Session 3 draws both
panels**, because §2.4 says to report both and the two say different things: on the
connectome's threshold the margin is flat (+0.5%), on each variant's own it grows ~8%.

**F7, F9, F10, F11 — the real null-model names, matching F1 to F6. Changed 17 August
2026 (session 3), on the author's review.** Act III's builders were on `VARIANT_LABEL` /
`VARIANT_TICK` (the rung numbering) while chapters 3 to 5 use `VARIANT_TITLE` /
`VARIANT_TITLE_TICK`, so three substrates were named one way in chapter 5 and another in
chapter 6. All four figures now use the plain names. The names are wider than the
one-unit category spacing, so F7's and F9's bar/dot axes **rotate their tick labels 30°**
rather than shrink them, and F9's panel-(a) legend became a **two-column crossed legend**
(substrate by colour, scale by dash) because four "Connectome, N = 448" entries are wider
than the panel. `VARIANT_TICK` and `VARIANT_LABEL` remain in `style.py`: this is a
per-figure choice, as it already was for F1 and F4b, not an amendment to the contract.
**`act3_prediction.py` (F12 to F14, F16) has not been changed** — it is session 4's.

**F11 — `|.|` before the median, not after, and the builder asserts it.** `mean_state`
is signed with a sign set by the input realisation. Under median-then-abs the σ = 6,
`f` = 0 column reads connectome **0.638** and weight-permuted **0.575**, i.e. the null
below the connectome — the panel would argue against its own caption and against
`TIER0` §3.7. Under abs-then-median it returns §3.7's published 0.759 / 0.949 / 0.959 /
0.989 exactly. This is the same defect Act II found in F4b (`report/act2_manifold.md`
audit item 1) and it was present in session 0's F11 builder too; both builders now
assert the connectome is lowest, so it fails the build rather than the reader.

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

**F18 - the zero-strip is undocumented in `TIER0` and load-bearing.**
`criticality_matched/closeout.py:floor_mass`, which produced §3.6's table, drops exact
zeros (`g = g[g > 0]`) before every one of the four statistics. `TIER0` §3.6 does not say
so, and without that step the **fraction below alpha reproduces for no variant**: the
connectome's published 6.6% reads 7.03% and Erdős–Rényi's 79.4% reads 83.59%, because the
number of numerically rank-deficient directions grows down the ladder (median 1.0 against
91.5). The other three statistics are untouched, since a zero contributes 0 to `d_eff` and
0 to the sensitivity and is never within a decade of alpha; only the fraction has a
denominator to move. The strip lives in `sources.py:_floor_statistics` with the reason
beside it. **`TIER0` §3.6 now names it**: amendment (a) of 24 August 2026 puts the strip,
the four full-denominator values and the per-variant zero counts into the rank-1 document,
so this flag is the figure-side pointer to it rather than an outstanding request.

**F18 - the dips in panel (b) are INTERIOR minima and the caption must never drop the
word.** Floor sensitivity vanishes at **both** ends of the spectrum, because each term
`g*alpha/(g+alpha)^2` peaks at 1/4 when `g == alpha` and falls away in either direction.
So a substrate whose spectrum is far above the floor and one whose spectrum has already
fallen far below it both read low, and every variant's curve goes to zero at sigma = 0
where the reservoir is dead. On the median curve the connectome's **global** minimum over
non-zero sigma is at **0.42** (2.687), below its interior dip at 3.58 (5.785). Read as a
global minimum, §3.6's claim does not reproduce for the connectome; read as the interior
dip, it reproduces exactly and in 8 of 10 seeds. **Panel (b) therefore draws the whole
curve including sigma = 0 and shades the low-sigma limb** rather than cropping the axis,
and the builder asserts both that each variant's sigma = 0 value is below its own dip and
that the connectome's first non-zero point is too.

**F18 - do not write that raising alpha costs Erdős–Rényi little.** Its floor sensitivity
(10.26) is the second lowest on the ladder for a **degenerate** reason: 20.4% of its
directions are exactly zero and a further 52.8% sit more than a decade below the floor, so
73.2% of its spectrum is stripped before the floor is raised at all and only about 75 of
448 directions survive. Per unit of surviving dimensionality it is the **most** sensitive
substrate on the ladder, losing **29.1%** of its `d_eff` per decade of alpha against the
connectome's **5.6%**. The stock is nearly exhausted; the rate is the highest here. A
sentence conflating the two errs in the direction that flatters the connectome.

**F18 - panels (a, b) and panel (c) are on two different sigma grids, and the caption says
so.** (a) and (b) come from the probe capture's 13-point grid (0 to 6); (c) comes from
Task B's 21-point grid (0 to 8, step 0.4). **3.5789 and 3.6 are two grids' nearest points
to the same place, not the same number**, and neither are 1.5789 and 1.6. Panel (c)'s
correspondence is **consistent-with, not fitted**: nothing regresses the optimum on the
sensitivity curve or bounds a residual, which is `TIER0` §3.6's own wording and this
figure does not improve on it. Two of the four land one grid step off their own dip, and
the caption names them rather than rounding the claim up.

**F18 - the three nulls coincide exactly in panel (c), so the markers nest.** Their
ridge-optimal sigma is identical at every alpha (1.2, then 1.6 at all four higher alpha),
so their curves superimpose and the panel would appear to draw two substrates rather than
four. The marker shrinks down the legend order so the coincident points read as
concentric rings. **Nothing is offset**: an offset would draw a disagreement the data does
not contain. Weight-permuted's and Erdős–Rényi's dotted dip rules coincide at 2.00 for the
same reason.

**F18 - ownership.** Chapter 5, Act II's own claim, `act2_manifold.py`. Session 2 owns
that module and closed on 17 August, so the **floor-sensitivity session of 24 August
renders F18** and is named here, per the module table above. Session 2's three figures
were not touched: a full `--all` re-render moved only F18, verified with `git status`
rather than assumed.

**F19 - its two sources are the only frozen artifact in the sweep that holds
adjacency, and this figure is why they exist.** Every other source is a reduction:
eigenvalues, task scores, Gram spectra. Nothing held the edges, so
`report/artifacts/build_substrate_graphs.py` was written and committed to freeze them,
and the numbers were promoted into `TIER0` §3.13. The parquets are gitignored, as every
parquet in this repository is; **the script is the committed object** and re-running it
reproduces both files.

**F19 - the zoom row magnifies a diagonal BLOCK, not a community, and the rule is
stated.** Of the diagonal blocks of the drawn ordering (hemisphere x community), the one
with the highest within-block binary edge density among blocks of 15 to 40 nodes: at
N = 448 that is hemisphere 1, community 5, 22 nodes, 125 internal edges, density 0.5411.
`TIER0` 3.13 carries the rule, the chosen block and every candidate in the range. **An
earlier community-level rule was withdrawn for non-contiguity**: hemisphere is the outer
key, so a community spanning both hemispheres occupies two non-contiguous diagonal
blocks, and the indicator on (e-h) would have to mark two squares and the rectangle
between them. `_densest_block` raises rather than widening the size range if no block
falls in it.

**F19 - the zoom panels are on the SAME colour scale as (e-h), and must stay there.**
Rescaling them to their own range would make (i) against (j) a comparison of two
different scales and say nothing. The builder asserts that (i) and (j) fill the same
cells before it renders, which is the block-level form of the connectome/control gate.

**F19 - the statistics moved out of the figure on 1 September 2026 and into
`tab:act1-topology`.** They were drawn as a four-row strip beneath the columns; four rows
of numbers under four matrices read as a fifth band of the figure rather than as a table,
and a table is what they are. **`substrate_topology.parquet` and `TIER0` 3.13 did not
change** and remain their source and their canonical home. The chapter table is filled
from 3.13 to four decimal places, the precision 3.13 publishes and the precision chapter
4's other topology tables already use.

**F19 - the reproduction gate lives in the builder script and is restated in the
figure.** Connectome against weight-permuted control: byte-identical binary adjacency,
then **exact equality** on all four statistics, to equality and not to a tolerance. It
runs before either parquet is written. The figure asserts the adjacency half again, so a
figure that has come apart from its artifact fails the build rather than drawing panels
(a) and (b) as two subtly different images when they are supposed to be one.

**F19 - all four statistics are BINARY-graph statistics, and the modularity uses a FIXED
partition.** Louvain on the binary connectome, resolution 1.0, seed 0, detected **once**
and applied unchanged to every variant. Do not re-detect per variant: that fits whatever
partition best suits each draw and reports a respectable modularity for a graph with no
community structure at all. `TIER0` §3.13 carries the method, the resolution and the six
community sizes.

**F19 - the node ordering is computed live, and carries F15's standing caveat.** Source
`substrate_order` is one of the two live sources (the other is `perron_yeo`): neither the
Louvain partition nor the release hemisphere labels are persisted anywhere. It costs one
substrate load and no run. The hemisphere labels come from the release geometry, so the
assumption F15 states applies here too, that the release node ordering matches the
consensus ordering. **Here it decides only the order rows and columns are drawn in**, so
nothing rests on it, which is why the figure states the ordering in its caption rather
than a hemisphere identity.

**F19 - it carries no contribution, and must not acquire one.** It prints in chapter 4's
opening section, which `report/act1_structure.md` §4 registers as carrying no results.
It quotes no spectral quantity, no gap ratio and no task: the gap is F1's and F2's, and
no task appears in Act I at all. Its statistics strip is a set of design facts about four
graphs.

**F19 - the seed is F1's, and that is the point.** The two randomised variants are drawn
at the seed whose `bulk95` is nearest the median, which is the seed F1's panels a-d draw
(degree 1, Erdős–Rényi 2). The rule lives once in
`act1_structure._representative_row`, which both builders call, so a reader setting the
two figures side by side sees the same two matrices and the two cannot drift apart.

**F15 — no frozen parquet, and one soft assumption.** The leading eigenvector is not
persisted anywhere, so this figure recomputes it. It also assumes the release node
ordering matches the consensus ordering; the loader documents that as verified by
node-strength and edge-weight correspondence at **r >= 0.98**, which is an agreement, not
an identity. State it in the caption. (Recomputed here: Perron root 0.188862, matching
`lambda_max_raw` to six decimals, so the substrate is the right one.)

**F20 — it re-runs a reservoir, and that is why it has a gate.** Every other figure in
the sweep reads a frozen parquet. F20 draws the state matrix itself, which working rule 5
forbids persisting (10 to 44 MB per cell), so the cell is regenerated through the
evaluators' opt-in `collect_states` path on every build: 0.3 s, nothing written, no cache.
`report/act2_manifold.md` §2.7 is the reproduction gate — eigenvalues of `A^T A` from the
re-run against the frozen `eig_gram`, worst relative deviation **3.4e-07** over the 438
directions above the ridge floor, with `mc`, `mean_state` and the design shape reproducing
alongside — and the builder re-asserts a one-scalar form of it (`d_eff` from the re-run
against the frozen spectrum, to 1e-3) so a drifted re-run fails the build.

**F20 — the cell is F6a's cell and is never re-derived.** The builder takes the seed,
sigma and alpha from source `gram_spectra`, which already applies the rule, rather than
re-implementing "the seed whose `d_eff` is nearest the median of the ten". Two figures
captioned as drawing the same cell must not each own a copy of the rule. It asserts the
resolution is **seed 7** and that the strength percentiles still return **119, 346, 262**,
because §2.7 and the caption name those and a silent change would leave both wrong.

**F20 — the panel scales are correctness constraints, not layout.** Three of them.
**(b) and (c) share one vertical scale**, and it is the activity's own bound: `leak_rate`
is 1.0, so a state is exactly `tanh(.)` and lies in (-1, 1). On a shared scale centring is
visibly a *shift* — each trace slides to zero keeping its shape — which is all (c) claims.
**(d)'s two sub-panels share that same box**, so the raw and centred clouds are comparable
and neither is zoomed. **(e) is symmetric-logarithmic**, and this one changed the answer:
on a *linear* shared scale the rank-one term reads as strong structure and the fluctuation
term as a near-blank wash, because the first is an outer product and heavy-tailed (median
|entry| 83, 99th percentile 2088) while the second is comparatively even (median 435, 99th
percentile 618). That picture says the fixed pattern dominates the activity — which is
**§5.2's question, not this figure's**, and is false of the quantity the caption quotes,
since the two terms carry 51.3% and 48.7% of the trace. The bound `|entry| <= T_eff`
(from `|x| < 1` and Cauchy-Schwarz) is asserted, so the shared scale clips nothing.

**F20 — no dimensionality is stated anywhere on it, and the drawn text is checked.**
The figure counts nothing: no `d_eff`, no rank, no direction count, and none of
"low-dimensional", "subspace", "sheet", "plane", "surface". Where a word for the
eigenvalues of `A^T A` is needed it is **Gram spectrum**, in full, and it appears in the
caption rather than on a panel. Sigma = 3.05 is never labelled critical or near-critical.

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

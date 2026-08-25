# GAPS: what the fact sheets could not source, and where the documents disagree

> **Updated 25 August 2026, after the author's decisions.** Five recorded disagreements
> are now **RESOLVED** (B2, B3, B10, B11, B12), one section A row is resolved, and one
> housekeeping item (the four-orders phrasing) was found **already discharged** and
> needed no edit. Resolved items are kept in place with what was decided and where it
> landed, not deleted, so the audit can see the reasoning. Everything still marked open
> is open.

**Written for the numeral audit.** Three sections: (A) numbers an outline commits to
stating that no document contains; (B) places where `TIER0_STATE_OF_PLAY.md`,
`report/FIGURE_LIST.md`, an act file and `report/checks/floor_sensitivity_check.md`
disagree, with both values and **no attempt to resolve them**; (C) every row across the
thirteen sheets whose only source is an act file, `FIGURE_LIST` or the check file, so the
audit knows which numerals it **cannot check against TIER0**.

Source key: **T0** = `TIER0_STATE_OF_PLAY.md`. **FL** = `report/FIGURE_LIST.md`.
**A1** = `report/act1_structure.md`. **A2** = `report/act2_manifold.md`.
**CHK** = `report/checks/floor_sensitivity_check.md`. **CONV** = `report/CONVENTIONS.md`.
**SPINE** = `report/CROSS_ACT_SPINE.md`.

---

## A. Numbers the outlines commit to that are in no document

Nothing below was reconstructed, computed from neighbouring values, or omitted silently.

| what is missing | which section commits to it | where I looked |
|---|---|---|
| **Per-variant `\|lambda_1\|` (`lambda_max_raw`) at N = 1000.** T0 §3.1's table of `bulk95`, `abs(lambda_1)` and absolute bulk exists **only at N = 448**; at N = 1000 only the two spreads (6.4% / 6.9%) and the gap ratios are published | chapter 4 outline item 6, "Scale", and F2 panel (b), which draws `\|lambda_1\|` at both scales | T0 §2.1, §3.1, §2.4, §2.5; A1 §2.1 to §2.5; FL F2 and S1 rows and flags; A1's F2 and S1 caption blocks |
| **Per-variant absolute bulk values at N = 1000** (the four numbers behind the 6.4% spread), the counterpart of 0.0614 / 0.0599 / 0.0595 / 0.0587 at N = 448 | as above, and F2 panel (a) | as above |
| **How the N = 448 consensus was built**: subject count, dMRI processing, consensus rule, edge count and density at N = 448. Only "self-built consensus", "N = 448", "cortical nodes", "release RSN labels from `data/human/Suarez2021_Data`" and node-ordering agreement at **r >= 0.98** appear. The **N = 1000** edge count (10,784 undirected edges) is stated in A1 §5 item 3; the N = 448 figure is nowhere | chapter 4 outline **item 2**, "The substrate and the null ladder" | T0 §0 to §6 in full; A1 in full; FL F1, F2, F15 rows and flags; SPINE; A2 |
| **What `erdos_renyi` preserves.** The rung is named in CONV's style contract and used throughout, but no document in this set states its construction (matched density? matched edge count? matched weight pool?) | chapter 4 outline item 2, "the four rungs and what each holds fixed" | T0 (all); A1 (all, including §2.6's null-generation audit); FL; CONV; A2 |
| **What `clustering_rewire` and `modularity_rewire` preserve.** Named in CONV's style contract and in A2 §2.2's per-rung table, never defined | chapter 5 outline item 5, which quotes the seven-rung range | T0 §3.12; A2 §2.2; FL F6 row and flag; CONV |
| **The weight-permuted row of the anisotropy table.** T0 §3.6's rejected-hypothesis table gives PR, decay exponent and top-mode fraction for **connectome, degree and Erdős–Rényi only**; weight-permuted is absent | chapter 5 outline item **4.6**, "the anisotropy retraction", which is stated of the ladder | T0 §3.6 in full; CHK (which does not recompute the anisotropy table at all); A2 §4 item 4.6; FL F18 row and flags |
| ~~**The four position bins ... in a rank-1 document.**~~ **RESOLVED 25 August 2026.** The full four-variant by four-bin table is now **T0 §3.6 amendment (e)**, sourced to CHK §5.1, with the two required qualifiers carried beside it: the bins partition each individual cell exactly while the four per-bin medians are not constrained to sum to 100 (connectome **102.1%**), and the zero-strip of amendment (a) applies. T0 §3.6 now has **five** amendments | chapter 5 outline item **4.1** | as before; promoted into T0 |
| **The sigma-resolved floor-sensitivity curve.** T0 §3.6 states that sensitivity is strongly sigma-dependent and gives the minima, but the 13-point per-variant curve F18b draws exists **only in CHK §3.1**. **Deliberately left there on 25 August 2026**: it is figure data, not a published result, and the author's decision on the position table excluded it by name | chapter 5 outline item **4.4**, and F18 panel (b) | T0 §3.6 in full; FL F18 row and flags; A2 F18 block |
| **The five per-alpha migration rows.** T0 §3.6 and §3.3 publish only the endpoints (2.4 to 3.6; 1.2 to 1.6). The five-by-four table F18c draws exists **only in CHK §3.3**. **Deliberately left there on 25 August 2026**, on the same grounds as the row above | chapter 5 outline item **4.5**, and F18 panel (c) | T0 §3.3, §3.6; FL F18 row and flags; A2 §4 item 4.5 |
| ~~**A figure reference that no longer exists.**~~ **RESOLVED 25 August 2026.** A1 §4 item 1.3 read "The normaliser's own noise **(F3b)**"; it now reads "in prose, no panel", with a dated note recording that the panel was cut on 15 August 2026 and that the pointer was **worse than dead**, since F3's current panel (b) exists and shows the `sigma*bulk95` axis. The numbers survive in A1 §5 items 6 and 7 and in FL's F3 flag | chapter 3 outline item 1.3 | as before; corrected in place |

---

## B. Disagreements between documents, both values given, unresolved

### B1. The task prompt against TIER0 (recorded because a number has drifted in conversation)

| what the prompt says | what the document says | where |
|---|---|---|
| "section 3.6's **three** amendments of 24 August" | T0 §3.6 carries **four** dated amendments of 24 August 2026: **(a)** the zero-strip and the full-448 fractions, **(b)** interior minima and the withdrawal of 1.8 to 3.9, **(c)** ER's degeneracy as level against rate, **(d)** "four orders" corrected to **five** | T0 §3.6 |

Amendment (d) is the one a three-amendment reading would drop, and it changes wording a
row must carry: the alpha grid spans **five orders of magnitude in four steps**. It is
carried on sheet 09 §4.5.

**Updated 25 August 2026: there are now five.** Amendment **(e)** promotes the
four-variant by four-bin position table into §3.6 (Decision 2 below). Anything counting
§3.6's amendments after this date counts five.

### B2. Peak `d_eff/N`, connectome and Erdős–Rényi, at N = 448: **RESOLVED 25 August 2026**

| document | value |
|---|---|
| T0 §3.2 | connectome **0.961**; every null **>= 0.993**, at alpha = 1e-6 |
| FL, F3 flag, and A1 §3's F3 block | connectome **0.965**; Erdős–Rényi **0.997 of N = 448** |

Both are N = 448 peak `d_eff/N` and are quoted in the same argument (the ceiling is
load-bearing). They come from different sources and filters (T0's taskA alpha sweep,
per-variant peak over sigma at alpha = 1e-6, against the E0.2 panel's per-substrate
medians over seeds on the nominal axis).

**Resolved by cross-note, not by change. Neither value is wrong and neither was
edited.** T0 §3.2 now carries a dated cross-note naming 0.997 / 0.965 and its filter;
FL's F3 flag and A1's F3 block each carry the reciprocal note naming T0's pair and its
filter. **The thesis quotes T0's pair**, and 0.997 / 0.965 appears only inside F3's own
caption where its filter is stated, never in body prose. Sheet 00 now carries the two as
**separate rows**, T0's marked as the pair body prose uses.

### B3. The Jensen bias of 0.087: **RESOLVED 25 August 2026**

| document | claim |
|---|---|
| CONV, numerical conventions, and T0 §1.3 | "the per-seed mean of `1/bulk95` is biased upward by up to **0.087** at N=1000", stated in the ladder's context |
| A1 §5 item 4 | 0.0868 reproduces exactly, but for **`random_gaussian` at N=1000**, a rung **outside the four-rung ladder**. Within the ladder the mean-against-mean gap tops out at **0.0431** (ER, N=1000); against the **median** the ladder maximum is **0.0727** and the sign is **negative** for all three N=1000 nulls |

A1 says `common.SR_CRIT_CONVENTION`'s own source comment names `random_gaussian` and that
CONV drops it.

**Resolved in favour of the ladder value, in both documents.** T0 §1.3's paragraph now
reads **0.0431** within the four-rung ladder (Erdős–Rényi, N=1000) and carries a dated
**amendment (a) of 25 August 2026** recording that 0.087 is right but is
`random_gaussian`'s (**0.0868**), a rung outside the ladder, so the larger number stays
traceable rather than disappearing. The amendment also carries the second looseness A1
found: against the **median** the ladder maximum is **0.0727** and the sign is
**negative** for all three N=1000 nulls, so "biased upward" is mean-against-mean, not
mean-against-median. `report/CONVENTIONS.md`'s numerical-conventions bullet was
corrected the same day with the source named. **The convention itself does not change:
median, not mean.** Sheet 00 now carries 0.0431 as the row and 0.0868 as a second row
attributed to `random_gaussian`.

### B4. The curvature "between band" share on Lorenz

| document | value |
|---|---|
| T0 §3.10, and FL's F12 row | **0.56%**, 215 of **38,280** Lorenz cells in [0.6, 2.2] rad, on the Jacobian capture |
| A2 §1 and §5 item 15 | **0.82%** of **12,180** Lorenz cells, on this act's own Probe 1 capture |

A2 states this is a **different population, not a disagreement** (a 58-sigma grid against
E0.1's Jacobian capture). Recorded so a numeral audit does not read the pair as one number
stated twice. Carried on sheet 12 with both.

### B5. The flat Lorenz curvature value at `f` = 0

| document | value |
|---|---|
| T0 §3.11 | **0.26** at sigma = 2, 4, 6, 8 and 11.2 for the connectome; **0.26 / 0.26 / 0.26 / 0.27 / 1.70** for Erdős–Rényi |
| A2 §1 and §5 item 15 | seed-median **0.261** (connectome) and **0.263** (Erdős–Rényi) across sigma = 0 to 6, maximum 0.26 for both |

Two captures, two sigma grids, two precisions, and A2's Erdős–Rényi value does not extend
to the sigma = 11.2 point where T0's reads 1.70. Carried on sheet 12 as two rows.

### B6. Modes within a decade of alpha

| document | value |
|---|---|
| T0 §3.6 | **36 / 84 / 82 / 48** |
| CHK §1.2 | **36.0 / 83.5 / 82.0 / 47.5**; T0's 84 and 48 are 83.5 and 47.5 **rounded half-up**, because the median of 50 integer counts lands on a half |

CHK calls it a display convention rather than a disagreement, and says a figure drawing
these counts should plot the halves and let the caption carry the integers, or state which
it is doing. Carried on sheet 09 §4.3.

### B7. `\|lambda_1\|` correlation with the largest sampled weight

| document | value |
|---|---|
| A1 A1.7 | "**+0.85 to +0.95**" |
| FL, F3 flag | "**+0.854 to +0.949**" |
| A1 §5 item 7 | **+0.854** (degree) and **+0.939** (ER) at N=448; **+0.949** and **+0.906** at N=1000 |

The four measured values are inside both bands and the bands differ only in rounding.
Recorded because three documents state three forms and a numeral audit will see three.
Carried on sheet 00.

### B8. Largest sampled weight, relative s.d.

| document | value |
|---|---|
| FL, F3 flag | **0.119** at N=448, **0.167** at N=1000 |
| A1 §5 item 7 | **0.118992** at N=448, **0.167018** at N=1000 |

Rounding only. Recorded for completeness. Carried on sheet 00.

### B9. Absolute-bulk spread at N = 448 under the two aggregations

| document | value |
|---|---|
| T0 §3.1 | **4.4%** under the product of medians and **"identical" 4.4%** under the median of per-seed products |
| A1 §2.2 | **4.426%** and **4.447%** respectively |

Identical at the published 1 d.p.; not identical at three. Carried on sheet 03.

### B10. Whether FIGURE_LIST's F2 row states the aggregation the builder uses: **RESOLVED 25 August 2026**

| document | state |
|---|---|
| A1 §5 item 5 | "`FIGURE_LIST`'s F2 row specifies the median-of-products form and is now inconsistent with the builder. **The row should be updated to `median(bulk95) x median(lambda_max_raw)`**" |
| FL, F2 row, as it currently reads | `abs_bulk = median(bulk95) * median(lambda_max_raw)` |

**Verified by reading FL's F2 row on 25 August 2026: the change has landed.** The source
cell reads `abs_bulk = median(bulk95) * median(lambda_max_raw)`, the product-of-medians
form A1 §5 item 5 asked for and the one the builder and T0 §3.1's table both use. **This
was housekeeping, not a live defect**, and nothing was edited to make it so. A1 §5 item
5 is now **marked resolved in place** with the date and the verification, rather than
deleted, because the reasoning in its first half (why panel c is not panel b over panel
a unless both are on the product of medians, and the 0.055 gap at N=1000 that shows it)
is still why the row has to read that way.

### B11. The supplementary-figure bar: **RESOLVED 25 August 2026**

| document | the bar |
|---|---|
| FL, 19 August 2026 amendment | **one clause**: "no claim the main text does not already make". The second clause, "and it is built by an existing builder at different parameters", was **dropped** |
| A1's S1 block, and A2 §5 item 16 | still state the **two-clause** bar, including "reuses an existing builder at different parameters" |

Both act files predated the amendment. **Both now carry the current one-clause bar with
a dated note naming the 19 August 2026 amendment.** A1's S1 governance bullet is
corrected outright, since it states a **rule** and a rule is present tense; it also
records that S1 clears the bar under either version, since it reuses F1's builder. A2 §5
item 16 is a **dated handover** written at session 2's close, so its reasoning is left
standing and a bracketed note beside it records that the second clause was dropped, that
E1 became **S2** on its own builder and was admitted as supplementary anyway, and that
the cost the item named is therefore no longer a cost. Affects governance wording, not a
number.

**Still stale and NOT edited, because it is out of scope:**
`report/figlib/figures/__init__.py` states the **two-clause** bar in the comment above
`SUPPLEMENTARY`, and says above the assertion that `FIGURE_LIST.md` "caps the main text
at 15 and the assertion above enforces it". Both are stale in the same two ways. The
registry is under `report/figlib` and this session may not edit it; recorded here for
whoever next opens it.

### B12. The main-text figure count: **RESOLVED 25 August 2026**

| document | count |
|---|---|
| FL, head of file, as amended 24 August 2026 | **17** (F1 to F7, F9 to F18) |
| FL, supplementary section body | "`FIGURES` in `report/figlib/figures/__init__.py` still holds exactly **15**" |
| CONV, figure style contract | "all **15** sweep figures ... were re-rendered" |
| A1 §5 item 10 | "All **15** sweep figures were re-rendered" |
| A2 §5 item 2 | "a full re-render of all **16** figures" |

Four different counts across four documents, each correct at its own date (15 to 16 on 19
August for F17, 16 to 17 on 24 August for F18).

**Resolved by the present-tense rule.** FL's supplementary-section body was a
**present-tense claim** and is **corrected outright to 17**, with a note recording that
"enforces" also became wrong on 19 August when the cap became a soft count. The other
three are **historical records on dates when their counts were true**, so the sentences
stand and each gained a bracketed note giving the current count: CONV's Okabe-Ito
paragraph, A1 §5 item 10 and A2 §5 item 2. Falsifying a dated log entry to make it agree
with today's count would destroy the record of what was actually re-rendered when.

**Verified against the registry by reading it, not by inference.**
`report/figlib/figures/__init__.py` holds 17 entries (F1 to F7, F9 to F18) and asserts
`assert len(FIGURES) == 17, f"registry holds {len(FIGURES)} figures, not 17"`. **The
file was not edited.**

### B13. How many cells the "spectrum is real" check covers

| document | value |
|---|---|
| A1 §2.5 | max `\|Im lambda\|` = **0.0** over all **80** ladder cells, both scales |
| A1's F1 caption | "max \|Im λ\| = 0 across all **40** cells", N = 448 only |

40 per scale, 80 across both. Not a disagreement; recorded because the two numbers sit in
one document for one check. Carried on sheet 02.

---

## C. Rows whose only source is an act file, FIGURE_LIST or the check file

These numerals **cannot be checked against TIER0**. Grouped by sheet.

### Sheet 00 (chapter 3, the comparison problem)
- **9.4** and **8.3**, the maximum parting of the difference of medians from the median of
  differences; **+338.1** at the nominal peak. FL's F3 flag and A1's F3 block.
- **0.997** and **0.965**, peak `d_eff/N`. FL's F3 flag and A1's F3 block. **Still
  act-and-FIGURE_LIST-only as values**, but B2 is resolved: T0 §3.2 now names them and
  their filter, and T0's own pair (**>= 0.993** / **0.961**) is what body prose quotes.
- `\|lambda_1\|` relative s.d. **0 / 0.0628 / 0.0885 / 0.0867** (N=448) and
  **0 / 0.0385 / 0.0908 / 0.1285** (N=1000). FL's F3 flag; A1 A1.7 and §5.
- **6.3%**, the placement-only residual. A1 A1.7.
- Largest sampled weight relative s.d. **0 / 0.119 / 0.167**, **2 distinct values across 10
  seeds** (3 at N=1000), correlation **+0.854 to +0.949**. FL's F3 flag; A1 §5 item 7.
- Hill index **2.49 -> 2.28**, attributed to the **empirical weight pool**. FL's F3 flag,
  citing E0.4 §5.
- ~~The ladder-internal Jensen figures **0.0431** and **0.0727**. A1 §5 item 4.~~
  **RESOLVED**: both are now in **T0 §1.3 amendment (a)**, along with `random_gaussian`'s
  **0.0868**. No longer act-file-only. See B3.

### Sheet 01 (the substrate and the null ladder)
- **40 rows** per scale; the four-rung ladder as a style-contract fact (CONV).
- Degree-rewire convergence: **107,840** swaps, **1,078,400** attempts, **10,784**
  undirected edges, retention **15.4 / 5.2 / 3.6%** then flat **3.6 / 3.8 / 3.8 / 3.7%**,
  chance floor **~2.2%**, median `bulk95` **0.4288 ... 0.4280**, range **0.0116** =
  **0.26** of the between-seed s.d. All A1 §5 item 3.
- **2500 x 448**, no bias column. A2 §2.5, §2.6.
- The **13** probe spectral radii. CHK Task 2.
- `perron_root == 1.0`, `bulk95_radius` is the ratio. FL's F1/F2 flag; A1 §2.5.
- The N=1000 cell-for-cell rebuild at **0.000e+00**. A1 §2.5, §5 item 15.

### Sheet 02 (the spectrum is real)
- max `\|Im lambda\|` = **0.0**, `is_symmetric` true, **80** cells (**40** in the caption).
  A1 §2.5 and F1 caption.
- **0.188862**, the live-recomputed Perron root. FL's F15 flag.
- The `bulk95` definition (95th percentile over the **full** spectrum, outlier included).
  A1 §2.6 finding 1.
- **2.6e-08** / **2.8e-08** recomputation deviation; per-row `sr_crit == 1/bulk95`. A1 §2.5.
- The F1 density-axis derivation (**1.000000**, **0.6220**, **0.3110**, **52.25**),
  ranges **+/-0.215** and **+/-0.266**, densities **(0.310, 50.9)** and **(0.112, 56.3)**,
  the median-scaling offsets **+0.00630** and **-0.00759**, the bin overhangs **91.1%** and
  **93.1%**, and the **2.8%** residual. A1 §3 and §5 item 13; FL's F1 flag.

### Sheet 03 (the bulk is everyone's; the gap is not, and it is placement)
- **0.325 against 0.52 to 0.55** read off the normalised ECDF; bulk edges **0.0587 to
  0.0614** as a drawn range. A1's F1 caption; FL's F1 flag.
- The identity breaking **by up to 0.055** under the median of per-seed products, and
  holding to **< 1e-15** under the product of medians. A1 §2.3.
- The recomputed spreads **4.426% / 4.447%**. A1 §2.2. See B9.
- The **range / mean** spread convention, which A1 §5 item 2 records as **stated nowhere**
  and recovered by reproduction; it notes range/min gives 4.51 / 6.72 / 7.18 / 70.35 /
  73.20 and that range/max, range/median and the CV all miss.

### Sheet 04 (scale)
- **3.99, 2.39, 2.30, 2.44** in S1 row order, and the non-monotonicity warning. FL's S1
  flag; A1's S1 caption.
- **0.251 against 0.410 to 0.435** at N = 1000. A1's S1 caption.
- The N=1000 rebuild at **0.000e+00**. A1 §2.5, §5 item 15.
- The recomputed spreads **6.430% / 6.886%**. A1 §2.2.

### Sheet 05 (Act I hands over)
- No act-only numerals. Every number is a restatement of T0 §2.1 or §3.1.

### Sheet 06 (Act II, what was handed over)
- **2500 x 448**, no bias column. A2 §2.5, §2.6 finding 4.

### Sheet 07 (the probes and their limits)
- The three conditions' operating points **3.0526 / 2.5263 / 1.2632**. A2 §2.3.
- NARMA-10 **1e-8** and Lorenz **1e-7**, and the hard-coded-default caveat. CHK
  provenance; A2 §2.6 finding 1.
- **8,190 rows**, the complete factorial, `eig_gram` in **8,190 of 8,190**, lengths
  **448** and **449**, the **13** radii, **520** MC ladder cells of which **200**
  supercritical. All CHK Task 2.
- The per-lag Gram offset **0.31 to 0.82** `d_eff` units, **1.6%** of the Weyl bound,
  **0.24%** of the ladder range. A2 §2.5, §2.6 finding 3, §5 item 8.
- The bias-direction bound **1.0** unit, in practice **~1e-12**. A2 §2.6 finding 5.
- **3.3e-16**, time-centring against `np.cov`. A2 §2.5, §2.6 finding 2.
- The **pooled median over n = 30** aggregation behind 0.0001, which A2 records as **not
  stated in T0**. A2 §2.1, §5 item 6.

### Sheet 08 (the Perron mode carries the mean)
- **0.0006** (0.000642) for MC alone, and **4.5x** / **3.9x**. A2 §2.1, §5 item 6, F4
  caption.
- **29 of 30** cells below baseline; the mean-based degeneracy (0.00217 against 0.00232).
  A2 §2.1, §5 item 6.
- **10 of 10 seeds at every `k` <= 5** and chance by **`k` ~ 20**. A2 A2.1, F4 caption.
- **7.6x above chance at `k` = 1** for the harmonics. A2's F4 block and caption.
- The chance band **0.00136 to 0.00321**, and the single-direction s.d. **0.0029** about
  **0.0025**. A2's F4 block.
- **0.575** (weight-permuted under median-then-abs) and the **0.676** maximum
  discrepancy at sigma = 2.42. A2 §2.4, §5 item 1; FL's F11 flag.
- **1/N = 0.002232**. A2 §2.1.

### Sheet 09 (the Gram spectrum against the ridge floor) - the heaviest concentration
- ~~**89.0%** and **11.4%**, the section's own headline pair.~~ **RESOLVED 25 August
  2026**: promoted into **T0 §3.6 amendment (e)**, sourced to CHK §5.1.
- ~~The full four-by-four position table (**0.2 / 4.9 / 8.0 / 89.0**, **2.6 / 36.0 / 18.6
  / 38.1**, **9.9 / 49.3 / 18.3 / 22.0**, **20.4 / 52.8 / 10.6 / 11.4**).~~ **RESOLVED**:
  all sixteen cells are now in **T0 §3.6 amendment (e)**.
- ~~**102.1%**, the sum of the connectome's four per-bin medians.~~ **RESOLVED**: carried
  in **T0 §3.6 amendment (e)** as a required qualifier on the table, beside the
  zero-strip of amendment (a).
- **398.5** directions more than a decade clear. A2's F18 block and §5 item 18.
- **83.5** and **47.5** as the unrounded mode counts. CHK §1.2. See B6.
- **6.4 times** as floor-sensitive per unit of surviving dimensionality; **about 75**
  against **about 413** directions left to lose; **83%** of ER's reservoir unusable and
  **92%** of the connectome's usable. CHK §5.2 and §5.3.
- The 13-point per-variant floor-sensitivity curve, including every variant's **0.00** at
  sigma = 0. CHK §3.1.
- The per-seed argmin splits (**7 of 10**, **7 of 10**, **5 of 10 at each**) and
  `d_eff` = **20.8** at sigma = 0.4211. CHK §3.2.
- The five per-alpha migration rows and the reproduction of `taskB_mc_alpha_peaks.csv`
  (**0.0** on peak sigma, **1.8e-15** on peak MC over 20 rows). CHK §3.3.
- "**two of the four land one grid step off their own dip**" and "the three nulls'
  optimum is identical at every alpha". A2's F18 block; FL's F18 flag.
- The cell-for-cell agreement of `closeout_floor_mass.csv` with the parquet over 910 rows
  (**5.7e-14**, **7.1e-15**, exact, exact, **1.1e-16**). CHK §1.1.

### Sheet 10 (which counting scheme sees it)
- **438 of 448** directions with ridge weight above 0.5; **two directions carry 95% of
  PR = 1.28**; the single cell's `d_eff` = **431** against the median **413**. A2 A2.4 and
  the F6 block and caption.
- The PR identity `sum_i p_i / sum_j p_j^2 = PR` written out. A2's F6 block.
- The seven-rung per-variant table of `d_eff` / PR / MC, and **2.98-fold** for MC. A2 §2.2.
- The recomputed correlations **+0.107143**, **+0.998172**, **+0.308132**, **-0.180**,
  **-0.541**, **-0.607**. A2 §2.2, §5 item 3.
- **"one and the same 2500 x 448 matrix"**, and that this is **not** true of NARMA-10
  (2800 captured, 2000 in the design). A2 §2.6 finding 4.

### Sheet 11 (sign selects the basis)
- **0.00045**, the worst deviation across the 18 reproduced basis cells. A2 §2.3.
- The degree-matched null's swap values **0.168 / 0.002**, **0.011 / 0.102**,
  **0.011 / 0.355**. A2's F5 caption only.
- The three operating points **3.0526 / 2.5263 / 1.2632**. A2 §2.3.

### Sheet 12 (what Act II hands to Act III)
- **0.261** and **0.263** rad, maximum **0.26**, over **36,540** cells. A2 §1 and §5 item
  15. See B5.
- **0.82%**, **49.6%**, **45.0%**, on **12,180** Lorenz cells. A2 §1 and §5 item 15. See
  B4.

---

## D. Status after the decisions of 25 August 2026

**Resolved and closed:** section A's F3b pointer; section A's position-table row;
**B2** (peak `d_eff/N`, by cross-note in three places, no value changed); **B3** (the
Jensen bias, corrected to the ladder in T0 and CONV); **B10** (FL's F2 row verified,
A1's audit item marked resolved in place); **B11** (the S-figure bar, both act files);
**B12** (the figure count, one present-tense correction and three historical
annotations). **B1** is updated rather than closed: §3.6 now has **five** amendments.

**Found already discharged, no edit made:** the four-orders phrasing. A2 A2.7, A2 §4
item 4.5 and CHK §3.3 all already read "five orders"; A2 §5 item 19 records the
correction as made on 24 August 2026. The only surviving occurrences are inside that
dated entry's own table of what documents used to say, and inside T0 §3.6 amendment
(d), which is the correction quoting the old wording. Both are historical and were left
alone.

**Still open, and deliberately so:** section A's items on the **substrate build**, on
what **`erdos_renyi`** preserves, and on what **`clustering_rewire` and
`modularity_rewire`** preserve. These are properties of the code, not of any document
in this set, and were out of scope for this session. Also open: the **N = 1000
per-variant `\|lambda_1\|` and absolute bulk**, the **weight-permuted row of the
anisotropy table**, the **sigma-resolved sensitivity curve** and the **five per-alpha
migration rows** (the last two left in the check file by decision, as figure data), and
disagreements **B4 to B9** and **B13**, none of which was put to the author.

**Newly found and not edited, for whoever opens the file next:**
`report/figlib/figures/__init__.py` states the withdrawn two-clause S-figure bar and
says the assertion "enforces" a cap of 15; both are stale, and the registry is out of
this session's scope. Separately, `FIGURE_LIST`'s F3 flag says "F3 has no panel
letters" while its own F3 **row** and A1's F3 block both describe lettered panels (a),
(b), (c): the flag predates F3's re-expansion and is stale. Neither was in scope.

## E. One standing note for the audit

`report/checks/floor_sensitivity_check.md` says of itself that it "is not canonical for
results" and flags two of its own findings for whoever owns T0 §3.6. One of the two, the
zero-strip, **was** absorbed into T0 as amendment (a) on 24 August 2026. The other, the
interior-minimum wording, was absorbed as amendment (b). The numbers that remain
check-file-only, listed under C above, are the ones **no rank-1 document has yet
absorbed**, and a claim resting on any of them is resting on a check file.

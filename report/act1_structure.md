# Act I — structure sets the spectrum

**Session 1 of the §4b sweep.** Read `report/CONVENTIONS.md` first. Canonical results
live in `TIER0_STATE_OF_PLAY.md`; canonical claims in `ACTION_PLAN_JOURNAL_ROADMAP.md` §1.

**The withdrawn phrase this act must not resurrect:** "compact bulk" / "compressed bulk".
Write **"large spectral gap"** — the absolute bulk is everyone's. This is the act where
the phrase would come back, because in the units the literature reports (`W / |lambda_1|`)
the connectome's bulk genuinely does look narrower: `bulk95` 0.3249 against the nulls'
0.5203 to 0.5535. That appearance is manufactured by dividing by the one quantity that
differs. F1 shows both unit systems side by side for exactly this reason.

---

## 1. Claims register

Every claim this chapter makes, each with a figure and a source. The chapter is written to
this register, not the other way round.

| # | claim (one sentence, as it will appear) | figure | TIER0 § | artifact |
|---|---|---|---|---|
| A1.1 | The recurrent matrix of the non-negative human substrate has an entirely real spectrum consisting of one large Perron eigenvalue standing clear of a bulk. | F1 | §3.1 | `eigenspectrum/results/scale_448/spectra_per_seed.parquet` |
| A1.2 | The **absolute** bulk radius is near-identical across the connectome and its nulls at N=448 (spread 4.4% of the mean, 0.0587 to 0.0614); the entire between-variant difference sits in `\|lambda_1\|`. | F1a-d, F2a-b | §3.1 | same, both scales |
| A1.3 | The headline structural statistic is the gap ratio `\|lambda_1\| / absolute bulk`, identically `1/median(bulk95)` and identically `sr_crit`: **3.078** for the connectome against **1.807 to 1.922** for the nulls at N=448. | F1f, F2c | §3.1, §2.1 | same |
| A1.4 | What survives a 2.2x change in N is the **gap-ratio separation** (3.985 against 2.301 to 2.438 at N=1000), not the near-identity of the bulks, whose spread loosens to 6.4%. | F2, **S1** | §3.1 | `scale_1000/spectra_per_seed.parquet` |
| A1.5 | The effect is weight **placement**: the weight-permuted control holds topology and the exact weight multiset fixed, scrambles only which edge carries which weight, and lands with the nulls (`bulk95` 0.5203, gap ratio 1.922). | F1, F2 | §2.1 | same |
| A1.6 | **Neither matching axis is neutral.** Nominal `sigma` fixes the Perron root and `sigma·bulk95` fixes the bulk; the variants differ *only* in `\|lambda_1\|`, and the memory mechanism under test *is* the Perron mode, so each axis flatters a different answer (+343.3 at nominal 4.47 / -217.4, against +196.5 at 1.949 / -24.0). | F3 | §1.1, §2.2 | `criticality_matched/results/e02_panel.parquet`, `e02_axis_summary.csv` |
| A1.7 | The normaliser is a single **non-concentrating order statistic**: for the resampling nulls the largest sampled weight takes 2 distinct values across 10 seeds and correlates +0.85 to +0.95 with `\|lambda_1\|`; freezing the multiset by permutation still leaves 6.3% relative s.d. in `\|lambda_1\|`, which is the placement contribution alone. | **none — prose** | §2.1 (recomputed, §5 below) | `spectra_per_seed.parquet` both scales |

**A1.7 is the one claim here carried by prose rather than a figure**, and that is a
decision, not an oversight. It had a panel (F3b) which was cut; see the F3 block. The
numbers above are the ones the methods text must state, and `FIGURE_LIST`'s F3 flag
carries the full set plus two phrasings that must **not** be used.

**Claims deliberately NOT made here** (and why):

- **"Compact bulk" / "compressed bulk", in any form.** Withdrawn (`CONVENTIONS`, `TIER0`
  §3.1). The absolute bulk is everyone's; the difference is the gap. A1.2 is the
  replacement and it names the units.
- **That the near-identity of the bulks is scale-robust.** It is not: 4.4% at N=448,
  6.4% at N=1000 (6.9% under the per-seed-product aggregation). Only the gap-ratio
  separation carries. `TIER0` §3.1 is explicit that one sentence must not carry both.
- **Any ordering among the three nulls by `bulk95`.** It reverses between scales
  (N=448 `perm < degree < ER`; N=1000 `ER < perm < degree`), reproduced in §2 below.
  The ordering is quoted at a named scale or not at all.
- **A mechanism for *why* placement produces the gap.** Act I establishes that it does.
  Nothing here explains which topological feature of the placement is responsible; the
  connectome-vs-permuted contrast localises it to placement and stops there.
- **"The connectome is a better reservoir."** No task appears in this act. Contributions
  1 and 5 are properties of `W` and of the matching axis; `FIGURE_LIST`'s claim-to-task
  mapping records them as **task-free**, and no task can corroborate or refute them.
- **That `sigma·bulk95` is the "correct" axis.** A1.6 is symmetric: it says neither axis
  is neutral, not that one is right. The claim rests on surviving both.

---

## 2. Reproduction gate

Run before any figure work. A failed reproduction is the finding and stops the act.

**Verdict: PASSED.** Every documented value returns at the precision `TIER0` publishes it
to. Recomputed from the frozen `spectra_per_seed.parquet` at both scales, filtered to
`condition == "human_empirical"` and the four ladder variants (40 rows per scale, 10 seeds
per variant), every quantity a median over seeds per `CONVENTIONS`.

### 2.1 `bulk95` and `sr_crit` (TIER0 §2.1)

| variant | scale | TIER0 `bulk95` | recomputed | TIER0 `sr_crit` | recomputed | agrees to |
|---|---|---|---|---|---|---|
| connectome | 448 | 0.3249 | 0.324900 | 3.078 | 3.077872 | all published digits |
| weight-permuted | 448 | 0.5203 | 0.520339 | 1.922 | 1.921825 | all published digits |
| degree | 448 | 0.5338 | 0.533804 | 1.873 | 1.873348 | all published digits |
| Erdős–Rényi | 448 | 0.5535 | 0.553468 | 1.807 | 1.806789 | all published digits |
| connectome | 1000 | 0.2509 | 0.250916 | 3.985 | 3.985400 | all published digits |
| weight-permuted | 1000 | 0.4176 | 0.417567 | 2.395 | 2.394827 | all published digits |
| degree | 1000 | 0.4346 | 0.434575 | 2.301 | 2.301097 | all published digits |
| Erdős–Rényi | 1000 | 0.4102 | 0.410223 | 2.438 | 2.437698 | all published digits |

### 2.2 Absolute bulk radius and its spread (TIER0 §3.1)

`abs_bulk = bulk95 * lambda_max_raw`. The spread convention is **range / mean**, recovered
by reproduction (see the audit log — it is stated nowhere).

| quantity | TIER0 | recomputed | agrees to |
|---|---|---|---|
| abs. bulk, connectome N=448 | 0.0614 | 0.061361 | 4 d.p. |
| abs. bulk, weight-permuted N=448 | 0.0599 | 0.059915 | 4 d.p. |
| abs. bulk, degree N=448 | 0.0595 | 0.059512 | 4 d.p. |
| abs. bulk, ER N=448 | 0.0587 | 0.058711 | 4 d.p. |
| abs.-bulk spread N=448, median(bulk95) x median(\|λ₁\|) | 4.4% | 4.426% | 1 d.p. |
| abs.-bulk spread N=448, median of per-seed products | 4.4% ("identical") | 4.447% | 1 d.p. |
| abs.-bulk spread N=1000, product of medians | 6.4% | 6.430% | 1 d.p. |
| abs.-bulk spread N=1000, median of per-seed products | **6.9%** | 6.886% | 1 d.p. |
| `bulk95` spread N=448 | 47.3% | 47.310% | 1 d.p. |
| `bulk95` spread N=1000 | 48.5% | 48.546% | 1 d.p. |

### 2.3 Gap ratio (TIER0 §3.1)

| quantity | TIER0 | recomputed | agrees to |
|---|---|---|---|
| gap ratio, connectome N=448 | 3.08 | 3.077872 | 3 s.f. |
| gap ratio, nulls N=448 | 1.81–1.92 | 1.806789 – 1.921825 | 3 s.f., both ends |
| gap ratio, connectome N=1000 | 3.99 | 3.985400 | 3 s.f. |
| gap ratio, nulls N=1000 | 2.30–2.44 | 2.301097 – 2.437698 | 3 s.f., both ends |
| identity `\|λ₁\|/abs_bulk == 1/median(bulk95) == sr_crit` | asserted | holds to < 1e-15 | machine precision |

The identity holds **only under the product-of-medians aggregation**. Taking the median of
the per-seed products instead breaks it by up to 0.055 at N=1000 (degree: 2.356 against
`sr_crit` 2.301). This constrains F2 — see the audit log.

### 2.4 The connectome/ER `bulk95` ratio, and the convention test

| convention | N=448 | N=1000 | direction | TIER0 |
|---|---|---|---|---|
| **median (canonical)** | 0.587025 | 0.611657 | **rising** | 0.587 → 0.612 ✓ |
| mean (withdrawn) | 0.589788 | 0.582600 | falling | 0.590 → 0.583 ✓ |

Both directions reproduce to 3 d.p., which is the strongest single check in this gate: the
ratio is the one published quantity whose *sign of change* depends on the aggregator, so
recovering "rising" on medians and "falling" on means confirms the recomputation is on the
canonical convention rather than confirming the table by luck.

The withdrawn per-seed **means** listed in §2.1's correction note also return exactly —
0.512003 / 0.523817 / 0.550875 at N=448 and 0.425413 / 0.444868 / 0.430683 at N=1000,
against the note's 0.5120 / 0.5238 / 0.5509 and 0.4254 / 0.4449 / 0.4307. The session-0
correction is therefore confirmed at its source, not merely accepted.

**Null ordering reversal** (TIER0 §2.1) reproduces: at N=448 `perm (0.5203) < degree
(0.5338) < ER (0.5535)`; at N=1000 `ER (0.4102) < perm (0.4176) < degree (0.4346)`.

### 2.5 Integrity checks beyond the published numbers

| check | result |
|---|---|
| `perron_root == 1.0` in every row | holds, both scales |
| `bulk95_radius == bulk95` (the ratio, despite the name) | holds exactly, both scales |
| stored per-seed `sr_crit == 1/bulk95` row by row | holds exactly, both scales |
| `bulk95` recomputed from the stored eigenvalue arrays as `pct95(\|λ\|)/max(\|λ\|)` | max deviation 2.6e-08 (N=448), 2.8e-08 (N=1000) — the `float32` storage precision of `eig_w_real` |
| spectrum is real | `max \|Im λ\| = 0.0` over all 80 ladder cells; `is_symmetric` true in every row |
| **cell-for-cell rebuild from the substrate builder** | **max \|Δ\| = 0.000e+00 on `bulk95`, `lambda_max_raw` and `perron_root`, 40 cells at N=448 and 40 at N=1000** |

The last row closes a real gap: E0.4's own reproduction gate compares against
`analysis/results/scale_{N}/w_spectra.parquet` and **skips at N=1000**, because no
committed reference exists there (`tables.py:reproduction_gate`, and `TIER0` §2.1 states
the gate only for N=448). Rebuilding every ladder cell from `HumanSubstrateBuilder` and
re-running `recurrent_spectrum` reproduces the frozen N=1000 parquet bit-for-bit, so the
N=1000 numbers now have the same standing as the N=448 ones.

**Functions audited:** `bulk95` computation, the `|lambda_1|` normalisation, null generation and its assertions

**Findings:**

1. **`bulk95` is what it claims to be.** `src/analysis/spectral.py:116` computes
   `np.percentile(mods, 95)` where `mods` is `|lambda| / |lambda_1|` over the **full**
   spectrum, sorted descending, with the Perron outlier included in the percentile
   population — the 95th percentile of `|lambda|` over the full spectrum divided by
   `|lambda_1|`, exactly as `common.BULK95_DEFINITION` states and as the independent
   recomputation in §2.5 confirms. One implementation, reached by every caller through
   `manifold.spectra.capture_w_spectra`; nothing re-derives it.
2. **`sr_crit` uses the median convention where it is reported.**
   `tables.py:summarise` sets `sr_crit = 1 / bulk95_median` and renames the per-seed
   aggregates to `sr_crit_perseed_mean/median/std` so the two cannot be confused. The
   per-seed `sr_crit = 1/bulk95` written into `spectra_per_seed.parquet` by
   `tables.py:derive` is a per-row value, not an aggregate, and is correct as such.
   **But see audit-log item 1: the headline gate and the committed markdown summary are
   still on the mixed convention that produced the withdrawn §2.1 values.**
3. **The degree-preserving rewire converges at N=1000.** E0.4 was silent on this and the
   builder's assertion does not test it — `validate_null(..., "degree_sequence")` checks
   the sorted degree sequence, which double-edge swaps preserve *by construction* after
   any number of swaps, including zero. Tested directly: see audit-log item 3. It
   converges.
4. **The Jensen bound in `CONVENTIONS` is real but belongs to a rung outside the ladder.**
   See audit-log item 4.

---

## 3. Figures

One block per figure ID from `FIGURE_LIST.md`. **Caption written before the figure.**

### F1 — the spectral gap

- **Claim carried:** A1.1, A1.2, A1.3, A1.5
- **Source:** `eigenspectrum/results/scale_448/spectra_per_seed.parquet`, source
  `spectra_448`; columns `eig_w_real`, `bulk95`, `lambda_max_raw`; filter
  `condition == "human_empirical"` and `variant in LADDER` (40 rows).
- **Layout:** descends from the committed E0.4 Figure 1
  (`eigenspectrum/figures/fig1_spectrum.png`) — small multiples, an ECDF, a per-seed
  strip — with every axis re-pointed from `bulk95` to the gap. That figure is titled
  "Connectome weight placement compresses the eigenvalue bulk" and draws all six of its
  panels in units of `|lambda_1|`, which is precisely what makes the connectome's band
  look narrow. Here the small multiples are **stacked vertically down the left on one
  shared raw-units axis**, with (e) top right and (f) bottom right.
- **Panels:** (a-d) one substrate per row, raw units, shared x and y, log density; bulk
  band shaded at ±`median(bulk95) x median(|lambda_1|)`, gap shaded from there out to
  ±`median(|lambda_1|)` (dotted); substrate name and gap ratio set **above** each row as
  left- and right-aligned titles, in the white space between panels. One spectrum per
  row — for the nulls, the seed whose `bulk95` is nearest the median — **scaled by the
  median `|lambda_1|`, not by that seed's own** (see the audit log). (e) ECDF of
  **normalised** `|lambda| / |lambda_1|`, all 10 seeds, 95th-percentile level drawn and
  labelled above its own rule, legend lower right. (f) per-seed gap ratio with a median
  bar and `bulk95` on the right-hand axis.
- **Column split 1 : 1.25**, left to right — (e) and (f) carry a legend, two axis labels
  each and a secondary axis, and need the width more than the stacked rows do. **One
  naming scheme throughout**: `style.VARIANT_TITLE` for the row titles, the (e) legend
  and the (f) tick labels, so the four substrates are not named three ways in one
  figure. Row titles are at full `TITLE_SIZE`.
- **The split is what the typography is tuned against, so re-tune if it moves.** The
  binding constraint is the longest row-title pair, "Weight-permuted" against
  "gap ratio = 1.92". Measured from the rendered text extents, not judged by eye:

  | column split | row-title clearance | (f) tick clearance | titles at |
  |---|---|---|---|
  | 1 : 1.5 | 0.8 px | — | `TITLE_SIZE` |
  | 1 : 1.5 | 14.1 px | 22.3 px | `TITLE_SIZE − 1` |
  | **1 : 1.25 (current)** | **12.2 px** | **16.1 px** | **`TITLE_SIZE`** |

  At 1:1.5 the left column could not carry the titles at full size at all; at 1:1.25 it
  can. Widening the right column again means dropping the row titles a step, and
  narrowing it squeezes (f)'s two-line tick labels instead.
- **Panel labels are placed by absolute offset, not axes fraction.**
  `style.panel_label`'s `dx` / `dy` are axes fractions, so the offset they buy scales
  with the panel — fine for a figure whose panels are one size, which is every other
  figure here, and why that remains the default. F1 stacks four 91.8 px rows beside two
  203.0 px panels, so a shared `dy` put the 'e' **21.5 px higher on the page** than the
  'a' level with it. `panel_label` now takes an optional `offset_points=(dx_pt, dy_pt)`
  which anchors the letter a fixed distance from the axes' top-left corner. All six of
  F1's labels now sit **6.1 px above their own panel top, spread 0.00 px**, and 'a' and
  'e' are level to within half a pixel. The vertical offset matches the row titles' pad,
  so a-d's letters align with their titles; the horizontal offset differs by column
  because each must clear its own y-label and ticks. **No other figure moved** — the
  new argument defaults to `None` and the fractional path is untouched.
- **The density axis is derived, not chosen.** `density=True` integrates to exactly
  1.000000 over the bins for all four substrates (checked). A bin holding exactly one of
  the 448 eigenvalues therefore sits at `1 / (448 x bin width)` = 0.6220, so the floor is
  set to half that (0.3110) and single eigenvalues out in the gap stay visible as bars
  rather than being clipped into the spine; the ceiling is twice the largest peak
  (2 x 26.126 = 52.25). All four rows share the axis, so bar heights are comparable down
  the column. Ticks at 1 and 10, both inside the range.
- **Nothing is labelled inside the panels.** The bulk band, the gap band and the
  `lambda_1` rule are named in the caption instead: with four rows, in-panel labels
  repeat visually and crowd the histogram, and `lambda_1` sits close enough to the right
  edge that its rule cut through anything placed there.
- **Why the stack, and why (e) is normalised.** The vertical stack puts the four bulk
  bands at the same page coordinate, so "the bulk is common, the gap is not" is read by
  sighting down the column rather than inferred from four separate axes. That makes a
  *raw-units* ECDF redundant — an earlier draft used one as (e) and it was making the
  same point less directly — which frees (e) to show the substrates in the units the
  rest of the thesis matches on. The two halves are the same spectra one division apart,
  and the caption says so explicitly rather than leaving the reader to notice.
- **Caption (final wording):**

  > **Figure F1. Connectome weight placement buys a large spectral gap, not a compact
  > bulk.** Eigenvalues of the un-rescaled recurrent matrix `W` on the all-positive human
  > substrate (N = 448 self-built consensus, empirical weights). The substrate is
  > symmetric, so the spectrum is entirely real (max |Im λ| = 0 across all 40 cells) and
  > is drawn on the real axis; a complex-plane scatter would be degenerate, with all mass
  > on one line. **(a-d)** One substrate per row in **raw units of `W`**, on a shared
  > axis, with the bulk (±absolute bulk radius, coloured) and the gap out to ±λ₁ (grey)
  > shaded. Sighting down the column, the four coloured bulk edges sit at the same place —
  > 0.0587 to 0.0614, a spread of 4.4% of their mean — while λ₁ (dotted) runs from 0.1061
  > for Erdős–Rényi to 0.1889 for the connectome, so the grey gap grows from row d to row
  > a and the gap ratio rises from 1.81 to 3.08. The weight-permuted control (b) holds
  > the topology and the exact weight multiset fixed and scrambles only which edge carries
  > which weight, and it sits with the nulls: the effect is weight **placement**, not
  > weight statistics and not topology alone. Each row draws a single spectrum — for the
  > nulls, the seed whose bulk95 is nearest the median — so all four are 448 eigenvalues
  > at equal sampling noise; the connectome is one fixed graph and has no seed variation
  > to average. **(e)** The same spectra as ECDFs after each substrate is divided by its
  > own λ₁, which is the normalisation every spectral-radius-matched comparison in this
  > thesis uses. In these units the curves separate everywhere and the connectome's
  > appears compressed — that separation is the division, not a difference in the bulk,
  > as (a-d) show. Since bulk95 is defined as the 95th percentile of |λ| over |λ₁|, the
  > crossings of the 95% line are bulk95 itself and can be read off the axis: 0.325 for
  > the connectome against 0.52 to 0.55 for the nulls. **(f)** The gap ratio
  > |λ₁| / absolute bulk per seed, with its reciprocal bulk95 on the right-hand axis:
  > 3.078 for the connectome against 1.807 to 1.922 for the nulls. The connectome's ten
  > seeds coincide exactly, because it is one fixed graph and only the nulls are
  > resampled.

### F2 — gap, not bulk, at both N

- **Claim carried:** A1.2, A1.3, A1.4, A1.5
- **Source:** source `spectra_both` = `scale_448` and `scale_1000`
  `spectra_per_seed.parquet` concatenated with a `scale` column, same filter (80 rows).
  Panel a `median(bulk95) x median(lambda_max_raw)`; panel b `median(lambda_max_raw)`;
  panel c `1 / median(bulk95)`.
- **Panels:** three zero-based bar panels, N = 448 solid and N = 1000 translucent:
  (a) absolute bulk radius; (b) |λ₁| in raw units; (c) the gap ratio. **No panel titles
  or in-panel annotations** — the figure is kept clean and the numbers live in the
  caption.
- **Substrates are named once, in a figure-level legend, not on three x-axes.** F1, F2
  and F3 all use `style.VARIANT_TITLE`'s plain names; the rung numbering was dropped
  because it named the same four substrates a second way in the same chapter. In F2 the
  plain names then would not fit: three panels at 198 px carry the same four categories,
  and the labels collide by up to 12.4 px at the contract's tick size, clearing only at
  5pt — well below the 8pt floor and not legible. Measured, not judged by eye. So the
  substrate names moved to one horizontal legend under the panels, which also removes
  three redundant copies of the same axis. **Two legends, each carrying one variable:**
  colour is substrate (figure legend), alpha is scale (panel c). F3's panel b had room
  and keeps its tick labels, at +13.0 px clearance.
- **F7, F9 and F13 still split `VARIANT_LABEL` on " · " and so still show rung
  numbering.** They belong to later sessions and were not touched. If the plain names
  are wanted thesis-wide, `style.VARIANT_TITLE_TICK` is there for them — but F7 and F13
  have panels narrower than F2's, so they will hit the same fit problem and probably
  want F2's legend treatment rather than a tick swap.
- **The caption is load-bearing here, which it is not for every figure.** All three
  panels are zero-based, so "near-identical" in (a) against "separated" in (b) is a
  comparison the reader makes directly rather than one an axis crop has arranged. The
  cost of a zero-based axis is that it *hides* the 4.4%: panel (a) alone reads as
  identity, not near-identity. Three numbers therefore have to survive anywhere the
  caption is shortened — **the absolute-bulk spread (4.4% / 6.4%), the 1.78x Perron
  ratio, and the `sr_crit` identity**. They were previously set as panel titles and are
  now caption-only.
- **Caption (final wording):**

  > **Figure F2. The difference between the connectome and its nulls is a spectral gap,
  > not a compact bulk, and what carries across scale is the gap.** Per-seed spectra of
  > the un-rescaled `W` on the all-positive substrate, four variants x 10 seeds, at both
  > parcellation scales (solid N = 448, translucent N = 1000). All three panels are
  > zero-based and use one aggregation throughout — median over seeds of `bulk95` and of
  > |λ₁| — so panel c is exactly panel b divided by panel a. **(a)** The absolute bulk
  > radius is near-identical across variants at N = 448 (spread 4.4% of the mean) and
  > merely close at N = 1000 (6.4%; 6.9% if the per-seed products are taken before the
  > median, which is the aggregation that must be quoted with the number at this scale).
  > **(b)** |λ₁| in raw units, where the variants do separate: the connectome's Perron
  > root is 1.78x ER's at N = 448. **(c)** The gap ratio |λ₁| / absolute bulk, which is
  > identically 1/median(bulk95) and identically the critical scale `sr_crit`: **3.078**
  > for the connectome against **1.807 to 1.922** for the nulls at N = 448, and **3.985**
  > against **2.301 to 2.438** at N = 1000. Across a 2.2x change in N the connectome
  > stands ~1.7x clear of every null in (c) while the near-identity in (a) loosens, so the
  > scale-robust statement is the separation, not the coincidence of the bulks. The
  > ordering *among* the three nulls by bulk95 reverses between scales and is not read
  > across them.

### F3 — neither matching axis is neutral

- **Claim carried:** A1.6 (contribution 5; sits in chapter 3, methods)
- **Source:** `criticality_matched/results/e02_panel.parquet` filter
  `interp == "linear"`, columns `x, axis, d_eff_connectome, d_eff_erdos_renyi,
  dD_median, dD_q25, dD_q75`, plus `e02_axis_summary.csv` (2 rows). 121 grid points per
  axis, both already restricted to the four-variant overlap.
- **Panels:** (a) connectome and ER on **nominal σ**; (b) the same two on **σ·bulk95**;
  (c) the two deltas, with peak and most-negative points marked. (a) and (b) share a y
  axis and shade the band between the curves.
- **Grouped by axis, not by substrate.** `dD` is a between-substrate quantity at fixed x,
  so putting both substrates in one panel makes the **vertical gap between the curves be
  the delta** — it collapses from (a) to (b) in front of the reader. Grouping by
  substrate (one panel per substrate, both axes in each) shows each curve re-indexed,
  which is real but secondary, and it separates the two curves that need comparing.
- **The `d_eff = N = 448` ceiling is drawn**, per `CONVENTIONS`. It is not decoration
  here: **ER runs along it** (peak 0.997 of N against the connectome's 0.965), so the
  "connectome advantage" in (c) is largely *how far below ceiling the connectome sits and
  where*, which the delta panel alone cannot show. This is the reason the split was
  worth making.
- **0.997 / 0.965 is this panel's pair; `TIER0` §3.2 has a different one, and neither is
  wrong. Added 25 August 2026.** `TIER0` §3.2 gives peak `d_eff/N` as **≥0.993 for every
  null and 0.961 for the connectome**, at α = 1e-6 over the taskA α sweep, per-variant
  peak over σ. The values above come from **this figure's own source**,
  `e02_panel.parquet`, as per-substrate medians over seeds on the nominal axis. Same
  argument, two filters, and neither document named the other until now. **The thesis
  quotes `TIER0`'s pair**; 0.997 / 0.965 stays inside F3's caption with its filter
  stated, and is not carried into body prose. `FIGURE_LIST`'s F3 flag carries the same
  cross-note.
- **(a) and (b) do not subtract to (c), by construction.** `dD_median` is the median over
  seeds of the **per-seed difference**; `d_eff_connectome` and `d_eff_erdos_renyi` are
  the medians of each substrate **separately**, and the median of differences is not the
  difference of medians. They part by up to **9.4** on the nominal axis and **8.3** on
  the matched one; at the peak, +343.3 against +338.1. The paired per-seed statistic is
  the correct one for a paired comparison and is what `TIER0` §2.2 publishes, so (c)
  keeps it. **The caption states the distinction** rather than letting a reader measure
  the gap in (a) and find ~9 units missing — the same defect class as F2's mixed
  aggregation, which was caught the same way.
- **Reduced from the merged F3 + F8, then re-expanded.** Session 1 first cut the
  merged-in F8 panel (relative s.d. of |λ₁| across seeds) because it argued a *different*
  claim — "the normaliser is unstable" rather than "neither axis is neutral" — and two
  arguments in one figure read as two half-figures. A1.7 moved to methods prose;
  `FIGURE_LIST`'s F3 flag carries the numbers it must state. The three panels here are
  all the *same* argument at increasing levels of aggregation.
- **Ownership:** Session 1 renders this; **Session 3 must not re-render it**, and Session
  3's E0.2 reproduction gate is what validates it.
- **Caption (final wording):**

  > **Figure F3. Spectral-radius matching is not a neutral comparison.** Ridge effective
  > rank `d_eff` for the connectome and Erdős–Rényi at f = 0, N = 448, medians over 10
  > seeds. **(a)** Against **nominal σ**, which holds the Perron root fixed. The two
  > substrates are badly misaligned: ER reaches the `d_eff = N` ceiling near σ = 2 and
  > falls away, while the connectome peaks later and lower, so the shaded gap between
  > them is large and changes sign. **(b)** The identical data against **σ·bulk95**,
  > which holds the bulk radius fixed. The curves now coincide almost exactly up to the
  > peak and separate only supercritically; the gap has largely closed. **(c)** Those
  > gaps as Δd_eff. On nominal σ the connectome runs from −217.4 to +343.3 at σ = 4.47;
  > on σ·bulk95 the same data gives −24.0 and +196.5 at 1.949 — retaining 57% of the
  > advantage and removing **89% of the apparent subcritical deficit**. The two axes are
  > not alternative conveniences: the four substrates differ *only* in |λ₁| (F1, F2 —
  > their absolute bulk radii agree to 4.4%), so there is one degree of freedom between
  > them and each axis holds fixed exactly what the other lets vary, while the memory
  > mechanism under test is the Perron mode itself. Each axis therefore assumes away part
  > of what is being tested, in opposite directions. This thesis reports both, states
  > what each holds fixed, and rests no claim on one alone. *Note:* (c) plots the median
  > over seeds of the per-seed difference, which is the paired statistic and the
  > published one; (a) and (b) plot each substrate's median separately. The two differ by
  > up to 9 `d_eff` units, so (a) and (b) are not expected to subtract exactly to (c).


### F19: the four substrates, as graphs

- **Claim carried:** **none.** F19 prints in §4's outline item 2, "The substrate and the
  null ladder", which is registered above as carrying **no results**: every numeral in it
  is a design fact or a count. The figure is the ladder drawn rather than described.
  Added 1 September 2026; `FIGURE_LIST` carries the count amendment and the reason.
- **Source:** `report/artifacts/substrate_edges.parquet` (source `substrate_edges`;
  117,106 rows = 22 (variant, seed) cells x 5,323 edges) and
  `substrate_topology.parquet` (source `substrate_topology`; 22 rows). Node ordering from
  source `substrate_order`, **computed live**, as `perron_yeo` is. The seed for the two
  randomised variants comes from `spectra_448` by F1's own rule.
- **The sources did not exist.** Every frozen artifact in the sweep is a *reduction* of a
  substrate: eigenvalues, task scores, Gram spectra. None held adjacency, so
  `report/artifacts/build_substrate_graphs.py` was written and committed to freeze it.
  It rebuilds the four cells from `HumanSubstrateBuilder` at N = 448 on
  `human_empirical`, which §2.5 above shows reproduces the frozen spectra cell for cell
  at 0.000e+00. **No run happened and none was needed.** Parquets are gitignored
  repo-wide; the script is the committed object.
- **Verifications, then the gate, then the write.** Edge count 5,323 in all 22 cells;
  every `degree_rewire` seed's sorted degree sequence equal to the connectome's; then
  connectome against control, **byte-identical binary adjacency and exact equality on all
  four statistics**. The gate is the reason the figure exists in this section: it is the
  check that the placement control is a placement control, and a nonzero difference on
  any of the four would be a defect in the permutation rather than a finding.
- **Panels:** 3 x 4. (a-d) binary adjacency, zeros white, with the degree marginal above
  each column on shared y limits; (e-h) weighted adjacency on a shared logarithmic colour
  scale, same ordering; (i-l) one diagonal block magnified, marked on (e-h) and drawn on
  that same scale. One node ordering throughout: hemisphere, then community, then
  descending degree within community, with separator lines at the community boundaries
  and the hemisphere split drawn heavier.
- **The magnified block is selected by a stated rule, and it is a BLOCK not a community.
  Added 1 September 2026.** Of the diagonal blocks of the drawn ordering, the one with
  the highest within-block binary edge density among blocks of 15 to 40 nodes:
  hemisphere 1, community 5, 22 nodes, 125 internal edges, density 0.5411, with all three
  in-range candidates recorded in `TIER0` §3.13. An earlier community-level rule was
  withdrawn for **non-contiguity**: hemisphere is the outer key, so a community spanning
  both hemispheres occupies two non-contiguous diagonal blocks and the indicator would
  have to mark two squares and the rectangle between them. `_densest_block` raises rather
  than widening the range. **The zoom panels share (e-h)'s scale**; rescaling them would
  make (i) against (j) a comparison of two scales. The builder asserts that (i) and (j)
  fill the same 250 cells, which is the block-level form of the connectome/control gate. A community that spans the hemispheres therefore appears as two blocks,
  because hemisphere is the outer key.
- **The sequential maps are not variant colours.** A matrix cell is an edge, not a
  substrate, so the Okabe-Ito palette is spent where substrate identity is carried: the
  column titles and the degree marginals. `Greys` and `magma_r` are both colourblind-safe
  and monotone in luminance, and both put zero at white.
- **The seed is F1's.** The two randomised variants are drawn at the seed whose `bulk95`
  is nearest the median (degree 1, Erdős–Rényi 2), which is what F1's panels a-d draw.
  The rule was extracted into `act1_structure._representative_row` and both builders now
  call it, so the two figures cannot come to draw different graphs. F1 and S1 re-render
  byte-identical after that extraction, checked rather than assumed.
- **The four statistics are a chapter table, not a panel. Changed 1 September 2026.**
  They were drawn as a strip beneath the columns and are now `tab:act1-topology` in
  chapter 4, filled from `TIER0` §3.13 to four decimal places. Four rows of numbers under
  four matrices read as a fifth band of the figure rather than as a table.
  `substrate_topology.parquet` and `TIER0` §3.13 are unchanged; only the rendering moved,
  and the figure no longer reads the topology source at all.
- **What the numbers are** (medians over the ten seeds for the two randomised variants;
  the connectome and the control are single graphs). Promoted to `TIER0` §3.13, which is
  the canonical home:

  | variant | mean clustering | modularity (fixed) | degree assortativity | global efficiency |
  |---|---|---|---|---|
  | connectome | 0.4277 | 0.5486 | 0.1067 | 0.4064 |
  | weight-permuted | 0.4277 | 0.5486 | 0.1067 | 0.4064 |
  | degree | 0.0697 | -0.0002 | -0.0192 | 0.4789 |
  | Erdős–Rényi | 0.0529 | -0.0036 | -0.0068 | 0.4820 |

  The seed spread on the fixed-partition modularity straddles zero for both randomised
  variants (degree -0.0086 to +0.0031, ER -0.0082 to +0.0090), so the sign of either
  median is not a reading. Four decimal places is what the table uses, which keeps every
  cell on one precision and never prints a signed zero.

### S1 — F1 at N = 1000 (appendix, outside the cap)

- **Claim carried:** A1.4 (and A1.1 to A1.3, A1.5 at the larger parcellation)
- **Source:** `eigenspectrum/results/scale_1000/spectra_per_seed.parquet`, source
  `spectra_1000`; same filter as `spectra_448` (40 rows, 1000 floats per `eig_w_real`).
  Frozen; **no run was needed** and none happened.
- **Builder:** the same one as F1. `f1_spectrum` and `s1_spectrum_n1000` are both thin
  wrappers over `_spectrum_figure(ctx, source_name)`, so the two scales cannot drift: the
  median-`|lambda_1|` scaling, the per-row `[-lambda_1, +lambda_1]` binning and both
  assertions live in the shared path.
- **Governance.** `CONVENTIONS` working rule 3 is "no figure that is not on
  `FIGURE_LIST.md` — if one seems missing, report and stop", and `FIGURE_LIST` records
  the main-text count with `figures/__init__.py` asserting it. A scale replicate is
  exactly the case
  that would erode a cap by increments, so it went into a **separate `SUPPLEMENTARY`
  registry** instead. **The bar recorded in `FIGURE_LIST` is that an S-figure makes no
  claim the main text does not already make.** That is the whole bar.
  **Updated 25 August 2026.** As written on 15 August this bullet stated a **two-clause**
  bar, the second clause being "and reuses an existing builder at different parameters",
  and said `FIGURES` "still holds 15". `FIGURE_LIST`'s amendment of **19 August 2026**
  (session 4) **dropped the second clause**: it was a *proxy* for the test that matters
  and it excluded exactly the case a supplementary figure is most useful for, supplying
  intuition for a claim the main text asserts but cannot illustrate. S1 satisfied both
  clauses and made the proxy look free; **S2 is the case that showed it was not**, since
  E1 needs its own builder and was admitted as supplementary anyway. The count is **17**
  as of 25 August 2026, and the assertion **records** the count rather than gating it,
  per the same 19 August amendment. S1's own standing is unchanged: it reuses F1's
  builder and makes no new claim, so it clears the bar under either version.
- **Two axis assumptions were hard-coded to N=448 and are now derived.** The x ticks were
  a fixed `[-0.2 ... 0.2]` and the y ticks a fixed `[1, 10]`. Both happen to remain valid
  at N=1000 — the spectrum runs to ±0.266 rather than ±0.215, and the density range is
  (0.112, 56.3) rather than (0.310, 50.9) — but they survived by luck, not design. The
  ticks are now computed from the range, so a third parcellation cannot silently clip.
- **Caption (final wording):**

  > **Figure S1. F1 at the larger parcellation (N = 1000).** As Figure F1 in every
  > respect — same substrate family, same null ladder, same builder — at the N = 1000
  > self-built consensus rather than N = 448. **(a-d)** The four bulk bands again sit at
  > the same place while λ₁ separates, and the gap ratio again stands the connectome
  > ~1.7x clear of every null: **3.99 against 2.30 to 2.44**. **The rows are in ladder
  > order and their gap ratios are not monotone here** — reading down, 3.99, 2.39, 2.30,
  > 2.44 — because the ordering of the three nulls by bulk95 reverses between the two
  > parcellations (`TIER0` §2.1). What is scale-robust is the connectome's separation
  > from the nulls, not the arrangement among them, and not the near-identity of the
  > bulks, whose spread loosens from 4.4% at N = 448 to 6.4% here. **(e)** bulk95 read
  > off the 95th-percentile crossing: 0.251 for the connectome against 0.410 to 0.435.
  > **(f)** The per-seed gap ratio; the connectome's ten seeds again coincide exactly,
  > because it is one fixed graph and only the nulls are resampled.


---

## 4. Section outline

Structure only, at the level of section headings and the argument each carries. Prose is
written by hand, not generated (see the roadmap §4b note on drafting).

**Chapter 3 (methods) — the one section Act I owns there**

1. **The comparison problem.** Why connectome-reservoir work matches on spectral radius;
   what that normalisation does to a family of matrices that differ only in |λ₁|.
   *Carries A1.6.* Figure F3.
   1. The two axes, and what each holds fixed.
   2. The same data on both (F3a): the deficit is 89% axis, the advantage 57% robust.
   3. The normaliser's own noise, **in prose, no panel**: non-concentrating order
      statistic, and the permutation control that separates weight draw from
      placement. *Carries A1.7.* **Corrected 25 August 2026**: this item read
      "(F3b)". That panel was cut on 15 August 2026 when the merged-in F8 was
      removed, and A1.7 moved to methods prose. §1 marks it "none — prose" and
      `FIGURE_LIST`'s F3 flag carries the numbers it must state. The pointer was
      worse than dead: F3's current panel (b) exists and shows the σ·bulk95 axis,
      not the normaliser's noise. The numbers survive in §5 items 6 and 7.
   4. The rule adopted for the rest of the thesis: report both, state what each fixes,
      rest the claim on surviving both.

**Chapter 4 — Act I proper**

2. **The substrate and the null ladder.** Self-built consensus at N = 448 and N = 1000;
   the four rungs and what each holds fixed; why `connectome_weight_permuted` is the
   control that isolates placement. No results.
3. **The spectrum is real, and it has one outlier.** *Carries A1.1.* Figure F1a.
   Symmetry, the Perron root, why the figure is a histogram and not an eigenvalue cloud.
4. **The bulk is everyone's; the gap is not.** *Carries A1.2, A1.3.* Figures F1b, F2a-c.
   1. Raw units against normalised units, and what the normalisation manufactures.
   2. The gap ratio, and the identity `|λ₁|/abs_bulk = 1/bulk95 = sr_crit` — one quantity,
      three names, named after what it measures.
   3. The explicit retraction of "compact bulk", stated once, in the direction the data
      supports.
5. **It is placement.** *Carries A1.5.* The weight-permuted contrast, and the limit of
   what it licenses: placement, not *which* feature of placement.
6. **Scale.** *Carries A1.4.* Figure F2, both scales. What carries (the separation), what
   loosens (the near-identity), what reverses (the null ordering) and is therefore not
   quoted across scales.
7. **What Act I hands to Act II.** `sr_crit` as the criticality scale each substrate
   brings with it; the Perron mode as the object Act II decomposes. One paragraph.

---

## 5. Audit log and open issues

Anything that did not reproduce, any number that moved, any claim that had to be weakened,
and anything a later session needs to know.

1. **The mixed-convention defect — RESOLVED 16 August 2026, after being mis-scoped
   twice.** `TIER0` §2.1 was corrected in session 0 (commit `861984e`), but the code that
   produced the withdrawn values was not: `tables.py:_markdown` printed `bulk95` as
   **mean ± sd** in a column beside `sr_crit = 1/median(bulk95)` — two conventions side by
   side, which is exactly the Jensen trap §1.3 exists to prevent, and the origin of the
   withdrawn 0.5120 / 0.5238 / 0.5509. `_HEADLINE_448`'s note was also backwards, calling
   the correct median (0.520) "a documentation drift" against the mean (0.512).

   **Two things this session got wrong about it, corrected here.** First, the note was
   described as needing an E0.4 re-run to clear. It did not: the summary is a pure
   function of the frozen `spectra_per_seed.parquet` — verified, `summarise()` on that
   file reproduces the committed CSV to 1e-12 at both scales — so it can be rebuilt
   without re-capturing. `run()` would have re-captured 210 eigendecompositions **and
   rewritten `spectra_per_seed.parquet`**, the source F1, F2 and S1 read, which working
   rule 1 forbids. `tables.rewrite_summaries(scale)` does the rebuild instead, asserts
   the parquet does not move, and replays the gate lines from `manifest_tables.json`
   labelled as replayed rather than claiming a gate it did not run.

   Second, this file and commit `e992cfc` both called the summaries **"committed"**. They
   are not. `.gitignore` excludes the whole of `eigenspectrum/results/` — parquets (229),
   CSVs (254), markdown (265) and manifests (267) — so every E0.4 output is a local,
   regenerable artifact. Nothing in the repo ever carried the withdrawn numbers; what
   carried them was the generator, which is tracked and is now fixed.

   **Why the summaries were not simply deleted**, which was the proposal: `bulk95_
   summary.csv` is a **live dependency**, read by
   `criticality_matched/common.py:eigenspectrum_summary()` — the E0.2/E0.3 pipeline that
   produces F3's source — and by `eigenspectrum/summary.py`, with
   `criticality_matched/__main__.py` erroring if the N=1000 file is absent. It is also
   not defective: it carries `bulk95_mean` **and** `bulk95_median` alongside
   `sr_crit`. Only the `.md` rendering was wrong, and deleting a generated file would
   have left the generator intact to recreate it.

   Both scales' `.md` and `.csv` are now rebuilt from the frozen spectra. The N=448
   human_empirical table reads 0.3249 / 3.078, 0.5203 / 1.922, 0.5338 / 1.873,
   0.5535 / 1.807 — `TIER0` §2.1 exactly, with `sr_crit` now reproducible by hand as
   `1 / bulk95` row by row. The header records what the table used to print and why it
   changed.

2. **The spread convention was not documented and had to be recovered.** `TIER0` §3.1
   quotes 4.4% / 6.4% / 6.9% / 47.3% / 48.5% without saying how a "spread" is formed.
   Only **range / mean** reproduces all five; range/min gives 4.51/6.72/7.18/70.35/73.20
   and range/max, range/median and the CV all miss. The convention is now stated in F2's
   caption and in §2.2 above. Worth promoting into `CONVENTIONS`' numerical section, since
   a later session recomputing a spread will otherwise re-derive it or, worse, not notice.
3. **The degree-preserving rewire converges at N=1000 — tested, since E0.4 was silent.**
   Production is `n_swaps_multiplier = 10`, i.e. 107,840 accepted double-edge swaps
   against a cap of 1,078,400 attempts at N=1000 (10,784 undirected edges). Re-ran the
   chain at multipliers 1, 2, 5, 10, 20, 40 on 5 seeds. Every chain completed (no
   `NetworkXAlgorithmError`) and preserved the degree sequence exactly. Retention of the
   original edge set falls 15.4% → 5.2% → 3.6% and is then **flat** from multiplier 5 to
   40 (3.6%, 3.8%, 3.8%, 3.7%), against a ~2.2% chance floor at this density. Median
   `bulk95` is stationary: 0.4288, 0.4281, 0.4189, 0.4172, 0.4210, 0.4280 — a total range
   of 0.0116, which is **0.26 of the between-seed s.d.**, and non-monotone (multiplier 40
   lands where multiplier 1 does). The chain is mixed well before the production setting;
   the docstring's "sufficient to decorrelate at N=300" understates where it was verified,
   and it now holds at N=1000 too.
4. **`CONVENTIONS`' Jensen figure of 0.087 is right, but not about the ladder.**
   Reproduced exactly as `mean(1/bulk95) − 1/mean(bulk95) = 0.0868` for **`random_gaussian`
   at N=1000** on `human_empirical` — which is what `common.SR_CRIT_CONVENTION`'s source
   comment says ("for random_gaussian, whose bulk95 is the most dispersed"), but which
   `CONVENTIONS.md` drops. Within the four-rung ladder the true Jensen gap tops out at
   **0.0431** (ER, N=1000). Against the *median* rather than the mean the ladder maximum is
   0.0727 (ER, N=1000) and the sign is **negative** for all three N=1000 nulls — the
   per-seed mean of `1/bulk95` sits *below* `1/median(bulk95)` there. So "biased upward"
   is a statement about mean-vs-mean, not mean-vs-median. The convention is unaffected
   (the median is still the right aggregator, and it is the one in use); only the gloss is
   loose.
5. **F2's panels were on two different aggregations, and the figure's own claim needs
   them on one.** As built in session 0, panel a took `median(per-seed abs_bulk)` while
   panel c took `1/median(bulk95)`. Panel c is then *not* panel b over panel a: at N=1000
   the degree rung gives 2.356 by division against 2.301 as `sr_crit`, a 0.055 gap. Since
   the whole point of panel c is the identity `|λ₁|/abs_bulk ≡ 1/bulk95 ≡ sr_crit`, panel
   a was moved to `median(bulk95) x median(|λ₁|)`, which is also `TIER0` §3.1's table
   convention and reproduces it exactly. The quoted N=1000 spread therefore becomes 6.4%
   rather than 6.9%; both are in §3.1 and the caption names which. `FIGURE_LIST`'s F2 row
   specifies the median-of-products form and is now inconsistent with the builder —
   **the row should be updated to `median(bulk95) x median(lambda_max_raw)`.**

   **RESOLVED 25 August 2026.** Verified by reading `FIGURE_LIST`'s F2 row, whose source
   cell now reads `abs_bulk = median(bulk95) * median(lambda_max_raw)`, the
   product-of-medians form this item asked for, and the one the builder and `TIER0`
   §3.1's table both use. The row is therefore consistent with the builder and nothing
   was edited to make it so. The item is marked resolved in place rather than deleted,
   because the reasoning in its first half (why panel c is not panel b over panel a
   unless both are on the product of medians, and the 0.055 gap at N=1000 that shows it)
   is still the reason the row has to read that way.
6. **`FIGURE_LIST`'s F3 flag contains a false statement, corrected in place.** It reads
   "The permuted-multiset control (relative s.d. exactly 0) is the evidence and belongs in
   the panel." The permuted control's relative s.d. of **|λ₁|** is **0.0628** at N=448 and
   0.0385 at N=1000, not 0. What is exactly 0 under permutation is the **largest sampled
   weight** (the multiset is identical every seed), and what is exactly 0 for **|λ₁|** is
   the *connectome*, trivially, because it is one fixed graph. Built as specified, the
   panel would have annotated a 0.063 bar as though it were zero. The panel now shows the
   decomposition instead — permutation freezes the weight draw and leaves the placement
   contribution — which is a stronger version of the same argument and is what the flag's
   own "defensible wording" paragraph actually describes. The flag has been corrected.
7. **E0.4 §5's Hill/`|λ₁|` correlation reproduces.** `FIGURE_LIST` attributes "corr +0.85
   to +0.95" between the largest sampled weight and |λ₁| to E0.4 §5. Recomputed across
   seeds: +0.854 (degree) and +0.939 (ER) at N=448, +0.949 and +0.906 at N=1000. All four
   inside the quoted band. The max-weight relative s.d. is *identical* for degree and ER
   (0.118992 at N=448, 0.167018 at N=1000) because both draw the same pool under the same
   seed; only 2 distinct maxima occur across 10 seeds at N=448 and 3 at N=1000, which is
   the non-concentration the claim rests on, shown directly.
8. **Withdrawn language survives in a code docstring.** `src/analysis/spectral.py`'s module
   docstring still reads "more compressed bulk" and "Lower `bulk95_ratio` / `mean_ratio`
   => more compressed bulk => milder effective dynamics". Not report prose and not
   changed here (it would touch a module every act depends on, for no figure), but it is
   the last place in the repo that states the withdrawn direction as fact, and it should
   be rewritten when that file is next opened for a substantive reason.
9. **`style.VARIANT_TICK` added.** `VARIANT_LABEL` is a legend label and is too wide for a
   four-category bar axis at 8pt — "connectome" and "perm. weights" overlapped in F2 and
   F3. A two-line tick variant was added to `report/figlib/style.py`. **Applied to F2 and
   F3 only.** F7 and F9 (`figures/act3_memory.py`) and F13
   (`figures/act3_prediction.py`) still split `VARIANT_LABEL` on " · " and will hit the
   same collision; they are those sessions' to change, and the helper is there for them.
   Note F7 and F13 have panels narrower than F2's, so a straight tick swap will not fit —
   they will want F2's figure-legend treatment instead.
10. **The palette moved to Okabe-Ito, thesis-wide, on the author's decision.** The
    session-0 set put the three nulls on purple `#9467bd` / pink `#e377c2` / light blue
    `#88aadd`, which is weak under deuteranopia and collapses in greyscale — a defect in
    figures whose entire job is telling four substrates apart. `report/figlib/style.py`
    and `src/experiment/plots._VARIANT_STYLE` were changed **together in one commit**,
    because `style.check_colour_consistency()` asserts they are equal and the smoke
    entry point runs it. `CONVENTIONS`' colour clause carries a dated amendment marking
    this as a deliberate one-time change and not a precedent. Okabe-Ito was already the
    palette of the committed E0.4 figures, so the move also ended a split between those
    and the sweep. All 15 sweep figures were re-rendered. [15 was the count on that
    date; it is **17** as of 25 August 2026, F17 added 19 August and F18 added
    24 August. Left as the historical record of what the palette change touched.]
11. **Re-rendering the per-task figures cost no compute, and needed a new tool.** Each
    task's `run.py:main` calls `runner.run_matrix` before `plots.run`, so invoking it
    would re-run the experiment — against `CONVENTIONS` working rule 4. But `plots.run`
    needs only the config and the frozen `results.parquet` / `stats_*.parquet`, all of
    which were on disk. `tools/replot_task_figures.py` rebuilds each task's config
    through that task's own `build_config` (so the two cannot drift) and calls
    `plots.run` alone. **22 of the 24 tracked variant-styled figures were re-rendered**
    across human MC / NARMA-10 / Lorenz at both scales and C. elegans Mackey-Glass at
    both horizons. No simulation ran. MG was included because
    `PREREG_MACKEY_GLASS.md` §§1-3 are written and committed, lifting working rule 6.

    **Extended to the manifold probes, where the obvious entry point would have
    regenerated a frozen source.** Six further committed figures use `_VARIANT_STYLE`:
    probe1's `manifold_{pr,mean_curvature,spectral_entropy}_vs_sr.png` and probe3's
    `probe3_deff_{vs_mc,vs_sr,two_axis}.png`. **None is a thesis figure** —
    `FIGURE_LIST` is canonical for those, and Act II's chapter figures F4 to F6 render
    through `figlib` on the current palette — so these are analysis-time artifacts,
    refreshed only so the repo does not carry two palettes. The trap: `probe3.run_deff`
    describes itself as *"No reservoir runs"*, which is true of compute, but it
    **rewrites `probe3_deff.parquet`** — the frozen source F6 reads and the one
    `TIER0` §3.12's numbers were promoted from. `probe3.run` likewise rewrites
    `manifold_geometry_performance.parquet` and `manifold_gap_tracking.parquet`. The
    tool therefore reads the frozen parquets and calls the plotting functions directly
    (probe3's are private `_plot_*`; that is deliberate), and **fingerprints every
    parquet under `experiments/` before and after, raising if one moves**. 90 parquets,
    unchanged, verified on the run that produced these six.
12. **Two tracked figures were already stale before this session and remain so.**
    `celegans_mackey_glass/figures/h{84,300}/effect_sizes_vs_spectral_radius.png` are
    untagged legacy names from before `plots.py` began metric-tagging its effect-size
    output (commit `ba23ebc`). Nothing produces that filename any more, their
    metric-tagged replacements sit beside them and were re-rendered, and they are now
    stale in palette as well as in name. **They should be deleted**, but deleting tracked
    artifacts is not this session's call to make unilaterally.
13. **F1's rows mixed two aggregations, and the largest eigenvalue fell outside the
    drawn gap.** Caught by eye on the rendered figure, not by any check. Panels a-d drew
    one seed's spectrum scaled by **that seed's** `|lambda_1|`, while the bulk band, the
    gap band and the `lambda_1` rule were all **medians over seeds** — and the seed is
    selected for `bulk95` nearest the median, which constrains its `|lambda_1|` not at
    all. The two therefore disagreed by whatever that seed's `|lambda_1|` happened to be:

    | row | seed | seed `\|lambda_1\|` | median `\|lambda_1\|` | offset |
    |---|---|---|---|---|
    | a connectome | 0 | 0.18886 | 0.18886 | **0.00000** |
    | b weight-permuted | 0 | 0.11432 | 0.11515 | −0.00083 |
    | c degree | 1 | 0.10390 | 0.11149 | −0.00759 |
    | d Erdős–Rényi | 2 | 0.11238 | 0.10608 | **+0.00630** |

    So the ER row's largest eigenvalue overshot its own `lambda_1` rule by 6%, and the
    degree row's fell 7% short, leaving a dead strip inside the grey gap. **Panel a was
    exact only because the connectome is one fixed graph**, which is precisely why the
    defect survived several rounds of looking at the figure: the row a reader checks
    first is the one row that could not show it.

    **Fixed** by scaling each displayed spectrum by the **median** `|lambda_1|` rather
    than the seed's own. `eig_w_real` is stored normalised (max `|lambda|` = 1), so the
    largest bar now lands exactly on the rule by construction — which is what
    `lambda_1` means. A uniform scale factor preserves the shape exactly, and it strips
    the seed-to-seed `|lambda_1|` jitter that F3 measures at 6 to 9% relative s.d. and
    that has no business moving a panel whose every drawn number is a median. **The
    builder now asserts** that the drawn spectrum's largest `|lambda|` equals the rule,
    so this fails the build rather than the eye if the storage convention ever changes.
    Residual, stated rather than hidden: the displayed bars' own 95th percentile still
    differs from the drawn median bulk edge by up to 2.8% (ER), because one seed's
    `bulk95` is not the median `bulk95`. That one is mid-distribution rather than at a
    hard visual edge, and drawing per-seed bulk edges instead would show a 7.3% spread
    across the four rows where the published figure is 4.4%.

    **A second, independent defect at the same edge, found the same way.** With the
    scaling fixed, bars still crossed the `lambda_1` rule — because all four rows shared
    one bin grid whose edges have nothing to do with any variant's `lambda_1`. The bar
    *containing* the extreme eigenvalue spans a whole bin, and that bin's outer edge
    falls wherever the grid puts it. Measured overhang, as a fraction of a bin width:

    | row | overhang past `+lambda_1` | and past `-lambda_1` |
    |---|---|---|
    | a connectome | 36.8% | none |
    | b weight-permuted | **91.1%** | none |
    | c degree | **93.1%** | none |
    | d Erdős–Rényi | 43.8% | **0.0016 (also outside)** |

    The eigenvalues were in the right places; their bars were not. Rows b and c were the
    conspicuous ones at ~92% of a bin, which is what drew the eye; row d's negative-side
    overhang had not been noticed at all. **Fixed** by binning each row over exactly
    `[-lambda_1, +lambda_1]` instead of a shared grid: `lambda_1` is the largest modulus,
    so that interval contains every eigenvalue by definition and the histogram's support
    *is* the shaded region. Bin *count* varies per row so bin *width* stays constant to
    ~0.3%, keeping bar widths comparable down the column and the densities on the same
    footing. **The builder asserts** that every eigenvalue is captured by the row's bins,
    so a bar outside the gap fails the build. Confirmed by measuring the rendered
    artists rather than by eye: all four rows' bars span within ±`lambda_1` exactly.

    **The general lesson, worth carrying to other figures:** both defects were invisible
    on the connectome row — the first because it is one fixed graph, the second because
    its `lambda_1` happened to land early in its bin. The row a reader checks first was
    the row that could not show either problem, and both survived several rounds of
    inspection because of it. Shared-grid histograms drawn against per-series reference
    lines should be assumed guilty until measured.
14. **`figures.py` split into a package, one module per act.** It had reached 1006
    lines and was still growing; four more sessions add to it. Split along the section
    banners it already carried, so the seams were structural rather than invented:
    `figures/__init__.py` (registry + cap assertion), `common.py`, and
    `act1_structure` / `act2_manifold` / `act3_memory` / `act3_prediction` /
    `act4_anchor` — **one module per act, which is one module per sweep session**, so
    sessions 2 to 4 each edit one file. Largest is now 428 lines (Act I, which carries
    the 237-line shared `_spectrum_figure` behind F1 and S1).

    **The act decides the module, not the chapter.** F3 prints in chapter 3 but is Act
    I's argument and Session 1 renders it; F16 prints in chapter 6 but needs both Act III
    arms so Session 4 renders it. Chapter 6 splits cleanly along the two arms, which is
    also the sessions-3/4 boundary.

    **The registry stayed central deliberately.** A per-module registry merged at import
    time could be grown one figure at a time without anything noticing — exactly the
    drift `FIGURE_LIST`'s cap of 15 exists to prevent. It stays in `__init__.py` with the
    assertion, and that assertion was tested by injection (a bogus 16th entry raises
    `cap is 15 figures, registry holds 16`) rather than assumed.

    **Verified byte-identical.** Renders were first shown deterministic across two runs,
    making a hash comparison a meaningful gate; all 16 figures then hashed identically
    before and after the move. Public names are unchanged, so
    `from report.figlib.figures import FIGURES` still resolves and `--only`, `--smoke`,
    `--all` are unaffected. No unused imports left behind (checked per module).

    **`sources.py` was deliberately not split.** At 669 lines it has the same shape, but
    its natural axis is different: sources are shared across acts (`spectra_both` feeds
    F2, `taskb` feeds F7), so an act split would cut across the grain. If it is ever
    split it should be by experiment — eigenspectrum, criticality_matched, manifold
    probes, phase diagram — and not in the same change.
15. **N=1000 now has a cell-for-cell reproduction, which it did not before.** E0.4's
    `reproduction_gate` skips at N=1000 for want of a committed `w_spectra.parquet`
    reference, so `TIER0` §2.1's "Reproduction gate passed at N=448" was the only such
    statement on record. Rebuilding all 40 N=1000 ladder cells from
    `HumanSubstrateBuilder` reproduces the frozen parquet to **0.000e+00** on `bulk95`,
    `lambda_max_raw` and `perron_root`. Worth a line in `TIER0` §2.1 next time it is
    edited.

16. **Outline compression, recorded 24 August 2026 so it is not rediscovered as an open
    question during drafting.** **Chapter 4's third and fourth sections merge into one
    when the chapter is written**: *"The bulk is everyone's; the gap is not"* and *"It is
    placement"*. Between them they carry **one decomposition and one control**, the
    bulk-against-gap split and the weight-permuted contrast that says the split is
    placement, and a section break inside a single argument buys nothing.

    **The two numberings differ by one, so both are given.** §4's outline runs 1 to 7
    across two chapters: item 1 is the chapter 3 methods section Act I owns, and items 2
    to 7 are chapter 4. Counted **within chapter 4** the merging pair is its **3rd and
    4th** sections; counted **in the outline** they are items **4 and 5**. Both
    descriptions name the same pair, and a reader who takes "sections 3 and 4" as outline
    items would merge the wrong two, since outline item 3 is *"The spectrum is real, and
    it has one outlier"*, which is decomposition without a control and stays where it is.

    Nothing moves with the merge. **A1.2, A1.3 and A1.5** are carried by the merged
    section exactly as the outline carries them now, F1 and F2 are unchanged, and the
    limit A1.5 is always quoted with, placement rather than *which feature* of placement,
    travels intact. **The outline itself is left as it stands**, because this is a
    drafting decision rather than a structural one and the register is what the chapter is
    written to. No other act file changed structurally in this pass except Act II's, whose
    §4 gained a section (`act2_manifold.md` item 17).

# Pre-registration: what makes weight placement produce the spectral gap

**Written before any of the analysis below was run.** Commit this file alone,
before the analysis commit. Follows the pattern of `PREREG_MACKEY_GLASS.md`:
sections 1 to 3 are the prediction and are frozen at commit; section 4 is
written afterwards and may not edit sections 1 to 3.

**Status of the claim being tested.** Act I currently claims that the effect is
weight **placement** and explicitly claims no mechanism for why placement
produces the gap. `act1_structure.md` §1 lists "a mechanism for why placement
produces the gap" among the claims deliberately not made, and fact sheets 03
and 05 carry it as a forbidden phrasing. **Nothing in the register changes
unless section 4 records a clean result**, and the decision rule for "clean" is
in §3 below, fixed in advance.

---

## 1. The candidate account

For a symmetric non-negative matrix, the Perron root is the maximum of the
Rayleigh quotient over non-negative vectors. Heavy weights on edges that share
endpoints reinforce one another in that quotient, because it counts paths
through the nodes they meet at. Heavy weights scattered over a sparse graph do
not.

The weight-permuted control holds the graph and the exact weight multiset fixed
and destroys only which edge carries which weight. So it destroys exactly that
coincidence, and nothing else.

**Candidate account:** the connectome's heavy edges are adjacent to one another,
forming a heavily weighted core; a heavy core carries a large Perron root; the
permutation scatters the heavy edges and the core dissolves. In the connectomics
literature this structure is the weighted rich club, and its standard null is a
weight permutation on the fixed graph, which is this thesis's control.

**Two alternative accounts, tested here and expected to fail.**

- **More weight.** Excluded by construction: the multiset is preserved exactly,
  so total and mean strength are identical. For a symmetric non-negative matrix
  `mean_strength <= lambda_1 <= max_strength`, and the lower bound is exactly
  invariant under permutation. The entire connectome-to-control difference in
  `|lambda_1|` lives inside that interval.
- **One strong node.** The upper bound is not invariant, so a single dominant
  hub could in principle carry the difference.

## 2. What will be measured

All three from `report/artifacts/substrate_edges.parquet`, already frozen for
the substrate figure. N = 448, `condition == "human_empirical"`, the four drawn
substrates, the two randomised ones at all ten seeds. No new run, no new
simulation, read-only against the existing artifact.

1. **Heaviest-edge masking curve.** For each substrate, order edges by weight
   descending, keep the heaviest `k`, zero the rest, and record `lambda_1` of
   the masked matrix as a fraction of the unmasked `lambda_1`. Sweep `k` from a
   small fraction of the edge count to all 5,323 edges. Masking entries of a
   non-negative matrix downward cannot raise its spectral radius, so each point
   is a rigorous lower bound on the full `lambda_1` and the curve is monotone
   non-decreasing in `k`.

   **Internal control, required:** the same sweep on the connectome with edges
   kept in **random** order rather than heaviest-first, ten orderings. Without
   it the panel is a statement about sparsification and not about weight
   placement.

2. **The strength sandwich.** Mean node strength, maximum node strength and
   `|lambda_1|`, per substrate, in raw units of `W`.

3. **Weight against endpoint degree product.** Mean edge weight binned by the
   product of its two endpoints' binary degrees, connectome and control, with
   a rank correlation and its confidence interval.

## 3. Predictions, and the decision rule

Locked before any of the above is computed.

- **P1.** The connectome's masking curve lies materially above the control's at
  every mask below half the edges, and above its own random-order control.
- **P2.** The ratio of maximum node strength, connectome over control, is
  smaller than their Perron ratio of **1.64**, so a single strong node does not
  account for the gap.
- **P3.** Edge weight correlates positively with endpoint degree product in the
  connectome, and at approximately zero in the control, where it is zero by
  construction up to sampling.

**Decision rule, fixed here.**

- **Clean positive:** P1 holds with visible separation at the median mask, and
  P2 holds. Then a mechanism claim enters the register as A1.8, the existing
  exclusion is **narrowed and not deleted**, and the six documents listed below
  are edited in one pass.
- **Clean negative:** the connectome and control masking curves coincide. Then
  the heavy-core account is refuted, the register is unchanged, and the result
  is written into the main text in three sentences beside the claim it bounds,
  as a negative result.
- **Equivocal, meaning anything else:** the register is unchanged, the current
  limit stands as written, and the analysis is recorded here and goes no
  further. **Equivocal is not to be resolved by looking harder.**

**One session. No second analysis if the first is equivocal.**

## 3.1 What this cannot claim, on any outcome

- **No derivation.** A masking curve shows that the heaviest edges carry more of
  the Perron root in the connectome than in a permutation of it. It does not
  derive `|lambda_1|` from any structural statistic and it predicts no value.
- **No sufficiency.** "Heavy edges are adjacent" is not shown to be sufficient
  to produce the gap, only to distinguish these two substrates on this graph.
- **No task claim.** No task appears in Act I.
- **"Compact bulk" and "compressed bulk"** remain withdrawn on every outcome.
- **The bulk is untouched.** This concerns `|lambda_1|` only. The absolute bulk
  is near-identical across substrates at N = 448 and nothing here revisits it.
- **Nothing about the connectome's communities**, unless a measurement below
  actually addresses them. The masking curve does not.

## 3.2 Documents that change on a clean positive, and only then

Edited in one pass, after section 4 is written, never before:

1. `act1_structure.md` §1: new A1.8; the "no mechanism" exclusion narrowed to
   "no derivation of `|lambda_1|` from a structural statistic, and no
   sufficiency claim".
2. `TIER0_STATE_OF_PLAY.md`: new subsection under §3 with the numbers, the
   aggregation, the artifact path and a scope guard.
3. Fact sheet 03: forbidden phrasing revised from "a mechanism" to the narrowed
   form.
4. Fact sheet 05: the same, plus the handover's "no mechanism" row.
5. `CROSS_ACT_SPINE.md`: Act I's "hands on" entry, which currently records "no
   mechanism" as the limit.
6. Chapter 4 §3 final paragraph and §5 closing sentence.

`CONVENTIONS.md` is **not** on this list. No withdrawn phrasing is affected by
any outcome.

---

## 4. Result

*Written after the analysis. Sections 1 to 3 are frozen and may not be edited
from here.*

### 4.1 What was read, and the reconstruction gate

Read-only against two frozen files. No run, no regeneration, no published number moved.

* `report/artifacts/substrate_edges.parquet`, N = 448, `condition == "human_empirical"`,
  the four drawn substrates: connectome at seed 0, weight-permuted control at seed 0
  (F1's representative-seed rule, which is what that file stores), `degree_rewire` and
  `erdos_renyi` at all ten seeds. 22 cells, 5,323 undirected edges each.
* `eigenspectrum/results/scale_448/spectra_per_seed.parquet`, column `lambda_max_raw`,
  the gate.

Every weighted adjacency was rebuilt from its edge rows and its `|lambda_1|` checked
against `lambda_max_raw` for the same `(variant, seed)` before anything else was
computed.

**Gate PASSED.** Over the 22 cells the maximum absolute deviation is **4.30e-16** and the
maximum relative deviation is **3.61e-15** (`degree_rewire`, seed 1), against a float32
storage precision of 1.19e-07.

The weight column holds 5,323 distinct values, so the descending sort has no ties and the
connectome and its control keep the **identical weight values** at every `k`. Between
those two rows only which edge carries which weight differs.

Written by `report/artifacts/build_placement_mechanism.py` to five parquets under
`report/artifacts/`: `placement_mechanism_gate`, `_masking`, `_strength`,
`_degree_weight`, `_rank_correlation`.

### 4.2 Heaviest-edge masking curve

64 values of `k`, log-spaced from 1% to 100% of the 5,323 edges and dense at the low end,
with the four masks below forced in exactly. Each entry is `lambda_1` of the masked matrix
as a fraction of **that cell's own** unmasked `lambda_1`. Monotone non-decreasing in `k`
on all 32 curves, asserted. Medians over the ten seeds for the two randomised substrates.
The random-order control is the connectome's own edges kept in random order, ten
independent orderings, quoted as min / median / max.

| mask | connectome | weight-permuted | degree rewire | Erdős–Rényi | random-order connectome |
|---|---|---|---|---|---|
| 5% (k = 266) | **0.7848** | 0.9338 | 0.9251 | 0.9629 | 0.1304 / 0.2071 / 0.5560 |
| 10% (k = 532) | **0.8667** | 0.9413 | 0.9327 | 0.9738 | 0.2495 / 0.2974 / 0.5561 |
| 25% (k = 1331) | **0.9409** | 0.9650 | 0.9482 | 0.9864 | 0.3253 / 0.4867 / 0.5870 |
| 50% (k = 2662) | **0.9901** | 0.9871 | 0.9791 | 0.9933 | 0.5458 / 0.7024 / 0.7357 |

The connectome's curve lies **below** the control's at every mask below **39.2%** of the
edges (`k` = 2086), which is where the two first meet. Above that it lies fractionally
above, by +0.0030 at the 50% mask. The gap at the 5% mask is 0.149, the control over the
connectome.

The connectome's curve lies above its own random-order control at every `k` short of the
full edge set.

### 4.3 The strength sandwich

Raw units of `W`. Medians over the ten seeds for the two randomised substrates.

| variant | mean strength | `\|lambda_1\|` | max strength |
|---|---|---|---|
| connectome | 0.077349 | 0.188862 | **0.517022** |
| weight-permuted | 0.077349 | 0.114319 | **0.203490** |
| degree rewire | 0.077995 | 0.111487 | 0.263071 |
| Erdős–Rényi | 0.077995 | 0.106078 | 0.188844 |

Both gates hold. `mean_strength <= |lambda_1| <= max_strength` on all 22 cells, and mean
strength is identical between connectome and control: 0.077349271856294810 against
0.077349271856294796, a difference of 1.39e-17.

**Max-strength ratio, connectome over control: 2.5408.** The Perron ratio §3 fixes for the
comparison is 1.64 (median over seeds, 0.1889 / 0.1151); the cell-matched ratio at the
seed both rows are stored at is 1.6521. The max-strength ratio is larger than either.

### 4.4 Weight against endpoint degree product

**Binning rule:** 20 equal-count bins (`pandas.qcut`, 20 quantiles) on the product of the
two endpoints' binary degrees, cut on the connectome's products. The control is the same
binary graph, so both rows are binned identically and are comparable bin for bin: 255 to
277 edges per bin, degree product spanning 36 to 3,795.

Spearman rank correlation of edge weight against endpoint degree product, with a 95%
percentile bootstrap interval over 10,000 resamples of the 5,323 edges, seed 0:

| variant | Spearman rho | 95% CI |
|---|---|---|
| connectome | **-0.1242** | [-0.1507, -0.0979] |
| weight-permuted control | **-0.0033** | [-0.0304, +0.0237] |

Mean edge weight in the connectome runs from 0.004627 in the lowest degree-product bin to
0.002993 in the highest. The control's twenty bin means range over 0.002719 to 0.004209.

### 4.5 The three predictions

**P1 does not hold.** Its second clause does: the connectome's curve lies far above its
own random-order control at every mask, 0.7848 against a random-order median of 0.2071 at
the 5% mask. Its first clause fails, and fails in the direction opposite to the
prediction. The connectome's curve does not lie materially above the control's below half
the edges; it lies below it at every mask under 39.2%.

**P2 does not hold.** The max-strength ratio is 2.5408, larger than the Perron ratio of
1.64 rather than smaller, so the exclusion P2 was written to perform does not go through.

**P3 does not hold.** Its second clause does: the control's correlation is -0.0033 with an
interval covering zero. Its first clause fails. The connectome's correlation is negative,
-0.1242, with an interval excluding zero, not positive.

### 4.6 Verdict: EQUIVOCAL

Against the decision rule frozen in §3, and applied as written:

* **Not a clean positive.** That branch requires P1 and P2. Neither holds.
* **Not a clean negative.** That branch is defined by the connectome and control masking
  curves **coinciding**. They do not coincide: they separate materially at every mask
  below 39.2% of the edges, by 0.149 at the 5% mask.

Anything else is equivocal, so the verdict is **equivocal**.

Per §3, therefore: the register is unchanged, the current limit in `act1_structure.md` §1
stands as written, none of the six documents listed in §3.2 is edited, and this analysis
is recorded here and goes no further. **Equivocal is not to be resolved by looking
harder**, and §3's "one session, no second analysis" governs.

§3.1's limits stand on this outcome as on any other: no derivation of `|lambda_1|` from a
structural statistic, no sufficiency claim, no task claim, and every withdrawn phrasing
stays withdrawn.
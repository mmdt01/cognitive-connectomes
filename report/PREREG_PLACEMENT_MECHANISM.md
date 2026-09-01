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

[to be completed]
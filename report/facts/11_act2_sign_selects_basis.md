# Fact sheet 11: chapter 5 section 6, "Sign selects the basis"

**Section:** `report/act2_manifold.md` §4, **section 6**. **Deliberately short**, and framed
as a statement about the decomposition rather than about sign.
**Claims carried:** A2.3. This is the one claim in the act that is **deliberately not a
contribution**.
**Figure:** F5 (a, b, c).

**What is claimed is the swap, not the capture.** On the all-positive substrate neither
basis captures much at `k` = 10, so "the manifold lives in low-frequency graph harmonics"
overstates it.

Source key: **T0** = `TIER0_STATE_OF_PLAY.md`. **A2** = `report/act2_manifold.md`.
**FL** = `report/FIGURE_LIST.md`.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| MC all-positive **0.056 / 0.009**; signed **0.017 / 0.060**; gaussian **0.020 / 0.040** | captured variance at `k` = 10, harmonics against `W` eigenmodes | T0 §3.12(2) | `results/scale_448/manifold_alignment.parquet` | seed medians over 10 seeds, connectome, each condition at **its own** supercritical operating point (3.0526 / 2.5263 / 1.2632) | 448 | nominal | **Probe 2 scope: two substrates at four spectral radii.** No statement here may imply the four-variant ladder |
| NARMA-10 all-positive **0.040 / 0.002**; signed **0.005 / 0.527**; gaussian **0.006 / 0.886** | the same at `k` = 10 | T0 §3.12(2) | as above | as above | 448 | nominal | as above |
| Lorenz all-positive **0.168 / 0.004**; signed **0.019 / 0.081**; gaussian **0.012 / 0.522** | the same at `k` = 10 | T0 §3.12(2) | as above | as above | 448 | nominal | as above. **F5 draws Lorenz**, which is the clearest case, not the only one; the swap reproduces in MC and NARMA-10 too |
| the **ordering swaps in all three tasks** | the claim | T0 §3.12(2) | as above | as above | 448 | nominal | harmonics ahead when weights are non-negative, `W` eigenmodes ahead once signs are balanced, **and the topology never changes**. **State the swap, not the capture** |
| **0.04 to 0.17** | the whole range of `k` = 10 capture on the all-positive substrate, either basis | T0 §3.12(2) | as above | as above | 448 | nominal | **this is the qualifier that stops the overstatement.** Neither basis captures much, so "the manifold lives in low-frequency graph harmonics" overstates it |
| **0.886** | gaussian NARMA-10's `W`-eigenmode capture at `k` = 10, the high-capture case | T0 §3.12(2) | as above | as above | 448 | nominal | quoted **as the other end of the agreement with Probe 3**: where `d_eff` is low the capture is high |
| supercritical `d_eff` **~413 of 448** on the all-positive substrate | why the low capture is expected | T0 §3.12(2), §3.2 | `probe3_deff.parquet` | median over 50 supercritical cells | 448 | nominal | the fluctuations occupy **hundreds of directions** and **no 10-vector basis should capture them**. The two probes **agree without being fitted to each other**, which is the strongest thing in this section |
| **0.00045** | worst absolute deviation across all 18 reproduced cells of the basis table | **Not in T0.** A2 §2.3 | `manifold_alignment.parquet` | recomputation against the published table | 448 | nominal | the reproduction gate for this claim; the swap reproduces in all three tasks |
| degree-matched null: **0.168 / 0.002**, **0.011 / 0.102**, **0.011 / 0.355** | the same swap on the only other substrate the capture covers | **Not in T0.** A2 F5 caption only | as above | seed medians | 448 | nominal | used **once, as a cross-check inside a caption**. It is a **two-substrate result and implies nothing about the null ladder** |
| **3.0526 / 2.5263 / 1.2632** | the three conditions' own supercritical operating points | **Not in T0.** A2 §2.3, F5 block | as above | read from the data | 448 | nominal | each panel is at **its own** condition's operating point; the three are not one sigma |
| `k` = 10 | where the table is quoted, not where anything happens | **Not in T0** as a statement. A2 F5 block | as above | not applicable | 448 | nominal | the swap is visible across the whole curve; the rule at `k` = 10 exists **so the figure and the table can be read against each other** |
| **confirmatory of Krauss (2019)** | the priority position | T0 §3.12 priority note; A2 §1 and F5 block; FL F4/F5 flag | not applicable | not applicable | 448 | not applicable | sign-gating of the manifold transition is **largely pre-empted by Krauss 2019** and is on the roadmap's "what must NOT be claimed" list. It is here because **Act II needs the basis fixed before section 5 can ask how many directions the readout uses** |
| the `W`-eigenmode alignment has already been **absorbed into the mean** | how this section connects back to section 3 | A2 §4 item 6.1. **Not in T0** | not applicable | not applicable | 448 | nominal | with non-negative weights, what is left for the fluctuations to be organised by is **graph structure**; balancing signs hands it back. **That is the decomposition talking, not a separate phenomenon** |
| one clause forward-referencing **chapter 6 §6.3** | where the signed condition stops being a comparison | A2 §4 item 6.5; `report/CROSS_ACT_SPINE.md` | not applicable | not applicable | 448 | not applicable | in chapter 6 §6.3 the signed condition becomes an **intervention**, a lesion that removes the proposed cause. Here it is a comparison |

## Forbidden phrasings for this section

- **"the manifold lives in low-frequency graph harmonics."** Withdrawn as an
  overstatement: on the all-positive substrate neither basis captures much at `k` = 10
  (0.04 to 0.17). The claim is which basis **wins**.
- **Any ladder reading of Probe 2.** `manifold_alignment.parquet` holds `connectome` and
  `degree_rewire` only, at four spectral radii. Neither F5 nor F4a may be read as a ladder
  result, and the degree rung appears once, as a caption-level cross-check.
- **"sign-gating of the manifold transition is a new result."** It is largely pre-empted by
  Krauss 2019 and is presented as **confirmatory**.
- **"balancing the signs improves the representation."** The claim is which basis the
  fluctuations occupy, not that one basis is better.
- **Quoting the capture values as evidence of how much structure the bases hold.** State
  the swap.
- **Treating this section as a `f` result.** The signed and gaussian **conditions** are
  weight families in the same capture; `f` as an intervention is chapter 6 §6.3, and this
  section carries one forward-referencing clause and no more.
- **"compact bulk", "compressed bulk."**
- Any **graded curvature or trajectory-straightness** account.

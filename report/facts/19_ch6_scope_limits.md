# Fact sheet 19: chapter 6 section 7, "What the account does not cover"

**Section:** `report/CROSS_ACT_SPINE.md`, Act III, **§6.7** of the seven-section breakdown
added 28 August 2026. The scope limit returned to **deliberately**, at the end of the
chapter rather than left to the discussion.
**Claims carried:** none new. A3P.9 restated from the other side; RM §1's "what must NOT
be claimed" entries on the `f` = 0 generation regime and on contribution 2's missing
out-of-sample test.
**Figures:** none.

**Extraction only.** Every number was read from the document named in its source cell.
**No Mackey-Glass data was inspected** (CONV working rule 6).

Source key: **T0** = `TIER0_STATE_OF_PLAY.md` (rank 1). **RM** =
`ACTION_PLAN_JOURNAL_ROADMAP.md` §1 and §5. **FL** = `report/FIGURE_LIST.md`. **A3M** =
`report/act3a_memory.md`. **A3P** = `report/act3b_prediction.md`. **PREREG** =
`report/PREREG_MACKEY_GLASS.md`. **SPINE** = `report/CROSS_ACT_SPINE.md` (structure
only). A row whose source is not T0 is **not TIER0-backed** and says so.

## Movement 1: the account is a statement about the `f` > 0 counterfactual

**This is §6.3's open problem restated from the other side**, and it is returned to
deliberately rather than allowed to fade.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| "capacity is gated by which dynamical regime the manifold is in" is a statement about the **`f` > 0 counterfactual**, not about the biological substrate | the scope limit itself | T0 §3.11 | `e01_jacobian_scale_448.parquet` | not applicable | 448 | nominal | T0 §3.10 and §3.11 both carry it. It is **the** sentence this section exists to state |
| curvature **0.26** flat across the whole sweep while VPT falls **~10x** | the measurement the limit rests on | T0 §3.11 | as above | seed medians at `f` = 0 | 448 | nominal | at `f` = 0 generation degrades smoothly with **no geometric event at all**, and curvature is blind to it. The full table is §6.3's; this section restates the pair |
| **take the negative weights away and the switch, and the explanation resting on it, both disappear** | why this is consistent with the map argument rather than a contradiction of it | T0 §3.11, §3.9 | as above | not applicable | 448 | nominal | the switch **is** a sign-composition phenomenon, and **a non-negative matrix has no dominant negative eigenvalue to flip** |
| not geometry, not the locator (`sigma_eff` = **0.014** for ER, on the descending branch), not memory (**11.43** against **2.42** MC with **0.81** against **1.18** VPT at sigma = 6) | the three candidates already ruled out | T0 §3.10, §3.11 | as above; `e03_frontier_scale_448.parquet` | seed medians at `f` = 0 | 448 | nominal | **named as an open question, not a fourth guess.** Every ratio travels with both levels |
| what is **inference** in the unifying account: that a single leading-eigenvalue account generates both readouts | the status of contribution 2's mechanism | T0 §3.9 | not applicable | not applicable | 448 | not applicable | **consistent with everything measured, not yet a derivation.** The chapter says so in its own voice rather than leaving a reader to discover it |
| `sigma*bulk95` matches the **linear operator**, not the dynamics: realised gain **0.542** (connectome) against **0.690** (Erdős–Rényi) at each variant's `sigma_eff` fold | a limit on the matched axis that must not be matched away | T0 §6.2 | `e01_sigma_eff_fold_scale_448.csv` | per variant at its own fold | 448 | sigma*bulk95 | this **is part of the mechanism**; "matched effective criticality" must be read narrowly |
| **n = 10 seeds**, Fisher exact **p = 0.033** | the sample carrying the biological half of the prediction claim | T0 §2.3; SPINE open flag 5 | `item2_collapse_loci_scale_448.csv` | seeds, not replicates | 448 | nominal | **the weight it carries relative to its sample is stated in the text.** T0 §6.8: a two-sided Wilcoxon on 10 pairs cannot return below **p = 0.00195**, so **no Holm correction over more than about 25 tests can reach 0.05 at any effect size**; declare the family narrowly and rest on CIs and effect sizes |
| peak `d_eff` is ceiling-limited **at any N** (peak `d_eff/N` **0.971 to 0.999** at N = 1000) | the limit on the memory arm's peak | T0 §6.6 | `n1000_memory_scale_1000.parquet` | maximum over cells | 1000 | both | **no parcellation makes the peak comparison informative.** The chapter reads the decay region and says why |
| whether `bulk95` is the ladder controller is **open**, partially answered: **26%** absorbed at `f` = 0, nearly all by `f` >= 0.2 | the limit on the mechanism test | T0 §6.7, §3.7 | `e03_mechanism_matched_scale_448.csv` | median absolute gap, matched axis | 448 | sigma*bulk95 | a properly powered test needs **more seeds, or a variant pair whose `bulk95` separation is large and stable across scales** |
| the `f` > 0 flip pattern is **not machine-portable** (cross-machine only) | a reproducibility limit on every `f` > 0 statement | T0 §6.4 | `item2_f_extension_scale_448.parquet` | per cell | 448 | both | distributions agree (**60/60** groups within 4 SE); **per-cell values do not**. On the originating machine all **19,200** shared `f` > 0 cells reproduced exactly. Use each file's own `bulk95` when reindexing its cells |
| on the Dale axis, sign fraction and **non-normality co-vary**, unequally across variants | the limit on §6.4's placement paragraph | T0 §6.5 | not applicable | not applicable | 448 | nominal | Dale-arm claims are about **node-wise inhibition, not sign fraction alone** |
| the boundary above the all-replicates coverage edge rests on a **`bulk95`-selected subsample** | the limit on §6.6's figure | T0 §6.10 | `e02_heatmap_boundaries_extension.csv` | contour level over fully covered cells | 448 | sigma*bulk95 | the region is **drawn but should not be read quantitatively** |

## Movement 2: contribution 2 has no out-of-sample test in this thesis

**Stated here rather than left to the discussion.** It is a consequence of a design
decision taken in session 0, before any Mackey-Glass data was inspected, and it is
reported as such.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| **contribution 2 has no out-of-sample test in this thesis** | the statement itself | FL, claim-to-primary-task mapping ("Addition 2"); RM §5; A3P §5 item 12(iii) | not applicable | not applicable | 448 | not applicable | it rests on **F16 plus the joint reading of F7 and F13**. Stated plainly, not papered over |
| the joint claim's primary is **MC + Lorenz jointly**, corroborating **none** | why no task fills the gap | FL, claim-to-primary-task mapping | not applicable | not applicable | 448 | not applicable | declared **before any data was inspected**, which is what stops "there is always a task where it holds" |
| the implemented Mackey-Glass task is **teacher-forced** | why it cannot be the out-of-sample test | FL "Addition 2"; RM §5; PREREG §1.1 | not applicable | not applicable | 448 | not applicable | the reservoir is **re-anchored by the true input every step**, so the regime switch has no consequence for the metric; both branches of the interior-optimum prediction are **uninterpretable rather than merely hard to detect** |
| the original MG pre-registration is **withdrawn on design grounds, before any data was inspected**, and a narrower one registered in its place | the governance record | FL "Addition 2"; PREREG §1.1, §2 | not applicable | not applicable | 448 | not applicable | preserved **verbatim** in `PREREG_MACKEY_GLASS.md` §1.1 with the reason. The replacement prediction is on the **memory** side and corroborates **MC**, not Lorenz |
| closed-loop MG needs **~150 to 250 lines** mirroring the Lorenz protocol, a null-tuned hyperparameter check and **~23 core-hours** | what the missing test would cost | RM §5 | not applicable | not applicable | 448 | not applicable | **deferred work, not a gap that MG's presence in the task list quietly fills** |
| the driven MG data **is still collected in §4b** | the roadmap's statement of the data's status | RM §5; SPINE open flag 4 | not applicable | not applicable | 448 | not applicable | **A3P §5 item 7 says the opposite**: "Mackey-Glass on the human substrate **has never been run**", and PREREG §3 item 1 recorded on 15 August 2026 that **no human MG results existed in the repo**. Carried as a disagreement (`GAPS.md` B19), not resolved, and **no MG data was inspected to settle it** |
| **Mackey-Glass was not inspected** | the inspection status, stated in both act files | A3M §5 item 10; A3P §5 item 11; PREREG §4 is an unwritten placeholder; **T0 does not mention Mackey-Glass anywhere** | not applicable | not applicable | 448 | not applicable | this is the answer to SPINE open flag 4, and it is reported rather than resolved. CONV working rule 6 still binds |

## Forbidden phrasings for this section

- **Letting the `f` > 0 mechanism read as general.** "Capacity is gated by which dynamical
  regime the manifold is in" is a statement about the **`f` > 0 counterfactual**.
- **"the single-axis account explains generation at `f` = 0."** It demonstrably does not,
  and this section is where the thesis says so in its own voice.
- **Offering a fourth candidate** for what sets generation at `f` = 0, or hedging the open
  problem into a suggestion.
- **"the biological cut"** for `f` = 0. `f` = 0 is what the instrument produces; `f` > 0 is
  the missing half of the biology.
- **Implying Mackey-Glass fills the out-of-sample gap**, or that its presence in the task
  list is evidence for contribution 2. Closed-loop MG is **deferred work**.
- **Stating that Mackey-Glass was analysed, or that it was not collected.** What the
  documents support is that it was **not inspected**; whether the human driven grid was
  collected is a disagreement between RM/SPINE and A3P/PREREG.
- **"scale-invariant" full stop**, and any margin quoted without its levels.
- **Treating the map argument as a derivation**, or contribution 2 as tested.
- **Burying any of this in the discussion chapter.** The scope limit and the missing
  out-of-sample test are stated **here**, where the claim they bound was made.
- **"generation tracks trajectory straightness"**, **"`sigma_eff` crosses 1"**, **"hub
  inhibition collapses memory"**, **"compact bulk"**, **"the connectome is a better
  reservoir."**

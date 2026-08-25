# Fact sheet 05: chapter 4 section 5, "What Act I hands to Act II"

**Section:** `report/act1_structure.md` §4, chapter 4 outline **item 7**. One paragraph.
**Claims carried:** none new. It restates two things and names them as objects the next
chapter works on.
**Figures:** none.

`report/CROSS_ACT_SPINE.md`: Act I hands on **`sr_crit` as the criticality scale each
substrate brings with it**, which is what makes the second matching axis available at all,
and **the Perron mode as the object Act II decomposes**.

Source key: **T0** = `TIER0_STATE_OF_PLAY.md`. **SPINE** = `report/CROSS_ACT_SPINE.md`
(canonical for structure, **not** for numbers). **CONV** = `report/CONVENTIONS.md`.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| `sr_crit` **3.078** / **1.922** / **1.873** / **1.807** | the criticality scale each substrate carries with it | T0 §2.1, §3.1 | `eigenspectrum/results/scale_448/spectra_per_seed.parquet` | `1 / median_over_seeds(bulk95)` | 448 | not applicable | this is the **same number** as the gap ratio and as `1/bulk95`; adopting it costs nothing and names the quantity after what it measures |
| the second matching axis exists **because** each substrate brings its own `sr_crit` | what the hand-over licenses | SPINE, Act I "Hands on"; T0 §1.1 for the axis pair | not applicable | not applicable | 448 | both | the handed-over object is what makes `sigma*bulk95` **available**, not what makes it correct. Neither axis is neutral |
| **3.078** as the supercritical threshold applied to every variant | the connectome's own critical point, used as the filter later chapters read | T0 §2.4, §3.2 | `taskB_extended_sweep_scale_448.parquet` | as above | 448 | nominal | it is the **conservative** choice: it samples every null further above its own critical point. T0 §2.4 requires both filters be reported wherever the margin is quoted, so this sentence forward-refers rather than settles |
| the Perron mode, `\|lambda_1\|` **1.78x** Erdős–Rényi's over a bulk that is essentially everyone's | the object Act II decomposes | T0 §3.1 | as above | medians | 448 | not applicable | handed over as an **object to be decomposed**, not as an explanation. Act II measures where each half of the spectrum ends up in the `T x N` state matrix |
| **f = 0** throughout | the sign condition every chapter-4 and chapter-5 number sits at | SPINE, "The primary variable and the intervention" | not applicable | not applicable | 448 and 1000 | not applicable | `f` is **not mentioned before chapter 6 §6.3**, except as a forward reference in the methods paragraph that defines it. `f` = 0 is what the instrument produces, not "the biological cut" |
| **no mechanism** for why placement produces the gap | the limit of what Act I hands over | `report/act1_structure.md` §1, "claims deliberately NOT made" | not applicable | not applicable | 448 | not applicable | the connectome against weight-permuted contrast localises the effect to **placement** and stops there. Act II does not receive an explanation, only an object |

## Forbidden phrasings for this section

- **"Act I explains the gap."** It establishes that weight placement produces it and
  names the limit: placement, not which feature of placement.
- **"the gap keeps the spectrum clear of the floor"** stated here as though Act I had
  shown it. That link is chapter 5 §4, it runs through the common-mode account, and Act I
  hands over an object rather than a chain.
- **"compact bulk", "compressed bulk."**
- **"the connectome is a better reservoir"**, or any anticipation of a task result. No
  task appears in Act I.
- **Introducing `f`** as anything other than a forward reference to chapter 6 §6.3.
- **"the matched axis is the corrected comparison."** `sr_crit` makes the second axis
  available; it does not make it neutral.

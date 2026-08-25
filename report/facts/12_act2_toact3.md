# Fact sheet 12: chapter 5 section 7, "What Act II hands to Act III"

**Section:** `report/act2_manifold.md` §4, **section 7**. One paragraph, and it hands over
**four** things, the fourth being a **boundary rather than a result**.
**Claims carried:** none new.
**Figures:** none.

The four: the **common-mode account**; the **floor account** that makes it spectral and
therefore radius-dependent; **`d_eff`** as the measure, now earned; and **the temporal
axis, stated as flat at `f` = 0**. The fourth is the seam between the two halves of the
thesis and **must not become an appendix sentence**.

Source key: **T0** = `TIER0_STATE_OF_PLAY.md`. **A2** = `report/act2_manifold.md`.
**SPINE** = `report/CROSS_ACT_SPINE.md` (structure only). **FL** =
`report/FIGURE_LIST.md`.

| number as it will appear | quantity it measures | source | artifact path | aggregation convention | scale (N) | axis | required qualifier |
|---|---|---|---|---|---|---|---|
| `\|mean_state\|` **0.759** against **0.949 to 0.989** at sigma = 6 | the common-mode account, restated as what is handed over | T0 §3.7 | `saturation_diagnostics.parquet` | **absolute value per seed, then seed median** | 448 | nominal | with its sigma. Act III's memory arm turns this into a mechanism |
| `d_eff` **412.9** against **74.8** | the floor account's headline, restated | T0 §3.6 | `covariance_spectra.parquet` | median over 50 supercritical cells | 448 | nominal | handed over as **radius-dependent**: not a fixed property of a substrate but a property of a substrate **at an operating point**, which is what lets Act III read the same axis twice |
| **0.261 rad** (connectome) and **0.263 rad** (Erdős–Rényi) | Lorenz seed-median curvature across the whole sigma = 0 to 6 sweep at `f` = 0 | **Not in T0.** A2 §1 ("claims deliberately NOT made") and §5 item 15 only | this act's own Probe 1 capture (36,540 cells) | seed median, `f` = 0, all-positive, over the whole sweep | 448 | nominal | **maximum 0.26 for both**: the metric is a **constant at Act II's operating point** and there is nothing to draw. This is T0 §3.11's scope limit confirmed on an independent capture. Stated as a **boundary**, not as a result |
| connectome curvature **0.26 / 0.26 / 0.26 / 0.26 / 0.26** at sigma = 2, 4, 6, 8, 11.2, with VPT **4.43 / 2.81 / 0.81 / 1.18 / 0.44** | the same flatness in T0's own table, on the Jacobian capture | T0 §3.11 | `e01_jacobian_scale_448.parquet` | seed medians at `f` = 0 | 448 | nominal | **the geometry is flat across the entire sweep while prediction falls ~10x.** Erdős–Rényi reads 0.26 / 0.26 / 0.26 / 0.27 / **1.70** and VPT 3.73 / 2.45 / 1.18 / 0.49 / 0.23. This is the TIER0-backed twin of the row above, on a different capture and a different sigma grid |
| **0.82%** (Lorenz), **49.6%** (MC), **45.0%** (NARMA-10) | share of cells in the "between" band [0.6, 2.2] rad | **Not in T0.** A2 §1 and §5 item 15 only | this act's Probe 1 capture; n = 12,180 Lorenz cells | share of cells | 448 | nominal | **the qualifier that stops bimodality being stated as a property of the manifold.** Curvature is a property of the manifold **and the input driving it**: Lorenz is a smooth low-dimensional signal, whereas white-noise-driven MC turns sharply at every step. F12 states the bimodality **on Lorenz** and is right to; a general statement would not be |
| **0.56%** of **38,280** Lorenz cells (215 cells in [0.6, 2.2] rad) | the same bimodality on E0.1's Jacobian capture | T0 §3.10; FL F12 row | `e01_jacobian_scale_448.parquet` | share of cells | 448 | nominal | **a different population**, not a disagreement with the 0.82%: this act's 58-sigma grid against E0.1's Jacobian capture. Both are Lorenz-only |
| **36,540 cells** | the size of this act's Probe 1 capture | **Not in T0.** A2 §5 item 15 only | Probe 1 capture | not applicable | 448 | nominal | quoted with the 0.261 / 0.263 and the band shares, since they are all read off it |
| `sr_crit` as the scale, `d_eff` as the measure | what Act III inherits | SPINE, Act II "Hands on"; T0 §2.1, §3.12(3) | not applicable | not applicable | 448 | not applicable | `d_eff` is handed over **now earned rather than assumed**, which is why section 2 defines it and section 5 justifies it |
| **f = 0** throughout, `f` enters in chapter 6 §6.3 | the scope of everything handed over | SPINE, "The primary variable and the intervention" | not applicable | not applicable | 448 | nominal | `f` is an **intervention, not a peer** of sigma, and it appears in exactly one place. **`f` = 0 is what the instrument produces, not "the biological cut"** |

## Forbidden phrasings for this section

- **Bimodality stated as task-independent**, or as a property of the manifold. It is
  Lorenz-specific: on the two noise-driven tasks roughly half the cells sit in the band
  Lorenz leaves empty (49.6% and 45.0% against 0.82%).
- **Any graded curvature or trajectory-straightness account.** "generation tracks
  trajectory straightness" is withdrawn; write "capacity is gated by which dynamical
  regime the manifold is in", and **only of `f` > 0**.
- **"the manifold has been fully characterised."** Act II measured both axes and reports
  the spatial one because the temporal one does not move here. A reader who finishes the
  chapter believing otherwise would read chapter 6 as a reversal instead of as a boundary
  they were warned about.
- **Putting the temporal-axis paragraph in an appendix**, or reducing it to a sentence. It
  is the seam between the two halves of the thesis and belongs at the end of chapter 5.
- **"curvature is flat, so geometry does not matter."** At `f` = 0 capacity is lost **with
  the geometry intact**; what sets generation at `f` = 0 is a **named open question**, and
  memory does not answer it either.
- **"`sigma_eff` crosses 1 at the transition."** The criterion is falsified; `sigma_eff`
  survives as the best empirical **locator** only, it is Lorenz-only, and it must not cross
  panels.
- **"the connectome is a better reservoir."** It is not, at the peak; the advantage is
  supercritical robustness.
- **"the manifold lives in low-frequency graph harmonics."**
- **"compact bulk", "compressed bulk."**

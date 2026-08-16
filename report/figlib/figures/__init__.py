"""The figure registry. One entry per figure on ``report/FIGURE_LIST.md``.

**No figure exists outside this registry**, and none outside `FIGURE_LIST.md`. The
builders live one module per act, which is also one module per sweep session:

===================== ========= ================================================
``act1_structure``    session 1 F1, F2, F3, S1   (chapters 3 and 4)
``act2_manifold``     session 2 F4, F5, F6       (chapter 5)
``act3_memory``       session 3 F7, F9-F11       (chapter 6, memory arm)
``act3_prediction``   session 4 F12-F14, F16     (chapter 6, prediction arm)
``act4_anchor``       --        F15              (chapter 7)
===================== ========= ================================================

Split out of a single 1006-line ``figures.py`` on 16 August 2026, along the section
banners that module already carried; the move was verified byte-identical on all 16
rendered figures. A figure's **act** decides its module, not its chapter: F3 prints in
chapter 3 but is Act I's argument and Session 1's to render, and F16 prints in chapter 6
but needs both Act III arms so Session 4 renders it. `FIGURE_LIST` is canonical for both
the chapter and the owning session.

The public names are unchanged (``FIGURES``, ``SUPPLEMENTARY``, ``ALL_FIGURES``,
``WORKSHOP``), so ``from report.figlib.figures import FIGURES`` still resolves.
"""

from report.figlib.figures.act1_structure import (
    f1_spectrum, f2_gap_not_bulk, f3_two_axes, s1_spectrum_n1000)
from report.figlib.figures.act2_manifold import (
    f4_perron_carries_the_mean, f5_sign_selects_the_basis,
    f6_pr_misses_readout_structure)
from report.figlib.figures.act3_memory import (
    f7_the_crossing, f9_scale_invariance, f10_peak_parity, f11_perron_rescue)
from report.figlib.figures.act3_prediction import (
    f12_curvature_is_bimodal, f13_generation_as_vpt, f14_sigma_eff_is_a_locator,
    f16_phase_boundaries)
from report.figlib.figures.act4_anchor import f15_yeo_loads_the_perron_mode

# =============================================================================
# Registry -- the 15 rendered main-text figures. F8 is retired into F3.
# =============================================================================
FIGURES = {
    "F1": (4, "spectrum: a large real Perron root over everyone's bulk", f1_spectrum),
    "F2": (4, "gap not bulk, at both N", f2_gap_not_bulk),
    "F3": (3, "neither matching axis is neutral", f3_two_axes),
    "F4": (5, "the Perron mode carries the mean", f4_perron_carries_the_mean),
    "F5": (5, "sign selects the basis", f5_sign_selects_the_basis),
    "F6": (5, "PR misses readout-relevant structure", f6_pr_misses_readout_structure),
    "F7": (6, "the crossing: peaks lowest, retains most", f7_the_crossing),
    "F9": (6, "the supercritical margin is scale-invariant", f9_scale_invariance),
    "F10": (6, "peak parity, with CIs", f10_peak_parity),
    "F11": (6, "rescue from Perron domination", f11_perron_rescue),
    "F12": (6, "curvature is bimodal", f12_curvature_is_bimodal),
    "F13": (6, "generation read as VPT", f13_generation_as_vpt),
    "F14": (6, "sigma_eff as locator, not criterion", f14_sigma_eff_is_a_locator),
    "F15": (7, "which Yeo networks load the Perron mode", f15_yeo_loads_the_perron_mode),
    "F16": (6, "the crossing, with its axis and its coverage", f16_phase_boundaries),
}

# The workshop subset (5pp, ~4 figures), marked W on FIGURE_LIST.md. F16 is the first
# reserve if a fifth slot appears.
WORKSHOP = ("F1", "F2", "F7", "F12")

# Cap raised from 14 to 15 in session 0 to give contribution 2 a figure of its own.
# This assertion is why the registry lives here rather than one dict per act module: a
# per-module registry merged at import time could be grown a figure at a time without
# anything noticing, which is exactly the drift FIGURE_LIST's cap exists to prevent.
assert len(FIGURES) == 15, f"cap is 15 figures, registry holds {len(FIGURES)}"

# ---------------------------------------------------------------------------------
# Supplementary figures -- appendix only, NOT part of the numbered main-text list.
#
# Separate namespace on purpose. `FIGURE_LIST.md` caps the main text at 15 and the
# assertion above enforces it; a scale replicate of an existing figure is not a new
# claim and must not consume a main-text slot or quietly raise that cap. The rule that
# no figure exists outside `FIGURE_LIST.md` still binds, so S-figures are listed there
# in their own section.
#
# The bar for an S-figure: it makes NO claim the main text does not already make, and
# it is built by an EXISTING builder at different parameters. Anything that needs its
# own builder is a new figure and goes through the cap.
SUPPLEMENTARY = {
    "S1": (None, "F1 at N = 1000 (appendix scale replicate)", s1_spectrum_n1000),
}
for _id, (_chapter, _name, _builder) in SUPPLEMENTARY.items():
    assert _id.startswith("S") and _id not in FIGURES, (
        f"{_id}: supplementary IDs are S-prefixed and must not collide with the "
        "numbered main-text list.")

# What the entry point renders. FIGURES stays the cap-checked main-text list.
ALL_FIGURES = {**FIGURES, **SUPPLEMENTARY}

"""The figure registry. One entry per figure on ``report/FIGURE_LIST.md``.

**No figure exists outside this registry**, and none outside `FIGURE_LIST.md`. The
builders live one module per act, which is also one module per sweep session:

===================== ========= ================================================
``act1_structure``    session 1 F1, F2, F3, F19, S1, S3, S4  (chapters 3 and 4)
``act2_manifold``     session 2 F4, F5, F6       (chapter 5)
``act3_memory``       session 3 F7, F9-F11       (chapter 6, memory arm)
``act3_prediction``   session 4 F12-F14, F16, F17, S2 (chapter 6; S2 prints in 5)
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
    f1_spectrum, f2_gap_not_bulk, f3_two_axes, f19_substrates_as_graphs,
    s1_spectrum_n1000, s3_weight_against_degree_product,
    s4_full_substrate_family)
from report.figlib.figures.act2_manifold import (
    f4_perron_carries_the_mean, f5_sign_selects_the_basis,
    f6_pr_misses_readout_structure, f18_gram_spectrum_against_the_floor)
from report.figlib.figures.act3_memory import (
    f7_the_crossing, f9_scale_invariance, f10_peak_parity, f11_perron_rescue)
from report.figlib.figures.act3_prediction import (
    f12_curvature_is_bimodal, f13_generation_as_vpt, f14_sigma_eff_is_a_locator,
    f16_phase_boundaries, f17_free_run_attractors, s2_curvature_regimes)
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
    "F17": (6, "the free-running attractor, and how it fails", f17_free_run_attractors),
    "F18": (5, "the Gram spectrum against the ridge floor",
            f18_gram_spectrum_against_the_floor),
    "F19": (4, "the four substrates, as graphs", f19_substrates_as_graphs),
}

# The workshop subset (5pp, ~4 figures), marked W on FIGURE_LIST.md. F16 is the first
# reserve if a fifth slot appears.
WORKSHOP = ("F1", "F2", "F7", "F12")

# **The cap is now a soft count, and this assertion records the count rather than
# enforcing a ceiling.** Raised from 14 to 15 in session 0 (contribution 2 needed a
# figure of its own), and from 15 to 16 in session 4 on the author's decision of
# 19 August 2026, which replaced the old "one slot, first past the post" rule for E1 and
# E2 with "build both, place each on what it turns out to show". F17 is E2: the
# free-running rollout, which no other artifact in the repository captures, carrying a
# pre-registered claim whose second clause it refutes. It is evidence, not an
# illustration, so it takes a main-text slot.
#
# The assertion stays for the reason it was written: a per-module registry merged at
# import time could be grown a figure at a time without anything noticing, and this is
# the one place a session must edit -- and therefore justify -- to add one. What changed
# is that the number is a fact to keep true, not a gate to argue past.
#
# **16 to 17 on 24 August 2026, for F18.** `CROSS_ACT_SPINE.md` makes the Gram spectrum's
# position relative to the ridge floor step 3 of the causal chain -- the link between the
# common-mode account and `d_eff` -- and chapter 5's outline commits to a section on it.
# The result was recorded in `TIER0` §3.6 under a REJECTED anisotropy hypothesis and had
# never been drawn, so the chain's middle link was the one step with no figure.
# `report/checks/floor_sensitivity_check.md` verified all sixteen published cells against
# the frozen artifacts first and found the four-variant, sigma-resolved coverage already
# in `covariance_spectra.parquet`, so F18 needed no run. It is Act II's own claim and
# session 2's module, but session 2 closed on 17 August; `FIGURE_LIST` names this
# session as its owner explicitly, which is the F3 and F16 arrangement.
#
# **17 to 18 on 1 September 2026, for F19.** Chapter 4's first section sets out the four
# substrates and what each preserves, and had only a preservation table to do it with:
# the chapter described the ladder in prose and drew it nowhere, so a reader met the
# weight-permuted control as a sentence rather than as a picture of the connectome's own
# graph. F19 draws all four as matrices under one node ordering, with the four
# binary-graph statistics beneath. It is Act I's own figure and Act I's module. **It
# carries no contribution and makes no claim**: it prints in the section
# `act1_structure.md` registers as having no results, and its statistics strip is a set
# of design facts about four graphs. Its source parquets did not exist and were built
# for it by `report/artifacts/build_substrate_graphs.py`, whose reproduction gate --
# connectome against control, byte-identical binary adjacency and exact equality on all
# four statistics -- runs before anything is written.
assert len(FIGURES) == 18, f"registry holds {len(FIGURES)} figures, not 18"

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
    # S2 is E1. It makes no claim the main text does not already make -- curvature is
    # bimodal is F12's claim -- so it is supplementary; but it needs its own builder,
    # which the original S-figure bar forbade. Session 4 amended that bar (see
    # `FIGURE_LIST.md`): "no new claim" is the test that matters, and "an existing
    # builder at different parameters" was a proxy for it that excluded the one thing a
    # supplementary figure is most useful for -- supplying intuition for a claim the main
    # text asserts. It prints in chapter 5, where the manifold is decomposed.
    "S2": (None, "the two curvature regimes made visible (chapter 5)",
           s2_curvature_regimes),
    # S3 is the pre-registered placement-mechanism test, drawn where it fails. It clears
    # the bar because it makes NO claim the main text does not already make: the register
    # is unchanged, the verdict on `PREREG_PLACEMENT_MECHANISM.md` was EQUIVOCAL, and A1.5
    # still says placement with no mechanism attached. What the panel adds is a NEGATIVE
    # result put where the claim it bounds is made (`CONVENTIONS`, working rule 8) --
    # the registered prediction was a positive weight-against-degree-product correlation
    # and the connectome's is negative. Its numbers are `TIER0` 3.14(b). Act I's own
    # measurement and Act I's module.
    #
    # **One panel, and the other two of the sketch are deliberately not built.** The
    # masking curve was posed as a fraction of each cell's own `|lambda_1|`, which divides
    # by the one quantity the substrates differ in and is not interpretable as posed
    # (`TIER0` 3.14(d)); the strength sandwich would give a figure to an account `TIER0`
    # 3.14(c) records as untested, which is the post-hoc move the registration exists to
    # prevent. Neither is a layout problem and neither is to be revisited by looking
    # harder: the prereg's 3 fixes one session and no second analysis.
    "S3": (None, "the registered placement prediction, refuted (appendix)",
           s3_weight_against_degree_product),
    # S4 is F19 widened from the ladder's four substrates to the family of seven. It
    # clears the bar on both clauses: it makes NO claim the main text does not already
    # make -- it makes no claim at all, as F19 does not -- and it is the existing
    # substrate builder at different parameters, which is the clause S2 had to amend.
    # It prints in the appendix, beside `tab:act1-offladder`, because that is where the
    # three off-ladder rungs are on the record.
    #
    # **Drawing seven substrates does not widen the ladder.** TIER0 3.1(b)'s scope guard
    # holds over it: no comparison is made, no spectral quantity is quoted, no statistics
    # strip is drawn, and nothing is recomputed across the wider set.
    # `substrate_topology.parquet` and TIER0 3.13 are the four-substrate ladder's and are
    # untouched.
    #
    # **It reads a source of its own, and that is the point.** F19 takes its columns from
    # `edges.variant.unique()`, so adding the three rungs to `substrate_edges.parquet`
    # would have silently widened a four-column figure to seven. The build script writes
    # `substrate_edges_full.parquet` as a second output instead, asserting that the four
    # ladder variants come through it unchanged; F19 still reads the four-variant file
    # and re-renders byte-identical.
    "S4": (None, "the full substrate family, as graphs (appendix)",
           s4_full_substrate_family),
}
for _id, (_chapter, _name, _builder) in SUPPLEMENTARY.items():
    assert _id.startswith("S") and _id not in FIGURES, (
        f"{_id}: supplementary IDs are S-prefixed and must not collide with the "
        "numbered main-text list.")

# What the entry point renders. FIGURES stays the cap-checked main-text list.
ALL_FIGURES = {**FIGURES, **SUPPLEMENTARY}

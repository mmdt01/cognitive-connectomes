"""Illustrative methods figure: the design-Gram spectrum against the ridge floor.

**Not a results figure.** It carries no claim, is not on ``FIGURE_LIST.md`` and is not
registered in ``report/figlib``. It exists to show a chapter-5 reader where two
substrates' design-Gram spectra fall relative to the ridge floor ``alpha``, and how many
directions each therefore holds clear of it -- the quantity ``d_eff`` sums.

Both spectra are drawn in their contract colours. The Erdos-Renyi region between its
spectrum and the floor is washed in its own green, and each substrate's floor crossing is
dropped to the axis as a dotted vertical in its own colour. Neither count is printed on
the panel; the caption carries them.

Read-only on the data. The parquet is hashed before and after and the two are asserted
equal, and a four-part reproduction gate against the published scalars in
``report/act2_manifold.md`` A2.4 runs before anything is drawn. A failed gate prints and
exits without writing a figure.

    python report/scratch/illustration_gram_floor.py
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_REPO_ROOT = Path(__file__).resolve().parents[2]
PARQUET = (_REPO_ROOT / "experiments/human/analysis/results/scale_448"
           / "covariance_spectra.parquet")
FIGURE_ID = "illustration_gram_floor"

# The cell F6(a) draws, pinned by report/act2_manifold.md A2.4 and by the rule in
# report/figlib/sources._gram_spectra. Nothing here is chosen by hand.
TASK, CONDITION, VARIANT, REFERENCE = "mc", "human_empirical", "connectome", "erdos_renyi"
SPECTRAL_RADIUS, ALPHA = 3.0526, 1e-6

SPAN_Y = -0.135      # axes fractions: where the range arrows sit below the axis

# The published scalars the gate reproduces (report/act2_manifold.md A2.4, TIER0 §3.12).
PUBLISHED = dict(n_directions=448, d_eff=431, n_above_half=438, n_total=448, pr=1.28)


def _load_style():
    """Import ``report/figlib/style.py`` read-only, without the package ``__init__``.

    Loading it as ``report.figlib.style`` would execute the package ``__init__``, which
    pulls in the builder registry and the source loaders. This figure needs the style
    contract and nothing else, so it takes the module on its own.
    """
    path = _REPO_ROOT / "report" / "figlib" / "style.py"
    spec = importlib.util.spec_from_file_location("_figlib_style", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def select_cell(frame: pd.DataFrame, variant: str) -> tuple:
    """The seed whose ``d_eff`` is nearest the median of the ten, at the pinned cell.

    ``d_eff = sum_i g_i / (g_i + alpha)``. With ten seeds the median falls between the
    fifth and sixth, so *both* of them sit exactly ``(sixth - fifth) / 2`` from it and
    the rule is always a two-way tie. It is broken the way the published source breaks
    it -- ``idxmin`` takes the first row attaining the minimum, in the parquet's own
    seed-ascending order -- so this selects the same cell F6(a) draws. The gate below is
    what actually proves that, since the two tied seeds have different ``d_eff``.
    """
    cell_rows = frame[(frame.task == TASK) & (frame.condition == CONDITION)
                      & (frame.variant == variant) & (frame.alpha == ALPHA)
                      & np.isclose(frame.spectral_radius, SPECTRAL_RADIUS)]
    d_eff = cell_rows.eig_gram.map(
        lambda g: float((np.asarray(g, float) / (np.asarray(g, float) + ALPHA)).sum()))
    cell = cell_rows.loc[(d_eff - d_eff.median()).abs().idxmin()]
    return cell, d_eff


def run_gate(cell, d_eff_all) -> bool:
    """The four checks of step 1. Returns True only if every one passes."""
    g = np.asarray(cell.eig_gram, float)
    verdicts = []

    ok_a = (g.size == PUBLISHED["n_directions"] and not np.isnan(g).any()
            and bool((g >= 0).all()))
    verdicts.append(("a  eig_gram well-formed",
                     f"length {g.size}, {int(np.isnan(g).sum())} NaN, min {g.min():.3e}",
                     f"length {PUBLISHED['n_directions']}, 0 NaN, non-negative", ok_a))

    d_eff = float((g / (g + ALPHA)).sum())
    ok_b = round(d_eff) == PUBLISHED["d_eff"]
    verdicts.append(("b  d_eff", f"{d_eff:.4f} -> {round(d_eff)}",
                     str(PUBLISHED["d_eff"]), ok_b))

    n_above = int(((g / (g + ALPHA)) > 0.5).sum())
    ok_c = n_above == PUBLISHED["n_above_half"]
    verdicts.append(("c  directions with ridge weight > 0.5",
                     f"{n_above} of {g.size}",
                     f"{PUBLISHED['n_above_half']} of {PUBLISHED['n_total']}", ok_c))

    eig_cov = np.asarray(cell.eig_cov, float)
    pr = float(eig_cov.sum() ** 2 / np.sum(eig_cov ** 2))
    ok_d = round(pr, 2) == PUBLISHED["pr"]
    verdicts.append(("d  participation ratio", f"{pr:.6f} -> {round(pr, 2):.2f}",
                     f"{PUBLISHED['pr']:.2f}", ok_d))

    print("\nSTEP 1 - reproduction gate")
    for name, recomputed, published, ok in verdicts:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:38s} "
              f"recomputed {recomputed:44s} published {published}")
    if not all(ok for *_, ok in verdicts):
        print("\nGATE FAILED - no figure written.")
        return False
    return True


def build(style, cells) -> tuple:
    """Draw the four-rung ladder against the ridge floor. ``cells`` is variant -> row."""
    import matplotlib.pyplot as plt
    from matplotlib.ticker import LogLocator

    spectra = {v: np.asarray(cells[v].eig_gram, float) for v in cells}
    g, g_ref = spectra[VARIANT], spectra[REFERENCE]   # already rank-ordered, descending
    rank = np.arange(1, g.size + 1)

    y_low, y_high = 1e-13, 5e6
    fig, ax = plt.subplots(figsize=(5.6, 3.5))
    ax.set_yscale("log")
    ax.set_xlim(-4, g.size + 5)
    ax.set_ylim(y_low, y_high)

    green = style.VARIANT_COLOUR[REFERENCE]

    # The region below the Erdos-Renyi spectrum and above the ridge floor, in a light
    # wash of that substrate's own green. It pinches shut exactly where the spectrum
    # meets the floor, so the wash *is* the set of directions Erdos-Renyi holds clear of
    # it. ``interpolate=True`` closes it on the crossing rather than on the last whole
    # direction above it.
    ax.fill_between(rank, ALPHA, g_ref, where=g_ref > ALPHA, interpolate=True,
                    color=green, alpha=0.18, lw=0, zorder=1)

    ax.axhline(ALPHA, color=style.ANNOTATION_ACCENT, lw=1.0, ls="--", zorder=2)
    # Hard against the left edge, just above the floor. Every spectrum is orders of
    # magnitude higher at these ranks, so nothing crosses the label; it sits on the pale
    # green wash and nothing else. The gap between the floor and the connectome further
    # right looks roomier but is under one line tall by rank 410, which is what put this
    # label back on the left.
    ax.text(8, ALPHA * 1.7, r"ridge floor, $\alpha$", color=style.ANNOTATION_ACCENT,
            fontsize=style.TICK_SIZE, ha="left", va="bottom", zorder=7)

    # Every rung in its contract colour and width, so a substrate reads the same here as
    # in every other figure. Two deliberate departures from `variant_kwargs`: every line
    # is solid, and the legend takes the plain `VARIANT_TITLE` names rather than the
    # rung-numbered `VARIANT_LABEL` ones, because this panel contrasts the substrates
    # themselves and not their position on the null ladder. Dropping the dashes costs the
    # redundant greyscale encoding; Okabe-Ito still separates these four by luminance.
    # Plotted in the contract's legend order, with z-order set separately: the connectome
    # is the gated cell and sits on top, Erdos-Renyi is the annotated one just under it.
    depth = {"connectome": 6, "erdos_renyi": 5,
             "connectome_weight_permuted": 4, "degree_rewire": 3}
    for variant in style.ordered_variants(cells):
        ax.plot(rank, spectra[variant], zorder=depth[variant],
                **style.variant_kwargs(variant, ls="-",
                                       label=style.VARIANT_TITLE[variant]))

    # Where each spectrum crosses the floor. Interpolated in log g rather than rounded to
    # the last whole direction above it, because the axis is logarithmic and the count is
    # read off position. Only the gated cell and the annotated one are drawn down to the
    # axis; four verticals would be four counts to hold at once.
    crossings, marked = {}, (VARIANT, REFERENCE)
    for variant in style.ordered_variants(cells):
        spectrum = spectra[variant]
        # Exact zeros are dropped first: degree_rewire's Gram carries one at rank 448,
        # and log10(0) would both warn and put an inf in the interpolation table. They
        # are far below the floor either way, so the crossing is untouched.
        positive = spectrum > 0
        # -log10(spectrum) is increasing, which is what np.interp needs.
        crossing = float(np.interp(-np.log10(ALPHA), -np.log10(spectrum[positive]),
                                   rank[positive]))
        crossings[variant] = (crossing, int((spectrum > ALPHA).sum()))
        if variant in marked:
            ax.plot([crossing, crossing], [y_low, ALPHA], lw=1.0, ls=":", zorder=7,
                    color=style.VARIANT_COLOUR[variant], solid_capstyle="butt")

    style.legend(ax, loc="upper right", handlelength=2.2, borderaxespad=0.4)

    # The two ranges, below the axis: what Erdos-Renyi holds clear of the floor and what
    # it loses to it, split at its own crossing. Both are **Erdos-Renyi's**, so both are
    # drawn in its green -- the other rungs' crossings are not spanned, or the reader has
    # four sets of ranges to hold.
    #
    # x in data coordinates, y in axes fractions, via ``get_xaxis_transform``, so the
    # spans keep their vertical position under the tick labels whatever the y limits do.
    # ``annotation_clip=False`` is what lets them draw outside the axes at all.
    below = ax.get_xaxis_transform()
    er_crossing = crossings[REFERENCE][0]
    for text, left, right in (("counted by $d_{\\rm eff}$", 1.0, er_crossing),
                              ("suppressed by the ridge", er_crossing, float(g.size))):
        ax.annotate("", xy=(left, SPAN_Y), xytext=(right, SPAN_Y),
                    xycoords=below, textcoords=below, annotation_clip=False,
                    arrowprops=dict(arrowstyle="<->", color=green, lw=0.9,
                                    shrinkA=0, shrinkB=0))
        ax.text((left + right) / 2.0, SPAN_Y - 0.055, text, transform=below,
                color=green, fontsize=style.TICK_SIZE, ha="center", va="top")

    # labelpad clears the spans and their labels, so the axis title sits below both.
    ax.set_xlabel("direction index, ordered largest to smallest", labelpad=46)
    ax.set_ylabel(r"Gram eigenvalue  $g_i$  (log scale)")
    ax.set_xticks([1, 100, 200, 300, 400, g.size])
    ax.yaxis.set_major_locator(LogLocator(base=10.0, numticks=8))
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=(), numticks=8))

    return fig, spectra, crossings


def main() -> int:
    style = _load_style()
    style.apply_rcparams()

    for name in (FIGURE_ID + ".png", FIGURE_ID + ".pdf"):
        target = _REPO_ROOT / "report" / "figures" / name
        if target.exists():
            print(f"STOP: {target} already exists; refusing to overwrite.")
            return 2

    print(f"parquet : {PARQUET}")
    print(f"size    : {PARQUET.stat().st_size} bytes")
    hash_before = sha256(PARQUET)
    print(f"sha256 before : {hash_before}")

    frame = pd.read_parquet(PARQUET)
    # Every rung of the criticality-matched ladder, each by the same median rule.
    cells, d_effs = {}, {}
    for variant in style.LADDER:
        cells[variant], d_effs[variant] = select_cell(frame, variant)
    print("\nselected seeds (nearest-the-median rule, same filter for every rung)")
    for variant in style.ordered_variants(cells):
        series = d_effs[variant]
        print(f"  {variant:27s} seed {int(cells[variant].seed)}   "
              f"d_eff {series.loc[cells[variant].name]:8.4f}   "
              f"median of ten {series.median():8.4f}")

    if not run_gate(cells[VARIANT], d_effs[VARIANT]):
        return 1

    fig, spectra, crossings = build(style, cells)
    written = style.save(fig, FIGURE_ID)

    print("\nSTEP 2 - spectrum span, and where each rung meets the floor")
    for variant, (crossing, count) in crossings.items():
        spectrum = spectra[variant]
        print(f"  {variant:27s} min {spectrum.min():.6e}  max {spectrum.max():.6e}  "
              f"crosses alpha at rank {crossing:7.2f}  above the floor: {count}")

    hash_after = sha256(PARQUET)
    print("\nSTEP 3 - integrity")
    print(f"  sha256 before : {hash_before}")
    print(f"  sha256 after  : {hash_after}")
    assert hash_before == hash_after, "the parquet changed while it was being read"
    print("  unchanged     : True")
    print("\nwritten:")
    for path in written:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

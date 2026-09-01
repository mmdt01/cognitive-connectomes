"""Scratch: the four substrates' binary adjacency as four flat colour blocks.

**Not a thesis figure.** It carries no claim, is not on ``FIGURE_LIST.md``, has no
builder in ``report/figlib`` and touches no artifact, register or TIER0 section. It
exists to give a slide a schematic of the ladder: four 448 x 448 binary matrices, one
per substrate, each in that substrate's own contract colour, with nothing on the panel
but a border in that same colour -- no axes, no ticks, no colourbar, no marginals, no
statistics.

Everything load-bearing is borrowed rather than restated. The edge list, the drawn seed,
the node ordering and the symmetrise-and-permute step are F19's own
(``act1_structure._drawn_seed`` / ``_adjacency``, source ``substrate_edges`` at
``condition = human_empirical``, ``N = 448``), so these blocks are the same four matrices
F19 draws in its (a-d) row, at the same seed and under the same ordering. The colours are
``style.VARIANT_COLOUR`` and the titles ``style.VARIANT_TITLE``.

Two renders, same matrices:

* ``substrates_binary_normal.png``   -- panel transparent, connections in the colour.
* ``substrates_binary_inverted.png`` -- panel in the substrate colour, connections white.

Read-only on the data; writes only the two PNGs beside this file.

    python report/scratch/substrates_binary_blocks.py [--span N]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from matplotlib.colors import ListedColormap, to_rgb

_REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO_ROOT))

import matplotlib.pyplot as plt                                    # noqa: E402
from report.figlib import style                                    # noqa: E402
from report.figlib.sources import Context                          # noqa: E402
from report.figlib.figures.common import N_NODES                   # noqa: E402
from report.figlib.figures.act1_structure import (                 # noqa: E402
    _adjacency, _drawn_seed)

OUT_DIR = Path(__file__).resolve().parent
TRANSPARENT = (0.0, 0.0, 0.0, 0.0)

# How many cells wide each edge is DRAWN. At 5.32% density one edge is one cell in 448,
# which lands at roughly one pixel once the panel is on a slide and antialiases into a
# pale wash -- the whole panel reads faint even though every mark is fully opaque. Two
# cells is a mark-size choice, the same kind a scatter plot makes: the number of marks is
# still exactly the edge count and no cell gains an edge it does not have, but the ink
# fraction rises from 5.3% to about 18% and the panel reads at slide scale. It does
# inflate APPARENT density, so this is a schematic and not a picture to measure off.
MARK_SPAN = 2
BORDER_WIDTH = 1.8


def substrates():
    """F19's four binary matrices: same seed, same node ordering, same edge list."""
    ctx = Context()
    edges = ctx.frame("substrate_edges")
    ordering = ctx.frame("substrate_order").sort_values("position")
    spectra = ctx.frame("spectra_448")
    order = ordering.node.to_numpy(int)
    variants = style.ordered_variants(edges.variant.unique())
    return {v: _adjacency(edges, v, _drawn_seed(edges, spectra, v), order) > 0
            for v in variants}


def thicken(matrix, span: int):
    """Draw each edge as a ``span`` x ``span`` block of cells instead of one cell.

    A centred dilation, so the drawn matrix stays symmetric, and padded rather than
    rolled so nothing wraps from one edge of the panel to the other.
    """
    if span <= 1:
        return matrix
    n, pad = matrix.shape[0], span
    padded = np.pad(matrix, pad)
    out = np.zeros_like(matrix)
    for dx in range(span):
        for dy in range(span):
            sx, sy = dx - span // 2, dy - span // 2
            out |= padded[pad - sx:pad - sx + n, pad - sy:pad - sy + n]
    return out


def render(binary, inverted: bool, filename: str, span: int) -> Path:
    """Four panels in a row, one flat two-colour image each, nothing else."""
    fig, axes = plt.subplots(1, len(binary), figsize=(11.0, 3.0))
    for ax, (variant, matrix) in zip(np.atleast_1d(axes), binary.items()):
        colour = to_rgb(style.VARIANT_COLOUR[variant])
        # Index 0 is the empty cell, index 1 the edge. Inverted paints the panel in the
        # substrate colour and cuts the edges out in white; normal leaves the empty
        # cells fully transparent so the panel drops onto any slide background.
        cmap = ListedColormap([colour, (1.0, 1.0, 1.0, 1.0)] if inverted
                              else [TRANSPARENT, colour])
        ax.imshow(thicken(matrix, span).astype(float), cmap=cmap, vmin=0, vmax=1,
                  interpolation="nearest", rasterized=True)
        ax.set_title(style.VARIANT_TITLE[variant], fontsize=style.TITLE_SIZE + 1,
                     color=style.VARIANT_COLOUR[variant], pad=6)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        # The border, in the panel's own substrate colour. rcParams drops the top and
        # right spines for line plots, so all four are re-enabled here. On the inverted
        # render it sits on a panel of the same colour and is invisible by construction;
        # it is drawn anyway so the two renders are the same figure.
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(BORDER_WIDTH)
            spine.set_color(style.VARIANT_COLOUR[variant])
    fig.subplots_adjust(left=0.01, right=0.99, top=0.90, bottom=0.02, wspace=0.06)
    path = OUT_DIR / filename
    # `transparent=True` clears the canvas around and between the panels in both
    # renders. In the inverted render the connections stay opaque white, because there
    # they are the drawn thing rather than the background.
    fig.savefig(path, dpi=style.DPI, transparent=True, bbox_inches="tight",
                pad_inches=0.03)
    plt.close(fig)
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--span", type=int, default=MARK_SPAN,
                        help="cells wide each edge is drawn (1 = one cell per edge)")
    span = parser.parse_args().span

    style.apply_rcparams()
    binary = substrates()
    cells = N_NODES * N_NODES
    print(f"mark span {span} cell(s)")
    for variant, matrix in binary.items():
        edges = int(matrix.sum() // 2)
        print(f"  {variant:27s} {edges} edges   density {2 * edges / cells:.2%}"
              f"   ink drawn {thicken(matrix, span).sum() / cells:.2%}")
    for inverted, name in ((False, "substrates_binary_normal.png"),
                           (True, "substrates_binary_inverted.png")):
        print(f"written: {render(binary, inverted, name, span)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

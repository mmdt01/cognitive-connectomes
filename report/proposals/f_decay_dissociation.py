"""Proposal figure for chapter 6 section 6.3 -- the curvature / VPT dissociation.

STANDALONE AND DELIBERATELY UNREGISTERED. This figure is not on
``report/FIGURE_LIST.md``, is not in ``report/figlib/figures/__init__.py`` and does not
build through the figlib registry. It writes beside itself in ``report/proposals/`` so
that it can be deleted without trace if the proposal is rejected. It imports
``report.figlib.style`` for the palette and the style contract -- one substrate, one
colour, thesis-wide -- but it does *not* use ``style.save()``, because that writes into
the canonical ``report/figures/`` directory.

Read-only against the results tree: it opens one frozen parquet with
``pandas.read_parquet`` and computes nothing that is stored anywhere else.

    python report/proposals/f_decay_dissociation.py

CAPTION (draft; not written to any file, see the note at the foot of this docstring)
-----------------------------------------------------------------------------------
Trajectory curvature and prediction skill come apart along the gain sweep. All-positive
substrate (f = 0), Lorenz task, N = 448, ten seeds per grid point, nominal-sigma axis.
(a) Mean trajectory curvature in radians, linear axis, plotted over its full range: the
connectome's curvature never leaves 0.25-0.28 rad anywhere on the sweep, and the flat
line is flat in the data rather than flattened by the axis. Curvature is bimodal, not
graded -- a seed sits either on the smooth branch near 0.26 rad or on a period-two orbit
near pi rad, with three of 1160 seed-cells anywhere in between -- so the per-seed points
carry the result and the median line does not. At the top of the sweep Erdos-Renyi's
seeds are split five and five between the two branches, and the median describes neither
group. (b) Valid prediction time on a log axis. Prediction skill decays across the whole
sweep for every substrate, including the connectome, whose curvature does not move at
all. Seeds whose VPT is exactly zero cannot be drawn on a log axis and are shown on the
dedicated "0" strip below the break, stacked within each cell so that height reads as a
count: 84 of the 1160 seed-cells, 53 of them the connectome's, 24 weight-permuted, 7
Erdos-Renyi and none degree-matching.

NOTE ON THE MISSING CAPTION FILE. The task asked for the zero count to be stated "in the
caption text file", but the write scope for this task permits exactly four paths (this
script, the PNG, the PDF and the values CSV) and forbids creating anything else. The
caption therefore lives here, in the file that is allowed to exist, and the count is also
reported in the run log printed by ``main``.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

_REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO_ROOT))

from report.figlib import style  # noqa: E402

PARQUET = (_REPO_ROOT / "experiments" / "human" / "analysis" / "criticality_matched"
           / "results" / "e01_jacobian_scale_448.parquet")
OUT_DIR = Path(__file__).resolve().parent
STEM = "f_decay_dissociation"

# The four rungs of the criticality-matched ladder, in the contract's order.
LADDER = list(style.LADDER)
CURVATURE_COL = "mean_curvature"
VPT_COL = "vpt"

# Horizontal offsets so the four substrates' seed clouds sit side by side at each grid
# point rather than on top of one another. The sweep step is 0.4, so +-0.135 of total
# spread leaves the grid points cleanly separated.
_OFFSET_STEP = 0.075
_JITTER = 0.022
_SEED_MARKER = dict(s=3.0, alpha=0.55, linewidths=0.0, zorder=2)

# The gate published in TIER0 section 3.11: seed-median curvature and VPT at f = 0 for
# the connectome and for Erdos-Renyi, to two decimal places.
GATE = {
    ("connectome", CURVATURE_COL): [0.26, 0.26, 0.26, 0.26, 0.26],
    ("connectome", VPT_COL): [4.43, 2.81, 0.81, 1.18, 0.44],
    ("erdos_renyi", CURVATURE_COL): [0.26, 0.26, 0.26, 0.27, 1.70],
    ("erdos_renyi", VPT_COL): [3.73, 2.45, 1.18, 0.49, 0.23],
}
GATE_SIGMA = [2.0, 4.0, 6.0, 8.0, 11.2]


def load_seed_table() -> pd.DataFrame:
    """One row per (variant, spectral_radius, seed) at f = 0, read-only.

    The parquet carries three draws per seed. At f = 0 no edges are flipped, so the
    three draws are bit-identical duplicates of one run rather than independent units;
    ``main`` asserts that before collapsing them, so the seed is the unit of analysis.
    """
    df = pd.read_parquet(PARQUET)
    d0 = df[df["f"] == 0.0]
    keys = ["variant", "spectral_radius", "seed"]
    spread = d0.groupby(keys)[[CURVATURE_COL, VPT_COL]].nunique().max().max()
    if spread != 1:
        raise SystemExit(f"draws are not duplicates at f = 0 (max distinct values {spread})")
    return d0.groupby(keys, as_index=False)[[CURVATURE_COL, VPT_COL]].first()


def check_gate(seeds: pd.DataFrame) -> bool:
    """Reproduce TIER0 section 3.11. Nothing is plotted unless this passes."""
    medians = seeds.groupby(["variant", "spectral_radius"])[[CURVATURE_COL, VPT_COL]].median()
    passed = True
    for (variant, column), expected in GATE.items():
        got = [round(float(medians.loc[(variant, s), column]), 2) for s in GATE_SIGMA]
        ok = all(abs(g - e) < 1e-9 for g, e in zip(got, expected))
        passed &= ok
        print(f"  gate {'PASS' if ok else 'FAIL'}  {variant:26s} {column:14s} "
              f"expected {expected} got {got}")
    return passed


def _seed_cloud(ax, sub: pd.DataFrame, column: str, offset: float, colour: str,
                rng: np.random.Generator) -> None:
    x = sub["spectral_radius"].to_numpy() + offset
    x = x + rng.uniform(-_JITTER, _JITTER, size=x.size)
    ax.scatter(x, sub[column].to_numpy(), color=colour, **_SEED_MARKER)


def build(seeds: pd.DataFrame):
    """Two stacked panels sharing the nominal-sigma axis, with a zero strip under (b)."""
    fig = plt.figure(figsize=(7.4, 5.9))
    # Two-level grid: the zero strip has to sit hard under (b) with only the break
    # between them, while (a) and (b) need ordinary panel spacing.
    outer = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.06], hspace=0.16)
    inner = outer[1].subgridspec(2, 1, height_ratios=[1.0, 0.10], hspace=0.06)
    ax_curv = fig.add_subplot(outer[0])
    ax_vpt = fig.add_subplot(inner[0], sharex=ax_curv)
    ax_zero = fig.add_subplot(inner[1], sharex=ax_curv)

    positive = seeds.loc[seeds[VPT_COL] > 0, VPT_COL]
    rng = np.random.default_rng(20260830)

    for index, variant in enumerate(LADDER):
        colour = style.VARIANT_COLOUR[variant]
        offset = (index - 1.5) * _OFFSET_STEP
        sub = seeds[seeds["variant"] == variant].sort_values("spectral_radius")

        _seed_cloud(ax_curv, sub, CURVATURE_COL, offset, colour, rng)
        _seed_cloud(ax_vpt, sub[sub[VPT_COL] > 0], VPT_COL, offset, colour, rng)

        # Zeros are real measurements, not missing data, and cannot go on a log axis.
        # They get their own strip, stacked inside the cell so height reads as a count.
        zeros = sub[sub[VPT_COL] == 0.0]
        for sigma, cell in zeros.groupby("spectral_radius"):
            n = len(cell)
            ys = 0.5 + (np.arange(n) - (n - 1) / 2.0) * (0.72 / 9.0)
            ax_zero.scatter(np.full(n, sigma + offset), ys, color=colour,
                            s=3.0, alpha=0.75, linewidths=0.0)

        median = sub.groupby("spectral_radius")[[CURVATURE_COL, VPT_COL]].median()
        # Solid for every substrate. The contract's dashes exist to separate lines that
        # overlap; here the seed clouds are already colour-coded underneath them, and a
        # dashed median reads as a different kind of object from a solid one.
        line = style.variant_kwargs(variant, label=style.VARIANT_TITLE[variant],
                                    ls="-", zorder=3)
        ax_curv.plot(median.index, median[CURVATURE_COL], **line)
        ax_vpt.plot(median.index, median[VPT_COL].where(median[VPT_COL] > 0), **line)

    # (a) curvature, linear, over the full observed range. The connectome's line has to
    # be visibly flat rather than flattened, so the axis is not clipped or truncated.
    top = float(seeds[CURVATURE_COL].max())
    ax_curv.set_ylim(0.0, top * 1.08)
    ax_curv.set_ylabel("mean curvature (rad)")
    ax_curv.tick_params(axis="x", which="both", labelbottom=False)
    style.panel_label(ax_curv, "a")
    # One column, stacked down the left. Placed in the empty band between the two
    # curvature branches: the top of the panel is where Erdos-Renyi's collapsed seeds
    # live and a legend there would hide them.
    style.legend(ax_curv, loc="center left", ncol=1, bbox_to_anchor=(0.02, 0.58))

    # (b) VPT, log, with the zeros exiled to their own strip below the break.
    ax_vpt.set_yscale("log")
    ax_vpt.set_ylim(float(positive.min()) * 0.6, float(positive.max()) * 1.5)
    ax_vpt.set_ylabel("VPT (Lyapunov times)")
    ax_vpt.spines["bottom"].set_visible(False)
    ax_vpt.tick_params(axis="x", which="both", bottom=False, labelbottom=False)
    style.panel_label(ax_vpt, "b")

    ax_zero.set_ylim(0.0, 1.0)
    ax_zero.set_yticks([0.5])
    ax_zero.set_yticklabels(["0"])
    ax_zero.tick_params(axis="y", length=0)
    ax_zero.spines["top"].set_visible(False)
    ax_zero.grid(False)
    ax_zero.set_xlabel(style.AXIS_LABEL["nominal"])
    ax_zero.set_xlim(-0.35, 11.55)
    # Even ticks every 2.0, all of which are sampled sigmas (the sweep steps by 0.4).
    # The sweep actually ends at 11.2, past the last tick; the axis is not padded out to
    # a round 12, so the right-hand edge of the data is where the drawing stops.
    ax_zero.set_xticks(np.arange(0.0, 10.1, 2.0))

    _draw_break(fig, ax_vpt, ax_zero)
    return fig


def _draw_break(fig, upper, lower) -> None:
    """The two slashes that say the axis is cut between the log panel and the strip."""
    kwargs = dict(marker=[(-1.0, -0.6), (1.0, 0.6)], markersize=6, linestyle="none",
                  color=style.ANNOTATION_COLOUR, mec=style.ANNOTATION_COLOUR, mew=0.9,
                  clip_on=False)
    upper.plot([0.0, 1.0], [0.0, 0.0], transform=upper.transAxes, **kwargs)
    lower.plot([0.0, 1.0], [1.0, 1.0], transform=lower.transAxes, **kwargs)


def main() -> int:
    style.apply_rcparams()
    style.check_colour_consistency()
    print("check_colour_consistency: OK (sweep palette equals src/experiment/plots)")

    seeds = load_seed_table()
    print(f"loaded {len(seeds)} seed-cells from {PARQUET.name} (f = 0)")

    if not check_gate(seeds):
        raise SystemExit("TIER0 section 3.11 did not reproduce; no figure written")
    print("gate: PASSED (20 / 20)")

    fig = build(seeds)
    for suffix in ("png", "pdf"):
        path = OUT_DIR / f"{STEM}.{suffix}"
        fig.savefig(path, dpi=style.DPI, bbox_inches="tight")
        print(f"wrote {path}")
    plt.close(fig)

    values = seeds.rename(columns={CURVATURE_COL: "curvature_rad", VPT_COL: "vpt"})
    values = values.sort_values(["variant", "spectral_radius", "seed"])
    csv_path = OUT_DIR / f"{STEM}_values.csv"
    values.to_csv(csv_path, index=False)
    print(f"wrote {csv_path}  ({len(values)} rows)")

    zeros = values[values["vpt"] == 0.0]
    print(f"VPT exactly zero: {len(zeros)} of {len(values)} seed-cells")
    for variant, count in zeros.groupby("variant").size().items():
        print(f"    {variant:26s} {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

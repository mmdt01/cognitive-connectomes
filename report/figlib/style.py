"""The figure style contract from ``report/CONVENTIONS.md``, fixed in one place.

Every figure in the §4b sweep is rendered through this module, so a style decision is
made once here and never again in a figure builder. Nothing below is a suggestion: the
colours, fonts, panel-label style, dpi and output paths are the contract, and a figure
that wants its own is a bug in the figure, not a missing option here.

The variant colours are the ones the committed per-task figures already use
(``src/experiment/plots._VARIANT_STYLE``), so a sweep figure and a task figure put the
same substrate in the same colour. ``check_colour_consistency`` asserts that, and is run
by the smoke entry point, so the two cannot drift apart silently.
"""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

_REPO_ROOT = Path(__file__).resolve().parents[2]
FIGURES_DIR = _REPO_ROOT / "report" / "figures"

# --------------------------------------------------------------------------- output
DPI = 300
FORMATS = ("pdf", "png")

# ------------------------------------------------------------------------- variants
# Fixed in session 0, held across every figure. Never varied.
#
# **Moved to Okabe-Ito in session 1, deliberately and thesis-wide.** The session-0 set
# (purple #9467bd / pink #e377c2 / light blue #88aadd for the three nulls) is weak under
# deuteranopia and collapses in greyscale, which for a figure whose whole job is telling
# four substrates apart is a defect rather than a taste question. Okabe-Ito is
# colourblind-safe under deuteranopia, protanopia and tritanopia and separates by
# luminance in greyscale. It was already the palette of the committed E0.4 figures
# (`experiments/human/analysis/eigenspectrum/common.VARIANT_COLOR`), so this change also
# ends a split that existed between those figures and the sweep.
#
# `src/experiment/plots._VARIANT_STYLE` moved with it in the same commit --
# `check_colour_consistency()` asserts the two are equal and would raise otherwise.
VARIANT_COLOUR = {
    "connectome": "#000000",                   # black
    "connectome_weight_permuted": "#D55E00",   # vermillion
    "degree_rewire": "#0072B2",                # blue
    "erdos_renyi": "#009E73",                  # bluish green
    "random_gaussian": "#CC79A7",              # reddish purple
    # The two upper rungs. CONVENTIONS names the five above; these are needed because
    # Probe 3's ladder is seven rungs, and one colour per substrate has to hold there too.
    "clustering_rewire": "#56B4E9",            # sky blue
    "modularity_rewire": "#E69F00",            # orange
}
VARIANT_LABEL = {
    "connectome": "connectome",
    "connectome_weight_permuted": "connectome · perm. weights",
    "degree_rewire": "rung 2 · degree",
    "erdos_renyi": "rung 1 · ER",
    "random_gaussian": "rung 0 · random",
    "clustering_rewire": "rung 3 · clustering",
    "modularity_rewire": "rung 4 · modularity",
}
# Two-line categorical-axis labels. VARIANT_LABEL is a legend label and is too wide
# for a four-bar x-axis at 9pt -- splitting on " · " leaves "connectome\nperm.
# weights", which collides with its neighbours. Same names, same order, wrapped to
# fit; use these for tick labels and VARIANT_LABEL for legends.
# Plain substrate names for small-multiple panel titles, where the panels contrast the
# substrates themselves rather than their position on the null ladder, so the rung
# numbering carried by VARIANT_LABEL is noise. Matches the committed E0.4 figure's
# titles, which is where this idiom comes from.
VARIANT_TITLE = {
    "connectome": "Connectome",
    "connectome_weight_permuted": "Weight-permuted",
    "degree_rewire": "Degree-matching",
    "erdos_renyi": "Erdős–Rényi",
    "random_gaussian": "Random gaussian",
    "clustering_rewire": "Clustering-matching",
    "modularity_rewire": "Modularity-matching",
}
VARIANT_TICK = {
    "connectome": "connec-\ntome",
    "connectome_weight_permuted": "perm.\nweights",
    "degree_rewire": "rung 2\ndegree",
    "erdos_renyi": "rung 1\nER",
    "random_gaussian": "rung 0\nrandom",
    "clustering_rewire": "rung 3\nclust.",
    "modularity_rewire": "rung 4\nmodul.",
}
# Wrapped VARIANT_TITLE, for a categorical axis inside a figure whose other panels are
# titled with VARIANT_TITLE. Mixing the two naming schemes in one figure (rung numbers
# on the axis, plain names on the panels) makes them read as different sets of things.
VARIANT_TITLE_TICK = {
    "connectome": "Connectome",
    "connectome_weight_permuted": "Weight-\npermuted",
    "degree_rewire": "Degree-\nmatching",
    "erdos_renyi": "Erdős–\nRényi",
    "random_gaussian": "Random\ngaussian",
    "clustering_rewire": "Clustering-\nmatching",
    "modularity_rewire": "Modularity-\nmatching",
}
# Substrate first, then the null ladder outward from it. Legends follow this order.
VARIANT_ORDER = ["connectome", "connectome_weight_permuted", "degree_rewire",
                 "erdos_renyi", "random_gaussian", "clustering_rewire",
                 "modularity_rewire"]
# The four the criticality-matched programme actually sweeps.
LADDER = ["connectome", "connectome_weight_permuted", "degree_rewire", "erdos_renyi"]

VARIANT_LINESTYLE = {
    "connectome": "-",
    "connectome_weight_permuted": "-.",
    "degree_rewire": "-",
    "erdos_renyi": "--",
    "random_gaussian": "--",
    "clustering_rewire": ":",
    "modularity_rewire": ":",
}
VARIANT_LINEWIDTH = {
    "connectome": 2.0,
    "connectome_weight_permuted": 1.5,
    "degree_rewire": 1.4,
    "erdos_renyi": 1.4,
    "random_gaussian": 1.2,
    "clustering_rewire": 1.2,
    "modularity_rewire": 1.2,
}

CONDITION_LABEL = {
    "human_empirical": "all-positive (f = 0)",
    "human_empirical_signed": "signed (empirical weights)",
    "human_gaussian": "gaussian weights",
}

# ------------------------------------------------------------------- bases / measures
# Act II contrasts *bases* (F4, F5) and *dimensionality measures* (F6), neither of which
# is a substrate. They get their own two-colour accent set, **off the Okabe-Ito wheel on
# purpose**, plus grey for whichever series is the chance baseline.
#
# Why a separate set at all. Okabe-Ito has eight hues, the variant contract spends seven
# of them, and the eighth (#F0E442 yellow) is unusable on white. So a basis palette must
# either reuse a substrate colour -- and F4 draws bases in (a) beside variants in (b),
# which would give one hue two meanings in one figure -- or leave the wheel. It leaves.
#
# Why these two. Chosen by measurement, not by eye: CIE76 dE in Lab after Vienot/Brettel
# dichromacy simulation, scored on separation among the bases, distance from all seven
# substrate colours, and greyscale luminance. Indigo/brick dominated every candidate
# tried on all three at once (among-bases 50.8, vs-variants 11.5, greyscale dL 14.5;
# runners-up traded one against another). `check_basis_palette()` re-derives those
# numbers and is run by the smoke entry point, so the choice cannot silently drift into
# a clash. dE ~ 2.3 is a just-noticeable difference and >15 is comfortably distinct.
#
# Dash and marker are kept **as well as** hue. The encoding is deliberately redundant so
# the series survive greyscale printing and any dichromacy, rather than resting on colour
# alone -- which is what made the previous all-black version unreadable in the first place.
BASIS_COLOUR = {"harmonics": "#33356B", "wmodes": "#A63603", "random": "#9A9A9A"}
BASIS_STYLE = {
    "harmonics": dict(color=BASIS_COLOUR["harmonics"], ls="-", marker="o", ms=3.2, lw=1.6),
    "wmodes": dict(color=BASIS_COLOUR["wmodes"], ls="--", marker="s", ms=3.2, lw=1.6),
    "random": dict(color=BASIS_COLOUR["random"], ls=":", marker=None, lw=1.3),
}
BASIS_LABEL = {
    "harmonics": "graph harmonics (low freq.)",
    "wmodes": r"$W$ eigenmodes (dominant)",
    "random": "random orthonormal (chance)",
}
BASIS_BAND_COLOUR = BASIS_COLOUR["random"]

# The two dimensionality measures F6 contrasts, on the same accent pair. Nothing links
# `d_eff` to harmonics or PR to the W-modes -- the pair simply means "the two quantities
# this act sets against each other", and reusing it keeps one accent set across Act II
# rather than inventing a third.
MEASURE_STYLE = {
    "d_eff": dict(color=BASIS_COLOUR["harmonics"], ls="-", lw=1.7),
    "pr": dict(color=BASIS_COLOUR["wmodes"], ls="--", lw=1.7),
}
MEASURE_FILL = {"d_eff": BASIS_COLOUR["harmonics"], "pr": BASIS_COLOUR["wmodes"]}
CONDITION_COLOUR = {
    "human_empirical": "#c44e52",
    "human_empirical_signed": "#dd8452",
    "human_gaussian": "#4c72b0",
}

# --------------------------------------------------------------------------- axes
# The two matching axes, always labelled with what each holds fixed (CONVENTIONS,
# "Two axes, always both"). Never plot one without saying which it is.
AXIS_LABEL = {
    "nominal": r"nominal $\sigma$   (spectral radius held fixed)",
    "effective": r"$\sigma \cdot \mathrm{bulk95}$   (bulk radius held fixed)",
}
AXIS_SHORT = {"nominal": "nominal", "effective": r"$\sigma\cdot$bulk95"}
# One colour per matching axis, for the figures that contrast the two rather than
# plotting on one of them (F3 panel c, F11 panel b). Not substrate colours and not
# boundary colours: a third small namespace, for the same reason the other two exist --
# the nominal axis is one colour everywhere it is set against the matched one.
AXIS_COLOUR = {"nominal": "#1f77b4", "effective": "#c44e52"}

# The two phase boundaries. Not variants, so they get their own pair, held fixed for
# the same reason the variant colours are: the memory boundary is one colour everywhere.
BOUNDARY_COLOUR = {"dD": "#1f77b4", "dStraight": "#d95f02"}
BOUNDARY_LABEL = {"dD": "memory boundary", "dStraight": "generative boundary"}
# Region past the all-replicates coverage edge: drawn, never read (TIER0 §6.10).
UNCOVERED_COLOUR = "#b0b0b0"

# Shading for the supercritical region and for annotation furniture.
SUPERCRITICAL_COLOUR = "#fff3e0"
CEILING_COLOUR = "#888888"
ANNOTATION_COLOUR = "#333333"
# The one accent used to mark a *claim* inside a panel -- a band, a threshold, the bar
# that carries the result. Added in session 4 as a NAME for a value already in use as a
# literal in `act1_structure` and `act4_anchor`, so no rendered figure changes colour;
# it exists so the prediction arm's five annotation marks cannot drift apart. Not a
# variant, axis or boundary colour: those three namespaces stay closed.
ANNOTATION_ACCENT = "#c44e52"

# --------------------------------------------------------------------------- fonts
AXIS_LABEL_SIZE = 9
TICK_SIZE = 8
PANEL_LABEL_SIZE = 10
LEGEND_SIZE = 8
TITLE_SIZE = 9

_RCPARAMS = {
    "figure.dpi": 110,               # on-screen; save() forces DPI for the file
    "savefig.dpi": DPI,
    "savefig.bbox": "tight",
    "font.size": AXIS_LABEL_SIZE,
    "axes.labelsize": AXIS_LABEL_SIZE,
    "axes.titlesize": TITLE_SIZE,
    "xtick.labelsize": TICK_SIZE,
    "ytick.labelsize": TICK_SIZE,
    "legend.fontsize": LEGEND_SIZE,
    "legend.frameon": False,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linewidth": 0.5,
    "lines.linewidth": 1.4,
    "pdf.fonttype": 42,              # embed TrueType, not Type 3: editable in Illustrator
    "ps.fonttype": 42,
}


def apply_rcparams() -> None:
    """Install the style contract. Called once by the entry point, before any build."""
    matplotlib.use("Agg")
    plt.rcParams.update(_RCPARAMS)


# ----------------------------------------------------------------------- furniture
def panel_label(ax, letter: str, dx: float = -0.08, dy: float = 1.06,
                offset_points: tuple = None) -> None:
    """Lower-case bold panel label at the top left, per the style contract.

    ``dx`` / ``dy`` are **axes fractions**, so the absolute offset they buy scales with
    the panel. That is fine while a figure's panels are all one size, which is true of
    every figure here except F1, and it is why this remains the default.

    Pass ``offset_points=(dx_pt, dy_pt)`` instead when a figure mixes panel sizes: the
    label is then placed a fixed distance from the axes' top-left corner regardless of
    how tall the panel is, which is what makes a set of labels line up. F1 stacks four
    short rows beside two tall panels (91.8 px against 203.0 px), where the same ``dy``
    put the 'e' 21.5 px higher on the page than the 'a' beside it.
    """
    if offset_points is not None:
        ax.annotate(letter, xy=(0.0, 1.0), xycoords="axes fraction",
                    xytext=offset_points, textcoords="offset points",
                    fontsize=PANEL_LABEL_SIZE, fontweight="bold",
                    va="bottom", ha="right")
        return
    ax.text(dx, dy, letter, transform=ax.transAxes, fontsize=PANEL_LABEL_SIZE,
            fontweight="bold", va="top", ha="right")


def variant_kwargs(variant: str, **overrides) -> dict:
    """Line style for one variant: colour, dash and width, all from the contract."""
    kwargs = dict(color=VARIANT_COLOUR[variant], label=VARIANT_LABEL[variant],
                  ls=VARIANT_LINESTYLE[variant], lw=VARIANT_LINEWIDTH[variant])
    kwargs.update(overrides)
    return kwargs


def ordered_variants(present) -> list:
    """The variants in ``present``, in the contract's legend order."""
    present = set(present)
    return [v for v in VARIANT_ORDER if v in present]


def draw_ceiling(ax, n_nodes: int, label: str = None, on: str = "y",
                 side: str = "right") -> None:
    """Draw the ``d_eff = N`` ceiling. CONVENTIONS: every memory figure shows it.

    ``on`` names the axis ``d_eff`` is plotted against. F3 puts it on y (the default,
    unchanged); F6 puts it on x, where a horizontal rule would mark nothing.

    ``side`` moves the rule's label to the other end of it, for a panel whose right
    edge is already spoken for. F7 needs it: its top-of-overlap rule stands at the
    right-hand edge and a right-aligned ceiling label has the rule drawn through it.
    """
    if on == "y":
        ax.axhline(n_nodes, color=CEILING_COLOUR, lw=0.9, ls=":", zorder=1)
        at, align = ((0.995, "right") if side == "right" else (0.008, "left"))
        ax.text(at, n_nodes, label or f"$d_{{\\rm eff}} = N = {n_nodes}$",
                transform=ax.get_yaxis_transform(), ha=align, va="bottom",
                fontsize=TICK_SIZE, color=CEILING_COLOUR)
        return
    if on != "x":
        raise ValueError(f"draw_ceiling: 'on' must be 'x' or 'y', got {on!r}")
    ax.axvline(n_nodes, color=CEILING_COLOUR, lw=0.9, ls=":", zorder=1)
    ax.text(n_nodes, 0.99, label or f"$N = {n_nodes}$ ",
            transform=ax.get_xaxis_transform(), ha="right", va="top",
            rotation=90, fontsize=TICK_SIZE, color=CEILING_COLOUR)


def shade_supercritical(ax, start: float, end: float = None) -> None:
    """Shade the supercritical region from ``start`` to the right-hand limit."""
    end = ax.get_xlim()[1] if end is None else end
    ax.axvspan(start, end, color=SUPERCRITICAL_COLOUR, zorder=0)


def legend(ax, **kwargs) -> None:
    handles, labels = ax.get_legend_handles_labels()
    if not handles:
        return
    seen, pairs = set(), []
    for handle, label in zip(handles, labels):
        if label not in seen:
            seen.add(label)
            pairs.append((handle, label))
    ax.legend(*zip(*pairs), **kwargs)


# ---------------------------------------------------------------------------- save
def save(fig, figure_id: str, subdir: str = None) -> list:
    """Write ``figure_id`` to ``report/figures/`` as 300 dpi PDF plus PNG.

    ``subdir`` puts a build somewhere other than the canonical directory; the smoke
    entry point uses it so placeholder renders can never be mistaken for real ones.
    """
    out_dir = FIGURES_DIR / subdir if subdir else FIGURES_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for suffix in FORMATS:
        path = out_dir / f"{figure_id}.{suffix}"
        fig.savefig(path, dpi=DPI)
        written.append(path)
    plt.close(fig)
    return written


# --------------------------------------------------------------------- consistency

# Vienot/Brettel dichromacy simulation, used only by `check_basis_palette` below.
_LMS = [[17.8824, 43.5161, 4.11935], [3.45565, 27.1554, 3.86714],
        [0.0299566, 0.184309, 1.46709]]
_DICHROMAT = {
    "protanopia": [[0, 2.02344, -2.52581], [0, 1, 0], [0, 0, 1]],
    "deuteranopia": [[1, 0, 0], [0.494207, 0, 1.24827], [0, 0, 1]],
    "tritanopia": [[1, 0, 0], [0, 1, 0], [-0.395913, 0.801109, 0]],
}
# Floors the measured palette clears with room to spare (50.8 / 11.5 in the session-2
# search). Set below the measurement, not at it, so an intentional future tweak is not
# forced to reproduce these hexes exactly -- only to stay legible and un-clashing.
BASIS_SEPARATION_FLOOR = 25.0      # among the bases, worst case over all vision types
BASIS_VARIANT_FLOOR = 8.0          # any basis colour against any substrate colour


def _lab(hex_colour: str, vision: str = "normal"):
    import numpy as np
    raw = hex_colour.lstrip("#")
    rgb = np.array([int(raw[i:i + 2], 16) / 255.0 for i in (0, 2, 4)])
    if vision != "normal":
        rgb = np.clip(np.linalg.solve(np.array(_LMS),
                                      np.array(_DICHROMAT[vision]) @ (np.array(_LMS) @ rgb)),
                      0, 1)
    linear = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    xyz = (np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722],
                     [0.0193, 0.1192, 0.9505]]) @ linear) / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.array([116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])])


def check_basis_palette() -> dict:
    """Assert the Act II accent colours are legible and do not clash with substrates.

    Re-derives the two numbers the palette was chosen on (CIE76 dE after Vienot/Brettel
    dichromacy simulation) so a later edit cannot quietly reintroduce either failure the
    current palette was picked to avoid: three basis curves that cannot be told apart,
    or a basis hue a reader would read as a substrate.
    """
    import numpy as np
    visions = ("normal", "protanopia", "deuteranopia", "tritanopia")
    keys = list(BASIS_COLOUR)
    among = min(float(np.linalg.norm(_lab(BASIS_COLOUR[a], v) - _lab(BASIS_COLOUR[b], v)))
                for v in visions for i, a in enumerate(keys) for b in keys[i + 1:])
    versus = min(float(np.linalg.norm(_lab(BASIS_COLOUR[k], v) - _lab(c, v)))
                 for v in visions for k in keys for c in VARIANT_COLOUR.values())
    assert among >= BASIS_SEPARATION_FLOOR, (
        f"Act II basis colours are not separable: worst pairwise dE {among:.1f} over "
        f"normal vision and the three dichromacies, floor {BASIS_SEPARATION_FLOOR}. "
        "Three curves share a panel in F4a and F5; they have to be tellable apart.")
    assert versus >= BASIS_VARIANT_FLOOR, (
        f"An Act II basis colour collides with a substrate colour: worst dE "
        f"{versus:.1f}, floor {BASIS_VARIANT_FLOOR}. F4 draws bases in (a) beside "
        "variants in (b), so a shared hue would carry two meanings in one figure.")
    return {"among_bases": among, "vs_variants": versus}


def check_colour_consistency() -> None:
    """Assert the sweep palette equals the committed task-figure palette.

    One substrate, one colour, across the whole thesis. If ``src/experiment/plots``
    ever changes a colour this raises rather than letting the chapters drift.
    """
    from src.experiment.plots import _VARIANT_STYLE
    mismatched = {v: (VARIANT_COLOUR[v], _VARIANT_STYLE[v]["color"])
                  for v in VARIANT_COLOUR
                  if _VARIANT_STYLE[v]["color"] != VARIANT_COLOUR[v]}
    assert not mismatched, (
        "figure-module palette has drifted from src/experiment/plots._VARIANT_STYLE: "
        f"{mismatched}. Fix one of the two; the thesis uses one colour per substrate.")

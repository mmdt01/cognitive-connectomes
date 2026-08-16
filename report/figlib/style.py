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


def draw_ceiling(ax, n_nodes: int, label: str = None) -> None:
    """Draw the ``d_eff = N`` ceiling. CONVENTIONS: every memory figure shows it."""
    ax.axhline(n_nodes, color=CEILING_COLOUR, lw=0.9, ls=":", zorder=1)
    ax.text(0.995, n_nodes, label or f"$d_{{\\rm eff}} = N = {n_nodes}$",
            transform=ax.get_yaxis_transform(), ha="right", va="bottom",
            fontsize=TICK_SIZE, color=CEILING_COLOUR)


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

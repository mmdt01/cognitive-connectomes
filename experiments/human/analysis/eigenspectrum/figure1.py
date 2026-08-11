"""E0.4 step 3: the publication figures.

Separate from the analysis driver on purpose -- these get iterated many times during
writing and must never require re-running an eigendecomposition. Everything here
**reads** ``tables.py`` / ``bulk95_f.py`` output; nothing is recomputed.

Three figures, each written as vector PDF (the paper artifact) + 300 dpi PNG (the
tracked preview), on the Okabe-Ito colourblind-safe palette:

``fig1_spectrum``
    The paper's Figure 1, drawn entirely at ``common.PRIMARY_SCALE`` so no panel mixes
    parcellations. (a-d) the eigenvalue distribution of the normalised recurrent
    matrix for connectome / weight-permuted / degree-matching / Erdos-Renyi, with the
    ``bulk95`` band shaded; (e) the ECDF of ``|lambda|`` with the 95th-percentile
    level drawn, which *is* the definition of ``bulk95``, so the number can be read
    off the figure; (f) ``bulk95`` per variant with every seed shown, and
    ``sr_crit = 1/bulk95`` on the right-hand axis.

    The point it must make: **the connectome and its weight-permuted control have the
    same topology and the same multiset of weights** -- they differ only in which
    weight sits on which edge -- **yet have visibly different bulk radii.** Placement,
    not topology alone and not weight statistics alone. A generated caption
    (``fig1_spectrum_caption.md``) states this and the per-panel reading, with the
    numbers pulled live from the data so they cannot drift from the figure.

``figS_complex_plane``
    The literal complex-plane scatter. For the human substrate ``W`` is symmetric, so
    the spectrum is real to machine precision and the scatter collapses onto the real
    axis; the panel states the measured ``max |Im lambda|`` rather than pretending
    otherwise. Kept because the *C. elegans* directed substrate and the Dale sign arm
    do have genuinely complex spectra.

``figS_bulk95_vs_f``
    ``bulk95`` against the sign fraction ``f``, per variant and sign mode -- the
    diagnostic that any (f, sr) reindex needs a per-``f`` ``bulk95``.
"""

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.human.analysis.eigenspectrum import common

_INK, _MUT, _GRID = "#111111", "#8a8a8a", "#dddddd"
_LOG_FLOOR = 2e-2          # bottom of the log density axis

# Panel titles: plain substrate names, no rung numbering (the ladder position is not
# what these four panels are contrasting).
_PANEL_TITLE = {
    "connectome": "Connectome",
    "connectome_weight_permuted": "Weight-permuted",
    "degree_rewire": "Degree-matching",
    "erdos_renyi": "Erdős–Rényi",
}
# Compact axis-tick names for the summary panel, where the full titles collide.
_SHORT_TITLE = {
    "connectome": "Connectome",
    "connectome_weight_permuted": "Weight-\npermuted",
    "degree_rewire": "Degree-\nmatching",
    "erdos_renyi": "Erdős–\nRényi",
}
_PANEL_LABEL_KW = dict(fontsize=10, fontweight="bold", va="top", ha="left",
                       color=_INK)

# Publication rcParams, applied locally so no global matplotlib state is mutated.
_RC = {
    "font.size": 8,
    "axes.labelsize": 8,
    "axes.titlesize": 8.5,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "axes.linewidth": 0.7,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "axes.edgecolor": _INK,
    "axes.labelcolor": _INK,
    "text.color": _INK,
    "xtick.color": _INK,
    "ytick.color": _INK,
    "pdf.fonttype": 42,      # embed TrueType, so the PDF text stays editable/selectable
    "ps.fonttype": 42,
    "savefig.bbox": "tight",
}


def _save(fig, path_stem) -> None:
    """Vector PDF (paper) + 300 dpi PNG (tracked preview)."""
    for suffix, kwargs in ((".pdf", {}), (".png", {"dpi": 300})):
        path = path_stem.with_suffix(suffix)
        fig.savefig(path, **kwargs)
        print(f"Saved {path}")
    plt.close(fig)


def _style(ax) -> None:
    ax.grid(True, color=_GRID, lw=0.5, alpha=0.8)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def _label(ax, letter) -> None:
    ax.text(-0.14, 1.14, letter, transform=ax.transAxes, **_PANEL_LABEL_KW)


def _eigenvalues(df: pd.DataFrame, variant: str) -> np.ndarray:
    """All (seed-pooled) real parts of the normalised spectrum for one variant."""
    sub = df[(df.condition == common.BASE_CONDITION) & (df.variant == variant)]
    return np.concatenate([np.asarray(v, dtype=float) for v in sub.eig_w_real])


def _moduli(df: pd.DataFrame, variant: str) -> np.ndarray:
    sub = df[(df.condition == common.BASE_CONDITION) & (df.variant == variant)]
    return np.concatenate([
        np.hypot(np.asarray(r, dtype=float), np.asarray(i, dtype=float))
        for r, i in zip(sub.eig_w_real, sub.eig_w_imag)])


def _bulk95(df: pd.DataFrame, variant: str) -> np.ndarray:
    sub = df[(df.condition == common.BASE_CONDITION) & (df.variant == variant)]
    return sub.bulk95.to_numpy(float)


# ---------------------------------------------------------------------------
# Figure 1
# ---------------------------------------------------------------------------
def fig1(spectra: dict, path_stem) -> None:
    """Every panel is drawn at ``common.PRIMARY_SCALE`` -- one parcellation
    throughout, so nothing in the figure mixes N."""
    primary = spectra[common.PRIMARY_SCALE]
    variants = common.FIGURE_VARIANTS

    with plt.rc_context(_RC):
        fig = plt.figure(figsize=(7.4, 5.4))
        # Nested gridspecs so the two rows get independent column spacing: (a)-(d)
        # sit close as a series, while (e) and (f) are two separate arguments and
        # need clear separation.
        gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.15], hspace=0.62)
        gs_top = gs[0].subgridspec(1, 4, wspace=0.36)
        gs_bottom = gs[1].subgridspec(1, 2, wspace=0.52)

        # --- (a)-(d): eigenvalue distribution per variant ---------------------
        bins = np.linspace(-1.02, 1.02, 121)
        top_axes = []
        for col, variant in enumerate(variants):
            ax = fig.add_subplot(gs_top[0, col])
            top_axes.append(ax)
            colour = common.VARIANT_COLOR[variant]
            values = _eigenvalues(primary, variant)
            b95 = float(_bulk95(primary, variant).mean())

            ax.axvspan(-b95, b95, color=colour, alpha=0.13, lw=0, zorder=0)
            ax.hist(values, bins=bins, density=True, color=colour, alpha=0.85,
                    lw=0, zorder=2)
            for edge in (-b95, b95):
                ax.axvline(edge, color=colour, lw=1.0, ls="--", zorder=3)
            ax.set_xlim(-1.08, 1.14)
            ax.set_yscale("log")
            ax.set_ylim(_LOG_FLOOR, 60)
            ax.set_xticks([-1, 0, 1])
            ax.set_xlabel(r"$\lambda\,/\,|\lambda_1|$", labelpad=1)
            ax.set_title(f"{_PANEL_TITLE[variant]}\n"
                         rf"bulk$_{{95}}$ = {b95:.3f}", pad=4)
            _style(ax)
            if col == 0:
                ax.set_ylabel("density (log)", labelpad=2)
                _label(ax, "a")
            else:
                ax.set_yticklabels([])
                _label(ax, "bcd"[col - 1])

        # --- (e): ECDF of |lambda| -- the definition of bulk95 ------------------
        ax = fig.add_subplot(gs_bottom[0, 0])
        for variant in variants:
            mods = np.sort(_moduli(primary, variant))
            ecdf = np.arange(1, mods.size + 1) / mods.size
            ax.plot(mods, ecdf, color=common.VARIANT_COLOR[variant], lw=1.4,
                    label=_PANEL_TITLE[variant], solid_capstyle="round")
        ax.axhline(0.95, color=_MUT, lw=0.9, ls=":")
        ax.text(0.015, 0.955, "95th percentile", fontsize=6.5, color=_MUT,
                va="bottom", ha="left")
        for variant in variants:
            b95 = float(_bulk95(primary, variant).mean())
            ax.plot([b95, b95], [0.0, 0.95], color=common.VARIANT_COLOR[variant],
                    lw=0.8, ls="--", alpha=0.8)
        ax.set_xlim(0, 1.02)
        ax.set_ylim(0, 1.02)
        ax.set_xlabel(r"$|\lambda|\,/\,|\lambda_1|$", labelpad=1)
        ax.set_ylabel("cumulative fraction of modes", labelpad=2)
        # Nudged right and narrowed so its left edge clears the bulk95 drop lines,
        # the rightmost of which sits at ~0.55 on this axis.
        ax.legend(loc="lower right", bbox_to_anchor=(1.055, -0.012), frameon=False,
                  handlelength=0.95, handletextpad=0.5, labelspacing=0.32,
                  borderaxespad=0.0, fontsize=6.4)
        _style(ax)
        _label(ax, "e")

        # --- (f): bulk95 per variant, one point per seed ------------------------
        ax = fig.add_subplot(gs_bottom[0, 1])
        rng = np.random.default_rng(0)
        for i, variant in enumerate(variants):
            values = _bulk95(primary, variant)
            jitter = rng.uniform(-0.10, 0.10, values.size)
            ax.plot(i + jitter, values, ls="none", marker="o", ms=3.2, alpha=0.55,
                    color=common.VARIANT_COLOR[variant], mew=0)
            ax.plot([i - 0.22, i + 0.22], [values.mean()] * 2,
                    color=common.VARIANT_COLOR[variant], lw=2.0,
                    solid_capstyle="butt")
        ax.set_xticks(range(len(variants)))
        ax.set_xticklabels([_SHORT_TITLE[v] for v in variants], fontsize=6.5)
        ax.set_ylabel(r"bulk$_{95}$", labelpad=2)
        ax.set_xlim(-0.5, len(variants) - 0.5)
        # Bound the axis away from zero *before* attaching the reciprocal twin: the
        # sr_crit = 1/bulk95 map diverges at 0, and an unbounded twin makes the tight
        # bbox explode.
        all_values = np.concatenate([_bulk95(primary, v) for v in variants])
        lo, hi = float(all_values.min()), float(all_values.max())
        pad = 0.08 * (hi - lo)
        ax.set_ylim(max(lo - pad, 1e-3), hi + pad)
        secondary = ax.secondary_yaxis(
            "right", functions=(lambda y: 1.0 / np.maximum(y, 1e-3),
                                lambda y: 1.0 / np.maximum(y, 1e-3)))
        secondary.set_ylabel(r"$sr_{crit} = 1/\mathrm{bulk}_{95}$", labelpad=2)
        secondary.spines["right"].set_visible(True)
        _style(ax)
        _label(ax, "f")

        fig.suptitle("Connectome weight placement compresses the eigenvalue bulk",
                     fontsize=9.5, y=1.00)
        _save(fig, path_stem)


def fig1_caption(spectra: dict, path) -> None:
    """Write the Figure 1 caption, with every number read from the plotted data."""
    primary = spectra[common.PRIMARY_SCALE]
    n_nodes = int(np.asarray(primary.eig_w_real.iloc[0]).size)
    stats = {v: (float(_bulk95(primary, v).mean()), float(_bulk95(primary, v).std()))
             for v in common.FIGURE_VARIANTS}
    conn, perm = stats["connectome"][0], stats["connectome_weight_permuted"][0]
    deg, er = stats["degree_rewire"][0], stats["erdos_renyi"][0]
    max_imag = float(primary.max_abs_imag.max())
    imag_text = "exactly 0" if max_imag == 0.0 else f"max |Im λ| = {max_imag:.1e}"
    # The definition string carries backticks of its own, so quote it as a block
    # rather than nesting inline code (which would not render).
    definition = common.BULK95_DEFINITION.replace("``", "`")

    text = f"""# Figure 1 — caption

**Connectome weight placement compresses the eigenvalue bulk.**
Spectra of the recurrent matrix `W` for the human structural connectome and three
controls, human SC consensus, N = {n_nodes}, {common.N_SEEDS} seeds per variant. Every
panel is drawn on the **normalised** matrix `W / |λ₁|`, the object the reservoir build
actually rescales, so the leading eigenvalue sits at 1 by construction and all
quantities are scale-invariant ratios. `W` is symmetric here, so the spectrum is real
({imag_text} imaginary part); the complex-plane view is therefore degenerate and is
given separately as `figS_complex_plane`. No reservoir is simulated anywhere in this
figure — it is eigendecomposition only.

**The four substrates.** *Connectome*: the real weighted SC. *Weight-permuted*: the
connectome's exact topology carrying a random permutation of its own exact weight
multiset — so it differs from the connectome **only in which weight sits on which
edge**. *Degree-matching*: a degree-preserving rewire (rung 2), which randomises
topology while holding the exact degree sequence. *Erdős–Rényi*: a random graph with
the same edge count (rung 1). Reading left to right, the panels strip away first
weight placement, then degree structure, then topology.

**(a)–(d) Eigenvalue distributions.** Histogram (log density) of the normalised
eigenvalues for each substrate, pooled over seeds. The shaded band and dashed lines
mark ±`bulk95`, the radius containing 95% of the spectrum. The bulk is visibly
narrowest for the connectome (`bulk95` = {conn:.3f}) and broadens across the controls
({perm:.3f}, {deg:.3f}, {er:.3f}). **The comparison that carries the claim is (a)
versus (b):** identical topology, identical weight values, yet the bulk widens by
{100 * (perm - conn) / conn:.0f}% once the weights are shuffled between edges. The
compression is therefore a property of *where the weights sit*, not of the graph's
topology alone and not of the weight distribution alone — which (c) and (d) confirm by
moving `bulk95` comparatively little further as degree structure and then topology are
destroyed in turn.

**(e) Cumulative spectrum.** Empirical CDF of `|λ| / |λ₁|` for the four substrates.
The dotted horizontal line marks the 95th percentile and the coloured dashed verticals
drop to each substrate's `bulk95`, so the panel *is* the definition of the statistic
rather than a summary of it: `bulk95` is simply where each curve crosses 0.95. The
connectome's curve rises far more steeply — the great majority of its modes are
strongly sub-dominant — while the three controls are tightly bunched, showing that the
connectome is the outlier and the controls are not meaningfully different from one
another.

**(f) `bulk95` per substrate, with the critical scale.** One point per seed (jittered
horizontally), the bar marking the mean; the right-hand axis converts to
`sr_crit = 1/bulk95`, the nominal spectral radius at which that substrate's bulk
reaches criticality. The connectome shows **zero seed-to-seed spread** — it is a single
fixed graph, and only the nulls are resampled, so its `bulk95` has no sampling
distribution. The gap between the connectome and every control exceeds the controls'
own spread by a wide margin. In `sr_crit` terms the connectome stays subcritical to
{1 / conn:.2f} while the controls turn critical between {1 / er:.2f} and {1 / perm:.2f},
which is why matching substrates on *nominal* spectral radius does not match them on
effective criticality.

**Definition.**

> {definition}
"""
    path.write_text(text)
    print(f"Saved {path}")


# ---------------------------------------------------------------------------
# Supplementary: the literal complex plane
# ---------------------------------------------------------------------------
def fig_complex_plane(spectra: dict, path_stem) -> None:
    primary = spectra[common.PRIMARY_SCALE]
    variants = common.FIGURE_VARIANTS
    theta = np.linspace(0, 2 * np.pi, 361)

    with plt.rc_context(_RC):
        fig, axes = plt.subplots(1, len(variants), figsize=(7.2, 2.15),
                                 squeeze=False)
        for ax, variant in zip(axes[0], variants):
            colour = common.VARIANT_COLOR[variant]
            sub = primary[(primary.condition == common.BASE_CONDITION)
                          & (primary.variant == variant) & (primary.seed == 0)]
            real = np.asarray(sub.eig_w_real.iloc[0], dtype=float)
            imag = np.asarray(sub.eig_w_imag.iloc[0], dtype=float)
            b95 = float(sub.bulk95.iloc[0])

            ax.plot(np.cos(theta), np.sin(theta), color=_GRID, lw=0.8, ls="--",
                    zorder=1)
            ax.plot(b95 * np.cos(theta), b95 * np.sin(theta), color=colour, lw=1.2,
                    zorder=3)
            ax.axhline(0, color=_GRID, lw=0.5, zorder=0)
            ax.axvline(0, color=_GRID, lw=0.5, zorder=0)
            ax.scatter(real, imag, s=5, color=colour, alpha=0.55, lw=0, zorder=2)
            lead = int(np.argmax(np.hypot(real, imag)))
            ax.plot([real[lead]], [imag[lead]], marker="*", ms=8, color=_INK,
                    ls="none", zorder=4)
            ax.set_aspect("equal")
            ax.set_xlim(-1.15, 1.15)
            ax.set_ylim(-1.15, 1.15)
            ax.set_xticks([-1, 0, 1])
            ax.set_yticks([-1, 0, 1])
            ax.set_title(f"{common.VARIANT_TITLE[variant]}\n"
                         rf"bulk$_{{95}}$ = {b95:.3f}", pad=4)
            ax.set_xlabel(r"Re $\lambda / |\lambda_1|$", labelpad=1)
            _style(ax)
        axes[0][0].set_ylabel(r"Im $\lambda / |\lambda_1|$", labelpad=2)
        max_imag = float(primary.max_abs_imag.max())
        fig.suptitle(
            "Complex plane (human SC, seed 0). $W$ is symmetric, so the spectrum is "
            f"real: max $|$Im $\\lambda| = {max_imag:.1e}$. "
            "Star = leading mode; circle = bulk$_{95}$.",
            fontsize=8, y=1.10)
        _save(fig, path_stem)


# ---------------------------------------------------------------------------
# Supplementary: bulk95 vs f
# ---------------------------------------------------------------------------
def fig_bulk95_vs_f(summary: pd.DataFrame, scale: int, path_stem) -> None:
    sign_modes = [m for m in common.F_SIGN_MODES if m in set(summary.sign_mode)]
    with plt.rc_context(_RC):
        fig, axes = plt.subplots(1, len(sign_modes), figsize=(3.5 * len(sign_modes), 2.7),
                                 squeeze=False, sharey=True)
        for ax, sign_mode in zip(axes[0], sign_modes):
            sub = summary[summary.sign_mode == sign_mode]
            for variant in common.F_VARIANTS:
                v = sub[sub.variant == variant].sort_values("f")
                if v.empty:
                    continue
                colour = common.VARIANT_COLOR[variant]
                ax.plot(v.f, v.bulk95_mean, color=colour, lw=1.4, marker="o", ms=2.6,
                        label=common.VARIANT_TITLE[variant])
                spread = v.bulk95_std.fillna(0.0)
                ax.fill_between(v.f, v.bulk95_mean - spread, v.bulk95_mean + spread,
                                color=colour, alpha=0.15, lw=0)
            ax.set_xlabel("negative-weight fraction $f$", labelpad=1)
            ax.set_title(f"`{sign_mode}` sign mode", pad=4)
            _style(ax)
        axes[0][0].set_ylabel(r"bulk$_{95}$", labelpad=2)
        axes[0][-1].legend(loc="best", frameon=False, handlelength=1.5)
        fig.suptitle(rf"bulk$_{{95}}$ depends on $f$ (human N={scale}, "
                     f"{common.F_TARGETING})", fontsize=9, y=1.04)
        _save(fig, path_stem)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def run(scales=None) -> None:
    scales = common.SCALES if scales is None else scales
    spectra = {}
    for scale in scales:
        results_dir, _ = common.scale_dirs(scale)
        path = results_dir / "spectra_per_seed.parquet"
        if path.exists():
            spectra[scale] = pd.read_parquet(path)
            print(f"Loaded {path}  ({len(spectra[scale])} rows)")
        else:
            print(f"  [figures] {path} absent -- N={scale} omitted from Figure 1f.")
    if common.PRIMARY_SCALE not in spectra:
        raise FileNotFoundError(
            f"scale_{common.PRIMARY_SCALE}/spectra_per_seed.parquet is required for "
            f"Figure 1 -- run `--tables --scale {common.PRIMARY_SCALE}` first.")

    common.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig1(spectra, common.FIGURES_DIR / "fig1_spectrum")
    fig1_caption(spectra, common.FIGURES_DIR / "fig1_spectrum_caption.md")
    fig_complex_plane(spectra, common.FIGURES_DIR / "figS_complex_plane")

    for scale in spectra:
        results_dir, figures_dir = common.scale_dirs(scale)
        f_summary = results_dir / "bulk95_vs_f_summary.csv"
        if not f_summary.exists():
            print(f"  [figures] {f_summary} absent -- skipping bulk95-vs-f at N={scale}.")
            continue
        figures_dir.mkdir(parents=True, exist_ok=True)
        fig_bulk95_vs_f(pd.read_csv(f_summary), scale,
                        figures_dir / "figS_bulk95_vs_f")

    common.write_manifest(
        common.FIGURES_DIR / "manifest_figures.json", "E0.4 figures",
        scale=sorted(spectra),
        figure_variants=common.FIGURE_VARIANTS,
        base_condition=common.BASE_CONDITION,
        palette="Okabe-Ito (colourblind-safe)",
        outputs=["fig1_spectrum.{pdf,png}", "figS_complex_plane.{pdf,png}",
                 "scale_<N>/figS_bulk95_vs_f.{pdf,png}"],
    )

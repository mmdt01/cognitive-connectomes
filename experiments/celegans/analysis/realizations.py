"""Weight-realization comparison of the C. elegans connectome.

Characterises the *same connectome topology* under the three realism conditions
-- v2a (undirected, symmetric gaussian), v2b (directed, empirical non-negative),
v2d (directed, empirical signed/Dale) -- on the **weight axis**. Companion to the
null-ladder driver (which walks the *topology* axis): this one fixes the variant
to the connectome and walks the realism ladder of weight schemes, making the key
differences -- directionality, weight magnitude, and sign structure -- legible.

Uses the generic ``src.analysis.weight_structure`` tools for the weighted-matrix
and weight-distribution views, and reuses ``src.analysis.spectral`` for the
eigenvalue view (the dynamical consequence).

    python -m experiments.celegans.analysis.realizations

Outputs (here):
  figures/realization_weighted_matrices.png    weighted adjacency heatmaps (red +, blue −)
  figures/realization_weight_distributions.png nonzero-weight histograms (log count)
  figures/realization_eigenvalue_spectra.png   connectome spectra (λ/|λ₁|) per condition
  results/realization_summary.csv / .md        per-condition weight/spectral summary
"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np
import pandas as pd

from src.reservoir import blas  # noqa: F401  (limit BLAS threads; import early)
from src.analysis import spectral, weight_structure, null_models
from experiments.celegans.substrates import SubstrateBuilder
from experiments.celegans import matrix_config

_DIR = Path(__file__).resolve().parent
FIGURES_DIR = _DIR / "figures"
RESULTS_DIR = _DIR / "results"

CONDITIONS = matrix_config.CONDITIONS  # v2a, v2ae, v2bg, v2b, v2d
REPRESENTATIVE_SEED = 0  # gaussian-weight conditions are a draw; show one representative

CONDITION_TITLE = {
    "v2a": "Undirected Gaussian",
    "v2ae": "Undirected Empirical",
    "v2bg": "Directed Gaussian",
    "v2b": "Directed Empirical",
    "v2d": "Directed Signed (Dale)",
}
CONDITION_COLOR = {
    "v2a": "#4477aa",
    "v2ae": "#66ccee",
    "v2bg": "#ee8866",
    "v2b": "#cc6677",
    "v2d": "#9467bd",
}


def _matrix_caption(weighted: np.ndarray) -> str:
    symmetry = "symmetric" if np.allclose(weighted, weighted.T) else "asymmetric"
    nonzero = weighted[weighted != 0]
    frac_negative = float((nonzero < 0).mean()) if nonzero.size else 0.0
    if frac_negative == 0.0:
        sign = "all positive"
    elif frac_negative > 0.4:
        sign = f"{frac_negative:.0%} negative (balanced ±)"
    else:
        sign = f"{frac_negative:.1%} negative (sparse inhibition)"
    return f"{symmetry} · {sign}"


def _distribution_caption(weighted: np.ndarray, sign_coverage: dict,
                          condition: str) -> str:
    nonzero = weighted[weighted != 0]
    lines = [f"{nonzero.size} edges",
             f"|w|: mean {np.abs(nonzero).mean():.2f}, max {np.abs(nonzero).max():.1f}"]
    if condition == "v2d":
        lines.append(f"{sign_coverage['n_inhibitory']} inhibitory neurons")
    return "\n".join(lines)


def main() -> None:
    builder = SubstrateBuilder()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    matrices, weight_arrays, node_orders, boundaries, spectra = {}, {}, {}, {}, {}
    matrix_captions, distribution_captions, summary_rows = {}, {}, []

    for condition in CONDITIONS:
        weighted = builder.weighted(condition, "connectome", REPRESENTATIVE_SEED)
        topology = matrix_config.CONDITION_SPEC[condition]["topology"]
        order, block_boundaries = null_models.community_order(
            builder.partitions[topology])

        matrices[condition] = weighted
        weight_arrays[condition] = weighted[weighted != 0]
        node_orders[condition] = order
        boundaries[condition] = block_boundaries
        spectra[("connectome", condition)] = spectral.normalized_eigenvalues(weighted)
        matrix_captions[condition] = _matrix_caption(weighted)
        distribution_captions[condition] = _distribution_caption(
            weighted, builder.sign_coverage, condition)

        nonzero = weight_arrays[condition]
        eigenvalues = np.linalg.eigvals(weighted)
        summary_rows.append(dict(
            condition=condition,
            topology=topology,
            symmetric=bool(np.allclose(weighted, weighted.T)),
            n_edges=int(nonzero.size),
            frac_negative=float((nonzero < 0).mean()),
            weight_mean_abs=float(np.abs(nonzero).mean()),
            weight_max_abs=float(np.abs(nonzero).max()),
            spectral_radius=float(np.abs(eigenvalues).max()),
            frac_real_eigenvalues=float((np.abs(eigenvalues.imag) < 1e-9).mean()),
        ))

    # --- summary table --------------------------------------------------------
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(RESULTS_DIR / "realization_summary.csv", index=False)
    _write_markdown_summary(summary, RESULTS_DIR / "realization_summary.md")
    print(f"Saved {RESULTS_DIR / 'realization_summary.csv'}")
    print(f"Saved {RESULTS_DIR / 'realization_summary.md'}")

    # --- A: weighted adjacency heatmaps (headline) ----------------------------
    weight_structure.plot_weighted_matrices(
        matrices, CONDITIONS, CONDITION_TITLE, node_orders,
        FIGURES_DIR / "realization_weighted_matrices.png",
        boundaries=boundaries, panel_captions=matrix_captions,
        suptitle="Connectome weights across realizations "
                 "(nodes ordered by community; red = +, blue = −)",
    )
    print(f"Saved {FIGURES_DIR / 'realization_weighted_matrices.png'}")

    # --- B: weight-value distributions ----------------------------------------
    weight_structure.plot_weight_distributions(
        weight_arrays, CONDITIONS, CONDITION_TITLE, CONDITION_COLOR,
        FIGURES_DIR / "realization_weight_distributions.png",
        panel_captions=distribution_captions,
        suptitle="Edge-weight distributions across realizations "
                 "(gaussian → empirical heavy tail → + sparse inhibition)",
    )
    print(f"Saved {FIGURES_DIR / 'realization_weight_distributions.png'}")

    # --- C: connectome eigenvalue spectra (dynamical consequence) -------------
    spectral.plot_eigenvalue_grid(
        spectra, ["connectome"], CONDITIONS, {"connectome": "connectome"},
        CONDITION_TITLE, CONDITION_COLOR,
        FIGURES_DIR / "realization_eigenvalue_spectra.png",
        suptitle="Connectome eigenvalue spectra (λ / |λ₁|): "
                 "real-line (symmetric) → Perron + compressed bulk → signed spread",
    )
    print(f"Saved {FIGURES_DIR / 'realization_eigenvalue_spectra.png'}")

    # --- headline glance ------------------------------------------------------
    print("\nPer-condition weight summary:")
    for row in summary_rows:
        print(f"  [{row['condition']}] {row['topology']:>10}  "
              f"symmetric={row['symmetric']!s:>5}  edges={row['n_edges']}  "
              f"neg={row['frac_negative']:.1%}  "
              f"|λ₁|={row['spectral_radius']:.2f}  "
              f"real-eig={row['frac_real_eigenvalues']:.0%}")
    print("\nDone.")


def _write_markdown_summary(summary: pd.DataFrame, path: Path) -> None:
    lines = ["# C. elegans weight-realization summary (connectome)\n",
             "The same connectome under three realism conditions. `symmetric` "
             "encodes directionality (undirected ⇒ symmetric W); `frac_negative` "
             "the sign structure; `frac_real_eigenvalues` the spectral consequence "
             "(a symmetric matrix has an all-real spectrum).\n",
             "| condition | topology | symmetric | n_edges | frac_negative | "
             "mean\\|w\\| | max\\|w\\| | \\|λ₁\\| | real-eig frac |",
             "|---|---|---|---|---|---|---|---|---|"]
    for _, row in summary.iterrows():
        lines.append(
            f"| {row['condition']} | {row['topology']} | {row['symmetric']} | "
            f"{int(row['n_edges'])} | {row['frac_negative']:.3f} | "
            f"{row['weight_mean_abs']:.2f} | {row['weight_max_abs']:.1f} | "
            f"{row['spectral_radius']:.2f} | {row['frac_real_eigenvalues']:.2f} |")
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

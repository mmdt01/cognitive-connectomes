"""Weight-realization comparison of the human structural consensus.

Human analogue of ``experiments/celegans/analysis/realizations.py``. Fixes the
variant to the connectome and walks the (undirected) weight ladder --
``human_gaussian`` (symmetric gaussian, balanced ±), ``human_empirical_signed``
(real magnitudes, random ±), ``human_empirical`` (real, all-positive, heavy-tailed)
-- making the sign and magnitude structure of the *same* consensus topology
legible on the weight axis. Reuses the generic ``src.analysis.weight_structure``
and ``src.analysis.spectral`` tools.

    python -m experiments.human.analysis.realizations

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
from experiments.human.substrates import HumanSubstrateBuilder
from experiments.human import matrix_config

_DIR = Path(__file__).resolve().parent
FIGURES_DIR = _DIR / "figures"
RESULTS_DIR = _DIR / "results"

CONDITIONS = matrix_config.CONDITIONS  # human_gaussian, human_empirical_signed, human_empirical
REPRESENTATIVE_SEED = 0  # gaussian / random-sign conditions are a draw; show one

CONDITION_TITLE = {
    "human_gaussian": "Human · Gaussian",
    "human_empirical_signed": "Human · Empirical ±",
    "human_empirical": "Human · Empirical",
}
CONDITION_COLOR = {
    "human_gaussian": "#4477aa",
    "human_empirical_signed": "#88ccee",
    "human_empirical": "#cc6677",
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
        sign = f"{frac_negative:.1%} negative (sparse)"
    return f"{symmetry} · {sign}"


def _distribution_caption(weighted: np.ndarray) -> str:
    nonzero = weighted[weighted != 0]
    frac_neg = float((nonzero < 0).mean()) if nonzero.size else 0.0
    if frac_neg == 0.0:
        sign = "all positive (+)"
    elif frac_neg > 0.4:
        sign = f"{frac_neg:.0%} negative (balanced ±)"
    else:
        sign = f"{frac_neg:.1%} negative (sparse)"
    return "\n".join([
        f"{nonzero.size} edges", sign,
        f"|w|: mean {np.abs(nonzero).mean():.3g}, max {np.abs(nonzero).max():.3g}",
    ])


def main() -> None:
    builder = HumanSubstrateBuilder()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Undirected: all conditions share the consensus mask -> one community order.
    order, block_boundaries = null_models.community_order(builder.partition)

    matrices, weight_arrays, node_orders, boundaries, spectra = {}, {}, {}, {}, {}
    matrix_captions, distribution_captions, summary_rows = {}, {}, []

    for condition in CONDITIONS:
        weighted = builder.weighted(condition, "connectome", REPRESENTATIVE_SEED)
        matrices[condition] = weighted
        weight_arrays[condition] = weighted[weighted != 0]
        node_orders[condition] = order
        boundaries[condition] = block_boundaries
        spectra[("connectome", condition)] = spectral.normalized_eigenvalues(weighted)
        matrix_captions[condition] = _matrix_caption(weighted)
        distribution_captions[condition] = _distribution_caption(weighted)

        nonzero = weight_arrays[condition]
        eigenvalues = np.linalg.eigvals(weighted)
        summary_rows.append(dict(
            condition=condition,
            symmetric=bool(np.allclose(weighted, weighted.T)),
            n_edges=int(nonzero.size),
            frac_negative=float((nonzero < 0).mean()),
            weight_mean_abs=float(np.abs(nonzero).mean()),
            weight_max_abs=float(np.abs(nonzero).max()),
            spectral_radius=float(np.abs(eigenvalues).max()),
            frac_real_eigenvalues=float((np.abs(eigenvalues.imag) < 1e-9).mean()),
        ))

    summary = pd.DataFrame(summary_rows)
    summary.to_csv(RESULTS_DIR / "realization_summary.csv", index=False)
    _write_markdown_summary(summary, RESULTS_DIR / "realization_summary.md")
    print(f"Saved {RESULTS_DIR / 'realization_summary.csv'}")

    # A: weighted adjacency heatmaps (nodes ordered by community; red +, blue −)
    weight_structure.plot_weighted_matrices(
        matrices, CONDITIONS, CONDITION_TITLE, node_orders,
        FIGURES_DIR / "realization_weighted_matrices.png",
        boundaries=boundaries, panel_captions=matrix_captions,
        suptitle="Human consensus weights across realizations "
                 "(N=448, nodes ordered by community; red = +, blue = −)",
    )
    print(f"Saved {FIGURES_DIR / 'realization_weighted_matrices.png'}")

    # B: weight-value distributions (log count exposes the empirical heavy tail)
    weight_structure.plot_weight_distributions(
        weight_arrays, CONDITIONS, CONDITION_TITLE, CONDITION_COLOR,
        FIGURES_DIR / "realization_weight_distributions.png",
        panel_captions=distribution_captions,
        suptitle="Human consensus edge-weight distributions "
                 "(gaussian & signed are balanced ±; empirical is all-positive, "
                 "heavy-tailed — the sign step that drives the effect)",
    )
    print(f"Saved {FIGURES_DIR / 'realization_weight_distributions.png'}")

    # C: connectome eigenvalue spectra (the dynamical consequence)
    spectral.plot_eigenvalue_grid(
        spectra, ["connectome"], CONDITIONS, {"connectome": "connectome"},
        CONDITION_TITLE, CONDITION_COLOR,
        FIGURES_DIR / "realization_eigenvalue_spectra.png",
        suptitle="Human consensus eigenvalue spectra (λ / |λ₁|): "
                 "balanced-sign real line → all-positive Perron spike + crushed bulk",
    )
    print(f"Saved {FIGURES_DIR / 'realization_eigenvalue_spectra.png'}")

    print("\nPer-condition weight summary:")
    for row in summary_rows:
        print(f"  [{row['condition']:24s}] symmetric={row['symmetric']!s:>5}  "
              f"edges={row['n_edges']}  neg={row['frac_negative']:.1%}  "
              f"|λ₁|={row['spectral_radius']:.3g}  "
              f"real-eig={row['frac_real_eigenvalues']:.0%}")
    print("\nDone.")


def _write_markdown_summary(summary: pd.DataFrame, path: Path) -> None:
    lines = ["# Human consensus weight-realization summary (N=448 connectome)\n",
             "The same consensus topology under three undirected weight schemes. "
             "`frac_negative` encodes the sign structure; `frac_real_eigenvalues` "
             "the spectral consequence (a symmetric matrix has an all-real spectrum).\n",
             "| condition | symmetric | n_edges | frac_negative | mean\\|w\\| | "
             "max\\|w\\| | \\|λ₁\\| | real-eig frac |",
             "|---|---|---|---|---|---|---|---|"]
    for _, row in summary.iterrows():
        lines.append(
            f"| {row['condition']} | {row['symmetric']} | {int(row['n_edges'])} | "
            f"{row['frac_negative']:.3f} | {row['weight_mean_abs']:.3g} | "
            f"{row['weight_max_abs']:.3g} | {row['spectral_radius']:.3g} | "
            f"{row['frac_real_eigenvalues']:.2f} |")
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

"""Interactive 3D glass brain of the human structural consensus (nilearn).

Renders the self-built WITH-subcortical consensus (N=463) on MNI parcel centroids
with nilearn's field-standard connectome plotters (Suárez et al. use the same):

  * ``view_connectome`` -> a rotatable in-browser 3D HTML (drop straight into a
    thesis/site), nodes coloured by Yeo intrinsic network, edges by fibre-density
    weight. Output: figures/brain_connectome_interactive.html
  * ``plot_connectome`` -> a static MNI glass-brain still (ortho: sagittal/coronal/
    axial), same node colouring + strongest edges. Output:
    figures/brain_connectome_nilearn.png

Geometry (MNI coords) and Yeo groups come from ``load_routing_geometry(448)``, node
-order-matched to the with-subcortical graph, so the 15 subcortical nodes (grey,
the routing input aperture) and the 7 cortical Yeo readout apertures are all shown.
Complements the self-contained matplotlib glass brain in ``brain_overlay.py`` (that
one is cortex-only, N=448; this one is interactive and includes subcortex).

    python -m experiments.human.analysis.brain_glass_interactive

Requires nilearn (`uv pip install nilearn`; pure-CPU, no template fetch needed for
these plotters -- the MNI152 glass-brain outline is bundled).
"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np
import matplotlib
matplotlib.use("Agg")
from nilearn import plotting

from src.connectomes.human_suarez import load_routing_geometry, _BUILT_DIR

_DIR = Path(__file__).resolve().parent
FIGURES_DIR = _DIR / "figures"

SCALE = 448                    # cortical scale -> with-subcortical N=463
EDGE_TOP_FRAC_HTML = 0.10      # strongest 10% of edges in the interactive view
EDGE_TOP_FRAC_STILL = 0.015    # strongest 1.5% in the static still (less clutter)

# Same Yeo palette as the other human analysis figures + subcortical group.
YEO = {
    "VIS": "#781286", "SM": "#4682B4", "DA": "#00760E", "VA": "#C43AFA",
    "LIM": "#E8C55F", "FP": "#E69422", "DMN": "#CD3E4E", "subctx": "#8a8a8a",
}


def _edge_threshold(C: np.ndarray, top_frac: float) -> float:
    """Weight cut keeping the strongest ``top_frac`` of the non-zero edges."""
    nz = C[np.triu_indices(C.shape[0], k=1)]
    nz = nz[nz > 0]
    return float(np.quantile(nz, 1 - top_frac))


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    geo = load_routing_geometry(SCALE)
    coords = geo["coords"]                                   # (463, 3) MNI
    rsn = geo["rsn_labels"]
    C = np.load(_BUILT_DIR / f"consensus_full_{SCALE}.npy")  # (463, 463)
    N = C.shape[0]

    node_color = [YEO[str(r)] for r in rsn]
    strength = C.sum(1)
    s_norm = strength / strength.max()

    # --- interactive rotatable 3D HTML -----------------------------------------
    thr_html = _edge_threshold(C, EDGE_TOP_FRAC_HTML)
    view = plotting.view_connectome(
        C, coords,
        edge_threshold=thr_html,
        edge_cmap="YlOrRd",
        symmetric_cmap=False,          # weights are non-negative -> sequential map
        linewidth=4.0,
        node_color=node_color,
        node_size=(7.0 + 11.0 * s_norm).tolist(),
        colorbar=True,
        title=f"Human structural consensus (N={N}, with subcortical) — "
              f"nodes: Yeo network, edges: fibre density",
    )
    html_out = FIGURES_DIR / "brain_connectome_interactive.html"
    # nilearn 0.14's save_as_html writes an <iframe srcdoc="..."> wrapper; write the
    # standalone <!DOCTYPE html> document instead so it drops straight into a site.
    html_out.write_text(view.get_standalone(), encoding="utf-8")

    # --- static MNI glass-brain still (ortho) ----------------------------------
    thr_still = _edge_threshold(C, EDGE_TOP_FRAC_STILL)
    png_out = FIGURES_DIR / "brain_connectome_nilearn.png"
    display = plotting.plot_connectome(
        C, coords,
        node_color=node_color,
        node_size=(15 + 90 * s_norm),
        edge_threshold=thr_still,
        edge_cmap="YlOrRd",
        edge_vmin=0.0,
        edge_vmax=float(C.max()),
        display_mode="ortho",
        alpha=0.5,
        colorbar=True,
        node_kwargs={"edgecolors": "white", "linewidths": 0.3},
        title=f"Human structural consensus (N={N}, with subcortical)",
    )
    display.savefig(str(png_out), dpi=300)
    display.close()

    n_html = int((C[np.triu_indices(N, 1)] >= thr_html).sum())
    n_still = int((C[np.triu_indices(N, 1)] >= thr_still).sum())
    print(f"Saved {html_out}  (interactive, {n_html} edges)")
    print(f"Saved {png_out}  (ortho still, {n_still} edges)")
    print(f"  N={N} nodes ({int((rsn=='subctx').sum())} subcortical), "
          f"Yeo-coloured; open the HTML in a browser to rotate.")


if __name__ == "__main__":
    main()

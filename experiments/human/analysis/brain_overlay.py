"""Anatomical 'glass-brain' rendering of the human structural consensus (N=448).

Self-contained (matplotlib only -- no nilearn/nibabel): places each cortical node
at its MNI centroid (from the Suarez 2021 release geometry), draws a convex-hull
cortical silhouette per anatomical view, overlays the strongest consensus edges as
a faint web, and colours nodes by Yeo intrinsic network (sized by connection
strength). Three standard projections: sagittal, coronal, axial.

    python -m experiments.human.analysis.brain_overlay

Output: figures/brain_connectome_glass.png
"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull

from src.connectomes.human_suarez import _load_release_geometry, _RELEASE_DIR, _BUILT_DIR

_DIR = Path(__file__).resolve().parent
FIGURES_DIR = _DIR / "figures"

SCALE = 448
EDGE_TOP_FRAC = 0.04   # draw the strongest 4% of consensus edges

# Yeo 7-network palette (approx. the standard colours) + subcortical fallback.
YEO = {
    "VIS": "#781286", "SM": "#4682B4", "DA": "#00760E", "VA": "#C43AFA",
    "LIM": "#E8C55F", "FP": "#E69422", "DMN": "#CD3E4E", "subctx": "#8a8a8a",
}
VIEWS = [  # (name, x-axis coord, y-axis coord, xlabel, ylabel)
    ("Sagittal", 1, 2, "posterior → anterior", "inferior → superior"),
    ("Coronal", 0, 2, "left → right", "inferior → superior"),
    ("Axial", 0, 1, "left → right", "posterior → anterior"),
]


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    coords, _hemi, cidx = _load_release_geometry(SCALE)          # (448, 3) MNI
    rsn = np.load(_RELEASE_DIR / f"rsn_mapping/rsn_human_{250}.npy")[cidx]
    C = np.load(_BUILT_DIR / f"consensus_{SCALE}.npy")           # (448, 448)

    strength = C.sum(1)
    node_size = 10 + 150 * (strength / strength.max())
    node_color = [YEO.get(str(r), "#888888") for r in rsn]

    # strongest edges (upper triangle)
    iu = np.triu_indices(C.shape[0], k=1)
    w = C[iu]
    thr = np.quantile(w[w > 0], 1 - EDGE_TOP_FRAC)
    keep = w >= thr
    ei, ej, ew = iu[0][keep], iu[1][keep], w[keep]
    a_lo, a_hi = ew.min(), ew.max()

    fig, axes = plt.subplots(1, 3, figsize=(16.5, 5.6))
    for ax, (name, a, b, xl, yl) in zip(axes, VIEWS):
        P = coords[:, [a, b]]

        # cortical silhouette (convex hull of the projected centroids)
        hull = ConvexHull(P)
        ax.add_patch(Polygon(P[hull.vertices], closed=True, facecolor="0.94",
                             edgecolor="0.78", lw=1.1, zorder=0))

        # edge web (alpha ~ weight)
        for i, j, wv in zip(ei, ej, ew):
            alpha = 0.08 + 0.55 * (wv - a_lo) / (a_hi - a_lo + 1e-12)
            ax.plot([P[i, 0], P[j, 0]], [P[i, 1], P[j, 1]],
                    color="0.35", lw=0.35, alpha=alpha, zorder=1)

        # nodes
        ax.scatter(P[:, 0], P[:, 1], s=node_size, c=node_color,
                   edgecolors="white", linewidths=0.3, alpha=0.92, zorder=2)

        ax.set_title(name, fontsize=13)
        ax.set_xlabel(xl, fontsize=9)
        ax.set_ylabel(yl, fontsize=9)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)

    handles = [plt.Line2D([], [], marker="o", ls="", color=c, label=k, markersize=8)
               for k, c in YEO.items() if k != "subctx"]
    fig.legend(handles=handles, loc="lower center", ncol=7, frameon=False,
               fontsize=10, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle(
        f"Human structural consensus on the cortical surface (N={SCALE})\n"
        f"nodes at MNI centroids, coloured by Yeo network, sized by connection "
        f"strength; strongest {int(EDGE_TOP_FRAC*100)}% of edges shown",
        fontsize=13)
    fig.tight_layout(rect=[0, 0.05, 1, 0.92])
    out = FIGURES_DIR / "brain_connectome_glass.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}  ({len(ei)} edges drawn, {C.shape[0]} nodes)")


if __name__ == "__main__":
    main()

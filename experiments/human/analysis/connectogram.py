"""Yeo-network connectogram of the human structural consensus (with subcortical).

Self-contained (matplotlib only): places every node of the WITH-subcortical
consensus (N=463) on a circle, grouped into contiguous arcs by Yeo intrinsic
network (VIS/SM/DA/VA/LIM/FP/DMN) with subcortical as an eighth group, then draws
the strongest consensus edges as Bezier arcs bundled toward the centre. Edges are
coloured by the network pair they join: WITHIN-network edges take that network's
colour (bold), BETWEEN-network edges are a faint grey web -- making within- vs
between-network structure pop. Node ticks are sized by connection strength.

Built on the same self-built with-subcortical substrate as the routing thread
(``consensus_full_448.npy``, N=463) with geometry / Yeo groups from
``load_routing_geometry`` -- so the subcortical input aperture and the seven
cortical Yeo readout apertures (Suárez's I/O routing subsets) are all visible.

    python -m experiments.human.analysis.connectogram

Output: figures/connectogram_yeo.png
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
from matplotlib.patches import Wedge, Patch
from matplotlib.collections import LineCollection

from src.connectomes.human_suarez import load_routing_geometry, _BUILT_DIR

_DIR = Path(__file__).resolve().parent
FIGURES_DIR = _DIR / "figures"

SCALE = 448                 # cortical scale -> with-subcortical N=463
EDGE_TOP_FRAC = 0.03        # draw the strongest 3% of consensus edges
R = 1.0                     # node ring radius
GROUP_GAP_DEG = 4.0         # angular gap between network wedges
BEND = 0.55                 # 0 = straight chords, 1 = bundle through centre

# Same Yeo palette as brain_connectome_glass.png / structure_by_yeo_network.png,
# plus the subcortical group (the routing input aperture).
YEO = {
    "VIS": "#781286", "SM": "#4682B4", "DA": "#00760E", "VA": "#C43AFA",
    "LIM": "#E8C55F", "FP": "#E69422", "DMN": "#CD3E4E", "subctx": "#8a8a8a",
}
# Ring order: the 7 cortical networks (canonical) then the subcortical aperture.
GROUP_ORDER = ["VIS", "SM", "DA", "VA", "LIM", "FP", "DMN", "subctx"]


def _bezier(p1: np.ndarray, p2: np.ndarray, n: int = 64) -> np.ndarray:
    """Quadratic Bezier from p1 to p2 with the control point pulled toward the
    centre by ``BEND`` (so arcs bow inward; longer chords bundle deeper)."""
    ctrl = 0.5 * (p1 + p2) * (1.0 - BEND)
    t = np.linspace(0.0, 1.0, n)[:, None]
    return (1 - t) ** 2 * p1 + 2 * (1 - t) * t * ctrl + t ** 2 * p2


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    geo = load_routing_geometry(SCALE)
    rsn = geo["rsn_labels"]                                   # (N,) str per node
    hemiid = geo["hemiid"]
    C = np.load(_BUILT_DIR / f"consensus_full_{SCALE}.npy")   # (463, 463)
    N = C.shape[0]

    groups = [g for g in GROUP_ORDER if (rsn == g).any()]
    # Node ordering: contiguous by group; within a group sort by hemisphere then
    # index, so the two hemispheres cluster within each network arc.
    order, spans = [], {}                       # spans[g] = (start, stop) in `order`
    for g in groups:
        idx = np.where(rsn == g)[0]
        idx = idx[np.lexsort((idx, hemiid[idx]))]
        spans[g] = (len(order), len(order) + len(idx))
        order.extend(idx.tolist())
    order = np.array(order)
    pos_of = np.empty(N, dtype=int)             # node index -> slot on the ring
    pos_of[order] = np.arange(N)

    # Angles: each group gets an arc proportional to its node count, with a fixed
    # gap between groups. Angles run clockwise from the top (12 o'clock).
    n_gap = len(groups)
    span_deg = 360.0 - n_gap * GROUP_GAP_DEG
    angles = np.zeros(N)
    group_arcs = {}                             # g -> (theta0, theta1) degrees
    cursor = 90.0                               # start at top
    for g in groups:
        s, e = spans[g]
        arc = span_deg * (e - s) / N
        # place this group's nodes evenly inside its arc (clockwise -> subtract)
        inner = np.linspace(cursor - arc * 0.02, cursor - arc * 0.98, e - s)
        angles[np.arange(s, e)] = inner
        group_arcs[g] = (cursor, cursor - arc)
        cursor -= arc + GROUP_GAP_DEG
    rad = np.deg2rad(angles)
    ring = np.column_stack([R * np.cos(rad), R * np.sin(rad)])   # slot -> xy

    # Strongest edges (upper triangle).
    iu = np.triu_indices(N, k=1)
    w = C[iu]
    nz = w[w > 0]
    thr = np.quantile(nz, 1 - EDGE_TOP_FRAC)
    keep = w >= thr
    ei, ej, ew = iu[0][keep], iu[1][keep], w[keep]
    ew_norm = (ew - ew.min()) / (ew.max() - ew.min() + 1e-12)

    within = rsn[ei] == rsn[ej]
    strength = C.sum(1)
    node_size = 6 + 90 * (strength / strength.max())

    fig, ax = plt.subplots(figsize=(11, 11))
    ax.set_aspect("equal")
    ax.axis("off")

    # --- edges: between-network first (faint grey), within-network on top -------
    def _draw(mask, colors, lw, alpha_base, alpha_span, zorder):
        segs, cols, lws = [], [], []
        for k in np.where(mask)[0]:
            p1, p2 = ring[pos_of[ei[k]]], ring[pos_of[ej[k]]]
            segs.append(_bezier(p1, p2))
            a = alpha_base + alpha_span * ew_norm[k]
            c = colors[k]
            cols.append((*matplotlib.colors.to_rgb(c), a))
            lws.append(lw * (0.5 + ew_norm[k]))
        if segs:
            ax.add_collection(LineCollection(segs, colors=cols, linewidths=lws,
                                             zorder=zorder, capstyle="round"))

    _draw(~within, ["#9a9a9a"] * len(ei), 0.6, 0.05, 0.22, zorder=1)
    within_cols = [YEO[str(rsn[ei[k]])] for k in range(len(ei))]
    _draw(within, within_cols, 1.5, 0.30, 0.55, zorder=2)

    # --- nodes ------------------------------------------------------------------
    node_cols = [YEO[str(rsn[order[s]])] for s in range(N)]
    ax.scatter(ring[:, 0], ring[:, 1], s=node_size[order], c=node_cols,
               edgecolors="white", linewidths=0.25, zorder=3)

    # --- outer coloured group band + labels -------------------------------------
    band_r0, band_r1 = R * 1.02, R * 1.07
    for g in groups:
        t_hi, t_lo = group_arcs[g]              # degrees (t_hi > t_lo, clockwise)
        ax.add_patch(Wedge((0, 0), band_r1, t_lo, t_hi, width=band_r1 - band_r0,
                           facecolor=YEO[g], edgecolor="white", lw=0.8, zorder=2))
        mid = np.deg2rad((t_hi + t_lo) / 2)
        lr = R * 1.16
        ax.text(lr * np.cos(mid), lr * np.sin(mid), g, ha="center", va="center",
                fontsize=11, fontweight="bold", color=YEO[g],
                rotation=0, zorder=4)

    ax.set_xlim(-1.28, 1.28)
    ax.set_ylim(-1.28, 1.28)

    frac_within = within.mean()
    handles = [
        plt.Line2D([], [], color="0.6", lw=1.4, label="between-network edge"),
        plt.Line2D([], [], color=YEO["DMN"], lw=2.2, label="within-network edge"),
    ]
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.06),
              ncol=2, frameon=False, fontsize=10)
    fig.suptitle(
        f"Human structural consensus connectogram — Yeo networks (N={N}, with subcortical)\n"
        f"strongest {int(EDGE_TOP_FRAC*100)}% of edges; within-network coloured by network, "
        f"between-network in grey ({frac_within:.0%} of strong edges are within-network)",
        fontsize=13, y=0.995)
    fig.tight_layout(rect=[0, 0.02, 1, 0.95])
    out = FIGURES_DIR / "connectogram_yeo.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved {out}")
    print(f"  nodes={N}  edges drawn={len(ei)}  "
          f"within-network={within.sum()} ({frac_within:.1%})  "
          f"between-network={(~within).sum()}")
    print("  group sizes:", {g: int((rsn == g).sum()) for g in groups})


if __name__ == "__main__":
    main()

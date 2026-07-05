"""Human structural consensus reordered by Yeo FUNCTIONAL networks.

Visualises the structure-function relationship: the (structural) consensus SC is
reordered so nodes are grouped by their Yeo intrinsic-network (functional) label,
with the same network colours as brain_connectome_glass.png. Strong within-network
(block-diagonal) structural connectivity => structure follows function. A companion
7x7 panel shows the network-averaged structural connectivity directly.

    python -m experiments.human.analysis.network_matrix

Output: figures/structure_by_yeo_network.png
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
import matplotlib.colors as mcolors
from matplotlib.colors import LogNorm
from matplotlib.patches import Patch
from mpl_toolkits.axes_grid1 import make_axes_locatable

from src.connectomes.human_suarez import _load_release_geometry, _RELEASE_DIR, _BUILT_DIR

_DIR = Path(__file__).resolve().parent
FIGURES_DIR = _DIR / "figures"
SCALE = 448

# Same palette as brain_connectome_glass.png
YEO = {"VIS": "#781286", "SM": "#4682B4", "DA": "#00760E", "VA": "#C43AFA",
       "LIM": "#E8C55F", "FP": "#E69422", "DMN": "#CD3E4E"}
CANON = ["VIS", "SM", "DA", "VA", "LIM", "FP", "DMN"]


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    _, _hemi, cidx = _load_release_geometry(SCALE)
    rsn = np.load(_RELEASE_DIR / "rsn_mapping/rsn_human_250.npy")[cidx].astype(str)
    C = np.load(_BUILT_DIR / f"consensus_{SCALE}.npy")

    nets = [n for n in CANON if (rsn == n).any()]
    # node order grouped by network; boundaries + tick centres
    order, bounds, centres = [], [], []
    for n in nets:
        idx = np.where(rsn == n)[0]
        start = len(order)
        order.extend(idx.tolist())
        centres.append((start + len(order) - 1) / 2)
        bounds.append(len(order))
    order = np.array(order)
    strip = np.array([mcolors.to_rgb(YEO[rsn[i]]) for i in order])  # (N,3)

    M = C[np.ix_(order, order)]
    Mm = np.ma.masked_where(M <= 0, M)
    nz = C[C > 0]
    vmin, vmax = np.percentile(nz, 10), np.percentile(nz, 99.5)

    # network-averaged (7x7) structural connectivity
    K = len(nets)
    netmean = np.zeros((K, K))
    for a, na in enumerate(nets):
        ia = np.where(rsn == na)[0]
        for b, nb in enumerate(nets):
            ib = np.where(rsn == nb)[0]
            blk = C[np.ix_(ia, ib)].astype(float)
            if na == nb:
                blk = blk.copy(); np.fill_diagonal(blk, np.nan)
            netmean[a, b] = np.nanmean(blk)

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(15, 6.6),
                                   gridspec_kw={"width_ratios": [3, 2]})

    # --- Panel A: full matrix, nodes grouped by Yeo network -------------------
    imA = axA.imshow(Mm, cmap="magma", norm=LogNorm(vmin=vmin, vmax=vmax),
                     interpolation="nearest")
    imA.cmap.set_bad("0.96")
    for b in bounds[:-1]:
        axA.axhline(b - 0.5, color="w", lw=0.6, alpha=0.7)
        axA.axvline(b - 0.5, color="w", lw=0.6, alpha=0.7)
    axA.set_xticks([]); axA.set_yticks([])
    axA.set_title("Structural consensus, nodes grouped by Yeo network\n"
                  "(bright block-diagonal = within-network structure)", fontsize=12)
    # coloured network strips (top + left) via a divider
    div = make_axes_locatable(axA)
    top = div.append_axes("top", size="3.5%", pad=0.04, sharex=axA)
    left = div.append_axes("left", size="3.5%", pad=0.04, sharey=axA)
    top.imshow(strip[np.newaxis, :, :], aspect="auto",
               extent=[-0.5, len(order) - 0.5, 0, 1])
    left.imshow(strip[:, np.newaxis, :], aspect="auto",
                extent=[0, 1, len(order) - 0.5, -0.5])
    for s in (top, left):
        s.set_xticks([]); s.set_yticks([])
    fig.colorbar(imA, ax=axA, fraction=0.046, pad=0.04,
                 label="structural weight (fibre density, log)")

    # --- Panel B: network-averaged 7x7 ----------------------------------------
    imB = axB.imshow(netmean, cmap="magma",
                     norm=LogNorm(vmin=netmean[netmean > 0].min(), vmax=netmean.max()),
                     interpolation="nearest")
    axB.set_xticks(range(K)); axB.set_yticks(range(K))
    axB.set_xticklabels(nets, rotation=45, ha="right")
    axB.set_yticklabels(nets)
    for t, n in zip(axB.get_xticklabels(), nets): t.set_color(YEO[n])
    for t, n in zip(axB.get_yticklabels(), nets): t.set_color(YEO[n])
    for spine in axB.spines.values(): spine.set_visible(False)
    axB.set_title("Network-averaged structural connectivity\n"
                  "(diagonal brightest = structure follows function)", fontsize=12)
    fig.colorbar(imB, ax=axB, fraction=0.046, pad=0.04,
                 label="mean structural weight (log)")

    handles = [Patch(facecolor=YEO[n], label=n) for n in nets]
    fig.legend(handles=handles, loc="lower center", ncol=K, frameon=False,
               fontsize=10, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("Human structural connectivity ordered by functional (Yeo) networks — "
                 f"N={SCALE} consensus", fontsize=14)
    fig.tight_layout(rect=[0, 0.04, 1, 0.94])
    out = FIGURES_DIR / "structure_by_yeo_network.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved {out}")
    print("Network sizes:", {n: int((rsn == n).sum()) for n in nets})
    within = np.diag(netmean).mean()
    off = netmean[~np.eye(K, dtype=bool)].mean()
    print(f"mean within-network weight = {within:.2e}  vs  between = {off:.2e}  "
          f"(ratio {within/off:.1f}x)")


if __name__ == "__main__":
    main()

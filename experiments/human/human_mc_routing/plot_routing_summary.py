"""Presentation figure (Suárez 2021 Fig 1c style): memory capacity vs spectral
radius for each Yeo intrinsic-network readout, under anatomical routing
(subcortical input), mean +/- SD across seeds.

    python -m experiments.human.human_mc_routing.plot_routing_summary            # both scales
    python -m experiments.human.human_mc_routing.plot_routing_summary --scale 448

Reads the existing full-run ``results.parquet`` (10 seeds already) -- no re-run.
The 7 lines are the connectome (real W, subcortical input) read through each Yeo
network; the shaded band is +/- 1 SD over seeds. A dashed marker at sr=1 flags the
edge of chaos (where these concentrated-input readouts peak).
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

_DIR = Path(__file__).resolve().parent

# Canonical Yeo-7 colours (domain convention). Limbic darkened from its pale cream
# and Frontoparietal deepened for legibility on white; CVD-separation validated
# (worst adjacent deltaE 18.2, above the 12 target). Identity is never colour-alone
# -- a legend is always shown.
YEO_ORDER = ["VIS", "SM", "DA", "VA", "LIM", "FP", "DMN"]
YEO_COLOR = {
    "VIS": "#781286", "SM": "#4682B4", "DA": "#00760E", "VA": "#C43AFA",
    "LIM": "#8A7A00", "FP": "#C86400", "DMN": "#CD3E4E",
}
YEO_FULL = {
    "VIS": "Visual", "SM": "Somatomotor", "DA": "Dorsal attention",
    "VA": "Ventral attention", "LIM": "Limbic", "FP": "Frontoparietal",
    "DMN": "Default mode",
}


def make_figure(scale: int, sr_min: float = 0.2, sr_max: float = 3.5,
                normalize: str = "peak") -> Path:
    # sr window: start at 0.2 (matches Suárez Fig 1c; skips the trivial near-zero
    # rise) and stop at 3.5 (past that the seed variance blows up and muddies the
    # bands). Raise sr_max to 6 to show the full collapse tail.
    res = pd.read_parquet(_DIR / f"results/scale_{scale}/results.parquet")
    conn = res[(res.variant == "connectome")
               & (res.spectral_radius >= sr_min)
               & (res.spectral_radius <= sr_max)]
    n_seeds = int(conn.seed.nunique())
    sr = np.array(sorted(conn.spectral_radius.unique()))

    means, sds = {}, {}
    for net in YEO_ORDER:
        g = conn.groupby("spectral_radius")[f"mc_{net}"]
        means[net] = g.mean().reindex(sr).to_numpy()
        sds[net] = g.std(ddof=1).reindex(sr).to_numpy()

    # Normalisation. Raw MC scales with readout SIZE (a bigger network reads more
    # of the reservoir's memory), so raw between-network heights largely reflect
    # network size, not dynamics. Suárez report MC in [0,1]; matching that also
    # removes the size confound and focuses the comparison on peak LOCATION and
    # decay SHAPE. "peak" = each network to its own peak; "global" = all by the one
    # global max (cosmetic, keeps the size-confounded ordering); "none" = raw.
    if normalize == "peak":
        for net in YEO_ORDER:
            f = np.nanmax(means[net]) or 1.0
            means[net], sds[net] = means[net] / f, sds[net] / f
        ylabel = "memory capacity  (normalised to each network's peak)"
    elif normalize == "global":
        f = max(np.nanmax(m) for m in means.values()) or 1.0
        for net in YEO_ORDER:
            means[net], sds[net] = means[net] / f, sds[net] / f
        ylabel = "memory capacity  (normalised, global max = 1)"
    else:
        ylabel = "memory capacity"

    fig, ax = plt.subplots(figsize=(7.6, 5.3))
    for net in YEO_ORDER:
        c = YEO_COLOR[net]
        ax.fill_between(sr, means[net] - sds[net], means[net] + sds[net],
                        color=c, alpha=0.15, lw=0, zorder=2)
        ax.plot(sr, means[net], color=c, lw=2.0, label=YEO_FULL[net], zorder=3)

    ax.axvline(1.0, color="0.55", lw=1.0, ls="--", zorder=1)
    ax.set_xlim(sr_min, sr_max)
    ax.set_ylim(bottom=0)
    top = ax.get_ylim()[1]
    ax.annotate("edge of chaos (sr = 1)", xy=(1.0, top), xytext=(1.08, top * 0.97),
                fontsize=8.5, color="0.4")

    ax.set_xlabel("spectral radius", fontsize=11)
    ax.set_ylabel(ylabel, fontsize=10.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(alpha=0.2, lw=0.6)
    ax.tick_params(labelsize=10)
    ax.legend(title="readout network", frameon=False, fontsize=9.5,
              title_fontsize=9.5, loc="center left", bbox_to_anchor=(1.01, 0.5),
              handlelength=1.6, labelspacing=0.45)
    ax.text(0.015, 0.03, f"shaded band: mean ± 1 SD ({n_seeds} seeds)",
            transform=ax.transAxes, fontsize=8.5, color="0.45")
    ax.set_title(
        "Anatomical I/O routing: memory capacity by intrinsic-network readout\n"
        f"human SC (Lausanne N={scale} cortical + 15 subcortical); "
        "input → subcortex, readout → each Yeo network",
        fontsize=11.5, loc="left")

    fig.tight_layout()
    suffix = "" if normalize == "none" else f"_{normalize}norm"
    out = _DIR / f"figures/scale_{scale}/mc_by_network_routing{suffix}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return out


def _flag(argv, flag, default, cast=int):
    for i, a in enumerate(argv):
        if a == flag and i + 1 < len(argv):
            return cast(argv[i + 1])
        if a.startswith(flag + "="):
            return cast(a.split("=", 1)[1])
    return default


if __name__ == "__main__":
    scale = _flag(sys.argv, "--scale", None, int)
    sr_min = _flag(sys.argv, "--sr-min", 0.2, float)
    sr_max = _flag(sys.argv, "--sr-max", 3.5, float)
    norm = _flag(sys.argv, "--norm", "peak", str)  # peak | global | none
    scales = [scale] if scale else [448, 1000]
    for s in scales:
        print("Saved", make_figure(s, sr_min=sr_min, sr_max=sr_max, normalize=norm))

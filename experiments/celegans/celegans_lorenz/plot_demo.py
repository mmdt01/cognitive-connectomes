"""Illustrative figure: closed-loop Lorenz free-running by the connectome reservoir.

Reproduces a single experiment cell exactly (same frozen hyperparameters and seed
convention), teacher-forces the readout, then cuts the reservoir loose to
free-run autonomously. Draws (left) the true trajectory and the free-run overlaid
per coordinate, with the valid-prediction-time horizon marked where they diverge,
and (right) the generated vs true attractor in 3-D -- the intuition for the two
metrics: how long the free-run tracks (vpt) and whether its cloud matches the
true attractor's shape (climate).

    python -m experiments.celegans.celegans_lorenz.plot_demo
"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src.reservoir.build import build_from_adjacency
from src.tasks import lorenz
from src.tasks.lorenz import (
    build_trajectory, _fit_ridge_readout, _extract_reservoir, _reset,
    _sync_state, _free_run, _valid_prediction_time,
)
from experiments.celegans.substrates import SubstrateBuilder
from experiments.celegans.celegans_lorenz.run import build_config

# The cells to showcase. Two honest, contrasting experiment cells:
#   1. The real connectome at its canonical operating point -- collapses to a
#      fixed point after ~1.4 Lyapunov times (poor climate; the headline result).
#   2. The weight-placement control supercritically -- the best-performing cell in
#      the sweep: free-runs faithfully for ~6 Lyapunov times and reproduces the
#      attractor (near-zero climate). Scrambling the connectome's weight placement
#      is exactly what unlocks this, so the pair visualises the placement effect.
DEMOS = [
    dict(condition="directed_empirical", variant="connectome", spectral_radius=0.95, seed=0,
         out="lorenz_dynamics_demo.png"),
    dict(condition="directed_empirical_dale", variant="connectome_weight_permuted",
         spectral_radius=1.8947, seed=0,
         out="lorenz_dynamics_demo_v2d_control_sr1.9.png"),
]
SHOW_LYAP = 8.0          # Lyapunov times of free-run to draw in the time series

# Readable variant labels for the figure caption.
_VARIANT_LABEL = {
    "connectome": "connectome",
    "connectome_weight_permuted": "connectome · permuted weights (placement control)",
}


def render(builder: SubstrateBuilder, condition: str, variant: str,
           spectral_radius: float, seed: int, out: str) -> None:
    cfg = build_config("vpt")
    p = cfg.task_params

    weighted = builder.weighted(condition, variant, seed)
    reservoir = build_from_adjacency(
        weighted_adjacency=weighted, target_spectral_radius=spectral_radius,
        leak_rate=cfg.leak_rate, input_scaling=cfg.input_scaling, seed=seed,
        input_dim=cfg.input_dim,
    )

    # Reproduce the experiment cell: z-scored trajectory, teacher-forced readout.
    S, holdout_start, _, _ = build_trajectory(
        seed + cfg.input_seed_offset, p["n_transient"], p["washout"], p["n_train"],
        p["sync_len"], p["n_windows"], p["window_spacing"], p["free_run_len"],
        p["sigma"], p["rho"], p["beta"], p["h"], p["x0"],
    )
    _reset(reservoir)
    states = reservoir.run(S[p["n_transient"]:holdout_start])[p["washout"]:]
    next_state = S[p["n_transient"] + p["washout"] + 1: holdout_start + 1]
    weights = _fit_ridge_readout(states, next_state, p["ridge_alpha"], p["readout_bias"])
    W, Win, lr, bias = _extract_reservoir(reservoir)
    rms_norm = float(np.sqrt(np.mean(np.sum(S[p["n_transient"]:holdout_start] ** 2, axis=1))))

    # One representative free-run from the first held-out synchronisation point.
    g = holdout_start
    x = _sync_state(reservoir, S[g - p["sync_len"]: g])
    free = _free_run(x, weights, p["readout_bias"], W, Win, lr, bias, p["free_run_len"])
    truth = S[g: g + p["free_run_len"]]
    vpt = _valid_prediction_time(free, truth, rms_norm, p["epsilon"], p["h"], p["lambda_max"])

    # A long free-run for the attractor (climate) panel.
    x = _sync_state(reservoir, S[g - p["sync_len"]: g])
    long_free = _free_run(x, weights, p["readout_bias"], W, Win, lr, bias, p["climate_len"])
    long_true = S[p["n_transient"]:]

    lyap = np.arange(p["free_run_len"]) * p["h"] * p["lambda_max"]
    n_show = int(np.searchsorted(lyap, SHOW_LYAP))
    coord_names = ["x", "y", "z"]

    fig = plt.figure(figsize=(13, 5.2))
    gs = fig.add_gridspec(3, 2, width_ratios=[1.7, 1.0], hspace=0.18, wspace=0.18)

    for d in range(3):
        ax = fig.add_subplot(gs[d, 0])
        ax.plot(lyap[:n_show], truth[:n_show, d], color="black", lw=1.8,
                label="true" if d == 0 else None)
        ax.plot(lyap[:n_show], free[:n_show, d], color="#d62728", lw=1.5, ls="--",
                label="free-run" if d == 0 else None)
        ax.axvline(vpt, color="#1f77b4", lw=1.4, ls=":")
        ax.set_ylabel(f"${coord_names[d]}$ (z)")
        ax.margins(x=0.01)
        if d < 2:
            ax.set_xticklabels([])
        if d == 0:
            ax.legend(loc="upper right", fontsize=8, framealpha=0.95)
            ax.set_title(f"Closed-loop free-run vs truth  (vpt = {vpt:.2f} Lyapunov times)",
                         fontsize=11)
    ax.set_xlabel("Lyapunov time  $t\\,\\lambda_{max}$")
    ax.text(vpt, ax.get_ylim()[0], "  vpt", color="#1f77b4", fontsize=8,
            ha="left", va="bottom")

    ax3d = fig.add_subplot(gs[:, 1], projection="3d")
    ax3d.plot(long_true[:, 0], long_true[:, 1], long_true[:, 2],
              color="#bbbbbb", lw=0.3, label="true attractor")
    if np.all(np.isfinite(long_free)):
        ax3d.plot(long_free[:, 0], long_free[:, 1], long_free[:, 2],
                  color="#d62728", lw=0.3, label="free-run")
    ax3d.set_title("Generated vs true attractor (climate)", fontsize=11)
    ax3d.set_xlabel("$x$"); ax3d.set_ylabel("$y$"); ax3d.set_zlabel("$z$")
    ax3d.legend(loc="upper left", fontsize=8)

    label = cfg.condition_spec[condition]["label"]
    fig.text(0.5, 0.005, f"substrate: {label}, {_VARIANT_LABEL.get(variant, variant)}  ·  "
             f"spectral radius {spectral_radius}  ·  seed {seed}",
             ha="center", fontsize=8, color="grey")

    cfg.figures_dir.mkdir(parents=True, exist_ok=True)
    out_path = cfg.figures_dir / out
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    climate_str = (f"{_climate_of(long_free[p['climate_washout']:], long_true):.3f}"
                   if np.all(np.isfinite(long_free)) else "diverged")
    print(f"{condition}/{variant} sr={spectral_radius}: vpt = {vpt:.2f} Lyapunov times, "
          f"climate = {climate_str}  ->  saved {out_path}")


def _climate_of(free, reference):
    from scipy.stats import wasserstein_distance
    return float(np.mean([wasserstein_distance(free[:, d], reference[:, d]) for d in range(3)]))


def main() -> None:
    builder = SubstrateBuilder()  # one builder, reused across demos
    for spec in DEMOS:
        render(builder, **spec)


if __name__ == "__main__":
    main()

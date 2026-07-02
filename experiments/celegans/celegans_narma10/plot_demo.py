"""Illustrative figure: NARMA-10 dynamics + the connectome reservoir's prediction.

Reproduces a single experiment cell exactly (same frozen hyperparameters and
seed convention), then draws a window spanning the train -> held-out-test
boundary: the random input on top, and the NARMA-10 target with the reservoir's
prediction overlaid on the held-out region below.

    python -m experiments.celegans.celegans_narma10.plot_demo
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
from src.tasks.narma import (
    narma10,
    _generate_input_and_target,
    _fit_ridge_readout,
    _predict,
)
from experiments.celegans.substrates import SubstrateBuilder
from experiments.celegans.celegans_narma10.run import build_config

# Which connectome reservoir to showcase (a single, honest experiment cell).
CONDITION = "directed_empirical"        # directed empirical -- the biologically realistic substrate
VARIANT = "connectome"
SPECTRAL_RADIUS = 0.95   # canonical operating point
SEED = 6                 # representative seed (NRMSE 0.49, near the 0.55 mean)

# How much of the train/test boundary window to draw.
SHOW_BEFORE = 40         # train steps shown before the boundary
SHOW_AFTER = 160         # held-out test steps shown after the boundary


def main() -> None:
    cfg = build_config()
    params = cfg.task_params
    washout, n_train, n_test = params["washout"], params["n_train"], params["n_test"]

    builder = SubstrateBuilder()
    weighted = builder.weighted(CONDITION, VARIANT, SEED)
    reservoir = build_from_adjacency(
        weighted_adjacency=weighted,
        target_spectral_radius=SPECTRAL_RADIUS,
        leak_rate=cfg.leak_rate,
        input_scaling=cfg.input_scaling,
        seed=SEED,
    )

    # Same input stream + split as the experiment for this seed.
    rng = np.random.default_rng(SEED + cfg.input_seed_offset)
    u, y, _ = _generate_input_and_target(
        rng, params["T"], params["u_low"], params["u_high"],
        params["divergence_bound"], params["max_input_tries"],
    )
    if getattr(reservoir, "state", None) is not None:
        reservoir.reset()
    states = reservoir.run(u.reshape(-1, 1))[washout:]
    targets = y[washout:]

    train_states, train_targets = states[:n_train], targets[:n_train]
    test_states = states[n_train:n_train + n_test]
    test_targets = targets[n_train:n_train + n_test]

    weights, _ = _fit_ridge_readout(
        train_states, train_targets, params["ridge_alpha"], params["readout_bias"]
    )
    predictions = _predict(test_states, weights, params["readout_bias"])
    nrmse = float(np.sqrt(np.mean((predictions - test_targets) ** 2)
                          / np.var(test_targets)))

    # Window around the train -> test boundary (in post-washout step index).
    lo, hi = n_train - SHOW_BEFORE, n_train + SHOW_AFTER
    steps = np.arange(lo, hi)
    target_window = targets[lo:hi]
    pred_steps = np.arange(n_train, hi)
    pred_window = predictions[:SHOW_AFTER]
    input_window = u[washout + lo:washout + hi]

    fig, (ax_u, ax_y) = plt.subplots(
        2, 1, figsize=(11, 5.2), sharex=True,
        gridspec_kw=dict(height_ratios=[1, 3], hspace=0.12),
    )

    ax_u.plot(steps, input_window, color="#7f7f7f", lw=1.0)
    ax_u.set_ylabel("input\n$u(t)$", fontsize=9)
    ax_u.set_title("NARMA-10: random input drives the system; "
                   "the connectome reservoir predicts the held-out target",
                   fontsize=12)
    ax_u.margins(x=0.005)

    ax_y.axvspan(n_train, hi, color="#fff3e0", zorder=0)
    ax_y.axvline(n_train, color="grey", lw=1.0, ls="--", zorder=1)
    ax_y.plot(steps, target_window, color="black", lw=2.0,
              label="NARMA-10 target $y(t)$", zorder=3)
    ax_y.plot(pred_steps, pred_window, color="#d62728", lw=1.8, ls="--",
              label="reservoir prediction $\\hat{y}(t)$", zorder=4)
    ax_y.set_ylabel("system output $y(t)$")
    ax_y.set_xlabel("time step (after washout)")
    ax_y.legend(loc="upper left", fontsize=9, framealpha=0.95)
    ax_y.margins(x=0.005)

    ax_y.text(n_train + 0.5 * SHOW_AFTER, 0.04, "held-out test", color="#b35900",
              ha="center", va="bottom", fontsize=9)
    ax_y.text(n_train - 0.5 * SHOW_BEFORE, 0.04, "training", color="grey",
              ha="center", va="bottom", fontsize=9)
    ax_y.text(0.985, 0.93, f"test NRMSE = {nrmse:.3f}", transform=ax_y.transAxes,
              ha="right", va="top", fontsize=10,
              bbox=dict(boxstyle="round", fc="white", ec="grey", alpha=0.9))

    label = cfg.condition_spec[CONDITION]["label"]
    fig.text(0.5, 0.005, f"substrate: {label}, connectome  ·  "
             f"spectral radius {SPECTRAL_RADIUS}  ·  seed {SEED}",
             ha="center", fontsize=8, color="grey")

    cfg.figures_dir.mkdir(parents=True, exist_ok=True)
    out = cfg.figures_dir / "narma_dynamics_demo.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"test NRMSE = {nrmse:.3f}")
    print(f"Saved {out}")


if __name__ == "__main__":
    main()

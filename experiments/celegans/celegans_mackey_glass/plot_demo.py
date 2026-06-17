"""Illustrative figure: Mackey-Glass dynamics + the connectome's held-out forecast.

Reproduces a single experiment cell exactly (same frozen hyperparameters and
seed convention), then draws a window spanning the train -> held-out-test
boundary: the Mackey-Glass series that drives the reservoir on top, and the
horizon-step-ahead target with the reservoir's forecast overlaid on the held-out
region below. Rendered at **both** horizons -- the moderate one (the forecast
visibly tracks) and the hard one (chaos-limited: the forecast holds the gross
oscillation but drifts in phase) -- one figure per horizon directory.

    python -m experiments.celegans.celegans_mackey_glass.plot_demo
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
from src.tasks.mackey_glass import build_driven_series, _fit_ridge_readout, _predict
from experiments.celegans.substrates import SubstrateBuilder
from experiments.celegans.celegans_mackey_glass.run import build_config
from experiments.celegans.celegans_mackey_glass.task_config import HORIZONS

# Which connectome reservoir to showcase (a single, honest experiment cell).
CONDITION = "v2b"        # directed empirical -- the biologically realistic substrate
VARIANT = "connectome"
SPECTRAL_RADIUS = 0.95   # canonical operating point
SEED = 0                 # representative seed

# How much of the train/test boundary window to draw (MG period ~50 steps).
SHOW_BEFORE = 60         # train steps shown before the boundary
SHOW_AFTER = 300         # held-out test steps shown after the boundary


def render(builder: SubstrateBuilder, horizon: int) -> None:
    cfg = build_config(horizon)
    params = cfg.task_params
    washout, n_train, n_test = params["washout"], params["n_train"], params["n_test"]

    weighted = builder.weighted(CONDITION, VARIANT, SEED)
    reservoir = build_from_adjacency(
        weighted_adjacency=weighted,
        target_spectral_radius=SPECTRAL_RADIUS,
        leak_rate=cfg.leak_rate,
        input_scaling=cfg.input_scaling,
        seed=SEED,
    )

    # Same driven series + split as the experiment for this seed (z-scored), then
    # de-normalise back to physical Mackey-Glass units for the plot.
    input_norm, target_norm, mean, std = build_driven_series(
        SEED + cfg.input_seed_offset, params["T"], washout, n_train, horizon,
        params["n_transient"], params["tau"], params["a"], params["b"],
        params["n"], params["x0"], params["h"],
    )
    if getattr(reservoir, "state", None) is not None:
        reservoir.reset()
    states = reservoir.run(input_norm.reshape(-1, 1))[washout:]
    targets = target_norm[washout:]

    train_states, train_targets = states[:n_train], targets[:n_train]
    test_states = states[n_train:n_train + n_test]
    test_targets = targets[n_train:n_train + n_test]

    weights, _ = _fit_ridge_readout(
        train_states, train_targets, params["ridge_alpha"], params["readout_bias"]
    )
    predictions = _predict(test_states, weights, params["readout_bias"])
    nrmse = float(np.sqrt(np.mean((predictions - test_targets) ** 2)
                          / np.var(test_targets)))

    # De-normalise to physical units.
    input_phys = input_norm * std + mean
    targets_phys = targets * std + mean
    pred_phys = predictions * std + mean

    # Window around the train -> test boundary (in post-washout step index).
    lo, hi = n_train - SHOW_BEFORE, n_train + SHOW_AFTER
    steps = np.arange(lo, hi)
    target_window = targets_phys[lo:hi]
    pred_steps = np.arange(n_train, hi)
    pred_window = pred_phys[:SHOW_AFTER]
    input_window = input_phys[washout + lo:washout + hi]

    fig, (ax_u, ax_y) = plt.subplots(
        2, 1, figsize=(11, 5.2), sharex=True,
        gridspec_kw=dict(height_ratios=[1, 3], hspace=0.12),
    )

    ax_u.plot(steps, input_window, color="#7f7f7f", lw=1.2)
    ax_u.set_ylabel("drive\n$x(t)$", fontsize=9)
    ax_u.set_title(f"Mackey-Glass: the connectome reservoir, driven by $x(t)$, "
                   f"forecasts the held-out target $x(t{{+}}{horizon})$",
                   fontsize=12)
    ax_u.margins(x=0.005)

    ax_y.axvspan(n_train, hi, color="#fff3e0", zorder=0)
    ax_y.axvline(n_train, color="grey", lw=1.0, ls="--", zorder=1)
    ax_y.plot(steps, target_window, color="black", lw=2.0,
              label=f"target $x(t{{+}}{horizon})$", zorder=3)
    ax_y.plot(pred_steps, pred_window, color="#d62728", lw=1.8, ls="--",
              label="reservoir forecast $\\hat{x}(t+h)$", zorder=4)
    ax_y.set_ylabel("Mackey-Glass $x$")
    ax_y.set_xlabel("time step (after washout)")
    ax_y.legend(loc="upper left", fontsize=9, framealpha=0.95)
    ax_y.margins(x=0.005)

    y_lo = ax_y.get_ylim()[0]
    ax_y.text(n_train + 0.5 * SHOW_AFTER, y_lo, "held-out test", color="#b35900",
              ha="center", va="bottom", fontsize=9)
    ax_y.text(n_train - 0.5 * SHOW_BEFORE, y_lo, "training", color="grey",
              ha="center", va="bottom", fontsize=9)
    ax_y.text(0.985, 0.93, f"test NRMSE = {nrmse:.3f}", transform=ax_y.transAxes,
              ha="right", va="top", fontsize=10,
              bbox=dict(boxstyle="round", fc="white", ec="grey", alpha=0.9))

    label = cfg.condition_spec[CONDITION]["label"]
    fig.text(0.5, 0.005, f"substrate: {label}, connectome  ·  "
             f"spectral radius {SPECTRAL_RADIUS}  ·  horizon {horizon}  ·  seed {SEED}",
             ha="center", fontsize=8, color="grey")

    cfg.figures_dir.mkdir(parents=True, exist_ok=True)
    out = cfg.figures_dir / "mackey_glass_dynamics_demo.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"horizon={horizon}: test NRMSE = {nrmse:.3f}  ->  saved {out}")


def main() -> None:
    builder = SubstrateBuilder()  # one builder; reused across horizons
    for horizon in HORIZONS:
        render(builder, horizon)


if __name__ == "__main__":
    main()

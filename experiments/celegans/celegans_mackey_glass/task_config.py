"""Task config for the C. elegans Mackey-Glass forecasting experiment.

Only the task-specific pieces live here; the matrix structure and substrate
settings come from ``experiments.celegans.matrix_config``. ``task(horizon)``
supplies the task fields of the ``ExperimentConfig`` for a given forecast
horizon, so the same task dir runs at two horizons (a moderate benchmark and a
hard, chaos-limited one) writing to horizon-separated output directories.
"""

from pathlib import Path

from src.tasks.mackey_glass import evaluate as evaluate_mackey_glass

_DIR = Path(__file__).resolve().parent

# Two forecast horizons (confirmed): h=84 is the canonical Mackey-Glass
# benchmark (easy under driven teacher-forcing here, NRMSE ~0.09 at rung-0 --
# the honest baseline at the recognised operating point); h=300 is the
# chaos-limited regime (NRMSE ~0.47) where substrate differences are visible.
MODERATE_HORIZON = 84
HARD_HORIZON = 300
HORIZONS = (MODERATE_HORIZON, HARD_HORIZON)

# Per-horizon figure y-axis. The moderate horizon is easy (NRMSE well below the
# no-skill line, so that reference is omitted as clutter); the hard horizon
# spans no-skill and the supercritical null blow-ups, so it keeps the reference
# and a higher cap (blow-ups to ~5-7 clip above it).
_METRIC_YMAX = {MODERATE_HORIZON: 0.6, HARD_HORIZON: 1.2}
_METRIC_NO_SKILL = {MODERATE_HORIZON: None, HARD_HORIZON: 1.0}

# Frozen reservoir hyperparameters (tuned once on the undirected_gaussian rung-0 baseline for
# Mackey-Glass; near-optimal at both horizons, then held fixed across every
# condition and variant -- only the spectral radius is swept). The smooth MG
# series wants a much lower leak than NARMA's 1.0.
INPUT_SCALING = 0.5
LEAK_RATE = 0.3

# Mackey-Glass task parameters (frozen; ``horizon`` injected per run). Canonical
# mild-chaos DDE params (a=beta=0.2, b=gamma=0.1, n=10, tau=17), h=1.0 step.
MG_PARAMS = dict(
    T=3000,
    washout=200,
    n_train=2000,
    n_test=800,
    n_transient=200,
    ridge_alpha=1e-8,
    readout_bias=True,
    tau=17,
    a=0.2,
    b=0.1,
    n=10,
    x0=1.2,
    h=1.0,
)


def task(horizon: int) -> dict:
    """Task-specific fields of the ExperimentConfig (merged with shared()).

    Parameterised by forecast ``horizon``: the metric metadata and the output
    directories are horizon-tagged so the two runs don't collide.
    """
    return dict(
        experiment_name=f"celegans_mackey_glass_h{horizon}",
        task_name=f"Mackey-Glass {horizon}-step forecast",
        input_scaling=INPUT_SCALING,
        leak_rate=LEAK_RATE,
        task_evaluate=evaluate_mackey_glass,
        task_params=dict(MG_PARAMS, horizon=horizon),
        metric="nrmse",
        metric_lower_is_better=True,
        metric_label=f"Mackey-Glass NRMSE, h={horizon}  (lower = better)",
        metric_no_skill=_METRIC_NO_SKILL.get(horizon, 1.0),
        metric_ymax=_METRIC_YMAX.get(horizon, 1.5),
        extra_metric_fields=("horizon",),
        results_dir=_DIR / "results" / f"h{horizon}",
        figures_dir=_DIR / "figures" / f"h{horizon}",
        # NRMSE > 2 is an unambiguous blow-up (a working ESN scores well under 1.5);
        # such seeds are capped and counted in the divergence rate.
        metric_divergence_cap=2.0,
    )

"""Task config for the human Mackey-Glass forecasting experiment (human SC).

Only the task-specific pieces live here. ``task(horizon)`` supplies the task
fields for a given forecast horizon, so the same task dir runs at two horizons (a
moderate benchmark and a hard, chaos-limited one) writing to horizon-separated
output directories. Reservoir hyperparameters are the C. elegans Mackey-Glass
frozen values, kept identical so the human results read on the same footing.
"""

from pathlib import Path

from src.tasks.mackey_glass import evaluate as evaluate_mackey_glass

_DIR = Path(__file__).resolve().parent

MODERATE_HORIZON = 84
HARD_HORIZON = 300
HORIZONS = (MODERATE_HORIZON, HARD_HORIZON)

_METRIC_YMAX = {MODERATE_HORIZON: 0.6, HARD_HORIZON: 1.2}
_METRIC_NO_SKILL = {MODERATE_HORIZON: None, HARD_HORIZON: 1.0}

# Frozen reservoir hyperparameters (the smooth MG series wants a much lower leak
# than NARMA's 1.0). Only the spectral radius is swept.
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
        experiment_name=f"human_mackey_glass_h{horizon}",
        task_name=f"Mackey-Glass {horizon}-step forecast (human SC)",
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
        # NRMSE > 2 is an unambiguous blow-up; such seeds are capped + counted.
        metric_divergence_cap=2.0,
    )

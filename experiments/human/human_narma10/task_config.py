"""Task config for the human NARMA-10 experiment (human SC substrate).

Only the task-specific pieces live here; the matrix structure and substrate
settings come from ``experiments.human.matrix_config``. Reservoir hyperparameters
are the C. elegans NARMA-10 frozen values (tuned once on the gaussian rung-0
baseline, then held fixed across every condition/variant; only sr swept) -- kept
identical so the human results are read on the same footing.
"""

from pathlib import Path

from src.tasks.narma import evaluate as evaluate_narma

_DIR = Path(__file__).resolve().parent
RESULTS_DIR = _DIR / "results"
FIGURES_DIR = _DIR / "figures"

INPUT_SCALING = 0.2
LEAK_RATE = 1.0

NARMA_PARAMS = dict(
    T=3000,
    washout=200,
    n_train=2000,
    n_test=800,
    ridge_alpha=1e-8,
    readout_bias=True,
    u_low=0.0,
    u_high=0.5,
    divergence_bound=10.0,
    max_input_tries=50,
)


def task() -> dict:
    """Task-specific fields of the ExperimentConfig (merged with shared())."""
    return dict(
        experiment_name="human_narma10",
        task_name="NARMA-10 emulation (human SC)",
        input_scaling=INPUT_SCALING,
        leak_rate=LEAK_RATE,
        task_evaluate=evaluate_narma,
        task_params=NARMA_PARAMS,
        metric="nrmse",
        metric_lower_is_better=True,
        metric_label="NARMA-10 NRMSE  (lower = better)",
        metric_no_skill=1.0,
        metric_ymax=1.5,
        extra_metric_fields=("n_rejected_inputs",),
        results_dir=RESULTS_DIR,
        figures_dir=FIGURES_DIR,
        # NRMSE > 2 is an unambiguous blow-up (a working ESN scores well under 1.5);
        # such seeds are capped and counted in the divergence rate.
        metric_divergence_cap=2.0,
    )

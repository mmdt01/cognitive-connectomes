"""Task config for the human SC Jaeger memory-capacity experiment.

Identical task surface to the C. elegans MC task -- the evaluator
(``src.tasks.memory_capacity``) is connectome-agnostic, so only the experiment
identity and output dirs change. MC keeps its v1-pinned probe hyperparameters
(``input_scaling=1.0, leak=1.0, ridge_alpha=1e-6, T=3000, warmup=500,
max_lag=50``); ``input_scaling`` sets both the ``Win`` scaling and the
white-noise amplitude.
"""

from pathlib import Path

from src.tasks.memory_capacity import evaluate as evaluate_mc

_DIR = Path(__file__).resolve().parent
RESULTS_DIR = _DIR / "results"
FIGURES_DIR = _DIR / "figures"

INPUT_SCALING = 1.0
LEAK_RATE = 1.0

MC_PARAMS = dict(
    T=3000,
    warmup=500,
    max_lag=50,
    ridge_alpha=1e-6,
    input_scaling=INPUT_SCALING,
)


def task() -> dict:
    """Task-specific fields of the ExperimentConfig (merged with shared())."""
    return dict(
        experiment_name="human_mc",
        task_name="Jaeger memory capacity (human SC)",
        input_scaling=INPUT_SCALING,
        leak_rate=LEAK_RATE,
        task_evaluate=evaluate_mc,
        task_params=MC_PARAMS,
        metric="mc",
        metric_lower_is_better=False,
        metric_label="Memory capacity (Jaeger MC)  (higher = better)",
        metric_no_skill=None,
        metric_ymax=None,                  # MC ~ 0-15; let it autoscale
        extra_metric_fields=(),            # mc_per_lag is an array, not a scalar
        results_dir=RESULTS_DIR,
        figures_dir=FIGURES_DIR,
        metric_divergence_cap=None,        # MC is bounded (tanh saturates)
    )

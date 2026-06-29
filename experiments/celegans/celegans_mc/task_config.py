"""Task config for the C. elegans Jaeger memory-capacity experiment.

Memory capacity (MC) is the project's foundational task: feed white noise, train a
ridge readout per lag to reconstruct ``u(t-k)`` from the state ``x(t)``, and sum the
squared Pearson correlations across lags. It is where this project began
(v1 -> v2a -> v2c -> v2b); re-running it on the shared 7-variant ladder x 3 realism
conditions x wide spectral-radius sweep puts it on the same footing as the three
prediction tasks, so MC can be read through the same operating-point lens.

Hyperparameters are the v1-pinned MC values -- MC is a standard probe, not a tuned
task, so it keeps ``input_scaling=1.0, leak=1.0, ridge_alpha=1e-6, T=3000,
warmup=500, max_lag=50``. ``input_scaling`` sets both the ``Win`` scaling (build) and
the white-noise amplitude (the evaluator), so it appears in both places.
"""

from pathlib import Path

from src.tasks.memory_capacity import evaluate as evaluate_mc

_DIR = Path(__file__).resolve().parent
RESULTS_DIR = _DIR / "results"
FIGURES_DIR = _DIR / "figures"

INPUT_SCALING = 1.0
LEAK_RATE = 1.0

# v1-pinned MC hyperparameters. ``input_scaling`` here is the white-noise amplitude
# fed to the evaluator; it matches the Win input_scaling above.
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
        experiment_name="celegans_mc",
        task_name="Jaeger memory capacity",
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
        # MC is bounded (tanh saturates -> states stay finite even at high sr), so
        # only non-finite values are treated as divergent. No numeric cap.
        metric_divergence_cap=None,
    )

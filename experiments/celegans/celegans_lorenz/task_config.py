"""Task config for the C. elegans Lorenz attractor experiment.

Only the task-specific pieces live here; the matrix structure and substrate
settings come from ``experiments.celegans.matrix_config``. Unlike the driven
tasks, Lorenz scores **one matrix cell on two metrics** -- a stability metric
(``vpt``) and a fidelity metric (``climate_error``) -- so ``task(metric)`` builds
the task fields for whichever metric we want to analyse. The matrix is run
**once** (under the ``vpt`` config, which carries ``climate_error`` along as an
extra recorded field); ``stats``/``plots`` are then run once per metric, reading
the same ``results.parquet`` and writing metric-tagged outputs.

Frozen reservoir hyperparameters were tuned once on the v2a rung-0 baseline for
this closed-loop task, then held fixed across every condition and variant -- only
the spectral radius is swept. Closed-loop free-running is sensitive and lands at
a different operating point than the driven tasks (a much lower input scaling).
"""

from pathlib import Path

from src.tasks.lorenz import evaluate as evaluate_lorenz, LAMBDA_MAX

_DIR = Path(__file__).resolve().parent

# Frozen reservoir hyperparameters (tuned on v2a rung-0; baseline vpt ~2.3
# Lyapunov times / climate ~4). Closed-loop free-running wants a much lower input
# scaling than the driven tasks -- a strong drive overwhelms the feedback.
INPUT_SCALING = 0.1
LEAK_RATE = 1.0

# Lorenz task parameters (frozen). Direct next-state prediction (the increment
# form blows the climate metric up at the connectome-fixed N=300). The local RK4
# generator uses the canonical chaotic params (sigma=10, rho=28, beta=8/3) at
# h=0.03; lambda_max ~ 0.9056 expresses vpt in Lyapunov time.
LORENZ_PARAMS = dict(
    n_transient=1000,     # steps discarded onto the attractor
    washout=200,          # teacher-forcing washout before collecting states
    n_train=10000,        # readout training length
    sync_len=200,         # teacher-forced steps to synchronise each free-run
    n_windows=20,         # held-out free-runs averaged for vpt
    window_spacing=500,   # spacing of window start points in the held-out region
    free_run_len=600,     # vpt roll-out length (~16 Lyapunov times; max vpt ~5)
    climate_len=3000,     # long free-run length for the climate metric
    climate_washout=500,  # settling transient discarded before measuring climate
    epsilon=0.4,          # vpt error threshold on ||pred-true|| / rms(||true||)
    ridge_alpha=1e-7,
    readout_bias=True,
    sigma=10.0,
    rho=28.0,
    beta=8.0 / 3.0,
    h=0.03,
    x0=(1.0, 1.0, 1.0),
    lambda_max=LAMBDA_MAX,
)

# Per-metric metadata. ``vpt`` (Lyapunov time, higher = better) is the metric the
# matrix runs under -- it carries ``climate_error`` as an extra recorded column,
# so a single results.parquet holds both. ``climate_error`` (marginal
# Wasserstein-1, lower = better) is analysed from that same file.
_METRICS = {
    "vpt": dict(
        metric="vpt",
        metric_lower_is_better=False,
        metric_label="Lorenz valid-prediction time (Lyapunov times)  (higher = better)",
        metric_no_skill=None,
        metric_ymax=6.0,
        extra_metric_fields=("climate_error",),
        # vpt is bounded by free_run_len (it cannot blow up), so no cap is needed.
        metric_divergence_cap=None,
    ),
    "climate_error": dict(
        metric="climate_error",
        metric_lower_is_better=True,
        metric_label="Lorenz attractor-climate error (marginal $W_1$)  (lower = better)",
        metric_no_skill=None,
        metric_ymax=10.0,
        extra_metric_fields=("vpt",),
        # A free-run that leaves the attractor gives a huge/inf Wasserstein;
        # values >= 10 (z-scored units) are treated as divergent and capped.
        # Bounded-but-unfaithful runs (~2-9) stay below this.
        metric_divergence_cap=10.0,
    ),
}


def task(metric: str = "vpt") -> dict:
    """Task-specific fields of the ExperimentConfig (merged with shared()).

    ``metric`` selects which of the two metrics' metadata to attach; the frozen
    hyperparameters, task params, and output directories are identical across the
    two (the metric-tagged stats/plots filenames keep them from colliding).
    """
    if metric not in _METRICS:
        raise ValueError(f"unknown metric {metric!r}; expected one of {list(_METRICS)}")
    return dict(
        experiment_name="celegans_lorenz",
        task_name="Lorenz attractor (closed-loop free-running)",
        input_scaling=INPUT_SCALING,
        leak_rate=LEAK_RATE,
        input_dim=3,                       # 3-D state fed back in closed loop
        task_evaluate=evaluate_lorenz,
        task_params=dict(LORENZ_PARAMS),
        results_dir=_DIR / "results",
        figures_dir=_DIR / "figures",
        **_METRICS[metric],
    )

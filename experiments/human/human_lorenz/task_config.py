"""Task config for the human Lorenz attractor experiment (human SC substrate).

Only the task-specific pieces live here; the matrix structure and substrate
settings come from ``experiments.human.matrix_config``. Like the C. elegans Lorenz
task, this scores **one matrix cell on two metrics** -- a stability metric
(``vpt``) and a fidelity metric (``climate_error``) -- so ``task(metric)`` builds
the task fields for whichever metric we want to analyse. The matrix is run
**once** (under the ``vpt`` config, which carries ``climate_error`` along as an
extra recorded field); ``stats``/``plots`` are then run once per metric, reading
the same ``results.parquet`` and writing metric-tagged outputs.

Reservoir hyperparameters are the **C. elegans Lorenz frozen values, copied
verbatim** (input_scaling=0.1, leak=1.0, ridge_alpha=1e-7, readout_bias=True, the
divergence caps, and the full closed-loop protocol) -- kept identical so the human
results read on the same footing and comparability is preserved. Only the spectral
radius is swept. Do NOT silently re-tune these: closed-loop Lorenz on the human SC
is a genuine open question (symmetric/real spectrum, no rotational modes), and
re-tuning would break the cross-connectome comparison. If the frozen values give
near-total divergence, flag it -- re-tuning is a decision for the user.
"""

from pathlib import Path

from src.tasks.lorenz import evaluate as evaluate_lorenz, LAMBDA_MAX

_DIR = Path(__file__).resolve().parent

# Frozen reservoir hyperparameters (C. elegans Lorenz values, verbatim). Closed-loop
# free-running wants a much lower input scaling than the driven tasks -- a strong
# drive overwhelms the feedback.
INPUT_SCALING = 0.1
LEAK_RATE = 1.0

# Lorenz task parameters (frozen; identical to the C. elegans run). Direct
# next-state prediction. The local RK4 generator uses the canonical chaotic params
# (sigma=10, rho=28, beta=8/3) at h=0.03; lambda_max ~ 0.9056 expresses vpt in
# Lyapunov time.
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
        experiment_name="human_lorenz",
        task_name="Lorenz attractor (closed-loop free-running, human SC)",
        input_scaling=INPUT_SCALING,
        leak_rate=LEAK_RATE,
        input_dim=3,                       # 3-D state fed back in closed loop
        task_evaluate=evaluate_lorenz,
        task_params=dict(LORENZ_PARAMS),
        results_dir=_DIR / "results",
        figures_dir=_DIR / "figures",
        **_METRICS[metric],
    )

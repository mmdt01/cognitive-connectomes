"""Run the human Lorenz experiment: matrix (once) -> stats -> figures (per metric).

Thin wiring -- composes the HumanSubstrateBuilder, the shared human matrix config,
this task's config, and the generic ``src/experiment`` runner. Like the C. elegans
Lorenz task, one matrix cell scores **two metrics** (``vpt`` and ``climate_error``),
so the matrix is run **once** (under the ``vpt`` config, which records
``climate_error`` as an extra column) and then ``stats``/``plots`` are run once per
metric -- both reading the single ``results.parquet`` and writing metric-tagged
outputs (``stats_<metric>.parquet``, ``<metric>_vs_spectral_radius.png``).

Outputs are scale-tagged (results/scale_<N>/, figures/scale_<N>/), like the other
human tasks. On ada Lorenz runs fast with ``--jobs 128``, so the parallel path is
the default; checkpointing is only available on the sequential (``jobs=1``) path.

    python -m experiments.human.human_lorenz.run [--smoke] [--jobs N] [--scale N] [--sr-max V]
"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.reservoir import blas  # noqa: F401  (limit BLAS threads; import early)
from src.experiment.config import ExperimentConfig
from src.experiment import runner, stats, plots
from experiments.human.substrates import HumanSubstrateBuilder
from experiments.human import matrix_config
from experiments.human.human_lorenz import task_config

# The metric the matrix runs under (the other rides along via extra_metric_fields).
RUN_METRIC = "vpt"
METRICS = ("vpt", "climate_error")


def build_config(metric: str, scale: int, sr_max: float | None, span: dict) -> ExperimentConfig:
    """Assemble a scale-tagged config for ``metric``.

    All metrics share the same scale-tagged ``results_dir`` (so they read the one
    ``results.parquet`` the matrix run produced) and get scale-tagged figures.
    """
    cfg = ExperimentConfig(**matrix_config.shared(), **task_config.task(metric))
    cfg.results_dir = cfg.results_dir / f"scale_{scale}"
    cfg.figures_dir = cfg.figures_dir / f"scale_{scale}"
    if sr_max is not None:
        cfg.spectral_radii = matrix_config.spectral_sweep(sr_max)
        cfg.supercritical_radii = [sr for sr in cfg.spectral_radii if sr >= 1.25]
    cfg.supercritical_span = span
    return cfg


def main(smoke: bool = False, jobs: int = 1, scale: int | None = None,
         sr_max: float | None = None) -> None:
    scale = matrix_config.SCALE if scale is None else scale
    builder = HumanSubstrateBuilder(scale=scale)
    # Where the connectome's bulk goes supercritical (shading for the figures).
    span = builder.connectome_supercritical_radii(matrix_config.CONDITIONS)

    # Run the matrix once. The vpt config carries climate_error along, so the
    # single results.parquet holds both metrics' columns.
    run_cfg = build_config(RUN_METRIC, scale, sr_max, span)
    print(f"\n{'=' * 72}\n  Lorenz attractor (closed-loop free-running)  scale={scale}\n{'=' * 72}")
    if smoke:
        runner.run_matrix(builder, run_cfg, spectral_radii=[0.0, 0.95, 1.5], n_seeds=2,
                          jobs=jobs)
    elif jobs and jobs > 1:
        # Parallel path (the ada default): fast, but no checkpointing.
        runner.run_matrix(builder, run_cfg, jobs=jobs)
    else:
        # Sequential path: checkpoint so a hard interruption resumes rather than
        # restarts (Lorenz's closed-loop rollout is the slow task).
        runner.run_matrix(
            builder, run_cfg,
            checkpoint_path=str(run_cfg.results_dir / "lorenz_checkpoint.parquet"),
        )

    # Stats + figures per metric, both reading the shared results.parquet.
    for metric in METRICS:
        cfg = build_config(metric, scale, sr_max, span)
        print(f"\n{'-' * 72}\n  Metric: {metric}\n{'-' * 72}")
        stats.run(cfg)
        plots.run(cfg)
    print("\nPipeline complete.")


def _flag(argv, flag, default, cast=int):
    """Parse ``--flag V`` / ``--flag=V`` from argv (cast applied); default if absent."""
    for i, arg in enumerate(argv):
        if arg == flag and i + 1 < len(argv):
            return cast(argv[i + 1])
        if arg.startswith(flag + "="):
            return cast(arg.split("=", 1)[1])
    return default


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv,
         jobs=_flag(sys.argv, "--jobs", 1, int),
         scale=_flag(sys.argv, "--scale", None, int),
         sr_max=_flag(sys.argv, "--sr-max", None, float))

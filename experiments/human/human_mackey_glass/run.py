"""Run the human Mackey-Glass experiment: matrix -> stats -> figures.

Runs the full pipeline at each forecast horizon in ``task_config.HORIZONS``,
reusing a single SubstrateBuilder (null masks are horizon-independent). Outputs
are scale- AND horizon-tagged (results/scale_<N>/h<horizon>/).

    python -m experiments.human.human_mackey_glass.run [--smoke] [--jobs N] [--scale N] [--sr-max V]
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
from experiments.human.human_mackey_glass import task_config


def build_config(horizon: int) -> ExperimentConfig:
    return ExperimentConfig(**matrix_config.shared(), **task_config.task(horizon))


def main(smoke: bool = False, jobs: int = 1, scale: int | None = None,
         sr_max: float | None = None) -> None:
    scale = matrix_config.SCALE if scale is None else scale
    # One builder for both horizons; connectome bulk radii are horizon-independent.
    builder = HumanSubstrateBuilder(scale=scale)
    span = builder.connectome_supercritical_radii(matrix_config.CONDITIONS)
    for horizon in task_config.HORIZONS:
        cfg = build_config(horizon)
        # scale-tag the horizon-separated output dirs: results/scale_<N>/h<horizon>/
        cfg.results_dir = cfg.results_dir.parent / f"scale_{scale}" / cfg.results_dir.name
        cfg.figures_dir = cfg.figures_dir.parent / f"scale_{scale}" / cfg.figures_dir.name
        if sr_max is not None:
            cfg.spectral_radii = matrix_config.spectral_sweep(sr_max)
            cfg.supercritical_radii = [sr for sr in cfg.spectral_radii if sr >= 1.25]
        cfg.supercritical_span = span
        print(f"\n{'=' * 72}\n  Mackey-Glass  horizon={horizon}  scale={scale}\n{'=' * 72}")
        if smoke:
            runner.run_matrix(builder, cfg, spectral_radii=[0.0, 0.95, 1.5], n_seeds=2,
                              jobs=jobs)
        else:
            runner.run_matrix(builder, cfg, jobs=jobs)
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

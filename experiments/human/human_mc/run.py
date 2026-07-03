"""Run the human SC memory-capacity experiment: matrix -> stats -> figures.

Thin wiring -- composes the HumanSubstrateBuilder, the shared human matrix config,
this task's config, and the generic ``src/experiment`` runner.

    python -m experiments.human.human_mc.run            # full run
    python -m experiments.human.human_mc.run --smoke    # tiny check
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
from experiments.human.human_mc import task_config


def build_config() -> ExperimentConfig:
    return ExperimentConfig(**matrix_config.shared(), **task_config.task())


def main(smoke: bool = False, jobs: int = 1) -> None:
    cfg = build_config()
    builder = HumanSubstrateBuilder()
    if smoke:
        runner.run_matrix(builder, cfg, spectral_radii=[0.0, 0.95, 1.5], n_seeds=2,
                          jobs=jobs)
    else:
        runner.run_matrix(builder, cfg, jobs=jobs)
    # Shade each figure's panel from where the connectome's bulk goes supercritical.
    cfg.supercritical_span = builder.connectome_supercritical_radii(cfg.conditions)
    stats.run(cfg)
    plots.run(cfg)
    print("\nPipeline complete.")


def _parse_jobs(argv) -> int:
    """--jobs N or --jobs=N (default 1 = sequential)."""
    for i, arg in enumerate(argv):
        if arg == "--jobs" and i + 1 < len(argv):
            return int(argv[i + 1])
        if arg.startswith("--jobs="):
            return int(arg.split("=", 1)[1])
    return 1


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv, jobs=_parse_jobs(sys.argv))

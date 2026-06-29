"""Run the C. elegans memory-capacity experiment: matrix -> stats -> figures.

Thin wiring -- composes the connectome's SubstrateBuilder, the shared matrix
config, this task's config, and the generic ``src/experiment`` runner.

    python -m experiments.celegans.celegans_mc.run            # full run
    python -m experiments.celegans.celegans_mc.run --smoke    # tiny check
"""

import sys
from pathlib import Path

# Ensure the repo root is importable so `experiments.*` resolves regardless of
# how this script is launched (module or file).
_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.reservoir import blas  # noqa: F401  (limit BLAS threads; import early)
from src.experiment.config import ExperimentConfig
from src.experiment import runner, stats, plots
from experiments.celegans.substrates import SubstrateBuilder
from experiments.celegans import matrix_config
from experiments.celegans.celegans_mc import task_config


def build_config() -> ExperimentConfig:
    return ExperimentConfig(**matrix_config.shared(), **task_config.task())


def main(smoke: bool = False) -> None:
    cfg = build_config()
    builder = SubstrateBuilder()
    if smoke:
        runner.run_matrix(builder, cfg, spectral_radii=[0.0, 0.95, 1.5], n_seeds=2)
    else:
        runner.run_matrix(builder, cfg)
    # Shade each figure's panel from where the connectome's bulk goes supercritical.
    cfg.supercritical_span = builder.connectome_supercritical_radii(cfg.conditions)
    stats.run(cfg)
    plots.run(cfg)
    print("\nPipeline complete.")


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)

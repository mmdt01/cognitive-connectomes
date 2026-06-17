"""Run the C. elegans Mackey-Glass experiment: matrix -> stats -> figures.

Thin wiring -- composes the connectome's SubstrateBuilder, the shared matrix
config, this task's config, and the generic ``src/experiment`` runner. Runs the
full pipeline at each forecast horizon in ``task_config.HORIZONS``, reusing a
single SubstrateBuilder so the (expensive) directed null masks are generated
once and reused across horizons.

    python -m experiments.celegans.celegans_mackey_glass.run            # full run
    python -m experiments.celegans.celegans_mackey_glass.run --smoke    # tiny check
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
from experiments.celegans.celegans_mackey_glass import task_config


def build_config(horizon: int) -> ExperimentConfig:
    return ExperimentConfig(**matrix_config.shared(), **task_config.task(horizon))


def main(smoke: bool = False) -> None:
    # One builder for both horizons: null masks are horizon-independent and
    # cached on (topology, variant, seed), so the directed rewires are built once.
    builder = SubstrateBuilder()
    for horizon in task_config.HORIZONS:
        cfg = build_config(horizon)
        print(f"\n{'=' * 72}\n  Mackey-Glass  horizon = {horizon}\n{'=' * 72}")
        if smoke:
            runner.run_matrix(builder, cfg, spectral_radii=[0.0, 0.95, 1.5], n_seeds=2)
        else:
            runner.run_matrix(builder, cfg)
        stats.run(cfg)
        plots.run(cfg)
    print("\nPipeline complete.")


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)

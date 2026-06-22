"""Run the C. elegans Lorenz experiment: matrix (once) -> stats -> figures (per metric).

Thin wiring -- composes the connectome's SubstrateBuilder, the shared matrix
config, this task's config, and the generic ``src/experiment`` runner. Unlike the
driven tasks, Lorenz produces **two metrics per cell** (``vpt`` and
``climate_error``), so the matrix is run **once** (under the ``vpt`` config, which
records ``climate_error`` as an extra column) and then ``stats``/``plots`` are run
once per metric -- both reading the single ``results.parquet`` and writing
metric-tagged outputs (``stats_<metric>.parquet``,
``<metric>_vs_spectral_radius.png``).

    python -m experiments.celegans.celegans_lorenz.run            # full run
    python -m experiments.celegans.celegans_lorenz.run --smoke    # tiny check
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
from experiments.celegans.celegans_lorenz import task_config

# The metric the matrix runs under (the other rides along via extra_metric_fields).
RUN_METRIC = "vpt"
METRICS = ("vpt", "climate_error")


def build_config(metric: str) -> ExperimentConfig:
    return ExperimentConfig(**matrix_config.shared(), **task_config.task(metric))


def main(smoke: bool = False) -> None:
    builder = SubstrateBuilder()

    # Run the matrix once. The vpt config carries climate_error along, so the
    # single results.parquet holds both metrics' columns.
    run_cfg = build_config(RUN_METRIC)
    print(f"\n{'=' * 72}\n  Lorenz attractor (closed-loop free-running)\n{'=' * 72}")
    if smoke:
        runner.run_matrix(builder, run_cfg, spectral_radii=[0.0, 0.95, 1.5], n_seeds=2)
    else:
        runner.run_matrix(builder, run_cfg)

    # Stats + figures per metric, both reading the shared results.parquet.
    for metric in METRICS:
        cfg = build_config(metric)
        print(f"\n{'-' * 72}\n  Metric: {metric}\n{'-' * 72}")
        stats.run(cfg)
        plots.run(cfg)
    print("\nPipeline complete.")


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)

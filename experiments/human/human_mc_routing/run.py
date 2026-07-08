"""Run the human anatomical I/O-routing memory-capacity experiment.

    python -m experiments.human.human_mc_routing.run            # full run
    python -m experiments.human.human_mc_routing.run --smoke    # tiny check
    python -m experiments.human.human_mc_routing.run --jobs 128 --scale 448 --sr-max 6

Subcortical input, per-Yeo-network + pooled-cortex readout apertures, on the
with-subcortical published consensus. The connectome + weight-placement control +
5-rung ladder keep FIXED anatomical I/O (only W changes); ``connectome_random_
routing`` is the random-placement control. One reservoir run -> MC per aperture.
Stats are computed per aperture (each aperture's MC column is a metric); the
routing figures are custom (the generic single-metric plots don't fit).
"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.reservoir import blas  # noqa: F401  (limit BLAS threads; import early)
from src.experiment.config import ExperimentConfig
from src.experiment import runner, stats
from experiments.human import matrix_config
from experiments.human.routing_substrate import (
    RoutingSubstrateBuilder,
    RANDOM_READOUT_VARIANT,
    DENSE_INPUT_VARIANT,
)
from experiments.human.human_mc_routing import task_config, plots_routing


def build_config() -> ExperimentConfig:
    shared = matrix_config.shared()
    shared.update(task_config.routing_overrides())
    return ExperimentConfig(**shared, **task_config.task())


def _run_stats_per_aperture(cfg) -> None:
    """Run the generic (variant-agnostic) stats once per readout aperture, swapping
    the metric so each aperture writes its own stats_<metric>.parquet."""
    primary = cfg.metric
    for aperture in task_config.APERTURES:
        cfg.metric = f"mc_{aperture}"
        cfg.metric_label = f"Memory capacity ({aperture} readout)"
        print(f"\n########## stats: readout aperture = {aperture} ##########")
        stats.run(cfg)
    cfg.metric = primary


def main(smoke: bool = False, jobs: int = 1, scale: int | None = None,
         sr_max: float | None = None) -> None:
    scale = matrix_config.SCALE if scale is None else scale
    cfg = build_config()
    # Smoke writes to a separate ``*_smoke`` dir so a tiny check never clobbers the
    # canonical full-run results/figures (a gotcha that bit us before).
    tag = f"scale_{scale}" + ("_smoke" if smoke else "")
    cfg.results_dir = cfg.results_dir / tag
    cfg.figures_dir = cfg.figures_dir / tag
    if sr_max is not None:
        cfg.spectral_radii = matrix_config.spectral_sweep(sr_max)
        cfg.supercritical_radii = [sr for sr in cfg.spectral_radii if sr >= 1.25]

    builder = RoutingSubstrateBuilder(scale=scale, source=task_config.SUBSTRATE_SOURCE)
    aperture_sizes = {k: v for k, v in builder.summary()["readout_apertures"].items()}

    if smoke:
        runner.run_matrix(
            builder, cfg,
            variants=["connectome", "degree_rewire", "random_gaussian",
                      RANDOM_READOUT_VARIANT, DENSE_INPUT_VARIANT],
            spectral_radii=[0.0, 0.95, 1.5, 3.0], n_seeds=2, jobs=jobs,
        )
    else:
        runner.run_matrix(builder, cfg, jobs=jobs)

    _run_stats_per_aperture(cfg)
    plots_routing.run(cfg, list(task_config.APERTURES), aperture_sizes)
    print("\nRouting pipeline complete.")


def _flag(argv, flag, default, cast=int):
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

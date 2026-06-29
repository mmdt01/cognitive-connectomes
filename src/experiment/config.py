"""The ``ExperimentConfig`` consumed by the generic runner/stats/plots.

Assembled per experiment by merging a connectome's shared matrix config
(``matrix_config.shared()``) with a task config (``task_config.task()``). The
generic modules read only this object — they import no experiment-specific
module — which is what makes them reusable across tasks and connectomes.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass
class ExperimentConfig:
    # identity
    experiment_name: str
    task_name: str
    # matrix structure (shared, connectome-level)
    conditions: list
    condition_spec: dict
    variants: list
    null_variants: list
    variant_rung: dict
    spectral_radii: list
    supercritical_radii: list
    n_seeds: int
    # substrate construction (shared)
    weight_transform: str
    clustering_tolerance: float
    louvain_seed: int
    swap_multiplier: int
    # reservoir hyperparameters (task-tuned, then frozen)
    input_scaling: float
    leak_rate: float
    input_seed_offset: int
    # task
    task_evaluate: Callable
    task_params: dict
    metric: str                    # results column used as the performance metric
    metric_lower_is_better: bool
    metric_label: str              # y-axis label for the metric figure
    metric_no_skill: float | None  # reference line (e.g. NRMSE=1); None to omit
    metric_ymax: float | None      # y-axis cap for the metric figure; None to auto
    extra_metric_fields: tuple     # other scalar fields from evaluate() to record
    # statistics
    n_permutations: int
    permutation_seed: int
    alpha: float
    # output paths (per experiment)
    results_dir: Path
    figures_dir: Path
    # divergence-robust statistics (optional; default off). A metric value beyond
    # this cap (above it for lower-is-better, below for higher-is-better) or
    # non-finite is treated as a blow-up: clipped to the cap for the parametric
    # effect and counted in the divergence rate. None -> only non-finite values
    # are treated as divergent.
    metric_divergence_cap: float | None = None
    # number of reservoir input channels (Win columns). 1 for the single-channel
    # driven tasks (NARMA, Mackey-Glass -- left at the default so they build
    # byte-identically); 3 for Lorenz (the 3-D state fed back in closed loop).
    input_dim: int = 1
    # optional {condition: spectral_radius} marking where the *connectome's*
    # eigenvalue bulk becomes supercritical (sr_crit = 1/bulk95_ratio). The
    # metric/effect-size figures shade each condition's panel from this point
    # rather than the fixed nominal-supercritical threshold (min(supercritical_radii)).
    # None -> fall back to that fixed threshold. Set per run from the substrate.
    supercritical_span: dict | None = None

    @property
    def results_parquet(self) -> Path:
        return self.results_dir / "results.parquet"

    @property
    def null_diagnostics_parquet(self) -> Path:
        return self.results_dir / "null_diagnostics.parquet"

    @property
    def stats_parquet(self) -> Path:
        # Metric-tagged so tasks that score one matrix on two metrics (Lorenz:
        # vpt + climate_error, sharing a single results.parquet) write distinct
        # stats files instead of overwriting. Single-metric tasks (NARMA,
        # Mackey-Glass) just get e.g. stats_nrmse.parquet.
        return self.results_dir / f"stats_{self.metric}.parquet"

    @property
    def manifest_json(self) -> Path:
        return self.results_dir / "manifest.json"

    def manifest_dict(self) -> dict:
        """JSON-serialisable snapshot for the run manifest (the audit trail)."""
        return {
            "experiment_name": self.experiment_name,
            "task_name": self.task_name,
            "conditions": self.conditions,
            "condition_spec": self.condition_spec,
            "variants": self.variants,
            "spectral_radii": self.spectral_radii,
            "n_seeds": self.n_seeds,
            "weight_transform": self.weight_transform,
            "clustering_tolerance": self.clustering_tolerance,
            "louvain_seed": self.louvain_seed,
            "swap_multiplier": self.swap_multiplier,
            "input_scaling": self.input_scaling,
            "leak_rate": self.leak_rate,
            "task_params": self.task_params,
            "input_seed_offset": self.input_seed_offset,
            "metric": self.metric,
            "n_permutations": self.n_permutations,
            "permutation_seed": self.permutation_seed,
            "alpha": self.alpha,
            "metric_divergence_cap": self.metric_divergence_cap,
        }

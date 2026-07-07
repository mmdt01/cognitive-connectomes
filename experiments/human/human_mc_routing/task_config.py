"""Task + matrix config for the human anatomical I/O-routing MC experiment.

Memory capacity through **anatomical readout apertures** (each Yeo intrinsic
network + pooled cortex) with **subcortical input**, on the with-subcortical
published consensus. Differs from the standard human MC in two ways:

  * the evaluator is ``memory_capacity_routing`` (one reservoir run -> MC per
    aperture; the aperture columns become the metrics), and
  * the variant list adds the ``connectome_random_routing`` placement control and
    drops the extra sign/tail conditions (routing lives in the empirical, real-W
    cell -- the sign story is settled elsewhere), so only ``human_empirical`` runs.

``routing_overrides()`` supplies the matrix-level fields that differ from
``matrix_config.shared()``; ``task()`` supplies the task-level fields. MC keeps its
v1-pinned hyperparameters.
"""

from pathlib import Path

from src.tasks import memory_capacity_routing
from src.connectomes.human_suarez import YEO_NETWORKS
from experiments.human.routing_substrate import RANDOM_ROUTING_VARIANT

_DIR = Path(__file__).resolve().parent
RESULTS_DIR = _DIR / "results"
FIGURES_DIR = _DIR / "figures"

# Readout apertures: pooled cortex (the primary/headline metric) + 7 Yeo networks.
PRIMARY_APERTURE = "cortex"
APERTURES = (PRIMARY_APERTURE,) + YEO_NETWORKS           # ("cortex","VIS",...,"DMN")
APERTURE_METRICS = tuple(f"mc_{a}" for a in APERTURES)   # results.parquet columns

INPUT_SCALING = 1.0
LEAK_RATE = 1.0

MC_PARAMS = dict(
    T=3000,
    warmup=500,
    max_lag=50,
    ridge_alpha=1e-6,
    input_scaling=INPUT_SCALING,
    primary_aperture=PRIMARY_APERTURE,
)

# Substrate provenance -- pinned here as a single, swappable decision (Stage-0
# config audit trail). "published_full" = Suárez published with-subctx consensus
# (current: fast path to verify their MC). FUTURE: a self-built with-subctx
# consensus ("consensus_full" once its loader exists); the routing logic is
# substrate-agnostic, so this one value is the only thing that changes. Recorded
# in the run manifest via the builder summary.
SUBSTRATE_SOURCE = "published_full"

# One condition (the real-W empirical cell); the connectome + weight-placement
# control + 5-rung ladder all keep FIXED anatomical I/O, plus the random-placement
# routing control. Variant names match the ladder so stats works unchanged.
CONDITIONS = ["human_empirical"]
CONDITION_SPEC = {
    "human_empirical": {
        "topology": "undirected",
        "weight_scheme": "symmetric_empirical",
        "label": "Human SC (published, +subctx) · anatomical I/O routing",
    },
}
VARIANTS = [
    "connectome",
    "connectome_weight_permuted",
    "random_gaussian",
    "erdos_renyi",
    "degree_rewire",
    "clustering_rewire",
    "modularity_rewire",
    RANDOM_ROUTING_VARIANT,        # placement control: real W, random I/O placement
]
NULL_VARIANTS = [v for v in VARIANTS if v != "connectome"]
VARIANT_RUNG = {
    "connectome_weight_permuted": -1,
    "random_gaussian": 0,
    "erdos_renyi": 1,
    "degree_rewire": 2,
    "clustering_rewire": 3,
    "modularity_rewire": 4,
    RANDOM_ROUTING_VARIANT: -1,
}


def routing_overrides() -> dict:
    """Matrix-level fields that override ``matrix_config.shared()`` for routing."""
    return dict(
        conditions=CONDITIONS,
        condition_spec=CONDITION_SPEC,
        variants=VARIANTS,
        null_variants=NULL_VARIANTS,
        variant_rung=VARIANT_RUNG,
        factorial_grid=None,
    )


def task() -> dict:
    """Task-level fields of the ExperimentConfig (merged with the shared matrix)."""
    return dict(
        experiment_name="human_mc_routing",
        task_name="Memory capacity · anatomical I/O routing (human SC)",
        input_scaling=INPUT_SCALING,
        leak_rate=LEAK_RATE,
        task_evaluate=memory_capacity_routing.evaluate,
        task_params=MC_PARAMS,
        metric=f"mc_{PRIMARY_APERTURE}",
        metric_lower_is_better=False,
        metric_label="Memory capacity (pooled-cortex readout)",
        metric_no_skill=None,
        metric_ymax=None,
        # Every non-primary aperture is recorded as its own results column.
        extra_metric_fields=tuple(m for m in APERTURE_METRICS
                                  if m != f"mc_{PRIMARY_APERTURE}"),
        results_dir=RESULTS_DIR,
        figures_dir=FIGURES_DIR,
        metric_divergence_cap=None,     # MC is bounded
    )

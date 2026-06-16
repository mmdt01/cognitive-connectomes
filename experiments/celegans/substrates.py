"""Substrate construction for C. elegans experiments (task-agnostic).

A ``SubstrateBuilder`` loads both connectome processings once, precomputes the
empirical weight pool, the Dale sign vector, and the (per-topology) Louvain
partitions, then turns any ``(condition, variant, seed)`` cell into a weighted
recurrent matrix ``W``. It is shared across every C. elegans task (NARMA-10,
Mackey-Glass, ...); the task only changes downstream of the weighted ``W``.

Key efficiency point: v2b and v2d share the same *directed* topology, so their
null masks are identical. Masks are cached on ``(topology, variant, seed)`` and
reused across conditions — the expensive directed rung-3 clustering rewire is
generated once, not twice.

Conventions: the connectome variant keeps its *real* weights (v2b/v2d) or gets
fresh symmetric-Gaussian weights (v2a); nulls sample magnitudes from the
empirical pool (v2b/v2d) or get fresh Gaussian weights (v2a). Every null is
validated against the property it claims to preserve before use.
"""

import warnings

import networkx as nx
import numpy as np

from src.connectomes.celegans_cook2019 import load as load_connectome
from src.connectomes.neurotransmitters import load_neuron_signs
from src.nulls import (
    random_gaussian,
    erdos_renyi,
    degree_rewire,
    clustering_rewire,
    modularity_rewire,
)
from src.nulls.validation import validate_null
from src.reservoir.weights import apply_weight_scheme

from experiments.celegans import matrix_config as config


class SubstrateBuilder:
    def __init__(self):
        # Connectomes (undirected for v2a; directed for v2b/v2d).
        self.undirected = load_connectome("binary_undirected_chemical")
        self.directed = load_connectome("directed_weighted_chemical")
        self.undirected_mask = self.undirected.adjacency  # binary symmetric
        self.directed_adjacency = self.directed.adjacency  # weighted directed
        self.directed_mask = (self.directed_adjacency != 0).astype(float)

        # Empirical weight pool for v2b/v2d (raw or sqrt synapse counts).
        if config.WEIGHT_TRANSFORM == "sqrt":
            weighted = np.where(
                self.directed_adjacency > 0, np.sqrt(self.directed_adjacency), 0.0
            )
        elif config.WEIGHT_TRANSFORM == "raw":
            weighted = self.directed_adjacency.astype(float).copy()
        else:
            raise ValueError(f"unknown WEIGHT_TRANSFORM {config.WEIGHT_TRANSFORM!r}")
        self.directed_weighted = weighted
        self.empirical_pool = weighted[weighted != 0].copy()

        # Dale sign vector for v2d (aligned to directed node order).
        self.signs, self.sign_coverage = load_neuron_signs(self.directed.node_labels)

        # Fixed Louvain partitions for rung 4 (one per topology family).
        self.partitions = {
            "undirected": nx.community.louvain_communities(
                nx.from_numpy_array(self.undirected_mask), seed=config.LOUVAIN_SEED
            ),
            "directed": nx.community.louvain_communities(
                nx.from_numpy_array(
                    self.directed_mask.astype(int), create_using=nx.DiGraph
                ),
                seed=config.LOUVAIN_SEED,
            ),
        }

        self._mask_cache: dict = {}
        self.diagnostics: list[dict] = []

    # -- topology helpers ---------------------------------------------------
    def _base_mask(self, topology: str) -> np.ndarray:
        return self.undirected_mask if topology == "undirected" else self.directed_mask

    # -- mask generation (cached + validated) -------------------------------
    def get_mask(self, topology: str, variant: str, seed: int) -> np.ndarray:
        key = (topology, variant, seed)
        if key in self._mask_cache:
            return self._mask_cache[key]

        directed = topology == "directed"
        base = self._base_mask(topology)
        partition = self.partitions[topology]

        if variant == "connectome":
            mask = base.copy()
        elif variant == "random_gaussian":
            mask = random_gaussian.generate(base, seed=seed, directed=directed)
        elif variant == "erdos_renyi":
            mask = erdos_renyi.generate(base, seed=seed, directed=directed)
        elif variant == "degree_rewire":
            mask = degree_rewire.generate(
                base, seed=seed, directed=directed,
                n_swaps_multiplier=config.SWAP_MULTIPLIER,
            )
        elif variant == "clustering_rewire":
            with warnings.catch_warnings():
                warnings.simplefilter("error", RuntimeWarning)
                mask, diag = clustering_rewire.generate(
                    base, seed=seed, directed=directed,
                    tolerance=config.CLUSTERING_TOLERANCE,
                    n_swaps_multiplier=config.SWAP_MULTIPLIER,
                    return_diagnostics=True,
                )
            self._record_clustering(topology, variant, seed, base, mask, diag, directed)
        elif variant == "modularity_rewire":
            mask, diag = modularity_rewire.generate(
                base, seed=seed, directed=directed,
                community_partition=partition,
                n_swaps_multiplier=config.SWAP_MULTIPLIER,
                return_diagnostics=True,
            )
            self._record_modularity(topology, variant, seed, base, mask, diag, partition, directed)
        else:
            raise ValueError(f"unknown variant {variant!r}")

        if variant == "random_gaussian":
            self._record_random(topology, variant, seed, base, mask)
        elif variant == "erdos_renyi":
            self._record_edge_count(topology, variant, seed, base, mask)
        elif variant == "degree_rewire":
            self._record_degree(topology, variant, seed, base, mask, directed)

        self._mask_cache[key] = mask
        return mask

    # -- weighting per condition -------------------------------------------
    def weighted(self, condition: str, variant: str, seed: int) -> np.ndarray:
        spec = config.CONDITION_SPEC[condition]
        mask = self.get_mask(spec["topology"], variant, seed)

        if condition == "v2a":
            return apply_weight_scheme(mask, "symmetric_gaussian", seed=seed)

        # v2b / v2d: connectome keeps its real weights; nulls sample the pool.
        if variant == "connectome":
            weighted = self.directed_weighted.copy()
            if condition == "v2d":
                weighted = weighted * self.signs[np.newaxis, :]
            return weighted

        if condition == "v2b":
            return apply_weight_scheme(
                mask, "asymmetric_empirical", seed=seed,
                empirical_weights=self.empirical_pool,
            )
        # v2d
        return apply_weight_scheme(
            mask, "asymmetric_empirical_signed", seed=seed,
            empirical_weights=self.empirical_pool, neuron_signs=self.signs,
        )

    # -- validation recorders ----------------------------------------------
    # Each rung is validated against the property it actually claims to
    # preserve: rung 0 (random) only matches density in expectation; rung 1
    # (ER) preserves exact edge count; rung 2 (degree) preserves the (in/out)
    # degree sequence.
    def _record_random(self, topology, variant, seed, base, mask):
        self.diagnostics.append(dict(
            topology=topology, variant=variant, seed=seed,
            property="density_in_expectation", preserved=True,
            base_edges=int((base != 0).sum()), mask_edges=int((mask != 0).sum()),
        ))

    def _record_edge_count(self, topology, variant, seed, base, mask):
        check = validate_null(base, mask, "edge_count")
        assert check["preserved"], (
            f"erdos_renyi ({topology}) seed={seed}: edge count not preserved."
        )
        self.diagnostics.append(dict(
            topology=topology, variant=variant, seed=seed,
            property="edge_count", preserved=True,
        ))

    def _record_degree(self, topology, variant, seed, base, mask, directed):
        properties = (["in_degree_sequence", "out_degree_sequence"] if directed
                      else ["degree_sequence"])
        for prop in properties:
            check = validate_null(base, mask, prop)
            assert check["preserved"], (
                f"degree_rewire ({topology}) seed={seed}: {prop} not preserved."
            )
            self.diagnostics.append(dict(
                topology=topology, variant=variant, seed=seed,
                property=prop, preserved=True,
            ))

    def _record_clustering(self, topology, variant, seed, base, mask, diag, directed):
        prop = "directed_clustering" if directed else "clustering"
        check = validate_null(base, mask, prop, tolerance=config.CLUSTERING_TOLERANCE)
        assert check["preserved"], (
            f"{variant} ({topology}) seed={seed}: clustering not preserved within "
            f"{config.CLUSTERING_TOLERANCE} (expected={check['expected']:.4f}, "
            f"actual={check['actual']:.4f})"
        )
        self.diagnostics.append(dict(
            topology=topology, variant=variant, seed=seed, property=prop,
            preserved=True, acceptance_rate=diag["acceptance_rate"],
            clustering_initial=diag.get("clustering_initial"),
            clustering_final=diag.get("clustering_final"),
            T_initial=diag.get("T_initial"), T_final=diag.get("T_final"),
        ))

    def _record_modularity(self, topology, variant, seed, base, mask, diag, partition, directed):
        if directed:
            check = validate_null(base, mask, "directed_block_matrix",
                                  community_partition=partition)
            prop = "directed_block_matrix"
        else:
            check = validate_null(base, mask, "modularity", tolerance=0.01,
                                  community_partition=partition)
            prop = "modularity"
        assert check["preserved"], (
            f"{variant} ({topology}) seed={seed}: {prop} not preserved."
        )
        self.diagnostics.append(dict(
            topology=topology, variant=variant, seed=seed, property=prop,
            preserved=True, acceptance_rate=diag["acceptance_rate"],
            n_communities=diag.get("n_communities"),
            Q_initial=diag.get("Q_initial"), Q_final=diag.get("Q_final"),
        ))

    # -- summary ------------------------------------------------------------
    def summary(self) -> dict:
        return {
            "n_nodes_undirected": int(self.undirected_mask.shape[0]),
            "n_nodes_directed": int(self.directed_mask.shape[0]),
            "n_directed_edges": int(self.directed_mask.sum()),
            "empirical_pool_size": int(self.empirical_pool.size),
            "weight_transform": config.WEIGHT_TRANSFORM,
            "n_inhibitory": self.sign_coverage["n_inhibitory"],
            "n_excitatory": self.sign_coverage["n_excitatory"],
            "partition_sizes": {
                topology: sorted([len(c) for c in part], reverse=True)
                for topology, part in self.partitions.items()
            },
        }

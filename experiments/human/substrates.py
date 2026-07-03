"""Substrate construction for the human macro-scale connectome (undirected-only).

A ``HumanSubstrateBuilder`` loads a single-subject human SC once, precomputes its
undirected empirical weight pool and a fixed Louvain partition, then turns any
``(condition, variant, seed)`` cell into a weighted symmetric recurrent matrix
``W``. It is the undirected analogue of the C. elegans ``SubstrateBuilder`` --
exposing the same duck-typed interface the generic runner consumes
(``weighted``, ``summary``, ``sign_coverage``, ``diagnostics``,
``connectome_supercritical_radii``) -- for the three undirected conditions of the
sign x tail factorial:

    human_gaussian          symmetric gaussian on the topology -> tail/normal baseline
    human_empirical_signed  real magnitudes, balanced ± sign   -> sign control
    human_empirical         real SC weights                    -> connectome substrate

Simpler than the C. elegans builder: the SC is already symmetric + weighted (no
directed processing, no reciprocal-sum derivation) and there is no Dale layer
(``sign_coverage`` is trivially all-excitatory). Nulls use the undirected paths of
the shared generators; weights come from the shared symmetric schemes.
"""

import warnings

import networkx as nx
import numpy as np

from src.connectomes.human_suarez import load as load_human, load_built_consensus
from src.nulls import (
    random_gaussian,
    erdos_renyi,
    degree_rewire,
    clustering_rewire,
    modularity_rewire,
)
from src.nulls.validation import validate_null
from src.reservoir.weights import apply_weight_scheme

from experiments.human import matrix_config as config


class HumanSubstrateBuilder:
    def __init__(self, source: str | None = None, scale: int | None = None,
                 subject: int | None = None):
        self.source = config.SOURCE if source is None else source
        self.scale = config.SCALE if scale is None else scale
        self.subject = config.SUBJECT if subject is None else subject
        if self.source == "consensus":
            self.connectome = load_built_consensus(scale=self.scale)
        elif self.source == "single_subject":
            self.connectome = load_human(scale=self.scale, subject=self.subject)
        else:
            raise ValueError(f"unknown substrate source {self.source!r}")

        # Real symmetric weighted SC = the human_empirical connectome. Binary
        # symmetric mask + upper-triangle edge weights = the empirical pool the
        # nulls sample from.
        self.sc_weighted = self.connectome.adjacency.astype(float).copy()
        self.mask = (self.sc_weighted != 0).astype(float)  # binary symmetric
        self._upper = np.triu(self.mask, k=1).astype(bool)
        self.empirical_pool = self.sc_weighted[self._upper].copy()

        # No Dale layer for a macro-scale parcellation: all-excitatory placeholder
        # so the runner's sign_coverage print + summary() work unchanged.
        n_nodes = int(self.mask.shape[0])
        self.sign_coverage = {
            "n_inhibitory": 0,
            "n_excitatory": n_nodes,
            "inhibitory_labels": [],
        }

        # Fixed Louvain partition for rung 4 (one, undirected).
        self.partition = nx.community.louvain_communities(
            nx.from_numpy_array(self.mask), seed=config.LOUVAIN_SEED
        )

        self._mask_cache: dict = {}
        self.diagnostics: list[dict] = []

    # -- mask generation (cached + validated) -------------------------------
    def get_mask(self, variant: str, seed: int) -> np.ndarray:
        key = (variant, seed)
        if key in self._mask_cache:
            return self._mask_cache[key]

        base = self.mask
        if variant == "connectome":
            mask = base.copy()
        elif variant == "random_gaussian":
            mask = random_gaussian.generate(base, seed=seed, directed=False)
        elif variant == "erdos_renyi":
            mask = erdos_renyi.generate(base, seed=seed, directed=False)
        elif variant == "degree_rewire":
            mask = degree_rewire.generate(
                base, seed=seed, directed=False,
                n_swaps_multiplier=config.SWAP_MULTIPLIER,
            )
        elif variant == "clustering_rewire":
            with warnings.catch_warnings():
                warnings.simplefilter("error", RuntimeWarning)
                mask, diag = clustering_rewire.generate(
                    base, seed=seed, directed=False,
                    tolerance=config.CLUSTERING_TOLERANCE,
                    n_swaps_multiplier=config.SWAP_MULTIPLIER,
                    return_diagnostics=True,
                )
            self._record_clustering(variant, seed, base, mask, diag)
        elif variant == "modularity_rewire":
            mask, diag = modularity_rewire.generate(
                base, seed=seed, directed=False,
                community_partition=self.partition,
                n_swaps_multiplier=config.SWAP_MULTIPLIER,
                return_diagnostics=True,
            )
            self._record_modularity(variant, seed, base, mask, diag)
        else:
            raise ValueError(f"unknown variant {variant!r}")

        if variant == "random_gaussian":
            self._record_random(variant, seed, base, mask)
        elif variant == "erdos_renyi":
            self._record_edge_count(variant, seed, base, mask)
        elif variant == "degree_rewire":
            self._record_degree(variant, seed, base, mask)

        self._mask_cache[key] = mask
        return mask

    # -- weighting per condition -------------------------------------------
    def weighted(self, condition: str, variant: str, seed: int) -> np.ndarray:
        # Placement control: connectome topology + a permutation of its real
        # weights. Bypasses the mask ladder entirely.
        if variant == "connectome_weight_permuted":
            return self._weight_permuted(condition, seed)

        mask = self.get_mask(variant, seed)

        if condition == "human_gaussian":
            # Every variant (incl. connectome) gets fresh symmetric gaussian
            # weights; only the mask differs.
            return apply_weight_scheme(mask, "symmetric_gaussian", seed=seed)

        if condition == "human_empirical":
            # Connectome keeps its REAL weights; nulls sample the empirical pool.
            if variant == "connectome":
                return self.sc_weighted.copy()
            return apply_weight_scheme(
                mask, "symmetric_empirical", seed=seed,
                empirical_weights=self.empirical_pool,
            )

        if condition == "human_empirical_signed":
            # human_empirical with a balanced random sign per edge (sign control).
            # Connectome keeps its exact real magnitudes; only the sign is random.
            if variant == "connectome":
                rng = np.random.default_rng(seed)
                up = self._upper
                signs = rng.choice([-1.0, 1.0], size=int(up.sum()))
                signed = np.zeros_like(self.sc_weighted)
                signed[up] = self.sc_weighted[up] * signs
                return signed + signed.T
            return apply_weight_scheme(
                mask, "symmetric_empirical_randsign", seed=seed,
                empirical_weights=self.empirical_pool,
            )

        raise ValueError(f"unknown condition {condition!r}")

    def _weight_permuted(self, condition: str, seed: int) -> np.ndarray:
        """Connectome topology + a permutation of its real weights (placement control).

        Holds the topology + exact weight multiset fixed and scrambles which edge
        carries which weight (permutation, not the rung nulls' with-replacement
        resample). Decomposes:

            connectome vs this          -> weight PLACEMENT (topology + multiset fixed)
            this       vs degree_rewire  -> TOPOLOGY (placement randomised in both)

        For human_gaussian the "real weights" are a symmetric-gaussian draw, so
        permuting them is distribution-preserving -> a negative control that
        should match the connectome.
        """
        rng = np.random.default_rng(seed)
        up = self._upper

        if condition == "human_gaussian":
            base_W = apply_weight_scheme(self.mask, "symmetric_gaussian", seed=seed)
            permuted = np.zeros_like(base_W)
            permuted[up] = rng.permutation(base_W[up])
            return permuted + permuted.T

        if condition == "human_empirical":
            permuted = np.zeros_like(self.sc_weighted)
            permuted[up] = rng.permutation(self.empirical_pool)
            return permuted + permuted.T

        if condition == "human_empirical_signed":
            signs = rng.choice([-1.0, 1.0], size=int(up.sum()))
            permuted = np.zeros_like(self.sc_weighted)
            permuted[up] = rng.permutation(self.empirical_pool) * signs
            return permuted + permuted.T

        raise ValueError(f"unknown condition {condition!r}")

    # -- validation recorders (undirected) ----------------------------------
    def _record_random(self, variant, seed, base, mask):
        self.diagnostics.append(dict(
            topology="undirected", variant=variant, seed=seed,
            property="density_in_expectation", preserved=True,
            base_edges=int((base != 0).sum()), mask_edges=int((mask != 0).sum()),
        ))

    def _record_edge_count(self, variant, seed, base, mask):
        check = validate_null(base, mask, "edge_count")
        assert check["preserved"], f"erdos_renyi seed={seed}: edge count not preserved."
        self.diagnostics.append(dict(
            topology="undirected", variant=variant, seed=seed,
            property="edge_count", preserved=True,
        ))

    def _record_degree(self, variant, seed, base, mask):
        check = validate_null(base, mask, "degree_sequence")
        assert check["preserved"], (
            f"degree_rewire seed={seed}: degree_sequence not preserved."
        )
        self.diagnostics.append(dict(
            topology="undirected", variant=variant, seed=seed,
            property="degree_sequence", preserved=True,
        ))

    def _record_clustering(self, variant, seed, base, mask, diag):
        check = validate_null(base, mask, "clustering",
                              tolerance=config.CLUSTERING_TOLERANCE)
        assert check["preserved"], (
            f"{variant} seed={seed}: clustering not preserved within "
            f"{config.CLUSTERING_TOLERANCE} (expected={check['expected']:.4f}, "
            f"actual={check['actual']:.4f})"
        )
        self.diagnostics.append(dict(
            topology="undirected", variant=variant, seed=seed, property="clustering",
            preserved=True, acceptance_rate=diag["acceptance_rate"],
            clustering_initial=diag.get("clustering_initial"),
            clustering_final=diag.get("clustering_final"),
            T_initial=diag.get("T_initial"), T_final=diag.get("T_final"),
        ))

    def _record_modularity(self, variant, seed, base, mask, diag):
        check = validate_null(base, mask, "modularity", tolerance=0.01,
                              community_partition=self.partition)
        assert check["preserved"], f"{variant} seed={seed}: modularity not preserved."
        self.diagnostics.append(dict(
            topology="undirected", variant=variant, seed=seed, property="modularity",
            preserved=True, acceptance_rate=diag["acceptance_rate"],
            n_communities=diag.get("n_communities"),
            Q_initial=diag.get("Q_initial"), Q_final=diag.get("Q_final"),
        ))

    # -- operating-point helper --------------------------------------------
    def connectome_supercritical_radii(self, conditions, n_seeds: int = 10) -> dict:
        """Per-condition ``sr_crit = 1 / bulk95_ratio`` (seed-averaged), used to
        shade each metric-vs-sr panel's "connectome supercritical" region."""
        from src.analysis.spectral import spectral_metrics

        out = {}
        for condition in conditions:
            ratios = [
                spectral_metrics(self.weighted(condition, "connectome", s))["bulk95_ratio"]
                for s in range(n_seeds)
            ]
            mean_ratio = float(np.mean(ratios))
            if mean_ratio > 1e-9:
                out[condition] = 1.0 / mean_ratio
        return out

    # -- summary ------------------------------------------------------------
    def summary(self) -> dict:
        n_nodes = int(self.mask.shape[0])
        n_edges = int(self.mask.sum() // 2)
        return {
            "connectome": f"human_suarez_{self.source}",
            "scale_n_nodes": n_nodes,
            "subject": self.subject,
            "n_undirected_edges": n_edges,
            "empirical_pool_size": int(self.empirical_pool.size),
            "density": n_edges / (n_nodes * (n_nodes - 1) / 2),
            "weight_transform": config.WEIGHT_TRANSFORM,
            "n_inhibitory": self.sign_coverage["n_inhibitory"],
            "n_excitatory": self.sign_coverage["n_excitatory"],
            "partition_sizes": sorted([len(c) for c in self.partition], reverse=True),
        }

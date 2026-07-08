"""Substrate + anatomical I/O placement for the human routing thread (undirected).

Wraps ``HumanSubstrateBuilder`` on the **with-subcortical published consensus**
(N=463/1015 -- the self-built consensus is cortical-only, so subcortical *input*
needs this graph) and adds anatomical input/output routing on top of the standard
weighting + null ladder:

  * input  -> the 15 **subcortical** nodes (Suárez's thalamus/BG/hippocampus/amygdala)
  * output -> per **Yeo intrinsic network** (+ a pooled-cortex) readout aperture

Two placement controls (both on the REAL connectome ``W``), each isolating one clean
question, alongside the null ladder:

    connectome vs connectome_random_readout  -> does the READOUT-NETWORK identity matter
                                                (subcortical input held fixed; readout =
                                                a size-matched RANDOM cortical patch)
    connectome vs connectome_dense_input     -> is the edge-of-chaos peak due to the
                                                SUBCORTICAL INPUT vs the substrate
                                                (input made DENSE on the same graph)
    connectome vs null ladder (fixed I/O)    -> does the RECURRENCE matter given routing

Why the readout-only placement control (not random input): the reservoir is built
ONCE per (variant, seed) with a single ``Win``, then read through every aperture. A
*random input* placement is therefore shared across all apertures and cannot be kept
disjoint from the cortical readouts (whose union is the whole cortex), so random input
LEAKS directly into the readout (~15/15 input nodes land in the pooled-cortex readout)
-- an unfair advantage the anatomical subcortical input never has. Holding input at the
subcortical nodes (disjoint from every cortical readout by construction) makes the
placement comparison leakage-free and turns it into Suárez's actual claim: is reading
from a specific intrinsic network better than from a random equal-sized cortical patch.

Every standard variant (connectome, weight-permuted control, 5-rung ladder) keeps the
FIXED anatomical I/O; only ``W`` changes. The generic runner picks up ``input_nodes`` +
``cell_task_kwargs`` via its optional routing hooks.
"""

import numpy as np

from experiments.human.substrates import HumanSubstrateBuilder
from src.connectomes.human_suarez import load_routing_geometry, YEO_NETWORKS

# Placement controls (real W; controls, not null rungs).
RANDOM_READOUT_VARIANT = "connectome_random_readout"   # subctx input, RANDOM cortical readout
DENSE_INPUT_VARIANT = "connectome_dense_input"          # DENSE input, anatomical readout
PLACEMENT_VARIANTS = (RANDOM_READOUT_VARIANT, DENSE_INPUT_VARIANT)

# Offset so the random-readout RNG stream is independent of the mask/weight/Win
# streams (which derive from the bare construction seed).
_READOUT_PLACEMENT_OFFSET = 600_000


class RoutingSubstrateBuilder(HumanSubstrateBuilder):
    def __init__(self, scale: int = 448, source: str = "published_full"):
        # ``source`` is the ONLY substrate-provenance coupling point. Default
        # "published_full" = the Suárez published with-subcortical consensus, used
        # first as the fast path to verify we reproduce their edge-of-chaos MC. The
        # INTENDED substrate is a SELF-BUILT with-subcortical consensus (as for the
        # cortical probe; published-as-anchor-only). To swap it in later: add a
        # loader + a HumanSubstrateBuilder source (e.g. "consensus_full") and pass
        # source=... here -- the routing geometry, apertures, placement controls,
        # and null ladder below are all substrate-agnostic (they key on node
        # identity, not on which consensus produced the weights), so nothing else
        # changes. The release geometry (subctx/Yeo indices) is reused either way,
        # since a self-built with-subctx consensus keeps the release node order.
        super().__init__(source=source, scale=scale)
        self.geom = load_routing_geometry(scale)
        self.subcortical = np.asarray(self.geom["subcortical"])
        self.cortical = np.asarray(self.geom["cortical"])
        self.yeo_groups = {k: np.asarray(v) for k, v in self.geom["yeo_groups"].items()}
        # Fixed anatomical readout apertures: pooled cortex + each Yeo network.
        self.anatomical_apertures = {"cortex": self.cortical}
        for name in YEO_NETWORKS:
            self.anatomical_apertures[name] = self.yeo_groups[name]

    # -- W: both placement controls reuse the real connectome's weights --------
    def weighted(self, condition: str, variant: str, seed: int) -> np.ndarray:
        if variant in PLACEMENT_VARIANTS:
            variant = "connectome"
        return super().weighted(condition, variant, seed)

    # -- input routing (runner hook) ------------------------------------------
    def input_nodes(self, variant: str, seed: int):
        # DENSE-input control: no routing -> None -> dense Win on all nodes (Fix 2,
        # isolates whether the edge-of-chaos peak is the subcortical INPUT vs the
        # substrate). Every other variant (connectome, nulls, random-READOUT
        # control) keeps the anatomical subcortical input.
        if variant == DENSE_INPUT_VARIANT:
            return None
        return self.subcortical

    # -- readout apertures per cell (runner hook) -----------------------------
    def cell_task_kwargs(self, condition: str, variant: str, seed: int) -> dict:
        if variant == RANDOM_READOUT_VARIANT:
            return {"readout_apertures": self._random_readout_apertures(seed)}
        return {"readout_apertures": self.anatomical_apertures}

    def _random_readout_apertures(self, seed: int) -> dict:
        """Size-matched random CORTICAL readout patches (subcortical input held fixed).

        Isolates readout-network IDENTITY: each Yeo network is replaced by a random
        cortical set of the same size. Leakage-free -- the input stays subcortical,
        disjoint from every cortical readout. ``cortex`` (all cortical) has no smaller
        random match, so it stays the full cortex (that aperture carries no placement
        contrast -- it is a recurrence/peak reference, not a placement test).
        """
        rng = np.random.default_rng(seed + _READOUT_PLACEMENT_OFFSET)
        apertures = {"cortex": self.cortical}
        for name in YEO_NETWORKS:
            m = int(self.yeo_groups[name].size)
            apertures[name] = rng.choice(self.cortical, size=m, replace=False)
        return apertures

    # -- summary --------------------------------------------------------------
    def summary(self) -> dict:
        s = super().summary()
        s.update(
            routing="anatomical (subcortical input / Yeo-network + pooled-cortex readout)",
            n_input_nodes=int(self.subcortical.size),
            readout_apertures={k: int(np.asarray(v).size)
                               for k, v in self.anatomical_apertures.items()},
            placement_controls={
                RANDOM_READOUT_VARIANT: "subctx input, random size-matched cortical readout",
                DENSE_INPUT_VARIANT: "dense input (all nodes), anatomical readout",
            },
        )
        return s

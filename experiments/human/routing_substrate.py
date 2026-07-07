"""Substrate + anatomical I/O placement for the human routing thread (undirected).

Wraps ``HumanSubstrateBuilder`` on the **with-subcortical published consensus**
(N=463/1015 -- the self-built consensus is cortical-only, so subcortical *input*
needs this graph) and adds anatomical input/output routing on top of the standard
weighting + null ladder:

  * input  -> the 15 **subcortical** nodes (Suárez's thalamus/BG/hippocampus/amygdala)
  * output -> per **Yeo intrinsic network** (+ a pooled-cortex) readout aperture

plus one **random-placement control** variant (``connectome_random_routing``): the
REAL connectome ``W`` with input at 15 random nodes and each readout aperture
re-drawn as a size-matched random cortical set (per seed). Two decompositions,
mirroring the ``connectome_weight_permuted`` weight-placement control:

    connectome vs connectome_random_routing  -> does anatomical I/O PLACEMENT matter
    connectome vs null ladder (fixed I/O)     -> does the RECURRENCE matter given routing

Every standard variant (connectome, weight-permuted control, 5-rung ladder) keeps
the FIXED anatomical I/O node indices; only ``W`` changes. The generic runner picks
up ``input_nodes`` + ``cell_task_kwargs`` via its optional routing hooks.
"""

import numpy as np

from experiments.human.substrates import HumanSubstrateBuilder
from src.connectomes.human_suarez import load_routing_geometry, YEO_NETWORKS

# The random-placement control variant (a placement control, not a null rung).
RANDOM_ROUTING_VARIANT = "connectome_random_routing"

# Offsets so the placement RNG streams are independent of the mask/weight/Win
# streams (which derive from the bare construction seed).
_INPUT_PLACEMENT_OFFSET = 500_000
_READOUT_PLACEMENT_OFFSET = 600_000


class RoutingSubstrateBuilder(HumanSubstrateBuilder):
    def __init__(self, scale: int = 448, source: str = "published_full"):
        # ``source`` is the ONLY substrate-provenance coupling point. Default
        # "published_full" = the Suárez published with-subcortical consensus, used
        # first as the fast path to verify we reproduce their edge-of-chaos MC. The
        # INTENDED substrate is a SELF-BUILT with-subcortical consensus (as for the
        # cortical probe; published-as-anchor-only). To swap it in later: add a
        # loader + a HumanSubstrateBuilder source (e.g. "consensus_full") and pass
        # source=... here -- the routing geometry, apertures, random-placement
        # control, and null ladder below are all substrate-agnostic (they key on
        # node identity, not on which consensus produced the weights), so nothing
        # else changes. The release geometry (subctx/Yeo indices) is reused either
        # way, since a self-built with-subctx consensus keeps the release node order.
        super().__init__(source=source, scale=scale)
        self.geom = load_routing_geometry(scale)
        self.subcortical = np.asarray(self.geom["subcortical"])
        self.cortical = np.asarray(self.geom["cortical"])
        self.yeo_groups = {k: np.asarray(v) for k, v in self.geom["yeo_groups"].items()}
        # Fixed anatomical readout apertures: pooled cortex + each Yeo network.
        self.anatomical_apertures = {"cortex": self.cortical}
        for name in YEO_NETWORKS:
            self.anatomical_apertures[name] = self.yeo_groups[name]

    # -- W: the random-routing control reuses the real connectome's weights ----
    def weighted(self, condition: str, variant: str, seed: int) -> np.ndarray:
        if variant == RANDOM_ROUTING_VARIANT:
            variant = "connectome"
        return super().weighted(condition, variant, seed)

    # -- input routing (runner hook) ------------------------------------------
    def input_nodes(self, variant: str, seed: int) -> np.ndarray:
        if variant == RANDOM_ROUTING_VARIANT:
            rng = np.random.default_rng(seed + _INPUT_PLACEMENT_OFFSET)
            return rng.choice(self.geom["n_full"], size=self.subcortical.size,
                              replace=False)
        return self.subcortical

    # -- readout apertures per cell (runner hook) -----------------------------
    def cell_task_kwargs(self, condition: str, variant: str, seed: int) -> dict:
        if variant == RANDOM_ROUTING_VARIANT:
            return {"readout_apertures": self._random_apertures(seed)}
        return {"readout_apertures": self.anatomical_apertures}

    def _random_apertures(self, seed: int) -> dict:
        """Size-matched random CORTICAL readout sets (isolates network identity).

        ``cortex`` (all cortical) has no smaller random match, so it stays the full
        cortex -> that aperture isolates INPUT placement (readout held constant)
        while the Yeo apertures randomise WHICH cortical nodes are read.
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
        )
        return s

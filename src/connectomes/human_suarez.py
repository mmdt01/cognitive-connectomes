"""Human structural connectome loaders (Griffa 2019 primary + Suárez 2021 release).

Primary data: ``data/human/Individual_Connectomes.mat`` (Griffa, Alemán-Gómez, Hagmann,
Zenodo 2872624; gitignored) -- ``connMatrices.SC`` is a length-5 object array over the
CORTICAL Lausanne/Cammoun scales N = 68/114/219/448/1000, each ``(N, N, 70)`` (70
subjects; symmetric, non-negative fibre densities). Geometry and the with-subcortical
data come from the Suárez 2021 release (``data/human/Suarez2021_Data/``). Full provenance
in ``data/human/README.md``.

Public surface, grouped:
  * ``load`` -- one subject's SC (dependency-free substrate for the plumbing smoke).
  * ``build_consensus`` / ``load_built_consensus`` -- self-built **cortical** (N=448/1000)
    distance-dependent group consensus (SC from the primary .mat) and its cache.
  * ``build_consensus_full`` / ``load_built_consensus_full`` -- self-built
    **with-subcortical** (N=463/1015) consensus (SC from the release individual stacks,
    the only with-subctx source) and its cache -- the anatomical I/O-routing substrate.
  * ``load_published_consensus`` / ``load_published_consensus_full`` / ``load_published_full``
    -- the published Suárez consensus (a validation anchor; the full one was the
    pre-self-build routing substrate).
  * ``load_routing_geometry`` + ``YEO_NETWORKS`` -- node sets for anatomical I/O routing.

Both self-builds run the vendored Betzel-2018 ``struct_consensus`` on the release geometry
(parcel centroids, hemisphere labels); they differ only in the SC source and whether the
geometry is cortical-restricted. Convention: SC is symmetric (undirected), so the reservoir
orientation ``adjacency[i, j] = weight j->i`` is moot -- the matrix is its own transpose.
"""

from pathlib import Path

import numpy as np
from scipy.io import loadmat
from scipy.spatial.distance import cdist

from . import ConnectomeData
from .consensus import struct_consensus

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DATA_PATH = _REPO_ROOT / "data" / "human" / "Individual_Connectomes.mat"
_RELEASE_DIR = _REPO_ROOT / "data" / "human" / "Suarez2021_Data"
_BUILT_DIR = _REPO_ROOT / "data" / "human" / "built_consensus"

# Lausanne/Cammoun cortical scales, in .mat object-array order.
SCALES = (68, 114, 219, 448, 1000)

# Map a .mat cortical scale (node count) to the release geometry tag. The release stores
# data at the WITH-subcortical scales (463 = 448 cortical + 15 subctx; 1015 = 1000 + 15);
# the cortical loaders restrict to the cortical subset via the cortical mask. Verified
# node-order correspondence (.mat SC <-> release cortical subset: node-strength +
# edge-weight, r >= 0.98). No N=219 in the release.
_MAT_N_TO_RELEASE_TAG = {448: "250", 1000: "500"}

# The 7 cortical Yeo intrinsic networks, in rsn_names.npy order (subctx excluded). These
# are Suárez's readout apertures; subcortical (subctx) is the input aperture.
YEO_NETWORKS = ("VIS", "SM", "DA", "VA", "LIM", "FP", "DMN")


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _graph_stats(C: np.ndarray) -> tuple[int, float, int]:
    """``(n_undirected_edges, density, n_isolated_nodes)`` for a symmetric weighted matrix."""
    mask = C != 0
    N = C.shape[0]
    n_edges = int(mask.sum() // 2)
    density = n_edges / (N * (N - 1) / 2)
    n_isolated = int((mask.sum(axis=1) == 0).sum())
    return n_edges, density, n_isolated


def _assert_symmetric_nonneg(C: np.ndarray, name: str) -> None:
    asym = float(np.max(np.abs(C - C.T)))
    assert asym < 1e-9, f"{name} not symmetric, max|C-C.T|={asym:.3e}"
    assert C.min() >= 0.0, f"{name} has negative weights, min={C.min():.3e}"


def _node_labels(stem: str, N: int) -> list[str]:
    """Placeholder region labels ``f"{stem}{N}_region0000"``... (the data has no labels)."""
    return [f"{stem}{N}_region{i:04d}" for i in range(N)]


def _release_tag(scale: int) -> str:
    tag = _MAT_N_TO_RELEASE_TAG.get(scale)
    if tag is None:
        raise ValueError(f"no release data for scale {scale} "
                         f"(available: {sorted(_MAT_N_TO_RELEASE_TAG)})")
    return tag


def _release_npy(kind: str, scale: int, *, allow_pickle: bool = False) -> np.ndarray:
    """Load ``Suarez2021_Data/<kind>_<tag>.npy`` for a .mat cortical ``scale``.

    ``kind`` is the path up to the ``_<tag>.npy`` suffix, e.g. ``coords/coords_human``,
    ``cortical/cortical_human``, ``connectivity/consensus/human``.
    """
    return np.load(_RELEASE_DIR / f"{kind}_{_release_tag(scale)}.npy",
                   allow_pickle=allow_pickle)


# ---------------------------------------------------------------------------
# Primary .mat -- single-subject SC (plumbing smoke)
# ---------------------------------------------------------------------------

def _load_sc_stack(scale: int) -> np.ndarray:
    """Return the ``(N, N, n_subjects)`` cortical SC stack for ``scale`` from the .mat.

    Loads only ``connMatrices`` and locates the scale by node count (not index order).
    """
    if scale not in SCALES:
        raise ValueError(f"Unknown scale {scale!r}; expected one of {SCALES}")
    raw = loadmat(_DATA_PATH, struct_as_record=False, squeeze_me=True,
                  variable_names=["connMatrices"])
    sc = raw["connMatrices"].SC
    stacks = [np.asarray(sc[i]) for i in range(len(sc))]
    match = [s for s in stacks if s.shape[0] == scale]
    if not match:
        raise ValueError(
            f"scale {scale} not found in .mat (shapes: {[s.shape for s in stacks]})")
    return np.array(match[0], dtype=float)


def load(scale: int = 219, subject: int = 0) -> ConnectomeData:
    """Load a single-subject human SC matrix as a reservoir substrate.

    Parameters
    ----------
    scale
        Lausanne parcellation scale (node count): 68/114/219/448/1000. Default 219
        (closest to C. elegans N=300, for a node-count-matched comparison).
    subject
        Subject index into the 0..69 stack. Default 0 (fixed representative graph).

    Returns
    -------
    ConnectomeData
        ``adjacency`` = the subject's symmetric, non-negative, zero-diagonal SC. No node
        labels/coordinates exist in the .mat, so placeholder region labels are used.
    """
    stack = _load_sc_stack(scale)
    n_subjects = stack.shape[2]
    if not 0 <= subject < n_subjects:
        raise ValueError(f"subject {subject} out of range 0..{n_subjects - 1}")

    W = np.array(stack[:, :, subject], dtype=float)
    N = W.shape[0]
    _assert_symmetric_nonneg(W, "SC")  # dMRI SC is symmetric + non-negative by construction

    # Strip the diagonal (self-weights present in the raw SC): the pipeline requires a
    # zero diagonal everywhere (weight-scheme asserts + null parity), mirroring the
    # C. elegans self-loop removal.
    self_loops_removed = int((np.diag(W) != 0).sum())
    self_loop_weight_removed = float(np.diag(W).sum())
    np.fill_diagonal(W, 0.0)

    n_edges, density, n_isolated = _graph_stats(W)
    print(f"Loaded Suárez 2021 human SC (single subject): scale N={N}, "
          f"subject={subject}/{n_subjects - 1}, undirected edges={n_edges}, "
          f"density={density:.3%}, self-loops removed={self_loops_removed}, "
          f"isolated nodes={n_isolated}")
    if n_isolated:
        print(f"  WARNING: {n_isolated} isolated node(s) -> dead reservoir unit(s).")

    metadata = {
        "source": "Suárez et al. 2021, Nat. Mach. Intell. 3:771-786",
        "modality": "dMRI structural connectivity (streamline fibre density)",
        "parcellation": f"Lausanne/Cammoun scale N={N}",
        "processing": "single_subject",
        "subject_index": subject,
        # The .mat carries 70 subjects; the paper reports 66 (logged, not reconciled).
        "n_subjects_in_file": n_subjects,
        "processing_notes": (
            "Single subject's SC from connMatrices.SC. Symmetric (undirected, normal), "
            "non-negative (fibre densities -- normalized fractions, not integer counts). "
            "Diagonal zeroed for pipeline/null parity. No node labels or coordinates in "
            "the .mat; placeholder region indices used."
        ),
        "n_edges": n_edges,
        "density": density,
        "self_loops_removed": self_loops_removed,
        "self_loop_weight_removed": self_loop_weight_removed,
        "n_isolated_nodes": n_isolated,
    }
    return ConnectomeData(adjacency=W, node_labels=_node_labels("scale", N), metadata=metadata)


# ---------------------------------------------------------------------------
# Release geometry (parcel centroids, hemisphere labels, Yeo/RSN groups)
# ---------------------------------------------------------------------------

def _load_release_geometry(scale: int):
    """Cortical-restricted ``(coords, hemiid, cortical_index)`` for a .mat scale.

    The release geometry lives at the with-subcortical scales; the cortical nodes are
    interspersed (not a leading block), so select via the cortical mask. Node order then
    matches the .mat SC (verified: node-strength + edge-weight correspondence, r >= 0.98).
    """
    coords = _release_npy("coords/coords_human", scale)
    hemiid = _release_npy("hemispheres/hemiid_human", scale)
    cortical = _release_npy("cortical/cortical_human", scale)
    cidx = np.where(cortical != 0)[0]
    if len(cidx) != scale:
        raise ValueError(f"cortical node count {len(cidx)} != scale {scale}")
    return coords[cidx], hemiid[cidx], cidx


def _load_release_geometry_full(scale: int):
    """Full (with-subcortical) ``(coords, hemiid)`` -- ALL N=463/1015 nodes, unlike the
    cortical-restricted ``_load_release_geometry``."""
    return (_release_npy("coords/coords_human", scale),
            _release_npy("hemispheres/hemiid_human", scale))


def load_routing_geometry(scale: int = 448) -> dict:
    """Node-set geometry for anatomical I/O routing on the with-subcortical graph.

    Every index is into the *full* (N=463 @scale 448 / N=1015 @scale 1000) node ordering,
    matched to ``load_published_consensus_full`` / ``load_built_consensus_full``. Returns
    the 15 subcortical input nodes, the cortical nodes, the per-Yeo-network cortical
    readout groups, and coords/hemiid. Subcortical nodes are interspersed, so groups are
    built from the cortical mask + RSN labels, never a raw slice.
    """
    coords = _release_npy("coords/coords_human", scale)
    hemiid = _release_npy("hemispheres/hemiid_human", scale)
    cortical = _release_npy("cortical/cortical_human", scale)
    rsn = _release_npy("rsn_mapping/rsn_human", scale, allow_pickle=True)
    rsn = np.asarray([str(x) for x in rsn])

    cortical_idx = np.where(cortical != 0)[0]
    subctx_idx = np.where(cortical == 0)[0]
    if len(cortical_idx) != scale:
        raise ValueError(f"cortical node count {len(cortical_idx)} != scale {scale}")

    yeo_groups = {name: np.where(rsn == name)[0] for name in YEO_NETWORKS}
    # The cortical nodes must partition exactly into the 7 Yeo networks, and the
    # subcortical nodes must all be labelled subctx (else the release ordering has drifted
    # from the consensus ordering -- a hard error, not a silent mislabel).
    covered = sum(len(v) for v in yeo_groups.values())
    assert covered == scale, f"Yeo groups cover {covered} nodes; {scale} cortical expected"
    for name, idx in yeo_groups.items():
        assert np.all(cortical[idx] != 0), f"Yeo network {name} includes non-cortical nodes"
    assert np.all(rsn[subctx_idx] == "subctx"), "subcortical nodes not all labelled subctx"

    return {
        "scale": scale,
        "n_full": int(len(cortical)),
        "subcortical": subctx_idx,
        "cortical": cortical_idx,
        "rsn_labels": rsn,
        "yeo_groups": yeo_groups,
        "coords": coords,
        "hemiid": hemiid,
    }


# ---------------------------------------------------------------------------
# Published Suárez consensus (validation anchor; the full one was the pre-self-build
# routing substrate)
# ---------------------------------------------------------------------------

def load_published_consensus(scale: int) -> np.ndarray:
    """The published consensus restricted to the cortical nodes, symmetric + zero-diagonal.
    Used ONLY to validate the self-built cortical consensus."""
    _, _, cidx = _load_release_geometry(scale)
    C = _release_npy("connectivity/consensus/human", scale)
    C = C[np.ix_(cidx, cidx)].astype(float).copy()
    np.fill_diagonal(C, 0.0)
    return C


def load_published_consensus_full(scale: int = 448) -> np.ndarray:
    """The published *with-subcortical* consensus (NOT cortical-restricted): full N=463
    (@scale 448) / N=1015 (@scale 1000). Validates the self-built full consensus and was
    the pre-self-build routing substrate. Symmetric, non-negative, zero-diagonal."""
    C = _release_npy("connectivity/consensus/human", scale).astype(float).copy()
    np.fill_diagonal(C, 0.0)
    _assert_symmetric_nonneg(C, "published consensus")
    return C


def load_published_full(scale: int = 448) -> ConnectomeData:
    """The published with-subcortical consensus as a ``ConnectomeData`` substrate.

    Thin ``ConnectomeData`` wrapper over ``load_published_consensus_full`` so the graph
    plugs into ``HumanSubstrateBuilder(source="published_full")`` -- the *fast verification
    path* for the routing thread, since superseded by the self-built
    ``load_built_consensus_full``.
    """
    C = load_published_consensus_full(scale)
    N = C.shape[0]
    n_edges, density, _ = _graph_stats(C)
    metadata = {
        "source": "Suárez et al. 2021 published distance-dependent consensus (Betzel 2018)",
        "processing": "published_with_subcortical",
        "scale": scale,
        "n_full": N,
        "n_edges": n_edges,
        "density": density,
        "processing_notes": (
            "Published with-subcortical group consensus (N=463 @scale 448 / N=1015 @scale "
            "1000). Symmetric, non-negative, zero-diagonal. The fast verification-path "
            "routing substrate, superseded by the self-built with-subcortical consensus."
        ),
    }
    return ConnectomeData(adjacency=C, node_labels=_node_labels("published_full_scale", N),
                          metadata=metadata)


# ---------------------------------------------------------------------------
# Self-built distance-dependent group consensus (Betzel 2018 struct_consensus)
# ---------------------------------------------------------------------------

def _load_release_individual_stack(scale: int) -> np.ndarray:
    """The with-subcortical per-subject SC stack ``(N_full, N_full, 70)`` from the
    release's ``connectivity/individual/`` (restored separately; ~665 MB). N_full = 463
    (@scale 448) / 1015 (@scale 1000). Symmetric, non-negative fibre densities; node order
    matches the release geometry (subcortical interspersed)."""
    path = _RELEASE_DIR / f"connectivity/individual/human_{_release_tag(scale)}.npy"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found; restore the release's connectivity/individual/ folder "
            f"(the with-subcortical per-subject SC stacks) to build the full consensus.")
    return np.load(path).astype(float)


def _consensus_from(stack, coords, hemiid, weighted, *, scale, kind, label_stem,
                    source, construction, notes) -> ConnectomeData:
    """Shared build: Betzel ``struct_consensus`` -> zero diagonal -> validate -> package.

    Runs the same procedure for both the cortical and with-subcortical builds; only the
    SC ``stack`` and ``coords``/``hemiid`` differ. ``kind`` labels the console line
    (``""`` cortical / ``"with-subcortical "`` full), ``label_stem`` the node-label prefix,
    and ``source``/``construction``/``notes`` the audit metadata.
    """
    distance = cdist(coords, coords)
    C = np.asarray(
        struct_consensus(stack, distance, hemiid.reshape(-1, 1), weighted=weighted),
        dtype=float,
    )
    np.fill_diagonal(C, 0.0)
    _assert_symmetric_nonneg(C, "consensus")

    N = C.shape[0]
    n_edges, density, n_isolated = _graph_stats(C)
    print(f"Built human {kind}consensus (self-derived): N={N} (scale {scale}), "
          f"undirected edges={n_edges}, density={density:.3%}, isolated nodes={n_isolated}")
    if n_isolated:
        print(f"  WARNING: {n_isolated} isolated node(s) -> dead reservoir unit(s).")

    metadata = {
        "source": source,
        "construction": construction,
        "construction_notes": notes,
        "scale": scale,
        "n_nodes": N,
        "weighted": weighted,
        "n_edges": n_edges,
        "density": density,
        "n_isolated_nodes": n_isolated,
    }
    return ConnectomeData(adjacency=C, node_labels=_node_labels(label_stem, N),
                          metadata=metadata)


def build_consensus(scale: int = 448, weighted: bool = True) -> ConnectomeData:
    """Self-built distance-dependent **cortical** group consensus (N=448/1000) from the
    .mat individual SC (the primary Lausanne source) + release geometry, via the vendored
    Betzel-2018 ``struct_consensus``.

    The substrate for the main human probe -- self-derived, NOT the published matrix (which
    validates it; see ``experiments/human/build_consensus.py``). ``weighted=True`` returns
    the mean-fibre-density-weighted consensus (heavy-tailed, non-negative).
    """
    stack = _load_sc_stack(scale)                         # (N, N, 70) cortical SC
    coords, hemiid, _ = _load_release_geometry(scale)
    return _consensus_from(
        stack, coords, hemiid, weighted, scale=scale, kind="", label_stem="scale",
        source="Suárez et al. 2021 individual Lausanne SC (Individual_Connectomes.mat)",
        construction="distance-dependent group consensus (Betzel et al. 2018)",
        notes=(
            f"Self-built from the {stack.shape[2]}-subject cortical individual SC at scale "
            f"N={scale} via the vendored struct_consensus (src/connectomes/consensus.py), "
            f"weighted={weighted} (mean fibre density over all subjects). Geometry "
            f"(centroids -> Euclidean distance, hemisphere labels) from the Suárez 2021 "
            f"release, cortical subset; node order verified against the .mat SC."
        ),
    )


def build_consensus_full(scale: int = 448, weighted: bool = True) -> ConnectomeData:
    """Self-built distance-dependent **with-subcortical** group consensus (N=463/1015) from
    the release's restored individual SC stacks + the full (all-node) geometry, via the
    same Betzel-2018 ``struct_consensus`` as ``build_consensus``.

    The intended anatomical I/O-routing substrate (subcortical input needs the subcortical
    nodes); the .mat is cortical-only, so this build's SC is necessarily release-sourced.
    Validated against the published with-subcortical consensus by
    ``experiments/human/build_consensus.py --full``. ``scale`` keys on the cortical node
    count (448/1000); the returned matrix is N=463/1015.
    """
    stack = _load_release_individual_stack(scale)         # (N_full, N_full, 70) with subctx
    coords, hemiid = _load_release_geometry_full(scale)
    return _consensus_from(
        stack, coords, hemiid, weighted, scale=scale, kind="with-subcortical ",
        label_stem="full_scale",
        source="Suárez et al. 2021 release individual SC (connectivity/individual/)",
        construction=("distance-dependent group consensus (Betzel et al. 2018), "
                      "with subcortical"),
        notes=(
            f"Self-built with-subcortical consensus from the {stack.shape[2]}-subject "
            f"release individual SC at scale N={scale} (+15 subcortical) via the vendored "
            f"struct_consensus, weighted={weighted}. Full release geometry (all-node "
            f"centroids -> Euclidean distance, hemisphere labels). Replaces the published "
            f"consensus as the routing substrate."
        ),
    )


# ---------------------------------------------------------------------------
# Cached self-built consensus loaders (fast path -- avoid reloading the raw SC)
# ---------------------------------------------------------------------------

def _load_cached_consensus(scale: int, *, prefix: str, processing: str, kind: str,
                           label_stem: str, build_cmd: str) -> ConnectomeData:
    """Load a cached self-built consensus ``built_consensus/<prefix>_<scale>.npy`` (+ its
    ``.meta.json``). Shared by ``load_built_consensus`` / ``load_built_consensus_full``."""
    import json

    path = _BUILT_DIR / f"{prefix}_{scale}.npy"
    if not path.exists():
        raise FileNotFoundError(f"{path} not found; build it with `{build_cmd}`.")
    C = np.load(path).astype(float)
    metadata = {"processing": processing, "scale": scale, "cache_path": str(path)}
    meta_path = _BUILT_DIR / f"{prefix}_{scale}.meta.json"
    if meta_path.exists():
        metadata.update(json.loads(meta_path.read_text()).get("metadata", {}))
    N = C.shape[0]
    n_edges, density, _ = _graph_stats(C)
    print(f"Loaded self-built {kind}consensus: N={N}, edges={n_edges}, density={density:.3%}")
    return ConnectomeData(adjacency=C, node_labels=_node_labels(label_stem, N),
                          metadata=metadata)


def load_built_consensus(scale: int = 448) -> ConnectomeData:
    """Load the cached self-built **cortical** consensus (see ``build_consensus.py``). Fast
    path -- reads ``built_consensus/consensus_<scale>.npy`` instead of the 701 MB .mat."""
    return _load_cached_consensus(
        scale, prefix="consensus", processing="consensus_cached", kind="",
        label_stem="scale", build_cmd="python -m experiments.human.build_consensus")


def load_built_consensus_full(scale: int = 448) -> ConnectomeData:
    """Load the cached self-built **with-subcortical** consensus (N=463/1015; see
    ``build_consensus.py --full``) -- the anatomical I/O-routing substrate."""
    return _load_cached_consensus(
        scale, prefix="consensus_full", processing="consensus_full_cached",
        kind="with-subcortical ", label_stem="full_scale",
        build_cmd="python -m experiments.human.build_consensus --full")

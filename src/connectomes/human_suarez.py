"""Suárez et al. 2021 human multi-scale structural connectome loader.

Source: Suárez, Richards, Lajoie, Mišić (2021), "Learning function from
structure in neuromorphic networks", Nature Machine Intelligence 3:771-786.
Group of 70 healthy subjects; Lausanne multi-scale parcellation (Cammoun 2012);
dMRI streamline-derived structural connectivity (SC).

Data file: ``data/human/Individual_Connectomes.mat`` (gitignored; download
separately). ``connMatrices.SC`` is a length-5 object array over Lausanne scales
N = 68/114/219/448/1000, each entry ``(N, N, 70)``: a stack of 70 per-subject
symmetric, non-negative, weighted SC matrices (fibre densities -- normalized
fractions, not integer counts). See ``data/human/README.md``.

This loader returns ONE fixed graph -- a single subject's SC at a chosen scale --
as the reservoir substrate ``W``. It is the dependency-free substrate for the
pipeline-validation smoke; the Suárez distance-dependent group consensus is a
separate, later addition (it needs external Cammoun atlas geometry, absent from
the .mat).

Convention note: the SC is symmetric (undirected), so the reservoir orientation
``adjacency[i, j] = weight from j to i`` is moot here -- the matrix is its own
transpose.
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

# Lausanne/Cammoun scales, in .mat object-array order.
SCALES = (68, 114, 219, 448, 1000)

# Map a .mat cortical scale (node count) to the release geometry tag. The release
# stores geometry at the WITH-subcortical scales (463 = 448 cortical + 15 subctx;
# 1015 = 1000 + 15); we restrict to the cortical subset via the cortical mask.
# Verified node-order correspondence (.mat SC <-> release cortical subset): the
# intra-hemispheric weight fraction, node-strength, and edge-weight all align
# (r >= 0.98). No N=219 in the release.
_MAT_N_TO_RELEASE_TAG = {448: "250", 1000: "500"}


def _load_sc_stack(scale: int) -> np.ndarray:
    """Return the ``(N, N, n_subjects)`` SC stack for the requested scale.

    Loads only the ``connMatrices`` variable and locates the requested scale by
    node count (rather than trusting index order).
    """
    if scale not in SCALES:
        raise ValueError(f"Unknown scale {scale!r}; expected one of {SCALES}")
    raw = loadmat(
        _DATA_PATH, struct_as_record=False, squeeze_me=True,
        variable_names=["connMatrices"],
    )
    sc = raw["connMatrices"].SC
    stacks = [np.asarray(sc[i]) for i in range(len(sc))]
    match = [s for s in stacks if s.shape[0] == scale]
    if not match:
        raise ValueError(
            f"scale {scale} not found in .mat (shapes: {[s.shape for s in stacks]})"
        )
    return np.array(match[0], dtype=float)


def load(scale: int = 219, subject: int = 0) -> ConnectomeData:
    """Load a single-subject human SC matrix as a reservoir substrate.

    Parameters
    ----------
    scale
        Lausanne parcellation scale (node count): 68/114/219/448/1000. Default
        219 (closest to C. elegans N=300, for a node-count-matched comparison).
    subject
        Subject index into the 0..69 stack. Default 0 (the fixed representative
        graph for the smoke).

    Returns
    -------
    ConnectomeData
        ``adjacency`` = the subject's symmetric, non-negative, zero-diagonal SC
        (weighted). No node labels/coordinates exist in the .mat, so placeholder
        region indices are used and ``node_positions`` is left None.
    """
    stack = _load_sc_stack(scale)
    n_subjects = stack.shape[2]
    if not 0 <= subject < n_subjects:
        raise ValueError(f"subject {subject} out of range 0..{n_subjects - 1}")

    W = np.array(stack[:, :, subject], dtype=float)
    N = W.shape[0]

    # dMRI SC is symmetric + non-negative by construction; verify (recon on
    # subject 0, N=219 confirmed exact symmetry and non-negativity).
    asym = float(np.max(np.abs(W - W.T)))
    assert asym < 1e-9, f"expected symmetric SC, max|W-W.T|={asym:.3e}"
    assert W.min() >= 0.0, f"expected non-negative SC, min={W.min():.3e}"

    # Strip the diagonal (recon: subject-0 N=219 carries 217 self-weights). The
    # pipeline requires zero diagonal everywhere (weight-scheme asserts + null
    # parity), mirroring the C. elegans self-loop removal.
    self_loops_removed = int((np.diag(W) != 0).sum())
    self_loop_weight_removed = float(np.diag(W).sum())
    np.fill_diagonal(W, 0.0)

    mask = W != 0
    n_edges = int(mask.sum() // 2)
    n_possible = N * (N - 1) // 2
    density = n_edges / n_possible
    degree = mask.sum(axis=1)
    n_isolated = int((degree == 0).sum())

    print(
        f"Loaded Suárez 2021 human SC (single subject): scale N={N}, "
        f"subject={subject}/{n_subjects - 1}, undirected edges={n_edges}, "
        f"density={density:.3%}, self-loops removed={self_loops_removed}, "
        f"isolated nodes={n_isolated}"
    )
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
            "Single subject's SC from connMatrices.SC. Symmetric (undirected, "
            "normal), non-negative (fibre densities -- normalized fractions, not "
            "integer counts). Diagonal zeroed for pipeline/null parity. No node "
            "labels or coordinates in the .mat; placeholder region indices used."
        ),
        "n_edges": n_edges,
        "density": density,
        "self_loops_removed": self_loops_removed,
        "self_loop_weight_removed": self_loop_weight_removed,
        "n_isolated_nodes": n_isolated,
    }

    node_labels = [f"scale{N}_region{i:04d}" for i in range(N)]
    return ConnectomeData(adjacency=W, node_labels=node_labels, metadata=metadata)


# ---------------------------------------------------------------------------
# Self-built group consensus (from the raw individual SC + release geometry)
# ---------------------------------------------------------------------------

def _load_release_geometry(scale: int):
    """Cortical-restricted ``(coords, hemiid, cortical_index)`` for a .mat scale.

    The release geometry lives at the with-subcortical scales; the cortical nodes
    are interspersed (not a leading block), so select via the cortical mask. Node
    order then matches the .mat SC (verified: hemisphere-organisation, node-
    strength and edge-weight correspondence, r >= 0.98).
    """
    tag = _MAT_N_TO_RELEASE_TAG.get(scale)
    if tag is None:
        raise ValueError(f"no release geometry for scale {scale} "
                         f"(available: {sorted(_MAT_N_TO_RELEASE_TAG)})")
    coords = np.load(_RELEASE_DIR / f"coords/coords_human_{tag}.npy")
    hemiid = np.load(_RELEASE_DIR / f"hemispheres/hemiid_human_{tag}.npy")
    cortical = np.load(_RELEASE_DIR / f"cortical/cortical_human_{tag}.npy")
    cidx = np.where(cortical != 0)[0]
    if len(cidx) != scale:
        raise ValueError(f"cortical node count {len(cidx)} != scale {scale}")
    return coords[cidx], hemiid[cidx], cidx


def load_published_consensus(scale: int) -> np.ndarray:
    """The Suárez published consensus restricted to the cortical nodes, symmetric
    and zero-diagonal. Used ONLY to validate the self-built consensus."""
    tag = _MAT_N_TO_RELEASE_TAG[scale]
    _, _, cidx = _load_release_geometry(scale)
    C = np.load(_RELEASE_DIR / f"connectivity/consensus/human_{tag}.npy")
    C = C[np.ix_(cidx, cidx)].astype(float).copy()
    np.fill_diagonal(C, 0.0)
    return C


# ---------------------------------------------------------------------------
# With-subcortical geometry for anatomical I/O routing (published consensus)
# ---------------------------------------------------------------------------

# The 7 cortical Yeo intrinsic networks, in rsn_names.npy order (subctx excluded).
# These are Suárez's readout apertures; subcortical (subctx) is the input aperture.
YEO_NETWORKS = ("VIS", "SM", "DA", "VA", "LIM", "FP", "DMN")


def load_published_consensus_full(scale: int = 448) -> np.ndarray:
    """The Suárez published *with-subcortical* consensus (NOT cortical-restricted).

    Unlike ``load_published_consensus`` (which slices to the cortical block for the
    self-build validation), this returns the full N=463 (@scale 448) / N=1015
    (@scale 1000) matrix -- the substrate for the anatomical I/O-routing thread,
    where input must be injected into the 15 subcortical nodes (absent from the
    cortical-only .mat, hence absent from our self-built consensus). Symmetric,
    non-negative, zero-diagonal.
    """
    tag = _MAT_N_TO_RELEASE_TAG[scale]
    C = np.load(
        _RELEASE_DIR / f"connectivity/consensus/human_{tag}.npy"
    ).astype(float).copy()
    np.fill_diagonal(C, 0.0)
    asym = float(np.max(np.abs(C - C.T)))
    assert asym < 1e-9, f"published consensus not symmetric, max|C-C.T|={asym:.3e}"
    assert C.min() >= 0.0, f"published consensus has negative weights, min={C.min():.3e}"
    return C


def load_routing_geometry(scale: int = 448) -> dict:
    """Node-set geometry for anatomical I/O routing on the with-subcortical graph.

    Every index is into the *full* published-consensus ordering (N=463 @scale 448 /
    N=1015 @scale 1000), matched to ``load_published_consensus_full``. Returns the
    15 subcortical input nodes, the cortical nodes, the per-Yeo-network cortical
    readout groups, and coords/hemiid. Subcortical nodes are interspersed (not a
    leading block), so groups are built from the cortical mask + RSN labels, never a
    raw slice.
    """
    tag = _MAT_N_TO_RELEASE_TAG[scale]
    coords = np.load(_RELEASE_DIR / f"coords/coords_human_{tag}.npy")
    hemiid = np.load(_RELEASE_DIR / f"hemispheres/hemiid_human_{tag}.npy")
    cortical = np.load(_RELEASE_DIR / f"cortical/cortical_human_{tag}.npy")
    rsn = np.load(_RELEASE_DIR / f"rsn_mapping/rsn_human_{tag}.npy", allow_pickle=True)
    rsn = np.asarray([str(x) for x in rsn])

    cortical_idx = np.where(cortical != 0)[0]
    subctx_idx = np.where(cortical == 0)[0]
    if len(cortical_idx) != scale:
        raise ValueError(f"cortical node count {len(cortical_idx)} != scale {scale}")

    yeo_groups = {name: np.where(rsn == name)[0] for name in YEO_NETWORKS}
    # The cortical nodes must partition exactly into the 7 Yeo networks, and the
    # subcortical nodes must all be labelled subctx (else the release ordering has
    # drifted from the consensus ordering -- a hard error, not a silent mislabel).
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


def load_published_full(scale: int = 448) -> ConnectomeData:
    """The published with-subcortical consensus as a ``ConnectomeData`` substrate.

    Thin wrapper over ``load_published_consensus_full`` so the with-subcortical
    graph plugs into ``HumanSubstrateBuilder(source="published_full")`` for the
    anatomical I/O-routing thread. The self-built consensus is cortical-only, so
    subcortical INPUT routing uses this validated (r≈0.99 vs self-build on the
    cortical block) published matrix -- a stated caveat of the routing thread.
    """
    C = load_published_consensus_full(scale)
    N = C.shape[0]
    n_edges = int((C != 0).sum() // 2)
    metadata = {
        "source": "Suárez et al. 2021 published distance-dependent consensus (Betzel 2018)",
        "processing": "published_with_subcortical",
        "scale": scale,
        "n_full": N,
        "n_edges": n_edges,
        "density": n_edges / (N * (N - 1) / 2),
        "processing_notes": (
            "Published with-subcortical group consensus (N=463 @scale 448 / "
            "N=1015 @scale 1000). Used as the routing substrate because subcortical "
            "input nodes are absent from the cortical-only .mat (and our self-built "
            "consensus). Symmetric, non-negative, zero-diagonal."
        ),
    }
    node_labels = [f"published_full_scale{scale}_region{i:04d}" for i in range(N)]
    return ConnectomeData(adjacency=C, node_labels=node_labels, metadata=metadata)


def build_consensus(scale: int = 448, weighted: bool = True) -> ConnectomeData:
    """Build our OWN distance-dependent group consensus from the .mat individual
    SC (the raw Lausanne source) + the release geometry, via the vendored
    Betzel-2018 ``struct_consensus``.

    This is the reservoir substrate for the human consensus probe -- self-derived
    end-to-end, NOT the published matrix (which is used only to validate this; see
    ``experiments/human/build_consensus.py``). ``weighted=True`` returns the
    mean-fibre-density-weighted consensus (heavy-tailed, non-negative).
    """
    stack = _load_sc_stack(scale)                        # (N, N, 70) cortical SC
    coords_c, hemiid_c, _ = _load_release_geometry(scale)
    distance = cdist(coords_c, coords_c)
    C = np.asarray(
        struct_consensus(stack, distance, hemiid_c.reshape(-1, 1), weighted=weighted),
        dtype=float,
    )
    np.fill_diagonal(C, 0.0)

    N = C.shape[0]
    asym = float(np.max(np.abs(C - C.T)))
    assert asym < 1e-9, f"consensus not symmetric, max|C-C.T|={asym:.3e}"
    assert C.min() >= 0.0, f"consensus has negative weights, min={C.min():.3e}"
    mask = C != 0
    n_edges = int(mask.sum() // 2)
    density = n_edges / (N * (N - 1) / 2)
    n_isolated = int((mask.sum(axis=1) == 0).sum())

    print(f"Built human consensus (self-derived): scale N={N}, "
          f"undirected edges={n_edges}, density={density:.3%}, "
          f"isolated nodes={n_isolated}")
    if n_isolated:
        print(f"  WARNING: {n_isolated} isolated node(s) -> dead reservoir unit(s).")

    metadata = {
        "source": "Suárez et al. 2021 individual Lausanne SC (Individual_Connectomes.mat)",
        "construction": "distance-dependent group consensus (Betzel et al. 2018)",
        "construction_notes": (
            f"Self-built from the {stack.shape[2]}-subject cortical individual SC "
            f"at scale N={N} via the vendored struct_consensus "
            f"(src/connectomes/consensus.py), weighted={weighted} (mean fibre "
            f"density over all subjects). Geometry (centroids -> Euclidean "
            f"distance, hemisphere labels) from the Suárez 2021 release, cortical "
            f"subset; node order verified against the .mat SC."
        ),
        "scale": scale,
        "weighted": weighted,
        "n_edges": n_edges,
        "density": density,
        "n_isolated_nodes": n_isolated,
    }
    node_labels = [f"scale{N}_region{i:04d}" for i in range(N)]
    return ConnectomeData(adjacency=C, node_labels=node_labels, metadata=metadata)


def load_built_consensus(scale: int = 448) -> ConnectomeData:
    """Load the cached self-built group consensus (see build_consensus.py).

    Fast path for the probe -- reads ``data/human/built_consensus/consensus_<scale>.npy``
    instead of reloading the 701 MB .mat. Raises with a build hint if absent.
    """
    import json

    path = _BUILT_DIR / f"consensus_{scale}.npy"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found; build it first with "
            f"`python -m experiments.human.build_consensus`."
        )
    C = np.load(path).astype(float)
    metadata = {"processing": "consensus_cached", "scale": scale, "cache_path": str(path)}
    meta_path = _BUILT_DIR / f"consensus_{scale}.meta.json"
    if meta_path.exists():
        metadata.update(json.loads(meta_path.read_text()).get("metadata", {}))
    N = C.shape[0]
    n_edges = int((C != 0).sum() // 2)
    print(f"Loaded self-built human consensus: scale N={N}, edges={n_edges}, "
          f"density={n_edges / (N * (N - 1) / 2):.3%}")
    node_labels = [f"scale{N}_region{i:04d}" for i in range(N)]
    return ConnectomeData(adjacency=C, node_labels=node_labels, metadata=metadata)

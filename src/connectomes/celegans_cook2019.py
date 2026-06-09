"""Cook et al. 2019 C. elegans connectome loader.

Source: Cook, S.J. et al. (2019), "Whole-animal connectomes of both
*Caenorhabditis elegans* sexes." Nature 571, 63–71.
DOI: 10.1038/s41586-019-1352-7. Downloaded from WormWiring SI 5
(corrected July 2020).
"""

from pathlib import Path

import numpy as np
import pandas as pd

from . import ConnectomeData


_REPO_ROOT = Path(__file__).resolve().parents[2]
_DATA_PATH = _REPO_ROOT / "data" / "cook2019_connectome.xlsx"


def load(processing: str = "binary_undirected_chemical") -> ConnectomeData:
    """Load Cook 2019 C. elegans hermaphrodite connectome.

    Parameters
    ----------
    processing
        "binary_undirected_chemical" — v2a default. Hermaphrodite
        chemical synapse sheet, binarised (A > 0) and symmetrised via
        (A + A.T > 0).
        "directed_weighted_chemical" — v2b. Hermaphrodite chemical
        sheet, NOT binarised and NOT symmetrised. Stored in reservoir
        convention (``adjacency[i, j]`` = weight from node ``j`` to
        node ``i``); the raw Cook 2019 layout (rows = presynaptic,
        columns = postsynaptic) is transposed at load time so all
        downstream code can use the matrix directly. Diagonal zeroed
        (autaptic self-synapses excluded for consistency with the
        v2a/v2c pipeline).

    Returns
    -------
    ConnectomeData
        Adjacency, node labels, and metadata describing source and
        processing.
    """
    if processing == "directed_weighted_chemical":
        return _load_directed_weighted_chemical()
    if processing != "binary_undirected_chemical":
        raise ValueError(f"Unknown processing: {processing!r}")

    df = pd.read_excel(
        _DATA_PATH,
        sheet_name="hermaphrodite chemical",
        header=2,
        index_col=2,
    )
    df = df.apply(pd.to_numeric, errors="coerce").fillna(0)

    common_labels = sorted(set(df.index.dropna()) & set(df.columns.dropna()))
    adjacency_weighted = df.loc[common_labels, common_labels].values.astype(float)

    adjacency_binary = (adjacency_weighted > 0).astype(float)
    adjacency_undirected = ((adjacency_binary + adjacency_binary.T) > 0).astype(float)

    # The hermaphrodite chemical sheet contains 38 self-synapses. v1 silently
    # kept them, producing inconsistent diagonal handling across its four
    # conditions (connectome + degree_rewire had self-loops; random_gaussian
    # + erdos_renyi did not). v2a's unified pipeline requires zero diagonal
    # everywhere; we drop the 38 self-loops here so the connectome enters the
    # pipeline on the same footing as the nulls. v1's reported "3019 edges"
    # double-counted via sum/2 with the diagonal still in place; the true
    # off-diagonal undirected edge count is 3000.
    self_loops_removed = int(np.diag(adjacency_undirected).sum())
    np.fill_diagonal(adjacency_undirected, 0)

    n_nodes = adjacency_undirected.shape[0]
    assert n_nodes == 300, f"Expected 300 nodes, got {n_nodes}"

    n_edges = int(adjacency_undirected.sum() // 2)
    density = n_edges / (n_nodes * (n_nodes - 1) / 2)
    print(
        f"Loaded C. elegans hermaphrodite chemical connectome: "
        f"N={n_nodes}, off-diagonal undirected edges={n_edges}, "
        f"density={density:.3%}, self-loops removed={self_loops_removed}"
    )

    metadata = {
        "source": "Cook et al. 2019, Nature 571:63-71 (DOI 10.1038/s41586-019-1352-7)",
        "sheet": "hermaphrodite chemical",
        "version": "WormWiring SI 5, corrected July 2020",
        "processing_notes": (
            "Hermaphrodite chemical synapse sheet only. Loaded with "
            "header=2, index_col=2; coerced to numeric (errors→NaN→0); "
            "restricted to labels common to rows and columns. Binarised "
            "by A > 0 and symmetrised via (A + A.T) > 0."
        ),
        "n_edges": n_edges,
        "density": density,
        "self_loops_removed": self_loops_removed,
    }

    return ConnectomeData(
        adjacency=adjacency_undirected,
        node_labels=list(common_labels),
        metadata=metadata,
    )


def _load_directed_weighted_chemical() -> ConnectomeData:
    """Load the Cook 2019 hermaphrodite chemical sheet as a directed weighted matrix.

    Returns the adjacency in **reservoir convention**: ``adjacency[i, j]``
    is the weight (integer synapse count) from node ``j`` (presynaptic)
    to node ``i`` (postsynaptic). Cook 2019 stores its matrix as
    ``[presynaptic, postsynaptic]`` (rows = "from", columns = "to"); we
    transpose at load time so all downstream operations (spectral-radius
    rescaling, ``build_from_adjacency``, eigendecomposition) use the
    matrix as-is without further reorientation.

    Diagonal is zeroed (autaptic self-synapses are a real biological
    feature in Cook 2019 but are excluded for consistency with the
    v2a/v2c pipeline; the count of removed self-loops is reported in
    the metadata).
    """
    df = pd.read_excel(
        _DATA_PATH,
        sheet_name="hermaphrodite chemical",
        header=2,
        index_col=2,
    )
    df = df.apply(pd.to_numeric, errors="coerce").fillna(0)

    common_labels = sorted(set(df.index.dropna()) & set(df.columns.dropna()))
    # Cook 2019 layout: rows = presynaptic (from), columns = postsynaptic (to).
    # Reservoir convention: adjacency[i, j] = weight from j to i. Transpose.
    adjacency_cook_layout = df.loc[common_labels, common_labels].values.astype(float)
    adjacency_reservoir_layout = adjacency_cook_layout.T.copy()

    self_loops_removed = int((np.diag(adjacency_reservoir_layout) > 0).sum())
    self_loop_synapses_removed = float(np.diag(adjacency_reservoir_layout).sum())
    np.fill_diagonal(adjacency_reservoir_layout, 0)

    n_nodes = adjacency_reservoir_layout.shape[0]
    assert n_nodes == 300, f"Expected 300 nodes, got {n_nodes}"
    assert adjacency_reservoir_layout.shape == (300, 300)

    nonzero_mask = adjacency_reservoir_layout != 0
    n_directed_edges = int(nonzero_mask.sum())
    density = n_directed_edges / (n_nodes * (n_nodes - 1))

    # Reciprocity: fraction of directed edges (i->j) whose reverse (j->i)
    # is also present. Computed on the binary directed mask.
    binary_directed = nonzero_mask.astype(float)
    reciprocated = float((binary_directed * binary_directed.T).sum())
    reciprocity = reciprocated / max(n_directed_edges, 1)

    print(
        f"Loaded C. elegans hermaphrodite chemical connectome "
        f"(directed weighted): N={n_nodes}, directed edges={n_directed_edges}, "
        f"density={density:.3%}, reciprocity={reciprocity:.3f}, "
        f"self-loops removed={self_loops_removed} "
        f"(synaptic count of removed self-loops={int(self_loop_synapses_removed)})"
    )

    metadata = {
        "source": "Cook et al. 2019, Nature 571:63-71 (DOI 10.1038/s41586-019-1352-7)",
        "sheet": "hermaphrodite chemical",
        "version": "WormWiring SI 5, corrected July 2020",
        "processing": "directed_weighted_chemical",
        "processing_notes": (
            "Hermaphrodite chemical synapse sheet only. Loaded with "
            "header=2, index_col=2; coerced to numeric (errors→NaN→0); "
            "restricted to labels common to rows and columns. NOT "
            "binarised and NOT symmetrised: integer synapse counts "
            "preserved as floats. Stored in reservoir convention "
            "(adjacency[i, j] = weight from j to i); Cook 2019's native "
            "layout (rows = presynaptic, columns = postsynaptic) is "
            "transposed at load time. Diagonal zeroed: autaptic "
            "self-synapses excluded for consistency with the v2a/v2c "
            "pipeline (known deviation from raw Cook 2019 data)."
        ),
        "orientation_convention": "reservoir (adjacency[i, j] = weight from j to i)",
        "n_directed_edges": n_directed_edges,
        "density": density,
        "reciprocity": reciprocity,
        "self_loops_removed": self_loops_removed,
        "self_loop_synapse_count_removed": int(self_loop_synapses_removed),
    }

    return ConnectomeData(
        adjacency=adjacency_reservoir_layout,
        node_labels=list(common_labels),
        metadata=metadata,
    )

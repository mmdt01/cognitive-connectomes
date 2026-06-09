"""Null-model validation helpers.

Used by every null generator to assert that the claimed property is
preserved within tolerance. Returns a structured result dict; prints a
clearly-formatted warning on failure but does not raise.
"""

import networkx as nx
import numpy as np


def validate_null(
    original: np.ndarray,
    generated: np.ndarray,
    preserved_property: str,
    tolerance: float | None = None,
    community_partition: list[set[int]] | None = None,
) -> dict:
    """Verify ``generated`` preserves ``preserved_property`` of ``original``.

    Parameters
    ----------
    original, generated
        Adjacency matrices to compare. Assumed binary symmetric here.
    preserved_property
        One of:
        - ``"edge_count"`` — sums match exactly.
        - ``"degree_sequence"`` — sorted row sums match exactly.
        - ``"in_degree_sequence"`` — sorted in-degree sequences match
          exactly. In reservoir convention (``adjacency[i, j]`` =
          weight from j to i), row sum of node ``i`` is its in-degree.
        - ``"out_degree_sequence"`` — sorted out-degree sequences match
          exactly. Column sum of node ``j`` is its out-degree.
        - ``"density"`` — relative difference within ``tolerance``
          (default 0.01).
        - ``"clustering"`` — relative difference in global clustering
          coefficient (``nx.transitivity``) within ``tolerance``
          (default 0.05).
        - ``"modularity"`` — absolute difference in modularity Q under
          ``community_partition`` within ``tolerance`` (default 0.01).
          Requires ``community_partition``.
        - ``"directed_clustering"`` — relative difference in mean Fagiolo
          (2007) directed clustering (``nx.average_clustering`` on the
          DiGraph) within ``tolerance`` (default 0.05).
        - ``"directed_block_matrix"`` — exact equality of the directed
          block edge-count matrix ``B[r, s]`` (number of directed edges
          from a node in block ``r`` to a node in block ``s``) under
          ``community_partition``. Requires ``community_partition``.
    tolerance
        Property-dependent — see above for defaults.
    community_partition
        Required for ``"modularity"`` and ``"directed_block_matrix"``;
        ignored otherwise.

    Returns
    -------
    dict
        ``{"property", "preserved", "expected", "actual", "details"}``.
    """
    if preserved_property == "edge_count":
        expected = int(original.sum())
        actual = int(generated.sum())
        preserved = expected == actual
        details = "sum(adjacency) — symmetric matrices counted with both entries"

    elif preserved_property == "degree_sequence":
        expected_seq = np.sort(original.sum(axis=1).astype(int))
        actual_seq = np.sort(generated.sum(axis=1).astype(int))
        preserved = bool(np.array_equal(expected_seq, actual_seq))
        expected = expected_seq
        actual = actual_seq
        details = "sorted row-sum degree sequences"

    elif preserved_property == "in_degree_sequence":
        # Reservoir convention: adjacency[i, j] = weight from j to i.
        # In-degree of node i is sum over j of A[i, j] (row sum).
        expected_seq = np.sort(
            (original != 0).sum(axis=1).astype(int)
        )
        actual_seq = np.sort(
            (generated != 0).sum(axis=1).astype(int)
        )
        preserved = bool(np.array_equal(expected_seq, actual_seq))
        expected = expected_seq
        actual = actual_seq
        details = "sorted in-degree sequences (row sums of binary mask)"

    elif preserved_property == "out_degree_sequence":
        # Out-degree of node j is sum over i of A[i, j] (column sum).
        expected_seq = np.sort(
            (original != 0).sum(axis=0).astype(int)
        )
        actual_seq = np.sort(
            (generated != 0).sum(axis=0).astype(int)
        )
        preserved = bool(np.array_equal(expected_seq, actual_seq))
        expected = expected_seq
        actual = actual_seq
        details = "sorted out-degree sequences (column sums of binary mask)"

    elif preserved_property == "density":
        tol = 0.01 if tolerance is None else tolerance
        n = original.shape[0]
        possible_undirected = n * (n - 1) / 2
        expected = float(original.sum() / 2) / possible_undirected
        actual = float(generated.sum() / 2) / possible_undirected
        rel_diff = abs(actual - expected) / max(expected, 1e-12)
        preserved = rel_diff <= tol
        details = f"relative difference {rel_diff:.4f} vs tolerance {tol}"

    elif preserved_property == "clustering":
        tol = 0.05 if tolerance is None else tolerance
        expected = float(nx.transitivity(nx.from_numpy_array(original)))
        actual = float(nx.transitivity(nx.from_numpy_array(generated)))
        rel_diff = abs(actual - expected) / max(expected, 1e-12)
        preserved = rel_diff <= tol
        details = (
            f"global clustering (transitivity): relative diff "
            f"{rel_diff:.4f} vs tolerance {tol}"
        )

    elif preserved_property == "modularity":
        if community_partition is None:
            raise ValueError(
                "preserved_property='modularity' requires community_partition."
            )
        tol = 0.01 if tolerance is None else tolerance
        expected = float(
            nx.community.modularity(
                nx.from_numpy_array(original), community_partition
            )
        )
        actual = float(
            nx.community.modularity(
                nx.from_numpy_array(generated), community_partition
            )
        )
        abs_diff = abs(actual - expected)
        preserved = abs_diff <= tol
        details = (
            f"modularity Q absolute diff {abs_diff:.4f} vs tolerance {tol} "
            f"(partition of {len(community_partition)} communities)"
        )

    elif preserved_property == "directed_clustering":
        tol = 0.05 if tolerance is None else tolerance
        graph_original = nx.from_numpy_array(
            (original != 0).astype(int), create_using=nx.DiGraph
        )
        graph_generated = nx.from_numpy_array(
            (generated != 0).astype(int), create_using=nx.DiGraph
        )
        expected = float(nx.average_clustering(graph_original))
        actual = float(nx.average_clustering(graph_generated))
        rel_diff = abs(actual - expected) / max(expected, 1e-12)
        preserved = rel_diff <= tol
        details = (
            f"mean Fagiolo directed clustering: relative diff "
            f"{rel_diff:.4f} vs tolerance {tol}"
        )

    elif preserved_property == "directed_block_matrix":
        if community_partition is None:
            raise ValueError(
                "preserved_property='directed_block_matrix' requires "
                "community_partition."
            )
        n_blocks = len(community_partition)
        node_to_block: dict[int, int] = {}
        for block_id, members in enumerate(community_partition):
            for node in members:
                node_to_block[int(node)] = block_id

        def _directed_block_matrix(matrix: np.ndarray) -> np.ndarray:
            block_matrix = np.zeros((n_blocks, n_blocks), dtype=int)
            # matrix[i, j] != 0 is a directed edge i -> j; B[block(i), block(j)].
            for i, j in np.argwhere(matrix != 0):
                block_matrix[node_to_block[int(i)], node_to_block[int(j)]] += 1
            return block_matrix

        expected = _directed_block_matrix(original)
        actual = _directed_block_matrix(generated)
        preserved = bool(np.array_equal(expected, actual))
        details = (
            f"directed block edge-count matrix ({n_blocks}x{n_blocks}) "
            f"exact preservation"
        )

    else:
        raise ValueError(f"Unknown preserved_property: {preserved_property!r}")

    result = {
        "property": preserved_property,
        "preserved": preserved,
        "expected": expected,
        "actual": actual,
        "details": details,
    }

    if not preserved:
        print(
            f"[validate_null] WARNING: {preserved_property!r} NOT preserved. "
            f"expected={expected!r}, actual={actual!r} ({details})"
        )

    return result

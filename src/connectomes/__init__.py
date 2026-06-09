"""Connectome loaders.

Interface contract
------------------

Every loader module exposes a ``load(**kwargs) -> ConnectomeData`` function.

.. code:: python

    @dataclass
    class ConnectomeData:
        adjacency: np.ndarray         # (N, N), weighted and directed by default
        node_labels: list[str]        # length N
        metadata: dict                # source, citation, version, processing notes
        node_positions: np.ndarray | None = None  # (N, 3) if spatially embedded
        node_types: list[str] | None = None       # cell types if known
        edge_types: np.ndarray | None = None      # for multi-relational connectomes

    def load(**kwargs) -> ConnectomeData:
        '''Returns the standardised connectome representation.

        Loaders preserve the connectome in its richest available form
        (directed, weighted). Binarisation and symmetrisation are
        downstream transformations applied in the notebook, not loader
        decisions. Document upstream processing choices (sheets,
        thresholds, sex, cell-type filters) in the docstring and in
        ``metadata['processing_notes']``.
        '''
"""

from dataclasses import dataclass, field
import numpy as np


@dataclass
class ConnectomeData:
    """Standardised connectome representation."""

    adjacency: np.ndarray
    node_labels: list[str]
    metadata: dict = field(default_factory=dict)
    node_positions: np.ndarray | None = None
    node_types: list[str] | None = None
    edge_types: np.ndarray | None = None

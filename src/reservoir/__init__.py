"""Reservoir construction helpers.

Layout
------

- ``blas`` — import-once side effect that caps BLAS threads.
- ``weights`` — applies a weight scheme to a binary topology mask.
- ``build`` — ``rescale_spectral_radius`` and ``build_from_adjacency``.

Construction contract
---------------------

.. code:: python

    def build_from_adjacency(
        weighted_adjacency: np.ndarray,
        target_spectral_radius: float,
        leak_rate: float,
        input_scaling: float,
        seed: int,
    ) -> Reservoir:
        '''Rescale the given (already-weighted) adjacency to the target
        spectral radius and instantiate a ReservoirPy Reservoir using it
        as the recurrent matrix W. The caller is responsible for
        applying the weight scheme before calling this — this function
        does not draw weights.
        '''
"""

"""Task evaluators.

Interface contract
------------------

Every task module exposes

.. code:: python

    def evaluate(reservoir, seed: int, **kwargs) -> dict:
        '''Returns a dict of performance metrics.

        Dict shape varies by task:
            MC returns {'mc': float, 'mc_per_lag': np.ndarray}
            classification returns {'accuracy': float, 'confusion_matrix': np.ndarray}
            IPC returns a degree-decomposed structure.

        Plotting code reads whatever shape it receives.
        '''
"""

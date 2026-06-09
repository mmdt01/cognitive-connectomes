"""Null-model generators.

Interface contract
------------------

Every generator module exposes a function

.. code:: python

    def generate(adjacency: np.ndarray, seed: int, **kwargs) -> np.ndarray:
        '''Returns a randomised adjacency matrix.

        Module-level docstring must specify exactly what is preserved and
        what is randomised. Caller is responsible for any binarisation /
        symmetrisation of the input; the null model itself doesn't make
        those choices.
        '''

Validation helper
-----------------

``validation.validate_null(original, generated, preserved_property,
tolerance=0.01) -> dict`` — verify the claimed property is preserved.
"""

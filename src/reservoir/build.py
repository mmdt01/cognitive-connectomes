"""Reservoir construction: spectral-radius rescaling and ReservoirPy build."""

import numpy as np
from reservoirpy.nodes import Reservoir


def rescale_spectral_radius(W: np.ndarray, target_spectral_radius: float) -> np.ndarray:
    """Rescale ``W`` so its spectral radius equals ``target_spectral_radius``.

    Uses dense ``np.linalg.eigvals``; fine at N=300, replace with
    ``scipy.sparse.linalg.eigs(W, k=1, which='LM')`` for larger N.
    """
    eigenvalues = np.linalg.eigvals(W)
    current_spectral_radius = float(np.max(np.abs(eigenvalues)))
    if current_spectral_radius < 1e-12:
        raise ValueError("Spectral radius ~0; cannot rescale.")
    return W * (target_spectral_radius / current_spectral_radius)


def build_from_adjacency(
    weighted_adjacency: np.ndarray,
    target_spectral_radius: float,
    leak_rate: float,
    input_scaling: float,
    seed: int,
) -> Reservoir:
    """Rescale a weighted adjacency to target spectral radius and build a Reservoir.

    The caller must already have applied a weight scheme. This function
    rescales, generates a per-seed Bernoulli ±1 input matrix scaled by
    ``input_scaling`` (preserving v1's input statistics), and hands W
    and Win to ReservoirPy's ``Reservoir`` constructor.
    """
    rescaled_W = rescale_spectral_radius(weighted_adjacency, target_spectral_radius)
    n_units = rescaled_W.shape[0]

    rng = np.random.default_rng(seed)
    Win = rng.choice([-1.0, 1.0], size=(n_units, 1)) * input_scaling

    return Reservoir(W=rescaled_W, Win=Win, lr=leak_rate, seed=seed)

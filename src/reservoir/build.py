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
    input_dim: int = 1,
    input_nodes: np.ndarray | None = None,
) -> Reservoir:
    """Rescale a weighted adjacency to target spectral radius and build a Reservoir.

    The caller must already have applied a weight scheme. This function
    rescales, generates a per-seed Bernoulli ±1 input matrix scaled by
    ``input_scaling`` (preserving v1's input statistics), and hands W
    and Win to ReservoirPy's ``Reservoir`` constructor.

    ``input_dim`` is the number of input channels (columns of ``Win``). It
    defaults to 1 -- the single-channel drive used by the driven tasks (NARMA,
    Mackey-Glass), so those build byte-identically. Multi-dimensional tasks
    (Lorenz: 3-D state fed back in closed loop) pass ``input_dim=3``; each
    channel gets its own independent Bernoulli ±1 column from the *same* per-seed
    RNG stream, so the single-channel case is unchanged.

    ``input_nodes`` routes the input to a **subset** of reservoir units (the
    anatomical I/O-routing thread: input injected into e.g. the subcortical
    nodes). ``None`` -> the default **dense** ``Win`` on all N units (every
    existing task builds byte-identically). When given, the full dense ``Win`` is
    still drawn from the same RNG stream and then **masked to zero off the input
    nodes**, so the surviving entries are identical to the dense case and
    ``input_nodes = all nodes`` reproduces the dense ``Win`` exactly.
    """
    rescaled_W = rescale_spectral_radius(weighted_adjacency, target_spectral_radius)
    n_units = rescaled_W.shape[0]

    rng = np.random.default_rng(seed)
    Win = rng.choice([-1.0, 1.0], size=(n_units, input_dim)) * input_scaling
    if input_nodes is not None:
        keep = np.zeros(n_units, dtype=bool)
        keep[input_nodes] = True
        Win[~keep] = 0.0

    return Reservoir(W=rescaled_W, Win=Win, lr=leak_rate, seed=seed)

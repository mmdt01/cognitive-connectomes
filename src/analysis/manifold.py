"""Manifold geometry of driven reservoir state matrices.

Connectome-agnostic, pure numpy/scipy: every function takes a driven state matrix
``states`` of shape ``(T, N)`` (warmup already discarded) and returns geometric
descriptors of the activity manifold the reservoir traces out over time. Sibling
to ``spectral.py`` -- which characterises the recurrent matrix ``W`` -- this tier
characterises the *activity* that ``W`` produces when driven.

Two axes (following the manifold-probe plan):

- **Spatial** (how many dimensions the activity occupies, how variance spreads):
  ``participation_ratio`` and ``spectral_entropy`` from the eigenvalues of the
  state covariance ``C = cov(X)``. PR counts effective dimensions; entropy weights
  the low-variance tail differently, so PR and entropy diverging is a signal that
  a heavy-tailed weight regime is reshaping the geometry.
- **Temporal** (how predictable motion along the manifold is):
  ``mean_curvature`` -- the mean turning angle between consecutive velocity
  vectors (the Henaff/Simoncelli straightening measure; lower = straighter = more
  linearly extrapolable). It disambiguates a manifold collapsed to a line (low PR,
  low curvature) from a genuinely straightened high-dimensional trajectory (high
  PR, low curvature).

Probe 2 (structural alignment) uses ``basis_alignment`` / ``random_basis_band``:
the fraction of state variance captured by the top-k vectors of a given orthonormal
basis (e.g. connectome-Laplacian harmonics or eigenvectors of ``W``), against a
random-orthonormal baseline band.

All covariance eigenvalues come from a symmetric solver (``eigvalsh``) with tiny
negative eigenvalues (numerical noise) clipped to zero.
"""

import numpy as np
from scipy.linalg import eigh, eigvalsh

# Relative tolerance for counting a covariance eigenvalue as a non-zero mode (used
# only to define the entropy normaliser's rank; excludes round-off "zeros").
_RANK_REL_TOL = 1e-12


# ---------------------------------------------------------------------------
# Covariance eigenvalues (shared by the spatial metrics)
# ---------------------------------------------------------------------------
def covariance_eigenvalues(states: np.ndarray) -> np.ndarray:
    """Eigenvalues of the time-centred state covariance, ascending and ``>= 0``.

    Centres ``states`` over time (subtract the per-column mean), forms
    ``C = (X.T @ X) / (T - 1)``, and returns its eigenvalues via ``eigvalsh``
    (``C`` is symmetric PSD) with tiny negatives clipped to zero.
    """
    states = np.asarray(states, dtype=float)
    if states.ndim != 2:
        raise ValueError(f"states must be 2-D (T, N); got shape {states.shape}")
    T = states.shape[0]
    if T < 2:
        raise ValueError(f"need at least 2 time steps to form a covariance; got T={T}")
    X = states - states.mean(axis=0, keepdims=True)
    C = (X.T @ X) / (T - 1)
    eig = eigvalsh(C)
    return np.clip(eig, 0.0, None)


def covariance_spectrum(states: np.ndarray) -> tuple[np.ndarray, float]:
    """Full time-centred covariance spectrum, **descending**, plus total variance.

    Returns ``(eig_desc, total_variance)`` where ``eig_desc`` are the eigenvalues
    of ``C = X^T X / (T - 1)`` (``X`` time-centred) in descending order and
    ``total_variance = sum(eig) == trace(C)``. Shares ``covariance_eigenvalues``
    (the exact spectrum Probes 1 and 2 use), so
    ``participation_ratio`` recomputed from ``eig_desc`` reproduces the Probe 1
    value to floating-point precision. The raw eigenvalues are the spatial
    fingerprint the participation ratio compresses to a scalar.
    """
    eig = covariance_eigenvalues(states)          # ascending, >= 0
    total_variance = float(eig.sum())
    return eig[::-1].copy(), total_variance


def gram_spectrum(design: np.ndarray) -> np.ndarray:
    """Eigenvalues of the readout design-matrix Gram ``A^T A``, **descending**.

    ``design`` is ``A`` exactly as the ridge solver forms it (any bias / input /
    scaling columns already appended by the caller), so the returned spectrum is
    the un-centred Gram the solve ``(A^T A + alpha I) w = A^T y`` inverts. Together
    with ``alpha`` it gives the ridge effective rank ``sum_i g_i / (g_i + alpha)``,
    the readout-relevant dimensionality. Length is ``A``'s column count (``N`` plus
    any extra design columns). ``A^T A`` is symmetric PSD, so ``eigvalsh`` is used
    and tiny negatives are clipped to zero.
    """
    design = np.asarray(design, dtype=float)
    gram = design.T @ design
    eig = np.clip(eigvalsh(gram), 0.0, None)
    return eig[::-1].copy()


def _pr_from_eigenvalues(eig: np.ndarray) -> float:
    s1 = float(eig.sum())
    s2 = float((eig ** 2).sum())
    return (s1 * s1 / s2) if s2 > 0.0 else 0.0


def _entropy_from_eigenvalues(eig: np.ndarray, normalise: bool) -> float:
    total = float(eig.sum())
    if total <= 0.0:
        return 0.0
    p = eig / total
    nz = p[p > 0.0]
    H = float(-(nz * np.log(nz)).sum())
    if normalise:
        rank = int((eig > eig.max() * _RANK_REL_TOL).sum())
        if rank > 1:
            H /= np.log(rank)
    return H


# ---------------------------------------------------------------------------
# Spatial metrics
# ---------------------------------------------------------------------------
def participation_ratio(states: np.ndarray, return_normalised: bool = False):
    """Spatial effective dimensionality ``PR = (sum lambda)^2 / sum(lambda^2)``.

    With ``return_normalised`` also returns ``PR / N`` (fraction of the ambient
    dimensions the activity occupies).
    """
    eig = covariance_eigenvalues(states)
    pr = _pr_from_eigenvalues(eig)
    if return_normalised:
        return pr, pr / states.shape[1]
    return pr


def spectral_entropy(states: np.ndarray, normalise: bool = True) -> float:
    """Spectral entropy of the covariance eigenvalue distribution.

    With ``p_i = lambda_i / sum lambda``, ``H = -sum p_i log p_i`` (``0 log 0 = 0``).
    If ``normalise``, divide by ``log(rank)`` (rank = number of non-zero modes) so
    ``H`` lands in ``[0, 1]``. Same spatial axis as PR but weights the low-variance
    tail more heavily.
    """
    return _entropy_from_eigenvalues(covariance_eigenvalues(states), normalise)


def mean_curvature(states: np.ndarray, min_speed: float = 1e-8) -> float:
    """Mean trajectory curvature (turning angle between successive velocities).

    Velocities ``v_t = x_{t+1} - x_t``; turning angle
    ``c_t = arccos( clip( (v_t . v_{t+1}) / (||v_t|| ||v_{t+1}||), -1, 1 ) )``.
    Steps where either speed ``< min_speed`` are skipped (an undefined direction).
    Returns the mean over ``t`` in **radians** (``nan`` if no step qualifies).
    Lower = straighter = more linearly predictable.
    """
    states = np.asarray(states, dtype=float)
    v = np.diff(states, axis=0)
    speed = np.linalg.norm(v, axis=1)
    if v.shape[0] < 2:
        return float("nan")
    v1, v2 = v[:-1], v[1:]
    s1, s2 = speed[:-1], speed[1:]
    valid = (s1 >= min_speed) & (s2 >= min_speed)
    if not valid.any():
        return float("nan")
    dots = np.sum(v1[valid] * v2[valid], axis=1)
    cos = np.clip(dots / (s1[valid] * s2[valid]), -1.0, 1.0)
    return float(np.mean(np.arccos(cos)))


def manifold_metrics(states: np.ndarray) -> dict:
    """Convenience wrapper: PR, PR/N, spectral entropy and mean curvature in one
    pass (a single covariance eigendecomposition shared by the spatial metrics).
    """
    eig = covariance_eigenvalues(states)
    pr = _pr_from_eigenvalues(eig)
    return {
        "pr": pr,
        "pr_norm": pr / states.shape[1],
        "spectral_entropy": _entropy_from_eigenvalues(eig, normalise=True),
        "mean_curvature": mean_curvature(states),
    }


# ---------------------------------------------------------------------------
# Probe 2: alignment of the activity manifold with a structural basis
# ---------------------------------------------------------------------------
def _covariance(states: np.ndarray) -> tuple[np.ndarray, float]:
    """Time-centred covariance ``C`` and its trace (total variance)."""
    states = np.asarray(states, dtype=float)
    T = states.shape[0]
    X = states - states.mean(axis=0, keepdims=True)
    C = (X.T @ X) / (T - 1)
    return C, float(np.trace(C))


def _captured_curve(C: np.ndarray, basis: np.ndarray, k_grid, total: float) -> np.ndarray:
    """Fraction of variance captured by the top-k columns of an orthonormal basis.

    For orthonormal columns ``u_j``, ``trace(U_k.T C U_k) = sum_{j<k} u_j.T C u_j``,
    so the per-vector captured variances ``q_j = u_j.T C u_j`` cumulatively sum to
    ``captured(k)``. ``basis`` columns are assumed ordered as intended (e.g.
    ascending Laplacian frequency, or descending |eigenvalue| of ``W``).
    """
    q = np.einsum("ij,ij->j", basis, C @ basis)  # u_j . (C u_j) per column
    cum = np.cumsum(q)
    n = cum.size
    if total <= 0.0:
        return np.zeros(len(k_grid))
    return np.array([float(cum[min(int(k), n) - 1] / total) for k in k_grid])


def basis_alignment(states: np.ndarray, basis: np.ndarray, k_grid) -> dict:
    """Cumulative state variance captured by the top-k vectors of ``basis``.

    ``basis`` is ``(N, N)`` orthonormal, columns ordered as intended. Returns
    ``{"k": [...], "captured": [...]}`` -- the fraction of total state variance in
    the first ``k`` basis directions, for each ``k`` in ``k_grid``. Compare against
    ``random_basis_band`` for a chance baseline.
    """
    C, total = _covariance(states)
    if basis.shape != C.shape:
        raise ValueError(f"basis shape {basis.shape} != covariance shape {C.shape}")
    return {
        "k": list(k_grid),
        "captured": _captured_curve(C, basis, k_grid, total),
    }


def random_basis_band(states: np.ndarray, k_grid, n_random: int = 20,
                      seed: int = 0) -> dict:
    """Chance-baseline captured-variance band over random orthonormal bases.

    Averages ``captured(k)`` over ``n_random`` random orthonormal bases (QR of a
    Gaussian matrix). Returns ``{"k", "mean", "std"}`` -- the mean curve and its
    across-basis standard-deviation spread band.
    """
    C, total = _covariance(states)
    N = C.shape[0]
    rng = np.random.default_rng(seed)
    curves = np.empty((n_random, len(k_grid)))
    for r in range(n_random):
        Q, _ = np.linalg.qr(rng.standard_normal((N, N)))
        curves[r] = _captured_curve(C, Q, k_grid, total)
    return {
        "k": list(k_grid),
        "mean": curves.mean(axis=0),
        "std": curves.std(axis=0),
    }


def graph_laplacian_harmonics(adjacency: np.ndarray) -> np.ndarray:
    """Orthonormal connectome harmonics: eigenvectors of the unnormalised graph
    Laplacian ``L = D - A``, ordered by **ascending** eigenvalue (low spatial
    frequency first).

    ``A = |adjacency|`` with a zeroed diagonal, so ``L`` is a valid non-negative
    graph Laplacian even for a signed weight scheme; for a non-negative substrate
    ``|adjacency| == adjacency``, so this is the ordinary weighted Laplacian. Pass
    the weighted symmetric connectivity that defines the reservoir (record the
    choice); a binary-mask variant is obtained by passing the mask.
    """
    A = np.abs(np.asarray(adjacency, dtype=float))
    np.fill_diagonal(A, 0.0)
    if not np.allclose(A, A.T, atol=1e-9):
        raise ValueError("adjacency must be symmetric for a Hermitian Laplacian")
    L = np.diag(A.sum(axis=1)) - A
    _, U = eigh(L)  # ascending eigenvalue == ascending spatial frequency
    return U


def symmetric_eigenbasis(W: np.ndarray, order: str = "abs_desc") -> np.ndarray:
    """Orthonormal eigenvectors of a symmetric matrix.

    ``order='abs_desc'`` (default) orders columns by **descending |eigenvalue|**
    (dominant dynamical modes first) -- the natural ``W``-mode basis for the
    alignment probe; ``'asc'`` keeps ``eigh``'s ascending-eigenvalue order.
    """
    W = np.asarray(W, dtype=float)
    if not np.allclose(W, W.T, atol=1e-9):
        raise ValueError("W must be symmetric to use eigh for an orthonormal basis")
    eigenvalues, U = eigh(W)
    if order == "abs_desc":
        U = U[:, np.argsort(np.abs(eigenvalues))[::-1]]
    elif order != "asc":
        raise ValueError(f"unknown order {order!r}")
    return U


def default_k_grid(n: int) -> list:
    """A log-spaced-ish ``k`` grid capped at ``n`` (for the alignment sweep)."""
    candidates = [1, 2, 3, 5, 10, 20, 30, 50, 100, 150, 200, 300, 400, 500,
                  750, 1000]
    grid = [k for k in candidates if k < n]
    if not grid or grid[-1] != n:
        grid.append(n)
    return grid


# ---------------------------------------------------------------------------
# Self-test (unit-scale sanity check): python -m src.analysis.manifold
# ---------------------------------------------------------------------------
def _selftest() -> None:
    rng = np.random.default_rng(0)
    T, N = 2000, 40

    # Rank-1 activity -> PR ~ 1, entropy ~ 0.
    line = np.outer(rng.standard_normal(T), rng.standard_normal(N))
    pr1 = participation_ratio(line)
    assert pr1 < 1.5, f"rank-1 PR should be ~1, got {pr1:.3f}"
    assert spectral_entropy(line) < 0.05, "rank-1 entropy should be ~0"

    # Isotropic activity -> PR ~ N, normalised entropy ~ 1.
    iso = rng.standard_normal((T, N))
    pr_iso, pr_norm = participation_ratio(iso, return_normalised=True)
    assert pr_iso > 0.7 * N, f"isotropic PR should approach N={N}, got {pr_iso:.1f}"
    assert spectral_entropy(iso) > 0.9, "isotropic normalised entropy should be ~1"
    assert abs(pr_norm - pr_iso / N) < 1e-9

    # Straight-line motion -> curvature ~ 0; random walk -> curvature ~ pi/2.
    straight = np.cumsum(np.ones((T, N)) * rng.standard_normal(N), axis=0)
    assert mean_curvature(straight) < 1e-3, "straight motion should have ~0 curvature"
    walk_curv = mean_curvature(np.cumsum(rng.standard_normal((T, N)), axis=0))
    assert 1.3 < walk_curv < 1.8, f"random-walk curvature should be ~pi/2, got {walk_curv:.3f}"

    # covariance_spectrum: descending, reproduces PR, trace == sum of variances.
    eig_desc, total_var = covariance_spectrum(iso)
    assert (np.diff(eig_desc) <= 1e-9).all(), "covariance_spectrum must be descending"
    assert abs(_pr_from_eigenvalues(eig_desc) - pr_iso) < 1e-6, \
        "PR from covariance_spectrum must match participation_ratio"
    assert abs(total_var - np.var(iso, axis=0, ddof=1).sum()) < 1e-6, \
        "total_variance must equal trace(C) (sum of per-column variances)"

    # gram_spectrum: descending, length = design columns; a bias column adds one
    # eigenvalue (the near-constant column's mass), and A^T A is PSD.
    g = gram_spectrum(iso)
    assert g.size == N and (np.diff(g) <= 1e-6).all() and (g >= -1e-9).all()
    g_bias = gram_spectrum(np.hstack([iso, np.ones((T, 1))]))
    assert g_bias.size == N + 1, "bias column must add one design dimension"

    # basis_alignment: the exact covariance eigenbasis captures 100% by k=N, and
    # its top-k dominates a random basis; random band matches k/N on isotropic data.
    C, total = _covariance(iso)
    eigvecs = np.linalg.eigh(C)[1][:, ::-1]  # descending-eigenvalue order
    k_grid = default_k_grid(N)
    cap = basis_alignment(iso, eigvecs, k_grid)["captured"]
    assert abs(cap[-1] - 1.0) < 1e-9, "full eigenbasis must capture all variance"
    band = random_basis_band(iso, k_grid, n_random=8, seed=1)
    assert (cap >= band["mean"] - 1e-9).all(), "eigenbasis should dominate random"
    kmid = k_grid.index(20)
    assert abs(band["mean"][kmid] - 20 / N) < 0.1, "random band ~ k/N on isotropic data"

    # Structural bases: harmonics orthonormal + lowest mode ~constant (Laplacian
    # nullspace of a connected graph); W-mode basis orthonormal + abs-desc ordered.
    A = np.abs(rng.standard_normal((N, N))); A = A + A.T; np.fill_diagonal(A, 0.0)
    U_L = graph_laplacian_harmonics(A)
    assert np.allclose(U_L.T @ U_L, np.eye(N), atol=1e-8), "harmonics not orthonormal"
    assert np.std(np.abs(U_L[:, 0])) < 1e-6, "lowest harmonic should be ~constant"
    Wsym = A - np.diag(A.sum(1))  # a symmetric matrix with spread eigenvalues
    U_W = symmetric_eigenbasis(Wsym, order="abs_desc")
    assert np.allclose(U_W.T @ U_W, np.eye(N), atol=1e-8), "W-basis not orthonormal"
    evals = np.linalg.eigvalsh(Wsym)
    assert abs(abs(U_W[:, 0] @ Wsym @ U_W[:, 0]) - np.abs(evals).max()) < 1e-6, \
        "first W-mode should carry the largest |eigenvalue|"

    print("manifold self-test passed:")
    print(f"  rank-1 PR={pr1:.3f}  isotropic PR={pr_iso:.1f} (/N={pr_norm:.3f})")
    print(f"  straight curvature~0  random-walk curvature={walk_curv:.3f} rad (~pi/2)")
    print(f"  eigenbasis captured(k=N)={cap[-1]:.6f}  random(k=20)~{band['mean'][kmid]:.3f}")


if __name__ == "__main__":
    _selftest()

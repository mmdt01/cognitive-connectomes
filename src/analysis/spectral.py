"""Spectral analysis of weighted recurrent matrices.

Connectome-agnostic: every function takes a plain weighted adjacency matrix ``W``
(the reservoir's recurrent matrix *before* spectral rescaling), so the same tools
characterise any connectome or null. Because the reservoir rescales ``W`` to a
matched nominal spectral radius (``|lambda_1|``), the informative quantities are
**scale-invariant ratios of the bulk to the dominant eigenvalue** -- they describe
how compressed the effective dynamics are at a matched operating point.

Metrics (``spectral_metrics``):

================== ====================================================================
``spectral_radius`` ``|lambda_1|`` -- dominant eigenvalue magnitude (raw scale).
``lambda2_ratio``   ``|lambda_2| / |lambda_1|`` -- Perron gap (low => 2nd mode far below top).
``bulk95_ratio``    ``pct95(|lambda|) / |lambda_1|`` -- bulk radius vs top.
``mean_ratio``      ``mean(|lambda|) / |lambda_1|`` -- overall compression.
``participation_ratio`` ``(sum|lambda|)^2 / sum|lambda|^2`` -- effective # of modes.
``n_critical``      ``# {|lambda| > 0.9 |lambda_1|}`` -- near-dominant modes.
================== ====================================================================

Lower ``bulk95_ratio`` / ``mean_ratio`` => more compressed bulk => milder effective
dynamics at a matched nominal spectral radius.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def spectral_metrics(W: np.ndarray) -> dict:
    """Scale-invariant spectral-compression metrics for a weighted matrix."""
    magnitudes = np.sort(np.abs(np.linalg.eigvals(W)))[::-1]  # descending |lambda|
    l1 = float(magnitudes[0])
    if l1 < 1e-12:
        return dict(spectral_radius=0.0, lambda2_ratio=0.0, bulk95_ratio=0.0,
                    mean_ratio=0.0, participation_ratio=0.0, n_critical=0)
    return dict(
        spectral_radius=l1,
        lambda2_ratio=float(magnitudes[1] / l1) if magnitudes.size > 1 else 0.0,
        bulk95_ratio=float(np.percentile(magnitudes, 95) / l1),
        mean_ratio=float(magnitudes.mean() / l1),
        participation_ratio=float(magnitudes.sum() ** 2 / (magnitudes ** 2).sum()),
        n_critical=int((magnitudes > 0.9 * l1).sum()),
    )


def recurrent_spectrum(W: np.ndarray, n_leading_ipr: int = 10,
                       near_degenerate_fracs: tuple = (0.10, 0.25),
                       symmetry_atol: float = 1e-9) -> dict:
    """Full eigen-spectrum of the **normalised** base matrix (spectral radius 1).

    ``W`` is a weighted recurrent matrix *before* spectral rescaling. The reservoir
    build rescales it to ``W(sr) = W * sr / |lambda_1|`` (dense ``np.linalg.eigvals``
    for ``|lambda_1|``), so this reports the spectrum of the normalised base
    ``W / |lambda_1|`` -- ``W(sr)``'s eigenvalues are exactly ``sr`` times these.

    Returns (all scalars on the normalised spectrum, where ``|lambda_1| == 1``):

    - ``eig_real`` / ``eig_imag`` -- eigenvalues, sorted by **descending modulus**
      (float32). For a symmetric ``W`` the eigenvalues are real (``eigh``); the
      general path (``eig``) keeps complex conjugate pairs.
    - ``is_symmetric`` -- ``W`` symmetric within ``symmetry_atol``.
    - ``perron_root`` -- largest real-part eigenvalue (the Perron-Frobenius root for
      a non-negative ``W``; ``== 1`` there, since the Perron mode sets the radius).
    - ``bulk95_radius`` -- ``pct95(|lambda|)`` (identical formula to
      ``spectral_metrics``' ``bulk95_ratio``, here with ``|lambda_1| == 1``).
    - ``spectral_gap`` -- ``|lambda_1| - |lambda_2|`` (normalised: ``1 - |lambda_2|``).
    - ``n_near_degenerate_10pct`` / ``_25pct`` -- count of ``|lambda_i|`` within 10%
      / 25% of ``|lambda_1|`` (``|lambda_i| >= 0.9`` / ``0.75``; includes the top).
    - ``top10_eigvec_ipr`` -- inverse participation ratio
      ``sum_i |v_i|^4 / (sum_i |v_i|^2)^2`` of the leading ``n_leading_ipr``
      eigenvectors (modulus for complex): high = localised on few nodes.
    - ``base_spectral_radius`` -- ``|lambda_1|`` of the un-normalised ``W`` (the
      raw scale divided out).

    Tests whether non-negative modular networks carry several near-degenerate
    leading modes (one per weakly coupled pool), each localised (high IPR) and
    supporting a slow mode -- the hypothesised basis of memory.
    """
    W = np.asarray(W, dtype=float)
    is_symmetric = bool(np.allclose(W, W.T, atol=symmetry_atol))
    if is_symmetric:
        # eigh gives real eigenvalues and an orthonormal (real) eigenbasis.
        eigenvalues, eigenvectors = np.linalg.eigh(W)
        eigenvalues = eigenvalues.astype(complex)
    else:
        # Non-normal (e.g. directed) W: right eigenvectors, generally complex.
        eigenvalues, eigenvectors = np.linalg.eig(W)

    magnitudes = np.abs(eigenvalues)
    l1 = float(magnitudes.max())
    if l1 < 1e-12:
        raise ValueError("spectral radius ~0; cannot normalise the base matrix.")

    order = np.argsort(magnitudes)[::-1]          # descending modulus
    eigenvalues = eigenvalues[order] / l1
    eigenvectors = eigenvectors[:, order]
    mods = magnitudes[order] / l1                 # |lambda| / |lambda_1|, desc

    iprs = []
    for j in range(min(n_leading_ipr, eigenvectors.shape[1])):
        v = np.abs(eigenvectors[:, j])
        s2 = float((v ** 2).sum())
        iprs.append(float((v ** 4).sum() / (s2 ** 2)) if s2 > 0.0 else 0.0)

    return dict(
        eig_real=eigenvalues.real.astype(np.float32),
        eig_imag=eigenvalues.imag.astype(np.float32),
        is_symmetric=is_symmetric,
        perron_root=float(eigenvalues.real.max()),
        bulk95_radius=float(np.percentile(mods, 95)),
        spectral_gap=float(mods[0] - (mods[1] if mods.size > 1 else 0.0)),
        n_near_degenerate_10pct=int((mods >= 1.0 - near_degenerate_fracs[0]).sum()),
        n_near_degenerate_25pct=int((mods >= 1.0 - near_degenerate_fracs[1]).sum()),
        top10_eigvec_ipr=np.asarray(iprs, dtype=np.float32),
        base_spectral_radius=l1,
    )


def normalized_eigenvalues(W: np.ndarray) -> np.ndarray:
    """Complex eigenvalues divided by ``|lambda_1|`` (dominant mode -> unit circle)."""
    eigenvalues = np.linalg.eigvals(W)
    l1 = np.abs(eigenvalues).max()
    return eigenvalues / l1 if l1 > 1e-12 else eigenvalues


def magnitude_decay(W: np.ndarray) -> np.ndarray:
    """Sorted ``|lambda| / |lambda_1|``, descending (compression as a curve)."""
    magnitudes = np.sort(np.abs(np.linalg.eigvals(W)))[::-1]
    return magnitudes / magnitudes[0] if magnitudes[0] > 1e-12 else magnitudes


# ---------------------------------------------------------------------------
# Plots (generic over keys; the driver supplies titles + colours)
# ---------------------------------------------------------------------------
def plot_eigenvalue_grid(spectra, row_keys, col_keys, row_titles, col_titles,
                         col_colors, path, suptitle=""):
    """Grid of normalized eigenvalue scatters; ``spectra[(row, col)]`` -> complex array."""
    nrows, ncols = len(row_keys), len(col_keys)
    fig, axes = plt.subplots(nrows, ncols, figsize=(2.7 * ncols, 2.7 * nrows),
                             squeeze=False)
    theta = np.linspace(0, 2 * np.pi, 256)
    for i, rkey in enumerate(row_keys):
        for j, ckey in enumerate(col_keys):
            ax = axes[i][j]
            eig = spectra[(rkey, ckey)]
            ax.plot(np.cos(theta), np.sin(theta), color="0.7", lw=0.7, ls="--", zorder=1)
            ax.axhline(0, color="0.85", lw=0.5, zorder=0)
            ax.axvline(0, color="0.85", lw=0.5, zorder=0)
            ax.scatter(eig.real, eig.imag, s=9, color=col_colors[ckey],
                       alpha=0.55, edgecolor="none", zorder=2)
            ax.set_aspect("equal")
            ax.set_xlim(-1.18, 1.18)
            ax.set_ylim(-1.18, 1.18)
            ax.set_xticks([])
            ax.set_yticks([])
            if i == 0:
                ax.set_title(col_titles[ckey], fontsize=10)
            if j == 0:
                ax.set_ylabel(row_titles[rkey], fontsize=9)
    fig.suptitle(suptitle, fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_metric_bars(metrics, metric_keys, metric_titles, condition_keys,
                     condition_titles, variant_keys, variant_titles,
                     variant_colors, path, suptitle=""):
    """Bars: rows = metrics, cols = conditions, bars = variants.
    ``metrics[(condition, variant)][metric_key]`` -> float (seed-averaged)."""
    nrows, ncols = len(metric_keys), len(condition_keys)
    fig, axes = plt.subplots(nrows, ncols, figsize=(3.4 * ncols, 3.0 * nrows),
                             squeeze=False, sharey="row")
    x = np.arange(len(variant_keys))
    for i, mkey in enumerate(metric_keys):
        for j, ckey in enumerate(condition_keys):
            ax = axes[i][j]
            ax.bar(x, [metrics[(ckey, v)][mkey] for v in variant_keys],
                   color=[variant_colors[v] for v in variant_keys])
            ax.set_xticks(x)
            ax.set_xticklabels([variant_titles[v] for v in variant_keys],
                               rotation=45, ha="right", fontsize=7)
            ax.grid(axis="y", alpha=0.25)
            if i == 0:
                ax.set_title(condition_titles[ckey], fontsize=10)
            if j == 0:
                ax.set_ylabel(metric_titles[i], fontsize=9)
    fig.suptitle(suptitle, fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_magnitude_decay(decays, condition_keys, condition_titles, variant_keys,
                         variant_titles, variant_colors, path, suptitle=""):
    """One panel per condition of sorted ``|lambda|/|lambda_1|`` decay curves.
    ``decays[(condition, variant)]`` -> 1D array."""
    fig, axes = plt.subplots(1, len(condition_keys),
                             figsize=(4.2 * len(condition_keys), 3.4),
                             squeeze=False, sharey=True)
    axes = axes[0]
    for ax, ckey in zip(axes, condition_keys):
        for v in variant_keys:
            curve = decays[(ckey, v)]
            ax.plot(np.arange(1, curve.size + 1), curve, color=variant_colors[v],
                    lw=1.4, label=variant_titles[v])
        ax.set_yscale("log")
        ax.set_xlabel("eigenvalue index (by |λ|, desc.)")
        ax.set_title(condition_titles[ckey], fontsize=10)
        ax.grid(alpha=0.25, which="both")
    axes[0].set_ylabel("|λ| / |λ₁|")
    axes[-1].legend(fontsize=7, framealpha=0.9, loc="lower left")
    fig.suptitle(suptitle, fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)

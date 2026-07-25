"""Graded sign-composition transform for a non-negative recurrent matrix.

Connectome-agnostic, pure numpy. Takes an all-positive symmetric weighted matrix
``W_base`` (the ``human_empirical`` substrate: real magnitudes on some topology) and
flips the sign of a controlled fraction ``f`` of its edges, returning a symmetric
``W`` whose negative-weight fraction is exactly ``f`` (up to within-stratum
rounding). This turns the binary "sign" switch of the sign-primary account
(all-positive vs balanced) into a graded, continuous axis.

**Symmetry is preserved.** Each undirected edge is one upper-triangle entry; a flip
negates that entry and mirrors it, so ``W`` stays symmetric (normal) -- the property
the human undirected substrate relies on for a clean real eigenbasis. ``f = 0`` is
the identity (recovers the non-negative substrate); ``f = 0.5`` is balanced sign.
Magnitudes ``|W|`` and the nonzero topology are left untouched; only signs change.

**Placement matters, so it is controlled.** The leading (Perron) eigenvalue of a
non-negative graph is dominated by high-degree / rich-club nodes, so *where* the
negative weights land -- not only how many -- moves the spectrum. Each edge gets an
importance score = product of its endpoints' node scores (endpoint **degree** by
default; **eigenvector centrality** for a robustness check), computed on the FIXED
base topology, so "hub edges" are a stable set for a given base:

- ``stratified`` (primary, placement-neutral): flip a fraction ``f`` of edges
  WITHIN each score decile, holding the hub-to-periphery composition of the flipped
  set constant across the whole ``f`` sweep -- ``f`` means "how much sign, holding
  where fixed".
- ``hub_first`` / ``periphery_first`` (the placement axis): flip the highest- /
  lowest-scored edges first, so hub (resp. peripheral) weights turn negative
  soonest as ``f`` rises.

The transform is applied to the base matrix BEFORE spectral-radius rescaling and
the flip pattern is held fixed across the sr sweep (the caller rescales), so ``f``
and sr are orthogonal axes of the phase diagram.
"""

import numpy as np

TARGETING_MODES = ("stratified", "hub_first", "periphery_first")
SCORE_MODES = ("degree", "eigenvector")


# ---------------------------------------------------------------------------
# Importance scores on the fixed base topology
# ---------------------------------------------------------------------------
def node_importance(W: np.ndarray, mode: str = "degree") -> np.ndarray:
    """Per-node importance score on the base topology of ``W``.

    ``degree`` -- binary degree (number of incident edges), the legible primary
    score. ``eigenvector`` -- the leading eigenvector of ``|W|`` (the Perron mode
    of the non-negative substrate; the continuous quantity closest to what moves
    the leading eigenvalue), returned as ``|v_1|``. For the undirected human ``W``
    the two correlate strongly; degree is the default, eigenvector the robustness
    check.
    """
    A = np.abs(np.asarray(W, dtype=float))
    np.fill_diagonal(A, 0.0)
    if mode == "degree":
        return (A > 0.0).sum(axis=1).astype(float)
    if mode == "eigenvector":
        # |W| symmetric non-negative -> real spectrum; leading (Perron) eigenvector.
        eigenvalues, eigenvectors = np.linalg.eigh(A)
        return np.abs(eigenvectors[:, int(np.argmax(eigenvalues))])
    raise ValueError(f"unknown score mode {mode!r}; expected one of {SCORE_MODES}")


def edge_importance(W: np.ndarray, node_score: np.ndarray):
    """Upper-triangle edge list and their endpoint-product importance scores.

    Returns ``(rows, cols, escore)`` for the present (nonzero) upper-triangle edges
    ``i < j`` of ``W``, with ``escore = node_score[i] * node_score[j]`` -- the
    product form, which most sharply selects hub-to-hub (rich-club) edges (the ones
    that dominate the Perron eigenvalue).
    """
    W = np.asarray(W, dtype=float)
    rows, cols = np.triu_indices(W.shape[0], k=1)
    present = W[rows, cols] != 0.0
    rows, cols = rows[present], cols[present]
    node_score = np.asarray(node_score, dtype=float)
    return rows, cols, node_score[rows] * node_score[cols]


# ---------------------------------------------------------------------------
# Which edges flip (the placement policy)
# ---------------------------------------------------------------------------
def _select_flips(escore: np.ndarray, f: float, targeting: str,
                  rng: np.random.Generator, n_strata: int) -> np.ndarray:
    """Boolean mask over edges: which flip, at fraction ``f`` under ``targeting``.

    ``hub_first`` / ``periphery_first`` flip the ``round(f * n_edges)`` highest- /
    lowest-scored edges (random tiebreak among equal scores). ``stratified`` flips
    ``round(f * stratum_size)`` edges chosen uniformly within each of ``n_strata``
    equal-count score bins, holding hub-to-periphery composition constant across f.
    """
    n = escore.size
    flip = np.zeros(n, dtype=bool)
    if n == 0 or f <= 0.0:
        return flip

    if targeting in ("hub_first", "periphery_first"):
        k = int(round(f * n))
        if k <= 0:
            return flip
        tiebreak = rng.random(n)                       # decorrelate equal scores
        signed = -escore if targeting == "hub_first" else escore
        order = np.lexsort((tiebreak, signed))         # primary: signed ascending
        flip[order[:k]] = True
        return flip

    if targeting == "stratified":
        # Rank edges by score, split into n_strata equal-count bins, flip a
        # fraction f within each so the flipped set mirrors the score distribution.
        ranks = np.argsort(np.argsort(escore))
        stratum = np.minimum((ranks * n_strata) // n, n_strata - 1)
        for s in range(n_strata):
            idx = np.flatnonzero(stratum == s)
            k = int(round(f * idx.size))
            if k > 0:
                flip[rng.choice(idx, size=k, replace=False)] = True
        return flip

    raise ValueError(f"unknown targeting {targeting!r}; expected one of {TARGETING_MODES}")


# ---------------------------------------------------------------------------
# The transform
# ---------------------------------------------------------------------------
def sign_fraction_matrix(W: np.ndarray, f: float, targeting: str,
                         rng: np.random.Generator, n_strata: int = 10,
                         score_mode: str = "degree",
                         node_score: np.ndarray | None = None) -> np.ndarray:
    """Flip the sign of a fraction ``f`` of ``W``'s edges, preserving symmetry.

    ``W`` must be a symmetric, non-negative (all-positive off-diagonal) weighted
    matrix. Returns a new symmetric matrix identical to ``W`` except that a fraction
    ``f`` of undirected edges (selected by ``targeting`` on the endpoint-product
    importance score) have their sign flipped. ``f = 0`` returns a copy unchanged.
    Pass a precomputed ``node_score`` to reuse the score across an ``f`` sweep
    (it depends only on the base topology); otherwise it is computed via
    ``node_importance(W, score_mode)``.
    """
    W = np.asarray(W, dtype=float)
    if not np.allclose(W, W.T, atol=1e-9):
        raise ValueError("base W must be symmetric (undirected substrate)")
    off = W.copy()
    np.fill_diagonal(off, 0.0)
    if (off < -1e-12).any():
        raise ValueError("base W must be non-negative (all-positive edges) so that "
                         "f is the negative-weight fraction")
    if f <= 0.0:
        return W.copy()

    if node_score is None:
        node_score = node_importance(W, mode=score_mode)
    rows, cols, escore = edge_importance(W, node_score)
    flip = _select_flips(escore, f, targeting, rng, n_strata)

    signs = np.where(flip, -1.0, 1.0)
    out = W.copy()
    out[rows, cols] = W[rows, cols] * signs
    out[cols, rows] = W[cols, rows] * signs      # mirror -> stays symmetric
    return out


def negative_fraction(W: np.ndarray) -> float:
    """Realised fraction of upper-triangle edges with negative weight (the achieved
    ``f`` after within-stratum rounding), for honest per-matrix reporting."""
    W = np.asarray(W, dtype=float)
    rows, cols = np.triu_indices(W.shape[0], k=1)
    edges = W[rows, cols]
    present = edges != 0.0
    n = int(present.sum())
    return float((edges[present] < 0.0).sum() / n) if n else 0.0


# ---------------------------------------------------------------------------
# Self-test (unit-scale sanity check): python -m src.analysis.sign_composition
# ---------------------------------------------------------------------------
def _selftest() -> None:
    rng = np.random.default_rng(0)
    N = 200
    # A sparse (~6%), symmetric, all-positive weighted graph with a broad (hub)
    # degree spread -- a stand-in for a non-negative structural connectome.
    upper = np.triu(rng.random((N, N)) < 0.06, k=1)
    mask = (upper | upper.T).astype(float)
    mags = np.triu(np.abs(rng.standard_normal((N, N))) + 0.1, k=1)
    W = mask * (mags + mags.T)
    assert np.allclose(W, W.T) and (W >= 0).all()
    n_edges = int((np.triu(W, 1) != 0).sum())

    # f=0 is the identity.
    same = sign_fraction_matrix(W, 0.0, "stratified", rng)
    assert np.array_equal(same, W), "f=0 must be the identity"

    for targeting in TARGETING_MODES:
        out = sign_fraction_matrix(W, 0.3, targeting, np.random.default_rng(1))
        assert np.allclose(out, out.T), f"{targeting}: output must stay symmetric"
        assert np.allclose(np.abs(out), np.abs(W)), \
            f"{targeting}: magnitudes and topology must be preserved (sign only)"
        nf = negative_fraction(out)
        assert abs(nf - 0.3) < 0.03, f"{targeting}: neg fraction {nf:.3f} should be ~0.3"

    # f=0.5 stratified -> balanced sign.
    balanced = sign_fraction_matrix(W, 0.5, "stratified", np.random.default_rng(2))
    assert abs(negative_fraction(balanced) - 0.5) < 0.03, "f=0.5 should be ~balanced"

    # Placement: hub_first flips higher-importance edges than periphery_first, and
    # stratified sits between them (placement-neutral, ~ the overall mean score).
    score = node_importance(W, "degree")
    rows, cols, escore = edge_importance(W, score)
    mean_all = escore.mean()

    def flipped_mean(targeting, seed):
        flip = _select_flips(escore, 0.3, targeting, np.random.default_rng(seed), 10)
        return escore[flip].mean()

    hub, strat, peri = (flipped_mean("hub_first", 3), flipped_mean("stratified", 3),
                        flipped_mean("periphery_first", 3))
    assert hub > strat > peri, \
        f"placement ordering wrong: hub={hub:.1f} strat={strat:.1f} peri={peri:.1f}"
    assert abs(strat - mean_all) / mean_all < 0.15, \
        "stratified flipped set should track the overall score mean (placement-neutral)"

    # Stratified holds composition roughly constant across f (the confound fix): the
    # flipped-set mean score stays near the overall mean at every f.
    for f in (0.1, 0.25, 0.5):
        flip = _select_flips(escore, f, "stratified", np.random.default_rng(4), 10)
        rel = abs(escore[flip].mean() - mean_all) / mean_all
        assert rel < 0.15, f"stratified composition drifts at f={f} (rel {rel:.2f})"

    # Spectral / common-mode signature. At f=0 the largest eigenvalue of the
    # non-negative matrix IS the spectral radius (Perron-Frobenius). The robust,
    # physically meaningful effect of signing is that the common mode -- the mean
    # off-diagonal entry, which drives |mean_state| in the reservoir -- collapses
    # from strongly positive (f=0) toward ~0 (f=0.5, balanced).
    def _mean_edge(M):
        r, c = np.triu_indices(M.shape[0], k=1)
        e = M[r, c]
        e = e[e != 0.0]
        return float(e.mean()) if e.size else 0.0

    ev0 = np.linalg.eigvalsh(W)
    assert abs(ev0.max() - np.abs(ev0).max()) < 1e-9, \
        "f=0 top eigenvalue must be the positive Perron root (== spectral radius)"
    m0 = _mean_edge(W)
    mb = _mean_edge(balanced)
    assert m0 > 0.0, "all-positive base should have a positive common mode"
    assert abs(mb) < 0.15 * m0, \
        f"f=0.5 should collapse the common mode toward 0 (got {mb:.3f} vs {m0:.3f})"

    # Eigenvector-centrality score path runs and is a valid per-node vector.
    ec = node_importance(W, "eigenvector")
    assert ec.shape == (N,) and (ec >= 0).all()

    print("sign_composition self-test passed:")
    print(f"  N={N} edges={n_edges}  neg_frac(f=0.3): "
          f"strat={negative_fraction(sign_fraction_matrix(W, 0.3, 'stratified', np.random.default_rng(5))):.3f}")
    print(f"  flipped-set mean score  hub={hub:.1f} > strat={strat:.1f} "
          f"(~mean {mean_all:.1f}) > peri={peri:.1f}")
    print(f"  common mode (mean edge)  f=0: {m0:.3f}  ->  f=0.5: {mb:.3f}")


if __name__ == "__main__":
    _selftest()

# w_spectra.parquet -- accompanying note

Normalised base-matrix (W) spectra, one row per (condition, variant, rung, seed)
= 210 rows for the human N=448 substrate. W does not depend on task, and the
spectral-radius sweep only rescales it.

## Scaling rule (base matrix -> W(sr))

The reservoir build (src/reservoir/build.py :: rescale_spectral_radius) rescales the
base weighted matrix `W_base = builder.weighted(condition, variant, seed)` to a target
nominal spectral radius:

    l1   = max(|eigvals(W_base)|)          # dense np.linalg.eigvals
    W(sr) = W_base * (sr / l1)

So the eigenvalues of W(sr) are exactly `sr` times the eigenvalues of the NORMALISED
base matrix `W_base / l1` (spectral radius 1). This file exports the spectrum of that
normalised base matrix; multiply eig_w_real / eig_w_imag by any sr to recover W(sr).

`base_spectral_radius` records the divided-out l1 (= |lambda_1| of W_base).

## Columns

- eig_w_real, eig_w_imag : length-N eigenvalues of the normalised base matrix,
  sorted by DESCENDING modulus. Human W is symmetric, so eig_w_imag ~ 0 and
  is_symmetric is True (eigh path; the general eig path is kept for directed W).
- is_symmetric           : W symmetric within 1e-9.
- perron_root            : largest real-part eigenvalue (Perron-Frobenius root for a
                           non-negative W; == 1 there, so it marks whether the top
                           mode is the real positive Perron mode).
- bulk95_radius          : pct95(|lambda|) / |lambda_1| -- identical formula to the
                           spectral tier's bulk95_ratio (here |lambda_1| == 1).
- spectral_gap           : |lambda_1| - |lambda_2| (normalised: 1 - |lambda_2|).
- n_near_degenerate_10pct / _25pct : count of |lambda_i| within 10% / 25% of
                           |lambda_1| (>= 0.9 / 0.75; includes the top mode).
- top10_eigvec_ipr       : IPR = sum_i |v_i|^4 / (sum_i |v_i|^2)^2 of the leading 10
                           eigenvectors -- high = localised on few nodes (tests the
                           near-degenerate-pool memory hypothesis).

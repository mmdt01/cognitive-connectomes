"""Close-out reanalyses for E0.2 (items 4 and 5). No new simulations.

Five short analyses that either harden a claim before it is written down, or test one
of the loose ends the earlier passes left:

**4a — paired CIs on "the connectome is worst at peak."** The point-estimate deficits
across the alpha grid (3.4% / 1.2% / 4.0% / 5.6% / 7.8%) are non-monotone at the small
end, which is what noise looks like. The seed convention pairs connectome and null on
the same ``Win`` and the same input series, so the per-seed difference is a paired
contrast and admits a proper interval.

**4b — the ladder ordering as a curve in sigma**, not a thresholded scalar, with the
``sigma >= 3.05`` threshold justified structurally rather than chosen.

**5a — a ``|lambda_1|``-free axis.** ``bulk95`` is a ratio whose denominator is
extreme-value noisy (E0.4 §5). Re-running the E0.2 panel against the *absolute* bulk
radius (``bulk95 * |lambda_1|``, which self-averages) tests whether the verdict depends
on that noise.

**5b — Dale minus edge at matched f**, isolating the non-normality contribution: the
edge transform is exactly normal at every ``f``, the Dale transform is not.

**5c — anisotropy of the state covariance**, testing the proposed explanation for the
connectome's alpha-dependent optimum: if its covariance spectrum decays faster, raising
alpha strips marginal directions sooner and it must expand further to compensate.
"""

import numpy as np
import pandas as pd
from scipy import stats

from experiments.human.analysis.criticality_matched import analysis, common

CONN, CTR = common.CONN, common.CONTRAST
MC_ALPHAS = [1e-8, 1e-6, 1e-5, 7e-5, 1e-3]
_LADDER = [CONN, "connectome_weight_permuted", "degree_rewire", CTR]


# ---------------------------------------------------------------------------
# 4a. Paired per-seed peak comparison
# ---------------------------------------------------------------------------
def peak_parity(extended: pd.DataFrame, alphas=MC_ALPHAS) -> pd.DataFrame:
    """Per-seed peak MC, connectome vs each null, as a paired difference with a CI.

    Each seed's peak is taken over that seed's own sigma sweep (the optimum is
    seed-dependent), then differenced within the seed. Reports the paired mean, a
    t-based 95% CI, and a Wilcoxon signed-rank p -- the latter because n = 10 and
    normality is not worth assuming.
    """
    rows = []
    for alpha in alphas:
        col = f"mc_alpha_{alpha:g}"
        if col not in extended.columns:
            continue
        peak = (extended.groupby(["variant", "seed"])[col].max().unstack(0))
        for other in _LADDER[1:]:
            if other not in peak.columns:
                continue
            diff = (peak[CONN] - peak[other]).to_numpy(float)
            n = diff.size
            mean = float(diff.mean())
            sem = float(diff.std(ddof=1) / np.sqrt(n))
            half = float(stats.t.ppf(0.975, n - 1) * sem)
            try:
                _, p = stats.wilcoxon(diff)
            except ValueError:
                p = np.nan
            rows.append(dict(
                alpha=float(alpha), contrast=f"connectome - {other}", n=n,
                mean_diff=mean, ci_lo=mean - half, ci_hi=mean + half,
                pct_of_null=100.0 * mean / float(peak[other].mean()),
                wilcoxon_p=float(p),
                ci_excludes_zero=bool((mean - half) * (mean + half) > 0)))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 4b. Ladder ordering as a curve, with a structural threshold
# ---------------------------------------------------------------------------
def ladder_threshold_justification(bulk95_connectome: float,
                                   flip_sigma: float) -> dict:
    """The ``sigma >= 3.05`` cut is the connectome's own critical point, not a choice.

    ``sr_crit = 1 / bulk95`` for the connectome is 3.078 at N=448. The ordering flips
    sign at ``flip_sigma`` ~ 2.3, *below* that, so a threshold placed at the critical
    point excludes some sigma where the ordering already holds -- i.e. it is
    conservative, not tuned to maximise the effect.
    """
    sr_crit = 1.0 / bulk95_connectome
    return {
        "connectome_bulk95": float(bulk95_connectome),
        "connectome_sr_crit": float(sr_crit),
        "threshold_used": 3.05,
        "ordering_flip_sigma": float(flip_sigma),
        "threshold_is_conservative": bool(flip_sigma < 3.05 <= sr_crit + 0.05),
        "margin_sigma": float(3.05 - flip_sigma),
    }


# ---------------------------------------------------------------------------
# 5a. |lambda_1|-free axis
# ---------------------------------------------------------------------------
def add_absolute_axis(cells: pd.DataFrame, scale: int = common.SCALE) -> pd.DataFrame:
    """Attach ``x_absolute = sigma * bulk95 * |lambda_1|`` -- the un-normalised bulk.

    ``bulk95`` divides by ``|lambda_1|``, and that denominator is set by the largest
    *sampled* weight for a resampling null, so it does not concentrate (E0.4 §5).
    Multiplying it back out gives the absolute bulk radius of the base matrix, whose
    relative spread *falls* with N as a spectral statistic should. Same ordering
    information, different noise.
    """
    spectra = pd.read_parquet(
        common.eigenspectrum_summary(scale).parent / "spectra_per_seed.parquet",
        columns=["condition", "variant", "seed", "bulk95", "lambda_max_raw"])
    spectra = spectra[spectra.condition == "human_empirical"]
    lam = spectra.set_index(["variant", "seed"]).lambda_max_raw
    out = cells.copy()
    out["lambda_max_raw"] = [lam.get((v, s), np.nan)
                             for v, s in zip(out.variant, out.seed)]
    out["_x_absolute"] = out.spectral_radius * out.bulk95 * out.lambda_max_raw
    missing = int(out._x_absolute.isna().sum())
    if missing:
        raise RuntimeError(f"[abs-axis] {missing} cells have no |lambda_1| to join.")
    return out


# ---------------------------------------------------------------------------
# 5b. Dale minus edge at matched f
# ---------------------------------------------------------------------------
def dale_minus_edge(scale: int = common.SCALE) -> pd.DataFrame:
    """``dD`` under Dale minus ``dD`` under edge, at matched ``f`` and matched sigma.

    Both arms flip the same *fraction* of weight, stratified the same way. Edge keeps
    ``W`` symmetric (exactly normal at every ``f``); Dale negates whole outgoing
    columns and does not. So the difference at matched ``f`` isolates what
    non-normality contributes -- with the caveat that the two arms use independent
    flip-RNG streams, so this is a between-arm contrast, not a paired one.
    """
    df = pd.read_parquet(
        common.phase_cells_path(scale),
        columns=["sign_mode", "targeting", "f", "variant", "spectral_radius", "seed",
                 "draw", "task", "d_eff", "bulk95"])
    df = df[(df.task == "mc") & (df.targeting == "stratified")
            & (df.variant.isin([CONN, CTR]))]
    med = (df.groupby(["sign_mode", "f", "spectral_radius", "variant"], as_index=False)
           .agg(d_eff=("d_eff", "median"), bulk95=("bulk95", "median")))
    wide = med.pivot_table(index=["sign_mode", "f", "spectral_radius"],
                           columns="variant", values="d_eff").reset_index()
    wide["dD"] = wide[CONN] - wide[CTR]
    both = wide.pivot_table(index=["f", "spectral_radius"], columns="sign_mode",
                            values="dD").reset_index()
    both["dale_minus_edge"] = both["dale"] - both["edge"]
    return both


# ---------------------------------------------------------------------------
# 5c. Anisotropy of the state covariance
# ---------------------------------------------------------------------------
def anisotropy(scale: int = common.SCALE) -> pd.DataFrame:
    """Participation ratio and spectral decay exponent of the state covariance.

    Hypothesis under test: the connectome's covariance is far more anisotropic (the
    Perron/common mode dominates), so raising ``alpha`` removes marginal directions
    sooner and it must run at higher sigma to compensate -- which would explain its
    alpha-dependent optimum while the nulls' stays put.

    The decay exponent is the slope of ``log(eigenvalue)`` against ``log(rank)`` over
    the top decile: steeper (more negative) = more anisotropic.
    """
    path = (common.probe3_path(scale).parent / "covariance_spectra.parquet")
    cov = pd.read_parquet(path)
    return _anisotropy_rows(cov)


def _anisotropy_rows(cov: pd.DataFrame) -> pd.DataFrame:
    cov = cov[(cov.task == "mc") & (cov.condition == "human_empirical")]
    rows = []
    for record in cov.itertuples():
        eig = np.asarray(record.eig_cov, dtype=float)
        eig = eig[eig > 0]
        if eig.size < 20:
            continue
        total = eig.sum()
        pr = float(total ** 2 / (eig ** 2).sum())
        k = max(10, eig.size // 10)
        ranks = np.arange(1, k + 1)
        slope = float(np.polyfit(np.log(ranks), np.log(eig[:k]), 1)[0])
        rows.append(dict(variant=record.variant, seed=int(record.seed),
                         spectral_radius=float(record.spectral_radius),
                         pr=pr, pr_norm=pr / eig.size,
                         decay_exponent=slope,
                         top_mode_fraction=float(eig[0] / total)))
    return pd.DataFrame(rows)


def floor_mass(scale: int = common.SCALE, alpha: float = 1e-6) -> pd.DataFrame:
    """Item 3: how much of the **design-Gram** spectrum sits at the ridge floor.

    §3.6 rejected the anisotropy hypothesis using a decay exponent fitted over the
    *top* decile -- but the surviving hypothesis ("the connectome has more directions
    near the ridge floor, so raising alpha strips more of them") is a claim about the
    *bottom*. This refits it there, and on the right object: ``d_eff`` sums
    ``g/(g+alpha)`` over the **Gram** spectrum, not the covariance, so the Gram is what
    the floor acts on.

    The decisive statistic is the sensitivity of ``d_eff`` to the floor,

        -d(d_eff)/d(log alpha) = sum_i  g_i * alpha / (g_i + alpha)^2

    which is exactly the number of directions sitting *at* the floor: each term peaks
    at 1/4 when ``g_i == alpha`` and vanishes when ``g_i`` is far from it either way.
    If the connectome has more mass there, raising alpha costs it more, and the moving
    optimum is explained.
    """
    path = (common.probe3_path(scale).parent / "covariance_spectra.parquet")
    cov = pd.read_parquet(path)
    cov = cov[(cov.task == "mc") & (cov.condition == "human_empirical")]
    rows = []
    for record in cov.itertuples():
        g = np.asarray(record.eig_gram, dtype=float)
        g = g[g > 0]
        if g.size == 0:
            continue
        sensitivity = float((g * alpha / (g + alpha) ** 2).sum())
        rows.append(dict(
            variant=record.variant, seed=int(record.seed),
            spectral_radius=float(record.spectral_radius),
            d_eff=float((g / (g + alpha)).sum()),
            floor_sensitivity=sensitivity,
            n_within_decade=int(((g > alpha / 10) & (g < alpha * 10)).sum()),
            n_below_floor=int((g < alpha).sum()),
            frac_below_floor=float((g < alpha).mean()),
            log10_condition=float(np.log10(g.max() / g.min())) if g.min() > 0 else np.nan,
        ))
    return pd.DataFrame(rows)


def median_bulk_axis(cells: pd.DataFrame) -> pd.DataFrame:
    """Replace each cell's own ``bulk95`` with its variant median.

    The real test of E0.4 §5's extreme-value concern: if the verdict is unchanged when
    every trace of per-seed ``bulk95`` noise is removed, the noise was not carrying it.
    """
    med = cells.groupby("variant").bulk95.median()
    out = cells.copy()
    out["_x_medbulk"] = out.spectral_radius * out.variant.map(med)
    return out


def run(scale: int = common.SCALE) -> dict:
    """Items 4a-4b and 5a-5c end to end; writes artifacts and a summary."""
    import json
    common.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    print("=" * 70 + "\nE0.2 close-out (items 4 and 5)\n" + "=" * 70)

    extended = pd.read_parquet(common.extended_sweep_path(scale))
    cells, _ = analysis.load_panel_cells(scale)
    cells = add_absolute_axis(cells, scale)
    cells = median_bulk_axis(cells)

    parity = peak_parity(extended)
    parity.to_csv(common.RESULTS_DIR / "closeout_peak_parity.csv", index=False)

    ordering = pd.read_csv(common.RESULTS_DIR / "taskA_ordering_by_sigma.csv")
    flip = float(ordering[ordering.spearman_vs_rank < 0].spectral_radius.min())
    justification = ladder_threshold_justification(
        float(cells[cells.variant == CONN].bulk95.median()), flip)

    axes = {}
    for col, name in (("_x_effective", "sigma*bulk95 (per-seed)"),
                      ("_x_medbulk", "sigma*bulk95 (variant median)"),
                      ("_x_absolute", "sigma*absolute bulk (|lambda1|-free)")):
        lo, hi = analysis.overlap_range(cells, col, [CONN, CTR])
        grid = np.linspace(lo, hi, common.N_GRID)
        frame = analysis.paired_difference(
            analysis.reindex(cells, col, grid, "linear"), grid)
        axes[name] = analysis.summarise_axis(frame, dict(
            axis=name, interp="linear", overlap_lo=lo, overlap_hi=hi,
            full_lo=float(cells[col].min()), full_hi=float(cells[col].max()),
            fraction_of_full_range=float("nan"), complete_seed_coverage=True))
    pd.DataFrame(axes.values()).to_csv(
        common.RESULTS_DIR / "closeout_axis_sensitivity.csv", index=False)

    scale_table = cells.groupby("variant").agg(
        bulk95=("bulk95", "median"), lambda_max_raw=("lambda_max_raw", "median"))
    scale_table["absolute_bulk"] = scale_table.bulk95 * scale_table.lambda_max_raw
    scale_table.to_csv(common.RESULTS_DIR / "closeout_bulk_decomposition.csv")

    dme = dale_minus_edge(scale)
    dme.to_csv(common.RESULTS_DIR / "closeout_dale_minus_edge.csv", index=False)
    aniso = anisotropy(scale)
    aniso.to_csv(common.RESULTS_DIR / "closeout_anisotropy.csv", index=False)
    floor = floor_mass(scale)
    floor.to_csv(common.RESULTS_DIR / "closeout_floor_mass.csv", index=False)

    common.write_manifest(
        common.RESULTS_DIR / "manifest_closeout.json", "E0.2 close-out", scale,
        mc_alpha_grid=MC_ALPHAS, ladder=_LADDER,
        ladder_threshold=justification,
        axes={k: {kk: vv for kk, vv in v.items() if isinstance(vv, (int, float, bool))}
              for k, v in axes.items()})
    print(json.dumps(justification, indent=2))
    print("\nClose-out complete.")
    return {"parity": parity, "axes": axes, "scale_table": scale_table,
            "dale_minus_edge": dme, "anisotropy": aniso, "floor_mass": floor,
            "justification": justification}

"""Frozen-artifact loaders: one per figure source, each carrying its exact filter.

This is the single place a figure learns *which* rows it is allowed to see. A figure
builder never touches a path or writes a filter; it asks for a named source and gets a
tidy frame back. That keeps the filter next to the claim it supports, and makes
``report/FIGURE_LIST.md`` checkable against code rather than against memory.

Each source also supplies a **placeholder** with the identical schema, so the smoke
entry point can render every layout with no frozen data present.

Filters that are not obvious are recorded on the ``Source`` and printed by ``--verify``:

* ``sr_crit`` is ``1 / median_over_seeds(bulk95)`` (CONVENTIONS), never the per-seed mean.
* The **absolute** bulk radius is ``bulk95 * lambda_max_raw``. ``bulk95_radius`` in the
  frozen parquet is the *ratio*, despite the name, and ``perron_root`` is 1.0 for every
  row because the spectrum is stored normalised. Use ``lambda_max_raw`` for ``|lambda_1|``.
* The N=1000 supercritical margin is taken at sigma >= the **connectome's** ``sr_crit``
  for every variant. Using each variant's own ``sr_crit`` gives 3.56/3.85, not TIER0's
  4.40/4.42.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd

_REPO_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS = _REPO_ROOT / "experiments" / "human" / "analysis"
CRIT = ANALYSIS / "criticality_matched" / "results"
EIGEN = ANALYSIS / "eigenspectrum" / "results"
PROBES = ANALYSIS / "results"

LADDER = ["connectome", "connectome_weight_permuted", "degree_rewire", "erdos_renyi"]
BASE_CONDITION = "human_empirical"
N_NODES = 448

# sr_crit = 1 / median_over_seeds(bulk95), recomputed by ``eigenspectrum`` at both
# scales (TIER0 §2.1). Held here because several filters key off the connectome's.
SR_CRIT = {448: {"connectome": 3.078, "connectome_weight_permuted": 1.922,
                 "degree_rewire": 1.873, "erdos_renyi": 1.807},
           1000: {"connectome": 3.985, "connectome_weight_permuted": 2.395,
                  "degree_rewire": 2.301, "erdos_renyi": 2.438}}

_RNG = np.random.default_rng(0)


@dataclass
class Source:
    """One frozen artifact plus the exact filter a figure is allowed to apply to it."""
    name: str
    path: Path
    columns: tuple
    filter_note: str
    load: Callable[[], pd.DataFrame] = field(repr=False)
    placeholder: Callable[[], pd.DataFrame] = field(repr=False)

    def exists(self) -> bool:
        return self.path.exists()


# =============================================================================
# Loaders
# =============================================================================
def _spectra(scale: int) -> pd.DataFrame:
    """E0.4 per-seed spectra, ladder only, on the non-negative substrate.

    Adds the two derived columns TIER0 §3.1 reports but the file does not carry:
    ``abs_bulk`` (= bulk95 * lambda_max_raw) and ``gap_ratio`` (= 1 / bulk95).
    """
    frame = pd.read_parquet(EIGEN / f"scale_{scale}/spectra_per_seed.parquet")
    frame = frame[(frame.condition == BASE_CONDITION)
                  & (frame.variant.isin(LADDER))].copy()
    frame["abs_bulk"] = frame.bulk95 * frame.lambda_max_raw
    frame["gap_ratio"] = 1.0 / frame.bulk95
    frame["scale"] = scale
    return frame


def _spectra_both_scales() -> pd.DataFrame:
    return pd.concat([_spectra(448), _spectra(1000)], ignore_index=True)


def _alignment() -> pd.DataFrame:
    """Probe 2 basis alignment: captured variance of the time-centred covariance."""
    return pd.read_parquet(PROBES / "scale_448/manifold_alignment.parquet")


def _saturation() -> pd.DataFrame:
    """Probe 1 saturation diagnostics; ``mean_state`` is the common-mode proxy."""
    frame = pd.read_parquet(PROBES / "scale_448/saturation_diagnostics.parquet")
    return frame[frame.variant.isin(LADDER)].copy()


def _probe3() -> pd.DataFrame:
    """Probe 3, MC on the non-negative substrate, supercritical, at the frozen alpha.

    ``alpha = 1e-6`` is the only alpha captured at sigma >= 3.05 in this file; the
    other two exist on the reduced grid only.
    """
    frame = pd.read_parquet(PROBES / "scale_448/probe3_deff.parquet")
    return frame[(frame.task == "mc") & (frame.condition == BASE_CONDITION)
                 & (frame.spectral_radius >= 3.05)
                 & (frame.alpha == 1e-6)].copy()


def _taskb() -> pd.DataFrame:
    """Task B: f = 0, MC, four variants, sigma to 8. Adds the matched axis x."""
    frame = pd.read_parquet(CRIT / "taskB_extended_sweep_scale_448.parquet").copy()
    frame["x"] = frame.spectral_radius * frame.bulk95
    return frame


def _e02_panel() -> pd.DataFrame:
    """E0.2 dD curve on both axes, 121 interpolated grid points each."""
    frame = pd.read_parquet(CRIT / "e02_panel.parquet")
    return frame[frame.interp == "linear"].copy()


def _e02_axis_summary() -> pd.DataFrame:
    return pd.read_csv(CRIT / "e02_axis_summary.csv")


def _n1000() -> pd.DataFrame:
    """N=448 control and N=1000 run, tagged by ``n_nodes``."""
    frames = [pd.read_parquet(CRIT / f"n1000_memory_scale_{s}.parquet") for s in (448, 1000)]
    return pd.concat(frames, ignore_index=True)


def _peak_parity() -> pd.DataFrame:
    """Paired per-seed peak differences with CIs across the alpha grid (TIER0 §3.4)."""
    return pd.read_csv(CRIT / "closeout_peak_parity.csv")


def _mechanism_matched() -> pd.DataFrame:
    """How much of the connectome-ER MC gap matching on x absorbs, per f (TIER0 §3.7)."""
    return pd.read_csv(CRIT / "e03_mechanism_matched_scale_448.csv")


def _f_extension() -> pd.DataFrame:
    """The f > 0 extension to sigma = 11.2, all four variants, MC and Lorenz.

    Two files, one per variant set; concatenated because they are the same grid.
    Carries ``mean_state`` (the common-mode proxy) and ``mean_curvature`` per cell.
    """
    frames = [pd.read_parquet(CRIT / "item2_f_extension_scale_448.parquet"),
              pd.read_parquet(CRIT / "item3_f_extension_nulls_scale_448.parquet")]
    return pd.concat(frames, ignore_index=True)


def _jacobian() -> pd.DataFrame:
    """The exact-Jacobian capture: 38,280 Lorenz cells, four variants (TIER0 §3.11)."""
    return pd.read_parquet(CRIT / "e01_jacobian_scale_448.parquet")


def _frontier() -> pd.DataFrame:
    """E0.3 absolute frontier: seed medians of MC and VPT over (variant, f, sigma)."""
    return pd.read_parquet(CRIT / "e03_frontier_scale_448.parquet")


def _frontier_paired() -> pd.DataFrame:
    """Paired connectome-minus-null contrasts with CIs and Holm-corrected p."""
    return pd.read_csv(CRIT / "e03_frontier_paired_scale_448.csv")


def _collapse_loci() -> pd.DataFrame:
    """Per-(f, variant) collapse fractions and loci. Quote **seeds**, not replicates."""
    return pd.read_csv(CRIT / "item2_collapse_loci_scale_448.csv")


def _threshold_invariance() -> pd.DataFrame:
    """Locator invariance by criterion. TIER0 §3.10's table is the ``f > 0`` scope."""
    return pd.read_csv(CRIT / "e01_threshold_invariance_scale_448.csv")


def _threshold_table() -> pd.DataFrame:
    """Per-(variant, f) transition brackets in sigma, x and sigma_eff."""
    return pd.read_csv(CRIT / "e01_threshold_table_scale_448.csv")


def _boundaries(axis: str) -> pd.DataFrame:
    """The two phase boundaries on one axis, over the sigma = 11.2 extension.

    ``panel == "dD"`` is the memory boundary, ``panel == "dStraight"`` the generative
    one. Three contour-level conventions ship side by side: ``f_star`` (level over
    fully covered cells, the one TIER0 §2.3 adopts), ``f_star_level_on_subrange`` (level
    pinned to the old x <= 2.336 range, which gives the identical crossing) and
    ``f_star_level_raw_max`` (level set by a cell backed by 1 replicate of 30, which
    gives no crossing at all and is the convention TIER0 rejects).

    ``f_star`` is NaN wherever the contour does not exist, so a figure must break the
    line there rather than interpolate across the gap.
    """
    suffix = "" if axis == "effective" else "_nominal"
    frame = pd.read_csv(CRIT / f"e02_heatmap_boundaries_extension{suffix}.csv")
    frame["axis"] = axis
    return frame


def _boundaries_both() -> pd.DataFrame:
    return pd.concat([_boundaries("effective"), _boundaries("nominal")],
                     ignore_index=True)


def _coverage() -> pd.DataFrame:
    """Per-f extent reached by ALL 30 replicates on the matched-bulk axis.

    Past ``x_hi`` the panel is populated only by the replicates whose own bulk95 reached
    that far, so the boundary there rests on a bulk95-selected subsample (TIER0 §6.10)
    and must be drawn as unreadable. The nominal axis needs no such mask: every nominal
    cell carries all 30 replicates (TIER0 §2.3).
    """
    return pd.read_csv(CRIT / "e02_heatmap_coverage_extension.csv")


def _perron_yeo() -> pd.DataFrame:
    """Perron-mode mass per Yeo network on the sweep substrate.

    The only source computed live rather than read from a frozen parquet: the leading
    eigenvector is not persisted anywhere. It is one ``eigh`` on the 448-node consensus
    plus the release RSN labels, so it is seconds, not a run. See FIGURE_LIST F15 for
    the standing caveat on the release-to-consensus node correspondence.
    """
    from src.connectomes.human_suarez import load_routing_geometry, YEO_NETWORKS
    from experiments.human.substrates import HumanSubstrateBuilder

    geometry = load_routing_geometry(N_NODES)
    builder = HumanSubstrateBuilder(scale=N_NODES)
    weighted = builder.weighted(BASE_CONDITION, "connectome", 0)
    eigenvalues, eigenvectors = np.linalg.eigh(weighted)
    perron = np.abs(eigenvectors[:, int(np.argmax(eigenvalues))])
    position = {node: i for i, node in enumerate(geometry["cortical"])}
    rows = []
    for network in YEO_NETWORKS:
        index = np.array([position[j] for j in geometry["yeo_groups"][network]
                          if j in position])
        rows.append(dict(network=network, n_nodes=len(index),
                         perron_mass=float((perron[index] ** 2).sum()),
                         mean_loading=float(perron[index].mean())))
    frame = pd.DataFrame(rows)
    frame["mass_per_node"] = frame.perron_mass / frame.n_nodes
    return frame


# =============================================================================
# Placeholders -- identical schema, synthetic values. Layout check only.
# =============================================================================
def _ph_spectra(scale: int = 448) -> pd.DataFrame:
    rows = []
    for variant, bulk in zip(LADDER, (0.32, 0.52, 0.53, 0.55)):
        for seed in range(10):
            noise = 1.0 + 0.05 * _RNG.standard_normal()
            eig = np.sort(np.concatenate([
                _RNG.uniform(-bulk, bulk, scale - 1), [1.0]]))
            rows.append(dict(condition=BASE_CONDITION, variant=variant, seed=seed,
                             eig_w_real=eig, bulk95=bulk * noise,
                             lambda_max_raw=0.19 / (bulk / 0.32) * noise,
                             perron_root=1.0, scale=scale))
    frame = pd.DataFrame(rows)
    frame["abs_bulk"] = frame.bulk95 * frame.lambda_max_raw
    frame["gap_ratio"] = 1.0 / frame.bulk95
    return frame


def _ph_spectra_both() -> pd.DataFrame:
    return pd.concat([_ph_spectra(448), _ph_spectra(1000)], ignore_index=True)


def _ph_alignment() -> pd.DataFrame:
    k_grid = [1, 2, 3, 5, 10, 20, 30, 50, 100, 150, 200, 300]
    rows = []
    for task in ("mc", "narma10", "lorenz"):
        for condition in ("human_empirical", "human_empirical_signed", "human_gaussian"):
            for basis, ceiling in (("harmonics", 0.2), ("wmodes", 0.6), ("random", 0.05)):
                for sr in (0.9474, 3.0526):
                    for k in k_grid:
                        rows.append(dict(task=task, condition=condition,
                                         variant="connectome", seed=0,
                                         spectral_radius=sr, basis=basis, k=k,
                                         captured=ceiling * k / (k + 40),
                                         captured_std=0.01))
    return pd.DataFrame(rows)


def _ph_saturation() -> pd.DataFrame:
    rows = []
    for task in ("mc", "narma10", "lorenz"):
        for variant, ceiling in zip(LADDER, (0.76, 0.95, 0.96, 0.99)):
            for sr in np.linspace(0, 6, 25):
                for seed in range(10):
                    rows.append(dict(task=task, condition=BASE_CONDITION,
                                     variant=variant, spectral_radius=sr, seed=seed,
                                     mean_state=ceiling * np.tanh(sr / 2),
                                     mean_gain=1 / (1 + sr), frac_saturated=0.1 * sr,
                                     effective_radius=0.3 * sr))
    return pd.DataFrame(rows)


def _ph_probe3() -> pd.DataFrame:
    variants = LADDER + ["clustering_rewire", "modularity_rewire", "random_gaussian"]
    rows = []
    for i, variant in enumerate(variants):
        for sr in (3.05, 4.0, 5.0, 6.0):
            for seed in range(10):
                d_eff = 420 - 50 * i + 5 * _RNG.standard_normal()
                rows.append(dict(task="mc", condition=BASE_CONDITION, variant=variant,
                                 rung=i - 1, spectral_radius=sr, seed=seed,
                                 alpha=1e-6, d_eff=d_eff, pr=1.2 + 0.02 * _RNG.standard_normal(),
                                 mc=4 + d_eff / 45))
    return pd.DataFrame(rows)


def _ph_taskb() -> pd.DataFrame:
    rows = []
    for variant, bulk, retained in zip(LADDER, (0.325, 0.520, 0.534, 0.554),
                                       (0.47, 0.28, 0.22, 0.11)):
        for sr in np.arange(0, 8.4, 0.4):
            for seed in range(10):
                x = sr * bulk
                d_eff = 440 * np.exp(-((x - 1.0) ** 2) / 0.9) if x < 1 else \
                    440 * retained ** ((x - 1.0) / 1.6)
                rows.append(dict(variant=variant, seed=seed, spectral_radius=sr,
                                 bulk95=bulk, x=x, d_eff=d_eff, mc=d_eff / 30,
                                 alpha=1e-6))
    return pd.DataFrame(rows)


def _ph_e02_panel() -> pd.DataFrame:
    rows = []
    for axis, hi, peak, at in (("nominal", 8.0, 343.3, 4.47), ("effective", 2.6, 196.5, 1.95)):
        for x in np.linspace(0, hi, 121):
            value = peak * np.exp(-((x - at) ** 2) / (0.25 * hi)) - 0.35 * peak * np.exp(-(x / (0.15 * hi)) ** 2)
            rows.append(dict(x=x, dD_median=value, dD_q25=value - 20, dD_q75=value + 20,
                             n_seeds=10, axis=axis, interp="linear",
                             d_eff_connectome=430 * np.exp(-x / hi),
                             d_eff_connectome_weight_permuted=445 * np.exp(-1.6 * x / hi),
                             d_eff_degree_rewire=444 * np.exp(-1.8 * x / hi),
                             d_eff_erdos_renyi=446 * np.exp(-2.4 * x / hi)))
    return pd.DataFrame(rows)


def _ph_n1000() -> pd.DataFrame:
    rows = []
    for n_nodes, top in ((448, 8.0), (1000, 10.4)):
        for variant, peak in zip(LADDER, (13.5, 12.0, 11.0, 10.0)):
            for sr in np.linspace(0, top, 21):
                for seed in range(10):
                    mc = peak * np.exp(-((sr - 2.0) ** 2) / 12) * (1.13 if n_nodes == 1000 else 1)
                    rows.append(dict(variant=variant, seed=seed, n_nodes=n_nodes,
                                     spectral_radius=sr, mc=mc, d_eff=30 * mc,
                                     d_eff_norm=30 * mc / n_nodes, bulk95=0.33,
                                     alpha=1e-6))
    return pd.DataFrame(rows)


def _ph_peak_parity() -> pd.DataFrame:
    rows = []
    for alpha in (1e-8, 1e-6, 1e-5, 7e-5, 1e-3):
        for null in ("connectome_weight_permuted", "degree_rewire", "erdos_renyi"):
            diff = -0.4 - 0.3 * _RNG.random()
            rows.append(dict(alpha=alpha, contrast=f"connectome - {null}", n=10,
                             mean_diff=diff, ci_lo=diff - 0.15, ci_hi=diff + 0.15,
                             pct_of_null=diff / 0.15, wilcoxon_p=0.01,
                             ci_excludes_zero=True))
    return pd.DataFrame(rows)


def _ph_mechanism_matched() -> pd.DataFrame:
    f_grid = np.arange(0, 0.55, 0.05)
    return pd.DataFrame(dict(
        f=f_grid, x_lo=0.0, x_hi=3.6 + 2 * f_grid,
        median_abs_gap_matched_x=4.75 * np.exp(-9 * f_grid) + 0.5,
        max_gap_matched_x=5.4 * np.exp(-8 * f_grid) + 1.2,
        median_abs_gap_matched_sigma=6.42 * np.exp(-9 * f_grid) + 1.0,
        max_gap_matched_sigma=11.3 * np.exp(-8 * f_grid) + 1.9))


def _ph_f_extension() -> pd.DataFrame:
    rows = []
    for variant, ceiling in zip(LADDER, (0.76, 0.95, 0.96, 0.99)):
        for f in np.arange(0, 0.55, 0.05):
            for sr in (2.0, 6.0):
                for seed in range(10):
                    rows.append(dict(variant=variant, f=f, spectral_radius=sr, seed=seed,
                                     draw=0, task="mc", mean_state=ceiling * np.exp(-9 * f),
                                     mean_curvature=0.26, mc=12 - 8 * np.exp(-9 * f),
                                     bulk95=0.33, alpha=1e-6))
    return pd.DataFrame(rows)


def _ph_jacobian() -> pd.DataFrame:
    n = 38280
    collapsed = _RNG.random(n) < 0.58
    curvature = np.where(collapsed, 3.0 + 0.08 * _RNG.standard_normal(n),
                         0.26 + 0.02 * _RNG.standard_normal(n))
    between = _RNG.random(n) < 0.0056
    curvature = np.where(between, _RNG.uniform(0.6, 2.2, n), curvature)
    vpt = np.where(collapsed, np.clip(0.4 * _RNG.random(n), 0, None),
                   2.5 + 1.5 * _RNG.random(n))
    return pd.DataFrame(dict(
        variant=_RNG.choice(LADDER, n), f=_RNG.choice(np.arange(0, 0.55, 0.05), n),
        spectral_radius=_RNG.choice(np.arange(0, 11.6, 0.4), n),
        seed=_RNG.integers(0, 10, n), draw=_RNG.integers(0, 3, n), task="lorenz",
        mean_curvature=curvature, vpt=vpt,
        lambda_min_J=-0.85 + 0.1 * _RNG.standard_normal(n),
        mean_gain=0.5 * _RNG.random(n), effective_radius=_RNG.random(n)))


def _ph_frontier() -> pd.DataFrame:
    rows = []
    for metric in ("mc", "vpt"):
        for variant, edge in zip(LADDER, (1.0, 0.55, 0.5, 0.4)):
            for f in np.arange(0, 0.55, 0.05):
                for sr in np.arange(0, 11.6, 0.4):
                    if metric == "mc":
                        value = (2.4 + 9 * edge) + (12 - 9 * edge) * (1 - np.exp(-12 * f))
                        value *= np.exp(-((sr - 6) ** 2) / 60)
                    else:
                        value = 4.4 * edge * np.exp(-4 * f * (1 - edge) - ((sr - 2) ** 2) / 8)
                    rows.append(dict(variant=variant, f=f, spectral_radius=sr,
                                     median=value, q25=value * 0.85, q75=value * 1.15,
                                     n_seeds=10, frac_at_floor=0.0, metric=metric,
                                     bulk95=0.33, x=sr * 0.33))
    return pd.DataFrame(rows)


def _ph_frontier_paired() -> pd.DataFrame:
    rows = []
    for null in ("connectome_weight_permuted", "degree_rewire", "erdos_renyi"):
        for f in np.arange(0, 0.55, 0.05):
            diff = 2.2 * (1 - np.exp(-9 * f)) * (0.8 + 0.2 * _RNG.random())
            rows.append(dict(metric="vpt", spectral_radius=2.0, f=f, null=null,
                             n_seeds=10, connectome_median=3.0, null_median=3.0 - diff,
                             mean_diff=diff, ci_lo=diff - 0.5, ci_hi=diff + 0.5,
                             cliffs_delta=0.6, p_raw=0.01, p_holm=0.03,
                             significant=f >= 0.2, p_floor_binding=False))
    return pd.DataFrame(rows)


def _ph_collapse_loci() -> pd.DataFrame:
    rows = []
    for variant, rate in zip(["connectome", "erdos_renyi"], (0.0, 0.5)):
        for f in np.arange(0, 0.55, 0.05):
            rows.append(dict(f=f, variant=variant, frac_collapsed=min(1.0, rate + 1.6 * f),
                             sigma_lo=7.6, sigma_hi=8.0, x_lo=2.5, x_hi=2.6,
                             sigma_eff_at_collapse=0.8,
                             n_seeds_collapsed=int(10 * min(1.0, rate + 1.6 * f)),
                             n_seeds=10, delta_sigma_collapse=0.0, delta_x_collapse=-0.2))
    return pd.DataFrame(rows)


def _ph_threshold_invariance() -> pd.DataFrame:
    rows = []
    for scope in ("all f", "f > 0", "f = 0"):
        for criterion, median, cv in (
                ("nominal sigma", 1.8, 0.667),
                ("sigma * bulk95  (linear negative-mode gain)", 1.002, 0.746),
                ("sigma_eff = bulk95 * sigma * <1-x^2>", 0.777, 0.209)):
            rows.append(dict(scope=scope, criterion=criterion, n=37, median=median,
                             iqr=median * cv, cv=cv, lo=median * 0.6, hi=median * 1.4))
    return pd.DataFrame(rows)


def _ph_threshold_table() -> pd.DataFrame:
    rows = []
    for variant, low in zip(LADDER, (0.71, 0.79, 0.82, 0.87)):
        for f in np.arange(0, 0.55, 0.05):
            rows.append(dict(variant=variant, f=f, frac_seeds_collapsed=0.8, n_seeds=10,
                             spectral_radius_lo=1.6, spectral_radius_hi=2.0,
                             x_linear_lo=1.0, x_linear_hi=1.2,
                             effective_radius_lo=low, effective_radius_hi=low + 0.08,
                             vpt_lo=1.0))
    return pd.DataFrame(rows)


def _ph_boundaries_both() -> pd.DataFrame:
    rows = []
    for axis, hi, cross_at in (("effective", 4.36, 2.94), ("nominal", 11.2, None)):
        for x in np.linspace(0, hi, 121):
            memory = 0.19 * np.clip((x - 0.9) / (hi - 0.9), 0, 1)
            generative = 0.35 - 0.30 * np.clip(x / hi, 0, 1)
            if cross_at is None:                      # nominal: no crossing survives
                generative = np.clip(generative - 0.14, 0.0, None)
            rows.append(dict(panel="dD", x=x, f_star=memory,
                             f_star_level_on_subrange=memory,
                             f_star_level_raw_max=memory * 0.6, axis=axis))
            rows.append(dict(panel="dStraight", x=x, f_star=generative,
                             f_star_level_on_subrange=generative,
                             f_star_level_raw_max=np.nan, axis=axis))
    return pd.DataFrame(rows)


def _ph_coverage() -> pd.DataFrame:
    f_grid = np.arange(0, 0.55, 0.05)
    return pd.DataFrame(dict(f=f_grid, x_lo=0.0,
                             x_hi=3.58 + 0.8 * f_grid, sigma_max=11.2))


def _ph_perron_yeo() -> pd.DataFrame:
    networks = ("VIS", "SM", "DA", "VA", "LIM", "FP", "DMN")
    sizes = (69, 97, 27, 58, 45, 30, 122)
    mass = np.array([0.001, 0.377, 0.001, 0.436, 0.001, 0.001, 0.183])
    frame = pd.DataFrame(dict(network=networks, n_nodes=sizes, perron_mass=mass,
                              mean_loading=mass / np.array(sizes)))
    frame["mass_per_node"] = frame.perron_mass / frame.n_nodes
    return frame


# =============================================================================
# Registry
# =============================================================================
SOURCES = {
    "spectra_448": Source(
        "spectra_448", EIGEN / "scale_448/spectra_per_seed.parquet",
        ("eig_w_real", "bulk95", "lambda_max_raw", "abs_bulk", "gap_ratio"),
        "condition == 'human_empirical' and variant in the four-variant ladder; "
        "40 rows (4 variants x 10 seeds). abs_bulk and gap_ratio derived here.",
        lambda: _spectra(448), lambda: _ph_spectra(448)),
    "spectra_both": Source(
        "spectra_both", EIGEN / "scale_1000/spectra_per_seed.parquet",
        ("bulk95", "lambda_max_raw", "abs_bulk", "gap_ratio", "scale"),
        "both scales concatenated with a 'scale' column; same filter as spectra_448.",
        _spectra_both_scales, _ph_spectra_both),
    "alignment": Source(
        "alignment", PROBES / "scale_448/manifold_alignment.parquet",
        ("task", "condition", "basis", "k", "captured"),
        "no row filter; figures select basis in {harmonics, wmodes, random} and the "
        "supercritical operating point per condition. Variants are connectome and "
        "degree_rewire only, which is all Probe 2 captured.",
        _alignment, _ph_alignment),
    "saturation": Source(
        "saturation", PROBES / "scale_448/saturation_diagnostics.parquet",
        ("task", "condition", "variant", "spectral_radius", "mean_state", "mean_gain"),
        "variant in the ladder; figures then select a task and condition.",
        _saturation, _ph_saturation),
    "probe3": Source(
        "probe3", PROBES / "scale_448/probe3_deff.parquet",
        ("variant", "d_eff", "pr", "mc"),
        "task == 'mc', condition == 'human_empirical', spectral_radius >= 3.05, "
        "alpha == 1e-6 (the only alpha captured supercritically). 350 rows, 7 variants.",
        _probe3, _ph_probe3),
    "taskb": Source(
        "taskb", CRIT / "taskB_extended_sweep_scale_448.parquet",
        ("variant", "spectral_radius", "bulk95", "x", "d_eff", "mc"),
        "no row filter; f = 0, MC, four variants, sigma in [0, 8] step 0.4, 10 seeds. "
        "x = spectral_radius * bulk95 from the file's own bulk95 column.",
        _taskb, _ph_taskb),
    "e02_panel": Source(
        "e02_panel", CRIT / "e02_panel.parquet",
        ("x", "dD_median", "dD_q25", "dD_q75", "axis"),
        "interp == 'linear'; 121 grid points per axis, axis in {nominal, effective}.",
        _e02_panel, _ph_e02_panel),
    "e02_axis_summary": Source(
        "e02_axis_summary", CRIT / "e02_axis_summary.csv",
        ("axis", "peak_dD", "peak_x", "min_dD", "min_x", "overlap_hi"),
        "two rows, one per axis. TIER0 §2.2's table verbatim.",
        _e02_axis_summary, lambda: pd.DataFrame(dict(
            axis=["nominal", "effective"], interp="linear", overlap_hi=[8.0, 2.599],
            peak_dD=[343.3, 196.5], peak_x=[4.467, 1.949], min_dD=[-217.4, -24.0],
            min_x=[1.533, 0.931]))),
    "n1000": Source(
        "n1000", CRIT / "n1000_memory_scale_1000.parquet",
        ("variant", "n_nodes", "spectral_radius", "mc", "d_eff", "d_eff_norm"),
        "both scale files concatenated. Supercritical means sigma >= the CONNECTOME's "
        "sr_crit (3.078 at N=448, 3.985 at N=1000) for every variant.",
        _n1000, _ph_n1000),
    "peak_parity": Source(
        "peak_parity", CRIT / "closeout_peak_parity.csv",
        ("alpha", "contrast", "mean_diff", "ci_lo", "ci_hi", "wilcoxon_p"),
        "15 rows: 5 alpha x 3 contrasts, all connectome minus a null.",
        _peak_parity, _ph_peak_parity),
    "mechanism_matched": Source(
        "mechanism_matched", CRIT / "e03_mechanism_matched_scale_448.csv",
        ("f", "median_abs_gap_matched_x", "median_abs_gap_matched_sigma"),
        "11 rows, one per f. The matched-axis residual that adjudicates §3.7; the "
        "correlation half of that test is confounded and must not be plotted.",
        _mechanism_matched, _ph_mechanism_matched),
    "f_extension": Source(
        "f_extension", CRIT / "item2_f_extension_scale_448.parquet",
        ("variant", "f", "spectral_radius", "task", "mean_state", "mean_curvature", "mc"),
        "item2 (connectome, ER) and item3 (permuted, degree) concatenated: the same "
        "grid, four variants, sigma to 11.2. Use this file's own bulk95 when reindexing.",
        _f_extension, _ph_f_extension),
    "jacobian": Source(
        "jacobian", CRIT / "e01_jacobian_scale_448.parquet",
        ("variant", "f", "spectral_radius", "mean_curvature", "vpt", "lambda_min_J"),
        "no row filter; 38,280 Lorenz cells = 4 variants x 11 f x 29 sigma x 10 seeds "
        "x 3 draws. The cell count TIER0 §3.10 quotes.",
        _jacobian, _ph_jacobian),
    "frontier": Source(
        "frontier", CRIT / "e03_frontier_scale_448.parquet",
        ("variant", "f", "spectral_radius", "median", "q25", "q75", "metric"),
        "metric in {mc, vpt}; seed medians. Figures read MC at sigma = 6 and VPT at "
        "sigma = 2, and must attach the sigma to any statement about either.",
        _frontier, _ph_frontier),
    "frontier_paired": Source(
        "frontier_paired", CRIT / "e03_frontier_paired_scale_448.csv",
        ("metric", "spectral_radius", "f", "null", "mean_diff", "ci_lo", "ci_hi"),
        "132 rows. Paired within seed, so this is the source for any connectome-minus-"
        "null statement; do not difference the frontier medians by hand.",
        _frontier_paired, _ph_frontier_paired),
    "collapse_loci": Source(
        "collapse_loci", CRIT / "item2_collapse_loci_scale_448.csv",
        ("f", "variant", "frac_collapsed", "n_seeds_collapsed", "n_seeds"),
        "22 rows. n_seeds_collapsed / n_seeds is the quotable unit; the three draws of "
        "a seed are duplicates at f = 0, so never quote replicates.",
        _collapse_loci, _ph_collapse_loci),
    "threshold_invariance": Source(
        "threshold_invariance", CRIT / "e01_threshold_invariance_scale_448.csv",
        ("scope", "criterion", "n", "median", "iqr", "cv"),
        "scope == 'f > 0' is the scope TIER0 §3.10's CV table reports (0.667 / 0.746 / "
        "0.209). The 'all f' scope gives 0.789 / 0.758 / 0.268 and is a different claim.",
        _threshold_invariance, _ph_threshold_invariance),
    "threshold_table": Source(
        "threshold_table", CRIT / "e01_threshold_table_scale_448.csv",
        ("variant", "f", "effective_radius_lo", "effective_radius_hi"),
        "44 rows, one per (variant, f). The bracket is [lo, hi] around the transition.",
        _threshold_table, _ph_threshold_table),
    "boundaries": Source(
        "boundaries", CRIT / "e02_heatmap_boundaries_extension.csv",
        ("panel", "x", "f_star", "f_star_level_on_subrange", "f_star_level_raw_max", "axis"),
        "both axis files concatenated with an 'axis' column; 121 x-points per (panel, "
        "axis). panel == 'dD' is the memory boundary, 'dStraight' the generative one. "
        "Use f_star (level over fully covered cells); f_star is NaN where no contour "
        "exists, so break the line rather than interpolate.",
        _boundaries_both, _ph_boundaries_both),
    "coverage": Source(
        "coverage", CRIT / "e02_heatmap_coverage_extension.csv",
        ("f", "x_lo", "x_hi", "sigma_max"),
        "11 rows, one per f. x_hi is the extent all 30 replicates reach on the matched "
        "axis; min over f is 3.58. Applies to the effective axis only.",
        _coverage, _ph_coverage),
    "perron_yeo": Source(
        "perron_yeo", _REPO_ROOT / "data/human/Suarez2021_Data",
        ("network", "n_nodes", "perron_mass", "mass_per_node"),
        "COMPUTED LIVE, not frozen: leading eigenvector of the N=448 consensus x the "
        "release RSN labels, restricted to cortical nodes. One eigh, no reservoir run.",
        _perron_yeo, _ph_perron_yeo),
}


class Context:
    """What a figure builder sees: named frames, real or placeholder, never a path."""

    def __init__(self, placeholder: bool = False):
        self.placeholder = placeholder
        self._cache: dict = {}

    def frame(self, name: str) -> pd.DataFrame:
        if name not in self._cache:
            source = SOURCES[name]
            self._cache[name] = (source.placeholder() if self.placeholder
                                 else source.load()).copy()
        return self._cache[name].copy()


def verify() -> pd.DataFrame:
    """Existence report over every registered source. Read before an act session."""
    return pd.DataFrame([
        dict(source=s.name, exists=s.exists(), path=str(s.path.relative_to(_REPO_ROOT)),
             filter=s.filter_note)
        for s in SOURCES.values()])

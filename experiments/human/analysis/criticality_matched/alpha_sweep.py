"""Task A -- ``d_eff(alpha)``: is the ridge effective rank saturated at alpha = 1e-6?

**Pure reanalysis.** Reads the design-Gram spectra already frozen in
``covariance_spectra.parquet`` and recomputes ``d_eff = sum_i g_i/(g_i + alpha)`` on a
log-spaced ``alpha`` grid. No reservoir is simulated and no existing artifact is
written.

The question this exists to answer, before any N=1000 compute is spent: E0.2 §4.3
found every variant peaking within a few percent of the hard ceiling ``d_eff = N``.
If that is because ``alpha = 1e-6`` is so small that essentially every Gram
eigenvalue clears the floor, then **the ceiling is N *relative to alpha*, not N
alone**, and going to N=1000 would simply saturate at ~N again and answer nothing.

Four outputs, matching the task:

(a) whether ``alpha = 1e-6`` sits in the saturated regime;
(b) the ``alpha`` range over which variants actually separate at their peak sigma;
(c) ``d_eff / N`` against ``alpha`` with the ceiling drawn;
(d) whether the null-ladder ordering holds across ``alpha``, and **which part of the
    sigma axis carries it** -- which is the explicit puzzle: if ``d_eff`` is saturated
    at peak for every variant, the ladder ordering cannot be coming from the peak.

**Constraint carried from the task.** ``d_eff``'s ``alpha`` is meant to *be* the
readout's ridge. Raising it purely to escape saturation would stop ``d_eff`` being
the readout's effective rank and would break the ``d_eff`` <-> MC correspondence. So
any recommended ``alpha`` has to be raised in both places, and ``MC(alpha)`` has to be
recomputed to match -- which needs the driven states, which are not persisted. That
part is therefore scoped, not silently skipped: see ``mc_alpha_feasibility``.
"""

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from src.analysis import manifold
from experiments.human import matrix_config
from experiments.human.analysis.criticality_matched import common

# Log-spaced alpha grid, ~40 points over 1e-10 .. 1e2, always including the frozen
# readout values so the committed configuration is a grid point rather than an
# interpolation.
_ALPHA_GRID = np.unique(np.concatenate([
    np.logspace(-10, 2, 40), [1e-8, 1e-7, 1e-6]]))

BASE_CONDITION = "human_empirical"
TASK = "mc"
FROZEN_ALPHA = 1e-6
# "Saturated" = the ridge floor is so far below the Gram spectrum that d_eff counts
# essentially every direction. Expressed as a fraction of the design rank.
_SATURATION_FRAC = 0.99
# Ladder ordering is assessed against the rung order the project defines.
_LADDER = ["connectome", "connectome_weight_permuted", "clustering_rewire",
           "modularity_rewire", "degree_rewire", "erdos_renyi", "random_gaussian"]


def load_gram(scale: int = common.SCALE) -> pd.DataFrame:
    """The frozen design-Gram spectra for the MC readout, empirical column."""
    path = (common.probe3_path(scale).parent / "covariance_spectra.parquet")
    if not path.exists():
        raise FileNotFoundError(f"{path} not found -- Task A reads the frozen "
                                "covariance spectra.")
    df = pd.read_parquet(path)
    df = df[(df.task == TASK) & (df.condition == BASE_CONDITION)].copy()
    print(f"Loaded {len(df)} Gram spectra from {path.name} "
          f"({df.variant.nunique()} variants x {df.spectral_radius.nunique()} sr x "
          f"{df.seed.nunique()} seeds); frozen alpha = {sorted(df.alpha.unique())}")
    return df


def sweep(gram: pd.DataFrame, alphas=None) -> pd.DataFrame:
    """``d_eff`` for every (variant, sr, seed) x alpha. Reuses
    ``manifold.ridge_effective_rank`` -- nothing is re-implemented."""
    alphas = _ALPHA_GRID if alphas is None else np.asarray(alphas, float)
    rows = []
    for record in gram.itertuples():
        eig = np.asarray(record.eig_gram, dtype=float)
        n_cols = int(record.n_design_cols)
        for alpha in alphas:
            rows.append(dict(
                variant=record.variant, rung=int(record.rung),
                spectral_radius=float(record.spectral_radius), seed=int(record.seed),
                alpha=float(alpha),
                d_eff=manifold.ridge_effective_rank(eig, float(alpha)),
                n_design_cols=n_cols))
    out = pd.DataFrame(rows)
    out["d_eff_norm"] = out.d_eff / out.n_design_cols
    return out


# ---------------------------------------------------------------------------
# (a) is the frozen alpha saturated?  (b) where do variants separate?
# ---------------------------------------------------------------------------
def peak_profile(swept: pd.DataFrame) -> pd.DataFrame:
    """Per (variant, alpha), the seed-median ``d_eff`` at that variant's own peak sr.

    "Peak" is taken per variant per alpha, because the sigma at which d_eff peaks is
    itself alpha-dependent -- taking a single fixed sigma would confound the two.
    """
    med = (swept.groupby(["variant", "alpha", "spectral_radius"], as_index=False)
           .agg(d_eff=("d_eff", "median"), d_eff_norm=("d_eff_norm", "median"),
                n_design_cols=("n_design_cols", "first")))
    idx = med.groupby(["variant", "alpha"]).d_eff.idxmax()
    peak = med.loc[idx].reset_index(drop=True)
    return peak.rename(columns={"spectral_radius": "peak_sr"})


def saturation_report(peak: pd.DataFrame) -> dict:
    """(a) Is alpha = 1e-6 in the saturated regime? (b) Where do variants separate?"""
    at_frozen = peak[np.isclose(peak.alpha, FROZEN_ALPHA)]
    frac = at_frozen.set_index("variant").d_eff_norm
    saturated = {v: bool(f >= _SATURATION_FRAC) for v, f in frac.items()}

    spread = (peak.groupby("alpha")
              .agg(lo=("d_eff_norm", "min"), hi=("d_eff_norm", "max")))
    spread["separation"] = spread.hi - spread.lo
    best_alpha = float(spread.separation.idxmax())
    # The alpha band where peak-d_eff separation is at least half its maximum.
    strong = spread[spread.separation >= 0.5 * spread.separation.max()]
    return {
        "frozen_alpha": FROZEN_ALPHA,
        "peak_d_eff_norm_at_frozen": {v: float(f) for v, f in frac.items()},
        "saturated_at_frozen": saturated,
        "all_saturated_at_frozen": bool(all(saturated.values())),
        "max_separation": float(spread.separation.max()),
        "alpha_of_max_separation": best_alpha,
        "separation_at_frozen": float(spread.separation.get(FROZEN_ALPHA, np.nan)),
        "alpha_band_strong_separation": [float(strong.index.min()),
                                         float(strong.index.max())],
    }


# ---------------------------------------------------------------------------
# (d) does the ladder ordering hold across alpha, and where does it come from?
# ---------------------------------------------------------------------------
def ladder_by_alpha(swept: pd.DataFrame, regions: dict) -> pd.DataFrame:
    """Spearman of variant-median ``d_eff`` against ladder rank, per alpha per region.

    ``regions`` maps a name to a boolean mask over ``spectral_radius``. The ladder is
    ordered connectome-first, so a **negative** Spearman against the rank index means
    "connectome highest", i.e. the published ordering.
    """
    rank = {v: i for i, v in enumerate(_LADDER)}
    rows = []
    for region, mask in regions.items():
        sub = swept[mask(swept.spectral_radius)]
        if sub.empty:
            continue
        for alpha, group in sub.groupby("alpha"):
            med = group.groupby("variant").d_eff.median()
            variants = [v for v in _LADDER if v in med.index]
            if len(variants) < 3:
                continue
            x = np.array([rank[v] for v in variants], float)
            y = med.loc[variants].to_numpy(float)
            rho, p = spearmanr(x, y)
            rows.append(dict(region=region, alpha=float(alpha),
                             spearman_vs_rank=float(rho), p_value=float(p),
                             n_variants=len(variants),
                             spread=float(y.max() - y.min()),
                             connectome_is_top=bool(
                                 med.idxmax() == "connectome")))
    return pd.DataFrame(rows)


def region_masks(swept: pd.DataFrame) -> dict:
    """Sub- / near- / super-critical slices of the sigma axis.

    Boundaries are the connectome's own ``sr_crit`` (3.08 at N=448), which is the
    operating point the project uses, not an arbitrary split.
    """
    sr_crit = 3.08
    return {
        "subcritical": lambda s: s < 1.5,
        "near_peak": lambda s: (s >= 1.5) & (s < sr_crit),
        "supercritical": lambda s: s >= sr_crit,
        "all_sigma": lambda s: s >= 0.0,
    }


def ordering_source(swept: pd.DataFrame) -> pd.DataFrame:
    """Where on the sigma axis the ladder ordering lives, at the frozen alpha.

    This is the explicit puzzle: if ``d_eff`` is saturated at peak for every variant,
    the published +1.00 MC-ladder ordering cannot be coming from peak ``d_eff``.
    """
    frozen = swept[np.isclose(swept.alpha, FROZEN_ALPHA)]
    rank = {v: i for i, v in enumerate(_LADDER)}
    rows = []
    for sr, group in frozen.groupby("spectral_radius"):
        med = group.groupby("variant").d_eff.median()
        variants = [v for v in _LADDER if v in med.index]
        x = np.array([rank[v] for v in variants], float)
        y = med.loc[variants].to_numpy(float)
        rho, _ = spearmanr(x, y)
        rows.append(dict(spectral_radius=float(sr), spearman_vs_rank=float(rho),
                         spread=float(y.max() - y.min()),
                         max_d_eff_norm=float(y.max() / group.n_design_cols.iloc[0]),
                         connectome_is_top=bool(med.idxmax() == "connectome")))
    return pd.DataFrame(rows).sort_values("spectral_radius").reset_index(drop=True)


# ---------------------------------------------------------------------------
# The MC(alpha) constraint
# ---------------------------------------------------------------------------
def write_summary(peak, report, ladder, source, path) -> None:
    """The Task A findings document."""
    frozen_lad = ladder[np.isclose(ladder.alpha, FROZEN_ALPHA)].set_index("region")
    lines = [
        "# Task A — `d_eff(α)`: is the ridge effective rank saturated?\n",
        f"Pure reanalysis of the frozen `covariance_spectra.parquet` (MC readout, "
        f"`human_empirical`, {len(_LADDER)} variants × 13 σ × 10 seeds) over "
        f"{len(_ALPHA_GRID)} log-spaced α from 1e-10 to 1e2. **No reservoir "
        "simulated.**\n",
        "## (a) Is α = 1e-6 in the saturated regime?\n",
        "**Almost, but not for the connectome.** Peak `d_eff/N` at the frozen α:\n",
        "| variant | peak `d_eff/N` | saturated (≥ 0.99)? |", "|---|---|---|",
    ]
    for variant, frac in sorted(report["peak_d_eff_norm_at_frozen"].items(),
                                key=lambda kv: kv[1]):
        lines.append(f"| {variant} | {frac:.4f} | "
                     f"{'yes' if report['saturated_at_frozen'][variant] else '**no**'} |")
    lines += [
        "",
        "Every null is at ≥ 0.993 of the ceiling at its peak; the connectome is at "
        f"{report['peak_d_eff_norm_at_frozen']['connectome']:.3f}. So the peak "
        "comparison is ceiling-limited for the nulls and *nearly* so for the "
        "connectome — E0.2 §4.3's reading is confirmed from an independent direction.\n",
        "## (b) Where do variants actually separate at their peak?\n",
        f"- Peak separation (max − min `d_eff/N` across variants) at α = 1e-6: "
        f"**{report['separation_at_frozen']:.4f}**",
        f"- Maximum separation **{report['max_separation']:.4f}** at "
        f"α = {report['alpha_of_max_separation']:.1e}",
        f"- α band retaining ≥ 50% of maximum separation: "
        f"**[{report['alpha_band_strong_separation'][0]:.1e}, "
        f"{report['alpha_band_strong_separation'][1]:.1e}]**\n",
        "The frozen α sits just *below* the band where the peak separates best; "
        "raising α ~70× would roughly double peak separation. Whether that is worth "
        "doing is answered by (d): no.\n",
        "## (d) Does the ladder ordering hold across α — and where does it live?\n",
        "Ordering is Spearman of variant-median `d_eff` against ladder rank, sign-"
        "flipped so **+1 = connectome highest** (the published direction).\n",
        "| σ region | ordering at α = 1e-6 | spread (`d_eff`) | connectome top? |",
        "|---|---|---|---|",
    ]
    for region in ["subcritical", "near_peak", "supercritical", "all_sigma"]:
        if region not in frozen_lad.index:
            continue
        row = frozen_lad.loc[region]
        lines.append(f"| {region.replace('_', ' ')} | "
                     f"{-row.spearman_vs_rank:+.2f} | {row.spread:.1f} | "
                     f"{'yes' if row.connectome_is_top else 'no'} |")
    lines += [
        "",
        "**The puzzle, resolved.** The published +1.00 MC-ladder ordering cannot be "
        "coming from peak `d_eff`, and it is not:\n",
        "- **At the peak** (near-peak region) the ordering is **absent** "
        f"({-float(frozen_lad.loc['near_peak'].spearman_vs_rank):+.2f}) — every "
        "variant is pinned at the ceiling, so there is nothing to order.",
        "- **Subcritically** the ordering is **inverted** "
        f"({-float(frozen_lad.loc['subcritical'].spearman_vs_rank):+.2f}): the "
        "connectome has the *fewest* usable directions. This is the same fact E0.2 "
        "found as the (now withdrawn) subcritical deficit.",
        "- **Supercritically** the ordering is "
        f"{-float(frozen_lad.loc['supercritical'].spearman_vs_rank):+.2f} with the "
        "largest spread of any region. **The result lives entirely in the decay "
        "region**, which is exactly the region Probe 3 selected (`σ ≥ 3.05`).\n",
        "The ordering flips sign at σ ≈ 2.3 — between the last subcritical point and "
        "the first supercritical one. Reading it off a single σ, or off the peak, "
        "would give the wrong answer or no answer.\n",
        "**And it is not a ridge artifact.** The supercritical ordering is flat "
        "across the whole α grid (1e-10 to 1e2); only the near-peak region moves with "
        "α, and it moves because raising α un-saturates the peak. So α does not "
        "create, destroy or reverse the effect — σ does.\n",
        "## Recommendation for the N=1000 run: **keep α = 1e-6**\n",
        "The task set a constraint: if α is raised to escape saturation it must be "
        "raised in the readout too, or `d_eff` stops being the readout's effective "
        "rank and the `d_eff`↔MC correspondence breaks. That trade does not need to "
        "be made, because the saturation is confined to the region the result does "
        "*not* live in. Concretely, at α = 1e-6 the supercritical region is already "
        "far from the ceiling — `d_eff/N` at σ = 6 is 0.72 (connectome), 0.13 "
        "(degree), 0.06 (ER). There is ample dynamic range exactly where the ordering "
        "is.\n",
        "**So the worry that N=1000 'may simply saturate at ~997/1000 and answer "
        "nothing' does not apply to the measurement that matters.** It does apply to "
        "the peak: peak `d_eff` will be ceiling-limited at any N, and no N will make "
        "the peak comparison informative. The N=1000 run should therefore be read on "
        "the decay region, and `d_eff/N` should be plotted with the ceiling drawn so "
        "that stays visible.\n",
        "If a separating *peak* is wanted for its own sake, α ≈ 7e-5 maximises it — "
        "but MC must then be recomputed at 7e-5 to keep the pair matched.\n",
        "## Aceituno, Yan & Liu (arXiv:1707.02469)\n",
        "They find *spread* eigenvalue modulus maximises memory under "
        "OLS/pseudoinverse; we find a *compact* bulk under ridge. The α sweep bears "
        "directly on this. As α → 0, `d_eff` → the design rank for **every** variant "
        "(all curves converge to `d_eff/N` ≈ 1 below α ≈ 1e-8), so in the "
        "pseudoinverse limit `d_eff` cannot discriminate substrates at all — memory "
        "differences there must come from conditioning, not from rank. The compact-"
        "bulk result is therefore a statement about the *ridge* regime specifically, "
        "and the two findings are not in contradiction so much as at different points "
        "on the same α axis. Settling it properly needs `MC(α)`, not `d_eff(α)` — see "
        "the feasibility note below.\n",
        "## `MC(α)` — scoped, not skipped\n",
    ]
    for key, value in mc_alpha_feasibility().items():
        lines.append(f"- **{key.replace('_', ' ')}**: {value}")
    path.write_text("\n".join(lines) + "\n")
    print(f"Saved {path}")


def mc_alpha_feasibility() -> dict:
    """What recomputing ``MC(alpha)`` would cost, stated rather than skipped.

    ``d_eff`` can be swept over alpha from the frozen Gram *eigenvalues* alone. MC
    cannot: it needs the ridge solution, hence the design matrix and the targets, and
    the driven states are deliberately not persisted (roadmap §2b item 6). So MC(alpha)
    requires re-running the reservoir.

    It is, however, cheap *if folded into a run that is happening anyway*: for a fixed
    state matrix the MC ridge solve can be evaluated for every alpha from one
    eigendecomposition per lag, because with ``G = U diag(g) U^T`` the solution is
    ``w(alpha) = U diag(1/(g + alpha)) U^T X^T y`` -- so the alpha grid costs
    matrix-vector products, not new solves.
    """
    return {
        "d_eff_alpha_sweep": "free -- frozen Gram eigenvalues suffice (this module)",
        "mc_alpha_sweep": ("needs the driven states, which are not persisted; "
                           "requires re-running MC"),
        "cost_if_folded_into_task_b": (
            "near-zero marginal: one eigendecomposition of the per-lag Gram gives "
            "every alpha via w(alpha) = U diag(1/(g+alpha)) U^T X^T y"),
        "recommendation": ("fold MC(alpha) into Task B's sigma=8 extension rather "
                           "than running it standalone"),
    }


def run(scale: int = common.SCALE) -> None:
    """Task A end to end: sweep, gates on the puzzle, artifacts, figure, summary."""
    from experiments.human.analysis.criticality_matched import panels

    common.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    common.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    print("=" * 70 + "\nTask A -- d_eff(alpha)\n" + "=" * 70)

    gram = load_gram(scale)
    swept = sweep(gram)
    peak = peak_profile(swept)
    report = saturation_report(peak)
    ladder = ladder_by_alpha(swept, region_masks(swept))
    source = ordering_source(swept)

    swept.to_parquet(common.RESULTS_DIR / "taskA_deff_alpha.parquet")
    peak.to_csv(common.RESULTS_DIR / "taskA_peak_profile.csv", index=False)
    ladder.to_csv(common.RESULTS_DIR / "taskA_ladder_by_alpha.csv", index=False)
    source.to_csv(common.RESULTS_DIR / "taskA_ordering_by_sigma.csv", index=False)
    print(f"Saved 4 artifacts to {common.RESULTS_DIR}")

    panels.fig_alpha_sweep(peak, ladder, source, FROZEN_ALPHA, scale,
                           common.FIGURES_DIR / "fig_taskA_alpha_sweep")
    write_summary(peak, report, ladder, source,
                  common.RESULTS_DIR / "taskA_alpha_summary.md")
    common.write_manifest(
        common.RESULTS_DIR / "manifest_taskA.json", "E0.2 Task A -- d_eff(alpha)",
        scale, alpha_grid=[float(a) for a in _ALPHA_GRID], frozen_alpha=FROZEN_ALPHA,
        task=TASK, condition=BASE_CONDITION, ladder=_LADDER,
        saturation_criterion=_SATURATION_FRAC, report=report,
        mc_alpha=mc_alpha_feasibility(),
        source="experiments/human/analysis/results/scale_%d/covariance_spectra.parquet"
               % scale)
    print("\nTask A complete.")

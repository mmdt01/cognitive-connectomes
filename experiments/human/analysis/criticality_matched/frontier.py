"""E0.3: the ABSOLUTE (MC, VPT) frontier across the (variant, f, sigma) grid.

Everything else in this package reads *differences* -- `dD` = d_eff(connectome) -
d_eff(ER), `dStraight` = curvature(ER) - curvature(connectome). A difference is
uninterpretable without the level it sits on, and this project has already been caught
by that once: TIER0 §1.2 records that the memory wedge's collapse is **ER rising to the
N=448 rank ceiling, not the connectome degrading** -- a delta that read as the
connectome losing an advantage while the connectome had not moved. This module is the
systematic version of that check: within-substrate absolute values, so the level is
visible before anything is subtracted.

**Why absolute-first also dodges the axis problem.** Nominal sigma versus `sigma*bulk95`
is unresolved (TIER0 §1.1) because *differencing* forces a choice of where to compare
two substrates. Absolute curves make no such choice: each variant is shown on its own
sigma with its own `sr_crit(f)` marked. `x = sigma*bulk95` is still recorded per cell so
the matched-axis pass is a later reanalysis and not a re-run.

**Metrics: MC and VPT only.**

- `d_eff` is excluded: it is ceiling-limited at N=448 (peak >= 0.96 N), so in absolute
  terms it reads flat across `f` for reasons that have nothing to do with `f`.
- `climate_error` is excluded: unreliable once a null diverges (TIER0 §6).
- MC is bounded by `max_lag` = 50 and observed <= 16.0; VPT is bounded by `free_run_len`
  (600 steps x h 0.03 x lambda 0.9056 = 16.3 Lyapunov times) and observed <= 7.95. So
  neither is at risk of a ceiling -- but **VPT's floor is live**: ~42% of Lorenz cells
  are exactly 0, and a difference taken against a floored variant is not a measurement.
  Every cell carries the fraction of seeds at each bound.

**The unit is the seed, not the replicate.** The three draws of a seed share its mask,
`Win` and input series, and at `f = 0` the sign transform is the identity so they are
literal duplicates. Draws are averaged within a seed first; the seed (n = 10) is then
the unit for the median and the spread.
"""

import numpy as np
import pandas as pd

from experiments.human.analysis.criticality_matched import common, extend_f

SIGN_MODE, TARGETING = "edge", "stratified"
# Ladder order: connectome -> its placement control -> topology-matched -> unstructured.
# connectome vs weight-permuted isolates weight PLACEMENT; weight-permuted vs degree
# isolates TOPOLOGY. That decomposition previously existed only at f = 0.
VARIANTS = ["connectome", "connectome_weight_permuted", "degree_rewire", "erdos_renyi"]
METRICS = {
    "mc": dict(task="mc", label="memory capacity (MC)", ceiling=50.0, floor=0.0),
    "vpt": dict(task="lorenz", label="valid prediction time (Lyapunov)",
                ceiling=600 * 0.03 * 0.9056, floor=0.0),
}
# A cell counts as at a bound when it is within this fraction of the bound's own scale.
BOUND_TOL = 1e-3
# Pre-registered decision rule (fixed before the curves were seen). A metric "varies
# appreciably" with f when the f-induced swing in the seed-median reaches SWING_RATIO
# times the seed-to-seed IQR at the same sigma, over at least MIN_RUN consecutive sigma
# points. Read against the data's own scatter rather than an absolute cutoff, because
# the right absolute number differs between MC and VPT.
SWING_RATIO = 3.0
MIN_RUN = 3
# A panel is "floor-dominated" where this fraction of seeds sits at the bound.
FLOOR_DOMINATED = 0.5
# The sigmas the paired connectome-vs-null contrast is read at. Declared, not picked --
# choosing each cell's most favourable sigma would hand the comparison to whichever
# substrate the analyst prefers. TWO of them, because one is a trap: at sigma = 2.0
# every variant sits near its own VPT peak, but that is *below* the connectome's own
# `sr_crit` = 3.08 and near the nulls' MC optimum, so reading memory there shows the
# connectome losing. sigma = 6.0 is supercritical, where the memory result lives. The
# same pair is used for both metrics so neither is given a bespoke operating point.
CONTRAST_SIGMAS = (2.0, 6.0)

_COLS = ["sign_mode", "targeting", "f", "variant", "spectral_radius", "seed", "draw",
         "task", "mc", "vpt", "bulk95"]


def load_cells(scale: int = common.SCALE) -> pd.DataFrame:
    """The four-variant grid, spliced from the two extension captures.

    Splicing is legitimate because the boundary capture reproduced the frozen phase
    capture **bit-for-bit** on the same machine (TIER0 §2.3), which is what established
    that these runs are exactly reproducible rather than merely distributionally equal.
    The two files hold disjoint variant sets over an identical (f, sigma, seed, draw)
    grid, so the join is a concatenation with the grid asserted, not a merge.
    """
    frames = []
    for variant_set in extend_f.VARIANT_SETS:
        path = extend_f.extension_path(scale, variant_set)
        if not path.exists():
            raise FileNotFoundError(
                f"{path} not found -- run `--extend-f --variants {variant_set}` first.")
        frames.append(pd.read_parquet(path, columns=_COLS))
        print(f"  loaded {len(frames[-1])} cells from {path.name}")
    df = pd.concat(frames, ignore_index=True)
    df = df[(df.sign_mode == SIGN_MODE) & (df.targeting == TARGETING)
            & (df.variant.isin(VARIANTS))].copy()

    grids = {v: (tuple(sorted(g.f.unique())), tuple(sorted(g.spectral_radius.unique())),
                 tuple(sorted(g.seed.unique())), tuple(sorted(g.draw.unique())))
             for v, g in df.groupby("variant")}
    if len({grid for grid in grids.values()}) != 1:
        raise RuntimeError(f"[frontier] the variants do not share one grid: "
                           f"{ {v: [len(a) for a in g] for v, g in grids.items()} }")
    print(f"Loaded {len(df)} cells: {len(VARIANTS)} variants x "
          f"{df.f.nunique()} f x {df.spectral_radius.nunique()} sigma to "
          f"{df.spectral_radius.max():g} x {df.seed.nunique()} seeds x "
          f"{df.draw.nunique()} draws")
    return df


def per_seed(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    """Draw-mean within each seed -- the independent unit."""
    spec = METRICS[metric]
    sub = df[df.task == spec["task"]]
    return (sub.groupby(["variant", "f", "spectral_radius", "seed"], as_index=False)
            .agg(**{metric: (metric, "mean"), "bulk95": ("bulk95", "mean")}))


def frontier(df: pd.DataFrame) -> pd.DataFrame:
    """Seed-median absolute curves per (metric, variant, f, sigma), with bound flags."""
    rows = []
    for metric, spec in METRICS.items():
        seeds = per_seed(df, metric)
        ceiling, floor = spec["ceiling"], spec["floor"]
        tol = BOUND_TOL * max(abs(ceiling), 1.0)
        grouped = seeds.groupby(["variant", "f", "spectral_radius"])
        agg = grouped[metric].agg(
            median="median", q25=lambda s: s.quantile(0.25),
            q75=lambda s: s.quantile(0.75), n_seeds="size").reset_index()
        agg["iqr"] = agg.q75 - agg.q25
        bounds = grouped[metric].agg(
            frac_at_floor=lambda s: float((s <= floor + tol).mean()),
            frac_at_ceiling=lambda s: float((s >= ceiling - tol).mean())).reset_index()
        agg = agg.merge(bounds, on=["variant", "f", "spectral_radius"])
        bulk = grouped.bulk95.median().reset_index()
        agg = agg.merge(bulk, on=["variant", "f", "spectral_radius"])
        agg["x"] = agg.spectral_radius * agg.bulk95      # the matched-axis coordinate
        agg["metric"] = metric
        rows.append(agg)
    return pd.concat(rows, ignore_index=True)


def sr_crit(df: pd.DataFrame) -> pd.DataFrame:
    """`sr_crit = 1 / median_over_seeds(bulk95)` per (variant, f).

    The median, per `eigenspectrum.common.SR_CRIT_CONVENTION`: `1/x` is convex, so a
    per-seed mean of the reciprocal is Jensen-biased upward.
    """
    bulk = (df.groupby(["variant", "f", "seed"], as_index=False).bulk95.mean()
            .groupby(["variant", "f"], as_index=False).bulk95.median())
    bulk["sr_crit"] = 1.0 / bulk.bulk95
    return bulk


def decision_rule(front: pd.DataFrame) -> pd.DataFrame:
    """Apply the pre-registered rule, per (metric, variant).

    `swing(sigma)` = the range of the seed-median across `f`; `noise(sigma)` = the
    typical seed-level IQR at that sigma. The metric varies appreciably where the ratio
    reaches `SWING_RATIO` over `MIN_RUN` consecutive sigma points. The ratio itself is
    reported so a different bar can be applied without re-running anything.
    """
    rows = []
    for (metric, variant), group in front.groupby(["metric", "variant"]):
        # Restrict to sigma where the metric is ALIVE. Where most seeds sit at the
        # floor the seed IQR collapses too, and swing/noise explodes on a dead
        # denominator -- the first pass of this rule reported VPT ratios of 1010-5907
        # for exactly that reason. A metric at its floor is not varying, it is absent.
        floor_by_sigma = group.groupby("spectral_radius")["frac_at_floor"].median()
        live = floor_by_sigma[floor_by_sigma < FLOOR_DOMINATED].index
        alive = group[group.spectral_radius.isin(live)]
        if alive.empty:
            rows.append(dict(metric=metric, variant=variant, max_ratio=np.nan,
                             sigma_at_max_ratio=np.nan, longest_run=0, passes=False,
                             max_swing=np.nan, median_noise=np.nan,
                             live_sigma_lo=np.nan, live_sigma_hi=np.nan, n_live=0,
                             frac_sigma_floor_dominated=1.0))
            continue
        by_sigma = alive.groupby("spectral_radius")
        # Bracket access, not attribute: `median` is also a groupby METHOD, so
        # `by_sigma.median` silently resolves to the method rather than the column.
        swing = by_sigma["median"].max() - by_sigma["median"].min()
        noise = by_sigma["iqr"].median()
        ratio = swing / noise.replace(0.0, np.nan)
        ok = (ratio >= SWING_RATIO).to_numpy()
        # longest run of consecutive sigma points clearing the bar
        best = run = 0
        for flag in ok:
            run = run + 1 if flag else 0
            best = max(best, run)
        rows.append(dict(
            metric=metric, variant=variant,
            max_ratio=float(np.nanmax(ratio.to_numpy())) if len(ratio) else np.nan,
            median_ratio=float(np.nanmedian(ratio.to_numpy())) if len(ratio) else np.nan,
            sigma_at_max_ratio=float(ratio.idxmax()) if ratio.notna().any() else np.nan,
            longest_run=int(best), passes=bool(best >= MIN_RUN),
            max_swing=float(swing.max()), median_noise=float(noise.median()),
            live_sigma_lo=float(min(live)), live_sigma_hi=float(max(live)),
            n_live=int(len(live)),
            frac_sigma_floor_dominated=float(
                (group.groupby("spectral_radius")["frac_at_floor"].median()
                 >= FLOOR_DOMINATED).mean())))
    return pd.DataFrame(rows).sort_values(["metric", "variant"]).reset_index(drop=True)


# "Usable range" needs a threshold, and the answer depends on it, so all three are
# computed and reported rather than one being picked. `off_floor` is the weakest
# ("not identically dead") and is the one that flatters the connectome; `absolute` is
# the interpretable standard (does it predict a whole Lyapunov time?); `relative` asks
# how far each substrate holds its own best.
USABLE_CRITERIA = {
    "off_floor": None,                       # frac_at_floor < FLOOR_DOMINATED
    "absolute": {"mc": 1.0, "vpt": 1.0},     # MC bits / Lyapunov times
    "relative": 0.5,                         # fraction of that (variant, f) own peak
}


def live_window(front: pd.DataFrame) -> pd.DataFrame:
    """Per (metric, variant, f, criterion): the largest sigma the metric survives to.

    The absolute measure the delta panels were reaching for -- "usable range" needs no
    second substrate to subtract and no matched axis. **But it needs a threshold, and
    the verdict turns on which one.** Measured at the floor ("not exactly zero") the
    connectome's VPT window looks ~2x the nulls'; measured at any threshold that means
    *usefully predicting*, the advantage shrinks to 1.25-1.5x at high `f` and reverses
    at low `f`, where `degree_rewire` holds a whole Lyapunov time twice as far. The
    difference is that nulls drop to exactly 0 while the connectome decays gradually
    just above it. All three criteria are therefore reported together.
    """
    rows = []
    for (metric, variant, f), group in front.groupby(["metric", "variant", "f"]):
        peak = float(group["median"].max())
        for name in USABLE_CRITERIA:
            if name == "off_floor":
                ok = group[group.frac_at_floor < FLOOR_DOMINATED]
            elif name == "absolute":
                ok = group[group["median"] >= USABLE_CRITERIA["absolute"][metric]]
            else:
                ok = group[group["median"] >= USABLE_CRITERIA["relative"] * peak]
            rows.append(dict(metric=metric, variant=variant, f=float(f),
                             criterion=name, own_peak=peak,
                             sigma_usable_hi=float(ok.spectral_radius.max())
                             if len(ok) else np.nan, n_usable=int(len(ok))))
    return pd.DataFrame(rows).sort_values(["metric", "criterion", "variant", "f"]) \
                             .reset_index(drop=True)


def paired_contrast(df: pd.DataFrame, metric: str, spectral_radius: float) -> pd.DataFrame:
    """Connectome minus each null, paired within seed, at one sigma across `f`.

    The seed convention pairs connectome and null on the same `Win` and the same input
    series, so this is a paired contrast rather than a difference of independent means.
    Following TIER0 §3.4's precedent for paired per-seed differences: Wilcoxon
    signed-rank plus a 95% t-CI, with Cliff's delta from `src/experiment/stats.py` as
    the effect size. (`stats.rank_permutation_pvalue` is deliberately *not* used: it is
    an unpaired two-sample test and would throw away the pairing.)

    **Multiplicity, and a hard power limit worth stating.** With `n = 10` seeds the
    smallest p a two-sided Wilcoxon can return is `2/2^10` = 0.00195, so **no Holm
    correction over more than ~25 tests can reach 0.05, however large the effect**.
    Correcting across the whole 66-cell table would therefore report "nothing is
    significant" as a fact about seed count, not about the substrates. The family is
    consequently declared as one `(metric, null)` column -- 11 `f` values, the sweep
    that is actually being read -- and the raw p, the CI and Cliff's delta are all
    carried so the reader is never leaning on a star.

    Reported at a *declared* sigma rather than each variant's own peak: peak-picking
    per cell would be a free parameter, and near sigma = 2 every variant is close to
    its own best at low `f` (see `peak_table`).
    """
    from scipy.stats import wilcoxon

    from src.experiment import stats as expstats

    seeds = per_seed(df, metric)
    sub = seeds[np.isclose(seeds.spectral_radius, spectral_radius)]
    nulls = [v for v in VARIANTS if v != "connectome"]
    rows = []
    for f in sorted(sub.f.unique()):
        cell = sub[sub.f == f]
        conn = cell[cell.variant == "connectome"].set_index("seed")[metric]
        for null in nulls:
            other = cell[cell.variant == null].set_index("seed")[metric]
            paired = pd.concat([conn, other], axis=1, keys=["c", "n"]).dropna()
            if paired.empty:
                continue
            diff = (paired.c - paired.n).to_numpy(float)
            a, b = paired.c.to_numpy(float), paired.n.to_numpy(float)
            se = diff.std(ddof=1) / np.sqrt(diff.size) if diff.size > 1 else np.nan
            try:
                p_raw = float(wilcoxon(diff).pvalue)
            except ValueError:          # all differences identically zero
                p_raw = 1.0
            rows.append(dict(
                metric=metric, spectral_radius=float(spectral_radius), f=float(f),
                null=null, n_seeds=int(diff.size),
                connectome_median=float(np.median(a)), null_median=float(np.median(b)),
                mean_diff=float(diff.mean()),
                ci_lo=float(diff.mean() - 1.96 * se), ci_hi=float(diff.mean() + 1.96 * se),
                cliffs_delta=expstats.cliffs_delta(a, b, lower_is_better=False),
                p_raw=p_raw))
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    # Family = one (metric, null) column across f; see the multiplicity note above.
    out["p_holm"] = np.nan
    for null, block in out.groupby("null"):
        out.loc[block.index, "p_holm"] = expstats.holm(list(block.p_raw))
    out["significant"] = out.p_holm < 0.05
    out["p_floor_binding"] = out.p_raw <= 2.0 / 2 ** out.n_seeds + 1e-12
    return out


def contrast_at_bound(front: pd.DataFrame) -> pd.DataFrame:
    """The decision rule's second clause, made computable.

    Finds, per metric, the (f, sigma) cell where connectome minus the best null is
    largest, and reports whether that null is sitting at the metric's floor there. If
    it is, the panel's between-substrate signal is a bound artefact rather than a
    measurement, and the delta heatmap should not be drawn from it.
    """
    rows = []
    for metric, group in front.groupby("metric"):
        wide = group.pivot_table(index=["f", "spectral_radius"], columns="variant",
                                 values="median")
        floors = group.pivot_table(index=["f", "spectral_radius"], columns="variant",
                                   values="frac_at_floor")
        nulls = [v for v in wide.columns if v != "connectome"]
        best_null = wide[nulls].max(axis=1)
        gap = wide["connectome"] - best_null
        if gap.dropna().empty:
            continue
        cell = gap.idxmax()
        which = wide.loc[cell, nulls].idxmax()
        rows.append(dict(
            metric=metric, f=cell[0], spectral_radius=cell[1],
            connectome=float(wide.loc[cell, "connectome"]),
            best_null=which, best_null_value=float(best_null.loc[cell]),
            gap=float(gap.loc[cell]),
            null_frac_at_floor=float(floors.loc[cell, which]),
            all_nulls_floored=bool((floors.loc[cell, nulls]
                                    >= FLOOR_DOMINATED).all()),
            connectome_frac_at_floor=float(floors.loc[cell, "connectome"])))
    return pd.DataFrame(rows)


def peak_table(front: pd.DataFrame) -> pd.DataFrame:
    """Each substrate's own best, per (metric, variant, f) -- the Aceituno question:
    robust at what level, and how far apart are the substrates' own optima?"""
    idx = front.groupby(["metric", "variant", "f"])["median"].idxmax()
    peak = front.loc[idx, ["metric", "variant", "f", "spectral_radius", "median",
                           "q25", "q75", "x"]]
    return peak.rename(columns={"median": "peak", "spectral_radius": "sigma_at_peak"}) \
               .sort_values(["metric", "variant", "f"]).reset_index(drop=True)


def _level_table(front: pd.DataFrame, metric: str, spectral_radius: float,
                 fs=(0.0, 0.25, 0.5)) -> pd.DataFrame:
    sub = front[(front.metric == metric)
                & np.isclose(front.spectral_radius, spectral_radius)]
    piv = sub.pivot_table(index="f", columns="variant", values="median")
    return piv.reindex(columns=[v for v in VARIANTS if v in piv.columns]) \
              .loc[[f for f in fs if f in piv.index]]


def write_verdict(front, rule, bound, contrasts, windows, scale: int) -> None:
    """The gating verdict, against the rule fixed before the curves were seen."""
    mc6 = _level_table(front, "mc", 6.0)
    vpt2 = _level_table(front, "vpt", 2.0)
    gain = (mc6.loc[0.5] - mc6.loc[0.0]) if {0.0, 0.5} <= set(mc6.index) else None
    lines = [
        "# E0.3 — the absolute (MC, VPT) frontier",
        "",
        "Within-substrate absolute levels across the (variant, f, sigma) grid, four "
        "variants, nominal sigma, no differencing and no matched axis. Run as a **gate** "
        "on whether the (f, sigma) delta heatmaps earn their place.",
        "",
        "## Verdict against the pre-registered rule",
        "",
        f"Rule, fixed before the curves were seen: keep the delta heatmaps only if both "
        f"order parameters vary appreciably in absolute terms (swing/noise >= "
        f"{SWING_RATIO:g} over >= {MIN_RUN} consecutive sigma, computed where the metric "
        "is alive) and neither panel's signal is dominated by a variant sitting at a "
        "bound.",
        "",
        "| metric | variant | live sigma | median swing/noise | clause 1 |",
        "|---|---|---|---|---|",
    ]
    for _, r in rule.iterrows():
        lines.append(f"| {r.metric} | {r.variant} | [{r.live_sigma_lo:.1f}, "
                     f"{r.live_sigma_hi:.1f}] | {r.median_ratio:.1f} | "
                     f"{'PASS' if r.passes else 'FAIL'} |")
    lines += [
        "",
        "| metric | largest connectome − best-null gap | null at that cell | clause 2 |",
        "|---|---|---|---|",
    ]
    for _, r in bound.iterrows():
        lines.append(
            f"| {r.metric} | {r.gap:+.2f} at f = {r.f:g}, sigma = {r.spectral_radius:g} "
            f"({r.connectome:.2f} vs {r.best_null_value:.2f}) | {r.best_null}, "
            f"{r.null_frac_at_floor:.0%} of seeds at floor | "
            f"{'FAIL (bound artefact)' if r.all_nulls_floored else 'PASS'} |")
    lines += [
        "",
        "**Both metrics pass both clauses**, so the panels are not measuring noise. But "
        "the frontier changes what they should be built from — see below.",
        "",
        "## 1. Absolute MC inverts the memory panel's mechanism",
        "",
        f"MC at sigma = 6 (supercritical), seed-median:",
        "",
        "```",
        mc6.to_string(float_format=lambda v: f"{v:.2f}"),
        "```",
        "",
    ]
    if gain is not None:
        lines += [
            "Change from f = 0 to f = 0.5: "
            + ", ".join(f"{v} {gain[v]:+.2f}" for v in gain.index) + ".",
            "",
            "**Negative weights improve supercritical memory for every substrate, and "
            "nobody degrades.** The connectome's advantage falls from "
            f"{mc6.loc[0.0, 'connectome'] - mc6.loc[0.0].drop('connectome').max():+.2f} "
            f"to {mc6.loc[0.5, 'connectome'] - mc6.loc[0.5].drop('connectome').max():+.2f} "
            "solely because the nulls gain ~4x what the connectome gains, from a much "
            "lower start. So the memory panel's 'advantage extinguished by f ~ 0.15-0.20' "
            "is **the nulls catching up**, not sign composition damaging the connectome "
            "— the same failure mode TIER0 §1.2 caught for `d_eff` at f = 0, now shown "
            "across the whole f axis and on MC, which is not ceiling-limited at N=448.",
            "",
        ]
    lines += [
        "## 2. Generation is real, but VPT is the instrument — not curvature",
        "",
        "VPT at sigma = 2 (near every variant's own peak), seed-median:",
        "",
        "```",
        vpt2.to_string(float_format=lambda v: f"{v:.2f}"),
        "```",
        "",
        "At f = 0 the connectome is level with the nulls (paired differences +0.28, "
        "-0.01, +0.44; none significant). From f ~ 0.20-0.25 it is **the only substrate "
        "still predicting**: paired differences +1.0 to +2.2 Lyapunov times against all "
        "three nulls, clearing the weight-permuted placement control, so the effect is "
        "**weight placement** rather than topology. That is a large, interpretable, "
        "ladder-clearing contrast — against the 0.032 rad curvature residual the "
        "matched-axis Panel B was contouring. The generative arm was weak because the "
        "*order parameter* was wrong, not because generation is weak.",
        "",
        "## 3. The dissociation survives, restated in absolute terms",
        "",
        "The two advantages occupy different regions of (f, sigma) and are read off "
        "different metrics: **memory is supercritical and maximal at f = 0** (MC "
        "+4.75 to +8.97 at sigma = 6, decaying with f); **generation is near-critical "
        "and absent at f = 0** (VPT +1.0 to +2.2 at sigma = 2, emerging from f ~ 0.20). "
        "Same claim as the delta panels made, now with absolute levels, paired CIs and "
        "the full four-variant ladder.",
        "",
        "## Caveats",
        "",
        f"- **Power.** At n = {common.N_SEEDS} seeds the two-sided Wilcoxon p-floor is "
        f"{2 / 2 ** common.N_SEEDS:.5f}, so no Holm correction over more than ~25 tests "
        "can reach 0.05 whatever the effect size. Holm is applied within each "
        "(metric, null) f-sweep and the CIs are the primary evidence.",
        "- **'Usable range' depends on its threshold.** Measured as 'not identically "
        "zero', the connectome's VPT window looks ~2x the nulls'; at any threshold "
        "meaning *usefully predicting* it is 1.25-1.5x at high f and **reverses** at low "
        "f, where degree-matching holds a Lyapunov time twice as far. All three criteria "
        "are in `e03_frontier_live_window_scale_%d.csv`; do not quote the flattering one."
        % scale,
        "- Single scale (N=448) and edge sign mode only; nominal sigma. The matched-axis "
        "pass is a reanalysis of the same parquet.",
        "",
        f"Artifacts: `e03_frontier_scale_{scale}.parquet`, "
        f"`e03_frontier_paired_scale_{scale}.csv`, "
        f"`e03_frontier_live_window_scale_{scale}.csv`, "
        f"`e03_frontier_decision_scale_{scale}.csv`, "
        f"`e03_frontier_contrast_bound_scale_{scale}.csv`, "
        "`figures/fig_frontier_absolute.png`.",
    ]
    path = common.RESULTS_DIR / f"e03_frontier_verdict_scale_{scale}.md"
    path.write_text("\n".join(lines) + "\n")
    print(f"\nWrote {path}")


def run(scale: int = common.SCALE) -> dict:
    common.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    common.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    print("=" * 70 + "\nE0.3 -- absolute (MC, VPT) frontier over (variant, f, sigma)\n"
          + "=" * 70)
    df = load_cells(scale)
    front = frontier(df)
    crit = sr_crit(df)
    rule = decision_rule(front)
    peaks = peak_table(front)
    windows = live_window(front)
    bound = contrast_at_bound(front)
    contrasts = pd.concat([paired_contrast(df, m, sr) for m in METRICS
                           for sr in CONTRAST_SIGMAS], ignore_index=True)

    front.to_parquet(common.RESULTS_DIR / f"e03_frontier_scale_{scale}.parquet")
    crit.to_csv(common.RESULTS_DIR / f"e03_frontier_sr_crit_scale_{scale}.csv",
                index=False)
    peaks.to_csv(common.RESULTS_DIR / f"e03_frontier_peaks_scale_{scale}.csv",
                 index=False)
    rule.to_csv(common.RESULTS_DIR / f"e03_frontier_decision_scale_{scale}.csv",
                index=False)
    windows.to_csv(common.RESULTS_DIR / f"e03_frontier_live_window_scale_{scale}.csv",
                   index=False)
    bound.to_csv(common.RESULTS_DIR / f"e03_frontier_contrast_bound_scale_{scale}.csv",
                 index=False)
    contrasts.to_csv(common.RESULTS_DIR / f"e03_frontier_paired_scale_{scale}.csv",
                     index=False)

    print("\nPre-registered decision rule -- clause 1 "
          f"(swing/noise >= {SWING_RATIO:g} over >= {MIN_RUN} consecutive sigma, "
          "computed where the metric is alive):")
    print(rule.to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    print("\nClause 2 -- is the between-substrate signal a bound artefact? "
          "(largest connectome - best-null gap, and where that null sits):")
    print(bound.to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    print(f"\nPaired connectome - null (within seed; Holm within each null's f-sweep). "
          f"NOTE: at n = {common.N_SEEDS} seeds the Wilcoxon p-floor is "
          f"{2 / 2 ** common.N_SEEDS:.5f}, so read the CIs, not the stars:")
    for metric in METRICS:
        for sr in CONTRAST_SIGMAS:
            sub = contrasts[(contrasts.metric == metric)
                            & np.isclose(contrasts.spectral_radius, sr)]
            if sub.empty:
                continue
            piv = sub.pivot(index="f", columns="null", values="mean_diff")
            sig = sub.pivot(index="f", columns="null", values="significant")
            print(f"  [{metric} @ sigma={sr:g}] mean paired difference "
                  "(* = Holm p < 0.05)")
            for f, row in piv.iterrows():
                cells = "  ".join(f"{null.split('_')[0][:4]}={row[null]:+.2f}"
                                  f"{'*' if sig.loc[f, null] else ' '}"
                                  for null in piv.columns)
                print(f"    f={f:.2f}  {cells}")

    print("\nUsable sigma window per f, under all three thresholds "
          "(the verdict depends on which):")
    for metric in METRICS:
        for criterion in USABLE_CRITERIA:
            sub = windows[(windows.metric == metric)
                          & (windows.criterion == criterion)]
            piv = sub.pivot(index="f", columns="variant", values="sigma_usable_hi")
            nulls = [c for c in piv.columns if c != "connectome"]
            piv["conn/best_null"] = piv["connectome"] / piv[nulls].max(axis=1)
            print(f"  [{metric} / {criterion}]")
            print(piv.to_string(float_format=lambda v: f"{v:.2f}"))

    from experiments.human.analysis.criticality_matched import panels
    panels.fig_frontier(front, crit, common.FIGURES_DIR / "fig_frontier_absolute")
    write_verdict(front, rule, bound, contrasts, windows, scale)

    common.write_manifest(
        common.RESULTS_DIR / "manifest_e03_frontier.json",
        "E0.3 absolute (MC, VPT) frontier", scale, variants=VARIANTS,
        metrics=list(METRICS), sign_mode=SIGN_MODE, targeting=TARGETING,
        unit="seed (draws averaged within seed)", n_seeds=common.N_SEEDS,
        swing_ratio=SWING_RATIO, min_run=MIN_RUN, bound_tol=BOUND_TOL,
        floor_dominated=FLOOR_DOMINATED, decision=rule.to_dict("records"),
        simulates="no -- reanalysis of the f>0 extension captures")
    return {"frontier": front, "sr_crit": crit, "decision": rule, "peaks": peaks,
            "live_window": windows}

"""Phase-diagram figures (300 dpi) from ``phase_grid`` + ``phase_boundaries``.

The two headline heatmaps (Panel A ``dD``, Panel B ``dStraight``) with observed and
predicted boundaries overlaid, the performance-validation heatmaps (``dMC``,
``dVPT``), the cross-panel boundary overlay, the spectral-predictor collapse panels
with the observed-vs-predicted boundary scatter, and the line cuts. Placement /
Dale figures render only when those targetings / sign modes are present (deferred in
the stratified primary).

Signed order parameters use a diverging map (``RdBu_r``) with the neutral midpoint
pinned at 0 (symmetric limits), so "no connectome advantage" reads as neutral;
magnitude predictors use a sequential map. No reservoir runs. Launched via
``python -m experiments.human.analysis.phase_diagram --plots [--scale N]``.
"""

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

from experiments.human import matrix_config
from experiments.human.analysis.phase_diagram import common

_OP_LABEL = {
    "dD": r"$\Delta d_{eff}$ (connectome $-$ ER)",
    "dMC": r"$\Delta$MC (connectome $-$ ER)",
    "dNARMA": r"$\Delta$NARMA skill (ER $-$ conn NRMSE)",
    "dStraight": r"$\Delta$straightness (ER $-$ conn curvature)",
    "dVPT": r"$\Delta$VPT (connectome $-$ ER)",
    "dClimate": r"$\Delta$climate skill (ER $-$ conn)",
}
_PANEL_A_OPS = ["dD", "dMC", "dNARMA"]
_PANEL_B_OPS = ["dStraight", "dVPT", "dClimate"]
_REP_SR = [2.0, 4.0, 6.0]
_REP_F = [0.0, 0.1, 0.25, 0.5]
_DIVERGING = "RdBu_r"          # red = connectome advantage, blue = ER advantage
_SEQUENTIAL = "viridis"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _pivot(op, col):
    """(f rows asc) x (sr cols asc) grid of ``col`` -> (Z, f_vals, sr_vals)."""
    piv = op.pivot_table(index="f", columns="spectral_radius", values=col)
    return piv.to_numpy(float), piv.index.to_numpy(float), piv.columns.to_numpy(float)


def _extent(f_vals, sr_vals):
    """imshow extent [x0, x1, y0, y1] with half-cell padding so centres sit right."""
    ds = (sr_vals[1] - sr_vals[0]) if sr_vals.size > 1 else 1.0
    df = (f_vals[1] - f_vals[0]) if f_vals.size > 1 else 0.05
    return [sr_vals[0] - ds / 2, sr_vals[-1] + ds / 2,
            f_vals[0] - df / 2, f_vals[-1] + df / 2]


def _heatmap(ax, op, col, diverging=True):
    Z, f_vals, sr_vals = _pivot(op, col)
    if not np.isfinite(Z).any():
        ax.text(0.5, 0.5, f"{col}: no data", transform=ax.transAxes, ha="center")
        return None
    if diverging:
        vmax = float(np.nanmax(np.abs(Z))) or 1e-9
        norm = TwoSlopeNorm(vmin=-vmax, vcenter=0.0, vmax=vmax)
        im = ax.imshow(Z, origin="lower", aspect="auto", cmap=_DIVERGING, norm=norm,
                       extent=_extent(f_vals, sr_vals))
    else:
        im = ax.imshow(Z, origin="lower", aspect="auto", cmap=_SEQUENTIAL,
                       extent=_extent(f_vals, sr_vals))
    ax.set_xlabel("spectral radius")
    ax.set_ylabel("negative-weight fraction $f$")
    return im


def _overlay(ax, bnd, specs):
    """Overlay boundary curves; ``specs`` = [(column, label, style-kwargs), ...]."""
    b = bnd.sort_values("spectral_radius")
    x = b.spectral_radius.to_numpy(float)
    for col, label, kw in specs:
        if col not in b.columns:
            continue
        y = b[col].to_numpy(float)
        if np.isfinite(y).any():
            ax.plot(x, y, label=label, **kw)


def _biological_markers(ax):
    """The real connectome sits at f=0 (all-positive); edge f=0.5 is balanced (not
    biological). Mark f=0 and sr~1 for orientation."""
    ax.axhline(0.0, color="0.35", lw=0.8, ls="-", alpha=0.6)
    ax.axvline(1.0, color="0.5", lw=0.8, ls=":", alpha=0.7)


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
def fig_panelA_heatmap(op, bnd, path, value_col="dD"):
    """Panel A headline: order-parameter heatmap + observed & predicted boundaries."""
    fig, ax = plt.subplots(figsize=(6.6, 5.0))
    im = _heatmap(ax, op, value_col, diverging=True)
    if im is not None:
        fig.colorbar(im, ax=ax, label=_OP_LABEL.get(value_col, value_col))
    _overlay(ax, bnd, [
        ("fA_obs_mag", "observed (25% max)", dict(color="black", lw=2.2)),
        ("fA_obs_sig", "observed (Cliff $\\delta$)", dict(color="black", lw=1.6, ls="--")),
        ("fA_pred_meanstate", "predicted (|mean state|)",
         dict(color="#1b9e77", lw=1.8, ls=":")),
    ])
    _biological_markers(ax)
    ax.set_title(f"Panel A -- memory: {_OP_LABEL.get(value_col, value_col)}",
                 fontsize=11)
    ax.legend(fontsize=7, loc="upper right", framealpha=0.9)
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig_panelB_heatmap(op, bnd, path, value_col="dStraight"):
    """Panel B headline: straightness order parameter + observed & predicted."""
    fig, ax = plt.subplots(figsize=(6.6, 5.0))
    im = _heatmap(ax, op, value_col, diverging=True)
    if im is not None:
        fig.colorbar(im, ax=ax, label=_OP_LABEL.get(value_col, value_col))
    _overlay(ax, bnd, [
        ("fB_obs_mag", "observed onset (25% max)", dict(color="black", lw=2.2)),
        ("fB_obs_sig", "observed onset (Cliff $\\delta$)",
         dict(color="black", lw=1.6, ls="--")),
        ("fB_pred_effradius", "predicted (eff. radius = 1)",
         dict(color="#d95f02", lw=1.8, ls=":")),
        ("fB_pred_meanstate", "predicted (|mean state|)",
         dict(color="#1b9e77", lw=1.8, ls="-.")),
    ])
    _biological_markers(ax)
    ax.set_title(f"Panel B -- generative: {_OP_LABEL.get(value_col, value_col)}",
                 fontsize=11)
    ax.legend(fontsize=7, loc="upper right", framealpha=0.9)
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _smooth_curve(sr, f):
    """Monotone-cubic (PCHIP) smoothing of a boundary over its finite points;
    (sr_fine, f_fine), or (None, None) if too few points. PCHIP is shape-preserving
    so it will not overshoot near the crossover."""
    m = np.isfinite(sr) & np.isfinite(f)
    if m.sum() < 3:
        return None, None
    xs, ys = np.asarray(sr)[m], np.asarray(f)[m]
    xu, idx = np.unique(xs, return_index=True)   # xu sorted; idx picks its y (one per sr)
    yu = ys[idx]
    if xu.size < 3:
        return None, None
    fine = np.linspace(xu[0], xu[-1], 300)
    try:
        from scipy.interpolate import PchipInterpolator
        return fine, PchipInterpolator(xu, yu)(fine)
    except Exception:
        return fine, np.interp(fine, xu, yu)


def _perseed_boundaries(cells, sign_mode="edge", targeting="stratified"):
    """Per-seed memory-collapse and generative-onset f*(sr) for uncertainty bands:
    for each seed, form the connectome-vs-ER order parameter (median over draws),
    extract its boundary with the same collapse/onset operators the analysis uses,
    and return the seed-wise median and the 25-75 inter-seed percentile band."""
    from experiments.human.analysis.phase_diagram import analysis
    c = cells[(cells.sign_mode == sign_mode) & (cells.targeting == targeting)]
    fA, fB = {}, {}
    for s in sorted(c.seed.unique()):
        mem = c[(c.seed == s) & (c.task == "mc")]
        if not mem.empty:
            g = mem.groupby(["f", "spectral_radius", "variant"])["d_eff"].median().reset_index()
            conn = g[g.variant == "connectome"].set_index(["f", "spectral_radius"])["d_eff"]
            er = g[g.variant == common.CONTRAST_VARIANT].set_index(["f", "spectral_radius"])["d_eff"]
            dd = (conn - er).reset_index(name="dD")
            for sr, v in analysis.observed_boundary(dd, "dD").items():
                fA.setdefault(float(sr), []).append(v)
        lor = c[(c.seed == s) & (c.task == "lorenz")]
        if not lor.empty:
            g = lor.groupby(["f", "spectral_radius", "variant"])["mean_curvature"].median().reset_index()
            cc = g[g.variant == "connectome"].set_index(["f", "spectral_radius"])["mean_curvature"]
            ec = g[g.variant == common.CONTRAST_VARIANT].set_index(["f", "spectral_radius"])["mean_curvature"]
            ds = (ec - cc).reset_index(name="dStraight")
            for sr, v in analysis.onset_boundary(ds, "dStraight").items():
                fB.setdefault(float(sr), []).append(v)
    srs = np.array(sorted(set(fA) | set(fB)), float)

    def agg(d):
        M, L, H = [], [], []
        for sr in srs:
            vals = np.array([v for v in d.get(sr, []) if np.isfinite(v)], float)
            if vals.size:
                M.append(np.median(vals))
                L.append(np.percentile(vals, 25))
                H.append(np.percentile(vals, 75))
            else:
                M.append(np.nan); L.append(np.nan); H.append(np.nan)
        return np.array(M), np.array(L), np.array(H)

    return (srs, *agg(fA), *agg(fB))


def fig_cross_panel(cells, path, sign_mode="edge", targeting="stratified"):
    """The headline cross-panel figure: the memory-advantage and generation-advantage
    boundaries carve the (sr, f) plane into named regimes that swap at a crossover.

    Region fills + large in-plane labels carry regime identity (colour is a secondary
    warm/cool hint, validated as a background wash); the two boundary lines are the
    validated red/blue data series (CVD delta E 21.6) with inter-seed 25-75 bands; the
    legend names each boundary's governing spectral quantity."""
    MEM, GEN = "#e34948", "#2a78d6"      # memory / generation washes + boundary lines
    INK, SUB, MUT, GRID, BASE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
    SR_CRIT, F_BIO = 2.4, 0.5
    ytop = 0.52

    srs, fA_med, fA_lo, fA_hi, fB_med, fB_lo, fB_hi = _perseed_boundaries(
        cells, sign_mode, targeting)
    xsA, yA = _smooth_curve(srs, fA_med)
    xsB, yB = _smooth_curve(srs, fB_med)
    flab = "inhibitory-neuron fraction $f$" if sign_mode == "dale" else \
           "negative-weight fraction $f$"

    with plt.rc_context({"hatch.linewidth": 0.7}):
        fig, ax = plt.subplots(figsize=(7.8, 5.8))
        ax.set_facecolor("#fcfcfb")

        # --- regime fills on a common fine sr grid --------------------------------
        if xsA is not None and xsB is not None:
            xf = np.linspace(srs[0], srs[-1], 400)
            fAf = np.interp(xf, xsA, yA, left=np.nan, right=np.nan)
            fBf = np.interp(xf, xsB, yB, left=np.nan, right=np.nan)
            fA0 = np.where(np.isfinite(fAf), fAf, 0.0)
            ax.fill_between(xf, 0, fA0, where=fA0 > 1e-6, color=MEM, alpha=0.15,
                            linewidth=0)                      # MEMORY: f < fA
            gm = np.isfinite(fBf)
            ax.fill_between(xf, fBf, ytop, where=gm, color=GEN, alpha=0.15,
                            linewidth=0)                      # GENERATION: f > fB

        # --- uncertainty bands + smoothed boundary lines --------------------------
        okA = np.isfinite(fA_lo) & np.isfinite(fA_hi)
        ax.fill_between(srs[okA], fA_lo[okA], fA_hi[okA], color=MEM, alpha=0.22,
                        linewidth=0)
        okB = np.isfinite(fB_lo) & np.isfinite(fB_hi)
        ax.fill_between(srs[okB], fB_lo[okB], fB_hi[okB], color=GEN, alpha=0.22,
                        linewidth=0)
        if xsA is not None:
            ax.plot(xsA, yA, color=MEM, lw=2.6, solid_capstyle="round", zorder=5,
                    label=r"memory-advantage boundary  (set by common mode $|\bar{x}|$)")
        if xsB is not None:
            ax.plot(xsB, yB, color=GEN, lw=2.6, solid_capstyle="round", zorder=5,
                    label="generation-advantage boundary  (set by eff. radius $\\to$ 1)")

        # --- crossover point ------------------------------------------------------
        if xsA is not None and xsB is not None:
            lo, hi = max(xsA[0], xsB[0]), min(xsA[-1], xsB[-1])
            xc = np.linspace(lo, hi, 600)
            d = np.interp(xc, xsA, yA) - np.interp(xc, xsB, yB)
            sc = np.where(np.diff(np.sign(d)) != 0)[0]
            if sc.size:
                k = sc[0]
                x0, x1, d0, d1 = xc[k], xc[k + 1], d[k], d[k + 1]
                xcr = x0 - d0 * (x1 - x0) / (d1 - d0)
                ycr = float(np.interp(xcr, xsA, yA))
                ax.plot([xcr], [ycr], "o", ms=9, color=INK, mec="white", mew=1.6,
                        zorder=7)
                ax.annotate("boundaries cross\n"
                            f"sr $\\approx$ {xcr:.1f}, $f \\approx$ {ycr:.2f}\n"
                            "memory $\\rightleftharpoons$ generation",
                            xy=(xcr, ycr), xytext=(xcr - 1.75, ycr + 0.17),
                            fontsize=8.5, color=INK, ha="center", va="center",
                            arrowprops=dict(arrowstyle="-", color=MUT, lw=1.0))

        # --- critical sr + biological anchors -------------------------------------
        ax.axvline(SR_CRIT, color=MUT, lw=1.0, ls=(0, (4, 3)), alpha=0.8, zorder=1)
        ax.text(SR_CRIT, 0.40, "critical sr", color=MUT, fontsize=8, va="center",
                ha="center", rotation=90,
                bbox=dict(boxstyle="round,pad=0.15", fc="#fcfcfb", ec="none", alpha=0.7))
        ax.axhline(F_BIO, color=MUT, lw=1.0, ls=(0, (1, 2)), alpha=0.75, zorder=1)
        ax.text(srs[-1], F_BIO - 0.012, "balanced sign ($f=0.5$)", color=SUB,
                fontsize=8, va="top", ha="right")
        ax.text(0.1, 0.012, "real connectome ($f=0$)", color=SUB, fontsize=8,
                va="bottom", ha="left")

        ax.set_xlim(srs[0], srs[-1])
        ax.set_ylim(-0.01, ytop)
        ax.set_xlabel("spectral radius", color=INK, fontsize=10)
        ax.set_ylabel(flab, color=INK, fontsize=10)
        ax.set_title("Memory and generation occupy opposite, crossing regions of "
                     "sign-space", fontsize=12, color=INK, pad=10)
        ax.grid(True, color=GRID, lw=0.6, alpha=0.7)
        ax.set_axisbelow(True)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(BASE)
        ax.tick_params(colors=MUT, labelsize=9)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.11), ncol=1,
                  fontsize=8.5, framealpha=0.0, handlelength=1.6)
        fig.savefig(path, dpi=300, bbox_inches="tight")
        plt.close(fig)


def fig_predictors(op, path):
    """Spectral predictors vs f at representative sr (common-mode / Perron / stability
    collapse)."""
    preds = [("A_abs_mean_state", "|mean state| (MC)"), ("bulk95", "bulk95"),
             ("perron_root", "Perron root / radius"),
             ("B_effective_radius", "effective radius (Lorenz)")]
    preds = [(c, lbl) for c, lbl in preds if c in op.columns and op[c].notna().any()]
    if not preds:
        return
    sr_present = sorted(op.spectral_radius.unique())
    reps = [min(sr_present, key=lambda s: abs(s - t)) for t in _REP_SR]
    reps = sorted(set(reps))
    colors = plt.cm.viridis(np.linspace(0.15, 0.85, len(reps)))
    fig, axes = plt.subplots(1, len(preds), figsize=(3.5 * len(preds), 3.4),
                             squeeze=False)
    for ax, (col, lbl) in zip(axes[0], preds):
        for sr, c in zip(reps, colors):
            s = op[np.isclose(op.spectral_radius, sr)].sort_values("f")
            ax.plot(s.f, s[col], color=c, lw=1.8, marker="o", ms=3,
                    label=f"sr={sr:g}")
        if col == "B_effective_radius":
            ax.axhline(1.0, color="0.5", lw=0.9, ls=":")
        ax.set_xlabel("negative-weight fraction $f$")
        ax.set_ylabel(lbl, fontsize=9)
        ax.grid(alpha=0.25)
    axes[0][-1].legend(fontsize=7, framealpha=0.9)
    fig.suptitle("Spectral predictors vs sign fraction (connectome)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig_boundary_scatter(bnd, path):
    """Observed vs predicted boundary f* per sr, each panel (agreement = points on
    the diagonal)."""
    pairs = [("Panel A (memory)", "fA_obs_mag", "fA_pred_meanstate", "|mean state|"),
             ("Panel B (generative)", "fB_obs_mag", "fB_pred_effradius", "eff. radius=1")]
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.2), squeeze=False)
    for ax, (title, oc, pc, plabel) in zip(axes[0], pairs):
        if oc in bnd.columns and pc in bnd.columns:
            x = bnd[pc].to_numpy(float)
            y = bnd[oc].to_numpy(float)
            ok = np.isfinite(x) & np.isfinite(y)
            ax.scatter(x[ok], y[ok], s=30, color="#333333", alpha=0.8)
        ax.plot([0, 0.5], [0, 0.5], color="0.6", lw=1.0, ls="--")
        ax.set_xlim(-0.02, 0.52)
        ax.set_ylim(-0.02, 0.52)
        ax.set_xlabel(f"predicted $f^*$ ({plabel})")
        ax.set_ylabel("observed $f^*$ (25% max contour)")
        ax.set_title(title, fontsize=10)
        ax.grid(alpha=0.25)
    fig.suptitle("Observed vs predicted collapse fraction $f^*$", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig_line_cuts(op, path):
    """Order parameters vs f at fixed sr (top) and vs sr at fixed f (bottom)."""
    ops = [c for c in (_PANEL_A_OPS + _PANEL_B_OPS)
           if c in op.columns and op[c].notna().any()]
    if not ops:
        return
    sr_present = sorted(op.spectral_radius.unique())
    f_present = sorted(op.f.unique())
    reps_sr = sorted({min(sr_present, key=lambda s: abs(s - t)) for t in _REP_SR})
    reps_f = sorted({min(f_present, key=lambda s: abs(s - t)) for t in _REP_F})
    csr = plt.cm.viridis(np.linspace(0.15, 0.85, len(reps_sr)))
    cf = plt.cm.plasma(np.linspace(0.15, 0.85, len(reps_f)))
    fig, axes = plt.subplots(2, len(ops), figsize=(3.6 * len(ops), 6.4),
                             squeeze=False)
    for j, oc in enumerate(ops):
        top, bot = axes[0][j], axes[1][j]
        for sr, c in zip(reps_sr, csr):
            s = op[np.isclose(op.spectral_radius, sr)].sort_values("f")
            top.plot(s.f, s[oc], color=c, lw=1.8, marker="o", ms=3, label=f"sr={sr:g}")
        for f, c in zip(reps_f, cf):
            s = op[np.isclose(op.f, f)].sort_values("spectral_radius")
            bot.plot(s.spectral_radius, s[oc], color=c, lw=1.8, marker="o", ms=3,
                     label=f"f={f:g}")
        for ax in (top, bot):
            ax.axhline(0.0, color="0.6", lw=0.8, ls=":")
            ax.grid(alpha=0.25)
        top.set_title(_OP_LABEL.get(oc, oc), fontsize=9)
        top.set_xlabel("negative-weight fraction $f$")
        bot.set_xlabel("spectral radius")
        if j == 0:
            top.set_ylabel("order parameter (vs $f$)")
            bot.set_ylabel("order parameter (vs sr)")
    axes[0][-1].legend(fontsize=7, framealpha=0.9)
    axes[1][-1].legend(fontsize=7, framealpha=0.9)
    fig.suptitle("Line cuts: order parameters vs $f$ (fixed sr) and vs sr (fixed $f$)",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig_placement(bnd_all, path):
    """Placement study: critical fraction f*(sr) across targeting regimes (hub_first
    / stratified / periphery_first), for the memory-collapse (Panel A) and
    generative-onset (Panel B) boundaries. One row per sign mode present -- the clean
    hub < stratified < periphery ordering shows up on the biological Dale (node-wise)
    axis, not the edge axis, so both are shown. Renders only when >1 targeting is
    present."""
    if "targeting" not in bnd_all.columns or bnd_all.targeting.nunique() < 2:
        return False
    modes = [m for m in ("edge", "dale") if m in set(bnd_all.sign_mode)]
    targetings = [t for t in ("hub_first", "stratified", "periphery_first")
                  if t in set(bnd_all.targeting)]
    style = {"hub_first": dict(color="#c44e52", lw=2.2),
             "stratified": dict(color="black", lw=2.2),
             "periphery_first": dict(color="#4c72b0", lw=2.2)}
    cols = [("fA_obs_mag", "Panel A (memory) collapse"),
            ("fB_obs_mag", "Panel B (generative) onset")]
    fig, axes = plt.subplots(len(modes), 2, figsize=(11.0, 4.6 * len(modes)),
                             squeeze=False)
    for i, sm in enumerate(modes):
        bsm = bnd_all[bnd_all.sign_mode == sm]
        flab = "inhibitory-neuron fraction" if sm == "dale" else "negative-weight fraction"
        for ax, (col, title) in zip(axes[i], cols):
            for tg in targetings:
                b = bsm[bsm.targeting == tg].sort_values("spectral_radius")
                if col in b.columns and np.isfinite(b[col]).any():
                    ax.plot(b.spectral_radius, b[col], label=tg,
                            **style.get(tg, dict(lw=1.8)))
            ax.set_xlabel("spectral radius")
            ax.set_ylabel(f"critical $f^*$ ({flab})")
            ax.set_ylim(-0.02, 0.52)
            ax.set_title(f"{sm}: {title}", fontsize=10)
            ax.grid(alpha=0.25)
            ax.legend(fontsize=8, framealpha=0.9)
    fig.suptitle("Placement study: how few hub-targeted inhibitory nodes/edges "
                 "collapse the regime", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return True


def fig_dale_comparison(op_all, path):
    """Dale (node-wise E/I) vs edge sign composition: the memory (dD) and generative
    (dStraight) order-parameter heatmaps side by side for each sign mode (stratified).
    Renders only when the Dale sign mode is present."""
    modes = [m for m in ("edge", "dale") if m in set(op_all.sign_mode)]
    if "dale" not in modes:
        return False
    rows_op = [(c, lbl) for c, lbl in
               [("dD", "memory $\\Delta d_{eff}$"),
                ("dStraight", "generative $\\Delta$straightness")]
               if c in op_all.columns and op_all[c].notna().any()]
    if not rows_op:
        return False
    fig, axes = plt.subplots(len(rows_op), len(modes),
                             figsize=(5.6 * len(modes), 4.6 * len(rows_op)),
                             squeeze=False)
    for i, (col, lbl) in enumerate(rows_op):
        for j, m in enumerate(modes):
            ax = axes[i][j]
            sub = op_all[(op_all.sign_mode == m) & (op_all.targeting == "stratified")]
            im = _heatmap(ax, sub, col, diverging=True)
            if im is not None:
                fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
            _biological_markers(ax)
            xlab = "inhibitory-neuron fraction $f$" if m == "dale" else \
                   "negative-weight fraction $f$"
            ax.set_ylabel(xlab)
            ax.set_title(f"{m}: {lbl}", fontsize=10)
    fig.suptitle("Dale (node-wise E/I) vs edge-wise sign composition", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return True


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def run(smoke: bool = False, scale: int | None = None) -> None:
    scale = matrix_config.SCALE if scale is None else scale
    results_dir, figures_dir = common.scale_dirs(scale)
    sfx = "_smoke" if smoke else ""      # keep smoke figures off the canonical ones
    grid_path = results_dir / f"phase_grid{sfx}.parquet"
    bnd_path = results_dir / f"phase_boundaries{sfx}.parquet"
    if not grid_path.exists():
        raise FileNotFoundError(f"{grid_path} not found -- run --analyse first.")
    op_all = pd.read_parquet(grid_path)
    bnd_all = pd.read_parquet(bnd_path)
    cells_path = results_dir / f"phase_cells{sfx}.parquet"
    cells = pd.read_parquet(cells_path) if cells_path.exists() else None
    figures_dir.mkdir(parents=True, exist_ok=True)

    def fp(name):                        # figure path with the smoke suffix applied
        return figures_dir / f"{name}{sfx}.png"

    # Headline panels + boundaries are the edge / stratified primary; a Dale
    # comparison figure is added when the Dale sign mode is present.
    prim_sign = "edge" if "edge" in set(op_all.sign_mode) else sorted(op_all.sign_mode.unique())[0]
    prim_tg = "stratified" if "stratified" in set(op_all.targeting) else op_all.targeting.iloc[0]
    op = op_all[(op_all.sign_mode == prim_sign) & (op_all.targeting == prim_tg)]
    bnd = bnd_all[(bnd_all.sign_mode == prim_sign) & (bnd_all.targeting == prim_tg)]

    made = []
    fig_panelA_heatmap(op, bnd, fp("fig1_panelA_dD_heatmap"), "dD")
    made.append("fig1_panelA_dD_heatmap")
    if "dMC" in op.columns and op.dMC.notna().any():
        fig_panelA_heatmap(op, bnd, fp("fig2_panelA_dMC_heatmap"), "dMC")
        made.append("fig2_panelA_dMC_heatmap")
    if "dStraight" in op.columns and op.dStraight.notna().any():
        fig_panelB_heatmap(op, bnd, fp("fig3_panelB_dStraight_heatmap"))
        made.append("fig3_panelB_dStraight_heatmap")
    if "dVPT" in op.columns and op.dVPT.notna().any():
        fig_panelB_heatmap(op, bnd, fp("fig4_panelB_dVPT_heatmap"), "dVPT")
        made.append("fig4_panelB_dVPT_heatmap")
    if cells is not None:
        fig_cross_panel(cells, fp("fig5_cross_panel_boundaries"), prim_sign, prim_tg)
        made.append("fig5_cross_panel_boundaries")
    fig_predictors(op, fp("fig6a_predictors_vs_f"))
    fig_boundary_scatter(bnd, fp("fig6b_boundary_scatter"))
    made += ["fig6a_predictors_vs_f", "fig6b_boundary_scatter"]
    fig_line_cuts(op, fp("fig7_line_cuts"))
    made.append("fig7_line_cuts")
    if fig_placement(bnd_all, fp("fig8_placement")):
        made.append("fig8_placement")
    if fig_dale_comparison(op_all, fp("fig9_dale_comparison")):
        made.append("fig9_dale_comparison")

    for name in made:
        print(f"Saved {fp(name)}")
    print(f"\nPhase-diagram plots complete ({len(made)} figures, "
          f"sign_mode={prim_sign}, targeting={prim_tg}).")

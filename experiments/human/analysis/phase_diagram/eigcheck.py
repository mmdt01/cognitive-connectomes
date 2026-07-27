"""Eigenvector-centrality robustness check for the placement study.

The headline placement result (``hub_first < stratified < periphery_first``, with
hub targeting ~2x more efficient at collapsing the memory regime on the Dale axis)
used endpoint **degree** to define a "hub". This module tests whether that result
survives when "hub" is defined by **eigenvector centrality** instead -- a score
closer to what actually moves the leading eigenvalue.

It is a self-contained side analysis: it reads the committed degree headline cells
(``phase_cells.parquet``) and the score-tagged robustness run
(``phase_cells_eigenvector.parquet``), reuses the analysis boundary operators
unchanged, and writes ``fig10_eigenvector_check.png`` + ``phase_eigcheck_summary.md``.
The main capture -> analyse -> plots pipeline is untouched.

    python -m experiments.human.analysis.phase_diagram --eigcheck [--scale N]
"""

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from experiments.human import matrix_config
from experiments.human.analysis.phase_diagram import common, analysis

_TARG = {"hub_first": "#c44e52", "stratified": "#0b0b0b", "periphery_first": "#4c72b0"}
_INK, _MUT, _GRID = "#0b0b0b", "#898781", "#e1e0d9"
_SUPERCRIT = 3.0


def _boundaries(cells: pd.DataFrame) -> dict:
    """Per (sign_mode, targeting): (fA, fB) boundary dicts sr->f*, where fA is the
    memory-collapse boundary (dD) and fB the generative-onset boundary (dStraight),
    computed with the same operators the main analysis uses."""
    op = analysis.order_parameters(analysis.cell_medians(cells))
    out = {}
    for (sm, tg), g in op.groupby(["sign_mode", "targeting"]):
        out[(sm, tg)] = (analysis.observed_boundary(g, "dD"),
                         analysis.onset_boundary(g, "dStraight"))
    return out


def _mean_supercrit(fdict: dict) -> float:
    vals = [v for sr, v in fdict.items() if sr >= _SUPERCRIT and np.isfinite(v)]
    return float(np.mean(vals)) if vals else float("nan")


def _fig10(deg: dict, eig: dict, path) -> None:
    modes = [m for m in ("edge", "dale") if any(sm == m for sm, _ in deg)]
    panels = [(0, "memory-collapse $f^*$ (dD)"),
              (1, "generative-onset $f^*$ (dStraight)")]
    scores = [("degree", deg, "-"), ("eigenvector", eig, (0, (5, 2)))]
    fig, axes = plt.subplots(len(panels), len(modes),
                             figsize=(5.6 * len(modes), 4.6 * len(panels)),
                             squeeze=False)
    for i, (idx, ylab) in enumerate(panels):
        for j, sm in enumerate(modes):
            ax = axes[i][j]
            for _, bnds, ls in scores:
                for tg, col in _TARG.items():
                    d = bnds.get((sm, tg))
                    if d is None:
                        continue
                    fdict = d[idx]
                    srs = np.array(sorted(fdict), float)
                    ys = np.array([fdict[s] for s in srs], float)
                    ax.plot(srs, ys, ls=ls, color=col, lw=2.1, solid_capstyle="round")
            ax.set_xlabel("spectral radius", color=_INK)
            ax.set_ylabel(f"critical $f^*$ ({ylab})", color=_INK, fontsize=9)
            ax.set_ylim(-0.02, 0.52)
            ax.set_title(f"{sm}: {ylab}", fontsize=10, color=_INK)
            ax.grid(True, color=_GRID, lw=0.6, alpha=0.7)
            ax.set_axisbelow(True)
            for sp in ("top", "right"):
                ax.spines[sp].set_visible(False)
    # combined legend: colour = targeting, linestyle = score
    handles = [Line2D([0], [0], color=c, lw=2.4, label=t) for t, c in _TARG.items()]
    handles += [Line2D([0], [0], color=_MUT, lw=2.0, ls="-", label="degree score"),
                Line2D([0], [0], color=_MUT, lw=2.0, ls=(0, (5, 2)),
                       label="eigenvector score")]
    fig.legend(handles=handles, loc="lower center", ncol=5, fontsize=8.5,
               frameon=False, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("Placement robustness: degree vs eigenvector-centrality score",
                 fontsize=12, color=_INK)
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {path}")


def _summary(deg: dict, eig: dict, path) -> None:
    modes = [m for m in ("edge", "dale") if any(sm == m for sm, _ in deg)]
    order = ["hub_first", "stratified", "periphery_first"]
    lines = ["# Placement robustness: degree vs eigenvector-centrality score\n",
             "Memory-collapse `f*` (mean over supercritical sr >= 3); the placement "
             "claim is `hub_first < stratified < periphery_first`.\n",
             "| sign_mode | score | hub_first | stratified | periphery_first | "
             "hub<strat<peri |", "|---|---|---|---|---|---|"]
    for sm in modes:
        for label, bnds in [("degree", deg), ("eigenvector", eig)]:
            vals = {tg: _mean_supercrit(bnds.get((sm, tg), ({}, {}))[0]) for tg in order}
            ok = (np.isfinite(list(vals.values())).all()
                  and vals["hub_first"] < vals["stratified"] < vals["periphery_first"])
            cells = " | ".join(f"{vals[t]:.3f}" if np.isfinite(vals[t]) else "--"
                               for t in order)
            lines.append(f"| {sm} | {label} | {cells} | {'yes' if ok else 'no'} |")
    lines.append("")
    path.write_text("\n".join(lines) + "\n")
    print(f"Saved {path}")
    print("\n".join(lines[3:]))


def run(smoke: bool = False, scale: int | None = None) -> None:
    scale = matrix_config.SCALE if scale is None else scale
    results_dir, figures_dir = common.scale_dirs(scale)
    sfx = "_smoke" if smoke else ""
    deg_path = results_dir / f"phase_cells{sfx}.parquet"
    eig_path = results_dir / f"phase_cells_eigenvector{sfx}.parquet"
    for p, how in [(deg_path, "--capture"),
                   (eig_path, "--capture --score eigenvector")]:
        if not p.exists():
            raise FileNotFoundError(f"{p} not found -- run `{how}` first.")
    deg = _boundaries(pd.read_parquet(deg_path))
    eig = _boundaries(pd.read_parquet(eig_path))
    print(f"Eigenvector robustness check: degree {len(deg)} + eigenvector {len(eig)} "
          "(sign_mode, targeting) groups")
    figures_dir.mkdir(parents=True, exist_ok=True)
    _fig10(deg, eig, figures_dir / f"fig10_eigenvector_check{sfx}.png")
    _summary(deg, eig, results_dir / f"phase_eigcheck_summary{sfx}.md")
    print("\nEigenvector robustness check complete.")
